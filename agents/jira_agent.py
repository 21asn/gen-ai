import pandas as pd

def search_jira_issues(service, timeframe):
    df = pd.read_csv("data/jira.csv")
    issues = df[df["service_name"] == service]
    return {"issues": issues["summary"].tolist()} if not issues.empty else {"issues": []}
