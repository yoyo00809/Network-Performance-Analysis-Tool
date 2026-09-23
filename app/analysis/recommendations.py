# ==========================================
# Network Performance Analysis Tool (NPAT)
# Recommendations Module
# ==========================================


def generate_recommendations(metrics, analysis):
    """
    Generate recommendations based on network
    performance metrics and their analysis.

    Args:
        metrics (dict): Calculated network metrics.
        analysis (dict): Performance analysis results.

    Returns:
        list: List of recommendations.
    """

    recommendations = []

    latency_status = analysis.get(
        "latency_status"
    )

    jitter_status = analysis.get(
        "jitter_status"
    )

    packet_loss_status = analysis.get(
        "packet_loss_status"
    )

    # --------------------------------------
    # Latency Recommendations
    # --------------------------------------

    if latency_status == "Poor":
        recommendations.append(
            "High latency detected. "
            "Check network congestion, Wi-Fi signal "
            "strength, or the distance to the destination."
        )

    elif latency_status == "Average":
        recommendations.append(
            "Latency is moderate. "
            "Consider checking network usage if "
            "low response time is required."
        )

    # --------------------------------------
    # Jitter Recommendations
    # --------------------------------------

    if jitter_status == "Poor":
        recommendations.append(
            "High jitter detected. "
            "Check for network congestion, unstable "
            "Wi-Fi, or interference."
        )

    elif jitter_status == "Average":
        recommendations.append(
            "Jitter is moderate. "
            "Monitor the connection for fluctuations."
        )

    # --------------------------------------
    # Packet Loss Recommendations
    # --------------------------------------

    if packet_loss_status == "Poor":
        recommendations.append(
            "High packet loss detected. "
            "Check cables, Wi-Fi stability, network "
            "congestion, and the network connection."
        )

    elif packet_loss_status == "Average":
        recommendations.append(
            "Some packet loss was detected. "
            "Check the network connection and monitor "
            "for recurring packet drops."
        )

    # --------------------------------------
    # Overall Status
    # --------------------------------------

    overall_status = analysis.get(
        "overall_status"
    )

    if overall_status == "Good":
        recommendations.append(
            "Network performance is good. "
            "No immediate action is required."
        )

    elif overall_status == "Unavailable":
        recommendations.append(
            "Network performance could not be "
            "determined. Run the test again."
        )

    # --------------------------------------
    # Default Recommendation
    # --------------------------------------

    if not recommendations:
        recommendations.append(
            "No specific network issue was detected."
        )

    return recommendations