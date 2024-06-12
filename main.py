import streamlit as st
import requests
from dotenv import load_dotenv
import os


_ = load_dotenv()


endpoint = 'https://api.together.xyz/v1/chat/completions'


st.title("Joyce Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.placeholder = "Yeehaw"
    st.session_start.API_KEY = None

with st.sidebar:
    text_input = st.text_input(
        "Please put your Together AI API key 👇",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder,
    )
    st.session_state.API_KEY = text_input

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    if not st.session_state.API_KEY:
        st.toast('Put your Key in Bitch!')
    else:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        res = requests.post(endpoint, json={
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "max_tokens": 4096,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stop": [
                "<|eot_id|>"
            ],
            "messages": st.session_state.messages[-10:]
        }, headers={
            # "Authorization": f"Bearer {os.getenv('TOGETHERAPIKEY')}",
            "Authorization": f"Bearer {st.session_state.API_KEY}",
        })
        # res = requests.post(endpoint, json={
        # "model": "deepseek-ai/deepseek-coder-33b-instruct",
        # "max_tokens": 512,
        # "temperature": 0.7,
        # "top_p": 0.7,
        # "top_k": 50,
        # "repetition_penalty": 1,
        # "stop": [
        #     "<|EOT|>",
        #     "<｜begin▁of▁sentence｜>",
        #     "<｜end▁of▁sentence｜>"
        #     ],
        #     "messages": [
        #         {
        #             "content": f"{prompt}",
        #             "role": "user"
        #         }
        #     ]
        # }, headers={
            
        # })
        response_from_together = res.json()

        response = response_from_together['choices'][0]["message"]["content"]
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
