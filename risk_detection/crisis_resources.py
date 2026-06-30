"""
Crisis resource information by country.

Provides contact details for emergency mental health services.
"""

CRISIS_RESOURCES: dict[str, dict[str, str]] = {
    "US": {
        "name": "988 Suicide & Crisis Lifeline",
        "phone": "988",
        "text": "Text HOME to 741741",
        "web": "https://988lifeline.org",
    },
    "UK": {
        "name": "Samaritans",
        "phone": "116 123",
        "text": "Text SHOUT to 85258",
        "web": "https://www.samaritans.org",
    },
    "CA": {
        "name": "Talk Suicide Canada",
        "phone": "1-833-456-4566",
        "text": "Text 45645",
        "web": "https://talksuicide.ca",
    },
    "AU": {
        "name": "Lifeline Australia",
        "phone": "13 11 14",
        "text": "Text 0477 13 11 14",
        "web": "https://www.lifeline.org.au",
    },
    "IN": {
        "name": "Vandrevala Foundation",
        "phone": "1860-2662-345",
        "web": "https://www.vandrevalafoundation.com",
    },
    "DEFAULT": {
        "name": "International Association for Suicide Prevention",
        "web": "https://www.iasp.info/resources/Crisis_Centres/",
    },
}


def get_crisis_resources(country_code: str = "DEFAULT") -> dict[str, str]:
    """Return crisis resources for a given country.

    Args:
        country_code: ISO country code (US, UK, CA, AU, IN).

    Returns:
        Dict with 'name', 'phone', 'text', 'web' keys.
    """
    return CRISIS_RESOURCES.get(country_code, CRISIS_RESOURCES["DEFAULT"])


def format_crisis_resources(country_code: str = "DEFAULT") -> str:
    """Format crisis resources as a readable string.

    Args:
        country_code: ISO country code.

    Returns:
        Formatted crisis resource string.
    """
    resources = get_crisis_resources(country_code)
    lines = [f"**{resources['name']}**"]
    if "phone" in resources:
        lines.append(f"Phone: {resources['phone']}")
    if "text" in resources:
        lines.append(f"Text: {resources['text']}")
    if "web" in resources:
        lines.append(f"Web: {resources['web']}")
    return "\n".join(lines)
