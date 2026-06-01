---
name: zeitgeist-decoder
description: Decode cultural signals, semiotics, and search intent into defensible marketing strategy for in-house teams. Use this skill whenever the user mentions cultural trends, zeitgeist, semiotics, trend reports, cultural insight, audience analysis, keyword research with demographic or geographic angles, search intent, brand permission, cultural codes, or wants to turn a cultural observation into a brief, deck, or one-pager. Trigger even when the user describes the task in plain language ("help me figure out if my brand can talk about X", "what does this trend actually mean", "is this just hype or a real shift", "find me keywords for this audience in this city"); they are asking for cultural decoding even if they don't use the word. Also trigger when the user wants to sanity-check whether a creative idea is grounded in a real cultural shift versus a passing meme.
---

# Zeitgeist Decoder

A 5-phase cultural strategy workflow for in-house marketing teams. The goal is to turn a vague cultural observation into a defensible point of view, backed by semiotic rigor, search-demand reality, and an artifact the team can present.

Most "trend reports" fail because they describe what is happening without explaining what it *means*, who has permission to talk about it, or whether anyone is actually searching for it. This skill enforces the discipline of going through five phases in order. Do not skip ahead — each phase produces an input the next phase needs.

## Core principles

**Decode before opining.** Marketing teams jump from "I saw a TikTok" to "we should do a campaign" in 90 seconds. That's how brands end up cringe. Run the semiotic decode in Phase 2 before forming any creative or strategic recommendation.

**Permission is real.** Brands do not have equal rights to every cultural conversation. Phase 3 forces a permission audit. A B2B SaaS brand commenting on Brat summer is a different proposition than Charli XCX commenting on Brat summer. Be honest about where the user's brand sits.

**Search demand is the receipt.** Cultural intuition is necessary but not sufficient. Phase 4 forces a keyword reality check — if nobody is searching, the "trend" may be a media bubble. The keyword estimator script gives directional volumes by geography and demographic, and shows its math so the strategist can defend the numbers in a meeting.

**Output an artifact.** A conversation is not a deliverable. Phase 5 always produces a file the user can send, present, or upload — a trend brief, a cultural deck outline, or a keyword cluster sheet.

**Kill the clichés.** Marketing writing collapses into jargon by default. The cliché killlist (see `references/cliche-killlist.md`) is applied to every piece of written output before the artifact is finalized. The `scripts/cliche_lint.py` script automates this — run it on any draft text before saving.

---

## The 5-phase workflow

When a user comes in with a cultural observation, trend question, audience question, or request for a brief/deck, follow these phases in order. Announce the phase you are on. At the end of each phase, summarize what was decided and confirm before moving to the next phase — this is what makes it a workflow rather than a one-shot answer.

### Phase 1 — Signal capture

Goal: get a precise description of the cultural artifact, behavior, phrase, aesthetic, or shift the user is interested in. Strip out opinion and interpretation. Just describe what is observable.

Ask the user, if not already clear:
- What is the signal? (a phrase, a behavior, an aesthetic, a product, a meme, a sub-genre, a tension)
- Where did you encounter it? (platform, geography, sub-community)
- How long has it been visible to you?
- Who is the brand or team this analysis is for? What category?

Do not interpret yet. If the user offers interpretation ("I think it means Gen Z is rejecting..."), park it for Phase 2.

Exit gate: a one-paragraph signal description that a stranger could read and recognize. No "means," "represents," or "shows that" verbs allowed in this paragraph.

### Phase 2 — Semiotic decode

Goal: separate what the signal literally is from what it culturally means. Use the two frameworks in `references/semiotics-frameworks.md` — read that file now if you have not already this session.

Apply, in this order:
1. **Barthes' three layers** — denotation (what it literally is), connotation (associated meanings), myth (the ideology it naturalizes).
2. **Williams' residual / dominant / emergent** — is this a leftover from a past cultural era (residual), the mainstream now (dominant), or a signal of what is coming (emergent)? This is the single most important call to make, because it dictates strategy. A brand acting on a residual signal is nostalgic. A brand acting on a dominant signal is on-trend but undifferentiated. A brand acting on an emergent signal is pioneering — and risks being early.
3. **Floch's semiotic square** (optional, use when there's a clear tension) — map the signal against its opposite, contradiction, and complementary term to find unowned territory.

Exit gate: a written decode that names the denotation, connotation, myth, and the residual/dominant/emergent call with a one-sentence justification.

### Phase 3 — Audience permission map

Goal: figure out who owns this signal culturally, who would be cringe to touch it, and where the user's brand actually sits.

Read `references/strategy-frameworks.md` for the relevant frameworks — particularly Holt's cultural branding (does the brand resolve a cultural contradiction?) and Sharp's mental availability (does the brand have enough salience to be heard if it speaks?).

Produce:
- **Native owners** — who has full permission (the originators, the in-community voices)
- **Adjacent permission** — brands/creators who can play in this space credibly
- **No-fly zone** — categories where touching this signal would be cringe or extractive
- **Where the user's brand sits** — adjacent, no-fly, or genuinely native? Be honest. Most brands are adjacent at best. If the user's brand is in the no-fly zone, say so and recommend either passing on the trend or finding the adjacent angle.

