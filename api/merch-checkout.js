// POST /api/merch-checkout {sku, variant, qty} -> Stripe Checkout Session URL.
// INERT unless MERCH_LIVE === "true" and STRIPE_SECRET_KEY is set. No Stripe SDK; plain REST.
var catalog = require("../merch/catalog.json");

var SHIP_COUNTRIES = ["US","CA","GB","IE","AU","NZ","DE","FR","NL","BE","AT","ES","IT","SE","DK","FI","NO","CH","PT","PL","JP","MX","BR"];
// Flat shipping approved by Aaron 2026-10-16: $5.95 US / $14.99 international (cents).
var SHIP = [
  { label: "Standard (US)", cents: 595, min: 3, max: 8 },
  { label: "Standard (International)", cents: 1499, min: 5, max: 20 }
];

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });
  if (process.env.MERCH_LIVE !== "true" || !process.env.STRIPE_SECRET_KEY) {
    return res.status(503).json({ error: "Merch checkout not enabled" });
  }
  var b = req.body || {};
  var item = catalog.items[b.sku];
  var qty = Math.max(1, Math.min(10, parseInt(b.qty, 10) || 1));
  if (!item || !item.variants[b.variant]) return res.status(400).json({ error: "Unknown item" });

  var p = new URLSearchParams();
  p.append("mode", "payment");
  p.append("success_url", "https://www.walksteadfast.com/merch?ordered=1");
  p.append("cancel_url", "https://www.walksteadfast.com/merch");
  p.append("line_items[0][quantity]", String(qty));
  p.append("line_items[0][price_data][currency]", catalog.currency);
  p.append("line_items[0][price_data][unit_amount]", String(item.price_cents));
  p.append("line_items[0][price_data][product_data][name]", item.name + " (" + b.variant + ")");
  p.append("line_items[0][price_data][product_data][tax_code]", "txcd_99999999");
  p.append("metadata[merch_sku]", b.sku);
  p.append("metadata[merch_variant]", b.variant);
  p.append("metadata[merch_qty]", String(qty));
  p.append("phone_number_collection[enabled]", "true");
  if (process.env.STRIPE_TAX_ENABLED === "true") p.append("automatic_tax[enabled]", "true");
  SHIP_COUNTRIES.forEach(function (c, i) { p.append("shipping_address_collection[allowed_countries][" + i + "]", c); });
  SHIP.forEach(function (s, i) {
    var k = "shipping_options[" + i + "][shipping_rate_data]";
    p.append(k + "[type]", "fixed_amount");
    p.append(k + "[display_name]", s.label);
    p.append(k + "[fixed_amount][amount]", String(s.cents));
    p.append(k + "[fixed_amount][currency]", "usd");
    p.append(k + "[delivery_estimate][minimum][unit]", "business_day");
    p.append(k + "[delivery_estimate][minimum][value]", String(s.min));
    p.append(k + "[delivery_estimate][maximum][unit]", "business_day");
    p.append(k + "[delivery_estimate][maximum][value]", String(s.max));
  });

  var r = await fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: { Authorization: "Bearer " + process.env.STRIPE_SECRET_KEY, "Content-Type": "application/x-www-form-urlencoded" },
    body: p
  });
  var j = await r.json();
  if (!r.ok) return res.status(502).json({ error: "Stripe error" });
  return res.status(200).json({ url: j.url });
};
