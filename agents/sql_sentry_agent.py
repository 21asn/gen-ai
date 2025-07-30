import pandas as pd

def query_sql_sentry(service, timeframe):
    df = pd.read_csv("data/sql_sentry.csv")
    df = df[df["service_name"] == service]
    return df.iloc[-1].to_dict() if not df.empty else {}
