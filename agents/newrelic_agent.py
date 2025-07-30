import pandas as pd

def fetch_newrelic_metrics(service, timeframe):
    df = pd.read_csv("data/newrelic.csv")
    df = df[df["service_name"] == service]
    return df.iloc[-1].to_dict() if not df.empty else {}
