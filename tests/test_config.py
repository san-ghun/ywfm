import pytest

from main import ReminderConfig


class TestParseTimer:
    """Tests for ReminderConfig.parse_timer() static method."""

    def test_hours_minutes_seconds(self):
        assert ReminderConfig.parse_timer("1h10m15s") == 4215

    def test_hours_minutes(self):
        assert ReminderConfig.parse_timer("2h30m") == 9000

    def test_hours_seconds(self):
        assert ReminderConfig.parse_timer("1h45s") == 3645

    def test_minutes_seconds(self):
        assert ReminderConfig.parse_timer("10m30s") == 630

    def test_hours_only(self):
        assert ReminderConfig.parse_timer("2h") == 7200

    def test_minutes_only(self):
        assert ReminderConfig.parse_timer("30m") == 1800

    def test_seconds_only(self):
        assert ReminderConfig.parse_timer("45s") == 45

    def test_zero_values(self):
        assert ReminderConfig.parse_timer("0h0m0s") == 0

    def test_large_values(self):
        assert ReminderConfig.parse_timer("24h60m60s") == 90060

    def test_invalid_format_letters(self):
        with pytest.raises(ValueError, match="Invalid timer format"):
            ReminderConfig.parse_timer("invalid")

    def test_invalid_format_wrong_order(self):
        with pytest.raises(ValueError, match="Invalid timer format"):
            ReminderConfig.parse_timer("10s5m")

    def test_invalid_format_negative(self):
        with pytest.raises(ValueError, match="Invalid timer format"):
            ReminderConfig.parse_timer("-10m")


class TestWaitTime:
    """Tests for ReminderConfig.wait_time property."""

    def test_minimum_time_enforcement(self):
        config = ReminderConfig(timer="5s")
        assert config.wait_time == ReminderConfig.MIN_TIME
        assert config.is_time_limited is True

    def test_at_minimum_boundary(self):
        config = ReminderConfig(timer="15s")
        assert config.wait_time == 15
        assert config.is_time_limited is False

    def test_above_minimum(self):
        config = ReminderConfig(timer="30s")
        assert config.wait_time == 30
        assert config.is_time_limited is False

    def test_default_timer(self):
        config = ReminderConfig()
        assert config.wait_time == ReminderConfig.MIN_TIME * 60


class TestReminderConfigDefaults:
    """Tests for ReminderConfig default values."""

    def test_default_subject(self):
        config = ReminderConfig(timer="30s")
        assert config.subject == ReminderConfig.NAME

    def test_custom_subject(self):
        config = ReminderConfig(subject="Test", timer="30s")
        assert config.subject == "Test"

    def test_timestamps_set(self):
        config = ReminderConfig(timer="30s")
        assert config.created_at is not None
        assert config.trigger_at is not None

    def test_default_booleans(self):
        config = ReminderConfig(timer="30s")
        assert config.show_progress is False
        assert config.background is False
