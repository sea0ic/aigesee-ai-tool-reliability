from db import get_connection, save_health_check
from monitor import check_website


try:
    connection = get_connection()
    cursor = connection.cursor()

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

        result = check_website(website_url)

        print(f"Status: {result['status']}")
        print(f"HTTP status code: {result['status_code']}")
        print(f"Response time: {result['response_time_ms']} ms")
        print(f"Redirected: {result['redirected']}")

        if result["error_type"]:
            print(f"Error type: {result['error_type']}")

        save_health_check(connection, tool_id, result)

    connection.commit()

    cursor.close()
    connection.close()

    print("\nHealth check results saved to database.")


except Exception as error:
    print("Monitoring run failed.")
    print(f"Error: {error}")