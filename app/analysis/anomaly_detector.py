# ==========================================
# Network Performance Analysis Tool (NPAT)
# Anomaly Detection
# ==========================================


def _median(values):
    """
    Calculate median without external libraries.
    """

    values = sorted(values)

    if not values:
        return None

    middle = len(values) // 2

    if len(values) % 2 == 0:
        return (
            values[middle - 1] + values[middle]
        ) / 2

    return values[middle]


def detect_latency_anomalies(response_times):
    """
    Detect unusually high latency values.

    The detector uses a median-based threshold for
    small datasets and an IQR threshold when useful.

    This approach works well with NPAT's normal
    4-ping measurement.
    """

    if not response_times:
        return []

    values = [
        float(value)
        for value in response_times
        if value is not None
    ]

    if len(values) < 4:
        return []

    values = sorted(values)

    median_value = _median(values)

    if median_value is None or median_value <= 0:
        return []

    # --------------------------------------
    # Median-based threshold
    # --------------------------------------
    #
    # A value greater than twice the normal
    # median latency is considered a spike.
    #
    # Example:
    #
    # 20, 21, 22, 100
    #
    # median = 21.5
    # threshold = 43
    # 100 > 43 -> anomaly
    #
    median_threshold = median_value * 2

    # --------------------------------------
    # IQR threshold
    # --------------------------------------

    middle = len(values) // 2

    if len(values) % 2 == 0:

        lower_half = values[:middle]
        upper_half = values[middle:]

    else:

        lower_half = values[:middle]
        upper_half = values[middle + 1:]

    q1 = _median(lower_half)
    q3 = _median(upper_half)

    if q1 is not None and q3 is not None:

        iqr = q3 - q1

        iqr_threshold = q3 + (1.5 * iqr)

    else:

        iqr_threshold = float("inf")

    # --------------------------------------
    # Use the more practical threshold
    # --------------------------------------
    #
    # For small ping datasets, the median-based
    # threshold is better at catching sudden spikes.
    #
    upper_limit = min(
        median_threshold,
        iqr_threshold
    )

    anomalies = [
        value
        for value in values
        if value > upper_limit
    ]

    return anomalies


def detect_anomalies(
    metrics,
    response_times=None
):
    """
    Detect unusual network behavior.

    Checks:
    1. Unusual latency spikes
    2. Unusually high jitter
    3. Unusually high packet loss
    """

    if metrics is None:
        metrics = {}

    if response_times is None:
        response_times = []

    # --------------------------------------
    # Latency anomaly
    # --------------------------------------

    latency_anomalies = detect_latency_anomalies(
        response_times
    )

    # --------------------------------------
    # Other metrics
    # --------------------------------------

    jitter = metrics.get("jitter")

    packet_loss = metrics.get(
        "packet_loss"
    )

    anomaly_types = []

    details = []

    # --------------------------------------
    # Latency spike
    # --------------------------------------

    if latency_anomalies:

        anomaly_types.append(
            "Latency Spike"
        )

        details.append(
            "Unusual latency spike detected: "
            f"{latency_anomalies}"
        )

    # --------------------------------------
    # High jitter
    # --------------------------------------

    if (
        jitter is not None
        and jitter > 50
    ):

        anomaly_types.append(
            "High Jitter"
        )

        details.append(
            f"High jitter detected: {jitter} ms"
        )

    # --------------------------------------
    # High packet loss
    # --------------------------------------

    if (
        packet_loss is not None
        and packet_loss > 5
    ):

        anomaly_types.append(
            "High Packet Loss"
        )

        details.append(
            "High packet loss detected: "
            f"{packet_loss}%"
        )

    # --------------------------------------
    # Severity
    # --------------------------------------

    if not anomaly_types:

        severity = "Normal"

    elif len(anomaly_types) == 1:

        severity = "Warning"

    else:

        severity = "Critical"

    # --------------------------------------
    # Final result
    # --------------------------------------

    return {
        "anomaly_detected": bool(
            anomaly_types
        ),
        "anomaly_count": len(
            anomaly_types
        ),
        "anomaly_types": anomaly_types,
        "severity": severity,
        "latency_anomalies": latency_anomalies,
        "details": details,
    }