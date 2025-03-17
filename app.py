import os
import streamlit as st
import dotenv
dotenv.load_dotenv()

from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Streamlit UI
st.set_page_config(page_title='AI Data Science Tutor', page_icon="🧠", layout='wide')

# Custom CSS with modern UI elements
st.markdown("""
    <style>
        /* Main App Background */
        .stApp {
            background: linear-gradient(120deg, #f6f9fc, #eef2f7);
            font-family: 'Inter', sans-serif;
        }
        
        /* Header Styling */
        .main-header {
            background: linear-gradient(90deg, #3a1c71, #d76d77, #ffaf7b);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
            padding-top: 1.5rem;
        }
        
        .sub-header {
            color: #4a5568;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background: #1e293b;
            padding: 2rem 1.5rem;
            border-radius: 0;
        }
        
        /* Sidebar Titles */
        [data-testid="stSidebar"] h1 {
            color: #fff;
            font-weight: 700;
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid #475569;
            padding-bottom: 0.75rem;
        }
        
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #e2e8f0;
            font-weight: 600;
        }

        /* Sidebar Text */
        [data-testid="stSidebar"] p {
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        /* Sidebar Bullet Points */
        [data-testid="stSidebar"] ul {
            color: #cbd5e1;
            margin-left: 1rem;
        }
        
        [data-testid="stSidebar"] li {
            margin-bottom: 0.5rem;
        }

        /* Chat Container */
        .chat-container {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
            max-height: 60vh;
            overflow-y: auto;
        }
        
        /* User Message */
        .user-message {
            background: #075985;
            color: white;
            border-radius: 18px 18px 0 18px;
            padding: 0.75rem 1rem;
            margin: 1rem 0 1rem auto;
            max-width: 80%;
            position: relative;
            float: right;
            clear: both;
        }
        
        /* AI Message */
        .ai-message {
            background: #f1f5f9;
            color: #1e293b;
            border-radius: 18px 18px 18px 0;
            padding: 0.75rem 1rem;
            margin: 1rem auto 1rem 0;
            max-width: 80%;
            position: relative;
            float: left;
            clear: both;
        }
        
        /* Code blocks in AI messages */
        .ai-message pre {
            background: #1e293b;
            color: #e2e8f0;
            border-radius: 8px;
            padding: 0.75rem;
            overflow-x: auto;
            margin: 0.75rem 0;
        }
        
        /* Chat Input */
        .chat-input {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #3a1c71, #d76d77, #ffaf7b);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 0.6rem 1.5rem;
            font-size: 0.95rem;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }
        
        /* Learning Level Selector */
        .level-selector {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
        }
        
        /* Level Badges */
        .level-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }
        
        .beginner-badge {
            background-color: #22c55e;
            color: white;
        }
        
        .intermediate-badge {
            background-color: #3b82f6;
            color: white;
        }
        
        .advanced-badge {
            background-color: #8b5cf6;
            color: white;
        }
        
        /* Download Button */
        .download-button {
            background: #1e293b !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.85rem !important;
            margin-top: 1rem !important;
        }
        
        /* Clear Floats */
        .clearfix::after {
            content: "";
            clear: both;
            display: table;
        }
    </style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the chat model
chat_model = ChatGoogleGenerativeAI(model='gemini-1.5-pro', temperature=0.7, google_api_key=api_key)

# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# Custom header
st.markdown("<h1 class='main-header'>Data Science AI Tutor</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Your personal AI tutor for mastering data science concepts and techniques</p>", unsafe_allow_html=True)

# Sidebar content
st.sidebar.markdown("<h1>🧠 Learn With AI</h1>", unsafe_allow_html=True)
st.sidebar.markdown("""
<p>This AI-powered tutor helps you learn Data Science through interactive conversations. Get personalized explanations based on your knowledge level.</p>

<h2>Features</h2>
<ul>
    <li>Ask any Data Science questions</li>
    <li>Customize explanations to your level</li>
    <li>Get code examples and practical tips</li>
    <li>Export your learning session</li>
    <li>Continuous learning with memory</li>
</ul>

<h2>Topics You Can Explore</h2>
<ul>
    <li>Statistics & Probability</li>
    <li>Machine Learning Algorithms</li>
    <li>Data Visualization</li>
    <li>Feature Engineering</li>
    <li>Model Evaluation</li>
    <li>Python Libraries (Pandas, NumPy, Scikit-learn)</li>
    <li>Deep Learning Basics</li>
</ul>
""", unsafe_allow_html=True)

# Settings section
st.sidebar.markdown("<h2>Settings</h2>", unsafe_allow_html=True)

# Learning level selector with better styling
user_level = st.sidebar.radio(
    "Select your learning level:",
    ["Beginner", "Intermediate", "Advanced"],
    format_func=lambda x: f"{x} {'🔰' if x == 'Beginner' else '📚' if x == 'Intermediate' else '🚀'}"
)

# System message based on user level
system_message = SystemMessage(
    content=f"""You are an AI tutor specialized in answering only Data Science-related questions.
    If the user asks anything outside Data Science, politely refuse to answer.
    Provide responses based on the user's learning level: {user_level}.
    
    For Beginner level: Use simple explanations, avoid technical jargon, provide basic examples.
    For Intermediate level: Include more technical details, assume some prior knowledge, provide more complex examples.
    For Advanced level: Use advanced terminology, provide in-depth explanations, include cutting-edge techniques.
    
    Structure your responses with clear headings and use markdown formatting for better readability.
    When providing code examples, use proper code blocks with syntax highlighting.
    """
)

# Chat container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display chat history with improved styling
for msg in st.session_state.memory.chat_memory.messages:
    if isinstance(msg, HumanMessage):
        st.markdown(f"<div class='user-message'>{msg.content}</div><div class='clearfix'></div>", unsafe_allow_html=True)
    elif isinstance(msg, AIMessage):
        st.markdown(f"<div class='ai-message'>{msg.content}</div><div class='clearfix'></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# User input with improved styling
st.markdown("<div class='chat-input'>", unsafe_allow_html=True)
user_query = st.chat_input("Ask me anything about Data Science...")
st.markdown("</div>", unsafe_allow_html=True)

# Level indicator
level_color = "beginner-badge" if user_level == "Beginner" else "intermediate-badge" if user_level == "Intermediate" else "advanced-badge"
st.markdown(f"<div style='text-align: right;'><span class='level-badge {level_color}'>{user_level} {('🔰' if user_level == 'Beginner' else '📚' if user_level == 'Intermediate' else '🚀')}</span></div>", unsafe_allow_html=True)

# Process user input
if user_query:
    conversation_history = [system_message] + st.session_state.memory.chat_memory.messages + [HumanMessage(content=user_query)]

    with st.spinner("Thinking..."):
        ai_response = chat_model.invoke(conversation_history)

    # Extract response for the selected level
    def extract_response_for_level(full_response, level):
        sections = {
            "Beginner": "🔰 Beginner:",
            "Intermediate": "📚 Intermediate:",
            "Advanced": "🚀 Advanced:"
        }

        if sections[level] in full_response:
            start_idx = full_response.find(sections[level])
            next_section_idx = min(
                [full_response.find(sec) for sec in sections.values() if full_response.find(sec) > start_idx and sec != sections[level]] + [len(full_response)]
            )
            return full_response[start_idx:next_section_idx].strip()
        
        return full_response

    filtered_response = extract_response_for_level(ai_response.content, user_level)

    # Update memory
    st.session_state.memory.chat_memory.add_user_message(user_query)
    st.session_state.memory.chat_memory.add_ai_message(filtered_response)

    # Display updated chat (this will be shown on the next rerun)
    st.rerun()

# Collect chat history for download
chat_history = []
for msg in st.session_state.memory.chat_memory.messages:
    if isinstance(msg, HumanMessage):
        chat_history.append(f"User: {msg.content}")
    elif isinstance(msg, AIMessage):
        chat_history.append(f"AI: {msg.content}")

# Export and reset buttons
col1, col2 = st.columns([1, 1])

with col1:
    if chat_history:
        chat_text = "\n\n".join(chat_history)
        st.download_button(
            "📥 Download Chat History", 
            chat_text, 
            file_name="data_science_learning_session.txt",
            key="download-chat",
        )

with col2:
    if st.button("🔄 Reset Chat"):
        st.session_state.memory.clear()
        st.rerun()
