# ==========================================
# Network Performance Analysis Tool (NPAT)
# Analysis Tests
# ==========================================

from app.analysis.metrics import (
    calculate_average,
    calculate_minimum,
    calculate_maximum,
    calculate_jitter,
    calculate_packet_loss,
)

from app.analysis.analyzer import (
    analyze_latency,
    analyze_jitter,
    analyze_packet_loss,
    calculate_overall_status,
    analyze_performance,
)

from app.analysis.recommendations import (
    generate_recommendations,
)


# ==========================================
# Metrics Tests
# ==========================================

def test_calculate_average():

    values = [42, 28, 36, 44]

    assert calculate_average(values) == 37.5


def test_calculate_minimum():

    values = [42, 28, 36, 44]

    assert calculate_minimum(values) == 28


def test_calculate_maximum():

    values = [42, 28, 36, 44]

    assert calculate_maximum(values) == 44


def test_calculate_jitter():

    values = [42, 28, 36, 44]

    assert calculate_jitter(values) == 10.0


def test_calculate_packet_loss():

    assert calculate_packet_loss(4, 4) == 0.0
    assert calculate_packet_loss(4, 3) == 25.0


# ==========================================
# Analyzer Tests
# ==========================================

def test_analyze_latency():

    assert analyze_latency(30) == "Good"
    assert analyze_latency(75) == "Average"
    assert analyze_latency(150) == "Poor"


def test_analyze_jitter():

    assert analyze_jitter(10) == "Good"
    assert analyze_jitter(30) == "Average"
    assert analyze_jitter(60) == "Poor"


def test_analyze_packet_loss():

    assert analyze_packet_loss(0) == "Good"
    assert analyze_packet_loss(3) == "Average"
    assert analyze_packet_loss(10) == "Poor"


def test_calculate_overall_status():

    assert calculate_overall_status(
        "Good",
        "Good",
        "Good"
    ) == "Good"

    assert calculate_overall_status(
        "Good",
        "Average",
        "Good"
    ) == "Average"

    assert calculate_overall_status(
        "Good",
        "Good",
        "Poor"
    ) == "Poor"


def test_analyze_performance():

    metrics = {
        "latency_average": 37.5,
        "jitter": 10.0,
        "packet_loss": 0.0
    }

    result = analyze_performance(
        metrics
    )

    assert result["latency_status"] == "Good"
    assert result["jitter_status"] == "Good"
    assert result["packet_loss_status"] == "Good"
    assert result["overall_status"] == "Good"


# ==========================================
# Recommendations Tests
# ==========================================

def test_good_network_recommendation():

    metrics = {
        "latency_average": 30,
        "jitter": 5,
        "packet_loss": 0.0
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Good"
    }

    result = generate_recommendations(
        metrics,
        analysis
    )

    assert isinstance(result, list)
    assert len(result) >= 1

    assert (
        "Network performance is good."
        in result[0]
    )


def test_poor_latency_recommendation():

    metrics = {
        "latency_average": 150,
        "jitter": 5,
        "packet_loss": 0.0
    }

    analysis = {
        "latency_status": "Poor",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Poor"
    }

    result = generate_recommendations(
        metrics,
        analysis
    )

    assert len(result) >= 1

    assert any(
        "High latency detected"
        in recommendation
        for recommendation in result
    )


def test_poor_packet_loss_recommendation():

    metrics = {
        "latency_average": 30,
        "jitter": 5,
        "packet_loss": 25.0
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Poor",
        "overall_status": "Poor"
    }

    result = generate_recommendations(
        metrics,
        analysis
    )

    assert len(result) >= 1

    assert any(
        "High packet loss detected"
        in recommendation
        for recommendation in result
    )


def test_poor_jitter_recommendation():

    metrics = {
        "latency_average": 30,
        "jitter": 60,
        "packet_loss": 0.0
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Poor",
        "packet_loss_status": "Good",
        "overall_status": "Poor"
    }

    result = generate_recommendations(
        metrics,
        analysis
    )

    assert len(result) >= 1

    assert any(
        "High jitter detected"
        in recommendation
        for recommendation in result
    )