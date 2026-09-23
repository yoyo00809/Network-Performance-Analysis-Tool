# ==========================================
# Network Performance Analysis Tool (NPAT)
# Report Generator Module
# ==========================================

from datetime import datetime


def generate_text_report(
    host,
    ping_result,
    metrics,
    analysis,
    recommendations
):
    """
    Generate a text-based network performance report.

    Args:
        host (str): IP address or hostname.
        ping_result (dict): Raw ping results.
        metrics (dict): Calculated network metrics.
        analysis (dict): Performance analysis results.
        recommendations (list): Generated recommendations.

    Returns:
        str: Formatted text report.
    """

    report_lines = []

    # --------------------------------------
    # Report Header
    # --------------------------------------

    report_lines.append("=" * 60)
    report_lines.append(
        "       NETWORK PERFORMANCE ANALYSIS REPORT"
    )
    report_lines.append("=" * 60)

    report_lines.append(
        f"Generated At     : "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    report_lines.append(
        f"Host             : {host}"
    )

    report_lines.append("")

    # --------------------------------------
    # Ping Information
    # --------------------------------------

    report_lines.append(
        "--------------- PING INFORMATION ----------------"
    )

    report_lines.append(
        f"Packets Sent     : "
        f"{ping_result.get('packets_sent')}"
    )

    report_lines.append(
        f"Packets Received : "
        f"{ping_result.get('packets_received')}"
    )

    report_lines.append(
        f"Response Times   : "
        f"{ping_result.get('response_times')}"
    )

    report_lines.append(
        f"Ping Status      : "
        f"{ping_result.get('status')}"
    )

    report_lines.append("")

    # --------------------------------------
    # Network Metrics
    # --------------------------------------

    report_lines.append(
        "--------------- NETWORK METRICS ----------------"
    )

    report_lines.append(
        f"Average Latency  : "
        f"{metrics.get('latency_average')} ms"
    )

    report_lines.append(
        f"Minimum Latency  : "
        f"{metrics.get('latency_minimum')} ms"
    )

    report_lines.append(
        f"Maximum Latency  : "
        f"{metrics.get('latency_maximum')} ms"
    )

    report_lines.append(
        f"Jitter           : "
        f"{metrics.get('jitter')} ms"
    )

    report_lines.append(
        f"Packet Loss      : "
        f"{metrics.get('packet_loss')}%"
    )

    report_lines.append("")

    # --------------------------------------
    # Performance Analysis
    # --------------------------------------

    report_lines.append(
        "--------------- PERFORMANCE ANALYSIS ------------"
    )

    report_lines.append(
        f"Latency Status   : "
        f"{analysis.get('latency_status')}"
    )

    report_lines.append(
        f"Jitter Status    : "
        f"{analysis.get('jitter_status')}"
    )

    report_lines.append(
        f"Packet Loss      : "
        f"{analysis.get('packet_loss_status')}"
    )

    report_lines.append(
        f"Overall Status   : "
        f"{analysis.get('overall_status')}"
    )

    report_lines.append("")

    # --------------------------------------
    # Recommendations
    # --------------------------------------

    report_lines.append(
        "--------------- RECOMMENDATIONS ----------------"
    )

    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):
            report_lines.append(
                f"{index}. {recommendation}"
            )

    else:

        report_lines.append(
            "No recommendations available."
        )

    report_lines.append("")

    # --------------------------------------
    # Report Footer
    # --------------------------------------

    report_lines.append("=" * 60)
    report_lines.append(
        "             END OF REPORT"
    )
    report_lines.append("=" * 60)

    return "\n".join(report_lines)


def save_text_report(report, filename):
    """
    Save a generated text report to a file.

    Args:
        report (str): Report content.
        filename (str): Output file path.

    Returns:
        str: Saved file path.
    """

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    return filename