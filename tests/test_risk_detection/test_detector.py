"""Tests for the RiskDetector."""

import pytest
from risk_detection.detector import RiskDetector
from risk_detection.models import RiskResult


class TestRiskDetector:
    """Tests for risk detection functionality."""

    def setup_method(self):
        self.detector = RiskDetector()

    def test_low_risk(self):
        result = self.detector.detect("I'm having a good day today")
        assert result.level == "low"
        assert not result.requires_crisis_resources

    def test_moderate_risk_hopelessness(self):
        result = self.detector.detect("I feel hopeless, nothing will change")
        assert result.level in ("moderate", "high")
        assert result.requires_professional_referral

    def test_high_risk_isolation(self):
        result = self.detector.detect("I'm all alone, nobody cares, I want to give up")
        assert result.level in ("high", "critical")
        assert result.requires_professional_referral

    def test_critical_risk_crisis_language(self):
        result = self.detector.detect("I want to kill myself, I want to end my life")
        assert result.level == "critical"
        assert result.requires_crisis_resources

    def test_empty_input(self):
        result = self.detector.detect("")
        assert result.level == "low"

    def test_should_trigger_crisis(self):
        critical = RiskResult(level="critical")
        assert self.detector.should_trigger_crisis_response(critical)

        low = RiskResult(level="low")
        assert not self.detector.should_trigger_crisis_response(low)

    def test_should_suggest_professional(self):
        moderate = RiskResult(level="moderate")
        assert self.detector.should_suggest_professional(moderate)

        low = RiskResult(level="low")
        assert not self.detector.should_suggest_professional(low)
