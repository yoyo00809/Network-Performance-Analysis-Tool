# ==========================================
# Network Performance Analysis Tool (NPAT)
# Network Monitoring Module
# ==========================================

from app.network.ping import ping_host
from app.analysis.metrics import calculate_metrics
from app.analysis.analyzer import analyze_performance
from app.analysis.recommendations import generate_recommendations

from app.database.database import (
    create_database,
    save_network_test,
)


def monitor_once(host, count=4):
    """
    Perform one complete network monitoring cycle.

    The cycle collects ping data, calculates metrics,
    analyzes performance, generates recommendations,
    and stores the result in the database.

    Args:
        host (str): IP address or hostname.
        count (int): Number of ping requests.

    Returns:
        dict: Complete monitoring result.
    """

    # --------------------------------------
    # Step 1: Collect raw ping data
    # --------------------------------------

    ping_result = ping_host(
        host,
        count=count
    )

    # --------------------------------------
    # Step 2: Calculate metrics
    # --------------------------------------

    metrics = calculate_metrics(
        ping_result["response_times"],
        ping_result["packets_sent"]
    )

    # --------------------------------------
    # Step 3: Analyze performance
    # --------------------------------------

    analysis = analyze_performance(
        metrics
    )

    # --------------------------------------
    # Step 4: Generate recommendations
    # --------------------------------------

    recommendations = generate_recommendations(
        metrics,
        analysis
    )

    # --------------------------------------
    # Step 5: Save result to database
    # --------------------------------------

    app = create_database()

    with app.app_context():

        database_record = save_network_test(
            host,
            metrics,
            analysis
        )

        database_id = database_record.id

    # --------------------------------------
    # Return complete monitoring result
    # --------------------------------------

    return {
        "host": host,
        "ping": ping_result,
        "metrics": metrics,
        "analysis": analysis,
        "recommendations": recommendations,
        "database_id": database_id
    }