AGENT_DEFINITIONS = [
    {
        "agent": "sql_sentry_agent",
        "tool": "query_sql_sentry",
        "inputs": ["service", "timeframe"],
        "outputs": ["cpu_usage", "blocking_sessions", "io_wait"]
    },
    {
        "agent": "newrelic_agent",
        "tool": "fetch_newrelic_metrics",
        "inputs": ["service", "timeframe"],
        "outputs": ["latency_ms", "throughput_rpm", "error_rate_percent"]
    },
    {
        "agent": "jira_agent",
        "tool": "search_jira_issues",
        "inputs": ["service", "timeframe"],
        "outputs": ["issues"]
    },
    {
  "agent": "db_config_agent",
  "tool": "check_db_user_settings",
  "inputs": ["db_user_settings"],
  "outputs": ["findings", "non_compliant_users"]
    }
]
