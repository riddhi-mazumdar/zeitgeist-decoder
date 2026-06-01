#!/usr/bin/env python3
"""
cliche_lint.py — scan marketing drafts for jargon, dead phrases, and AI-tells.

Returns line numbers, severity, and suggested rewrites. Use before saving
any written artifact in Phase 5.

Usage:
  python3 cliche_lint.py --file draft.md
  python3 cliche_lint.py --text "In today's fast-paced world, brands must leverage..."
  python3 cliche_lint.py --file draft.md --json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Finding:
    line: int
    column: int
    matched: str
    severity: str  # "banned" | "warning"
    category: str
    rewrite: str
    context: str


# Phrases that are dead. Severity: banned.
BANNED_PHRASES = [
    ("in today's fast-paced world", "Delete it. Start with the actual point.", "dead-opener"),
    ("in an era of", "Delete; specify the actual change you mean.", "dead-opener"),
    ("it's no secret that", "Delete; if it's no secret, you don't need to say it.", "dead-opener"),
    ("now more than ever", "Delete; specify what's new about now.", "dead-opener"),
    ("unprecedented times", "Specify the specific change you mean.", "dead-opener"),
    ("the new normal", "Name the actual condition.", "dead-phrase"),
    ("game-changer", "Replace with the specific verb: 'halves', 'doubles', 'eliminates', 'replaces'.", "hollow-claim"),
    ("game-changing", "Replace with the specific verb: 'halves', 'doubles', 'eliminates', 'replaces'.", "hollow-claim"),
    ("disruptor", "Name what is being disrupted and how.", "hollow-claim"),
    ("disrupting the industry", "Name what is being disrupted and how.", "hollow-claim"),
    ("synergy", "Replace with the specific shared activity.", "jargon"),
    ("synergies", "Replace with the specific shared activity.", "jargon"),
    ("move the needle", "Specify the metric and the delta.", "jargon"),
    ("low-hanging fruit", "Name the specific opportunity.", "jargon"),
    ("take it to the next level", "Specify what the next level is.", "jargon"),
    ("best-in-class", "State the specific evidence for the claim.", "hollow-superlative"),
    ("world-class", "State the specific evidence for the claim.", "hollow-superlative"),
    ("leverage", "Replace with 'use'.", "jargon-verb"),
    ("leveraging", "Replace with 'using'.", "jargon-verb"),
    ("unlock potential", "Describe the specific outcome.", "vague-claim"),
    ("unlock value", "Describe the specific value.", "vague-claim"),
    ("at the end of the day", "Delete; whatever follows is your real point.", "filler"),
    ("going forward", "Delete or specify 'starting next quarter' / 'after launch'.", "filler"),
    ("circle back", "Replace with 'follow up' or specify the next action.", "jargon"),
    ("reach out", "Replace with 'email', 'call', 'ask', 'message'.", "jargon"),
    ("more than a campaign, it's a movement", "Delete the whole sentence. Movements are not announced.", "inflated-claim"),
    ("more than just", "Almost always followed by something inflated. Cut.", "inflated-claim"),
    ("we don't just", "Same pattern. Cut.", "inflated-claim"),
    ("it's not just about", "Same pattern. Cut.", "inflated-claim"),
    ("join the conversation", "Specify what people should actually do.", "jargon"),
]

# Words that signal trouble. Severity: warning (context-dependent).
WARNING_WORDS = [
    ("robust", "Usually means 'we don't know how to describe this'. Specify the quality.", "vague-adjective"),
    ("authentic", "When you have to say it, you don't have it. Show, don't tell.", "ironic-overuse"),
    ("authenticity", "Same. Show, don't tell.", "ironic-overuse"),
    ("curated", "Every brand 'curates' now. Describe the selection criterion instead.", "collapsed-word"),
    ("bespoke", "Overused; specify what is custom about it.", "collapsed-word"),
    ("artisanal", "Overused; describe the actual craft involved.", "collapsed-word"),
    ("storytelling", "Often means 'we wrote captions'. Name the actual format.", "vague-activity"),
    ("resonates", "Replace with 'lands', 'matters to', 'speaks to'.", "overused-verb"),
    ("resonant", "Replace with a specific descriptor.", "overused-verb"),
    ("cutting-edge", "Allowed only with a specific, verifiable claim.", "hollow-superlative"),
    ("state-of-the-art", "Allowed only with a specific reason.", "hollow-superlative"),
    ("revolutionary", "Describe the actual revolution.", "hollow-superlative"),
    ("groundbreaking", "Describe what ground is being broken.", "hollow-superlative"),
    ("transformative", "Describe the specific transformation.", "hollow-superlative"),
    ("empower", "Replace with what the thing actually lets people do.", "vague-verb"),
    ("empowering", "Replace with what it actually lets people do.", "vague-verb"),
    ("tap into", "Replace with a specific verb.", "jargon-verb"),
    ("deep dive", "Allowed only if what follows is actually deep.", "promise-check"),
    ("solutions", "When used as a generic noun ('our solutions for...'). Be specific.", "vague-noun"),
]


def find_phrases(text: str, phrases: list, severity: str) -> List[Finding]:
    findings = []
    lines = text.split("\n")
    for line_idx, line in enumerate(lines, start=1):
        lower = line.lower()
        for phrase, rewrite, category in phrases:
            start = 0
            while True:
                idx = lower.find(phrase, start)
                if idx == -1:
                    break
                # Word boundary check for short words to avoid matching inside words
                if len(phrase) <= 6:
                    before = lower[idx - 1] if idx > 0 else " "
                    after = lower[idx + len(phrase)] if idx + len(phrase) < len(lower) else " "
                    if before.isalnum() or after.isalnum():
                        start = idx + 1
                        continue
                findings.append(Finding(
                    line=line_idx,
                    column=idx + 1,
                    matched=line[idx:idx + len(phrase)],
                    severity=severity,
                    category=category,
                    rewrite=rewrite,
                    context=line.strip()[:120],
                ))
                start = idx + len(phrase)
    return findings


def find_em_dashes(text: str) -> List[Finding]:
    findings = []
    lines = text.split("\n")
    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        # Skip markdown structural lines:
        # - Frontmatter / section dividers: --- or more
        # - Table separator rows: |---|---| etc.
        # - Pure dash lines used as visual breaks
        if re.fullmatch(r"-{3,}", stripped):
            continue
        if re.fullmatch(r"\|?[-:\s|]+\|?", stripped) and "|" in stripped:
            continue
        # Match em-dash (—) and double-hyphen (--) used as em-dash *in prose*
        # For --, require it to be surrounded by word characters (not part of a divider)
        for match in re.finditer(r"—", line):
            findings.append(Finding(
                line=line_idx,
                column=match.start() + 1,
                matched=match.group(),
                severity="warning",
                category="em-dash-overuse",
                rewrite="Replace with comma, semicolon, period, colon, or parentheses. "
                        "Em-dashes are the single strongest AI-tell.",
                context=line.strip()[:120],
            ))
        for match in re.finditer(r"(?<=\w)--(?=\w| )", line):
            findings.append(Finding(
                line=line_idx,
                column=match.start() + 1,
                matched=match.group(),
                severity="warning",
                category="em-dash-overuse",
                rewrite="Replace with comma, semicolon, period, colon, or parentheses. "
                        "Em-dashes are the single strongest AI-tell.",
                context=line.strip()[:120],
            ))
    return findings


def find_rule_of_three(text: str) -> List[Finding]:
    """Detect 'X, Y, and Z' patterns where all three are adjectives or short nouns.
    Heuristic: catches obvious cases like 'bold, beautiful, and brilliant'."""
    findings = []
    lines = text.split("\n")
    # Match: word, word, and word — where the words are short (likely adjectives)
    pattern = re.compile(r"\b(\w{3,15}),\s+(\w{3,15}),\s+and\s+(\w{3,15})\b", re.IGNORECASE)
    for line_idx, line in enumerate(lines, start=1):
        for match in pattern.finditer(line):
            # Filter: only flag if all three words are similar in length (likely parallel adjectives)
            words = [match.group(1), match.group(2), match.group(3)]
            avg_len = sum(len(w) for w in words) / 3
            if all(abs(len(w) - avg_len) <= 3 for w in words):
                findings.append(Finding(
                    line=line_idx,
                    column=match.start() + 1,
                    matched=match.group(),
                    severity="warning",
                    category="rule-of-three",
                    rewrite="Check that all three items add information. "
                            "If the third is rhythm-filler, cut to two.",
                    context=line.strip()[:120],
                ))
    return findings


def find_vague_attributions(text: str) -> List[Finding]:
    findings = []
    lines = text.split("\n")
    patterns = [
        (r"\bstudies show\b", "Name the study and link it."),
        (r"\bexperts say\b", "Name the experts."),
        (r"\bresearch suggests\b", "Cite the research."),
        (r"\bit is widely known\b", "If it's widely known, you don't need to say so."),
        (r"\bmany believe\b", "Name who, or cite a poll."),
    ]
    for line_idx, line in enumerate(lines, start=1):
        for pattern, rewrite in patterns:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                findings.append(Finding(
                    line=line_idx,
                    column=match.start() + 1,
                    matched=match.group(),
                    severity="warning",
                    category="vague-attribution",
                    rewrite=rewrite,
                    context=line.strip()[:120],
                ))
    return findings


def lint(text: str) -> List[Finding]:
    findings = []
    findings.extend(find_phrases(text, BANNED_PHRASES, "banned"))
    findings.extend(find_phrases(text, WARNING_WORDS, "warning"))
    findings.extend(find_em_dashes(text))
    findings.extend(find_rule_of_three(text))
    findings.extend(find_vague_attributions(text))
    findings.sort(key=lambda f: (f.line, f.column))

    # Filter out findings on lines marked with IGNORE-LINT (for legitimate exceptions:
    # meta-discussion of bad phrases, banned-word lists in instructions, etc.)
    lines = text.split("\n")
    ignored_lines = {i + 1 for i, line in enumerate(lines) if "IGNORE-LINT" in line}
    findings = [f for f in findings if f.line not in ignored_lines]

    return findings


def format_human(findings: List[Finding], source: str) -> str:
    if not findings:
        return f"\nCLEAN. No clichés or AI-tells detected in {source}.\n"

    banned = [f for f in findings if f.severity == "banned"]
    warnings = [f for f in findings if f.severity == "warning"]

    lines = []
    lines.append("")
    lines.append("=" * 78)
    lines.append(f"CLICHÉ LINT REPORT — {source}")
    lines.append("=" * 78)
    lines.append(f"  Banned phrases found: {len(banned)}")
    lines.append(f"  Warnings: {len(warnings)}")
    lines.append("-" * 78)
    lines.append("")

    if banned:
        lines.append("BANNED (must fix before saving):")
        lines.append("")
        for f in banned:
            lines.append(f"  Line {f.line}, col {f.column}: '{f.matched}'  [{f.category}]")
            lines.append(f"    Context: ...{f.context}...")
            lines.append(f"    Rewrite: {f.rewrite}")
            lines.append("")

    if warnings:
        lines.append("WARNINGS (review and fix unless justified):")
        lines.append("")
        for f in warnings:
            lines.append(f"  Line {f.line}, col {f.column}: '{f.matched}'  [{f.category}]")
            lines.append(f"    Context: ...{f.context}...")
            lines.append(f"    Rewrite: {f.rewrite}")
            lines.append("")

    lines.append("=" * 78)
    if banned:
        lines.append("Do not save this draft until all BANNED items are fixed.")
    else:
        lines.append("No banned items. Review warnings, then save.")
    lines.append("=" * 78)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Scan marketing drafts for clichés, jargon, and AI-tells.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path to a text file to lint")
    group.add_argument("--text", help="Direct text to lint")
    parser.add_argument("--json", action="store_true",
                        help="Output findings as JSON")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
            source = args.file
        except FileNotFoundError:
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        text = args.text
        source = "input text"

    findings = lint(text)

    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print(format_human(findings, source))

    # Exit non-zero if banned items found, so CI / scripts can detect
    if any(f.severity == "banned" for f in findings):
        sys.exit(2)


if __name__ == "__main__":
    main()
