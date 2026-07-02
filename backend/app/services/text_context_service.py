def limit_text(text: str, max_chars: int = 6000) -> str:
    """
    Prevents optional LLM generation endpoints from sending oversized prompts.

    MVP strategy:
    - Keep the beginning of the resume/JD where most important sections usually appear.
    - Later we can replace this with section-aware resume extraction.
    """
    if not text:
        return ""

    cleaned = text.strip()

    if len(cleaned) <= max_chars:
        return cleaned

    return (
        cleaned[:max_chars]
        + "\n\n[TRUNCATED: text shortened to keep LLM generation stable]"
    )