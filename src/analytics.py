
def get_reliability_summary(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            t.name,
            t.category,
            COUNT(h.id) AS total_checks,
            COUNT(h.id) FILTER (WHERE h.status = 'up') AS successful_checks,
            COUNT(h.id) FILTER (WHERE h.status = 'down') AS failed_checks,
            ROUND(
                COUNT(h.id) FILTER (WHERE h.status = 'up') * 100.0
                / NULLIF(COUNT(h.id), 0),
                2
            ) AS uptime_percentage,
            ROUND(AVG(h.response_time_ms), 2) AS average_response_time_ms
        FROM ai_tools t
        LEFT JOIN health_checks h
            ON t.id = h.ai_tool_id
        WHERE t.is_active = TRUE
        GROUP BY t.id, t.name, t.category
        ORDER BY uptime_percentage DESC;
    """)

    rows = cursor.fetchall()

    cursor.close()

    summary = []

    for row in rows:
        summary.append({
            "name": row[0],
            "category": row[1],
            "total_checks": row[2],
            "successful_checks": row[3],
            "failed_checks": row[4],
            "uptime_percentage": row[5],
            "average_response_time_ms": row[6],
        })

    return summary


def get_recent_reliability_summary(connection, recent_checks=10):
    cursor = connection.cursor()

    cursor.execute("""
        WITH ranked_checks AS (
            SELECT
                h.ai_tool_id,
                h.status,
                h.response_time_ms,
                ROW_NUMBER() OVER (
                    PARTITION BY h.ai_tool_id
                    ORDER BY h.checked_at DESC
                ) AS check_number
            FROM health_checks h
        )
        SELECT
            t.name,
            t.category,
            COUNT(r.ai_tool_id) AS recent_checks,
            COUNT(r.ai_tool_id) FILTER (
                WHERE r.status = 'up'
            ) AS successful_checks,
            COUNT(r.ai_tool_id) FILTER (
                WHERE r.status = 'down'
            ) AS failed_checks,
            ROUND(
                COUNT(r.ai_tool_id) FILTER (
                    WHERE r.status = 'up'
                ) * 100.0
                / NULLIF(COUNT(r.ai_tool_id), 0),
                2
            ) AS recent_uptime_percentage,
            ROUND(
                AVG(r.response_time_ms),
                2
            ) AS average_response_time_ms
        FROM ai_tools t
        LEFT JOIN ranked_checks r
            ON t.id = r.ai_tool_id
            AND r.check_number <= %s
        WHERE t.is_active = TRUE
        GROUP BY t.id, t.name, t.category
        ORDER BY recent_uptime_percentage DESC;
    """, (recent_checks,))

    rows = cursor.fetchall()

    cursor.close()

    summary = []

    for row in rows:
        summary.append({
            "name": row[0],
            "category": row[1],
            "recent_checks": row[2],
            "successful_checks": row[3],
            "failed_checks": row[4],
            "recent_uptime_percentage": row[5],
            "average_response_time_ms": row[6],
        })

    return summary


def get_reachability_summary(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            t.name,
            t.category,
            COUNT(h.id) AS total_checks,
            COUNT(h.id) FILTER (
                WHERE h.status_code IS NOT NULL
            ) AS reachable_checks,
            COUNT(h.id) FILTER (
                WHERE h.status_code IS NULL
            ) AS unreachable_checks,
            ROUND(
                COUNT(h.id) FILTER (
                    WHERE h.status_code IS NOT NULL
                ) * 100.0
                / NULLIF(COUNT(h.id), 0),
                2
            ) AS reachability_percentage
        FROM ai_tools t
        LEFT JOIN health_checks h
            ON t.id = h.ai_tool_id
        WHERE t.is_active = TRUE
        GROUP BY t.id, t.name, t.category
        ORDER BY reachability_percentage DESC;
    """)

    rows = cursor.fetchall()

    cursor.close()

    summary = []

    for row in rows:
        summary.append({
            "name": row[0],
            "category": row[1],
            "total_checks": row[2],
            "reachable_checks": row[3],
            "unreachable_checks": row[4],
            "reachability_percentage": row[5],
        })

    return summary
