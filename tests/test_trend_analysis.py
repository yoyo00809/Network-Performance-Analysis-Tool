# ==========================================
# Network Performance Analysis Tool (NPAT)
# Historical Trend Analysis Tests
# ==========================================


from types import SimpleNamespace

import pytest

from app.analysis.trend_analysis import (
    calculate_trend,
    analyze_historical_tests,
    get_metric_series,
)


def test_calculate_trend():

    result = calculate_trend(
        [10, 20, 30, 40]
    )

    assert result["average"] == 25.0
    assert result["minimum"] == 10.0
    assert result["maximum"] == 40.0
    assert result["count"] == 4


def test_calculate_trend_ignores_none():

    result = calculate_trend(
        [10, None, 20, None, 30]
    )

    assert result["average"] == 20.0
    assert result["minimum"] == 10.0
    assert result["maximum"] == 30.0
    assert result["count"] == 3


def test_calculate_trend_empty_values():

    result = calculate_trend([])

    assert result["average"] is None
    assert result["minimum"] is None
    assert result["maximum"] is None
    assert result["count"] == 0


def test_analyze_historical_tests():

    records = [
        SimpleNamespace(
            latency_average=20.0,
            jitter=5.0,
            packet_loss=0.0,
            health_score=95.0,
            download_speed_mbps=100.0,
            upload_speed_mbps=50.0,
            network_state="Available",
            failure_detected=False,
            recovery_detected=False,
        ),
        SimpleNamespace(
            latency_average=40.0,
            jitter=10.0,
            packet_loss=2.0,
            health_score=80.0,
            download_speed_mbps=80.0,
            upload_speed_mbps=40.0,
            network_state="Unavailable",
            failure_detected=True,
            recovery_detected=False,
        ),
        SimpleNamespace(
            latency_average=30.0,
            jitter=15.0,
            packet_loss=1.0,
            health_score=90.0,
            download_speed_mbps=120.0,
            upload_speed_mbps=60.0,
            network_state="Available",
            failure_detected=False,
            recovery_detected=True,
        ),
    ]

    result = analyze_historical_tests(
        records
    )

    assert result["total_tests"] == 3

    # --------------------------------------
    # Latency
    # --------------------------------------

    assert result["latency"]["average"] == 30.0
    assert result["latency"]["minimum"] == 20.0
    assert result["latency"]["maximum"] == 40.0
    assert result["latency"]["count"] == 3

    # --------------------------------------
    # Jitter
    # --------------------------------------

    assert result["jitter"]["average"] == 10.0
    assert result["jitter"]["minimum"] == 5.0
    assert result["jitter"]["maximum"] == 15.0
    assert result["jitter"]["count"] == 3

    # --------------------------------------
    # Packet Loss
    # --------------------------------------

    assert result["packet_loss"]["average"] == 1.0
    assert result["packet_loss"]["minimum"] == 0.0
    assert result["packet_loss"]["maximum"] == 2.0
    assert result["packet_loss"]["count"] == 3

    # --------------------------------------
    # Health Score
    # --------------------------------------

    assert result["health_score"]["average"] == 88.33
    assert result["health_score"]["minimum"] == 80.0
    assert result["health_score"]["maximum"] == 95.0
    assert result["health_score"]["count"] == 3

    # --------------------------------------
    # Download Speed
    # --------------------------------------

    assert result["download_speed"]["average"] == 100.0
    assert result["download_speed"]["minimum"] == 80.0
    assert result["download_speed"]["maximum"] == 120.0
    assert result["download_speed"]["count"] == 3

    # --------------------------------------
    # Upload Speed
    # --------------------------------------

    assert result["upload_speed"]["average"] == 50.0
    assert result["upload_speed"]["minimum"] == 40.0
    assert result["upload_speed"]["maximum"] == 60.0
    assert result["upload_speed"]["count"] == 3

    # --------------------------------------
    # Availability
    # --------------------------------------

    assert result["availability"]["available"] == 2
    assert result["availability"]["unavailable"] == 1

    # --------------------------------------
    # Failure / Recovery
    # --------------------------------------

    assert result["failure_events"] == 1
    assert result["recovery_events"] == 1


def test_analyze_empty_history():

    result = analyze_historical_tests([])

    assert result["total_tests"] == 0

    assert result["latency"]["count"] == 0
    assert result["jitter"]["count"] == 0
    assert result["packet_loss"]["count"] == 0
    assert result["health_score"]["count"] == 0
    assert result["download_speed"]["count"] == 0
    assert result["upload_speed"]["count"] == 0

    assert result["availability"]["available"] == 0
    assert result["availability"]["unavailable"] == 0

    assert result["failure_events"] == 0
    assert result["recovery_events"] == 0


def test_get_metric_series():

    records = [
        SimpleNamespace(
            latency_average=20.0,
            jitter=5.0,
            packet_loss=0.0,
            health_score=95.0,
            download_speed_mbps=100.0,
            upload_speed_mbps=50.0,
        ),
        SimpleNamespace(
            latency_average=40.0,
            jitter=10.0,
            packet_loss=2.0,
            health_score=80.0,
            download_speed_mbps=80.0,
            upload_speed_mbps=40.0,
        ),
        SimpleNamespace(
            latency_average=None,
            jitter=None,
            packet_loss=None,
            health_score=None,
            download_speed_mbps=None,
            upload_speed_mbps=None,
        ),
    ]

    result = get_metric_series(
        records
    )

    assert result["latency"] == [
        20.0,
        40.0,
        None,
    ]

    assert result["jitter"] == [
        5.0,
        10.0,
        None,
    ]

    assert result["packet_loss"] == [
        0.0,
        2.0,
        None,
    ]

    assert result["health_score"] == [
        95.0,
        80.0,
        None,
    ]

    assert result["download_speed"] == [
        100.0,
        80.0,
        None,
    ]

    assert result["upload_speed"] == [
        50.0,
        40.0,
        None,
    ]