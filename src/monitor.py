import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()


USER_AGENT = os.getenv(
    "MONITOR_USER_AGENT",
    "AigeseeAI-Monitor/1.0",
)

REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml",
}


def check_website(url):
    start_time = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers=REQUEST_HEADERS,
        )

        end_time = time.perf_counter()

        response_time_ms = (end_time - start_time) * 1000

        if 200 <= response.status_code < 400:
            status = "up"
            error_type = None
        elif 400 <= response.status_code < 500:
            status = "down"
            error_type = "http_client_error"
        else:
            status = "down"
            error_type = "http_server_error"

        return {
            "status": status,
            "reachable": True,
            "status_code": response.status_code,
            "response_time_ms": round(response_time_ms, 2),
            "error_type": error_type,
            "error_message": None,
            "redirected": response.url != url,
            "redirect_url": response.url if response.url != url else None,
            "timeout": False,
        }

    except requests.exceptions.Timeout as error:
        return {
            "status": "down",
            "reachable": False,
            "status_code": None,
            "response_time_ms": None,
            "error_type": "timeout",
            "error_message": str(error),
            "redirected": False,
            "redirect_url": None,
            "timeout": True,
        }

    except requests.exceptions.RequestException as error:
        return {
            "status": "down",
            "reachable": False,
            "status_code": None,
            "response_time_ms": None,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "redirected": False,
            "redirect_url": None,
            "timeout": False,
        }