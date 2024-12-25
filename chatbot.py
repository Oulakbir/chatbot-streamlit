import requests
import streamlit as st

# FastAPI server URL
API_URL = "http://127.0.0.1:8000/predict/"

# Title for the web app
st.title("💬 Banking Chatbot Assistant")

# Add custom CSS for chatbot styling
st.markdown(
    """
    <style>
    .chat-window {
        position: fixed;
        bottom: 16px;
        right: 16px;
        background-color: #fff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        width: 440px;
        height: 634px;
        display: flex;
        flex-direction: column;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        padding: 16px;
    }
    .chat-header {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .chat-subheader {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 16px;
    }
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        margin-bottom: 16px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .chat-message.user {
        text-align: right;
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 16px 0 16px 16px;
        max-width: 60%;
        margin-left: auto;
        margin-bottom: 10px;
        margin-top: 10px;
        color: #12412e;
    }
    .chat-message.bot {
        text-align: left;
        background-color: #0078D7;
        color: white;
        padding: 10px;
        border-radius: 0 16px 16px 16px;
        max-width: 60%;
    }
    .chat-input-container {
        display: flex;
        gap: 8px;
    }
    .chat-input {
        flex: 1;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    .chat-send-button {
        background-color: #000;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    .chat-send-button:hover {
        background-color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state to store conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat window structure

st.markdown('<div class="chat-header">Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-subheader">Powered by AI Banking Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

# Display chat history
for message in st.session_state["messages"]:
    if message["user"]:
        st.markdown(f'<div class="chat-message user">{message["user"]}</div>', unsafe_allow_html=True)
    if message["bot"]:
        st.markdown(f'<div class="chat-message bot">{message["bot"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # End of chat-messages div

# Chat input and send button
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("", key="user_input", placeholder="Type your question...", label_visibility="collapsed")
    submit_button = st.form_submit_button("Send")

# Process the user's message
if submit_button and user_input:
    # Append user message
    st.session_state["messages"].append({"user": user_input, "bot": ""})

    # Send request to API
    response = requests.post(API_URL, json={"text": user_input})
    if response.status_code == 200:
        prediction = response.json()
        bot_reply = (
            f"Intent: {prediction['prediction']}<br>"
            f"Confidence: {prediction['confidence']:.2f}%"
        )
    else:
        bot_reply = "Error: Unable to process the request. Try again later."

    # Append bot reply
    st.session_state["messages"][-1]["bot"] = bot_reply
    st.rerun()  # Refresh the chat window

st.markdown('</div>', unsafe_allow_html=True)  # End of chat-window div
