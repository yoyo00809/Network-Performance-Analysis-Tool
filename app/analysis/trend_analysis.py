# ==========================================
# Network Performance Analysis Tool (NPAT)
# Historical Trend Analysis
# ==========================================


def calculate_trend(values):
    """
    Calculate basic statistics for historical values.

    Returns:
        dict: Average, minimum, maximum and count.
    """

    valid_values = [
        float(value)
        for value in values
        if value is not None
    ]

    if not valid_values:
        return {
            "average": None,
            "minimum": None,
            "maximum": None,
            "count": 0,
        }

    return {
        "average": round(
            sum(valid_values) / len(valid_values),
            2
        ),
        "minimum": round(
            min(valid_values),
            2
        ),
        "maximum": round(
            max(valid_values),
            2
        ),
        "count": len(valid_values),
    }


def analyze_historical_tests(records):
    """
    Analyze historical NetworkTest records.

    Args:
        records (list): NetworkTest database records.

    Returns:
        dict: Historical trend analysis.
    """

    if records is None:
        records = []

    latency_values = [
        record.latency_average
        for record in records
        if record.latency_average is not None
    ]

    jitter_values = [
        record.jitter
        for record in records
        if record.jitter is not None
    ]

    packet_loss_values = [
        record.packet_loss
        for record in records
        if record.packet_loss is not None
    ]

    health_score_values = [
        record.health_score
        for record in records
        if record.health_score is not None
    ]

    download_speed_values = [
        getattr(
            record,
            "download_speed_mbps",
            None
        )
        for record in records
        if getattr(
            record,
            "download_speed_mbps",
            None
        ) is not None
    ]

    upload_speed_values = [
        getattr(
            record,
            "upload_speed_mbps",
            None
        )
        for record in records
        if getattr(
            record,
            "upload_speed_mbps",
            None
        ) is not None
    ]

    available_count = sum(
        1
        for record in records
        if record.network_state == "Available"
    )

    unavailable_count = sum(
        1
        for record in records
        if record.network_state == "Unavailable"
    )

    failure_events = sum(
        1
        for record in records
        if record.failure_detected is True
    )

    recovery_events = sum(
        1
        for record in records
        if record.recovery_detected is True
    )

    return {
        "total_tests": len(records),

        "latency": calculate_trend(
            latency_values
        ),

        "jitter": calculate_trend(
            jitter_values
        ),

        "packet_loss": calculate_trend(
            packet_loss_values
        ),

        "health_score": calculate_trend(
            health_score_values
        ),

        "download_speed": calculate_trend(
            download_speed_values
        ),

        "upload_speed": calculate_trend(
            upload_speed_values
        ),

        "availability": {
            "available": available_count,
            "unavailable": unavailable_count,
        },

        "failure_events": failure_events,

        "recovery_events": recovery_events,
    }


def get_metric_series(records):
    """
    Extract historical metric series for charts.

    Returns:
        dict: Ordered metric series.
    """

    return {
        "latency": [
            record.latency_average
            for record in records
        ],

        "jitter": [
            record.jitter
            for record in records
        ],

        "packet_loss": [
            record.packet_loss
            for record in records
        ],

        "health_score": [
            record.health_score
            for record in records
        ],

        "download_speed": [
            getattr(
                record,
                "download_speed_mbps",
                None
            )
            for record in records
        ],

        "upload_speed": [
            getattr(
                record,
                "upload_speed_mbps",
                None
            )
            for record in records
        ],
    }