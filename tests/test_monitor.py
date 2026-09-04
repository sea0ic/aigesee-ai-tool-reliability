from monitor import check_website


def test_healthy_website():
    result = check_website("https://httpbin.org/status/200")

    print("\nHealthy website test:")
    print(result)

    assert result["status"] == "up"
    assert result["status_code"] == 200
    assert result["error_type"] is None
    assert result["timeout"] is False


def test_http_client_error():
    result = check_website("https://httpbin.org/status/404")

    print("\nHTTP client error test:")
    print(result)

    assert result["status"] == "down"
    assert result["status_code"] == 404
    assert result["error_type"] == "http_client_error"
    assert result["timeout"] is False


def test_http_server_error():
    result = check_website("https://httpbin.org/status/500")

    print("\nHTTP server error test:")
    print(result)

    assert result["status"] == "down"
    assert result["status_code"] == 500
    assert result["error_type"] == "http_server_error"
    assert result["timeout"] is False