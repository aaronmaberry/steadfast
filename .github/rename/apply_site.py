import json, pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
CREED_C = "A steadfast man stops waiting, picks up the weight, goes first, and works for God’s pay, not the room’s."   # curly, for HTML
CREED_S = "A steadfast man stops waiting, picks up the weight, goes first, and works for God's pay, not the room's."   # straight, for JSON
OLD_CREED_C = "A real man rejects passivity, accepts responsibility, leads courageously, and expects the greater reward, God’s reward."
OLD_CREED_S = "A real man rejects passivity, accepts responsibility, leads courageously, and expects the greater reward, God's reward."
V1 = "“If anyone, then, knows the good they ought to do and doesn’t do it, it is sin for them.” <cite>James 4:17 NIV</cite>"
V2_OLD = "“Fathers, do not exasperate your children; instead, bring them up in the training and instruction of the Lord.” <cite>Ephesians 6:4 NIV</cite>"
V2 = "“For each one should carry their own load.” <cite>Galatians 6:5 NIV</cite>"
V3_OLD = "“Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.” <cite>Joshua 1:9 NIV</cite>"
V3 = "“When he has brought out all his own, he goes on ahead of them, and his sheep follow him because they know his voice.” <cite>John 10:4 NIV</cite>"
V4_OLD = "“Anyone who comes to him must believe that he exists and that he rewards those who earnestly seek him.” <cite>Hebrews 11:6 NIV</cite>"
V4 = "“Whatever you do, work at it with all your heart, as working for the Lord, not for human masters, since you know that you will receive an inheritance from the Lord as a reward.” <cite>Colossians 3:23-24 NIV</cite>"
OLD_META = "A 24-week path for Christian men. Reject passivity. Accept responsibility. Lead courageously. Expect God’s reward."
NEW_META = "A 24-week path for Christian men. Stop waiting. Pick up the weight. Go first. Work for God’s pay."

