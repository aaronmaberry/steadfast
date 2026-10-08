const crypto = require("crypto");

function enc(value) {
  return encodeURIComponent(value).replace(/[!'()*]/g, (c) => "%" + c.charCodeAt(0).toString(16).toUpperCase());
}

function presign(key, expires) {
  const access = process.env.R2_ACCESS_KEY_ID;
  const secret = process.env.R2_SECRET_ACCESS_KEY;
  const account = process.env.R2_ACCOUNT_ID;
  const bucket = process.env.R2_BUCKET || "steadfast-files";
  const host = account + ".r2.cloudflarestorage.com";
  const now = new Date();
  const amzdate = now.toISOString().replace(/[:-]|\.\d{3}/g, "");
  const datestamp = amzdate.slice(0, 8);
  const credential = [access, datestamp, "auto", "s3", "aws4_request"].join("/");
  const canonicalUri = "/" + bucket + "/" + key.split("/").map(enc).join("/");
  const params = [
    ["X-Amz-Algorithm", "AWS4-HMAC-SHA256"],
    ["X-Amz-Credential", credential],
    ["X-Amz-Date", amzdate],
    ["X-Amz-Expires", String(expires)],
    ["X-Amz-SignedHeaders", "host"],
    ["response-content-disposition", 'attachment; filename="' + key + '"']
  ].sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0);
  const canonicalQuery = params.map(([k, v]) => enc(k) + "=" + enc(v)).join("&");
  const canonicalRequest = [
    "GET",
    canonicalUri,
    canonicalQuery,
    "host:" + host + "\n",
    "host",
    "UNSIGNED-PAYLOAD"
  ].join("\n");
  const scope = datestamp + "/auto/s3/aws4_request";
  const stringToSign = [
    "AWS4-HMAC-SHA256",
    amzdate,
    scope,
    crypto.createHash("sha256").update(canonicalRequest).digest("hex")
  ].join("\n");
  const hmac = (key, data) => crypto.createHmac("sha256", key).update(data).digest();
  const signing = hmac(hmac(hmac(hmac("AWS4" + secret, datestamp), "auto"), "s3"), "aws4_request");
  const signature = crypto.createHmac("sha256", signing).update(stringToSign).digest("hex");
  return "https://" + host + canonicalUri + "?" + canonicalQuery + "&X-Amz-Signature=" + signature;
}

module.exports = (req, res) => {
  if (!process.env.R2_SECRET_ACCESS_KEY) {
    res.status(500).send("File host is not configured.");
    return;
  }
  res.setHeader("Cache-Control", "no-store");
  res.redirect(302, presign("steadfast-men-audiobook.mp3", 600));
};
