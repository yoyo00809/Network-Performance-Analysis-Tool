# ==========================================
# Network Performance Analysis Tool (NPAT)
# Database Tests
# ==========================================

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