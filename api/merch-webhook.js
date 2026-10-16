// Stripe webhook: checkout.session.completed -> Printful order (v1 /orders).
// INERT unless MERCH_LIVE === "true". PRINTFUL_CONFIRM !== "true" creates DRAFT orders only (no charge to card on file).
var crypto = require("crypto");
var catalog = require("../merch/catalog.json");


function rawBody(req) {
  return new Promise(function (ok, bad) {
    var c = []; req.on("data", function (d) { c.push(d); }); req.on("end", function () { ok(Buffer.concat(c)); }); req.on("error", bad);
  });
}

function verify(buf, header, secret) {
  if (!header || !secret) return false;
  var parts = {}; header.split(",").forEach(function (kv) { var i = kv.indexOf("="); (parts[kv.slice(0, i)] = parts[kv.slice(0, i)] || []).push(kv.slice(i + 1)); });
  var t = parts.t && parts.t[0]; if (!t || Math.abs(Date.now() / 1000 - Number(t)) > 300) return false;
  var exp = crypto.createHmac("sha256", secret).update(t + "." + buf.toString("utf8")).digest("hex");
  return (parts.v1 || []).some(function (s) { return s.length === exp.length && crypto.timingSafeEqual(Buffer.from(s), Buffer.from(exp)); });
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();
  var buf = await rawBody(req);
  if (!verify(buf, req.headers["stripe-signature"], process.env.STRIPE_MERCH_WEBHOOK_SECRET)) return res.status(400).end();
  var evt = JSON.parse(buf.toString("utf8"));
  if (evt.type !== "checkout.session.completed") return res.status(200).json({ ignored: evt.type });
  if (process.env.MERCH_LIVE !== "true") return res.status(200).json({ skipped: "MERCH_LIVE off" });

  var s = evt.data.object, m = s.metadata || {};
  if (!m.merch_sku) return res.status(200).json({ ignored: "not merch" });
  var item = catalog.items[m.merch_sku], v = item && item.variants[m.merch_variant];
  if (!v || !v.printful_sync_variant_id) return res.status(500).json({ error: "unmapped variant" }); // Stripe retries; fix mapping
  var sh = (s.collected_information && s.collected_information.shipping_details) || s.shipping_details || {};
  var a = sh.address || {}, cd = s.customer_details || {};

  var order = {
    external_id: s.id.replace(/[^A-Za-z0-9_-]/g, "").slice(-32), // idempotency: Printful rejects duplicate external_id
    shipping: "STANDARD",
    recipient: { name: sh.name || cd.name, address1: a.line1, address2: a.line2 || "", city: a.city, state_code: a.state || "", country_code: a.country, zip: a.postal_code, email: cd.email, phone: cd.phone || "" },
    items: [{ sync_variant_id: v.printful_sync_variant_id, quantity: Number(m.merch_qty) || 1 }],
    retail_costs: { currency: "USD", subtotal: (s.amount_subtotal / 100).toFixed(2), shipping: ((s.total_details && s.total_details.amount_shipping || 0) / 100).toFixed(2), tax: ((s.total_details && s.total_details.amount_tax || 0) / 100).toFixed(2) }
  };
  var url = "https://api.printful.com/orders" + (process.env.PRINTFUL_CONFIRM === "true" ? "?confirm=true" : "");
  var r = await fetch(url, { method: "POST", headers: { Authorization: "Bearer " + process.env.PRINTFUL_API_TOKEN, "Content-Type": "application/json" }, body: JSON.stringify(order) });
  var j = await r.json().catch(function () { return {}; });
  if (r.ok || (j.error && /external/i.test(String(j.error.message)))) return res.status(200).json({ ok: true });
  return res.status(502).json({ error: "printful", code: r.status });
};

module.exports.config = { api: { bodyParser: false } };
