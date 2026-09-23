# ==========================================
# Network Performance Analysis Tool (NPAT)
# Active Monitoring Tests
# ==========================================

import pytest

from app.monitoring.active_monitor import (
    active_monitor,
)


def test_active_monitor_single_check():

    result = active_monitor(
        "127.0.0.1",
        checks=1,
        interval=0,
        count=2
    )

    assert isinstance(result, dict)

    assert result["host"] == "127.0.0.1"
    assert result["checks"] == 1
    assert result["interval"] == 0

    assert len(result["results"]) == 1

    assert result["available_checks"] >= 0
    assert result["unavailable_checks"] >= 0
    assert result["failure_events"] >= 0
    assert result["recovery_events"] >= 0


def test_active_monitor_multiple_checks():

    result = active_monitor(
        "127.0.0.1",
        checks=3,
        interval=0,
        count=2
    )

    assert result["checks"] == 3
    assert len(result["results"]) == 3

    for index, item in enumerate(
        result["results"],
        start=1
    ):

        assert item["check_number"] == index

        assert isinstance(
            item["result"],
            dict
        )

        assert "host" in item["result"]
        assert "ping" in item["result"]
        assert "metrics" in item["result"]
        assert "analysis" in item["result"]
        assert "health_score" in item["result"]
        assert "anomaly" in item["result"]
        assert "failure_recovery" in item["result"]
        assert "database_id" in item["result"]


def test_active_monitor_counts_match_results():

    result = active_monitor(
        "127.0.0.1",
        checks=4,
        interval=0,
        count=1
    )

    states = [
        item["result"]["failure_recovery"]["state"]
        for item in result["results"]
    ]

    expected_available = states.count(
        "Available"
    )

    expected_unavailable = states.count(
        "Unavailable"
    )

    assert (
        result["available_checks"]
        == expected_available
    )

    assert (
        result["unavailable_checks"]
        == expected_unavailable
    )


def test_active_monitor_rejects_invalid_checks():

    with pytest.raises(ValueError):

        active_monitor(
            "127.0.0.1",
            checks=0,
            interval=0,
            count=1
        )


def test_active_monitor_rejects_negative_interval():

    with pytest.raises(ValueError):

        active_monitor(
            "127.0.0.1",
            checks=1,
            interval=-1,
            count=1
        )


def test_active_monitor_rejects_invalid_host():

    with pytest.raises(ValueError):

        active_monitor(
            "",
            checks=1,
            interval=0,
            count=1
        )
        
def test_active_monitor_failure_recovery_transition(
    monkeypatch
):
    """
    Verify that Active Monitoring correctly handles
    an Available -> Unavailable -> Unavailable
    -> Available sequence.
    """

    from app.monitoring import active_monitor as active_module
    from app.monitoring.failure_recovery import (
        NetworkFailureRecoveryTracker,
    )

    tracker = NetworkFailureRecoveryTracker()

    states = [
        "Available",
        "Unavailable",
        "Unavailable",
        "Available",
    ]

    def fake_monitor_once(
        host,
        count=4
    ):
        state = states.pop(0)

        if state == "Available":

            ping_result = {
                "packets_sent": count,
                "packets_received": count,
                "response_times": [10.0] * count,
            }

        else:

            ping_result = {
                "packets_sent": count,
                "packets_received": 0,
                "response_times": [],
            }

        failure_recovery = (
            tracker.process_check(
                state == "Available"
            )
        )

        return {
            "host": host,
            "ping": ping_result,
            "metrics": {},
            "analysis": {},
            "health_score": {},
            "anomaly": {},
            "failure_recovery": failure_recovery,
            "recommendations": [],
            "database_id": None,
        }

    monkeypatch.setattr(
        active_module,
        "monitor_once",
        fake_monitor_once
    )

    result = active_module.active_monitor(
        "test.example",
        checks=4,
        interval=0,
        count=2
    )

    results = result["results"]

    assert len(results) == 4

    states_found = [
        item["result"][
            "failure_recovery"
        ]["state"]
        for item in results
    ]

    assert states_found == [
        "Available",
        "Unavailable",
        "Unavailable",
        "Available",
    ]

    failure_events = [
        item["result"][
            "failure_recovery"
        ]["failure_detected"]
        for item in results
    ]

    recovery_events = [
        item["result"][
            "failure_recovery"
        ]["recovery_detected"]
        for item in results
    ]

    assert failure_events == [
        False,
        True,
        False,
        False,
    ]

    assert recovery_events == [
        False,
        False,
        False,
        True,
    ]

    assert result["available_checks"] == 2
    assert result["unavailable_checks"] == 2
    assert result["failure_events"] == 1
    assert result["recovery_events"] == 1

    final_result = results[-1]["result"]

    assert (
        final_result[
            "failure_recovery"
        ]["failure_count"] == 0
    )

    assert (
        final_result[
            "failure_recovery"
        ]["failure_duration_seconds"]
        is not None
    )