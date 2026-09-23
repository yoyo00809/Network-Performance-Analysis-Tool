# ==========================================
# Network Performance Analysis Tool (NPAT)
# Metrics Calculation Module
# ==========================================


def calculate_average(values):
    """
    Calculate the arithmetic mean of a list of values.
    """

    if not values:
        return None

    return round(sum(values) / len(values), 2)


def calculate_minimum(values):
    """
    Calculate the minimum value from a list.
    """

    if not values:
        return None

    return round(min(values), 2)


def calculate_maximum(values):
    """
    Calculate the maximum value from a list.
    """

    if not values:
        return None

    return round(max(values), 2)


def calculate_jitter(response_times):
    """
    Calculate jitter as the average absolute difference
    between consecutive response times.
    """

    if len(response_times) < 2:
        return None

    differences = []

    for i in range(1, len(response_times)):
        difference = abs(
            response_times[i] - response_times[i - 1]
        )

        differences.append(difference)

    return round(
        sum(differences) / len(differences),
        2
    )


def calculate_packet_loss(packets_sent, packets_received):
    """
    Calculate packet loss percentage.
    """

    if packets_sent <= 0:
        return None

    lost_packets = packets_sent - packets_received

    packet_loss = (
        lost_packets / packets_sent
    ) * 100

    return round(packet_loss, 2)


def calculate_metrics(response_times, packets_sent):
    """
    Calculate all network performance metrics
    from raw ping response data.

    Args:
        response_times (list): Individual ping response times.
        packets_sent (int): Number of packets sent.

    Returns:
        dict: Calculated network performance metrics.
    """

    packets_received = len(response_times)

    return {
        "packets_sent": packets_sent,
        "packets_received": packets_received,
        "packet_loss": calculate_packet_loss(
            packets_sent,
            packets_received
        ),
        "latency_average": calculate_average(
            response_times
        ),
        "latency_minimum": calculate_minimum(
            response_times
        ),
        "latency_maximum": calculate_maximum(
            response_times
        ),
        "jitter": calculate_jitter(
            response_times
        ),
    }