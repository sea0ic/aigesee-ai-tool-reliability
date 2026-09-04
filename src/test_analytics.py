from db import get_connection
from analytics import get_reliability_summary


try:
    connection = get_connection()

    summary = get_reliability_summary(connection)

    print("\nReliability Summary")
    print("===================")

    for tool in summary:
        print(f"\n{tool['name']}")
        print(f"  Category: {tool['category']}")
        print(f"  Checks: {tool['total_checks']}")
        print(f"  Successful: {tool['successful_checks']}")
        print(f"  Failed: {tool['failed_checks']}")
        print(f"  Uptime: {tool['uptime_percentage']}%")
        print(f"  Avg response time: {tool['average_response_time_ms']} ms")

    connection.close()

except Exception as error:
    print("Analytics test failed.")
    print(f"Error: {error}")