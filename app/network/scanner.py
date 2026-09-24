# ==========================================
# Network Performance Analysis Tool (NPAT)
# Network Scanner Module
# ==========================================

import concurrent.futures
import ipaddress
import platform
import subprocess

from app.config.settings import PING_TIMEOUT


def get_local_network():
    """
    Get the local network range.

    Currently uses the common private network
    range detected from the Windows IP configuration.
    """

    try:
        result = subprocess.run(
            ["ipconfig"],
            capture_output=True,
            text=True,
            timeout=PING_TIMEOUT
        )

        output = result.stdout

        for line in output.splitlines():

            if "IPv4 Address" in line:

                ip_address = line.split(":")[-1].strip()

                # Ignore invalid addresses
                try:

                    ip = ipaddress.ip_address(
                        ip_address
                    )

                    if ip.is_private:

                        network = ipaddress.ip_network(
                            f"{ip_address}/24",
                            strict=False
                        )

                        return network

                except ValueError:
                    continue

    except Exception:
        pass

    return None


def ping_device(ip_address):
    """
    Check whether a device responds to a ping request.

    Args:
        ip_address (str): IP address of the device.

    Returns:
        bool: True if device responds, otherwise False.
    """

    system = platform.system().lower()

    if system == "windows":

        command = [
            "ping",
            "-n",
            "1",
            "-w",
            "1000",
            str(ip_address)
        ]

    else:

        command = [
            "ping",
            "-c",
            "1",
            "-W",
            "1",
            str(ip_address)
        ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=3
        )

        return result.returncode == 0

    except Exception:

        return False


def scan_network(
    network=None,
    max_workers=32
):
    """
    Scan a network range and identify reachable devices.

    Multiple hosts are scanned concurrently to reduce
    the time required for larger networks.

    Args:
        network: IPv4 network object.
        max_workers (int): Maximum number of concurrent
            ping operations.

    Returns:
        list: List of reachable IP addresses.
    """

    if network is None:

        network = get_local_network()

    if network is None:

        return []

    ip_addresses = list(
        network.hosts()
    )

    active_devices = []

    # --------------------------------------
    # Concurrent Network Scan
    # --------------------------------------

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        results = executor.map(
            ping_device,
            ip_addresses
        )

        for ip_address, is_active in zip(
            ip_addresses,
            results
        ):

            if is_active:

                active_devices.append(
                    str(ip_address)
                )

    return active_devices