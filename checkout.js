(function () {
  var PRODUCT_URL = /^https:\/\/buy\.stripe\.com\/[A-Za-z0-9_-]+$/;
  var PRODUCTS = { ebook: true, training: true, bundle: true };
  var TEST_LINKS = {
    training: "https://buy.stripe.com/test_28EaEQ8AI10F5BCgJtdnW00",
    ebook: "https://buy.stripe.com/test_8x2bIUeZ67p36FGgJtdnW01",
    bundle: "https://buy.stripe.com/test_14A14g8AI8t79RSfFpdnW02"
  };

  window.STEADFAST_CHECKOUT = {
    mode: "test",
    prices: { ebook: 14, training: 79, bundle: 89 },
    training: TEST_LINKS.training,
    ebook: TEST_LINKS.ebook,
    bundle: TEST_LINKS.bundle,
    giveOnce: "https://donate.stripe.com/test_28E00c8AIbFj8NOdxhdnW03",
    giveMonthly: {
      5: "https://donate.stripe.com/test_bJe00c04c10Fe88eBldnW05",
      10: "https://donate.stripe.com/test_4gM7sEcQYcJne8864PdnW06",
      25: "https://donate.stripe.com/test_5kQ4gs18geRv8NO0KvdnW04",
      50: "https://donate.stripe.com/test_7sY28kdV2fVzc00ctddnW07",
      100: "https://donate.stripe.com/test_8x28wI6sAdNr7JK3WHdnW08"
    }
  };

  function isProductUrl(url) {
    return typeof url === "string" && PRODUCT_URL.test(url);
  }

  function urlFor(sku) {
    var c = window.STEADFAST_CHECKOUT || {};
    return isProductUrl(c[sku]) ? c[sku] : "";
  }

  window.steadfastPay = function (sku) {
    var url = urlFor(sku);
    if (!url) return false;
    location.href = url;
    return true;
  };

  function paint() {
    document.querySelectorAll("[data-pay]").forEach(function (el) {
      var sku = el.getAttribute("data-pay");
      if (!PRODUCTS[sku]) return;
      if (!el.hasAttribute("data-pay-label")) {
        el.setAttribute("data-pay-label", el.textContent);
      }
      var url = urlFor(sku);
      if (url) {
        el.setAttribute("href", url);
        el.removeAttribute("aria-disabled");
        el.textContent = el.getAttribute("data-pay-label");
      } else {
        el.setAttribute("href", "#checkout");
        el.setAttribute("aria-disabled", "true");
        el.textContent = "Checkout not configured";
      }
    });
  }

  function rememberLabel(el) {
    if (!el.hasAttribute("data-pay-label")) {
      el.setAttribute("data-pay-label", el.textContent);
    }
  }

  document.addEventListener("click", function (e) {
    var el = e.target && e.target.closest ? e.target.closest("[data-pay]") : null;
    if (!el) return;
    var sku = el.getAttribute("data-pay");
    if (!PRODUCTS[sku]) return;
    rememberLabel(el);
    var url = urlFor(sku);
    if (!url) {
      e.preventDefault();
      el.setAttribute("href", "#checkout");
      el.setAttribute("aria-disabled", "true");
      el.textContent = "Checkout not configured";
      return;
    }
    el.setAttribute("href", url);
  });

  function wireForms() {
    document.querySelectorAll("[data-start-form]").forEach(function (form) {
      var offer = form.elements.offer;
      if (!offer || offer.tagName !== "SELECT") return;
      function sync() {
        var paid = !!PRODUCTS[offer.value];
        ["name", "email"].forEach(function (name) {
          var input = form.elements[name];
          if (!input) return;
          if (paid) input.removeAttribute("required");
          else input.setAttribute("required", "");
        });
      }
      offer.addEventListener("change", sync);
      sync();
      form.addEventListener("submit", function (e) {
        if (!PRODUCTS[offer.value]) return;
        e.preventDefault();
        e.stopImmediatePropagation();
        if (!window.steadfastPay(offer.value)) {
          var btn = form.querySelector("[type=submit]");
          if (btn) btn.textContent = "Checkout not configured";
        }
      }, true);
    });
  }

  function applyRemote(cfg) {
    if (!cfg || typeof cfg !== "object") return;
    var skus = ["ebook", "training", "bundle"];
    var useLive = cfg.mode === "live" && skus.every(function (sku) {
      return isProductUrl(cfg[sku]);
    });
    skus.forEach(function (sku) {
      window.STEADFAST_CHECKOUT[sku] = useLive ? cfg[sku] : TEST_LINKS[sku];
    });
    window.STEADFAST_CHECKOUT.mode = useLive ? "live" : "test";
    paint();
  }

  function boot() {
    paint();
    wireForms();
    fetch("/api/checkout-config", { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(applyRemote)
      .catch(function () {});
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
