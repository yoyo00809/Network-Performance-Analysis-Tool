# ==========================================
# Network Performance Analysis Tool (NPAT)
# Database Module
# ==========================================

from datetime import datetime
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config.settings import DATABASE_NAME


# ------------------------------------------
# Database Object
# ------------------------------------------

db = SQLAlchemy()


# ------------------------------------------
# Network Test Model
# ------------------------------------------

class NetworkTest(db.Model):
    """
    Database model for storing network
    performance test results.
    """

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    host = db.Column(
        db.String(255),
        nullable=False
    )

    packets_sent = db.Column(
        db.Integer,
        nullable=False
    )

    packets_received = db.Column(
        db.Integer,
        nullable=False
    )

    packet_loss = db.Column(
        db.Float,
        nullable=True
    )

    latency_average = db.Column(
        db.Float,
        nullable=True
    )

    latency_minimum = db.Column(
        db.Float,
        nullable=True
    )

    latency_maximum = db.Column(
        db.Float,
        nullable=True
    )

    jitter = db.Column(
        db.Float,
        nullable=True
    )

    latency_status = db.Column(
        db.String(20),
        nullable=True
    )

    jitter_status = db.Column(
        db.String(20),
        nullable=True
    )

    packet_loss_status = db.Column(
        db.String(20),
        nullable=True
    )

    overall_status = db.Column(
        db.String(20),
        nullable=True
    )

    # --------------------------------------
    # Network Health Score
    # --------------------------------------

    health_score = db.Column(
        db.Float,
        nullable=True
    )

    health_status = db.Column(
        db.String(20),
        nullable=True
    )

    latency_score = db.Column(
        db.Float,
        nullable=True
    )

    jitter_score = db.Column(
        db.Float,
        nullable=True
    )

    packet_loss_score = db.Column(
        db.Float,
        nullable=True
    )

    # --------------------------------------
    # Anomaly Detection
    # --------------------------------------

    anomaly_detected = db.Column(
        db.Boolean,
        nullable=True
    )

    anomaly_count = db.Column(
        db.Integer,
        nullable=True
    )

    anomaly_types = db.Column(
        db.Text,
        nullable=True
    )

    anomaly_severity = db.Column(
        db.String(20),
        nullable=True
    )

    anomaly_details = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ------------------------------------------
# Create Database
# ------------------------------------------

def create_database():
    """
    Create the SQLite database and tables.
    """

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{DATABASE_NAME}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


# ------------------------------------------
# Save Network Test
# ------------------------------------------

def save_network_test(
    host,
    metrics,
    analysis,
    health_score=None,
    anomaly=None
):
    """
    Save a network performance test result
    to the database.

    Args:
        host (str): IP address or hostname.
        metrics (dict): Calculated metrics.
        analysis (dict): Performance analysis.
        health_score (dict): Network health score data.
        anomaly (dict): Anomaly detection result.

    Returns:
        NetworkTest: Saved database record.
    """

    if health_score is None:
        health_score = {}

    if anomaly is None:
        anomaly = {}

    anomaly_types = anomaly.get(
        "anomaly_types",
        []
    )

    anomaly_details = anomaly.get(
        "details",
        []
    )

    test = NetworkTest(
        host=host,

        packets_sent=metrics.get(
            "packets_sent"
        ),

        packets_received=metrics.get(
            "packets_received"
        ),

        packet_loss=metrics.get(
            "packet_loss"
        ),

        latency_average=metrics.get(
            "latency_average"
        ),

        latency_minimum=metrics.get(
            "latency_minimum"
        ),

        latency_maximum=metrics.get(
            "latency_maximum"
        ),

        jitter=metrics.get(
            "jitter"
        ),

        latency_status=analysis.get(
            "latency_status"
        ),

        jitter_status=analysis.get(
            "jitter_status"
        ),

        packet_loss_status=analysis.get(
            "packet_loss_status"
        ),

        overall_status=analysis.get(
            "overall_status"
        ),

        # ----------------------------------
        # Health Score
        # ----------------------------------

        health_score=health_score.get(
            "health_score"
        ),

        health_status=health_score.get(
            "health_status"
        ),

        latency_score=health_score.get(
            "latency_score"
        ),

        jitter_score=health_score.get(
            "jitter_score"
        ),

        packet_loss_score=health_score.get(
            "packet_loss_score"
        ),

        # ----------------------------------
        # Anomaly Detection
        # ----------------------------------

        anomaly_detected=anomaly.get(
            "anomaly_detected"
        ),

        anomaly_count=anomaly.get(
            "anomaly_count"
        ),

        anomaly_types=json.dumps(
            anomaly_types
        ),

        anomaly_severity=anomaly.get(
            "severity"
        ),

        anomaly_details=json.dumps(
            anomaly_details
        )
    )

    db.session.add(test)
    db.session.commit()

    return test


# ------------------------------------------
# Get Test History
# ------------------------------------------

def get_test_history(limit=50):
    """
    Retrieve recent network test results.

    Args:
        limit (int): Maximum number of records.

    Returns:
        list: NetworkTest records.
    """

    return (
        NetworkTest.query
        .order_by(
            NetworkTest.created_at.desc()
        )
        .limit(limit)
        .all()
    )


# ------------------------------------------
# Database Health Score Test
# ------------------------------------------

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