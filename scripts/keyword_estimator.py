#!/usr/bin/env python3
"""
keyword_estimator.py — directional search volume estimation for cultural strategy.

This script estimates monthly search volumes for keywords by applying geography,
demographic, and intent multipliers to an anchor volume. Numbers are directional,
not definitive. The output explicitly shows the math so the strategist can
defend (or challenge) the numbers in a meeting.

Use as the Phase 4 input. Always cross-validate top candidates against
Google Keyword Planner, Semrush, or Ahrefs before betting media on them.

Usage:
  python3 keyword_estimator.py \\
    --keywords "soft life meaning,best slow fashion india,buy linen kurta online" \\
    --geo delhi-ncr \\
    --demo millennial-urban-female-sec-ab \\
    --anchor-volume 5000 \\
    --intents informational,commercial,transactional
"""

import argparse
import json
import sys
from typing import Dict, List, Tuple

# Geography multipliers (share of national volume)
# Calibrated for Indian market; see references/geo-demographic-modifiers.md
GEO_MULTIPLIERS: Dict[str, float] = {
    # India
    "all-india": 1.00,
    "delhi": 0.18,
    "delhi-ncr": 0.22,
    "mumbai": 0.18,
    "bangalore": 0.18,
    "bengaluru": 0.18,
    "pune": 0.06,
    "hyderabad": 0.06,
    "chennai": 0.06,
    "kolkata": 0.06,
    "ahmedabad": 0.06,
    "tier-2": 0.06,
    "tier-3": 0.02,
    "rural-india": 0.01,
    # International (rough)
    "us-national": 1.00,
    "nyc": 0.06,
    "la": 0.05,
    "uk-national": 1.00,
    "london": 0.18,
    "uae-national": 1.00,
    "dubai": 0.60,
}

# Demographic multipliers — combinations of cohort + gender + SEC + urbanity
# Calibrated against Indian urban search behaviour. See reference doc.
DEMO_MULTIPLIERS: Dict[str, float] = {
    # Cohort-only
    "gen-z": 1.35,
    "millennial": 1.20,
    "gen-x": 0.65,
    "boomer": 0.35,
    # Pre-composed common combinations
    "gen-z-urban-female-sec-ab": 1.35 * 1.15 * 1.15,  # ~1.79
    "gen-z-urban-male-sec-ab": 1.35 * 1.0 * 1.15,     # ~1.55
    "millennial-urban-female-sec-ab": 1.20 * 1.15 * 1.15,  # ~1.59
    "millennial-urban-male-sec-ab": 1.20 * 1.0 * 1.15,     # ~1.38
    "millennial-urban-female-sec-bc": 1.20 * 1.15 * 0.85,  # ~1.17
    "millennial-urban-male-sec-bc": 1.20 * 1.0 * 0.85,     # ~1.02
    "gen-x-urban-sec-ab": 0.65 * 1.15,                # ~0.75
    "all-urban-adults": 1.0,
}

# Intent decay from informational baseline
INTENT_DECAY: Dict[str, float] = {
    "informational": 1.00,
    "commercial": 0.40,
    "commercial-investigation": 0.40,
    "transactional": 0.15,
    "navigational": 0.25,  # rough — varies by brand
}


def parse_keywords_with_intent(keywords_str: str, intents_str: str) -> List[Tuple[str, str]]:
    """Pair each keyword with an intent. If the lists have unequal lengths,
    repeat the last intent or default to 'informational' for unspecified."""
    keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
    intents = [i.strip().lower() for i in intents_str.split(",") if i.strip()] if intents_str else []

    paired = []
    for i, kw in enumerate(keywords):
        if i < len(intents):
            intent = intents[i]
        elif intents:
            intent = intents[-1]
        else:
            intent = "informational"
        paired.append((kw, intent))
    return paired


