import os
import json
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from langchain.chat_models import BedrockChat
from langchain.schema import HumanMessage
from agents.sql_sentry_agent import query_sql_sentry
from agents.newrelic_agent import fetch_newrelic_metrics
from agents.jira_agent import search_jira_issues
from mcp.agent_definitions import AGENT_DEFINITIONS
from rag.rag_helper import query_chroma
from agents.db_config_agent import check_db_user_settings


load_dotenv()

model = BedrockChat(
    region_name=os.environ["AWS_REGION"],
    model_id=os.environ["CLAUDE_MODEL_ID"]
)

def run_agents(state):
    prompt = state.get("system_prompt", "You are an expert observability AI. Analyze the data and report anomalies.")

    service = state.get("service")
    timeframe = state.get("timeframe")

    sql_data = query_sql_sentry(service, timeframe) if service and timeframe else query_sql_sentry(None, None)
    nr_data = fetch_newrelic_metrics(service, timeframe) if service and timeframe else fetch_newrelic_metrics(None, None)
    jira_data = search_jira_issues(service, timeframe) if service and timeframe else search_jira_issues(None, None)

    # NEW: if db analysis is needed (always check)
    from agents.db_config_agent import check_db_user_settings
    db_findings = check_db_user_settings(service)

    summary = f"Here are the findings:\n"

    if service:
        summary += (
            f"- SQL Sentry: CPU {sql_data.get('cpu_usage')}%, Blocking Sessions: {sql_data.get('blocking_sessions')}\n"
            f"- New Relic: Latency {nr_data.get('latency_ms')}ms, Error Rate {nr_data.get('error_rate_percent')}%\n"
            f"- Jira: Issues: {jira_data.get('issues')}\n"
        )

    summary += f"- DB Policy Findings: {db_findings}"

    mcp_context = json.dumps(AGENT_DEFINITIONS, indent=2)
    rag_context = "\n".join([doc.page_content for doc in query_chroma(prompt)])

    messages = [
        HumanMessage(content=prompt),
        HumanMessage(content=f"The following agents are available:\n{mcp_context}"),
        HumanMessage(content=f"Relevant historical context:\n{rag_context}"),
        HumanMessage(content=f"Analyze this data:\n{summary}")
    ]
    ai_response = model(messages)
    state["report"] = ai_response.content
    return state


def is_service_specific(query: str) -> bool:
    keywords = ["analyze", "latency", "error rate", "performance", "App", "Service"]
    return any(kw.lower() in query.lower() for kw in keywords)


builder = StateGraph(dict)
builder.add_node("analyze", run_agents)
builder.set_entry_point("analyze")
builder.add_edge("analyze", END)
graph = builder.compile()

if __name__ == "__main__":
    user_prompt = input("💬 Ask your question (e.g., Analyze PaymentsService over the past 4 hours):\n")

    inputs = {
        "system_prompt": user_prompt
    }

    if is_service_specific(user_prompt):
        inputs["service"] = input("Service name: ")
        inputs["timeframe"] = input("Timeframe (e.g., past 2 hours): ")

    result = graph.invoke(inputs)

    print("\n🧠 Observability Report:\n")
    print(result["report"])
