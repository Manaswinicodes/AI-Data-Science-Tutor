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

# Custom CSS for sleek UI
st.markdown(
    """
    <style>
    body {
        color: white;
        background-color: #0E1117;
    }
    .stApp {
        max-width: 800px;
        margin: auto;
        padding: 20px;
    }
    .chat-container {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        max-height: 60vh;
        overflow-y: auto;
        display: flex;
        flex-direction: column-reverse; /* Ensures the latest message is always visible */
    }
    .user-message, .ai-message {
        padding: 12px;
        border-radius: 10px;
        margin: 5px 0;
        font-size: 16px;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #4CAF50;
        color: white;
        align-self: flex-end;
    }
    .ai-message {
        background-color: #333;
        color: white;
        align-self: flex-start;
    }
    .input-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        background-color: #1E1E1E;
        color: white;
        padding: 12px;
        font-size: 16px;
        width: 100%;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #388E3C;
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

# Chat Display Container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Show chat history
if st.session_state.memory.chat_memory.messages:
    for msg in reversed(st.session_state.memory.chat_memory.messages):  # Reverse to show the latest message at the
