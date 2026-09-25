"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");
const handler = require("../api/checkout-config");

const EBOOK = "https://buy.stripe.com/ebookFixtureAa";
const TRAINING = "https://buy.stripe.com/trainingFixtureBb";
const BUNDLE = "https://buy.stripe.com/bundleFixtureCc";
const FIXTURES = [EBOOK, TRAINING, BUNDLE];
const ENV_NAMES = [
  "STRIPE_CHECKOUT_LIVE",
  "STRIPE_PAYMENT_LINK_EBOOK",
  "STRIPE_PAYMENT_LINK_TRAINING",
  "STRIPE_PAYMENT_LINK_BUNDLE"
];
const TEST_LINKS = {
  ebook: "https://buy.stripe.com/test_8x2bIUeZ67p36FGgJtdnW01",
  training: "https://buy.stripe.com/test_28EaEQ8AI10F5BCgJtdnW00",
  bundle: "https://buy.stripe.com/test_14A14g8AI8t79RSfFpdnW02"
};

function withEnv(env, fn) {
  const prev = {};
  ENV_NAMES.forEach(function (name) {
    prev[name] = process.env[name];
    delete process.env[name];
  });
  Object.keys(env).forEach(function (name) {
    if (env[name] !== undefined) process.env[name] = env[name];
  });
  try {
    return fn();
  } finally {
    ENV_NAMES.forEach(function (name) {
      if (prev[name] === undefined) delete process.env[name];
      else process.env[name] = prev[name];
    });
  }
}

function call(method, env) {
  return withEnv(env, function () {
    const headers = {};
    let raw;
    const res = {
      statusCode: 0,
      setHeader: function (key, value) {
        headers[String(key).toLowerCase()] = value;
      },
      end: function (payload) {
        raw = payload;
      }
    };
    handler({ method: method }, res);
    return {
      status: res.statusCode,
      headers: headers,
      raw: raw,
      json: raw ? JSON.parse(raw) : undefined
    };
  });
}

function linkEnv(kind) {
  if (kind === "missing") return {};
  if (kind === "partial") return { STRIPE_PAYMENT_LINK_EBOOK: EBOOK };
  return {
    STRIPE_PAYMENT_LINK_EBOOK: EBOOK,
    STRIPE_PAYMENT_LINK_TRAINING: TRAINING,
    STRIPE_PAYMENT_LINK_BUNDLE: BUNDLE
  };
}

function flagEnv(flag) {
  if (flag === "unset") return {};
  return { STRIPE_CHECKOUT_LIVE: flag };
}

function assertHidden(result, staged) {
  assert.equal(result.status, 200);
  assert.deepEqual(result.json, {
    mode: "test",
    ebook: "",
    training: "",
    bundle: "",
    staged: staged
  });
  const raw = result.raw;
  FIXTURES.forEach(function (url) {
    assert.equal(raw.includes(url), false, "response leaked " + url);
  });
  assert.equal(result.headers["content-type"], "application/json; charset=utf-8");
  assert.equal(result.headers["cache-control"], "public, max-age=60, must-revalidate");
  assert.equal(result.headers["x-content-type-options"], "nosniff");
}

test("flag unset, false, and true against missing, partial, and all links", function () {
  ["unset", "false", "true"].forEach(function (flag) {
    ["missing", "partial", "all"].forEach(function (links) {
      const env = Object.assign({}, flagEnv(flag), linkEnv(links));
      const result = call("GET", env);
      const label = flag + " / " + links;
      if (flag === "true" && links === "all") {
        assert.deepEqual(result.json, {
          mode: "live",
          ebook: EBOOK,
          training: TRAINING,
          bundle: BUNDLE
        }, label);
        assert.equal(Object.prototype.hasOwnProperty.call(result.json, "staged"), false);
        assert.equal(result.status, 200);
        return;
      }
      assertHidden(result, links === "all");
      assert.equal(result.json.mode, "test", label);
    });
  });
});

test("only the exact string true arms live checkout", function () {
  ["TRUE", "True", "1", "yes", " true", "true "].forEach(function (flag) {
    const result = call("GET", Object.assign({ STRIPE_CHECKOUT_LIVE: flag }, linkEnv("all")));
    assert.equal(result.json.mode, "test", flag);
    assert.equal(result.json.staged, true);
    assert.equal(result.raw.includes(EBOOK), false);
  });
});

