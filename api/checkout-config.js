var PRODUCT_URL = /^https:\/\/buy\.stripe\.com\/[A-Za-z0-9_-]+$/;

function paymentLink(name) {
  var raw = process.env[name];
  if (typeof raw !== "string") return "";
  var url = raw.trim();
  return PRODUCT_URL.test(url) ? url : "";
}

function isLive(url) {
  return PRODUCT_URL.test(url) && url.indexOf("/test_") === -1;
}

module.exports = function handler(req, res) {
  if (req.method !== "GET" && req.method !== "HEAD") {
    res.statusCode = 405;
    res.setHeader("Allow", "GET, HEAD");
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ error: "method" }));
    return;
  }

  var ebook = paymentLink("STRIPE_PAYMENT_LINK_EBOOK");
  var training = paymentLink("STRIPE_PAYMENT_LINK_TRAINING");
  var bundle = paymentLink("STRIPE_PAYMENT_LINK_BUNDLE");
  var mode = isLive(ebook) && isLive(training) && isLive(bundle) ? "live" : "test";
  var body = JSON.stringify({
    mode: mode,
    ebook: ebook,
    training: training,
    bundle: bundle
  });

  res.statusCode = 200;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=60, must-revalidate");
  res.setHeader("X-Content-Type-Options", "nosniff");
  if (req.method === "HEAD") {
    res.end();
    return;
  }
  res.end(body);
};
