import os
import streamlit as st
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Validate API Key
if not api_key:
    st.error("⚠️ API key not found. Please check your .env file.")
    st.stop()

# Set page config
st.set_page_config(page_title="AI Data Science Tutor", page_icon="🧠", layout="wide")

# Custom CSS to style UI like ChatGPT
st.markdown(
    """
    <style>
    body {
        color: white;
        background-color: #0E1117;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .user-message {
        background-color: #4CAF50;
        color: white;
        text-align: left;
    }
    .ai-message {
        background-color: #1E1E1E;
        color: white;
        text-align: left;
    }
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        background-color: #1E1E1E;
        color: white;
        padding: 10px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px;
        width: 100%;
    }
    .chat-container {
        display: flex;
        flex-direction: column-reverse;
        height: 500px;
        overflow-y: auto;
        border: 1px solid #4CAF50;
        padding: 10px;
        border-radius: 10px;
        background-color: #222;
    }
    .fixed-input {
        position: fixed;
        bottom: 10px;
        width: 90%;
        left: 5%;
        padding: 10px;
        background-color: #0E1117;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.header("🛠 Settings")
user_level = st.sidebar.radio("Select your learning level:", ["Beginner", "Intermediate", "Advanced"])
st.sidebar.write("⚡ AI will adjust explanations based on your selected level.")

# Initialize chat model
chat_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,
    google_api_key=api_key
)

# Initialize memory for chat
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# Title and Description
st.title("🧠 AI Data Science Tutor")
st.markdown("Welcome to your **AI Tutor**, designed to help you master data science concepts efficiently!")

# Chat History UI
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in reversed(st.session_state.memory.chat_memory.messages):
    role = "user-message" if isinstance(msg, HumanMessage) else "ai-message"
    st.markdown(f'<div class="stChatMessage {role}">{msg.content}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# User Input Box at Bottom
with st.container():
    with st.form("chat_form"):
        user_input = st.text_input("🔍 Type your message...", key="user_input")
        submit = st.form_submit_button("Send")

# Handle User Input
if submit and user_input:
    try:
        system_message = SystemMessage(content=f"Provide responses at a {user_level} level.")
        user_message = HumanMessage(content=user_input)

        # Generate response
        response = chat_model.invoke([system_message, user_message])

        # Save chat history
        st.session_state.memory.save_context({"input": user_input}, {"output": response.content})

        # Refresh the page to show updated messages
        st.rerun()

    except Exception as e:
        st.error(f"🚨 Error: {e}")
