import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import openai

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-"

class GraphState(dict):
    pass

llm = ChatOpenAI(model="gpt-3.5-turbo")  # or "gpt-4"

def ask_llm(state: GraphState) -> GraphState:
    messages = state.get("messages", [])
    response = llm(messages)
    messages.append(AIMessage(content=response.content))
    return {"messages": messages}

def decide_next_step(state: GraphState) -> str:
    last_message = state["messages"][-1].content
    if last_message.strip().endswith("?"):
        return "ask"
    else:
        return "end"

builder = StateGraph(GraphState)
builder.add_node("ask", ask_llm)
builder.set_entry_point("ask")
builder.add_conditional_edges("ask", decide_next_step, {"ask": "ask", "end": END})
graph = builder.compile()

initial_input = {
    "messages": [HumanMessage(content="Tell me something interesting about space.")]
}

final_state = graph.invoke(initial_input)
print("\nConversation:")
for msg in final_state["messages"]:
    speaker = "User" if isinstance(msg, HumanMessage) else "AI"
    print(f"{speaker}: {msg.content}")
