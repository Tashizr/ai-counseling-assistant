"""
Conversation engine — the main orchestration brain.

Ties together emotion detection, risk detection, RAG, memory,
and LLM generation into a coherent conversation flow.
"""

import logging
from typing import Optional

from groq import Groq

from config import get_settings
from memory.short_term import ShortTermMemory, Message
from memory.long_term import LongTermMemory
from memory.summarizer import ConversationSummarizer
from rag.generator import RAGGenerator
from services.safety_service import SafetyService
from services.session_manager import SessionManager
from prompts.system_prompt import get_system_prompt
from prompts.templates import IDENTITY_DISCLAIMER

logger = logging.getLogger(__name__)


class ConversationEngine:
    """Main orchestration engine for the AI Counseling Assistant.

    Coordinates all modules to handle user interactions safely
    and effectively.
    """

    def __init__(
        self,
        safety_service: SafetyService,
        session_manager: SessionManager,
        rag_generator: Optional[RAGGenerator] = None,
        long_term_memory: Optional[LongTermMemory] = None,
    ) -> None:
        """Initialize the conversation engine.

        Args:
            safety_service: The SafetyService instance.
            session_manager: The SessionManager instance.
            rag_generator: Optional RAG generator for knowledge retrieval.
            long_term_memory: Optional long-term memory store.
        """
        self._settings = get_settings()
        self._safety = safety_service
        self._session = session_manager
        self._rag = rag_generator
        self._ltm = long_term_memory
        self._short_term = ShortTermMemory(max_messages=self._settings.short_term_max_messages)
        self._summarizer = ConversationSummarizer()
        self._message_count = 0
        logger.info("ConversationEngine initialized")

    def process_message(self, user_message: str) -> dict:
        """Process a user message through the full pipeline.

        Args:
            user_message: The raw user message.

        Returns:
            Dict with 'response', 'emotion', 'risk_level', 'crisis_triggered'.
        """
        safety_result = self._safety.check_input(user_message)

        if safety_result["blocked"]:
            return {
                "response": "I'm sorry, but I can't process that request. "
                           "If you're in distress, please reach out to a crisis hotline.",
                "emotion": "neutral",
                "risk_level": "low",
                "crisis_triggered": False,
            }

        emotion = safety_result["emotion"]
        risk = safety_result["risk"]

        self._short_term.add_message(Message(
            role="user",
            content=user_message,
            emotion=emotion.primary_emotion if emotion else None,
            risk_level=risk.level if risk else "low",
        ))

        if emotion:
            self._short_term.update_mood(emotion.primary_emotion)

        self._session.store_message(
            role="user",
            content=user_message,
            emotion_primary=emotion.primary_emotion if emotion else None,
            emotion_confidence=emotion.confidence if emotion else None,
            risk_level=risk.level if risk else "low",
        )

        if safety_result["crisis_triggered"]:
            rag_context = ""
            if self._rag:
                rag_context = self._rag.get_context(user_message)

            system_prompt = get_system_prompt(
                user_name=self._short_term.user_name,
                emotion=emotion.primary_emotion if emotion else None,
                risk_level="critical",
                rag_context=rag_context,
                memory_context="",
                conversation_context=self._short_term.get_context_string(),
            )

            response_text = self._generate_response(system_prompt, user_message)
            self._store_assistant_response(response_text, "critical")
            return {
                "response": response_text,
                "emotion": emotion.primary_emotion if emotion else "neutral",
                "risk_level": "critical",
                "crisis_triggered": True,
            }

        rag_context = ""
        if self._rag:
            rag_context = self._rag.get_context(user_message)

        memory_context = ""
        if self._ltm and self._session._user_id:
            memories = self._ltm.retrieve_memories(
                self._session._user_id, limit=5, min_importance=3
            )
            if memories:
                memory_context = "\n".join(m["content"] for m in memories)

        system_prompt = get_system_prompt(
            user_name=self._short_term.user_name,
            emotion=emotion.primary_emotion if emotion else None,
            risk_level=risk.level if risk else "low",
            rag_context=rag_context,
            memory_context=memory_context,
            conversation_context=self._short_term.get_context_string(),
        )

        response_text = self._generate_response(system_prompt, user_message)

        post_check = self._safety.check_output(response_text)
        if not post_check["is_safe"]:
            logger.warning("Safety violation in output: %s", post_check["violations"])
            response_text = ("I want to make sure my response is helpful and safe. "
                           "Could you tell me more about what you're experiencing?")

        self._store_assistant_response(response_text, risk.level if risk else "low")

        self._message_count += 1
        if self._message_count % self._settings.long_term_summary_interval == 0:
            self._trigger_periodic_tasks()

        return {
            "response": response_text,
            "emotion": emotion.primary_emotion if emotion else "neutral",
            "risk_level": risk.level if risk else "low",
            "crisis_triggered": False,
        }

    def _generate_response(self, system_prompt: str, user_message: str) -> str:
        """Generate a response using Groq cloud LLM.

        Args:
            system_prompt: The assembled system prompt.
            user_message: The user's message.

        Returns:
            Generated response text.
        """
        try:
            client = Groq(api_key=self._settings.groq_api_key)
            response = client.chat.completions.create(
                model=self._settings.groq_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=self._settings.temperature,
                top_p=self._settings.top_p,
                max_tokens=self._settings.max_response_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("LLM generation failed: %s", e)
            return ("I'm having trouble generating a response right now. "
                   "Please try again in a moment. If you're in crisis, "
                   "please contact a crisis hotline.")

    def _store_assistant_response(self, response: str, risk_level: str) -> None:
        """Store the assistant's response in short-term memory and database.

        Args:
            response: The generated response.
            risk_level: Current risk level.
        """
        self._short_term.add_message(Message(
            role="assistant",
            content=response,
        ))
        self._session.store_message(
            role="assistant",
            content=response,
            risk_level=risk_level,
        )

    def _trigger_periodic_tasks(self) -> None:
        """Run periodic maintenance tasks."""
        if self._ltm:
            self._ltm.cleanup_expired()
        logger.debug("Periodic tasks completed")

    def start_new_session(self, user_id: str) -> str:
        """Start a new conversation session.

        Args:
            user_id: The user identifier.

        Returns:
            The new conversation ID.
        """
        self._short_term.clear()
        self._message_count = 0
        conversation_id = self._session.start_conversation(user_id)
        logger.info("New session started: %s", conversation_id)
        return conversation_id

    def set_user_name(self, name: str) -> None:
        """Set the user's name in short-term memory.

        Args:
            name: The user's name.
        """
        self._short_term.set_user_name(name)

    def get_mood_score(self) -> Optional[int]:
        """Get the current mood score from short-term memory.

        Returns:
            Current mood score (1-10), or None.
        """
        return self._short_term.mood_score

    def get_conversation_context(self) -> str:
        """Get the current conversation context string.

        Returns:
            Formatted context of recent messages.
        """
        return self._short_term.get_context_string()
