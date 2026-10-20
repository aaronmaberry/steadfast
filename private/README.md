# Paid files (server-gated)

Everything under `private/` is served only to a signed-in session whose entitlement covers it.
`middleware.js` checks the `sm_sess` cookie (issued by `api/login.js`) before the CDN serves the file.
Old public paths (`/files/lessons/*`, the ebook and workbook under `/files/`, `/walksteadfast/audio/*`, `/training-locked/audio/*`) return 404.

## Lesson audio drop-in

Put the lesson mp3 at:

    private/lessons/lesson-NN.mp3     (NN = 01 to 24, two digits)

Encode at 96 kbps, 44.1 kHz, mono, same as lesson 01:

    ffmpeg -i S02-...-full.mp3 -ac 1 -ar 44100 -b:a 96k private/lessons/lesson-02.mp3

Commit and push. The Audio button on the paywall finds the file on load and turns on. Nothing else to edit.

## Other files here

- `private/lessons/lesson-NN-transcript.pdf`, `private/lessons/lesson-NN-page.pdf`: training or bundle entitlement
- `private/steadfast-way-workbook.pdf`: training or bundle entitlement
- `private/steadfast-men-ebook.pdf`: bundle entitlement only

## Accounts

`MEMBER_ACCOUNTS` (Vercel env, sensitive) is a JSON array:
`[{"email":"a@b.com","hash":"scrypt$<salt>$<hash>","ent":["training"]}]`
Make a hash with `node tools/member-hash.js 'password'`. `SESSION_SECRET` (32+ chars) signs the cookie.
