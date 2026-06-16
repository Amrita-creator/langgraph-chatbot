from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import os
import sqlite3
load_dotenv()
print("i am the backend")


llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    max_new_tokens=2400,
)
model = ChatHuggingFace(llm=llm)
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState) -> ChatState:
    # take user query from state
    messages = state["messages"]

    # send to llm
    response = model.invoke(messages)

    # response store state
    return {"messages": [response]}

conn = sqlite3.connect(database = 'chatbot.db',check_same_thread=False)    #explicitly restrict checking for same thread 
checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(ChatState)

# add node
graph.add_node("chat_node", chat_node)

# add edges
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# compile
chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_thread = set()
    for chpt in (checkpointer.list(None)): #None-> allthread
        all_thread.add(chpt.config['configurable']['thread_id'])
    return list(all_thread)

