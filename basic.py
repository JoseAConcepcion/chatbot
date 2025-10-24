import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url=st.secrets.base_url,
    api_key=st.secrets.api_key,
)

for msg in st.session_state.get("conversation", []):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

msg = st.chat_input()

if not msg:
    st.stop()

with st.chat_message("user"):
    st.write(msg)

if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.session_state.conversation.append(dict(role="user", content=msg))


def reply(str: str):
    conversation = st.session_state.conversation

    for chunk in client.chat.completions.create(
        model=st.secrets.model,
        messages=conversation,
        stream=True,
    ):
        if msg := chunk.choices[0].delta.content:
            yield msg


with st.chat_message("assistant"):
    response = st.write(reply(msg))

st.session_state.conversation.append(dict(role="assistant", content=response))
