# Stripe checkout — Steadfast Men, LLC

Public site: https://www.walksteadfast.com  
Vercel project: `walksteadfast` (framework Other, root `.`, production branch `main`)

The site is static HTML. Ebook, training, and bundle buy buttons redirect to Stripe Payment Links. They do not call the Checkout Sessions API.

## Locked prices

These are the only paid product SKUs. Payment Links in Stripe must use these amounts.

| SKU | Config key | Price | What it is |
| --- | --- | --- | --- |
| Ebook | `ebook` | $14 | Ebook alone |
| Training | `training` | $79 | 24-week training |
| Bundle | `bundle` | $89 | Training + print |

Give / donate buttons stay on the test donate Payment Links in `checkout.js`. They are not these three SKUs.

## How a buy button resolves

`checkout.js` is the only client source for the three product URLs. Buttons use `data-pay="ebook"`, `data-pay="training"`, or `data-pay="bundle"`. `window.steadfastPay(sku)` sends the browser to that URL.

On load, the script fetches `GET /api/checkout-config` (`api/checkout-config.js`). A valid `https://buy.stripe.com/…` value replaces that SKU. Anything else is ignored.

When a live env var is unset, the button keeps the Stripe **test** Payment Link checked in with `checkout.js`. `mode` stays `"test"` until all three overrides are live links (a live link has no `/test_` in the path). Button labels stay normal buy copy in either mode.

If a SKU has no usable URL, the control reads **Checkout not configured** and does not navigate.

`STRIPE_SECRET_KEY` and `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` are not read. Do not put a secret key in the repo or in client JavaScript. This static site does not inline `NEXT_PUBLIC_*` variables. A publishable key is unused because Payment Links do not need Stripe.js.

No webhook is deployed. There is no `STRIPE_WEBHOOK_SECRET` in use.

## Environment variables

Set these on Vercel project **walksteadfast**: Project → Settings → Environment Variables. Use Production. Add Preview only if preview deploys should send buyers to the same links. Save, then redeploy so the function sees the new values.

| Name | Required now | Value |
| --- | --- | --- |
| `STRIPE_PAYMENT_LINK_EBOOK` | When going live | Payment Link URL for the $14 ebook |
| `STRIPE_PAYMENT_LINK_TRAINING` | When going live | Payment Link URL for the $79 training |
| `STRIPE_PAYMENT_LINK_BUNDLE` | When going live | Payment Link URL for the $89 bundle |

Paste the bare Payment Link only, for example `https://buy.stripe.com/abc123`. No query string. Test-mode links are accepted and keep `mode` at `"test"`.

Not used by this wiring:

| Name | Status |
| --- | --- |
| `STRIPE_SECRET_KEY` | Unused. Reserve it for a future server Checkout Session or webhook handler. Never expose it to the browser. |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Unused. Named by Jarvis for a Next.js-style client. This site has no Stripe.js and does not publish a key. |
| `STRIPE_WEBHOOK_SECRET` | Unused. Reserve this name if a webhook is added later. Do not commit it. |

## Still pending — Aaron / Jarvis

Live Payment Link URLs are not in the repo. Create them in the Stripe Dashboard for **Steadfast Men, LLC** at the locked prices, then set the three `STRIPE_PAYMENT_LINK_*` variables on project `walksteadfast` and redeploy.

Also still open, only if you change approach later:

- Live `STRIPE_SECRET_KEY`, and a publishable key, if you replace Payment Links with Checkout Sessions
- `STRIPE_WEBHOOK_SECRET`, if you add a webhook

Until those live Payment Link URLs are set, buy buttons use the test Payment Links and `mode` stays `"test"`.
