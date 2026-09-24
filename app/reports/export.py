# ==========================================
# Network Performance Analysis Tool (NPAT)
# Report Export Module
# ==========================================

import csv
import os


def export_report_to_csv(
    filepath,
    host,
    ping_result,
    metrics,
    analysis,
    bandwidth=None
):
    """
    Export network performance results to a CSV file.

    Args:
        filepath (str): Output CSV file path.
        host (str): IP address or hostname.
        ping_result (dict): Raw ping results.
        metrics (dict): Calculated network metrics.
        analysis (dict): Performance analysis results.
        bandwidth (dict): Download and upload speed results.

    Returns:
        str: Path of the generated CSV file.
    """

    if bandwidth is None:
        bandwidth = {}

    # Create output directory if required
    directory = os.path.dirname(filepath)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    row = {
        "Host": host,

        "Packets Sent": ping_result.get(
            "packets_sent"
        ),

        "Packets Received": ping_result.get(
            "packets_received"
        ),

        "Packet Loss (%)": metrics.get(
            "packet_loss"
        ),

        "Average Latency (ms)": metrics.get(
            "latency_average"
        ),

        "Minimum Latency (ms)": metrics.get(
            "latency_minimum"
        ),

        "Maximum Latency (ms)": metrics.get(
            "latency_maximum"
        ),

        "Jitter (ms)": metrics.get(
            "jitter"
        ),

        "Download Speed (Mbps)": bandwidth.get(
            "download_speed_mbps"
        ),

        "Upload Speed (Mbps)": bandwidth.get(
            "upload_speed_mbps"
        ),

        "Latency Status": analysis.get(
            "latency_status"
        ),

        "Jitter Status": analysis.get(
            "jitter_status"
        ),

        "Packet Loss Status": analysis.get(
            "packet_loss_status"
        ),

        "Overall Status": analysis.get(
            "overall_status"
        ),
    }

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=row.keys()
        )

        writer.writeheader()
        writer.writerow(row)

    return filepath


def export_history_to_csv(
    filepath,
    history
):
    """
    Export multiple network test records
    to a CSV file.

    Args:
        filepath (str): Output CSV file path.
        history (list): List of NetworkTest records.

    Returns:
        str: Path of the generated CSV file.
    """

    directory = os.path.dirname(filepath)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    fieldnames = [
        "ID",
        "Host",
        "Packets Sent",
        "Packets Received",
        "Packet Loss (%)",
        "Average Latency (ms)",
        "Minimum Latency (ms)",
        "Maximum Latency (ms)",
        "Jitter (ms)",
        "Download Speed (Mbps)",
        "Upload Speed (Mbps)",
        "Latency Status",
        "Jitter Status",
        "Packet Loss Status",
        "Overall Status",
        "Created At",
    ]

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for record in history:

            writer.writerow({
                "ID": record.id,

                "Host": record.host,

                "Packets Sent": record.packets_sent,

                "Packets Received": record.packets_received,

                "Packet Loss (%)": record.packet_loss,

                "Average Latency (ms)": (
                    record.latency_average
                ),

                "Minimum Latency (ms)": (
                    record.latency_minimum
                ),

                "Maximum Latency (ms)": (
                    record.latency_maximum
                ),

                "Jitter (ms)": record.jitter,

                "Download Speed (Mbps)": getattr(
                    record,
                    "download_speed_mbps",
                    None
                ),

                "Upload Speed (Mbps)": getattr(
                    record,
                    "upload_speed_mbps",
                    None
                ),

                "Latency Status": (
                    record.latency_status
                ),

                "Jitter Status": (
                    record.jitter_status
                ),

                "Packet Loss Status": (
                    record.packet_loss_status
                ),

                "Overall Status": (
                    record.overall_status
                ),

                "Created At": (
                    record.created_at
                ),
            })

    return filepath