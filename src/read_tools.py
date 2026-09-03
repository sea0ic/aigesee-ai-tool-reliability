from db import get_connection


try:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, website_url, category, is_active
        FROM ai_tools
        WHERE is_active = TRUE
        ORDER BY id;
    """)

    tools = cursor.fetchall()

    print("AI tools found:")

    for tool in tools:
        print(tool)

    cursor.close()
    connection.close()

except Exception as error:
    print("Failed to read AI tools.")
    print(f"Error: {error}")