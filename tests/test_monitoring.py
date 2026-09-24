# ==========================================
# Network Performance Analysis Tool (NPAT)
# Monitoring Tests
# ==========================================

from unittest.mock import patch

from app.monitoring.monitor import (
    monitor_once,
    measure_bandwidth,
)


# ==========================================
# Existing Monitoring Tests
# ==========================================

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


# ==========================================
# Bandwidth Measurement Tests
# ==========================================

def test_measure_bandwidth_returns_speeds():

    with patch(
        "app.monitoring.monitor.measure_download_speed",
        return_value=100.5
    ) as mock_download:

        with patch(
            "app.monitoring.monitor.measure_upload_speed",
            return_value=50.25
        ) as mock_upload:

            result = measure_bandwidth()

    assert isinstance(result, dict)

    assert "download_speed_mbps" in result
    assert "upload_speed_mbps" in result

    assert result["download_speed_mbps"] == 100.5
    assert result["upload_speed_mbps"] == 50.25

    mock_download.assert_called_once()
    mock_upload.assert_called_once()


def test_measure_bandwidth_handles_download_failure():

    with patch(
        "app.monitoring.monitor.measure_download_speed",
        side_effect=Exception("Download test failed")
    ):

        with patch(
            "app.monitoring.monitor.measure_upload_speed",
            return_value=50.0
        ):

            result = measure_bandwidth()

    assert result["download_speed_mbps"] is None
    assert result["upload_speed_mbps"] == 50.0


def test_measure_bandwidth_handles_upload_failure():

    with patch(
        "app.monitoring.monitor.measure_download_speed",
        return_value=100.0
    ):

        with patch(
            "app.monitoring.monitor.measure_upload_speed",
            side_effect=Exception("Upload test failed")
        ):

            result = measure_bandwidth()

    assert result["download_speed_mbps"] == 100.0
    assert result["upload_speed_mbps"] is None


# ==========================================
# Bandwidth Integration Tests
# ==========================================

def test_monitor_once_bandwidth_disabled_by_default():

    result = monitor_once(
        "127.0.0.1",
        count=2
    )

    assert "bandwidth" in result

    assert result["bandwidth"]["download_speed_mbps"] is None
    assert result["bandwidth"]["upload_speed_mbps"] is None


def test_monitor_once_with_bandwidth():

    with patch(
        "app.monitoring.monitor.measure_download_speed",
        return_value=120.75
    ):

        with patch(
            "app.monitoring.monitor.measure_upload_speed",
            return_value=60.50
        ):

            result = monitor_once(
                "127.0.0.1",
                count=2,
                include_bandwidth=True
            )

    assert "bandwidth" in result

    assert result["bandwidth"]["download_speed_mbps"] == 120.75
    assert result["bandwidth"]["upload_speed_mbps"] == 60.50

    assert result["database_id"] is not None