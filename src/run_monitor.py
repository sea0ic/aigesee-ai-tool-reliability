from db import get_connection, save_health_check, save_monitoring_failure
from monitor import check_website


def run_monitor():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT id, name, website_url
            FROM ai_tools
            WHERE is_active = TRUE
            ORDER BY id;
        """)

        tools = cursor.fetchall()

        for tool in tools:
            tool_id, name, website_url = tool

            print(f"\nChecking: {name}")
            print(f"URL: {website_url}")

            try:
                result = check_website(website_url)

                print(f"Status: {result['status']}")
                print(f"Reachable: {result['reachable']}")
                print(f"HTTP status code: {result['status_code']}")
                print(f"Response time: {result['response_time_ms']} ms")
                print(f"Redirected: {result['redirected']}")

                if result["error_type"]:
                    print(f"Error type: {result['error_type']}")

                save_health_check(connection, tool_id, result)
                connection.commit()

            except Exception as error:
                print(f"Monitoring failed for {name}.")
                print(f"Error: {error}")

                save_monitoring_failure(connection, tool_id, error)
                connection.commit()

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    try:
        run_monitor()
        print("\nMonitoring run completed.")
    except Exception as error:
        print("Monitoring run failed.")
        print(f"Error: {error}")