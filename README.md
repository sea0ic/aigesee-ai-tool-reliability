# Aigesee AI

Aigesee AI is an independent AI tool reliability monitoring and analytics platform.

The project monitors publicly available AI-tool websites and services, records availability and performance over time, and turns the collected data into reliability analytics and visual insights.

## Project Goals

* Monitor AI tool availability
* Measure HTTP status and response time
* Track redirects, timeouts, and failures
* Store historical health-check results
* Calculate reliability and uptime metrics
* Analyze reliability across AI tool categories
* Automate periodic monitoring
* Provide a dashboard for exploring results

## Tech Stack

* Python
* Requests
* Python-dotenv
* PostgreSQL / Supabase
* Git / GitHub
* Streamlit
* Pytest

## Status

🚧 Project is currently under development.

## Project Structure

```text
aigesee-ai-tool-reliability/
├── src/
├── tests/
├── data/
├── .env.example
├── .gitignore
└── README.md
```
## Database Schema

### `ai_tools`

Stores publicly available AI tools that Aigesee AI may monitor.

| Column | Type | Description |
|---|---|---|
| `id` | BIGSERIAL | Unique identifier |
| `name` | TEXT | AI tool name |
| `website_url` | TEXT | Public website URL |
| `category` | TEXT | AI tool category |
| `description` | TEXT | Short description |
| `pricing_model` | TEXT | Pricing model |
| `pricing_url` | TEXT | Public pricing page |
| `documentation_url` | TEXT | Documentation URL |
| `github_url` | TEXT | Public GitHub repository |
| `source` | TEXT | Source of the tool information |
| `created_at` | TIMESTAMPTZ | Record creation time |
| `updated_at` | TIMESTAMPTZ | Last update time |
| `is_active` | BOOLEAN | Whether the tool is currently active |