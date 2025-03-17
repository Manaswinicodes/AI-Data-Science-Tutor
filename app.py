import os
import streamlit as st
from dotenv import load_dotenv
import json
import random
import datetime

from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import requests

# Streamlit UI
st.set_page_config(page_title='Cute Data Science Tutor', page_icon="🎀", layout='wide')

# Custom CSS with girly theme elements
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
            box-shadow: 0 6px 12px rgba(219, 112, 147, 0.4);
            background: linear-gradient(90deg, #ff6b99, #ff85a2, #ffa6c9);
        }
        
        /* Button glow effect */
        .stButton > button:hover {
            box-shadow: 0 0 15px #ff85a2, 0 0 25px #ffa6c9;
        }
        
        /* Learning Level Selector */
        .level-selector {
            background: rgba(255, 255, 255, 0.85);
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 4px 15px rgba(219, 112, 147, 0.15);
            margin-bottom: 1.5rem;
            border: 2px solid #ffd1dc;
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
        
        /* Download Button */
        .download-button {
            background: linear-gradient(90deg, #c71585, #db7093) !important;
            border-radius: 20px !important;
            padding: 0.5rem 1rem !important;
            font-size: 0.85rem !important;
            margin-top: 1rem !important;
            font-family: 'Poppins', sans-serif !important;
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
        
        /* Avatar Selection */
        .avatar-selection {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .avatar-option {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 3px solid transparent;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .avatar-option:hover {
            transform: scale(1.1);
        }
        
        .avatar-option.selected {
            border-color: #ff85a2;
            box-shadow: 0 0 10px #ffa6c9;
        }
        
        /* Theme Background Selector */
        .theme-selection {
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin: 1rem 0;
        }
        
        .theme-option {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 2px solid white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .theme-option:hover {
            transform: scale(1.1);
        }
        
        .theme-option.selected {
            border-color: #ff85a2;
            box-shadow: 0 0 10px #ffa6c9;
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
        
        .quiz-option.correct {
            background: rgba(144, 238, 144, 0.6);
            border-color: green;
        }
        
        .quiz-option.incorrect {
            background: rgba(255, 182, 193, 0.6);
            border-color: red;
        }
        
        /* Weather Widget */
        .weather-widget {
            background: rgba(255, 255, 255, 0.7);
            border-radius: 15px;
            padding: 0.75rem;
            box-shadow: 0 4px 10px rgba(219, 112, 147, 0.15);
            margin-bottom: 1rem;
            border: 1px solid #ffd1dc;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        /* Clear Floats */
        .clearfix::after {
            content: "";
            clear: both;
            display: table;
        }
        
        /* Stickers Panel */
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
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #ff85a2, #ffa6c
