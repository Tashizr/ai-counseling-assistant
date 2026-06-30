"""
Core system prompt construction for the AI Counseling Assistant.

Assembles all context components into a single system prompt sent
to the Ollama model on each request.
"""

import logging
from typing import Optional

from prompts.safety_rules import get_safety_rules
from prompts.templates import build_system_prompt
from risk_detection.crisis_resources import CRISIS_RESOURCES

logger = logging.getLogger(__name__)

CRISIS_RESOURCES_BLOCK = """
## Crisis Resources (weave these in naturally when appropriate)
If the person is in distress, share these resources conversationally — not as a cold list.
For example: "I want to make sure you have someone to talk to right now. You can reach
the {name} at {phone} — they're available 24/7 and really good at helping people through
moments like this."

US: 988 Suicide & Crisis Lifeline — call/text 988
UK: Samaritans — call 116 123
CA: Talk Suicide Canada — call 1-833-456-4566
AU: Lifeline Australia — call 13 11 14
IN: Vandrevala Foundation — call 1860-2662-345
International: https://www.iasp.info/resources/Crisis_Centres/
"""


def get_system_prompt(
    user_name: Optional[str] = None,
    emotion: Optional[str] = None,
    risk_level: str = "low",
    rag_context: str = "",
    memory_context: str = "",
    conversation_context: str = "",
) -> str:
    """Build the complete system prompt for the current conversation turn.

    Args:
        user_name: The user's name, if known.
        emotion: Most recently detected emotion label.
        risk_level: Current risk level (low, moderate, high, critical).
        rag_context: RAG-retrieved knowledge passages.
        memory_context: Long-term memory context.
        conversation_context: Recent conversation messages.

    Returns:
        The assembled system prompt string.
    """
    safety_rules = get_safety_rules()

    prompt = build_system_prompt(
        safety_rules=safety_rules,
        context=conversation_context,
        memory_context=memory_context,
        rag_context=rag_context,
        user_name=user_name,
        emotion=emotion,
        risk_level=risk_level,
    )

    if risk_level in ("high", "critical"):
        prompt += "\n" + CRISIS_RESOURCES_BLOCK

    logger.debug(
        "System prompt assembled: %d chars, risk=%s, emotion=%s",
        len(prompt),
        risk_level,
        emotion or "none",
    )

    return prompt
