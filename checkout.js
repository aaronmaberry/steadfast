window.STEADFAST_CHECKOUT = {
  mode: "test",
  training: "https://buy.stripe.com/test_28EaEQ8AI10F5BCgJtdnW00",
  ebook: "https://buy.stripe.com/test_8x2bIUeZ67p36FGgJtdnW01",
  bundle: "https://buy.stripe.com/test_14A14g8AI8t79RSfFpdnW02",
  giveOnce: "https://donate.stripe.com/test_28E00c8AIbFj8NOdxhdnW03",
  giveMonthly: {
    5: "https://donate.stripe.com/test_bJe00c04c10Fe88eBldnW05",
    10: "https://donate.stripe.com/test_4gM7sEcQYcJne8864PdnW06",
    25: "https://donate.stripe.com/test_5kQ4gs18geRv8NO0KvdnW04",
    50: "https://donate.stripe.com/test_7sY28kdV2fVzc00ctddnW07",
    100: "https://donate.stripe.com/test_8x28wI6sAdNr7JK3WHdnW08"
  }
};
window.steadfastPay = function (sku) {
  const c = window.STEADFAST_CHECKOUT || {};
  const url = c[sku];
  if (url) location.href = url;
};
