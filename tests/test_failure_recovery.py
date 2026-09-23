# ==========================================
# Network Performance Analysis Tool (NPAT)
# Failure & Recovery Detection Tests
# ==========================================

from datetime import datetime, timedelta

import pytest

from app.monitoring.failure_recovery import (
    NetworkFailureRecoveryTracker,
    is_network_available,
    process_ping_result,
)


def test_initial_state_is_unknown():
    tracker = NetworkFailureRecoveryTracker()

    assert tracker.state == "Unknown"
    assert tracker.failure_count == 0


def test_available_network_is_detected():
    tracker = NetworkFailureRecoveryTracker()

    result = tracker.process_check(
        True,
        datetime(2026, 9, 23, 10, 0, 0)
    )

    assert result["state"] == "Available"
    assert result["failure_detected"] is False
    assert result["recovery_detected"] is False


def test_failure_is_detected():
    tracker = NetworkFailureRecoveryTracker(
        initial_state="Available"
    )

    timestamp = datetime(2026, 9, 23, 10, 0, 0)

    result = tracker.process_check(
        False,
        timestamp
    )

    assert result["state"] == "Unavailable"
    assert result["failure_detected"] is True
    assert result["recovery_detected"] is False
    assert result["failure_count"] == 1


def test_consecutive_failures_are_counted():
    tracker = NetworkFailureRecoveryTracker(
        initial_state="Available"
    )

    timestamp = datetime(2026, 9, 23, 10, 0, 0)

    first = tracker.process_check(
        False,
        timestamp
    )

    second = tracker.process_check(
        False,
        timestamp + timedelta(seconds=5)
    )

    third = tracker.process_check(
        False,
        timestamp + timedelta(seconds=10)
    )

    assert first["failure_count"] == 1
    assert second["failure_count"] == 2
    assert third["failure_count"] == 3

    assert first["failure_detected"] is True
    assert second["failure_detected"] is False
    assert third["failure_detected"] is False


def test_recovery_is_detected():
    tracker = NetworkFailureRecoveryTracker(
        initial_state="Available"
    )

    timestamp = datetime(2026, 9, 23, 10, 0, 0)

    tracker.process_check(
        False,
        timestamp
    )

    result = tracker.process_check(
        True,
        timestamp + timedelta(seconds=15)
    )

    assert result["state"] == "Available"
    assert result["failure_detected"] is False
    assert result["recovery_detected"] is True
    assert result["failure_duration_seconds"] == 15.0
    assert result["failure_count"] == 0


def test_recovery_resets_failure_tracking():
    tracker = NetworkFailureRecoveryTracker(
        initial_state="Available"
    )

    timestamp = datetime(2026, 9, 23, 10, 0, 0)

    tracker.process_check(
        False,
        timestamp
    )

    tracker.process_check(
        True,
        timestamp + timedelta(seconds=20)
    )

    status = tracker.get_status()

    assert status["state"] == "Available"
    assert status["failure_count"] == 0
    assert status["failure_duration_seconds"] is None


def test_ping_result_availability():
    available_result = {
        "packets_received": 4
    }

    unavailable_result = {
        "packets_received": 0
    }

    assert is_network_available(
        available_result
    ) is True

    assert is_network_available(
        unavailable_result
    ) is False


def test_ping_result_can_be_processed():
    tracker = NetworkFailureRecoveryTracker(
        initial_state="Available"
    )

    timestamp = datetime(2026, 9, 23, 10, 0, 0)

    result = process_ping_result(
        tracker,
        {"packets_received": 0},
        timestamp
    )

    assert result["failure_detected"] is True
    assert result["state"] == "Unavailable"


def test_invalid_state_is_rejected():
    with pytest.raises(ValueError):
        NetworkFailureRecoveryTracker(
            initial_state="Broken"
        )


def test_invalid_availability_is_rejected():
    tracker = NetworkFailureRecoveryTracker()

    with pytest.raises(TypeError):
        tracker.process_check("yes")
