import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from agent.agent import run_agent

st.set_page_config(page_title="HR AI Agent", layout="wide")

st.title("🤖 HR AI Agent")

# Debug toggle
show_debug = st.sidebar.toggle("Show Debug Logs", value=True)

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Logs
if "logs" not in st.session_state:
    st.session_state.logs = []

# Show chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if query := st.chat_input("Ask HR related question..."):

    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):

        import io
        import sys

        log_stream = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = log_stream

        try:
            response = run_agent(query, st.session_state.messages)
        finally:
            sys.stdout = old_stdout

        logs = log_stream.getvalue()
        print(logs)  # also print in terminal

        # logs = log_stream.getvalue()

        st.markdown(response)

        st.session_state.logs.append({
            "query": query,
            "logs": logs
        })

    st.session_state.messages.append({"role": "assistant", "content": response})

# Debug panel
if show_debug:
    st.sidebar.title("🛠 Debug Logs")

    for log in reversed(st.session_state.logs[-5:]):
        with st.sidebar.expander(log["query"]):
            st.code(log["logs"])