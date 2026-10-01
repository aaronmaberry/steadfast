"use strict";

var CHECKOUT_CONFIG_URL = "https://www.walksteadfast.com/api/checkout-config";

// Store builds ship with an empty list. Purchase UI stays hidden on every platform.
var PURCHASE_PLATFORM_ALLOWLIST = Object.freeze([]);

function normalizeCheckout(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    return { mode: "closed" };
  }
  if (payload.mode === "live") return { mode: "live" };
  if (payload.mode === "test") return { mode: "test" };
  return { mode: "closed" };
}

function purchaseUiAllowed(checkout, platform, allowlist) {
  var list = allowlist === undefined ? PURCHASE_PLATFORM_ALLOWLIST : allowlist;
  if (!checkout || checkout.mode !== "live") return false;
  if (typeof platform !== "string" || platform.length === 0) return false;
  if (!Array.isArray(list)) return false;
  return list.indexOf(platform) !== -1;
}

function resolvePurchaseGate(payload, platform, failed, allowlist) {
  if (failed) {
    return { mode: "closed", purchasesAllowed: false };
  }
  var checkout = normalizeCheckout(payload);
  return {
    mode: checkout.mode,
    purchasesAllowed: purchaseUiAllowed(checkout, platform, allowlist)
  };
}

function isStripeBuyUrl(url) {
  return typeof url === "string" && url.indexOf("buy.stripe.com") !== -1;
}

function canOpenExternalUrl(url) {
  if (typeof url !== "string" || url.length === 0) return false;
  if (isStripeBuyUrl(url)) return false;
  return true;
}

function loadPurchaseGate(options) {
  var settings = options || {};
  var fetchImpl = settings.fetchImpl || global.fetch;
  var platform = settings.platform;
  var allowlist = settings.allowlist;

  return Promise.resolve()
    .then(function () {
      return fetchImpl(CHECKOUT_CONFIG_URL, { method: "GET" });
    })
    .then(function (response) {
      if (!response || response.ok !== true || typeof response.json !== "function") {
        return resolvePurchaseGate(null, platform, true, allowlist);
      }
      return Promise.resolve()
        .then(function () {
          return response.json();
        })
        .then(
          function (payload) {
            return resolvePurchaseGate(payload, platform, false, allowlist);
          },
          function () {
            return resolvePurchaseGate(null, platform, true, allowlist);
          }
        );
    })
    .catch(function () {
      return resolvePurchaseGate(null, platform, true, allowlist);
    });
}

module.exports = {
  CHECKOUT_CONFIG_URL: CHECKOUT_CONFIG_URL,
  PURCHASE_PLATFORM_ALLOWLIST: PURCHASE_PLATFORM_ALLOWLIST,
  normalizeCheckout: normalizeCheckout,
  purchaseUiAllowed: purchaseUiAllowed,
  resolvePurchaseGate: resolvePurchaseGate,
  isStripeBuyUrl: isStripeBuyUrl,
  canOpenExternalUrl: canOpenExternalUrl,
  loadPurchaseGate: loadPurchaseGate
};
