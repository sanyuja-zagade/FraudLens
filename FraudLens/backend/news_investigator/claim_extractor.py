def extract_claim(text):
    """
    Clean and prepare the user's news claim.
    """

    claim = text.strip()

    if not claim:
        return None

    return claim