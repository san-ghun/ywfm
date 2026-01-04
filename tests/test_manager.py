import json
import os
import tempfile
from unittest.mock import patch

import pytest

from main import ReminderManager


class TestReminderManager:
    """Tests for ReminderManager class."""

    @pytest.fixture
    def temp_state_dir(self):
        """Create a temporary state directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def manager_with_temp_dir(self, temp_state_dir):
        """Create a ReminderManager with a temporary state directory."""
        manager = ReminderManager()
        manager.state_dir = temp_state_dir
        return manager

    def test_is_process_running_current_process(self):
        """Current process should be detected as running."""
        manager = ReminderManager()
        assert manager._is_process_running(os.getpid()) is True

    def test_is_process_running_nonexistent_pid(self):
        """Nonexistent PID should not be detected as running."""
        manager = ReminderManager()
        # Use a very high PID that's unlikely to exist
        assert manager._is_process_running(999999999) is False

    def test_load_reminders_empty_dir(self, manager_with_temp_dir):
        """Empty state directory should return empty list."""
        reminders = manager_with_temp_dir._load_reminders()
        assert reminders == []

    def test_load_reminders_nonexistent_dir(self):
        """Nonexistent state directory should return empty list."""
        manager = ReminderManager()
        manager.state_dir = "/nonexistent/path/that/does/not/exist"
        reminders = manager._load_reminders()
        assert reminders == []

    def test_load_reminders_with_json_files(self, manager_with_temp_dir):
        """Should load valid JSON files from state directory."""
        # Create test JSON files
        test_data = {
            "pid": 12345,
            "params": {"subject": "Test", "duration": "1h"},
            "info": {"trigger_at": "2024-01-01_12:00:00"},
        }
        json_path = os.path.join(manager_with_temp_dir.state_dir, "test.json")
        with open(json_path, "w") as f:
            json.dump(test_data, f)

        reminders = manager_with_temp_dir._load_reminders()
        assert len(reminders) == 1
        assert reminders[0]["pid"] == 12345
        assert "_json_path" in reminders[0]

    def test_load_reminders_skips_invalid_json(self, manager_with_temp_dir):
        """Should skip invalid JSON files."""
        # Create invalid JSON file
        invalid_path = os.path.join(
            manager_with_temp_dir.state_dir, "invalid.json"
        )
        with open(invalid_path, "w") as f:
            f.write("not valid json {{{")

        reminders = manager_with_temp_dir._load_reminders()
        assert reminders == []

    def test_list_reminders_no_active(self, manager_with_temp_dir, capsys):
        """Should print message when no active reminders."""
        result = manager_with_temp_dir.list_reminders()
        captured = capsys.readouterr()
        assert result == 0
        assert "No active reminders" in captured.out

    def test_list_reminders_with_active(self, manager_with_temp_dir, capsys):
        """Should list active reminders."""
        # Create a reminder with current PID (so it appears active)
        test_data = {
            "pid": os.getpid(),
            "params": {"subject": "Test Subject", "duration": "30m"},
            "info": {"trigger_at": "2024-01-01_12:00:00"},
        }
        json_path = os.path.join(
            manager_with_temp_dir.state_dir, "active.json"
        )
        with open(json_path, "w") as f:
            json.dump(test_data, f)

        result = manager_with_temp_dir.list_reminders()
        captured = capsys.readouterr()
        assert result == 0
        assert "Test Subject" in captured.out
        assert "30m" in captured.out

    def test_cancel_nonexistent_reminder_by_pid(self, manager_with_temp_dir, capsys):
        """Should return error for nonexistent PID."""
        result = manager_with_temp_dir.cancel_reminder("999999999")
        captured = capsys.readouterr()
        assert result == 1
        assert "No running reminder" in captured.err

    def test_cancel_nonexistent_reminder_by_name(self, manager_with_temp_dir, capsys):
        """Should return error for nonexistent name."""
        result = manager_with_temp_dir.cancel_reminder("nonexistent_name")
        captured = capsys.readouterr()
        assert result == 1
        assert "No reminder found with name" in captured.err
