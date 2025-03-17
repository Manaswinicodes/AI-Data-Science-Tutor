import os
import streamlit as st
from dotenv import load_dotenv

from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import requests
import random
import json

# Streamlit UI
st.set_page_config(page_title='Cute Data Science Tutor', page_icon="🎀", layout='wide')

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
weather_api_key = os.getenv("OPENWEATHER_API_KEY")

# Custom CSS with girly theme
st.markdown("""
    <style>
        /* Import Custom Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&family=Poppins:wght@300;400;600&display=swap');
        
        /* Main App Background */
        .stApp {
            background: linear-gradient(120deg, #fff0f5, #ffefd5, #e6e6fa);
            font-family: 'Poppins', sans-serif;
        }
        
        /* Header Styling */
        .main-header {
            background: linear-gradient(90deg, #ff85a2, #ffa6c9, #ffb7ce);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            font-family: 'Dancing Script', cursive;
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
            padding-top: 1.5rem;
        }
        
        .sub-header {
            color: #db7093;
            text-align: center;
            font-family: 'Poppins', sans-serif;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffddf4, #ffe6f2);
            padding: 2rem 1.5rem;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(219, 112, 147, 0.2);
        }
        
        /* Sidebar Titles */
        [data-testid="stSidebar"] h1 {
            color: #db7093;
            font-family: 'Dancing Script', cursive;
            font-weight: 700;
            font-size: 2rem;
            margin-bottom: 1.5rem;
            border-bottom: 2px dashed #ffb7ce;
            padding-bottom: 0.75rem;
        }
        
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #db7093;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
        }

        /* Sidebar Text */
        [data-testid="stSidebar"] p {
            color: #ff69b4;
            font-family: 'Poppins', sans-serif;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        /* Sidebar Bullet Points */
        [data-testid="stSidebar"] ul {
            color: #ff69b4;
            margin-left: 1rem;
        }
        
        [data-testid="stSidebar"] li {
            margin-bottom: 0.5rem;
        }
        
        [data-testid="stSidebar"] li::marker {
            content: "🌸 ";
        }

        /* Chat Container */
        .chat-container {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(219, 112, 147, 0.15);
            margin-bottom: 1.5rem;
            max-height: 60vh;
            overflow-y: auto;
            border: 2px solid #ffd1dc;
        }
        
        /* User Message */
        .user-message {
            background: linear-gradient(90deg, #ffb7ce, #ffc1cc);
            color: #8b008b;
            border-radius: 18px 18px 0 18px;
            padding: 0.75rem 1rem;
            margin: 1rem 0 1rem auto;
            max-width: 80%;
            position: relative;
            float: right;
            clear: both;
            box-shadow: 0 3px 10px rgba(219, 112, 147, 0.2);
            animation: fadeInRight 0.5s ease-out;
        }
        
        /* AI Message */
        .ai-message {
            background: linear-gradient(90deg, #e6e6fa, #f0f8ff);
            color: #8b008b;
            border-radius: 18px 18px 18px 0;
            padding: 0.75rem 1rem;
            margin: 1rem auto 1rem 0;
            max-width: 80%;
            position: relative;
            float: left;
            clear: both;
            box-shadow: 0 3px 10px rgba(219, 112, 147, 0.2);
            animation: fadeInLeft 0.5s ease-out;
        }
        
        /* Animations for chat bubbles */
        @keyframes fadeInRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes fadeInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* Code blocks in AI messages */
        .ai-message pre {
            background: #36013f;
            color: #ffd1dc;
            border-radius: 12px;
            padding: 0.75rem;
            overflow-x: auto;
            margin: 0.75rem 0;
        }
        
        /* Chat Input */
        .chat-input {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 4px 15px rgba(219, 112, 147, 0.15);
            border: 2px solid #ffd1dc;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(90deg, #ff85a2, #ffa6c9, #ffb7ce);
            color: white;
            border-radius: 20px;
            border: none;
            padding: 0.6rem 1.5rem;
            font-size: 0.95rem;
            font-weight: 600;
            box-shadow: 0 4px 10px rgba(219, 112, 147, 0.3);
            transition: all 0.3s ease;
            font-family: 'Poppins', sans-serif;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(219, 112, 147, 0.4), 0 0 15px #ff85a2, 0 0 25px #ffa6c9;
        }
        
        /* Level Badges */
        .level-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 0.5rem;
            font-family: 'Poppins', sans-serif;
        }
        
        .beginner-badge {
            background-color: #ff85a2;
            color: white;
        }
        
        .intermediate-badge {
            background-color: #ffa6c9;
            color: white;
        }
        
        .advanced-badge {
            background-color: #ffb7ce;
            color: white;
        }
        
        /* Progress Tracker */
        .progress-container {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 4px 15px rgba(219, 112, 147, 0.15);
            margin: 1.5rem 0;
            border: 2px solid #ffd1dc;
        }
        
        .progress-bar {
            height: 20px;
            background: #f0f0f0;
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff85a2, #ffa6c9, #ffb7ce);
            border-radius: 10px;
            transition: width 0.5s ease;
        }
        
        .progress-stars {
            margin-top: 0.5rem;
            text-align: center;
            font-size: 1.2rem;
        }
        
        /* Emoji Reactions */
        .emoji-reactions {
            display: flex;
            justify-content: flex-end;
            margin-top: 0.5rem;
            gap: 0.5rem;
        }
        
        .emoji-button {
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            transition: transform 0.2s;
            padding: 0.2rem;
        }
        
        .emoji-button:hover {
            transform: scale(1.3);
        }
        
        /* Quiz Container */
        .quiz-container {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(219, 112, 147, 0.15);
            margin: 1.5rem 0;
            border: 2px solid #ffd1dc;
        }
        
        .quiz-option {
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid #ffd1dc;
            border-radius: 10px;
            padding: 0.75rem;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .quiz-option:hover {
            background: #ffd1dc;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(219, 112, 147, 0.2);
        }
        
        .stickers-panel {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.5rem;
            margin: 0.5rem 0;
        }
        
        .sticker-item {
            cursor: pointer;
            transition: transform 0.2s;
            text-align: center;
        }
        
        .sticker-item:hover {
            transform: scale(1.2);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
if "progress" not in st.session_state:
    st.session_state.progress = 0
if "stars_earned" not in st.session_state:
    st.session_state.stars_earned = 0
if "reactions" not in st.session_state:
    st.session_state.reactions = []
if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False
if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None
if "sticker_panel_open" not in st.session_state:
    st.session_state.sticker_panel_open = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "avatar" not in st.session_state:
    st.session_state.avatar = "👩‍🔬"  # Default avatar
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "Pink Dreams"

# Initialize the chat model
chat_model = ChatGoogleGenerativeAI(model='gemini-1.5-pro', temperature=0.7, google_api_key=api_key)

# Display header
st.markdown(f"<h1 class='main-header'>Cute Data Science Tutor</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-header'>Your adorable AI companion for learning data science! ✨</p>", unsafe_allow_html=True)

# Create two columns for the main layout
col1, col2 = st.columns([3, 1])

# Sidebar Configuration
with st.sidebar:
    st.markdown("<h1>Customize Your Experience</h1>", unsafe_allow_html=True)
    
    # Avatar selection
    st.markdown("<h2>Choose Your Avatar</h2>", unsafe_allow_html=True)
    avatar_options = ["👩‍🔬", "👨‍🔬", "🧚‍♀️", "🦄", "🌈", "🌸", "🐱", "🐶"]
    avatar_cols = st.columns(4)
    for i, avatar in enumerate(avatar_options):
        col_index = i % 4
        with avatar_cols[col_index]:
            if st.button(avatar, key=f"avatar_{i}"):
                st.session_state.avatar = avatar
    
    st.markdown(f"<p>Your current avatar: {st.session_state.avatar}</p>", unsafe_allow_html=True)
    
    # Theme selection
    st.markdown("<h2>Choose Your Theme</h2>", unsafe_allow_html=True)
    theme_options = ["Pink Dreams", "Lavender Mist", "Bubblegum Pop", "Pastel Paradise"]
    selected_theme = st.selectbox("Select Theme", theme_options, index=theme_options.index(st.session_state.selected_theme))
    if selected_theme != st.session_state.selected_theme:
        st.session_state.selected_theme = selected_theme
        st.experimental_rerun()
    
    # Difficulty level
    st.markdown("<h2>Difficulty Level</h2>", unsafe_allow_html=True)
    difficulty = st.select_slider(
        "Select your learning level:",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Beginner"
    )
    
    # Display badge based on difficulty
    if difficulty == "Beginner":
        badge_color = "beginner-badge"
    elif difficulty == "Intermediate":
        badge_color = "intermediate-badge"
    else:
        badge_color = "advanced-badge"
