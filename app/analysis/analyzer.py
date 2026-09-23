# ==========================================
# Network Performance Analysis Tool (NPAT)
# Performance Analyzer Module
# ==========================================

from app.config.settings import (
    LATENCY_GOOD,
    LATENCY_AVERAGE,
    JITTER_GOOD,
    JITTER_AVERAGE,
    PACKET_LOSS_GOOD,
    PACKET_LOSS_AVERAGE,
)


def analyze_latency(latency):
    """
    Classify latency based on configured thresholds.
    """

    if latency is None:
        return "Unavailable"

    if latency <= LATENCY_GOOD:
        return "Good"

    if latency <= LATENCY_AVERAGE:
        return "Average"

    return "Poor"


def analyze_jitter(jitter):
    """
    Classify jitter based on configured thresholds.
    """

    if jitter is None:
        return "Unavailable"

    if jitter <= JITTER_GOOD:
        return "Good"

    if jitter <= JITTER_AVERAGE:
        return "Average"

    return "Poor"


def analyze_packet_loss(packet_loss):
    """
    Classify packet loss based on configured thresholds.
    """

    if packet_loss is None:
        return "Unavailable"

    if packet_loss <= PACKET_LOSS_GOOD:
        return "Good"

    if packet_loss <= PACKET_LOSS_AVERAGE:
        return "Average"

    return "Poor"


def calculate_overall_status(
    latency_status,
    jitter_status,
    packet_loss_status
):
    """
    Determine the overall network performance status.

    The worst metric determines the overall status.
    """

    statuses = [
        latency_status,
        jitter_status,
        packet_loss_status
    ]

    if "Poor" in statuses:
        return "Poor"

    if "Average" in statuses:
        return "Average"

    if all(status == "Good" for status in statuses):
        return "Good"

    return "Unavailable"


def analyze_performance(metrics):
    """
    Analyze all network performance metrics.

    Args:
        metrics (dict): Calculated metrics from metrics.py.

    Returns:
        dict: Performance analysis results.
    """

    latency_status = analyze_latency(
        metrics.get("latency_average")
    )

    jitter_status = analyze_jitter(
        metrics.get("jitter")
    )

    packet_loss_status = analyze_packet_loss(
        metrics.get("packet_loss")
    )

    overall_status = calculate_overall_status(
        latency_status,
        jitter_status,
        packet_loss_status
    )

    return {
        "latency_status": latency_status,
        "jitter_status": jitter_status,
        "packet_loss_status": packet_loss_status,
        "overall_status": overall_status
    }