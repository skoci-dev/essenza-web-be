"""
Snippet Utility Module

Provides functions for generating context-aware search result snippets
from HTML content, with intelligent keyword highlighting positioning.
"""

from typing import Optional

from django.utils.html import strip_tags


def search_result_snippet(query: str, content: str, max_length: int = 300) -> str:
    """Generate a contextual snippet from content centered around search query keywords.

    Extracts a relevant portion of content by finding the first occurrence of any
    keyword from the search query, then creating a snippet centered around that keyword.
    If no keywords are found, returns the beginning of the content.

    Algorithm:
    1. Strip HTML tags and sanitize content
    2. Find the earliest occurring keyword from the query
    3. Center the snippet around the keyword position
    4. Add ellipsis indicators for truncated content

    Args:
        query: Search query string (can contain multiple keywords)
        content: HTML or plain text content to extract snippet from
        max_length: Maximum length of the returned snippet (default: 300)

    Returns:
        str: Formatted snippet with ellipsis indicators, centered on keyword if found

    Examples:
        >>> search_result_snippet("python", "Learn Python programming", 50)
        'Learn Python programming'
        >>> search_result_snippet("django", "A" * 200 + "django" + "B" * 200, 50)
        '...AAAAAAdjangoBBBBB...'
    """
    if not content:
        return ""

    # Sanitize content by removing HTML tags and extra whitespace
    clean_content = strip_tags(content).strip()

    # If no query provided, return beginning of content
    if not query or not query.strip():
        truncated_content = clean_content[:max_length]
        return (
            f"{truncated_content}..."
            if len(clean_content) > max_length
            else truncated_content
        )

    # Parse keywords and prepare lowercase version for case-insensitive search
    keywords = query.lower().split()
    content_lower = clean_content.lower()

    # Find the earliest occurring keyword in content
    earliest_pos = len(clean_content)
    found_keyword: Optional[str] = None

    for keyword in keywords:
        pos = content_lower.find(keyword)
        if pos != -1 and pos < earliest_pos:
            earliest_pos = pos
            found_keyword = keyword

    # If no keywords found, return beginning of content
    if found_keyword is None:
        truncated_content = clean_content[:max_length]
        return (
            f"{truncated_content}..."
            if len(clean_content) > max_length
            else truncated_content
        )

    # Calculate snippet boundaries centered on keyword
    keyword_center = earliest_pos + len(found_keyword) // 2
    snippet_start = max(0, keyword_center - max_length // 2)
    snippet_end = snippet_start + max_length

    # Adjust boundaries if snippet extends beyond content end
    if snippet_end > len(clean_content):
        snippet_end = len(clean_content)
        snippet_start = max(0, snippet_end - max_length)

    # Extract snippet from content
    snippet = clean_content[snippet_start:snippet_end]

    # Add ellipsis indicators for truncated portions
    prefix = "..." if snippet_start > 0 else ""
    suffix = "..." if snippet_end < len(clean_content) else ""

    return f"{prefix}{snippet}{suffix}"
