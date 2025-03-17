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
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50;
        border-radius: 12px;
        background-color: #1E1E1E;
        color: white;
        padding: 12px;
        font-size: 16px;
        width: 100%;
    }
    .stTextInput > div > div > input:focus {
        border-color: #90EE90;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #388E3C;
    }
    .chat-container {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        max-height: 400px;
        overflow-y: auto;
    }
    .user-message {
        text-align: right;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .ai-message {
        text-align: left;
        background-color: #333;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .input-container {
        position: fixed;
        bottom: 20px;
        width: 60%;
        left: 20%;
        right: 20%;
        display: flex;
        gap: 10px;
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
    for msg in st.session_state.memory.chat_memory.messages:
        role_class = "user-message" if isinstance(msg, HumanMessage) else "ai-message"
        role_label = "🧑‍💻 You" if isinstance(msg, HumanMessage) else "🤖 AI"
        st.markdown(f'<div class="{role_class}"><b>{role_label}:</b><br>{msg.content}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat Input Container
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.text_input("Type your message...", key="user_input", label_visibility="collapsed")
submit = st.button("Send")
st.markdown('</div>', unsafe_allow_html=True)

# Handle input submission
if submit and user_input:
    try:
        system_message = SystemMessage(content=f"Provide responses at a {user_level} level.")
        user_message = HumanMessage(content=user_input)

        # Generate response
        response = chat_model.invoke([system_message, user_message])

        # Save chat history
        st.session_state.memory.save_context({"input": user_input}, {"output": response.content})

        # Refresh the page to show new messages
        st.experimental_rerun()

    except Exception as e:
        st.error(f"🚨 Error: {e}")