EDITS = {
 "index.html": [
  (OLD_META, NEW_META, 3),
  ("<h3>Reject passivity</h3><p>Stop waiting for the room to captain itself.</p>",
   "<h3>Stop Waiting</h3><p>When it’s yours to do, start now, before you feel like it.</p>", 1),
  ("<h3>Accept responsibility</h3><p>Name what is yours. Carry it.</p><p class=\"mark-verse\">" + V2_OLD,
   "<h3>Pick Up the Weight</h3><p>Carry what’s yours, even when somebody else dropped it.</p><p class=\"mark-verse\">" + V2, 1),
  ("<h3>Lead courageously</h3><p>Go first when it costs you.</p><p class=\"mark-verse\">" + V3_OLD,
   "<h3>Go First</h3><p>Step out ahead of your people, scared or not.</p><p class=\"mark-verse\">" + V3, 1),
  ("<h3>Expect God’s reward</h3><p>Build for a yes that outlasts the week.</p><p class=\"mark-verse\">" + V4_OLD,
   "<h3>Work for God’s Pay</h3><p>Do it for the Lord’s reward, not the room’s applause.</p><p class=\"mark-verse\">" + V4, 1),
 ],
 "marks.html": [
  (OLD_CREED_C, CREED_C, 4),
  ("      <p>" + CREED_C + "</p>\n    </div>",
   "      <p>" + CREED_C + "</p>\n      <p>God’s pay is a Father’s inheritance, not wages.</p>\n    </div>", 1),
  ("<h2>Reject passivity</h2>\n        <p class=\"lede\">Passivity is the respectable sin of decent men. You are in the house and absent from it. The first mark is attention returned to God, wife, children, and work.</p>",
   "<h2>Stop Waiting</h2>\n        <p class=\"lede\">Waiting is the respectable sin of decent men. It looks like patience or keeping the peace. You are in the house and absent from it. When it’s yours to do, start now, before you feel like it.</p>", 1),
  ("<h2>Accept responsibility</h2>\n        <p class=\"lede\">Blame is cheap. Responsibility costs a calendar. This mark is the decision to carry what God actually assigned you, including the parts you hoped would resolve themselves.</p>\n        <p class=\"mark-verse\">" + V2_OLD,
   "<h2>Pick Up the Weight</h2>\n        <p class=\"lede\">Blame is cheap. Carrying costs a calendar. A man looks at what has landed in his house or his lane and says, “That’s mine.” Carry what’s yours, even when somebody else dropped it.</p>\n        <p class=\"mark-verse\">" + V2, 1),
  ("<h2>Lead courageously</h2>\n        <p class=\"lede\">Leadership here is not a title. It is going first — into prayer, into apology, into provision, into the conversation that has been rotting under the floorboards.</p>\n        <p class=\"mark-verse\">" + V3_OLD,
   "<h2>Go First</h2>\n        <p class=\"lede\">Going first is not a title. It is stepping out ahead of your people, scared or not: into prayer, into apology, into provision, into the conversation that has been rotting under the floorboards.</p>\n        <p class=\"mark-verse\">" + V3, 1),
  ("<h2>Expect God’s reward</h2>\n        <p class=\"lede\">If the payoff has to arrive this quarter, you will bargain. The fourth mark lifts a man’s eyes so he can stay when staying does not trend.</p>\n        <p class=\"mark-verse\">" + V4_OLD,
   "<h2>Work for God’s Pay</h2>\n        <p class=\"lede\">Do it for the Lord’s reward, not the room’s applause. God’s pay is an inheritance, what a Father gives His sons because they are His. Nobody earns it. You work like a son because you already are one.</p>\n        <p class=\"mark-verse\">" + V4, 1),
 ],
 "training.html": [
  ("<h3>Reject passivity</h3>", "<h3>Stop Waiting</h3>", 1),
  ("<h3>Accept responsibility</h3>", "<h3>Pick Up the Weight</h3>", 1),
  ("<h3>Lead courageously</h3>", "<h3>Go First</h3>", 1),
  ("<h3>Expect God’s reward</h3>", "<h3>Work for God’s Pay</h3>", 1),
 ],
 "program.html": [
  ("<h3 id=\"mark-name\">Reject passivity</h3>", "<h3 id=\"mark-name\">Stop Waiting</h3>", 1),
  ("<h3>Reject passivity</h3>", "<h3>Stop Waiting</h3>", 1),
  ("<h3>Accept responsibility</h3>", "<h3>Pick Up the Weight</h3>", 1),
  ("<h3>Lead courageously</h3>", "<h3>Go First</h3>", 1),
  ("<h3>Expect God’s reward</h3>", "<h3>Work for God’s Pay</h3>", 1),
  ("label: \"Reject passivity\"", "label: \"Stop Waiting\"", 1),
  ("label: \"Accept responsibility\"", "label: \"Pick Up the Weight\"", 1),
  ("label: \"Lead courageously\"", "label: \"Go First\"", 1),
  ("label: \"Expect God’s reward\"", "label: \"Work for God’s Pay\"", 1),
  ("The last mark is about reward that is not a raise — do not drag leadership trophies into it.",
   "The last mark is about God’s pay, which is not a raise. Do not drag leadership trophies into it.", 1),
 ],
 "groups.html": [
  ("alt=\"Reject passivity\"", "alt=\"Stop Waiting\"", 1),
  ("alt=\"Accept responsibility\"", "alt=\"Pick Up the Weight\"", 1),
  ("alt=\"Lead courageously\"", "alt=\"Go First\"", 1),
 ],
 "site.js": [
  ("The greater reward holds when payday does not.", "God’s pay holds when payday does not.", 1),
 ],
 # PROTECTED PAGE: only the sentence that literally contains the old mark names (and the Lewis credit tied to them)
 "t-table.html": [
  ("<p>Credit where it is due: the four marks — reject passivity, accept responsibility, lead courageously, expect the greater reward — were popularized by Robert Lewis. The exposition and the 24 weeks here are original.</p>",
   "<p>The four marks are stop waiting, pick up the weight, go first, and work for God’s pay. The exposition and the 24 weeks here are original.</p>", 1),
 ],
}

