"""Prompts package containing safety rules, templates, and system prompt construction."""

from prompts.safety_rules import get_safety_rules, SAFETY_RULES, CRISIS_RESOURCES
from prompts.templates import IDENTITY_DISCLAIMER
from prompts.system_prompt import get_system_prompt

__all__ = [
    "get_safety_rules",
    "SAFETY_RULES",
    "CRISIS_RESOURCES",
    "IDENTITY_DISCLAIMER",
    "get_system_prompt",
]
