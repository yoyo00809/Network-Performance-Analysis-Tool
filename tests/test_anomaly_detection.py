# ==========================================
# NPAT - Anomaly Detection Tests
# ==========================================

from app.analysis.anomaly_detector import (
    detect_latency_anomalies,
    detect_anomalies,
)


def test_no_latency_anomaly():

    response_times = [
        20,
        21,
        22,
        21,
    ]

    anomalies = detect_latency_anomalies(
        response_times
    )

    assert anomalies == []


def test_latency_spike_detected():

    response_times = [
        20,
        21,
        22,
        100,
    ]

    anomalies = detect_latency_anomalies(
        response_times
    )

    assert 100.0 in anomalies


def test_no_anomaly_for_short_data():

    response_times = [
        20,
        21,
        22,
    ]

    anomalies = detect_latency_anomalies(
        response_times
    )

    assert anomalies == []


def test_high_jitter_anomaly():

    metrics = {
        "jitter": 80,
        "packet_loss": 0,
    }

    result = detect_anomalies(
        metrics,
        [20, 21, 22, 23]
    )

    assert result["anomaly_detected"] is True

    assert "High Jitter" in result["anomaly_types"]

    assert result["severity"] == "Warning"


def test_high_packet_loss_anomaly():

    metrics = {
        "jitter": 5,
        "packet_loss": 10,
    }

    result = detect_anomalies(
        metrics,
        [20, 21, 22, 23]
    )

    assert result["anomaly_detected"] is True

    assert "High Packet Loss" in result["anomaly_types"]

    assert result["severity"] == "Warning"


def test_multiple_anomalies():

    metrics = {
        "jitter": 80,
        "packet_loss": 10,
    }

    result = detect_anomalies(
        metrics,
        [20, 21, 22, 100]
    )

    assert result["anomaly_detected"] is True

    assert result["anomaly_count"] == 3

    assert "Latency Spike" in result["anomaly_types"]

    assert "High Jitter" in result["anomaly_types"]

    assert "High Packet Loss" in result["anomaly_types"]

    assert result["severity"] == "Critical"


def test_normal_network():

    metrics = {
        "jitter": 5,
        "packet_loss": 0,
    }

    result = detect_anomalies(
        metrics,
        [20, 21, 22, 21]
    )

    assert result["anomaly_detected"] is False

    assert result["anomaly_count"] == 0

    assert result["anomaly_types"] == []

    assert result["severity"] == "Normal"