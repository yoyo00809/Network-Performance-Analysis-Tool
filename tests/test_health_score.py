from app.analysis.health_score import (
    calculate_latency_score,
    calculate_jitter_score,
    calculate_packet_loss_score,
    calculate_health_score,
)


def test_latency_score():
    assert calculate_latency_score(10) == 100
    assert calculate_latency_score(30) == 90
    assert calculate_latency_score(75) == 70
    assert calculate_latency_score(150) == 40
    assert calculate_latency_score(250) == 0


def test_jitter_score():
    assert calculate_jitter_score(2) == 100
    assert calculate_jitter_score(10) == 90
    assert calculate_jitter_score(30) == 70
    assert calculate_jitter_score(75) == 40
    assert calculate_jitter_score(150) == 0


def test_packet_loss_score():
    assert calculate_packet_loss_score(0) == 100
    assert calculate_packet_loss_score(0.5) == 90
    assert calculate_packet_loss_score(3) == 70
    assert calculate_packet_loss_score(8) == 40
    assert calculate_packet_loss_score(15) == 0


def test_health_score_good_network():
    metrics = {
        "latency_average": 30,
        "jitter": 10,
        "packet_loss": 0,
    }

    result = calculate_health_score(metrics)

    assert result["health_score"] == 93
    assert result["health_status"] == "Excellent"


def test_health_score_poor_network():
    metrics = {
        "latency_average": 250,
        "jitter": 150,
        "packet_loss": 15,
    }

    result = calculate_health_score(metrics)

    assert result["health_score"] == 0
    assert result["health_status"] == "Poor"


def test_health_score_unavailable():
    metrics = {
        "latency_average": None,
        "jitter": None,
        "packet_loss": None,
    }

    result = calculate_health_score(metrics)

    assert result["health_score"] is None
    assert result["health_status"] == "Unavailable"