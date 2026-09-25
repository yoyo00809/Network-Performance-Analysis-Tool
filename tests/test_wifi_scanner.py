import app.network.wifi_scanner as wifi_scanner


def test_parse_wifi_interface():
    sample_output = """
    State                   : connected
    SSID                    : TestWiFi
    BSSID                   : AA:BB:CC:DD:EE:FF
    Signal                  : 87%
    Receive rate (Mbps)     : 433
    Transmit rate (Mbps)    : 433
    Channel                 : 36
    Radio type              : 802.11ac
    """

    result = wifi_scanner.parse_wifi_interface(
        sample_output
    )

    assert result["state"] == "connected"
    assert result["ssid"] == "TestWiFi"
    assert result["bssid"] == "AA:BB:CC:DD:EE:FF"
    assert result["signal_percent"] == 87
    assert result["receive_rate_mbps"] == 433.0
    assert result["transmit_rate_mbps"] == 433.0
    assert result["channel"] == 36
    assert result["radio_type"] == "802.11ac"


def test_get_wifi_info(monkeypatch):
    sample_output = """
    State                   : connected
    SSID                    : TestWiFi
    Signal                  : 95%
    Receive rate (Mbps)     : 150
    Transmit rate (Mbps)    : 150
    Channel                 : 11
    Radio type              : 802.11n
    """

    class FakeResult:
        returncode = 0
        stdout = sample_output
        stderr = ""

    monkeypatch.setattr(
        wifi_scanner.subprocess,
        "run",
        lambda *args, **kwargs: FakeResult()
    )

    result = wifi_scanner.get_wifi_info()

    assert result["status"] == "Connected"
    assert result["ssid"] == "TestWiFi"
    assert result["signal_percent"] == 95
    assert result["receive_rate_mbps"] == 150.0
    assert result["transmit_rate_mbps"] == 150.0


def test_measure_gateway_latency(monkeypatch):
    class FakeResult:
        returncode = 0
        stdout = """
        Reply from 192.168.0.1: bytes=32 time=2ms TTL=64
        Reply from 192.168.0.1: bytes=32 time=3ms TTL=64
        Reply from 192.168.0.1: bytes=32 time=2ms TTL=64
        Reply from 192.168.0.1: bytes=32 time=3ms TTL=64
        """
        stderr = ""

    monkeypatch.setattr(
        wifi_scanner.subprocess,
        "run",
        lambda *args, **kwargs: FakeResult()
    )

    result = wifi_scanner.measure_gateway_latency(
        "192.168.0.1",
        count=4
    )

    assert result["status"] == "Success"
    assert result["latency_ms"] == 2.5
    assert result["packet_loss_percent"] == 0.0


def test_scan_wifi_area_without_speed(monkeypatch):
    monkeypatch.setattr(
        wifi_scanner,
        "get_wifi_info",
        lambda: {
            "status": "Connected",
            "ssid": "TestWiFi",
            "bssid": "AA:BB:CC:DD:EE:FF",
            "signal_percent": 90,
            "receive_rate_mbps": 300.0,
            "transmit_rate_mbps": 300.0,
            "channel": 36,
            "radio_type": "802.11ac",
        }
    )

    monkeypatch.setattr(
        wifi_scanner,
        "get_default_gateway",
        lambda: "192.168.0.1"
    )

    monkeypatch.setattr(
        wifi_scanner,
        "measure_gateway_latency",
        lambda gateway: {
            "status": "Success",
            "latency_ms": 3.0,
            "packet_loss_percent": 0.0,
        }
    )

    result = wifi_scanner.scan_wifi_area(
        "Bedroom Window",
        measure_speed=False
    )

    assert result["location"] == "Bedroom Window"
    assert result["status"] == "Success"
    assert result["ssid"] == "TestWiFi"
    assert result["signal_percent"] == 90
    assert result["receive_rate_mbps"] == 300.0
    assert result["gateway"] == "192.168.0.1"
    assert result["gateway_latency_ms"] == 3.0
    assert result["gateway_packet_loss_percent"] == 0.0
    assert result["download_speed_mbps"] is None
    assert result["upload_speed_mbps"] is None


def test_scan_wifi_area_not_connected(monkeypatch):
    monkeypatch.setattr(
        wifi_scanner,
        "get_wifi_info",
        lambda: {
            "status": "Not Connected",
            "ssid": None,
            "signal_percent": None,
        }
    )

    result = wifi_scanner.scan_wifi_area(
        "Test Location",
        measure_speed=False
    )

    assert result["location"] == "Test Location"
    assert result["status"] == "Not Connected"
    assert result["gateway"] is None