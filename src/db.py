import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    database_url = os.getenv("DIRECT_URL")

    if not database_url:
        raise ValueError("DIRECT_URL is not set in .env")

    return psycopg2.connect(database_url)


def save_health_check(connection, tool_id, result):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO health_checks (
            ai_tool_id,
            status,
            status_code,
            response_time_ms,
            error_type,
            error_message,
            redirect_url,
            redirected,
            timeout
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        tool_id,
        result["status"],
        result["status_code"],
        result["response_time_ms"],
        result["error_type"],
        result["error_message"],
        result["redirect_url"],
        result["redirected"],
        result["timeout"],
    ))

    cursor.close()


def save_monitoring_failure(connection, tool_id, error):
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO health_checks (
            ai_tool_id,
            status,
            status_code,
            response_time_ms,
            error_type,
            error_message,
            redirected,
            timeout
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        tool_id,
        "down",
        None,
        None,
        type(error).__name__,
        str(error),
        False,
        False,
    ))

    cursor.close()