def estimate_volume(
    anchor: float,
    geo: str,
    demo: str,
    intent: str,
    custom_geo_mult: float = None,
    custom_demo_mult: float = None,
) -> Dict:
    """Calculate estimated volume with math shown.

    Returns a dict with the breakdown so the strategist can explain the number."""
    geo_mult = custom_geo_mult if custom_geo_mult is not None else GEO_MULTIPLIERS.get(geo.lower(), None)
    demo_mult = custom_demo_mult if custom_demo_mult is not None else DEMO_MULTIPLIERS.get(demo.lower(), None)
    intent_mult = INTENT_DECAY.get(intent.lower(), 1.0)

    if geo_mult is None:
        return {
            "error": f"Unknown geography '{geo}'. Known: {sorted(GEO_MULTIPLIERS.keys())}. "
                     f"Pass --custom-geo-mult to override."
        }
    if demo_mult is None:
        return {
            "error": f"Unknown demographic '{demo}'. Known: {sorted(DEMO_MULTIPLIERS.keys())}. "
                     f"Pass --custom-demo-mult to override."
        }

    estimated = anchor * geo_mult * demo_mult * intent_mult

    return {
        "anchor_volume": anchor,
        "geo_multiplier": round(geo_mult, 3),
        "demo_multiplier": round(demo_mult, 3),
        "intent_multiplier": round(intent_mult, 3),
        "estimated_monthly_searches": int(round(estimated)),
        "math": f"{int(anchor)} (anchor) × {round(geo_mult, 3)} (geo: {geo}) "
                f"× {round(demo_mult, 3)} (demo: {demo}) × {round(intent_mult, 3)} "
                f"(intent: {intent}) = {int(round(estimated))}/mo"
    }


def main():
    parser = argparse.ArgumentParser(
        description="Directional keyword volume estimator for cultural strategy.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--keywords", required=True,
                        help="Comma-separated keyword list")
    parser.add_argument("--geo", required=True,
                        help="Geography key (e.g., delhi-ncr, mumbai, all-india, london)")
    parser.add_argument("--demo", required=True,
                        help="Demographic key (e.g., millennial-urban-female-sec-ab)")
    parser.add_argument("--anchor-volume", type=float, required=True,
                        help="Assumed national/global monthly volume for the base keyword")
    parser.add_argument("--intents", default="",
                        help="Comma-separated intents matching the keyword order. "
                             "If shorter than keyword list, last intent repeats. "
                             "Options: informational, commercial, transactional, navigational")
    parser.add_argument("--custom-geo-mult", type=float, default=None,
                        help="Override the geo multiplier with a custom value (0–1+)")
    parser.add_argument("--custom-demo-mult", type=float, default=None,
                        help="Override the demo multiplier with a custom value")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of human-readable table")
    args = parser.parse_args()

    pairs = parse_keywords_with_intent(args.keywords, args.intents)
    results = []

    for kw, intent in pairs:
        result = estimate_volume(
            anchor=args.anchor_volume,
            geo=args.geo,
            demo=args.demo,
            intent=intent,
            custom_geo_mult=args.custom_geo_mult,
            custom_demo_mult=args.custom_demo_mult,
        )
        result["keyword"] = kw
        result["intent"] = intent
        results.append(result)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    # Human-readable output
    print()
    print("=" * 78)
    print("KEYWORD VOLUME ESTIMATE — directional, not definitive")
    print("=" * 78)
    print(f"Geography: {args.geo}")
    print(f"Demographic: {args.demo}")
    print(f"Anchor volume: {int(args.anchor_volume)}/mo")
    print("-" * 78)
    print()

    for r in results:
        if "error" in r:
            print(f"  ERROR for keyword: {r.get('keyword', '?')}")
            print(f"    {r['error']}")
            print()
            continue

        print(f"  Keyword: {r['keyword']}")
        print(f"  Intent:  {r['intent']}")
        print(f"  Estimate: {r['estimated_monthly_searches']:,}/mo")
        print(f"  Math:    {r['math']}")
        print()

    print("-" * 78)
    print("Cross-validate top candidates in Google Keyword Planner, Semrush, or")
    print("Ahrefs before committing media spend. These numbers are for relative")
    print("comparison and storytelling defensibility, not bid setting.")
    print("=" * 78)


if __name__ == "__main__":
    main()
