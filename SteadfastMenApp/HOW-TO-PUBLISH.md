# Steadfast Men iPhone + iPad app

You do not need to write code. You need a Mac, one paid Apple account, and about an afternoon the first time.

## What this app does

- **Today** — morning walk. Pulls `https://www.walksteadfast.com/app/daily.json`. If the network fails it uses the copy bundled in the app.
- **Path** — buttons that open the live website for training ($79), book, shop, groups, merch.
- **Give** — one-time or monthly amount, then Safari to your giving page (Donorbox / Tithely / Givebutter / Stripe Payment Link). Paste that URL in `Config.swift` before you ship.
- **More** — website + socials. Empty social URLs fall back to the website until you paste real ones.

## 0. Buy the keys

1. Get a Mac (or borrow one). iPad and iPhone apps are built with **Xcode**, which only runs on a Mac.
2. Create an Apple ID if you do not have one.
3. Enroll in the **Apple Developer Program** — $99/year.  
   https://developer.apple.com/programs/
4. If this is a church or 501(c)(3), enroll as **Organization**, not Individual. You will need a D-U-N-S number. Tithe.ly’s walkthrough is clean: search “Apple Developer account for your church.”
5. Download **Xcode** from the Mac App Store. Open it once and let it install extra tools.

## 1. Open the project (first time)

1. Unzip `SteadfastMenApp`.
2. Open Xcode → **File → New → Project**.
3. Choose **iOS → App**. Next.
4. Product Name: `SteadfastMen`
5. Team: your paid developer team
6. Organization Identifier: `com.walksteadfast`
7. Interface: **SwiftUI**. Language: **Swift**.
8. Uncheck Core Data. Create it on your Desktop.
9. Delete the starter `ContentView.swift` Xcode made.
10. Drag every file from this folder’s `SteadfastMen/` into the Xcode left sidebar. Check **Copy items if needed**. Check the SteadfastMen target.
11. Drag `Resources/daily.json` in. In the right inspector check **Target Membership**.
12. Drag `Resources/AppIcon-1024.png` onto **Assets → AppIcon**.
13. At the top of Xcode, set the run destination to **iPhone 16** or your plugged-in phone.
14. Press the Play button. The app should open in the simulator.

If Play is grey: sign in Xcode → Settings → Accounts → add your Apple ID, then select your Team on the target’s **Signing & Capabilities** tab.

## 2. Fill the blanks before you ship

Open `Config.swift` and paste:

- `giveURL` — your live donation page
- `youtube`, `instagram`, `x`, `facebook`, `tiktok`, `podcast` — full https links

Do not ship with empty give URL if you show the Give tab. Apple reviewers click every button.

## 3. How you upload a daily devotion

You do **not** rebuild the app every morning.

1. On the website, keep a file at  
   `https://www.walksteadfast.com/app/daily.json`
2. A starter file is in this folder and also at `walksteadfast/app/daily.json`.
3. Each morning edit that JSON (or have Grok / an editor do it):

```json
{
  "updated": "2026-09-11",
  "items": [
    {
      "date": "2026-09-11",
      "title": "Your title",
      "verse": "The verse — Reference",
      "body": "The walk.",
      "videoURL": "https://youtu.be/xxxxx",
      "imageURL": ""
    }
  ]
}
```

4. Deploy that one file with the site. The app picks today’s `date`. If today is missing it uses the newest item.
5. Optional: add `"videoURL"` for the film slot.

Keep old days in the file if you want a back catalog. Newest-first is fine.

## 4. Giving and Apple’s rules (read this)

Apple is picky.

- **Selling the book or training inside the app** would require In-App Purchase and Apple’s cut. That is why Path opens the **website**. Do not add a “buy ebook here” checkout inside the app unless you are ready for StoreKit.
- **Donations**
  - If you are a registered nonprofit approved by Apple, you may fundraise in-app with Apple Pay.
  - If you are not, the safe pattern we shipped is: the Give tab opens Safari to your giving page. That is how most church apps start.
  - Never unlock app features because someone gave. Giving is a gift, not a paywall.
- Write in App Review notes: “Give opens our public donation page. Training and books are sold on the website, not as in-app purchases.”

## 5. Test on your phone

1. Plug in the iPhone or iPad.
2. Trust the computer on the device.
3. In Xcode pick the device name → Play.
4. First time: Settings → General → VPN & Device Management → trust your developer certificate.

## 6. Put it on the App Store

1. In Apple Developer, create an **App ID**: `com.walksteadfast.SteadfastMen`
2. Go to https://appstoreconnect.apple.com → **My Apps → +**
3. Name: `Steadfast Men`
4. Primary language: English (US)
5. Bundle ID: the App ID you just made
6. SKU: `steadfast-men-ios`
7. In Xcode: Product → Archive. Wait.
8. Window → Organizer → Distribute App → App Store Connect → Upload.
9. In App Store Connect fill:
   - Privacy policy URL (`https://www.walksteadfast.com/privacy`)
   - Support URL (`https://www.walksteadfast.com`)
   - Screenshots: iPhone 6.7" and iPad 13" (Xcode Simulator → Cmd-S)
   - Description, keywords: steadfast, biblical manhood, daily devotion, Christian men
   - Age rating: 4+
   - Category: Lifestyle or Reference
10. Submit for Review. First review often takes 24–72 hours. They may reject once. Read the email. Fix. Resubmit.

## 7. After it is live

- Daily work is only the JSON file.
- App updates (new screens) require a new Archive + Review.
- Yearly: renew the $99 developer membership or the app disappears.

## If you get stuck

Screenshot the Xcode error. Send it back here. Do not pay a random “we’ll publish your app” freelancer the first week — most of the wait is Apple’s review, not code.
