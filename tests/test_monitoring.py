# ==========================================
# Network Performance Analysis Tool (NPAT)
# Monitoring Tests
# ==========================================

from app.monitoring.monitor import (
    monitor_once,
)


def test_monitor_once_localhost():

    result = monitor_once(
        "127.0.0.1",
        count=2
    )

    assert isinstance(result, dict)

    assert result["host"] == "127.0.0.1"

    assert "ping" in result
    assert "metrics" in result
    assert "analysis" in result
    assert "recommendations" in result
    assert "database_id" in result

    assert isinstance(
        result["recommendations"],
        list
    )

    assert result["database_id"] is not None


def test_monitor_once_contains_metrics():

    result = monitor_once(
        "127.0.0.1",
        count=2
    )

    metrics = result["metrics"]

    assert "packets_sent" in metrics
    assert "packets_received" in metrics
    assert "packet_loss" in metrics
    assert "latency_average" in metrics
    assert "latency_minimum" in metrics
    assert "latency_maximum" in metrics
    assert "jitter" in metrics