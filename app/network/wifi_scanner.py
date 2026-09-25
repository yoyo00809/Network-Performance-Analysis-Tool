# ==========================================
# Network Performance Analysis Tool (NPAT)
# Wi-Fi Connectivity Area Scanner
# ==========================================

import re
import subprocess
import platform

from app.network.bandwidth import (
    measure_download_speed,
    measure_upload_speed,
)


# ==========================================
# Parse Wi-Fi Interface Information
# ==========================================

def parse_wifi_interface(output):
    """
    Parse the output of:

        netsh wlan show interfaces

    Returns a dictionary containing the
    currently connected Wi-Fi information.
    """

    result = {
        "state": None,
        "ssid": None,
        "bssid": None,
        "signal_percent": None,
        "receive_rate_mbps": None,
        "transmit_rate_mbps": None,
        "channel": None,
        "radio_type": None,
    }

    for raw_line in output.splitlines():

        line = raw_line.strip()

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if key == "state":
            result["state"] = value

        elif key == "ssid":
            result["ssid"] = value

        elif key == "bssid":
            result["bssid"] = value

        elif key == "signal":

            match = re.search(
                r"(\d+)\s*%",
                value
            )

            if match:
                result["signal_percent"] = int(
                    match.group(1)
                )

        elif key == "receive rate (mbps)":

            try:
                result["receive_rate_mbps"] = float(
                    value
                )
            except ValueError:
                pass

        elif key == "transmit rate (mbps)":

            try:
                result["transmit_rate_mbps"] = float(
                    value
                )
            except ValueError:
                pass

        elif key == "channel":

            try:
                result["channel"] = int(
                    value
                )
            except ValueError:
                pass

        elif key == "radio type":
            result["radio_type"] = value

    return result


# ==========================================
# Get Current Wi-Fi Information
# ==========================================

def get_wifi_info():
    """
    Get information about the currently
    connected Wi-Fi interface.

    Windows uses:

        netsh wlan show interfaces
    """

    if platform.system().lower() != "windows":

        return {
            "status": "Unsupported",
            "message": "Wi-Fi scanner currently supports Windows.",
        }

    try:

        completed = subprocess.run(
            [
                "netsh",
                "wlan",
                "show",
                "interfaces",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=10,
        )

        if completed.returncode != 0:

            return {
                "status": "Failed",
                "message": completed.stderr.strip(),
            }

        wifi_info = parse_wifi_interface(
            completed.stdout
        )

        if not wifi_info["ssid"]:

            return {
                "status": "Not Connected",
                **wifi_info,
            }

        return {
            "status": "Connected",
            **wifi_info,
        }

    except Exception as error:

        return {
            "status": "Failed",
            "message": str(error),
        }


# ==========================================
# Get Default Gateway
# ==========================================

def get_default_gateway():
    """
    Find the default IPv4 gateway on Windows.
    """

    if platform.system().lower() != "windows":
        return None

    try:

        completed = subprocess.run(
            ["ipconfig"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=10,
        )

        for line in completed.stdout.splitlines():

            if "Default Gateway" in line:

                gateway = line.split(":", 1)[-1].strip()

                if gateway:
                    return gateway

    except Exception:
        pass

    return None


# ==========================================
# Gateway Latency
# ==========================================

def measure_gateway_latency(
    gateway,
    count=4
):
    """
    Measure latency to the local Wi-Fi gateway.
    """

    if not gateway:
        return None

    if platform.system().lower() == "windows":

        command = [
            "ping",
            "-n",
            str(count),
            "-w",
            "1000",
            gateway,
        ]

    else:

        command = [
            "ping",
            "-c",
            str(count),
            "-W",
            "1",
            gateway,
        ]

    try:

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=15,
        )

        output = completed.stdout

        times = []

        for match in re.finditer(
            r"time[=<]\s*(\d+(?:\.\d+)?)\s*ms",
            output,
            re.IGNORECASE,
        ):

            times.append(
                float(match.group(1))
            )

        if not times:
            return {
                "status": "Failed",
                "latency_ms": None,
                "packet_loss_percent": 100.0,
            }

        packet_loss = round(
            ((count - len(times)) / count) * 100,
            2,
        )

        return {
            "status": "Success",
            "latency_ms": round(
                sum(times) / len(times),
                2,
            ),
            "packet_loss_percent": packet_loss,
        }

    except Exception:
        return {
            "status": "Failed",
            "latency_ms": None,
            "packet_loss_percent": 100.0,
        }


# ==========================================
# Wi-Fi Area Scan
# ==========================================

def scan_wifi_area(
    location="Current Location",
    measure_speed=True,
):
    """
    Perform a complete Wi-Fi area scan.

    Args:
        location:
            Human-readable location label.

        measure_speed:
            If True, perform download and upload
            bandwidth measurements.

    Returns:
        Dictionary containing Wi-Fi and
        connectivity measurements.
    """

    wifi_info = get_wifi_info()

    result = {
        "location": location,
        "status": wifi_info.get("status"),
        "ssid": wifi_info.get("ssid"),
        "bssid": wifi_info.get("bssid"),
        "signal_percent": wifi_info.get(
            "signal_percent"
        ),
        "receive_rate_mbps": wifi_info.get(
            "receive_rate_mbps"
        ),
        "transmit_rate_mbps": wifi_info.get(
            "transmit_rate_mbps"
        ),
        "channel": wifi_info.get(
            "channel"
        ),
        "radio_type": wifi_info.get(
            "radio_type"
        ),
        "gateway": None,
        "gateway_latency_ms": None,
        "gateway_packet_loss_percent": None,
        "download_speed_mbps": None,
        "upload_speed_mbps": None,
    }

    if wifi_info.get("status") != "Connected":

        result["message"] = wifi_info.get(
            "message",
            "Wi-Fi is not connected.",
        )

        return result

    # --------------------------------------
    # Gateway
    # --------------------------------------

    gateway = get_default_gateway()

    result["gateway"] = gateway

    gateway_result = measure_gateway_latency(
        gateway
    )

    result["gateway_latency_ms"] = (
        gateway_result.get("latency_ms")
    )

    result["gateway_packet_loss_percent"] = (
        gateway_result.get(
            "packet_loss_percent"
        )
    )

    # --------------------------------------
    # Internet Bandwidth
    # --------------------------------------

    if measure_speed:

        try:

            download_result = (
                measure_download_speed()
            )

            if isinstance(
                download_result,
                dict
            ):

                result[
                    "download_speed_mbps"
                ] = download_result.get(
                    "speed_mbps"
                )

        except Exception:
            pass

        try:

            upload_result = (
                measure_upload_speed()
            )

            if isinstance(
                upload_result,
                dict
            ):

                result[
                    "upload_speed_mbps"
                ] = upload_result.get(
                    "speed_mbps"
                )

        except Exception:
            pass

    result["status"] = "Success"

    return result