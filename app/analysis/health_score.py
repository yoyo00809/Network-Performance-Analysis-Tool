def calculate_latency_score(latency):
    """
    Calculate latency score from 0 to 100.

    <= 20 ms   -> 100
    <= 50 ms   -> 90
    <= 100 ms  -> 70
    <= 200 ms  -> 40
    > 200 ms   -> 0
    """
    if latency is None:
        return None

    if latency <= 20:
        return 100
    elif latency <= 50:
        return 90
    elif latency <= 100:
        return 70
    elif latency <= 200:
        return 40
    else:
        return 0


def calculate_jitter_score(jitter):
    """
    Calculate jitter score from 0 to 100.

    <= 5 ms   -> 100
    <= 20 ms  -> 90
    <= 50 ms  -> 70
    <= 100 ms -> 40
    > 100 ms  -> 0
    """
    if jitter is None:
        return None

    if jitter <= 5:
        return 100
    elif jitter <= 20:
        return 90
    elif jitter <= 50:
        return 70
    elif jitter <= 100:
        return 40
    else:
        return 0


def calculate_packet_loss_score(packet_loss):
    """
    Calculate packet loss score from 0 to 100.

    <= 0%  -> 100
    <= 1%  -> 90
    <= 5%  -> 70
    <= 10% -> 40
    > 10%  -> 0
    """
    if packet_loss is None:
        return None

    if packet_loss <= 0:
        return 100
    elif packet_loss <= 1:
        return 90
    elif packet_loss <= 5:
        return 70
    elif packet_loss <= 10:
        return 40
    else:
        return 0


def calculate_health_score(metrics):
    """
    Calculate overall network health score from 0 to 100.

    Weights:
    Latency     = 40%
    Jitter      = 30%
    Packet Loss = 30%
    """

    latency_score = calculate_latency_score(
        metrics.get("latency_average")
    )

    jitter_score = calculate_jitter_score(
        metrics.get("jitter")
    )

    packet_loss_score = calculate_packet_loss_score(
        metrics.get("packet_loss")
    )

    scores = []
    weights = []

    if latency_score is not None:
        scores.append(latency_score)
        weights.append(0.40)

    if jitter_score is not None:
        scores.append(jitter_score)
        weights.append(0.30)

    if packet_loss_score is not None:
        scores.append(packet_loss_score)
        weights.append(0.30)

    if not scores:
        return {
            "health_score": None,
            "health_status": "Unavailable",
            "latency_score": None,
            "jitter_score": None,
            "packet_loss_score": None,
        }

    total_weight = sum(
        weights
    )

    weighted_score = sum(
        score * weight
        for score, weight in zip(scores, weights)
    ) / total_weight

    health_score = round(weighted_score, 2)

    if health_score >= 90:
        health_status = "Excellent"
    elif health_score >= 75:
        health_status = "Good"
    elif health_score >= 50:
        health_status = "Fair"
    else:
        health_status = "Poor"

    return {
        "health_score": health_score,
        "health_status": health_status,
        "latency_score": latency_score,
        "jitter_score": jitter_score,
        "packet_loss_score": packet_loss_score,
    }