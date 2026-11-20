"""PDF-table arithmetic check for Paper C; NOT a raw-transcript reproduction.

Token inputs below are rounded millions as printed in Sections 3-5.
Rates are the historical rates quoted in that paper, not current prices.
No API calls, no dependencies, no experiment runs.
"""

TOKENS_M = {
    "decision_opus": {"input": 0.54, "output": 1.28, "cache_create": 4.57, "cache_read": 8.85},
    "research_sonnet": {"input": 1.33, "output": 1.88, "cache_create": 7.42, "cache_read": 67.94},
}
RATES_USD_PER_M = {
    "opus": {"input": 5.00, "output": 25.00},
    "sonnet_intro": {"input": 2.00, "output": 10.00},
    "sonnet_standard": {"input": 3.00, "output": 15.00},
}


def token_total_m(vector):
    return sum(vector.values())


def price_usd(vector, rate):
    """Cache-create = 1.25x input; cache-read = 0.10x input."""
    return (
        vector["input"] * rate["input"]
        + vector["output"] * rate["output"]
        + vector["cache_create"] * 1.25 * rate["input"]
        + vector["cache_read"] * 0.10 * rate["input"]
    )


def main():
    decision = TOKENS_M["decision_opus"]
    research = TOKENS_M["research_sonnet"]
    total = token_total_m(decision) + token_total_m(research)
    research_fraction = token_total_m(research) / total
    print("PAPER C: CHECK OF ROUNDED PDF TABLE VALUES")
    print(f"Decision tokens: {token_total_m(decision):.2f}M")
    print(f"Research tokens: {token_total_m(research):.2f}M")
    print(f"Research token share: {100 * research_fraction:.2f}% (paper: 83.8%)")
    print(f"Decision token share: {100 * (1 - research_fraction):.2f}% (paper: 16.2%)")

    opus = RATES_USD_PER_M["opus"]
    decision_opus_cost = price_usd(decision, opus)
    research_opus_cost = price_usd(research, opus)
    all_opus_cost = decision_opus_cost + research_opus_cost
    print(f"\nResearch share of all-Opus-priced dollars: {100 * research_opus_cost / all_opus_cost:.2f}% (paper: 66.4%)")
    print(f"All-Opus counterfactual: ${all_opus_cost:.2f} (paper: $201.67)")

    for label in ("sonnet_intro", "sonnet_standard"):
        tiered = decision_opus_cost + price_usd(research, RATES_USD_PER_M[label])
        saving = (all_opus_cost - tiered) / all_opus_cost * 100
        paper_value = "$121.32" if label == "sonnet_intro" else "$148.10"
        print(f"Tiered ({label}): ${tiered:.2f} (paper: {paper_value}); saving {saving:.1f}%")
    print("\nSmall dollar differences are expected: PDF token vectors are rounded.")
    print("This checks rate-card arithmetic, NOT original transcripts or parser deduplication.")


if __name__ == "__main__":
    main()
