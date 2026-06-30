"""Tests for the configuration module."""

import pytest
from config import Settings


class TestSettings:
    """Tests for Settings dataclass."""

    def test_default_values(self):
        s = Settings()
        assert s.ollama_base_url == "http://localhost:11434"
        assert s.ollama_model == "llama3.2"
        assert s.temperature == 0.7
        assert s.top_p == 0.9
        assert s.log_level == "INFO"

    def test_invalid_temperature(self):
        with pytest.raises(ValueError, match="temperature"):
            Settings(temperature=5.0)

    def test_invalid_top_p(self):
        with pytest.raises(ValueError, match="top_p"):
            Settings(top_p=2.0)

    def test_invalid_risk_threshold(self):
        with pytest.raises(ValueError, match="risk_threshold"):
            Settings(risk_threshold="invalid")

    def test_invalid_log_level(self):
        with pytest.raises(ValueError, match="log_level"):
            Settings(log_level="VERBOSE")

    def test_frozen(self):
        s = Settings()
        with pytest.raises(AttributeError):
            s.temperature = 1.0
