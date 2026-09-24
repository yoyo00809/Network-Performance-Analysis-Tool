# ==========================================
# Network Performance Analysis Tool (NPAT)
# Database Tests
# ==========================================

import json

from app.database.database import (
    db,
    NetworkTest,
    create_database,
    save_network_test,
    get_test_history,
)


def test_database_initialization():

    app = create_database()

    assert app is not None

    with app.app_context():

        result = db.session.execute(
            db.text(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' "
                "AND name='network_test'"
            )
        ).fetchone()

        assert result is not None


def test_save_network_test():

    app = create_database()

    metrics = {
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss": 0.0,
        "latency_average": 35.5,
        "latency_minimum": 30.0,
        "latency_maximum": 42.0,
        "jitter": 6.0,
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Good",
    }

    with app.app_context():

        test = save_network_test(
            "127.0.0.1",
            metrics,
            analysis
        )

        assert test.id is not None
        assert test.host == "127.0.0.1"
        assert test.packets_sent == 4
        assert test.packets_received == 4
        assert test.packet_loss == 0.0
        assert test.latency_average == 35.5
        assert test.jitter == 6.0
        assert test.overall_status == "Good"

        # Clean up test record
        db.session.delete(test)
        db.session.commit()


def test_get_test_history():

    app = create_database()

    metrics = {
        "packets_sent": 4,
        "packets_received": 3,
        "packet_loss": 25.0,
        "latency_average": 80.0,
        "latency_minimum": 70.0,
        "latency_maximum": 95.0,
        "jitter": 12.0,
    }

    analysis = {
        "latency_status": "Average",
        "jitter_status": "Good",
        "packet_loss_status": "Poor",
        "overall_status": "Poor",
    }

    with app.app_context():

        test = save_network_test(
            "test.example",
            metrics,
            analysis
        )

        history = get_test_history(
            limit=10
        )

        assert isinstance(history, list)
        assert len(history) >= 1

        matching_records = [
            record
            for record in history
            if record.host == "test.example"
        ]

        assert len(matching_records) >= 1

        # Clean up test record
        db.session.delete(test)
        db.session.commit()


def test_save_network_test_with_health_score():

    app = create_database()

    metrics = {
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss": 0.0,
        "latency_average": 30.0,
        "latency_minimum": 28.0,
        "latency_maximum": 34.0,
        "jitter": 5.0,
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Good",
    }

    health_score = {
        "health_score": 93.0,
        "health_status": "Excellent",
        "latency_score": 90,
        "jitter_score": 100,
        "packet_loss_score": 100,
    }

    with app.app_context():

        test = save_network_test(
            "health-test.example",
            metrics,
            analysis,
            health_score
        )

        assert test.id is not None
        assert test.host == "health-test.example"

        assert test.health_score == 93.0
        assert test.health_status == "Excellent"
        assert test.latency_score == 90
        assert test.jitter_score == 100
        assert test.packet_loss_score == 100

        # Clean up test record
        db.session.delete(test)
        db.session.commit()


# ------------------------------------------
# Anomaly Detection Database Test
# ------------------------------------------

def test_save_network_test_with_anomaly():

    app = create_database()

    metrics = {
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss": 0.0,
        "latency_average": 80.0,
        "latency_minimum": 20.0,
        "latency_maximum": 180.0,
        "jitter": 65.0,
    }

    analysis = {
        "latency_status": "Average",
        "jitter_status": "Poor",
        "packet_loss_status": "Good",
        "overall_status": "Poor",
    }

    anomaly = {
        "anomaly_detected": True,
        "anomaly_count": 2,
        "anomaly_types": [
            "Latency Spike",
            "High Jitter",
        ],
        "severity": "Critical",
        "details": [
            "Unusual latency spike detected: [180.0]",
            "High jitter detected: 65.0 ms",
        ],
    }

    with app.app_context():

        test = save_network_test(
            "anomaly-test.example",
            metrics,
            analysis,
            anomaly=anomaly
        )

        assert test.id is not None
        assert test.host == "anomaly-test.example"

        # ----------------------------------
        # Basic anomaly fields
        # ----------------------------------

        assert test.anomaly_detected is True
        assert test.anomaly_count == 2
        assert test.anomaly_severity == "Critical"

        # ----------------------------------
        # JSON anomaly types
        # ----------------------------------

        saved_types = json.loads(
            test.anomaly_types
        )

        assert saved_types == [
            "Latency Spike",
            "High Jitter",
        ]

        # ----------------------------------
        # JSON anomaly details
        # ----------------------------------

        saved_details = json.loads(
            test.anomaly_details
        )

        assert saved_details == [
            "Unusual latency spike detected: [180.0]",
            "High jitter detected: 65.0 ms",
        ]

        # Clean up test record
        db.session.delete(test)
        db.session.commit()


