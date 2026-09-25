from app.database.database import (
    create_database,
    db,
    save_wifi_area_scan,
    get_wifi_area_history,
)


def test_save_wifi_area_scan():

    app = create_database()

    scan_result = {
        "location": "Room A",
        "status": "Success",
        "ssid": "Test_WiFi",
        "bssid": "AA:BB:CC:DD:EE:FF",
        "signal_percent": 85,
        "receive_rate_mbps": 150.0,
        "transmit_rate_mbps": 120.0,
        "channel": 11,
        "radio_type": "802.11n",
        "gateway": "192.168.1.1",
        "gateway_latency_ms": 2.5,
        "gateway_packet_loss_percent": 0.0,
        "download_speed_mbps": 75.5,
        "upload_speed_mbps": 35.2,
    }

    with app.app_context():

        scan = save_wifi_area_scan(
            scan_result
        )

        assert scan.id is not None
        assert scan.location == "Room A"
        assert scan.ssid == "Test_WiFi"
        assert scan.signal_percent == 85
        assert scan.receive_rate_mbps == 150.0
        assert scan.transmit_rate_mbps == 120.0
        assert scan.channel == 11
        assert scan.gateway == "192.168.1.1"
        assert scan.gateway_latency_ms == 2.5
        assert scan.gateway_packet_loss_percent == 0.0
        assert scan.download_speed_mbps == 75.5
        assert scan.upload_speed_mbps == 35.2

        db.session.delete(scan)
        db.session.commit()


def test_get_wifi_area_history():

    app = create_database()

    scan_result = {
        "location": "Room B",
        "status": "Success",
        "ssid": "Test_WiFi",
        "signal_percent": 70,
        "receive_rate_mbps": 100.0,
        "transmit_rate_mbps": 80.0,
        "channel": 6,
        "radio_type": "802.11n",
        "gateway": "192.168.1.1",
        "gateway_latency_ms": 5.0,
        "gateway_packet_loss_percent": 0.0,
        "download_speed_mbps": 40.0,
        "upload_speed_mbps": 20.0,
    }

    with app.app_context():

        scan = save_wifi_area_scan(
            scan_result
        )

        history = get_wifi_area_history(
            limit=10
        )

        assert isinstance(history, list)
        assert any(
            record.id == scan.id
            for record in history
        )

        db.session.delete(scan)
        db.session.commit()


def test_save_wifi_area_scan_with_missing_values():

    app = create_database()

    scan_result = {
        "location": "Room C"
    }

    with app.app_context():

        scan = save_wifi_area_scan(
            scan_result
        )

        assert scan.id is not None
        assert scan.location == "Room C"
        assert scan.ssid is None
        assert scan.signal_percent is None
        assert scan.download_speed_mbps is None
        assert scan.upload_speed_mbps is None

        db.session.delete(scan)
        db.session.commit()
        