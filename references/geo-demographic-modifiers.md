# Geographic and demographic modifiers for search volume

This reference supports Phase 4. The `keyword_estimator.py` script reads these multipliers; you should also understand them qualitatively so you can interpret the script's output and adjust when the user's brief deviates from the defaults.

## How the modifiers work

The estimator takes an **anchor volume** — a known or assumed global/national search volume for a keyword — and multiplies it by:

1. A **geography modifier** — how that search behaviour scales (or contracts) in a specific city or region
2. A **demographic modifier** — how the searcher's age, income, language preference, and urbanity shifts the volume
3. An **intent decay** — how much volume is lost or gained as you move along the intent funnel

The final number is *directional* — useful for relative comparison between keywords and clusters, not a substitute for Keyword Planner or Semrush data on a specific keyword you intend to bid on.

## Geography modifiers

These are rough multipliers against a base of "national average for the country." They are calibrated for the Indian market by default (because most users of this skill will be Indian in-house teams), with notes for adapting to other markets.

### India

| Geography | Multiplier | Notes |
|---|---|---|
| All-India | 1.00 | The default base |
| Tier 1 metros (Delhi, Mumbai, Bangalore) | 0.18 each (≈0.54 combined) | English-language search disproportionately concentrated here |
| Tier 2 cities (Pune, Hyderabad, Chennai, Kolkata, Ahmedabad) | 0.06 each | Significant English search, growing Hindi/regional |
| Tier 3 cities | 0.02 each | Mostly regional language; English-keyword volume thins fast |
| Rural India | 0.01 collectively | Search behaviour exists but on very different keywords |
| Delhi-NCR specifically | 0.22 | Larger than Delhi alone because of Gurgaon/Noida/Ghaziabad |

### Other markets (rough calibrations)

| Country | Tier 1 city share of national | Notes |
|---|---|---|
| US | NYC 0.06, LA 0.05, Chicago 0.03 | Flatter distribution |
| UK | London 0.18 | Heavy London concentration |
| Germany | Berlin 0.08, Munich 0.05, Hamburg 0.04 | Distributed |
| UAE | Dubai 0.60 | Extreme concentration |

When the user's brief involves a non-Indian market, ask which city or region and apply judgement. The script accepts a custom multiplier flag.

## Demographic modifiers

These adjust the geography-adjusted volume based on the audience the brand is targeting. Multipliers are relative to "all adults in that geography."

### Age cohorts (India, 2026)

| Cohort | Multiplier | Notes |
|---|---|---|
| Gen Z (born 1997–2012, currently 14–29) | 1.35 for cultural/lifestyle/fashion keywords; 0.6 for finance/health | Highest search frequency per capita, heavily skewed toward cultural content |
| Millennial (born 1981–1996, currently 30–45) | 1.20 for finance/health/parenting; 1.0 for cultural/fashion | The most commercially valuable cohort for most categories |
| Gen X (born 1965–1980, currently 46–61) | 0.65 across most categories; 1.4 for health/finance/parenting-of-teens | Lower search frequency, but high commercial value when they search |
| Boomers (born before 1965, currently 62+) | 0.35 across categories; 1.1 for health and travel | Substantially lower digital-search behaviour in India |

### Income/SEC segments (India, urban)

| Segment | Multiplier | Notes |
|---|---|---|
| SEC A1/A2 (top ~5% urban) | 1.40 for premium goods, travel, finance | English-search dominant, brand-conscious |
| SEC A3/B1 (next ~15%) | 1.15 for most categories | Aspirational, comparison-heavy search behaviour |
| SEC B2/C (middle) | 0.85 | Often searches in Hinglish or regional language |
| SEC D/E | 0.30 for English keywords; native-language search is its own ecosystem | English-keyword data underrepresents this segment massively |

### Gender (use sparingly; many categories are not gender-skewed)

| Skew | Multiplier | Applies to |
|---|---|---|
| Female-skewed categories (beauty, fashion-women's, home, parenting) | 1.15 for female audiences | Self-explanatory |
| Male-skewed categories (auto, men's grooming, finance/investing) | 1.15 for male audiences | Closing the gap but still skewed |
| Neutral categories | 1.0 | Apply no modifier |

Be careful with gender modifiers — they reinforce stereotypes if applied without thought. Use them only when the brief explicitly targets a gender segment.

### Language preference

| Search language | Multiplier on English-keyword volume | Notes |
|---|---|---|
| English-first | 1.0 (the baseline assumption) | Tier 1/2 urban India, SEC A/B |
| Hinglish (Romanised Hindi mixed with English) | 1.4 (because the same searcher uses both, expanding total) | Critical for D2C, food, entertainment |
| Hindi/regional in Devanagari/native script | These are *separate* keyword universes, not modifiers | Run a separate analysis if the brief targets these audiences |

## Intent decay

As you move from informational to transactional, search volume on the same topic generally decreases (more people are curious than ready to buy).

| Intent | Decay multiplier from informational baseline |
|---|---|
| Informational | 1.0 (baseline) |
| Commercial investigation | 0.4 |
| Transactional | 0.15 |
| Navigational | varies wildly by brand — use brand-specific data |

So if "what is matcha" is 10,000/mo all-India, then "best matcha brand India" is likely around 4,000/mo and "buy matcha online India" around 1,500/mo. These are heuristics, not laws — check actual data for high-stakes keywords.

## Worked example

Brief: brand targeting urban millennial women in Delhi-NCR, considering a campaign around the "soft life" cultural signal.

Anchor volume: "soft life" — assume 50,000/mo searches globally (informational).

Step 1: Geography modifier
50,000 × 0.22 (Delhi-NCR share of India) = 11,000/mo Delhi-NCR (if India were the whole market — but signal originates in West African / Black American discourse, so the India share is itself smaller)

Step 2: Adjust for signal origin
Assume India accounts for ~10% of global "soft life" search volume → India-adjusted anchor: 5,000/mo
Apply Delhi-NCR share: 5,000 × 0.22 = 1,100/mo

Step 3: Demographic modifier
Urban millennial women, SEC A/B: 1.20 (millennial) × 1.15 (female for lifestyle) × 1.15 (SEC A/B) = 1.59
1,100 × 1.59 = 1,749/mo

Step 4: Intent decay for variants
- "soft life meaning" (informational): 1,749/mo
- "soft life vs hustle culture" (commercial investigation): ~700/mo
- "books about soft life" (commercial investigation, niche): ~260/mo

The script handles this math. You interpret it.

## When to override the multipliers

Override the defaults when:
- The signal is geography-specific (e.g., a Bengali cultural signal in Kolkata — Tier 2 multiplier underestimates)
- The signal is emergent and the search pattern is still forming (multipliers from past data underestimate growth — note this in the brief)
- The signal is fading (multipliers from past data overestimate — also note)
- The brand has unusual audience concentration (e.g., a niche luxury brand with 80% of customers in SEC A1 — apply higher multiplier)

Always show your math in the brief. "We applied a 1.59x demographic multiplier (millennial × female-lifestyle × SEC A/B) on a Delhi-NCR-adjusted anchor of 1,100/mo, producing 1,749/mo for the informational base term." That sentence is what makes the number defensible in a meeting.
