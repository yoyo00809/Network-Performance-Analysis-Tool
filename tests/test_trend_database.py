# ==========================================
# Network Performance Analysis Tool (NPAT)
# Historical Trend + Database Integration
# ==========================================

from app.database.database import (
    create_database,
    get_test_history,
)

from app.analysis.trend_analysis import (
    analyze_historical_tests,
    get_metric_series,
)


def test_trend_analysis_with_database_history():

    app = create_database()

    with app.app_context():

        records = get_test_history(
            limit=20
        )

        result = analyze_historical_tests(
            records
        )

        assert isinstance(
            result,
            dict
        )

        assert "total_tests" in result
        assert "latency" in result
        assert "jitter" in result
        assert "packet_loss" in result
        assert "health_score" in result
        assert "download_speed" in result
        assert "upload_speed" in result
        assert "availability" in result
        assert "failure_events" in result
        assert "recovery_events" in result

        assert (
            result["total_tests"]
            == len(records)
        )


def test_metric_series_with_database_history():

    app = create_database()

    with app.app_context():

        records = get_test_history(
            limit=20
        )

        series = get_metric_series(
            records
        )

        assert isinstance(
            series,
            dict
        )

        assert "latency" in series
        assert "jitter" in series
        assert "packet_loss" in series
        assert "health_score" in series
        assert "download_speed" in series
        assert "upload_speed" in series

        assert (
            len(series["latency"])
            == len(records)
        )

        assert (
            len(series["jitter"])
            == len(records)
        )

        assert (
            len(series["packet_loss"])
            == len(records)
        )

        assert (
            len(series["health_score"])
            == len(records)
        )
        
        assert (
            len(series["download_speed"])
            == len(records)
        )

        assert (
            len(series["upload_speed"])
            == len(records)
        )