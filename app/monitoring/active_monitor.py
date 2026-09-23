# ==========================================
# Network Performance Analysis Tool (NPAT)
# Active Connection Monitoring
# ==========================================

import time

from app.monitoring.monitor import monitor_once


def active_monitor(
    host,
    checks=5,
    interval=5,
    count=4
):
    """
    Perform repeated network monitoring checks.

    Args:
        host (str): IP address or hostname.
        checks (int): Number of monitoring cycles.
        interval (float): Delay between checks in seconds.
        count (int): Number of ping packets per check.

    Returns:
        dict: Active monitoring results.
    """

    if not isinstance(host, str) or not host.strip():
        raise ValueError(
            "host must be a non-empty string."
        )

    if not isinstance(checks, int) or checks <= 0:
        raise ValueError(
            "checks must be a positive integer."
        )

    if not isinstance(interval, (int, float)):
        raise TypeError(
            "interval must be a number."
        )

    if interval < 0:
        raise ValueError(
            "interval cannot be negative."
        )

    if not isinstance(count, int) or count <= 0:
        raise ValueError(
            "count must be a positive integer."
        )

    results = []

    for check_number in range(1, checks + 1):

        result = monitor_once(
            host,
            count=count
        )

        results.append({
            "check_number": check_number,
            "result": result,
        })

        if check_number < checks and interval > 0:
            time.sleep(interval)

    available_checks = sum(
        1
        for item in results
        if item["result"][
            "failure_recovery"
        ]["state"] == "Available"
    )

    unavailable_checks = sum(
        1
        for item in results
        if item["result"][
            "failure_recovery"
        ]["state"] == "Unavailable"
    )

    failure_events = sum(
        1
        for item in results
        if item["result"][
            "failure_recovery"
        ]["failure_detected"]
    )

    recovery_events = sum(
        1
        for item in results
        if item["result"][
            "failure_recovery"
        ]["recovery_detected"]
    )

    return {
        "host": host,
        "checks": checks,
        "interval": interval,
        "results": results,
        "available_checks": available_checks,
        "unavailable_checks": unavailable_checks,
        "failure_events": failure_events,
        "recovery_events": recovery_events,
    }