test("invalid or incomplete links stay hidden and are not staged", function () {
  const result = call("GET", {
    STRIPE_CHECKOUT_LIVE: "true",
    STRIPE_PAYMENT_LINK_EBOOK: EBOOK + "?prefilled_email=a@b.c",
    STRIPE_PAYMENT_LINK_TRAINING: TRAINING,
    STRIPE_PAYMENT_LINK_BUNDLE: "https://example.com/not-stripe"
  });
  assertHidden(result, false);
  assert.equal(result.raw.includes("example.com"), false);
  assert.equal(result.raw.includes("prefilled_email"), false);
});

test("trimmed valid links count as staged and go live only with the flag", function () {
  const env = {
    STRIPE_PAYMENT_LINK_EBOOK: "  " + EBOOK + "  ",
    STRIPE_PAYMENT_LINK_TRAINING: TRAINING,
    STRIPE_PAYMENT_LINK_BUNDLE: BUNDLE
  };
  const held = call("GET", env);
  assertHidden(held, true);
  const live = call("GET", Object.assign({ STRIPE_CHECKOUT_LIVE: "true" }, env));
  assert.equal(live.json.ebook, EBOOK);
  assert.equal(live.json.mode, "live");
});

test("HEAD and unsupported methods keep the existing response contract", function () {
  const head = call("HEAD", Object.assign({ STRIPE_CHECKOUT_LIVE: "true" }, linkEnv("all")));
  assert.equal(head.status, 200);
  assert.equal(head.raw, undefined);
  assert.equal(head.headers["content-type"], "application/json; charset=utf-8");
  assert.equal(head.headers["cache-control"], "public, max-age=60, must-revalidate");
  assert.equal(head.headers["x-content-type-options"], "nosniff");

  const denied = call("POST", linkEnv("all"));
  assert.equal(denied.status, 405);
  assert.deepEqual(denied.json, { error: "method" });
  assert.equal(denied.headers.allow, "GET, HEAD");
  assert.equal(denied.headers["content-type"], "application/json; charset=utf-8");
  assert.equal(denied.raw.includes(EBOOK), false);
});

function bootCheckout(cfg) {
  const listeners = {};
  const requested = [];
  const sandbox = {
    document: {
      readyState: "loading",
      addEventListener: function (type, fn) {
        (listeners[type] || (listeners[type] = [])).push(fn);
      },
      querySelectorAll: function () {
        return [];
      }
    },
    location: { href: "" },
    fetch: function (url) {
      requested.push(String(url));
      if (String(url).indexOf("buy.stripe.com") !== -1) {
        return Promise.reject(new Error("refusing to request buy.stripe.com"));
      }
      return Promise.resolve({
        ok: true,
        json: function () {
          return Promise.resolve(cfg);
        }
      });
    }
  };
  sandbox.window = sandbox;
  vm.runInNewContext(
    fs.readFileSync(path.join(__dirname, "../checkout.js"), "utf8"),
    sandbox,
    { filename: "checkout.js" }
  );
  (listeners.DOMContentLoaded || []).forEach(function (fn) {
    fn();
  });
  return new Promise(function (resolve) {
    setImmediate(resolve);
  }).then(function () {
    assert.deepEqual(requested, ["/api/checkout-config"]);
    return sandbox.STEADFAST_CHECKOUT;
  });
}

test("checkout.js keeps test links unless mode is live for every SKU", async function () {
  const partial = {
    mode: "live",
    ebook: EBOOK,
    training: "",
    bundle: BUNDLE
  };
  const held = await bootCheckout({
    mode: "test",
    ebook: EBOOK,
    training: TRAINING,
    bundle: BUNDLE,
    staged: true
  });
  assert.equal(held.mode, "test");
  assert.deepEqual(
    { ebook: held.ebook, training: held.training, bundle: held.bundle },
    TEST_LINKS
  );

  const incomplete = await bootCheckout(partial);
  assert.equal(incomplete.mode, "test");
  assert.deepEqual(
    { ebook: incomplete.ebook, training: incomplete.training, bundle: incomplete.bundle },
    TEST_LINKS
  );

  const live = await bootCheckout({
    mode: "live",
    ebook: EBOOK,
    training: TRAINING,
    bundle: BUNDLE
  });
  assert.equal(live.mode, "live");
  assert.equal(live.ebook, EBOOK);
  assert.equal(live.training, TRAINING);
  assert.equal(live.bundle, BUNDLE);
  assert.equal(live.giveOnce.indexOf("/test_") !== -1, true);
});
