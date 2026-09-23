from app.network.ping import ping_host


def test_ping_localhost():
    result = ping_host("127.0.0.1", count=2)

    assert result["host"] == "127.0.0.1"
    assert result["packets_sent"] == 2
    assert result["status"] in ["Success", "Failed"]