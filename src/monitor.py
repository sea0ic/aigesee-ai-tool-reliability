import time

import requests


def check_website(url):
    start_time = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
        )

        end_time = time.perf_counter()

        response_time_ms = (end_time - start_time) * 1000

        return {
            "status": "up",
            "status_code": response.status_code,
            "response_time_ms": round(response_time_ms, 2),
            "error_type": None,
            "error_message": None,
            "redirected": response.url != url,
            "redirect_url": response.url if response.url != url else None,
            "timeout": False,
        }

    except requests.exceptions.Timeout as error:
        return {
            "status": "down",
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
            "status_code": None,
            "response_time_ms": None,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "redirected": False,
            "redirect_url": None,
            "timeout": False,
        }