# ==========================================
# Network Performance Analysis Tool (NPAT)
# Monitoring Module
# ==========================================


from app.network.ping import ping_host


from app.analysis.metrics import (
    calculate_metrics
)


from app.analysis.analyzer import (
    analyze_performance
)


from app.analysis.recommendations import (
    generate_recommendations
)


from app.analysis.health_score import (
    calculate_health_score
)


from app.analysis.anomaly_detector import (
    detect_anomalies
)


from app.database.database import (
    create_database,
    save_network_test
)


from app.monitoring.failure_recovery import (
    NetworkFailureRecoveryTracker,
    process_ping_result
)


# ==========================================
# Failure & Recovery Tracker
# ==========================================

_trackers = {}


def get_failure_recovery_tracker(host):
    """
    Return the persistent failure/recovery tracker
    for a specific host.

    A separate tracker is maintained for each host
    so that availability transitions can be detected
    across repeated monitoring tests.
    """

    if host not in _trackers:

        _trackers[host] = (
            NetworkFailureRecoveryTracker()
        )

    return _trackers[host]


def reset_failure_recovery_tracker(host=None):
    """
    Reset failure/recovery tracking.

    If host is provided, only that host is reset.

    If host is None, all trackers are reset.
    """

    if host is None:

        _trackers.clear()

    elif host in _trackers:

        _trackers[host].reset()


def monitor_once(
    host,
    count=4
):
    """
    Perform one complete network monitoring test.

    Flow:

    Host
      ↓
    Ping
      ↓
    Metrics
      ↓
    Performance Analysis
      ↓
    Health Score
      ↓
    Anomaly Detection
      ↓
    Failure & Recovery Detection
      ↓
    Recommendations
      ↓
    Database
    """

    # --------------------------------------
    # Create database
    # --------------------------------------

    app = create_database()


    # --------------------------------------
    # Ping target
    # --------------------------------------

    ping_result = ping_host(
        host,
        count=count
    )


    # --------------------------------------
    # Calculate metrics
    # --------------------------------------

    metrics = calculate_metrics(
        ping_result["response_times"],
        ping_result["packets_sent"]
    )


    # --------------------------------------
    # Analyze performance
    # --------------------------------------

    analysis = analyze_performance(
        metrics
    )


    # --------------------------------------
    # Calculate health score
    # --------------------------------------

    health_score = calculate_health_score(
        metrics
    )


    # --------------------------------------
    # Detect anomalies
    # --------------------------------------

    anomaly_result = detect_anomalies(
        metrics,
        ping_result.get(
            "response_times",
            []
        )
    )


    # --------------------------------------
    # Failure & Recovery Detection
    # --------------------------------------

    failure_recovery_tracker = (
        get_failure_recovery_tracker(host)
    )

    failure_recovery = process_ping_result(
        failure_recovery_tracker,
        ping_result
    )


    # --------------------------------------
    # Generate recommendations
    # --------------------------------------

    recommendations = generate_recommendations(
        metrics,
        analysis
    )


    # --------------------------------------
    # Save result to database
    # --------------------------------------

    with app.app_context():

        database_record = save_network_test(
            host,
            metrics,
            analysis,
            health_score,
            anomaly_result,
            failure_recovery
        )

        database_id = database_record.id


    # --------------------------------------
    # Return complete result
    # --------------------------------------

    return {
        "host": host,

        "ping": ping_result,

        "metrics": metrics,

        "analysis": analysis,

        "health_score": health_score,

        "anomaly": anomaly_result,

        "failure_recovery": failure_recovery,

        "recommendations": recommendations,

        "database_id": database_id
    }