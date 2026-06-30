"""Tests for the SafetyService."""

import pytest
from services.safety_service import SafetyService


class TestSafetyService:
    """Tests for safety service functionality."""

    def setup_method(self):
        self.safety = SafetyService()

    def test_normal_input(self):
        result = self.safety.check_input("I'm feeling a bit stressed")
        assert not result["blocked"]
        assert result["emotion"] is not None
        assert result["risk"] is not None

    def test_crisis_detection(self):
        result = self.safety.check_input("I want to kill myself")
        assert result["crisis_triggered"]
        assert result["risk"].level == "critical"

    def test_blocked_content(self):
        result = self.safety.check_input("How to make a bomb")
        assert result["blocked"]

    def test_output_safety(self):
        result = self.safety.check_output("I hear you and I'm here to support you.")
        assert result["is_safe"]

    def test_crisis_response_formatting(self):
        from risk_detection.models import RiskResult
        risk = RiskResult(level="critical", requires_crisis_resources=True)
        response = self.safety.format_crisis_response(risk)
        assert "988" in response or "crisis" in response.lower()
