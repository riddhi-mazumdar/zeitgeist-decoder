# zeitgeist-decoder

**A Claude skill for in-house marketing teams who are tired of trend reports that don't decode anything.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blueviolet)](https://docs.claude.com)

---

## What this is

A structured cultural-strategy workflow, packaged as a Claude skill. It turns a vague cultural observation ("everyone's talking about soft life") into a defensible point of view backed by semiotic rigor, brand-permission analysis, and search-demand reality.

It does five things, in order, every time:

1. **Captures the signal** without letting you jump to interpretation
2. **Decodes meaning** using Barthes (denotation / connotation / myth) and Williams (residual / dominant / emergent)
3. **Audits permission** through Sharp, Sutherland, Ogilvy, and Holt
4. **Pressure-tests against search demand** with intent classification and geography/demographic-weighted volume estimates
5. **Outputs a real artifact** — a one-pager brief, a 14-slide deck structure, or a keyword cluster CSV

Plus a cliché linter that scans your draft for marketing jargon and AI-tells (em-dash overuse, "in today's fast-paced world," rule-of-three, vague attributions, etc.) and returns specific rewrites.

## Why this exists

Most "trend reports" describe what is happening without explaining what it means, who has permission to talk about it, or whether anyone is actually searching for it. Most "cultural insights" stop at connotation when the strategic gold is at the myth layer. Most keyword lists have no intent classification and no demographic adjustment, so the volumes are misleading.

This skill makes Claude follow a discipline. Discipline is what separates a strategist from a TikTok scroller.

## Who it's for

Built for in-house marketing teams (brand, strategy, content, growth). Useful for:

- Brand strategists at D2C and consumer brands
- Content teams who need to decide whether to chase a cultural moment
- Growth marketers who need to map cultural signals to search demand
- Founders doing their own marketing
- Agency teams who want to ship more rigorous strategy decks

Not for: pure performance marketing (use Semrush/Ahrefs directly), or pure community management (different workflow).

## Installation

### Option 1: Direct download

1. Download or clone this repo
2. In Claude.ai (Pro / Team / Enterprise), go to **Settings → Capabilities → Skills**
3. Upload the `zeitgeist-decoder` folder as a skill

### Option 2: Clone and use locally

```bash
git clone https://github.com/[your-username]/zeitgeist-decoder.git
cd zeitgeist-decoder
```

The scripts (`keyword_estimator.py` and `cliche_lint.py`) run on any system with Python 3.8+. No external dependencies — pure standard library.

### Option 3: Package as a .skill file

If you have the skill-creator skill installed:

```bash
python3 -m scripts.package_skill /path/to/zeitgeist-decoder
```

This produces a `.skill` file you can drop into any Claude instance that supports skills.

## How to use it

Once installed, just talk to Claude about cultural strategy. The skill triggers automatically on phrases like:

- "Help me make sense of this trend..."
- "What does [cultural signal] actually mean?"
- "Is [X] a real shift or just hype?"
- "Find keywords for [audience] in [city]"
- "Build me a trend brief on..."
- "I need a cultural deck about..."

Claude will walk you through the five phases and confirm at each gate before moving forward.

### Example prompts

```
"Help me figure out if [my brand, category Y] should act on the 'soft life'
cultural conversation happening among urban millennial women in India."
```

```
"Decode the 'dad cap revival' aesthetic and tell me whether a streetwear brand
in Delhi can credibly play in it."
```

```
"What's the actual search volume for 'quiet luxury' in tier-1 Indian cities,
and which intent is the highest opportunity for a slow-fashion brand?"
```

See `examples/soft-life-india-walkthrough.md` for a full worked example.

## What's in the box

```
zeitgeist-decoder/
├── SKILL.md                              # The brain. What Claude reads first.
├── README.md                             # This file.
├── LICENSE                               # MIT
├── references/
│   ├── semiotics-frameworks.md           # Barthes, Williams, Floch
│   ├── strategy-frameworks.md            # Sharp, Sutherland, Ogilvy, Holt
│   ├── cliche-killlist.md                # Banned phrases + AI-tells + rewrites
│   ├── search-intent-taxonomy.md         # 4 intents + how to classify
│   └── geo-demographic-modifiers.md      # Geo/demo multipliers (India-first)
├── assets/
│   ├── trend-brief-template.md           # One-pager output structure
│   ├── cultural-deck-template.md         # 14-slide deck outline
│   └── keyword-cluster-template.csv      # Keyword sheet format
├── scripts/
│   ├── keyword_estimator.py              # Directional volume estimation
│   └── cliche_lint.py                    # Jargon + AI-tell scanner
└── examples/
    └── soft-life-india-walkthrough.md    # Full worked example
```

## The scripts

### `keyword_estimator.py`

