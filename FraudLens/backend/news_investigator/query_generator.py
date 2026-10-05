def generate_queries(claim):
    """
    Generate simple search queries from a news claim.
    """

    queries = [
        claim,
        f"{claim} news",
        f"{claim} official source"
    ]

    return queries