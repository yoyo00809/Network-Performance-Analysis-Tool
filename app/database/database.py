# ==========================================
# Network Performance Analysis Tool (NPAT)
# Database Module
# ==========================================

from datetime import datetime

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
    analysis
):
    """
    Save a network performance test result
    to the database.

    Args:
        host (str): IP address or hostname.
        metrics (dict): Calculated metrics.
        analysis (dict): Performance analysis.

    Returns:
        NetworkTest: Saved database record.
    """

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