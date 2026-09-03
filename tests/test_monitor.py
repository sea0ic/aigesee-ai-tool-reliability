from src.monitor import check_website


def test_check_website():
    result = check_website("https://chatgpt.com")

    assert result["status"] == "up"
    assert result["status_code"] == 200
    assert result["response_time_ms"] is not None
    assert result["timeout"] is False