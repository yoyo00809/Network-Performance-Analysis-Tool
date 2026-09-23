# ==========================================
# Network Performance Analysis Tool (NPAT)
# Traceroute Module
# ==========================================

import platform
import re
import subprocess

from app.config.settings import PING_TIMEOUT


def traceroute_host(host, max_hops=15):
    """
    Trace the network path from the local computer
    to the specified destination.

    Args:
        host (str): IP address or hostname.
        max_hops (int): Maximum number of network hops.

    Returns:
        dict: Traceroute information.
    """

    system = platform.system().lower()

    if system == "windows":
        command = [
            "tracert",
            "-h",
            str(max_hops),
            host
        ]
    else:
        command = [
            "traceroute",
            "-m",
            str(max_hops),
            host
        ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=PING_TIMEOUT
        )

        output = result.stdout

        hops = parse_traceroute_output(
            output,
            system
        )

        return {
            "host": host,
            "hops": hops,
            "hop_count": len(hops),
            "status": "Success" if hops else "Failed"
        }

    except subprocess.TimeoutExpired:
        return {
            "host": host,
            "hops": [],
            "hop_count": 0,
            "status": "Timeout"
        }

    except FileNotFoundError:
        return {
            "host": host,
            "hops": [],
            "hop_count": 0,
            "status": "Traceroute command not found"
        }

    except Exception as error:
        return {
            "host": host,
            "hops": [],
            "hop_count": 0,
            "status": f"Error: {error}"
        }


def parse_traceroute_output(output, system):
    """
    Parse traceroute/tracert command output.

    Args:
        output (str): Raw command output.
        system (str): Operating system name.

    Returns:
        list: Parsed hop information.
    """

    hops = []

    for line in output.splitlines():

        line = line.strip()

        if not line:
            continue

        # Windows tracert format
        if system == "windows":

            match = re.match(
                r"^\s*(\d+)\s+(.+?)\s+(\d+\.\d+\.\d+\.\d+)",
                line
            )

            if match:
                hop_number = int(match.group(1))
                ip_address = match.group(3)

                hops.append({
                    "hop": hop_number,
                    "ip": ip_address
                })

        # Linux / Unix traceroute format
        else:

            match = re.match(
                r"^\s*(\d+)\s+.*?\(?(\d+\.\d+\.\d+\.\d+)\)?",
                line
            )

            if match:
                hop_number = int(match.group(1))
                ip_address = match.group(2)

                hops.append({
                    "hop": hop_number,
                    "ip": ip_address
                })

    return hops