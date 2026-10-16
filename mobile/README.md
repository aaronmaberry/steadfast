# Steadfast Men mobile

Expo companion for the Steadfast Men site. This directory is not part of the website deploy.

## Run

From the repo root:

```bash
cd mobile
npm install
cd app
npx expo start
```

`npm start` from `mobile/` runs the same `expo start` script.

## Store policy

The ebook ($14), 24-week training ($79), and training plus hardcover bundle ($89) are digital goods under Apple and Google rules.

On iOS and Android the app does not show buy buttons, prices to buy, or external purchase links for those products, and it does not send people to the website to buy them.

The app reads `https://www.walksteadfast.com/api/checkout-config`. Purchase UI renders only when that response has `mode` `"live"` and the current platform is listed in `PURCHASE_PLATFORM_ALLOWLIST` (`mobile/app/lib/purchasePolicy.js`). The list ships empty, so a store build never shows purchase CTAs. A failed fetch is treated as not live.

Do not open `buy.stripe.com` links from this app.
