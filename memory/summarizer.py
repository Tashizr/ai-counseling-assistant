"""
Conversation summarization for long-term memory storage.

Generates summaries of conversations using the LLM and extracts
key topics and goals.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ConversationSummarizer:
    """Summarizes conversations for long-term memory storage.

    Uses the LLM to generate concise summaries that capture the
    main themes, emotions, and outcomes of a conversation.
    """

    def __init__(self) -> None:
        """Initialize the conversation summarizer."""
        logger.debug("ConversationSummarizer initialized")

    def generate_summary_prompt(self, messages: list[dict]) -> str:
        """Generate a prompt for summarizing a conversation.

        Args:
            messages: List of message dicts with 'role' and 'content'.

        Returns:
            The summarization prompt.
        """
        conversation_text = "\n".join(
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in messages
        )

        return f"""Summarize this counseling conversation in 3-5 sentences.
Focus on: main topics discussed, emotions expressed, coping strategies mentioned,
and any goals or action items. Be empathetic and factual.
Do not include diagnostic language.

Conversation:
{conversation_text}

Summary:"""

    def extract_topics(self, messages: list[dict]) -> list[str]:
        """Extract main topics from conversation messages.

        Args:
            messages: List of message dicts.

        Returns:
            List of topic strings.
        """
        all_text = " ".join(m.get("content", "") for m in messages)
        topic_keywords = {
            "work": ["work", "job", "career", "boss", "colleague", "office"],
            "relationships": ["relationship", "partner", "family", "friend", "dating", "marriage"],
            "health": ["health", "doctor", "medication", "sleep", "exercise", "eating"],
            "stress": ["stress", "pressure", "overwhelmed", "deadline", "anxiety"],
            "self-esteem": ["confidence", "self-worth", "inadequate", "failure", "comparison"],
            "grief": ["loss", "grief", "death", "mourning", "passed away"],
            "loneliness": ["lonely", "alone", "isolated", "no friends", "disconnected"],
        }

        topics = []
        text_lower = all_text.lower()
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)

        return topics if topics else ["general"]

    def extract_coping_strategies(self, messages: list[dict]) -> list[str]:
        """Extract mentioned coping strategies.

        Args:
            messages: List of message dicts.

        Returns:
            List of coping strategy strings.
        """
        strategies = []
        strategy_keywords = [
            "exercise", "walking", "meditation", "deep breathing",
            "journaling", "talking to", "therapy", "counselor",
            "mindfulness", "relaxation", "hobby", "reading",
            "sleep", "rest", "taking a break", "self-care",
        ]

        for msg in messages:
            if msg.get("role") == "user":
                content_lower = msg.get("content", "").lower()
                for strategy in strategy_keywords:
                    if strategy in content_lower and strategy not in strategies:
                        strategies.append(strategy)

        return strategies
