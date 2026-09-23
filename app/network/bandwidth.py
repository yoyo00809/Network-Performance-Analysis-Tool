# ==========================================
# Network Performance Analysis Tool (NPAT)
# Bandwidth Measurement Module
# ==========================================

import time

import requests


def measure_download_speed(url, timeout=30):
    """
    Measure approximate download speed from an HTTP resource.

    Args:
        url (str): URL of a downloadable resource.
        timeout (int): Maximum request time in seconds.

    Returns:
        dict: Download speed measurement results.
    """

    try:
        start_time = time.perf_counter()

        response = requests.get(
            url,
            stream=True,
            timeout=timeout
        )

        response.raise_for_status()

        total_bytes = 0

        for chunk in response.iter_content(
            chunk_size=64 * 1024
        ):
            if chunk:
                total_bytes += len(chunk)

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        if elapsed_time <= 0:
            return {
                "status": "Failed",
                "speed_mbps": None,
                "bytes_received": total_bytes
            }

        speed_mbps = (
            total_bytes * 8
        ) / (
            elapsed_time * 1_000_000
        )

        return {
            "status": "Success",
            "speed_mbps": round(speed_mbps, 2),
            "bytes_received": total_bytes,
            "duration_seconds": round(elapsed_time, 2)
        }

    except requests.RequestException as error:
        return {
            "status": f"Error: {error}",
            "speed_mbps": None,
            "bytes_received": 0
        }


def measure_upload_speed(
    url,
    data_size_mb=1,
    timeout=30
):
    """
    Measure approximate upload speed using an HTTP POST request.

    Args:
        url (str): Server endpoint accepting POST data.
        data_size_mb (int): Amount of test data in MB.
        timeout (int): Maximum request time in seconds.

    Returns:
        dict: Upload speed measurement results.
    """

    try:
        data_size_bytes = data_size_mb * 1024 * 1024

        test_data = b"0" * data_size_bytes

        start_time = time.perf_counter()

        response = requests.post(
            url,
            data=test_data,
            timeout=timeout
        )

        response.raise_for_status()

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        if elapsed_time <= 0:
            return {
                "status": "Failed",
                "speed_mbps": None,
                "bytes_sent": data_size_bytes
            }

        speed_mbps = (
            data_size_bytes * 8
        ) / (
            elapsed_time * 1_000_000
        )

        return {
            "status": "Success",
            "speed_mbps": round(speed_mbps, 2),
            "bytes_sent": data_size_bytes,
            "duration_seconds": round(elapsed_time, 2)
        }

    except requests.RequestException as error:
        return {
            "status": f"Error: {error}",
            "speed_mbps": None,
            "bytes_sent": data_size_bytes
        }


def calculate_bandwidth_mbps(
    total_bytes,
    duration_seconds
):
    """
    Calculate bandwidth in Mbps.

    Args:
        total_bytes (int): Number of bytes transferred.
        duration_seconds (float): Transfer duration.

    Returns:
        float: Bandwidth in Mbps.
    """

    if duration_seconds <= 0:
        return None

    speed_mbps = (
        total_bytes * 8
    ) / (
        duration_seconds * 1_000_000
    )

    return round(speed_mbps, 2)