DAILY = [
 (OLD_CREED_S, CREED_S),
 ("Today you reject passivity.", "Today you stop waiting."),
 ("This is you rejecting passivity and accepting the work that already has your name on it.", "This is you done waiting, picking up the work that already has your name on it."),
 ("This is you rejecting passivity and expecting a harvest you cannot see yet.", "This is you done waiting on your mood, and working for a harvest you cannot see yet."),
 ("This is you rejecting passivity on the only day you actually have.", "This is you done waiting, on the only day you actually have."),
 ("This is you rejecting passivity in the one room built for it.", "This is you done waiting, in the one room built for it."),
 ("This is you rejecting passivity with the one light God put in your hand.", "This is you done waiting, with the one light God put in your hand."),
 ("This is you rejecting passivity.", "This is you done waiting."),
 ("This is you rejecting the passivity that hides in endless work, and expecting God to keep the night.", "This is you done hiding in endless work, and trusting God to keep the night."),
 ("This is you rejecting the passivity that hides inside constant noise.", "This is you done hiding inside constant noise."),
 ("This is you rejecting the passivity that lets pride drive.", "This is you done letting pride drive."),
 ("This is you accepting responsibility for what gets copied, and leading in the small talk.", "This is you picking up the weight of what gets copied, and going first in the small talk."),
 ("This is you accepting responsibility", "This is you picking up the weight"),
 ("This is you leading courageously, by submitting first.", "This is you going first, on your knees."),
 ("This is you leading courageously, because going first costs pride.", "This is you going first, and it costs pride."),
 ("This is you leading courageously", "This is you going first"),
 ("This is you expecting the greater reward, God's reward, the one the resurrection guarantees.", "This is you working for God's pay, the inheritance the resurrection guarantees."),
 ("This is you expecting the greater reward, God's reward", "This is you working for God's pay"),
 ("This is you expecting God's reward with your eyes.", "This is you working for God's pay with your eyes."),
 ("This is you expecting God's reward on a quiet field, and rejecting the line that says you already did your part.", "This is you working for God's pay on a quiet field, and refusing the line that says you already did your part."),
 ("You cannot keep a second life on a screen and expect God's reward.", "You cannot keep a second life on a screen and still work for God's pay."),
 ("Expect God's reward with your eyes under a rule that would still hold if the phone unlocked at the table.", "Work for God's pay with your eyes, under a rule that would still hold if the phone unlocked at the table."),
 ("That is the greater reward, and it does not depend on anyone noticing.", "That is God's pay, and it does not depend on anyone noticing."),
]

log = []
for fn, edits in EDITS.items():
    p = ROOT / fn; s = p.read_text(); o = s
    for a, b, n in edits:
        c = s.count(a)
        if c != n: raise SystemExit(f"{fn}: expected {n} of {a[:70]!r}, found {c}")
        s = s.replace(a, b); log.append((fn, a, b, c))
    if s != o: p.write_text(s)

p = ROOT / "app/daily.json"; raw = p.read_text(); d = json.loads(raw)
counts = {a: 0 for a, _ in DAILY}
for it in d["items"]:
    for k, v in list(it.items()):
        if isinstance(v, str):
            for a, b in DAILY:
                if a in v:
                    counts[a] += v.count(a); v = v.replace(a, b)
            it[k] = v
for a, b in DAILY:
    if counts[a] == 0: raise SystemExit(f"daily: no hit for {a!r}")
    log.append(("app/daily.json", a, b, counts[a]))
# keep original formatting style
indent = 2
p.write_text(json.dumps(d, indent=indent, ensure_ascii=False) + ("\n" if raw.endswith("\n") else ""))
json.dump(log, open("/tmp/site-change-log.json", "w"), indent=1, ensure_ascii=False)
print(len(log), "edits")
