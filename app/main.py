# ==========================================
# Network Performance Analysis Tool (NPAT)
# Main Application
# ==========================================

import os

from app.monitoring.monitor import monitor_once

from app.reports.report_generator import (
    generate_text_report,
    save_text_report,
)

from app.reports.export import (
    export_report_to_csv,
)


def main():

    print("========================================")
    print("   Network Performance Analysis Tool")
    print("========================================")

    # --------------------------------------
    # Get Target Host
    # --------------------------------------

    host = input(
        "Enter IP address or hostname: "
    ).strip()

    if not host:

        print("\nError: Host cannot be empty.")
        return

    print(
        f"\nTesting network connection to: {host}"
    )

    print("Please wait...\n")

    # --------------------------------------
    # Run Complete Monitoring Pipeline
    # --------------------------------------

    result = monitor_once(
        host,
        count=4
    )

    ping_result = result["ping"]
    metrics = result["metrics"]
    analysis = result["analysis"]
    recommendations = result["recommendations"]

    # --------------------------------------
    # Display Results
    # --------------------------------------

    print(
        "------------- RESULTS ----------------"
    )

    print(
        f"Host             : "
        f"{host}"
    )

    print(
        f"Packets Sent     : "
        f"{metrics['packets_sent']}"
    )

    print(
        f"Packets Received : "
        f"{metrics['packets_received']}"
    )

    print(
        f"Packet Loss      : "
        f"{metrics['packet_loss']}%"
    )

    print(
        f"Response Times   : "
        f"{ping_result['response_times']}"
    )

    print(
        f"Average Latency  : "
        f"{metrics['latency_average']} ms"
    )

    print(
        f"Minimum Latency  : "
        f"{metrics['latency_minimum']} ms"
    )

    print(
        f"Maximum Latency  : "
        f"{metrics['latency_maximum']} ms"
    )

    print(
        f"Jitter           : "
        f"{metrics['jitter']} ms"
    )

    print("--------------------------------------")

    print(
        f"Latency Status   : "
        f"{analysis['latency_status']}"
    )

    print(
        f"Jitter Status    : "
        f"{analysis['jitter_status']}"
    )

    print(
        f"Packet Loss      : "
        f"{analysis['packet_loss_status']}"
    )

    print(
        f"Overall Status   : "
        f"{analysis['overall_status']}"
    )

    print("--------------------------------------")

    # --------------------------------------
    # Recommendations
    # --------------------------------------

    print("RECOMMENDATIONS")
    print("--------------------------------------")

    for recommendation in recommendations:

        print(
            f"- {recommendation}"
        )

    print("--------------------------------------")

    # --------------------------------------
    # Database Information
    # --------------------------------------

    print(
        f"Database Record  : "
        f"{result['database_id']}"
    )

    # --------------------------------------
    # Generate Text Report
    # --------------------------------------

    report = generate_text_report(
        host,
        ping_result,
        metrics,
        analysis,
        recommendations
    )

    # --------------------------------------
    # Create Reports Directory
    # --------------------------------------

    reports_directory = os.path.join(
        "data",
        "reports"
    )

    os.makedirs(
        reports_directory,
        exist_ok=True
    )

    # --------------------------------------
    # Save Text Report
    # --------------------------------------

    text_report_path = os.path.join(
        reports_directory,
        "network_report.txt"
    )

    save_text_report(
        report,
        text_report_path
    )

    # --------------------------------------
    # Export CSV Report
    # --------------------------------------

    csv_report_path = os.path.join(
        reports_directory,
        "network_report.csv"
    )

    export_report_to_csv(
        csv_report_path,
        host,
        ping_result,
        metrics,
        analysis
    )

    # --------------------------------------
    # Report Information
    # --------------------------------------

    print("--------------------------------------")
    print("REPORTS GENERATED")
    print("--------------------------------------")

    print(
        f"Text Report     : "
        f"{text_report_path}"
    )

    print(
        f"CSV Report      : "
        f"{csv_report_path}"
    )

    print("--------------------------------------")


if __name__ == "__main__":
    main()