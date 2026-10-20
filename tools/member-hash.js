// Usage: node tools/member-hash.js 'password'  -> scrypt$salt$hash for MEMBER_ACCOUNTS
const crypto = require("crypto");
const salt = crypto.randomBytes(16);
console.log("scrypt$" + salt.toString("hex") + "$" + crypto.scryptSync(process.argv[2] || "", salt, 32).toString("hex"));