Estimates directional monthly search volumes for keywords, broken out by geography, demographic, and intent. Shows its math so you can defend (or challenge) the numbers in a meeting.

```bash
python3 scripts/keyword_estimator.py \
  --keywords "soft life meaning,best slow fashion india,buy linen kurta online" \
  --geo delhi-ncr \
  --demo millennial-urban-female-sec-ab \
  --anchor-volume 5000 \
  --intents informational,commercial,transactional
```

Numbers are directional, not definitive. Always cross-validate top candidates in Google Keyword Planner, Semrush, or Ahrefs before committing media spend.

### `cliche_lint.py`

Scans marketing drafts for banned phrases, jargon, and AI-tells. Returns line numbers, severity (banned / warning), and specific rewrites.

```bash
python3 scripts/cliche_lint.py --file draft.md
python3 scripts/cliche_lint.py --text "In today's fast-paced world..."
python3 scripts/cliche_lint.py --file draft.md --json
```

Exits with code 2 if banned phrases are found (so you can wire it into a pre-commit hook for your content repo if you're feeling fancy).

## Calibration

The geography and demographic multipliers are calibrated for the Indian urban market by default (because that's the primary audience). The reference doc `references/geo-demographic-modifiers.md` includes calibrations for US, UK, Germany, and UAE.

If you're working in a market not covered, you can pass custom multipliers:

```bash
python3 scripts/keyword_estimator.py \
  --keywords "[your keywords]" \
  --geo all-india \
  --demo all-urban-adults \
  --anchor-volume 1000 \
  --custom-geo-mult 0.45 \
  --custom-demo-mult 1.10
```

## Customisation

The skill is designed to be forked and tuned for your team or industry.

**Want a different framework set?** Edit `references/strategy-frameworks.md`. Add your favourite practitioners (Mark Pollard, Martin Weigel, Faris Yakob, Tom Roach, etc.). The SKILL.md will load whatever's there.

**Want stricter or looser cliché rules?** Edit `references/cliche-killlist.md` and `scripts/cliche_lint.py`. The lists are kept in plain Python at the top of the script — easy to modify.

**Want different output artifacts?** Add templates to `assets/` and reference them in SKILL.md Phase 5.

**Want different geo/demo multipliers?** Edit the `GEO_MULTIPLIERS` and `DEMO_MULTIPLIERS` dictionaries at the top of `scripts/keyword_estimator.py`. Replace with your own data if you have it.

## Screenshots

**The skill activating on a cultural question:**
![Skill trigger](screenshots/01-skill-trigger.png)

**Phase 2: Semiotic decode output:**
![Semiotic decode](screenshots/02-semiotic-decode.png)

**Keyword estimator with math shown:**
![Keyword estimator](screenshots/03-keyword-estimator.png)

**Cliché linter catching bad copy:**
![Cliché linter](screenshots/04-cliche-linter.png)

**Phase 5: Completed trend brief:**
![Trend brief](screenshots/05-trend-brief.png)

## Limitations and honest disclaimers

- **The keyword volumes are estimates.** They're useful for relative comparison between keywords in a cluster and for making the strategic argument legible. They are not a substitute for live keyword data tools.
- **The multipliers are heuristics.** They're calibrated against published research and informed observation, but they will be wrong in specific cases. The script shows its math precisely so you can argue with it.
- **The framework list is incomplete.** There are dozens of useful cultural and strategy frameworks. The four chosen (Sharp, Sutherland, Ogilvy, Holt) cover the most useful failure modes. Add your own.
- **This is a thinking tool, not a doing tool.** It will not run your campaign, write your captions, or replace your strategist. It will help your strategist think more rigorously and ship more defensible work.

## Contributing

Pull requests welcome, particularly:

- Calibration data for non-Indian markets (US, UK, EU, SEA, MEA)
- Additional strategy frameworks in the references
- More worked examples (each one is a calibration anchor)
- New asset templates (one-page positioning, manifesto outline, etc.)
- Better cliché detection patterns (especially regex for AI-tells)

## License

MIT — see [LICENSE](LICENSE). Use it, fork it, ship it, modify it. Attribution appreciated but not required.

## Credits

Built by Riddhi Mazumdar using Claude.

Methodology draws on:
- Roland Barthes, *Mythologies* (1957)
- Raymond Williams, *Marxism and Literature* (1977)
- Jean-Marie Floch, *Semiotics, Marketing and Communication* (1990)
- Byron Sharp, *How Brands Grow* (2010)
- Rory Sutherland, *Alchemy* (2019)
- David Ogilvy, *Confessions of an Advertising Man* (1963)
- Douglas Holt, *How Brands Become Icons* (2004)
- Wikipedia's "Signs of AI writing" guide (for the linter)

---

*If you ship something with this skill, tag me. I want to see it.*
