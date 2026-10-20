# Steadfast Men — Android app

Same product as the iPhone app. Same four tabs. Same daily JSON file. You still do not need to write code.

## Play with it today (no Play Store)

Use the same browser preview as iOS:

- `SteadfastMenApp/preview.html`
- or `https://www.walksteadfast.com/app/preview.html` after that folder is on the site

That is the design. The Kotlin project below is the real Android app.

## What you need

1. A computer. Windows, Mac, or Linux is fine for Android.
2. [Android Studio](https://developer.android.com/studio) — free.
3. A Google account.
4. Later, a one-time **$25** Google Play Developer registration (not yearly).

You do **not** need a Mac for Android.

## Open the project

1. Unzip `SteadfastMenAndroid`.
2. Open Android Studio → **Open** → pick the `SteadfastMenAndroid` folder (the one that contains `settings.gradle.kts`).
3. Let it download Gradle the first time. Coffee.
4. If it asks to generate a Gradle wrapper, say yes.
5. Top device menu: pick **Medium Phone** or plug in your Android phone (phone: enable Developer options → USB debugging).
6. Green Play button.

If Gradle fails: File → Sync Project with Gradle Files. JDK 17.

## Fill blanks before a public build

Open `app/src/main/java/com/walksteadfast/app/Config.kt` and paste:

- `GIVE` — Donorbox / Tithely / Givebutter / Stripe Payment Link
- `YOUTUBE`, `INSTAGRAM`, `X`, `FACEBOOK`, `TIKTOK`, `PODCAST`

Empty socials open the website. Fine for testing. Not fine if a Play reviewer taps them and hits a dead end — website fallback is already there.

## Daily devotionals (same file as iPhone)

Both apps read:

`https://www.walksteadfast.com/app/daily.json`

Edit that file. Deploy the site. Do not rebuild the app every morning.

A bundled copy lives at `app/src/main/assets/daily.json` for airplanes.

## Giving on Android

Same rule as iOS: Give opens the browser. Do not sell the book or training inside the app unless you are ready for Google Play Billing.

Write in the Play Console notes: “Give opens our public donation page. Books and training are sold on the website.”

## Put it on Google Play

1. Pay the $25 at https://play.google.com/console
2. Create app → name `Steadfast Men` → app → free
3. In Android Studio: Build → Generate Signed App Bundle / APK → Android App Bundle
4. First time: create a keystore. Write the password on paper. Lose it and you cannot update the app.
5. Upload the `.aab` in Play Console
6. Store listing: short description, screenshots (use the emulator), privacy URL `https://www.walksteadfast.com/privacy`
7. Content rating questionnaire
8. Data safety form — this app stores a local streak and fetches JSON. No login.
9. Send to review. First review is often 1–7 days.

## Phone test without Play

Android Studio → Play onto your phone. That install is only on that device.

Internal testing track in Play Console lets you invite a few Gmail addresses without a public listing.

## iPhone and Android stay twins

Change the daily JSON once. Both apps update.

Change screens? Edit the Swift files **and** these Kotlin files, or send both projects back here.
