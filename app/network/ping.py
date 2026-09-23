# ==========================================
# Network Performance Analysis Tool (NPAT)
# Ping Data Collection Module
# ==========================================

import platform
import subprocess
import re

from app.config.settings import (
    DEFAULT_PING_COUNT,
    PING_TIMEOUT,
)


def ping_host(host, count=DEFAULT_PING_COUNT):
    """
    Ping a host and collect raw network response data.

    This module is responsible only for collecting
    ping information. Metric calculations are handled
    by metrics.py.

    Args:
        host (str): IP address or hostname.
        count (int): Number of ping requests.

    Returns:
        dict: Raw ping data.
    """

    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", str(count), host]
    else:
        command = ["ping", "-c", str(count), host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=PING_TIMEOUT
        )

        output = result.stdout

        # Extract individual response times
        response_times = extract_response_times(output, system)

        # Count successful responses
        packets_received = len(response_times)

        return {
            "host": host,
            "packets_sent": count,
            "packets_received": packets_received,
            "response_times": response_times,
            "status": "Success" if packets_received > 0 else "Failed"
        }

    except subprocess.TimeoutExpired:
        return {
            "host": host,
            "packets_sent": count,
            "packets_received": 0,
            "response_times": [],
            "status": "Timeout"
        }

    except Exception as error:
        return {
            "host": host,
            "packets_sent": count,
            "packets_received": 0,
            "response_times": [],
            "status": f"Error: {error}"
        }


def extract_response_times(output, system):
    """
    Extract individual ping response times from
    the operating system's ping output.
    """

    if system == "windows":
        pattern = r"time[=<]\s*(\d+)\s*ms"
    else:
        pattern = r"time[=<]\s*([\d.]+)\s*ms"

    matches = re.findall(pattern, output)

    return [float(value) for value in matches]