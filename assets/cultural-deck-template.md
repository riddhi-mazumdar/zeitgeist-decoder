# Cultural deck template: slide-by-slide structure

*A 14-slide structure for presenting a cultural opportunity to internal stakeholders. Each slide has one job. Resist the urge to over-design: clarity wins rooms, not animation.*

---

## Slide 1: Title

**One line.** The cultural signal, named. Not a question. Not a tease.

Example: "The Soft Life Migration" not "What if there's a generation rejecting hustle?"

Subtitle: who prepared it, for whom, when.

## Slide 2: The opening image

**One image, no headline.** A photo, screenshot, or artifact that *is* the signal. Make the audience see it before you describe it. Stay on this slide for 15 seconds in silence if you can.

## Slide 3: What you're looking at

The signal described in two short paragraphs. Pure Phase 1: observation, no interpretation. End with "Here's what we think it means." (Transition to the decode.)

## Slide 4: Denotation, connotation, myth

A three-column layout:

| Denotation | Connotation | Myth |
|---|---|---|
| [literal] | [references] | [worldview naturalised] |

The myth column is the only one that should be a complete sentence. The other two are phrases.

## Slide 5: Residual, dominant, or emergent?

A three-position timeline visualisation. Place the signal on one of the three positions. One sentence justifying.

This is the most important slide in the deck. Spend time defending it. If the audience pushes back, this is where they'll do it.

## Slide 6: Who has permission

A 2x2 or three-tier diagram:

- Native owners (the originators)
- Adjacent permission (credible adjacents)
- No-fly zone (categories that would be extractive)

Show 3–5 specific brands or creators in each tier. Avoid hypothetical examples: name names the audience will recognise.

## Slide 7: Where we sit

A single arrow or pin showing your brand's position on the permission map. One sentence:

"[Brand] sits in [adjacent / native / no-fly] because [specific reason: product, heritage, audience overlap, or contradiction it resolves]."

If the brand is no-fly, this is where you make the case for not acting. Do not dress up a red light as a yellow one.

## Slide 8: The strategy framework lens

Pick one or two of the four frameworks (Sharp, Sutherland, Ogilvy, Holt) that most clearly support the verdict. Apply, in two short paragraphs.

Example: "Sharp's frame: this action will not build mental availability unless we anchor it in [distinctive brand asset]. Holt's frame: the underlying contradiction here is [X], and our brand can credibly resolve it because [Y]."

## Slide 9: Search reality

The keyword cluster table. 6–10 rows. Include intent and estimated volume.

Caption below: "Volumes are directional, validated against [source if applicable]. Cross-validate top candidates before media commit."

## Slide 10: The gap

One slide on the buzz-vs-search gap. A simple 2x2 (high/low buzz × high/low search), with the signal placed on it.

The placement tells the room which kind of opportunity this is:
- High buzz + high search = real shift, act now, expect competition
- High buzz + low search = either media bubble or pre-search emergent (different actions)
- Low buzz + high search = latent demand, undervalued by trend writers
- Low buzz + low search = not a trend, move on

## Slide 11: Verdict

One word at the top: **GREEN / YELLOW / RED**

Below: one paragraph explaining the verdict.

Use the same colour the slide describes: but resist over-designing. The word is the slide.

## Slide 12: The angle

If green or yellow: the specific creative or strategic angle to take. One paragraph. This is the slide the creative team will work from, so make it actionable.

If red: the alternative recommendation. What should the team do instead, given the underlying audience need.

## Slide 13: Next steps

A short list of specific, dated actions:

- [Action]: owner: [name]: by: [date]
- [Action]: owner: [name]: by: [date]
- [Action]: owner: [name]: by: [date]

Limit to 3–5 actions. More than that and nothing will get done.

## Slide 14: Sources and methodology

The artifacts that informed the brief (links, screenshots, quotes). Plus a one-line note:

"Methodology: zeitgeist-decoder skill. Semiotics from Barthes / Williams. Strategy lenses from Sharp / Sutherland / Ogilvy / Holt. Search estimates directional."

---

## Speaker notes: what to say in the room

**On slide 5 (R/D/E):** "I want to flag this is the call we should debate. Everything downstream rests on it. Here's why I'm calling it [emergent / dominant / residual]..."

**On slide 7 (where we sit):** "I want to be honest about our permission here. Brands routinely overestimate how native they are to a cultural conversation. Let me show you my reasoning."

**On slide 10 (the gap):** "Cultural buzz alone is not a strategy. This 2x2 is how we pressure-test whether what we're seeing in feeds matches actual demand."

**On slide 11 (verdict):** Say the word. Then pause. Then explain. Don't bury the verdict in qualifications.

---

## What not to do

- Do not put more than one idea on a slide.
- Do not use the rule of three in headlines ("Bold. Beautiful. Brilliant.").
- Do not use stock photos of "diverse people pointing at laptops."
- Do not use the em-dash. Anywhere. The cliché linter will catch it; pre-empt.
- Do not use words like "robust," "leverage," "synergy," "unlock," "empower" in the deck. Run the linter on the deck text before exporting.
- Do not promise a "movement" or "revolution." Promise specific outcomes.

When the deck is drafted, run:
```bash
python3 scripts/cliche_lint.py --file deck-text.md
```
Fix all banned items before exporting to PowerPoint, Keynote, or Google Slides.
