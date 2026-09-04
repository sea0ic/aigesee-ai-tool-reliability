
from analytics import (
    get_reachability_summary,
    get_recent_reliability_summary,
    get_reliability_summary,
)
from db import get_connection


try:
    connection = get_connection()

    historical_summary = get_reliability_summary(connection)

    print("\nHistorical Reliability Summary")
    print("------------------------------")

    for tool in historical_summary:
        print(f"\n{tool['name']}")
        print(f"  Category: {tool['category']}")
        print(f"  Checks: {tool['total_checks']}")
        print(f"  Successful: {tool['successful_checks']}")
        print(f"  Failed: {tool['failed_checks']}")
        print(f"  Uptime: {tool['uptime_percentage']}%")
        print(
            f"  Avg response time: "
            f"{tool['average_response_time_ms']} ms"
        )

    recent_summary = get_recent_reliability_summary(
        connection,
        recent_checks=10,
    )

    print("\n\nRecent Reliability Summary")
    print("--------------------------")

    for tool in recent_summary:
        print(f"\n{tool['name']}")
        print(f"  Category: {tool['category']}")
        print(f"  Recent checks: {tool['recent_checks']}")
        print(f"  Successful: {tool['successful_checks']}")
        print(f"  Failed: {tool['failed_checks']}")
        print(
            f"  Recent uptime: "
            f"{tool['recent_uptime_percentage']}%"
        )
        print(
            f"  Avg response time: "
            f"{tool['average_response_time_ms']} ms"
        )

    reachability_summary = get_reachability_summary(connection)

    print("\n\nReachability Summary")
    print("--------------------")

    for tool in reachability_summary:
        print(f"\n{tool['name']}")
        print(f"  Category: {tool['category']}")
        print(f"  Total checks: {tool['total_checks']}")
        print(f"  Reachable: {tool['reachable_checks']}")
        print(f"  Unreachable: {tool['unreachable_checks']}")
        print(
            f"  Reachability: "
            f"{tool['reachability_percentage']}%"
        )

    connection.close()

except Exception as error:
    print("Analytics test failed.")
    print(f"Error: {error}")
