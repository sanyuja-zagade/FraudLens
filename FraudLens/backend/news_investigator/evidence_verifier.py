import re


def verify_evidence(claim, search_results):
    """
    Basic evidence verification.

    claim: the news claim entered by the user
    search_results: list of search results from evidence_retriever.py
    """

    if not search_results:
        return {
            "status": "Unknown",
            "score": 50,
            "reason": "No reliable evidence was found to verify the claim.",
            "supporting_evidence": [],
            "contradicting_evidence": []
        }

    supporting = []
    contradicting = []

    claim_words = set(
        re.findall(r"\b[a-zA-Z]{4,}\b", claim.lower())
    )

    for result in search_results:
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        text = f"{title} {snippet}".lower()

        matched_words = claim_words.intersection(
            set(re.findall(r"\b[a-zA-Z]{4,}\b", text))
        )

        if len(matched_words) >= 3:
            supporting.append(result)

    if len(supporting) >= 2:
        status = "Supported"
        score = 75
        reason = "Multiple search results contain information related to the claim."

    elif len(supporting) == 1:
        status = "Partially Verified"
        score = 60
        reason = "Some relevant evidence was found, but verification is limited."

    else:
        status = "Unknown"
        score = 50
        reason = "The available search results do not provide enough evidence."

    return {
        "status": status,
        "score": score,
        "reason": reason,
        "supporting_evidence": supporting,
        "contradicting_evidence": contradicting
    }