Exit gate: a permission verdict — green (act on it), yellow (act on it with a specific angle), or red (do not act, but here's what to do instead).

### Phase 4 — Search reality check

Goal: pressure-test the cultural signal against actual search demand, broken out by geography and demographic.

Read `references/search-intent-taxonomy.md` and `references/geo-demographic-modifiers.md`.

Steps:
1. Generate 8–15 keyword candidates that map to the signal. Cover the full intent spectrum (informational, navigational, commercial, transactional).
2. For each keyword, classify the intent and the likely audience segment.
3. Run the volume estimator script:
   ```bash
   python3 scripts/keyword_estimator.py \
     --keywords "keyword1,keyword2,keyword3" \
     --geo "in-delhi" \
     --demo "millennial-urban-male" \
     --anchor-volume 10000
   ```
   The script returns estimated monthly searches with the math shown (base anchor × geo modifier × demographic modifier × intent decay). Always cite the script's output as *directional, not definitive* — recommend the user validate top candidates in Google Keyword Planner, Semrush, or Ahrefs.
4. Interpret the gap between cultural buzz and search demand. High buzz + high search = real shift. High buzz + low search = media bubble or pre-search (emergent — interest exists but doesn't yet have a keyword). Low buzz + high search = latent demand the trend writers missed.

Exit gate: a keyword cluster table with intent, estimated volume, and a one-line interpretation of the buzz-vs-search gap.

### Phase 5 — Artifact generation

Goal: produce a file the user can present.

Ask the user which artifact they need (or infer from earlier conversation):
- **Trend brief** — one-pager, ~400 words, for circulation to the team. Use `assets/trend-brief-template.md`.
- **Cultural deck outline** — slide-by-slide structure for a presentation. Use `assets/cultural-deck-template.md`.
- **Keyword cluster sheet** — CSV with keywords, intent, volume, audience. Use `assets/keyword-cluster-template.csv`.
- All three, if it's a full project.

Before finalizing any written artifact, run the cliché linter:
```bash
python3 scripts/cliche_lint.py --file <path-to-draft.md>
```
The linter scans for marketing jargon, AI-tells (em-dash overuse, rule-of-three sentences, hollow superlatives, "in today's fast-paced world" openers, etc.) and returns specific rewrites. Apply the rewrites before saving the final artifact.

Save the artifact to the user's output directory (`/mnt/user-data/outputs/` when running in Claude.ai). Use `present_files` to make it accessible.

Exit gate: a saved file path the user can open, plus a one-paragraph summary of what they're about to read.

---

## When to deviate from the workflow

The 5-phase order is the default for a fresh cultural question. Deviate if:

- **User is mid-phase already.** If they walk in with a signal description and a decode already done, jump to Phase 3. Don't make them repeat work.
- **User wants only keyword research.** Run Phase 1 lightly, skip 2 and 3, focus on Phase 4 and a keyword-sheet artifact. But always offer: "I can also run a semiotic decode on this if you want a richer brief — takes 5 more minutes."
- **User explicitly says "skip the framework stuff."** Respect it. Run a fast, intuition-led version, but flag the risk: "Without the decode you might end up with a recommendation that looks smart but isn't defensible in a room with a strategy director."

## Output conventions

- Use Indian English spellings if the user is based in India (this user is in Delhi by default; confirm if unclear). "Colour," "behaviour," "favourite," "organisation."
- Currency in INR for Indian-market briefs; specify when switching to USD/EUR/GBP for other markets.
- Do not use em-dashes (—) in user-facing output artifacts (trend briefs, decks, keyword sheets, copy). They are the single strongest AI-tell in marketing writing. Use commas, semicolons, sentences, colons, or parentheses instead. The cliché linter flags them. Em-dashes in internal scaffolding (headings, structural markers) are acceptable.
- Do not open paragraphs in output artifacts with "In today's...", "In an era of...", "It's no secret that...", or any other generic stage-setter.
- Avoid the rule-of-three sentence structure in output ("It's bold, beautiful, and brilliant") unless the third item genuinely adds information.
- If the user asks for a "deep dive," that means more research, not more adjectives.

## Reference files

- `references/semiotics-frameworks.md` — Barthes, Williams, Floch. Read in Phase 2.
- `references/strategy-frameworks.md` — Sharp, Sutherland, Ogilvy, Holt. Read in Phase 3.
- `references/cliche-killlist.md` — banned phrases, AI-tells, rewrite patterns. Reference in Phase 5.
- `references/search-intent-taxonomy.md` — four intent types with examples. Read in Phase 4.
- `references/geo-demographic-modifiers.md` — search behavior shifts by region/age/income. Read in Phase 4.

## Asset templates

- `assets/trend-brief-template.md` — one-pager structure
- `assets/cultural-deck-template.md` — deck slide-by-slide
- `assets/keyword-cluster-template.csv` — keyword sheet format

## Scripts

- `scripts/keyword_estimator.py` — directional volume estimation by geo/demo
- `scripts/cliche_lint.py` — jargon and AI-tell scanner with rewrites

Run scripts with `python3` from the skill directory.
