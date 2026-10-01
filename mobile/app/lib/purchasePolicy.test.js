"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const policy = require("./purchasePolicy");

const STRIPE = "https://buy.stripe.com/fixture";

test("allowlist ships empty so store platforms never qualify", function () {
  assert.deepEqual(policy.PURCHASE_PLATFORM_ALLOWLIST, []);
  assert.equal(policy.PURCHASE_PLATFORM_ALLOWLIST.includes("ios"), false);
  assert.equal(policy.PURCHASE_PLATFORM_ALLOWLIST.includes("android"), false);
  assert.equal(Object.isFrozen(policy.PURCHASE_PLATFORM_ALLOWLIST), true);
});

test("purchase UI requires live mode and an allowlisted platform", function () {
  assert.equal(policy.purchaseUiAllowed({ mode: "live" }, "ios"), false);
  assert.equal(policy.purchaseUiAllowed({ mode: "live" }, "android"), false);
  assert.equal(policy.purchaseUiAllowed({ mode: "test" }, "ios", ["ios"]), false);
  assert.equal(policy.purchaseUiAllowed({ mode: "live" }, "android", ["ios"]), false);
  assert.equal(policy.purchaseUiAllowed({ mode: "live" }, "ios", ["ios"]), true);
  assert.equal(policy.purchaseUiAllowed(null, "ios", ["ios"]), false);
  assert.equal(policy.purchaseUiAllowed({ mode: "live" }, "", ["ios"]), false);
});

test("fetch failure, bad JSON, and non-live mode stay closed", async function () {
  const failed = await policy.loadPurchaseGate({
    platform: "ios",
    fetchImpl: function () {
      return Promise.reject(new Error("offline"));
    }
  });
  assert.deepEqual(failed, { mode: "closed", purchasesAllowed: false });

  const httpError = await policy.loadPurchaseGate({
    platform: "ios",
    allowlist: ["ios"],
    fetchImpl: function () {
      return Promise.resolve({
        ok: false,
        json: function () {
          return Promise.resolve({ mode: "live" });
        }
      });
    }
  });
  assert.deepEqual(httpError, { mode: "closed", purchasesAllowed: false });

  const badJson = await policy.loadPurchaseGate({
    platform: "ios",
    allowlist: ["ios"],
    fetchImpl: function () {
      return Promise.resolve({
        ok: true,
        json: function () {
          return Promise.reject(new Error("not json"));
        }
      });
    }
  });
  assert.deepEqual(badJson, { mode: "closed", purchasesAllowed: false });

  const testMode = await policy.loadPurchaseGate({
    platform: "ios",
    allowlist: ["ios"],
    fetchImpl: function () {
      return Promise.resolve({
        ok: true,
        json: function () {
          return Promise.resolve({
            mode: "test",
            ebook: STRIPE,
            training: STRIPE,
            bundle: STRIPE,
            staged: true
          });
        }
      });
    }
  });
  assert.deepEqual(testMode, { mode: "test", purchasesAllowed: false });
});

test("a live payload still hides purchase UI and drops Stripe URLs", async function () {
  const gate = await policy.loadPurchaseGate({
    platform: "android",
    fetchImpl: function () {
      return Promise.resolve({
        ok: true,
        json: function () {
          return Promise.resolve({
            mode: "live",
            ebook: STRIPE,
            training: STRIPE,
            bundle: STRIPE
          });
        }
      });
    }
  });
  assert.deepEqual(gate, { mode: "live", purchasesAllowed: false });
  assert.equal(JSON.stringify(gate).indexOf("stripe") === -1, true);
  assert.equal(policy.canOpenExternalUrl(STRIPE), false);
  assert.equal(policy.canOpenExternalUrl("https://www.walksteadfast.com"), true);
});

test("screens do not render prices or Stripe purchase links", function () {
  const appDir = path.join(__dirname, "..");
  const files = [
    "App.js",
    "screens/StoreScreen.js",
    "screens/DailyScreen.js",
    "screens/HomeScreen.js",
    "screens/TrainingScreen.js"
  ];
  files.forEach(function (name) {
    const source = fs.readFileSync(path.join(appDir, name), "utf8");
    ["$14", "$79", "$89", "buy.stripe.com", "bought on the website", "web purchase"].forEach(
      function (phrase) {
        assert.equal(source.indexOf(phrase) === -1, true, name + " contains " + phrase);
      }
    );
  });
  const store = fs.readFileSync(path.join(appDir, "screens/StoreScreen.js"), "utf8");
  assert.equal(store.indexOf("No in-app purchase.") !== -1, true);
  const appsCopy = require("../../packages/content/data.json").appsCopy;
  assert.equal(appsCopy.body.indexOf("to buy") === -1, true);
  assert.equal(appsCopy.body, "Free iOS and Android. No in-app purchase.");
  const app = fs.readFileSync(path.join(appDir, "App.js"), "utf8");
  assert.equal(app.indexOf("purchasesAllowed") !== -1, true);
  assert.equal(app.indexOf("canOpenExternalUrl") !== -1, true);
});
