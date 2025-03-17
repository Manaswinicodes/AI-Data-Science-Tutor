import streamlit as st
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import requests
import random
import time
import google.generativeai as genai
import base64
from io import BytesIO
from PIL import Image

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

# Page config
st.set_page_config(page_title="Cute AI Travel Planner", page_icon="✈️", layout="wide")

# Custom CSS for animations and styling
st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #fcf7ff;
    }
    
    /* Header styles */
    .main-header {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        background: linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        text-align: center;
        padding: 1rem 0;
        font-size: 3rem !important;
    }
    
    .sub-header {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #f687b3;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Chat message animations */
    @keyframes pop-in {
        0% { transform: scale(0); opacity: 0; }
        70% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .user-message {
        background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
        color: white;
        border-radius: 20px 20px 5px 20px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 75%;
        float: right;
        clear: both;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: pop-in 0.5s forwards;
        position: relative;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
        color: #444;
        border-radius: 20px 20px 20px 5px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 75%;
        float: left;
        clear: both;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        animation: pop-in 0.5s forwards;
        position: relative;
    }
    
    .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
        vertical-align: middle;
    }
    
    /* Button glow effect */
    .stButton>button {
        background: linear-gradient(135deg, #fccb90 0%, #d57eeb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 5px 20px rgba(213, 126, 235, 0.4) !important;
    }
    
    .stButton>button::after {
        content: "" !important;
        position: absolute !important;
        top: -50% !important;
        left: -50% !important;
        width: 200% !important;
        height: 200% !important;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%) !important;
        opacity: 0 !important;
        transition: opacity 0.3s ease !important;
    }
    
    .stButton>button:hover::after {
        opacity: 1 !important;
    }
    
    /* Emoji reactions */
    .emoji-reaction {
        display: inline-block;
        background: white;
        border-radius: 20px;
        padding: 5px 10px;
        margin: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .emoji-reaction:hover {
        transform: scale(1.2);
    }
    
    .emoji-selected {
        background: #ffeaa7;
        transform: scale(1.1);
    }
    
    /* Progress bar */
    .progress-container {
        width: 100%;
        height: 25px;
        background-color: #f8edff;
        border-radius: 15px;
        margin: 10px 0;
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #fd79a8, #a29bfe);
        border-radius: 15px;
        transition: width 0.5s ease;
        position: relative;
    }
    
    .progress-star {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        font-size: 15px;
    }
    
    /* Quiz styles */
    .quiz-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    .quiz-option {
        padding: 10px 15px;
        margin: 8px 0;
        background: #f8edff;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .quiz-option:hover {
        background: #f0c7ff;
        transform: translateX(5px);
    }
    
    .quiz-correct {
        background: #c4f2c8 !important;
    }
    
    .quiz-incorrect {
        background: #ffd3d3 !important;
    }
    
    /* Background themes */
    .bg-cherry-blossoms {
        background-color: #ffeef2;
        background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZmZlZWYyIi8+PGNpcmNsZSBjeD0iMTAiIGN5PSIxMCIgcj0iMiIgZmlsbD0iI2ZmYzBjYiIvPjxjaXJjbGUgY3g9IjQwIiBjeT0iMjAiIHI9IjIiIGZpbGw9IiNmZmMwY2IiLz48Y2lyY2xlIGN4PSI3MCIgY3k9IjMwIiByPSIyIiBmaWxsPSIjZmZjMGNiIi8+PGNpcmNsZSBjeD0iMzAiIGN5PSI1MCIgcj0iMiIgZmlsbD0iI2ZmYzBjYiIvPjxjaXJjbGUgY3g9IjgwIiBjeT0iNzAiIHI9IjIiIGZpbGw9IiNmZmMwY2IiLz48Y2lyY2xlIGN4PSIyMCIgY3k9IjgwIiByPSIyIiBmaWxsPSIjZmZjMGNiIi8+PGNpcmNsZSBjeD0iNjAiIGN5PSI5MCIgcj0iMiIgZmlsbD0iI2ZmYzBjYiIvPjxjaXJjbGUgY3g9IjkwIiBjeT0iNDAiIHI9IjIiIGZpbGw9IiNmZmMwY2IiLz48Y2lyY2xlIGN4PSI1MCIgY3k9IjYwIiByPSIyIiBmaWxsPSIjZmZjMGNiIi8+PC9zdmc+');
    }
    
    .bg-dreamy-clouds {
        background-color: #f7fdff;
        background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjdmZGZmIi8+PGNpcmNsZSBjeD0iMjAiIGN5PSIzMCIgcj0iMTAiIGZpbGw9IiNlOGY0ZmYiLz48Y2lyY2xlIGN4PSI1MCIgY3k9IjIwIiByPSIxNSIgZmlsbD0iI2U4ZjRmZiIvPjxjaXJjbGUgY3g9IjcwIiBjeT0iNDAiIHI9IjEwIiBmaWxsPSIjZThmNGZmIi8+PGNpcmNsZSBjeD0iMzAiIGN5PSI2MCIgcj0iMTIiIGZpbGw9IiNlOGY0ZmYiLz48Y2lyY2xlIGN4PSI4MCIgY3k9IjcwIiByPSIxNCIgZmlsbD0iI2U4ZjRmZiIvPjwvc3ZnPg==');
    }
    
    .bg-sparkles {
        background-color: #fffaff;
        background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZmZmYWZmIi8+PHBhdGggZD0iTTIwIDIwIEwxOCAxOCBMMjIgMTggTDIwIDE2IEwyMCAyMCBaIiBmaWxsPSIjZmZkN2ZmIi8+PHBhdGggZD0iTTUwIDMwIEw0OCAyOCBMNTIgMjggTDUwIDI2IEw1MCAzMCBaIiBmaWxsPSIjZmZkN2ZmIi8+PHBhdGggZD0iTTgwIDQwIEw3OCAzOCBMODIgMzggTDgwIDM2IEw4MCA0MCBaIiBmaWxsPSIjZmZkN2ZmIi8+PHBhdGggZD0iTTMwIDUwIEwyOCA0OCBMMzIgNDggTDMwIDQ2IEwzMCA1MCBaIiBmaWxsPSIjZmZkN2ZmIi8+PHBhdGggZD0iTTcwIDYwIEw2OCA1OCBMNzIgNTggTDcwIDU2IEw3MCA2MCBaIiBmaWxsPSIjZmZkN2ZmIi8+PHBhdGggZD0iTTQwIDcwIEwzOCA2OCBMNDIgNjggTDQwIDY2IEw0MCA3MCBaIiBmaWxsPSIjZmZkN2ZmIi8+PHBhdGggZD0iTTkwIDgwIEw4OCA3OCBMOTIgNzggTDkwIDc2IEw5MCA4MCBaIiBmaWxsPSIjZmZkN2ZmIi8+PHBhdGggZD0iTTYwIDkwIEw1OCA4OCBMNjIgODggTDYwIDg2IEw2MCA5MCBaIiBmaWxsPSIjZmZkN2ZmIi8+PC9zdmc+');
    }
    
    /* Avatar selection */
    .avatar-option {
        display: inline-block;
        margin: 5px;
        cursor: pointer;
        transition: all 0.2s ease;
        border-radius: 50%;
        overflow: hidden;
    }
    
    .avatar-option:hover {
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .avatar-selected {
        border: 3px solid #fd79a8;
        transform: scale(1.1);
    }
    
    /* Message area with background themes */
    .chat-container {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        min-height: 300px;
        max-height: 500px;
        overflow-y: auto;
    }

    /* Sticker and GIF panel */
    .sticker-panel {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        background: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 5px 15
