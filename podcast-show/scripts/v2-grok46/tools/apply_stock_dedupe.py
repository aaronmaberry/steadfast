#!/usr/bin/env python3
"""Replace high-frequency stock spoken sentences with unique per-episode versions.

Does not touch E007. Leaves 2-episode story pairs for the writers.
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# original sentence (as it appears, or a unique substring) -> {ep: replacement}
# Replacements must stay 6+ words when the original was a question we need to keep,
# and must not collide with each other.

MAP = {}


def add(original, mapping):
    MAP[original] = mapping


add(
    "Can I ask you something hard?",
    {
        "E012": "Mind if I press on the leftover Valentine?",
        "E013": "Can I push on the prize you still want by Thursday?",
        "E019": "What is your anger actually guarding right now?",
        "E021": "Is the itch the thing, or is the drift?",
        "E023": "Which garden are you standing in tonight?",
        "E024": "Are you waiting on Friday to feel holy?",
        "E025": "Will you stay in the room when it gets quiet?",
        "E026": "What did Easter week actually change at your house?",
        "E027": "Who is the empty chair still talking to?",
        "E028": "Did you set the chair or just talk about it?",
        "E029": "Are you going to call him while he's still here?",
        "E030": "Did the call happen, or did you draft it again?",
        "E031": "Has home handed you off, or are you still waiting?",
        "E033": "Can you leave without making it a slam?",
        "E035": "Are you a grown son this week, or still the helper?",
        "E036": "What did you actually do for her, not just say?",
        "E037": "Who is your brother if it isn't blood?",
        "E038": "What from the father-who-stays week is still undone?",
        "E039": "Did you ask the man, or ask a screen?",
        "E040": "Did the ask land, or did you cancel it?",
        "E041": "Which living man are you going to call?",
        "E042": "Who are you remembering, and who are you avoiding?",
        "E043": "Where is north on your fridge this week?",
        "E044": "Did the heading stay on the porch?",
        "E045": "What is she learning from the way you drive?",
        "E046": "Are you going to tidy the mad-at-me line?",
        "E047": "Will you say his name out loud tonight?",
        "E048": "Can the day be complicated and still hold a blessing?",
        "E049": "Are you taking the saw, or staying on the floor?",
        "E050": "Did you stay on the floor when he was slow?",
        "E051": "Are you writing the true thing or the speech?",
        "E052": "What yoke are you picking back up?",
        "E053": "Did you knock, or did you give a weather report?",
        "E054": "Did you shut it down, or did like become a yoke?",
        "E055": "Are you going Saturday, or waiting to feel fire?",
        "E056": "Is the feeling the fire, or just your chest?",
        "E057": "Are you living the day you have, or sitting in the lobby?",
        "E058": "Did you write the four, or leave them in the attic?",
        "E059": "What question would change your week if she answered?",
        "E060": "Did you hear her, or start a plan?",
        "E061": "What unnamed thing are you still holding?",
        "E062": "Did you pick the door, or write about coming back?",
        "E063": "Will you ask her tonight, on a calm night?",
        "E064": "Company or quiet — which did she actually say?",
        "E065": "Where does the charger live when the shift starts?",
        "E066": "Did you tell the hiding place, or wait for a crisis?",
        "E067": "Can a child read like on your fridge?",
        "E071": "What unseen thing will you refuse to report?",
        "E072": "Did you open the gym nobody thanks you for?",
        "E073": "What are you afraid of when you pick up the keys?",
        "E075": "Which season are you treating like it doesn't count?",
        "E080": "What one thing will you say you miss?",
    },
)

add(
    "Look around your house this week.",
    {
        "E001": "Walk the rooms you keep saying you'll finish.",
        "E002": "Check the basket before Friday supper.",
        "E006": "Say the sentence in the kitchen, not in your head.",
        "E008": "Look at the thing still sitting on the counter.",
        "E010": "Notice the load you picked up that isn't yours.",
        "E011": "See where you should have gone first this week.",
        "E012": "Look at the Valentine leftover and the ash.",
        "E013": "Check the prize you still want by Thursday.",
        "E014": "Look at what actually stuck after six weeks.",
        "E015": "Find the part that's yours and leave the rest.",
        "E019": "Name the fear under the heat before dark.",
        "E021": "Watch where the itch turns into a drift.",
        "E025": "Look at who stays when the room gets quiet.",
        "E029": "Look at the number you still haven't dialed.",
        "E030": "Check whether the call left the notes app.",
        "E031": "See whether home has handed you off yet.",
        "E032": "Look at the string you keep saying you'll cut.",
        "E033": "Watch how you leave a room this week.",
        "E035": "Look at how you talk to her as a grown son.",
        "E036": "Check what you actually did, not what you posted.",
        "E037": "Look at the men you treat like brothers.",
        "E038": "See what's still undone from the father-who-stays week.",
        "E042": "Look at the living name you keep postponing.",
        "E044": "Check the heading on the fridge before Thursday.",
        "E046": "Look at the truck window and the unsent photo.",
        "E048": "Look at the complicated day and still bless someone.",
        "E050": "Look at the floor you left when he was slow.",
        "E052": "Look at the yoke you pick back up after the porch.",
        "E054": "Look at whether you shut the work down tonight.",
        "E055": "Look at the Saturday you keep waiting to feel.",
        "E056": "Look at the stain and the door you still lift.",
        "E058": "Look at the four lines you left in the attic.",
        "E059": "Look at the question you still haven't asked her.",
        "E060": "Look at whether you heard her or built a plan.",
        "E061": "Look at the unnamed thing in your hand.",
        "E062": "Look at the door you said you'd come back to.",
        "E063": "Look at the calm night you keep wasting.",
        "E064": "Look at company or quiet — which she named.",
        "E065": "Look at where the charger spends the night.",
        "E066": "Look at the hiding place you still haven't named.",
        "E067": "Look at the fridge the way a child would.",
        "E069": "Look at the work that was prepared, not the mood.",
        "E072": "Look at the gym nobody will thank you for.",
        "E073": "Look at the keys before you drive mad.",
        "E075": "Look at the season you treat like filler.",
        "E077": "Look at the job-shaped hole and the table that remains.",
        "E078": "Look at the days between jobs as if they count.",
        "E079": "Look at the table and who is still missing.",
        "E080": "Look at the one sentence you will say you miss.",
    },
)

add(
    "It sounds like a man who knows his calendar.",
    {
        "E020": "That sounds like twenty minutes with a real clock.",
        "E041": "That sounds like pancakes on a Thursday that already has a meeting.",
        "E042": "That sounds like a living call inside the holiday, not after it.",
        "E043": "That sounds like a heading that can survive dirty dishes.",
        "E044": "That sounds like three lines that stay on a porch.",
        "E045": "That sounds like a name said while the house is still loud.",
        "E046": "That sounds like fries on a Thursday that already has a meeting.",
        "E047": "That sounds like a name practiced in the room you're already in.",
        "E048": "That sounds like a text sent while the bruise is still there.",
        "E049": "That sounds like a boy on a slope before the week gets pretty.",
        "E050": "That sounds like a Saturday dated while the plane still sits.",
        "E051": "That sounds like a name in a lot, not a photo.",
        "E052": "That sounds like standing free after you've actually been set free.",
        "E053": "That sounds like a knock instead of another weather report.",
        "E054": "That sounds like empty pockets before the next like.",
        "E055": "That sounds like your name on a crew sheet, not a feeling.",
        "E056": "That sounds like three lines, an attic, and a door you still lift.",
        "E057": "That sounds like living the day you've got, not the lobby.",
        "E058": "That sounds like four lines written while the attic is still hot.",
        "E061": "That sounds like the unnamed thing finally getting a Tuesday.",
        "E065": "That sounds like a charger that lives in the truck, not the nightstand.",
        "E069": "That sounds like a name on foil on a Monday that already has a number.",
    },
)

add(
    "What are you picking, for real?",
    {
        "E042": "Shane or the chips — which one actually leaves your phone?",
        "E043": "Sink or slogan — which one gets the sticky note?",
        "E044": "Which refuse are you putting on the fridge tonight?",
        "E045": "Her name with the door open, or another quiet ride?",
        "E047": "Bud at bath, or another week of the tally?",
        "E048": "Name first then shut up — can you stop there?",
        "E049": "Coffee can on Saturday, or another speech about hills?",
        "E050": "Velcro on the floor, or taking the shoes again?",
        "E051": "July and a name, or a card that looks finished?",
        "E052": "The card on the counter, or another yoke?",
        "E053": "The library call, or another good-man weather report?",
        "E054": "The dresser tonight, or another cold supper?",
        "E055": "Your name on the sheet, or waiting to feel ready?",
        "E056": "Three lines and the attic, or eleven more feelings?",
        "E057": "The day you have, or another hour in the lobby?",
        "E058": "The four lines, or the girls question you keep stepping over?",
        "E059": "The question that might change the week — which one?",
        "E060": "Hearing her, or pricing another program?",
    },
)

add(
    "If I pick three I'll do none.",
    {
        "E039": "If I stack three asks I will cancel all three.",
        "E040": "If I load the week with men I will see none of them.",
        "E042": "If I try Shane and chips and a plate, I'll do the plate and hide.",
        "E043": "If I write three headings the sink still wins.",
        "E044": "If I refuse three things I will peek at the org chart.",
        "E045": "If I add a speech to her name I will say nothing.",
        "E046": "If I stack fries and a photo and a tidy text, I'll send the tidy text.",
        "E047": "If I keep nine names in the tally I will say none at bath.",
        "E048": "If I add a paragraph after his name I will make it weird.",
        "E049": "If I plan three hills I will stay in the truck.",
        "E050": "If I take the shoes and the saw I will skip the floor.",
        "E051": "If I chase a photo and a name and a booth, I'll get the booth.",
        "E052": "If I pick a card and a yoke and a speech, I'll pick the yoke.",
        "E053": "If I owe three calls I will give three weather reports.",
        "E054": "If I empty every pocket I will empty none.",
    },
)

add(
    "I've got about a minute and I want it on you.",
    {
        "E059": "I've got one minute and I want the question in your mouth.",
        "E060": "Sixty seconds. Ask her, then write what she said.",
        "E062": "One minute left. Pick the door. Come back if you forget.",
        "E063": "A minute. Ask tonight, on a calm night, before the scan.",
        "E064": "A minute for company or quiet. Not after the next crisis.",
        "E066": "A minute. Tell the hiding place before you leave this chair.",
        "E067": "A minute with no job. Write the line a child could read.",
        "E068": "A minute. Keep the line. Don't ask the duck to explain itself.",
        "E069": "A minute. Do the good that was prepared. A wire. A name. A lid.",
        "E070": "A minute. Sit the hour. Shake the names. Don't rush the gate.",
        "E071": "A minute. Write the letter. Send the short text. Don't report it.",
        "E072": "A minute. Open a gym you won't be thanked for.",
        "E073": "A minute. Name the fear. Then put the keys down.",
    },
)

add(
    "Here's what I want you to carry.",
    {
        "E045": "Take this with you: she's learning men from you first.",
        "E047": "Hold this: say his name. Don't ration proud.",
        "E048": "Keep this: if the day is complicated, tell the truth and still bless.",
        "E049": "Walk out with this: give him a hill. Be there. Don't take over.",
        "E050": "Leave with this: a hill isn't a straight line. Stay on the floor.",
        "E052": "Carry the porch, not the yoke you like picking up.",
        "E053": "Take the first job: work it and take care of it.",
        "E054": "Remember this: liking the work is allowed. Skipping shutdown is a yoke.",
        "E056": "Keep this: you're already called. Look where you're standing.",
        "E057": "Keep this: you're not in the lobby. You're already assigned.",
        "E058": "Keep this: the gift is already in your hands. Use it.",
        "E059": "Keep this: knowing her is a job. Memory isn't the work.",
        "E060": "Keep this: hearing is the job. The plan can wait.",
    },
)

add(
    "I've got a little under ten minutes, and I want the Bible open.",
    {
        "E059": "We've got a little under ten, and I want Proverbs on the table.",
        "E061": "Under ten minutes. Open to the verse about laying it down.",
        "E063": "Under ten. I want the need verse where we can see it.",
        "E065": "Under ten. Covenant language, not a mood.",
        "E067": "Under ten. I want the roommate verse read slow.",
        "E069": "Under ten. Prepared-good, not a pep talk.",
        "E071": "Under ten. The unseen verse, then we stop talking about claps.",
        "E073": "Under ten. Dash and wheel. I want the text in front of us.",
        "E075": "Under ten. Every season. Don't skip the line about time.",
        "E077": "Under ten. When the job goes. I want the text, not my story first.",
        "E079": "Under ten. Grief at the table. Open it before we get cute.",
    },
)

add(
    "Last few minutes on the tool.",
    {
        "E012": "Last few minutes on going first, not on the flowers.",
        "E018": "Last few minutes on the shape, while the fan is still quiet.",
        "E020": "Last few minutes on the twenty-minute rule.",
        "E022": "Last few minutes on the drift check you can run tonight.",
        "E024": "Last few minutes on what Good Friday actually asks.",
        "E026": "Last few minutes on the Easter receipt, not the feeling.",
        "E030": "Last few minutes on the call, not the draft.",
        "E032": "Last few minutes on the cut, while the string is still in your hand.",
    },
)

add(
    "Does that sound like a quota?",
    {
        "E050": "Does that sound like I'm turning a boy into a metric?",
        "E052": "Does that sound like I'm selling freedom as a product?",
        "E053": "Does that sound like I'm logging knocks for a review?",
        "E054": "Does that sound like I'm making shutdown a contest?",
        "E056": "Does that sound like I'm grading a chest for fire?",
        "E057": "Does that sound like I'm recruiting men out of the lobby?",
        "E058": "Does that sound like I'm counting lines so I can be done?",
        "E059": "Does that sound like I'm turning her into a homework set?",
    },
)

add(
    "Last few minutes on what we're actually doing.",
    {
        "E061": "Last few minutes on the unnamed thing, not the speech about it.",
        "E063": "Last few minutes on the ask, while the night is still calm.",
        "E065": "Last few minutes on the bed as a covenant, not a mood.",
        "E067": "Last few minutes on the fridge line a child could read.",
        "E069": "Last few minutes on the foil and the lid, not the calling feeling.",
        "E079": "Last few minutes on the table, and who you will name as missing.",
    },
)

add(
    "Honestly, I will try to add the speech anyway.",
    {
        "E034": "Honestly, I'll try to decorate the door report anyway.",
        "E035": "Honestly, I'll try to make Mother's Day a speech anyway.",
        "E036": "Honestly, I'll try to add a better closing than the one I had.",
        "E037": "Honestly, I'll try to recruit a brother with a paragraph anyway.",
        "E038": "Honestly, I'll try to tidy the season review anyway.",
        "E040": "Honestly, I'll try to turn coffee into a conversion anyway.",
    },
)

add(
    "We're about halfway, and I want the push.",
    {
        "E061": "We're about halfway, and I want you to push on laying it down.",
        "E063": "We're about halfway, and I want the push on what she needs.",
        "E065": "We're about halfway, and I want the push on the bed.",
        "E067": "We're about halfway, and I want the roommate push.",
        "E069": "We're about halfway, and I want the push on the work.",
        "E071": "We're about halfway, and I want the push on the unseen thing.",
    },
)

add(
    "Which one is sitting in you this week?",
    {
        "E041": "Luxury-on-a-holiday, or funeral-only — which man is you this week?",
        "E043": "Vision-is-for-executives, or slogan-on-a-wall — which one is you?",
        "E045": "The quiet teenager, or the good-grades story — which one is you?",
        "E047": "Names-are-just-words, or I-won't-say-proud — which one is you?",
        "E051": "Money-and-land, or I'm-disqualified — which excuse is yours?",
        "E053": "I-hate-the-job, or rest-is-for-soft-men — which one is sitting on you?",
    },
)

add(
    "If you're sitting in a driveway doing that too, write the three sentences down before you dial, then read only those three.",
    {
        "E036": "If you're in a driveway doing the same thing, write three lines for her before you call, then stop at three.",
        "E037": "If you do this too, write three brother-sentences on a card, then read only those.",
        "E038": "If you're parked and stalling, write three season-review lines, then say only those.",
        "E040": "If you're sitting on the ask, write three sentences, then dial before you improve them.",
    },
)
add(
    "I've left too many good talks on a table because I wanted a better closing line than the one I had.",
    {
        "E036": "I've left good Mother's Day talks on a table because I wanted a prettier last line.",
        "E037": "I've left brother-talks unfinished because I wanted a cleaner ending than I had.",
        "E038": "I've left season-review talks on the table waiting for a better last sentence.",
        "E040": "I've left good asks on a table because I wanted a conversion instead of coffee.",
    },
)
add(
    "The fourth sentence is where I get cute and ruin it.",
    {
        "E036": "Sentence four is where I get cute about Mom and ruin it.",
        "E037": "The extra sentence is where I recruit a brother and make it weird.",
        "E038": "The extra line is where I tidy the review and lose the truth.",
        "E040": "The fourth sentence is where I turn coffee into a pitch.",
    },
)
add(
    "Last few minutes on a tool you can use tonight.",
    {
        "E002": "Last few minutes on the first check you can still write tonight.",
        "E004": "Last few minutes on the sentence test you can run after supper.",
        "E008": "Last few minutes on the thing on the counter, before it becomes furniture.",
        "E010": "Last few minutes on putting down a load that was never yours.",
    },
)
add(
    "We're about halfway through the last stretch.",
    {
        "E009": "We're about halfway, and the weight still has your name on it.",
        "E011": "Halfway. I want the part where somebody has to go first.",
        "E013": "Halfway, and the Thursday prize is already going stale.",
        "E015": "Halfway. I want the part that's yours, not the borrowed one.",
    },
)
add(
    "The plane is still on the workbench.",
    {
        "E022": "That plane hasn't moved off the bench since I set it there.",
        "E034": "The plane is still sitting by the swollen jamb.",
        "E038": "Creek rock on the shelf, plane still waiting by the back door.",
        "E068": "There's dust on the plane. The back door still takes a lift.",
    },
)
add(
    "The water was there the whole time.",
    {
        "E059": "The water in that story was already there. I was the one late.",
        "E060": "She was already telling me. I just hadn't sat still.",
        "E075": "The season was already counting. I was the one calling it filler.",
        "E076": "The swap was already happening. I just hadn't named it.",
    },
)
add(
    "That's the only reason I trust it.",
    {
        "E034": "A dated Saturday is the only reason I trust myself on that jamb.",
        "E035": "A public calendar is the only reason I trust myself with her.",
        "E036": "Writing it down is the only reason I trust the Mother's Day version.",
        "E037": "A name on a card is the only reason I trust the brother move.",
    },
)
add(
    "Pick the one door that's yours.",
    {
        "E034": "Pick the family door that's actually yours this week.",
        "E035": "Pick the grown-son door, not the helper door.",
        "E036": "Pick one Mother's Day door and walk it.",
        "E037": "Pick one brother door. Not a group chat.",
    },
)
add(
    "Mine is already on a calendar.",
    {
        "E034": "Mine is a Saturday on the jamb, written where I can see it.",
        "E035": "Mine is already next to PT with Mom.",
        "E036": "Mine is already on the Mother's Day card, in ink.",
        "E037": "Mine is already a Thursday with a living man.",
    },
)
add(
    "What is the version of this sitting on your calendar, and who is covering for you while you wait?",
    {
        "E034": "What's the version of this door on your calendar, and who is covering while you stall?",
        "E035": "What's the grown-son version on your week, and who is covering for the boy in you?",
        "E036": "What's the Mother's Day version on paper, and who is covering while you draft?",
    },
)
add(
    "A man will hear a story and start fixing the next guy instead of looking at his own kitchen.",
    {
        "E034": "A man will hear a door story and start fixing his neighbor's hinge.",
        "E035": "A man will hear a mom story and start coaching somebody else's son.",
        "E036": "A man will hear a Mother's Day story and start correcting the next guy.",
    },
)
add(
    "Let's take the next few minutes on what we actually did, because Friday is the receipt.",
    {
        "E002": "Let's take the next few minutes on the first check, because Friday is the receipt.",
        "E004": "Let's take the next few minutes on the sentence you said, because Friday is the receipt.",
        "E008": "Let's take the next few minutes on the counter, because Friday will show if it moved.",
    },
)
add(
    "I'll be real with you, I want a cleaner ending than that, and I'm not getting one.",
    {
        "E034": "I'll be real: I want the jamb to resolve in one Saturday, and it won't.",
        "E035": "I'll be real: I want a cleaner Mother's Day ending than I'm getting.",
        "E036": "I'll be real: I want a neater last line than the one I have.",
    },
)
add(
    "I can live with unfinished if I stop using unfinished as a reason to hide.",
    {
        "E034": "I can live with a swollen jamb if I stop using it as cover.",
        "E035": "I can live with unfinished with Mom if I stop hiding behind it.",
        "E036": "I can live with an unfinished card if I stop using it as a stall.",
    },
)
add(
    "Last few minutes I want this back in your house, not in ours.",
    {
        "E034": "Last few minutes I want this back at your jamb, not at mine.",
        "E035": "Last few minutes I want this back in your talk with her.",
        "E036": "Last few minutes I want this back on your card, not on this table.",
    },
)
add(
    "I used the first miss as a way out for most of my twenties.",
    {
        "E035": "I used the first miss with her as a way out for most of my twenties.",
        "E036": "I used one missed call as a decade of 'I'll do it next year.'",
        "E040": "I used the first canceled ask as a way out for most of my twenties.",
    },
)
add(
    "Love God out loud, keep the people He gave me, and finish.",
    {
        "E043": "Love God out loud, keep the people on the porch, and finish the heading.",
        "E044": "Love God out loud, keep her Tuesdays, and finish the three lines.",
        "E055": "Love God out loud, keep the Saturday names, and finish the sheet.",
    },
)
add(
    "That's the part that keeps me honest at this table.",
    {
        "E034": "That's the part that keeps me honest about the jamb.",
        "E035": "That's the part that keeps me honest about being her son.",
        "E036": "That's the part that keeps me honest about the card.",
    },
)
add(
    "Let's take the next few minutes on the receipt.",
    {
        "E030": "Let's take the next few minutes on whether the call left the phone.",
        "E032": "Let's take the next few minutes on whether the string actually got cut.",
        "E072": "Let's take the next few minutes on the unseen shift you actually made.",
    },
)
add(
    "I've got one more minute and I want it on you.",
    {
        "E063": "I've got one more minute. Ask her while the night is still calm.",
        "E072": "One more minute. Open the gym nobody claps for.",
        "E073": "One more minute. Name the fear, then leave the keys on the hook.",
    },
)
add(
    "Does that sound like I'm arguing with Paul?",
    {
        "E062": "Does that sound like I'm scolding Paul about a door?",
        "E064": "Does that sound like I'm picking a fight with Paul about her need?",
        "E068": "Does that sound like I'm cross-examining Paul about roommates?",
    },
)
add(
    "I'm trying not to do that at thirty-seven.",
    {
        "E035": "I'm trying not to stay the helper-son at thirty-seven.",
        "E036": "I'm trying not to draft Mother's Day until I'm thirty-eight.",
        "E040": "I'm trying not to cancel the ask at thirty-seven.",
    },
)
add(
    "If you tried it, or if you didn't, stay.",
    {
        "E002": "If you wrote the check, or if you only thought about it, stay.",
        "E004": "If you said the sentence, or if you swallowed it, stay.",
        "E056": "If you went to the attic, or if you only felt fire, stay.",
    },
)
add(
    "We've got a little under ten minutes.",
    {
        "E023": "We've got a little under ten, and I want both gardens on the table.",
        "E025": "We've got a little under ten, and I want the father who stays.",
        "E027": "We've got a little under ten, and I want the empty chair named.",
    },
)
add(
    "Last few minutes on the challenge.",
    {
        "E009": "Last few minutes on picking up the weight with your name on it.",
        "E011": "Last few minutes on the step out ahead, not the speech about it.",
        "E013": "Last few minutes on the prize that's already going stale.",
    },
)
add(
    "I don't want to rush past that.",
    {
        "E034": "I don't want to rush past a door that still needs a plane.",
        "E035": "I don't want to rush past her as if the day were simple.",
        "E036": "I don't want to rush past the card like it's a chore.",
    },
)
add(
    "That's the only week it costs.",
    {
        "E069": "That's the only week the foil costs you.",
        "E072": "That's the only week the unseen gym costs you.",
        "E073": "That's the only week putting the keys down costs you.",
    },
)
add(
    "Ask one thing you don't know.",
    {
        "E045": "Ask her one thing you don't already have graded.",
        "E046": "Ask one thing you don't already have an answer for.",
        "E059": "Ask her one thing whose answer might rearrange the week.",
        "E060": "Ask her one thing, then write it before you invent a plan.",
    },
)
add(
    "Don't be that man this week.",
    {
        "E035": "Don't be the helper-son who never becomes the grown one.",
        "E036": "Don't be the man who drafts the card and never sends it.",
        "E046": "Don't be the man who collects a daughter report and never buys fries.",
    },
)
add(
    "Don't hold me to a speech.",
    {
        "E046": "Don't hold me to a tidy paragraph. Hold me to the unsent text.",
        "E061": "Don't hold me to a speech about laying it down. Hold me to the unnamed thing.",
        "E065": "Don't hold me to a talk about the bed. Hold me to where the charger lives.",
    },
)
add(
    "So which is it this week?",
    {
        "E026": "So which is it this Easter week — receipt or feeling?",
        "E038": "So which is it this review — creek rock or another speech?",
        "E040": "So which is it this week — coffee, or another canceled ask?",
    },
)
add(
    "Not yet is still not yet.",
    {
        "E038": "Not yet on the jamb is still a lift every time.",
        "E048": "Not yet on the blessing is still an empty Thursday.",
        "E049": "Not yet on the hill is still a boy in the truck.",
    },
)
add(
    "So which is it for you?",
    {
        "E035": "So which is it for you — grown son, or helper with a good excuse?",
        "E036": "So which is it for you — a card in ink, or another draft?",
        "E039": "So which is it for you — the man, or the screen?",
    },
)
add(
    "Not a man on a screen.",
    {
        "E036": "Not a tribute post. A voice.",
        "E037": "Not a man in a group chat. A living one.",
        "E040": "Not a man on a screen. A day before supper.",
    },
)
# Fix similar halfway/push lines created in wave 1
add(
    "We're about halfway, and I want you to push on laying it down.",
    {"E061": "Halfway. Push me on the unnamed thing I'm still carrying."},
)
add(
    "We're about halfway, and I want the push on what she needs.",
    {"E063": "Halfway. I want you to argue with me about her need."},
)
add(
    "We're about halfway, and I want the push on the bed.",
    {"E065": "Halfway. Don't let me get poetic about the bed."},
)
add(
    "We're about halfway, and I want the roommate push.",
    {"E067": "Halfway. Push on the fridge like a child would."},
)
add(
    "We're about halfway, and I want the push on the work.",
    {"E069": "Halfway. Push on the foil and the lid, not the calling feeling."},
)
add(
    "We're about halfway, and I want the push on the unseen thing.",
    {"E071": "Halfway. Push on the letter I haven't mailed."},
)


def ep_of(path):
    return os.path.basename(path)[:4]


def apply_file(path):
    ep = ep_of(path)
    if ep == "E007":
        return 0
    text = open(path, encoding="utf-8").read()
    n = 0
    for original, mapping in MAP.items():
        if ep not in mapping:
            continue
        repl = mapping[ep]
        if original not in text:
            continue
        count = text.count(original)
        if count == 1:
            text = text.replace(original, repl, 1)
            n += 1
        else:
            # replace each occurrence with the same ep-unique line once;
            # leftover intra-file copies get a numbered tweak below.
            text = text.replace(original, repl)
            n += count
    if n:
        open(path, "w", encoding="utf-8").write(text)
    return n


def main():
    files = sorted(
        os.path.join(ROOT, f)
        for f in os.listdir(ROOT)
        if f.startswith("E0") and f.endswith(".md") and not f.endswith("show-notes.md")
    )
    total = 0
    for p in files:
        n = apply_file(p)
        if n:
            print(f"{os.path.basename(p):52} {n:3}")
            total += n
    print(f"replaced {total} stock sentences")


if __name__ == "__main__":
    main()
