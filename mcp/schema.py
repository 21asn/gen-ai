from typing import TypedDict, List

class SQLSentryMetrics(TypedDict):
    cpu_usage: float
    blocking_sessions: int
    io_wait: float

class NewRelicMetrics(TypedDict):
    latency: float
    error_rate: float
    throughput: float

class JiraIssues(TypedDict):
    issues: List[str]
    priorities: List[str]
