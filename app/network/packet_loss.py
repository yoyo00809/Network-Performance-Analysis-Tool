# ==========================================
# Network Performance Analysis Tool (NPAT)
# Packet Loss Measurement Module
# ==========================================

from app.network.ping import ping_host


def measure_packet_loss(host, count=10):
    """
    Measure packet loss for a specified host.

    Args:
        host (str): IP address or hostname.
        count (int): Number of ping requests.

    Returns:
        dict: Packet loss measurement results.
    """

    result = ping_host(
        host,
        count=count
    )

    packets_sent = result["packets_sent"]
    packets_received = result["packets_received"]

    if packets_sent <= 0:
        packet_loss = None
    else:
        lost_packets = packets_sent - packets_received

        packet_loss = round(
            (lost_packets / packets_sent) * 100,
            2
        )

    return {
        "host": host,
        "packets_sent": packets_sent,
        "packets_received": packets_received,
        "packets_lost": packets_sent - packets_received,
        "packet_loss": packet_loss,
        "status": result["status"]
    }