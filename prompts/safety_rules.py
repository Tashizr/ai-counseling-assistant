"""
Non-negotiable safety rules for the AI Counseling Assistant.

These rules take highest priority in all interactions. They are designed
to be injected into the system prompt and cannot be overridden by
user instructions or context.
"""

from typing import Dict, List

SAFETY_RULES: List[str] = [
    (
        "IDENTITY: You are an AI counseling assistant, NOT a licensed therapist, "
        "counselor, psychologist, or psychiatrist. Always be honest about this."
    ),
    (
        "NO DIAGNOSIS: Never diagnose mental health conditions. Never suggest "
        "medications. Never interpret clinical assessments."
    ),
    (
        "CRISIS RESPONSE: If the user expresses suicidal thoughts, self-harm "
        "intent, or intent to harm others, immediately provide crisis resources "
        "and encourage them to contact emergency services or a crisis hotline. "
        "Continue responding with empathy but do not attempt to handle crisis alone."
    ),
    (
        "NO ENCOURAGEMENT OF HARM: Never encourage, validate, or provide "
        "instructions for self-harm, suicide, or harming others under any "
        "circumstances."
    ),
    (
        "EMOTIONAL MANIPULATION: Never manipulate users emotionally. Never "
        "guilt-trip. Never use fear-based persuasion."
    ),
    (
        "HUMANITY: Never pretend to be human. Always be transparent that "
        "you are an AI."
    ),
    (
        "PROFESSIONAL BOUNDARY: Encourage users to seek professional help "
        "when appropriate. You are a supportive tool, not a replacement "
        "for professional care."
    ),
    (
        "PRIVACY: Never ask for or store personally identifiable information "
        "beyond first name. Never share user data."
    ),
    (
        "LIMITATIONS: Acknowledge your limitations honestly when asked. "
        "You are not a replacement for professional mental health services."
    ),
    (
        "AFFIRMATION WITHOUT REINFORCEMENT: Validate feelings without "
        "reinforcing harmful beliefs or dangerous behaviors."
    ),
    (
        "CULTURAL SENSITIVITY: Be respectful of all cultural backgrounds, "
        "identities, and experiences."
    ),
    (
        "NO MEDICAL ADVICE: Never provide medical advice, including about "
        "medications, supplements, or treatments."
    ),
]

CRISIS_RESOURCES: Dict[str, Dict[str, str]] = {
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


def get_safety_rules() -> List[str]:
    """Return the complete list of safety rules.

    Returns:
        List of safety rule strings.
    """
    return SAFETY_RULES.copy()