# ==========================================
# Failure & Recovery Database Tests
# ==========================================

def test_save_network_test_with_failure_recovery():

    app = create_database()

    metrics = {
        "packets_sent": 4,
        "packets_received": 0,
        "packet_loss": 100.0,
        "latency_average": None,
        "latency_minimum": None,
        "latency_maximum": None,
        "jitter": None,
    }

    analysis = {
        "latency_status": "Unavailable",
        "jitter_status": "Unavailable",
        "packet_loss_status": "Poor",
        "overall_status": "Poor",
    }

    failure_recovery = {
        "state": "Unavailable",
        "failure_detected": True,
        "recovery_detected": False,
        "failure_count": 1,
        "failure_duration_seconds": None,
    }

    with app.app_context():

        test = save_network_test(
            "failure-test.example",
            metrics,
            analysis,
            failure_recovery=failure_recovery
        )

        assert test.id is not None
        assert test.host == "failure-test.example"

        assert test.network_state == "Unavailable"
        assert test.failure_detected is True
        assert test.recovery_detected is False
        assert test.failure_count == 1
        assert test.failure_duration_seconds is None

        # Clean up test record
        db.session.delete(test)
        db.session.commit()


def test_save_network_test_with_recovery():

    app = create_database()

    metrics = {
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss": 0.0,
        "latency_average": 30.0,
        "latency_minimum": 28.0,
        "latency_maximum": 34.0,
        "jitter": 4.0,
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Good",
    }

    failure_recovery = {
        "state": "Available",
        "failure_detected": False,
        "recovery_detected": True,
        "failure_count": 0,
        "failure_duration_seconds": 15.0,
    }

    with app.app_context():

        test = save_network_test(
            "recovery-test.example",
            metrics,
            analysis,
            failure_recovery=failure_recovery
        )

        assert test.id is not None
        assert test.host == "recovery-test.example"

        assert test.network_state == "Available"
        assert test.failure_detected is False
        assert test.recovery_detected is True
        assert test.failure_count == 0
        assert test.failure_duration_seconds == 15.0

        # Clean up test record
        db.session.delete(test)
        db.session.commit()


def test_save_network_test_with_failure_recovery_defaults():

    app = create_database()

    metrics = {
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss": 0.0,
        "latency_average": 25.0,
        "latency_minimum": 20.0,
        "latency_maximum": 30.0,
        "jitter": 3.0,
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Good",
    }

    with app.app_context():

        test = save_network_test(
            "default-test.example",
            metrics,
            analysis
        )

        assert test.id is not None

        assert test.network_state is None
        assert test.failure_detected is None
        assert test.recovery_detected is None
        assert test.failure_count is None
        assert test.failure_duration_seconds is None

        # Clean up test record
        db.session.delete(test)
        db.session.commit()
    
    
# ==========================================
# Bandwidth Database Tests
# ==========================================

def test_save_network_test_with_bandwidth():

    app = create_database()

    metrics = {
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss": 0.0,
        "latency_average": 25.0,
        "latency_minimum": 20.0,
        "latency_maximum": 30.0,
        "jitter": 3.0,
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Good",
    }

    bandwidth = {
        "download_speed_mbps": 120.75,
        "upload_speed_mbps": 60.50,
    }

    with app.app_context():

        test = save_network_test(
            "bandwidth-test.example",
            metrics,
            analysis,
            bandwidth=bandwidth
        )

        assert test.id is not None
        assert test.host == "bandwidth-test.example"

        assert test.download_speed_mbps == 120.75
        assert test.upload_speed_mbps == 60.50

        # Clean up test record
        db.session.delete(test)
        db.session.commit()


def test_get_test_history_with_bandwidth():

    app = create_database()

    metrics = {
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss": 0.0,
        "latency_average": 30.0,
        "latency_minimum": 25.0,
        "latency_maximum": 35.0,
        "jitter": 4.0,
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Good",
    }

    bandwidth = {
        "download_speed_mbps": 100.25,
        "upload_speed_mbps": 50.75,
    }

    with app.app_context():

        test = save_network_test(
            "bandwidth-history.example",
            metrics,
            analysis,
            bandwidth=bandwidth
        )

        history = get_test_history(
            limit=10
        )

        matching_records = [
            record
            for record in history
            if record.host == "bandwidth-history.example"
        ]

        assert len(matching_records) >= 1

        record = matching_records[0]

        assert record.download_speed_mbps == 100.25
        assert record.upload_speed_mbps == 50.75

        # Clean up test record
        db.session.delete(test)
        db.session.commit()