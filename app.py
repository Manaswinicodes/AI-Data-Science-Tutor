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

# Initialize Streamlit app
st.set_page_config(page_title="AI Data Science Tutor", page_icon="🧠", layout="wide")

# Initialize Chat Model
chat_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,
    google_api_key=api_key
)

# Initialize session state for chat memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# UI Headers
st.title("🧠 AI-Powered Data Science Tutor")
st.markdown("Welcome to your **AI Tutor**, designed to help you master data science concepts efficiently!")

# Sidebar settings
st.sidebar.header("🛠 Settings")
user_level = st.sidebar.radio("Select your learning level:", ["Beginner", "Intermediate", "Advanced"])
st.sidebar.write("⚡ AI will adjust explanations based on your selected level.")

# Set system message based on user level
system_message = SystemMessage(content=f"Provide responses at a {user_level} level.")

# User input
user_input = st.text_input("🔍 Ask a Data Science question:", key="user_input")

if user_input:
    try:
        # Convert input to proper format
        user_message = HumanMessage(content=user_input)
        
        # Generate response
        response = chat_model.invoke([system_message, user_message])  # Ensure the input is a list of messages
        
        # Store chat in session state
        st.session_state.memory.save_context({"input": user_input}, {"output": response.content})
        
        # Display response
        st.subheader("📢 AI Response:")
        st.write(response.content)
        
        # Show chat history
        with st.expander("📜 Chat History"):
            for msg in st.session_state.memory.chat_memory.messages:
                role = "🧑‍💻 You" if isinstance(msg, HumanMessage) else "🤖 AI"
                st.markdown(f"**{role}:** {msg.content}")

    except Exception as e:
        st.error(f"🚨 Error: {e}")
