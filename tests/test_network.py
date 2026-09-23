# ==========================================
# Network Performance Analysis Tool (NPAT)
# Network Tests
# ==========================================

import ipaddress

from app.network.scanner import (
    get_local_network,
    ping_device,
    scan_network,
)

from app.network.traceroute import (
    traceroute_host,
    parse_traceroute_output,
)

from app.network.packet_loss import (
    measure_packet_loss,
)

from app.network.bandwidth import (
    calculate_bandwidth_mbps,
)


# ==========================================
# Scanner Tests
# ==========================================

def test_get_local_network():

    network = get_local_network()

    if network is not None:
        assert network.version == 4
        assert network.is_private


def test_ping_device_localhost():

    result = ping_device(
        "127.0.0.1"
    )

    assert result is True


def test_scan_network_with_custom_network():

    network = ipaddress.ip_network(
        "127.0.0.0/30"
    )

    result = scan_network(
        network
    )

    assert isinstance(
        result,
        list
    )

    assert "127.0.0.1" in result


# ==========================================
# Traceroute Tests
# ==========================================

def test_traceroute_localhost():

    result = traceroute_host(
        "127.0.0.1",
        max_hops=5
    )

    assert result["host"] == "127.0.0.1"

    assert isinstance(
        result["hops"],
        list
    )

    assert isinstance(
        result["hop_count"],
        int
    )

    assert result["status"] in [
        "Success",
        "Failed",
        "Timeout",
        "Traceroute command not found"
    ]


def test_parse_traceroute_output_windows():

    sample_output = """
    Tracing route to google.com
    over a maximum of 5 hops:

      1    2 ms    2 ms    1 ms    192.168.1.1
      2   10 ms    9 ms   11 ms    10.20.30.1

    Trace complete.
    """

    hops = parse_traceroute_output(
        sample_output,
        "windows"
    )

    assert len(hops) == 2

    assert hops[0]["hop"] == 1
    assert hops[0]["ip"] == "192.168.1.1"

    assert hops[1]["hop"] == 2
    assert hops[1]["ip"] == "10.20.30.1"


# ==========================================
# Packet Loss Tests
# ==========================================

def test_measure_packet_loss_localhost():

    result = measure_packet_loss(
        "127.0.0.1",
        count=4
    )

    assert result["host"] == "127.0.0.1"
    assert result["packets_sent"] == 4
    assert result["packets_received"] >= 0
    assert result["packets_lost"] >= 0

    assert 0 <= result["packet_loss"] <= 100

    assert result["status"] in [
        "Success",
        "Failed",
        "Timeout"
    ]


def test_measure_packet_loss_calculation():

    packets_sent = 10
    packets_received = 8

    packets_lost = (
        packets_sent -
        packets_received
    )

    packet_loss = round(
        (packets_lost / packets_sent) * 100,
        2
    )

    assert packets_lost == 2
    assert packet_loss == 20.0


# ==========================================
# Bandwidth Tests
# ==========================================

def test_calculate_bandwidth_mbps():

    result = calculate_bandwidth_mbps(
        1_000_000,
        1
    )

    assert result == 8.0


def test_calculate_bandwidth_with_different_duration():

    result = calculate_bandwidth_mbps(
        2_000_000,
        2
    )

    assert result == 8.0


def test_calculate_bandwidth_invalid_duration():

    assert calculate_bandwidth_mbps(
        1_000_000,
        0
    ) is None

    assert calculate_bandwidth_mbps(
        1_000_000,
        -1
    ) is None

# ==========================================
# Report Generator Tests
# ==========================================

from app.reports.report_generator import (
    generate_text_report,
    save_text_report,
)


def test_generate_text_report():

    host = "127.0.0.1"

    ping_result = {
        "packets_sent": 4,
        "packets_received": 4,
        "response_times": [
            1.0,
            2.0,
            1.5,
            2.5
        ],
        "status": "Success",
    }

    metrics = {
        "packets_sent": 4,
        "packets_received": 4,
        "packet_loss": 0.0,
        "latency_average": 1.75,
        "latency_minimum": 1.0,
        "latency_maximum": 2.5,
        "jitter": 0.83,
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Good",
    }

    recommendations = [
        "Network performance is good. "
        "No immediate action is required."
    ]

    report = generate_text_report(
        host,
        ping_result,
        metrics,
        analysis,
        recommendations
    )

    assert isinstance(
        report,
        str
    )

    assert "NETWORK PERFORMANCE ANALYSIS REPORT" in report
    assert "127.0.0.1" in report
    assert "Average Latency" in report
    assert "Packet Loss" in report
    assert "Overall Status" in report
    assert "Good" in report
    assert "RECOMMENDATIONS" in report


def test_save_text_report(tmp_path):

    report = "Test Network Performance Report"

    file_path = tmp_path / "test_report.txt"

    result = save_text_report(
        report,
        str(file_path)
    )

    assert result == str(file_path)

    assert file_path.exists()

    saved_content = file_path.read_text(
        encoding="utf-8"
    )

    assert saved_content == report
    
# ==========================================
# Report Export Tests
# ==========================================

from app.reports.export import (
    export_report_to_csv,
    export_history_to_csv,
)


def test_export_report_to_csv(tmp_path):

    filepath = tmp_path / "network_report.csv"

    host = "127.0.0.1"

    ping_result = {
        "packets_sent": 4,
        "packets_received": 4,
    }

    metrics = {
        "packet_loss": 0.0,
        "latency_average": 2.0,
        "latency_minimum": 1.0,
        "latency_maximum": 3.0,
        "jitter": 0.67,
    }

    analysis = {
        "latency_status": "Good",
        "jitter_status": "Good",
        "packet_loss_status": "Good",
        "overall_status": "Good",
    }

    result = export_report_to_csv(
        str(filepath),
        host,
        ping_result,
        metrics,
        analysis
    )

    assert result == str(filepath)
    assert filepath.exists()

    content = filepath.read_text(
        encoding="utf-8"
    )

    assert "Host" in content
    assert "127.0.0.1" in content
    assert "Average Latency (ms)" in content
    assert "Overall Status" in content
    assert "Good" in content


def test_export_history_to_csv(tmp_path):

    filepath = tmp_path / "history.csv"

    class TestRecord:

        id = 1
        host = "127.0.0.1"
        packets_sent = 4
        packets_received = 4
        packet_loss = 0.0
        latency_average = 2.0
        latency_minimum = 1.0
        latency_maximum = 3.0
        jitter = 0.67
        latency_status = "Good"
        jitter_status = "Good"
        packet_loss_status = "Good"
        overall_status = "Good"
        created_at = "2026-09-23 12:00:00"

    history = [
        TestRecord()
    ]

    result = export_history_to_csv(
        str(filepath),
        history
    )

    assert result == str(filepath)
    assert filepath.exists()

    content = filepath.read_text(
        encoding="utf-8"
    )

    assert "ID" in content
    assert "Host" in content
    assert "127.0.0.1" in content
    assert "Overall Status" in content