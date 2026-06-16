import streamlit as st
from langgraph_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

st.write("version 2.0")
print("i am frontend")


# *********************************** Utility functions *******************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return str(thread_id)


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_threads(st.session_state["thread_id"])
    st.session_state["message_history"] = []


def add_threads(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    if state is None or not state.values:
        return []
    return state.values.get("messages", [])

# *********************************session-setup************************************

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(generate_thread_id())

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_threads(st.session_state["thread_id"])

# ********************************* Sidebar UI ***********************************
st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()

st.sidebar.divider()
st.sidebar.header("My conversations")

for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(thread_id, key=f"btn_{thread_id}"):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)

        temp_msg = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = "user"
            else:
                role = "assistant"
            temp_msg.append({"role": role, "content": msg.content})

        st.session_state["message_history"] = temp_msg
        st.rerun()


for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Type here")

if user_input:
    # first add the message to st.session_state['message_history']
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, _ in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                stream_mode="messages",
            )
        )
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})

