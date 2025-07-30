import pandas as pd
import os

os.makedirs("rag_data", exist_ok=True)

def csv_to_rag_text(csv_file, output_txt_file, formatter_fn):
    df = pd.read_csv(csv_file)
    with open(output_txt_file, "w") as f:
        for _, row in df.iterrows():
            f.write(formatter_fn(row))
            f.write("\n\n")

def format_sql(row):
    return (f"{row['service_name']} had CPU usage of {row['cpu_usage']}%, "
            f"{row['blocking_sessions']} blocking sessions, and IO wait of {row['io_wait']}.")

def format_newrelic(row):
    return (f"{row['service_name']} had {row['latency_ms']}ms latency, "
            f"{row['throughput_rpm']} RPM throughput, and {row['error_rate_percent']}% error rate.")

def format_jira(row):
    return f"{row['service_name']} has Jira issue reported: {row['summary']}."

csv_to_rag_text("../data/sql_sentry.csv", "rag_data/sql_rag.txt", format_sql)
csv_to_rag_text("../data/newrelic.csv", "rag_data/nr_rag.txt", format_newrelic)
csv_to_rag_text("../data/jira.csv", "rag_data/jira_rag.txt", format_jira)
