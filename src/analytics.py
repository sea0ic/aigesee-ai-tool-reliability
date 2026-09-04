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