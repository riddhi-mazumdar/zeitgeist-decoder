# The cliché killlist

Marketing writing dies of jargon. So does AI-assisted writing. This list is the standard the cliché linter enforces and the standard you should hold every written output to in Phase 5. When you find any of these in a draft, rewrite. When the user pushes back, hold the line.

## Banned phrases (no exceptions)

These phrases are dead. They contributed something once. They no longer do.

- "In today's fast-paced world"
- "In an era of"
- "It's no secret that"
- "Now more than ever"
- "Unprecedented times"
- "The new normal"
- "Game-changer" / "game-changing"
- "Disruptor" / "disrupting the industry"
- "Synergy" / "synergies"
- "Move the needle"
- "Low-hanging fruit"
- "Take it to the next level"
- "Best-in-class"
- "World-class"
- "Cutting-edge" (use only with a specific, verifiable claim)
- "State-of-the-art" (same — needs a specific reason)
- "Robust" (almost always means "we don't know how to describe this")
- "Solutions" as a generic noun ("our solutions for...")
- "Leverage" as a verb
- "Unlock" (as in "unlock potential," "unlock value")
- "Empower" / "empowering" (overused to the point of meaninglessness)
- "At the end of the day"
- "Going forward"
- "Reach out" (use "email," "call," "ask")
- "Circle back"
- "Deep dive" (when used as a noun for a paragraph that is not actually deep)
- "Curated" (every brand "curates" now, the word has collapsed)
- "Bespoke" (same)
- "Artisanal" (same)
- "Hand-crafted" (allowed only when literally true)
- "Storytelling" as a brand activity (almost always means "we wrote some captions")
- "Authentic" / "authenticity" (the most ironic word in marketing — when you have to say it, you don't have it)
- "Resonates" / "resonant" (overused; use "lands," "matters to," "speaks to")
- "Tap into" (as in "tap into the cultural moment")
- "Conversation" as a marketing noun ("join the conversation")
- "Journey" (customer journey is fine in operational contexts; "their journey" in copy is dead)

## AI-tells (the patterns that make writing read as machine-written)

These are the structural patterns Wikipedia's "Signs of AI writing" guide flagged, plus a few specific to marketing.

### Em-dash overuse
The em-dash (—) is a sophisticated punctuation mark. AI uses it three times per paragraph. Humans use it once per page. **Rule for this skill: no em-dashes at all in output.** Use commas, semicolons, sentences, or colons.

Before: "The product is fast — really fast — and it works."
After: "The product is fast. Really fast. And it works." Or: "The product is fast (genuinely so) and it works."

### Rule of three
"It's bold, beautiful, and brilliant." "We are passionate, persistent, and people-first." Three-item lists where the third item adds nothing but rhythm.

Rule: every item in a three-item list must add information. If the third is a rhythm-filler, cut to two or replace with one strong item.

### Negative parallelism
"It's not about X. It's about Y." Used once, this is fine. Used three times in a piece, it becomes a tic.

### Hollow superlatives without evidence
"Revolutionary." "Groundbreaking." "Transformative." Words that claim importance without providing it. If something is revolutionary, describe the revolution.

### "Indeed," "Moreover," "Furthermore" as paragraph-openers
Connector words doing the work that the argument should be doing. Cut them; let the next sentence do its own connecting.

### Inflated symbolism
"This is more than a campaign — it's a movement." (See em-dash too.) "It's not just a product, it's a philosophy." Almost always false, and the reader knows.

### Promotional language smuggled into supposedly neutral copy
"The visionary founder," "the iconic brand," "the beloved category leader." Adjectives that are doing the persuasion the facts should be doing.

### Superficial -ing analyses
"Brands are increasingly leveraging cultural moments, driving deeper engagement and unlocking new audiences." A sentence built entirely of marketing-flavoured present participles. No subject is doing anything specific.

### Vague attributions
"Studies show," "experts say," "research suggests." Either name the study and link it, or don't claim it.

### Excessive conjunctive phrases
"However, that being said, on the other hand, it should be noted that..." Pick one connector. The rest are throat-clearing.

## Rewrite patterns

When you find a banned phrase or AI-tell, here are the substitutions:

| Found | Replace with |
|---|---|
| "In today's fast-paced world" | Just delete it. Start with the actual point. |
| "Game-changing" | Specific verb: "halves," "doubles," "eliminates," "replaces" |
| "Leverage" | "Use" |
| "Unlock" | Cut, or replace with the literal action |
| "Empower" | Replace with what the thing actually lets people do |
| "Robust" | Specific quality: "fast," "reliable," "handles 10x load" |
| "Curated" | "Chosen," "selected," or describe the selection criterion |
| "Authentic" | Show, don't tell. Cut the word and let the evidence speak. |
| "Resonates with" | "Matters to," "speaks to," "lands with" |
| "Storytelling" | Name the actual format: "the films," "the captions," "the brand book" |
| "Cutting-edge tech" | Name the tech |
| Em-dash | Comma, sentence break, semicolon, colon, or parentheses |
| Hollow rule-of-three | Cut the weakest item |
| "Revolutionary" | Describe what is actually new |
| "More than a campaign, it's a movement" | Delete the whole sentence. Movements are not announced by their organisers. |

## What good marketing copy reads like (counterexamples)

For calibration, the standard the skill is trying to hit:

> "We deal with people who never go to the cinema." — actual line from a 1990s UK trade-press ad for an out-of-home media owner. Specific, surprising, claims something defensible.

> "Avis is only No. 2. We try harder." — Doyle Dane Bernbach, 1962. Admits a weakness, turns it into a positioning. No jargon.

> "The best a man can get." — Gillette, 1989. Five words. Specific brand promise. Has lasted 30+ years.

> "Probably the best beer in the world." — Carlsberg, 1973. The "probably" is the whole joke and the whole positioning.

Notice what these have in common: specific, short, no jargon, often a small surprise, and a clear point of view. The skill should produce copy in this register, not in the "in today's fast-paced world" register.

## How the linter uses this list

The `cliche_lint.py` script scans drafts for the banned phrases and AI-tells in this document. It returns:
- Found phrase
- Line and column
- Severity (banned / warning)
- Suggested rewrite

The strategist applies the rewrites before saving the final artifact. Do not save a draft that still contains banned phrases. The whole point of the skill is to produce work that does not sound like every other agency's deck.
