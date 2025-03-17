import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

def get_api_keys():
    """Retrieve API keys from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    weather_api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        st.error("GOOGLE_API_KEY is missing. Please check your .env file.")
    if not weather_api_key:
        st.error("OPENWEATHER_API_KEY is missing. Please check your .env file.")
    
    return api_key, weather_api_key

def setup_llm(api_key):
    """Initialize the ChatGoogleGenerativeAI model with the API key."""
    if api_key:
        return ChatGoogleGenerativeAI(api_key=api_key)
    else:
        return None

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="AI Chat App", layout="wide")
    
    # Apply custom CSS for sidebar
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #f4f4f4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("AI-Powered Chat Application")
    
    # Get API keys
    api_key, weather_api_key = get_api_keys()
    
    # Initialize LLM model
    llm = setup_llm(api_key)
    
    if llm:
        st.success("LLM model initialized successfully!")
    else:
        st.warning("LLM model could not be initialized. Check API key.")
    
    # Chat Input
    user_input = st.text_input("Ask me something:")
    
    if st.button("Send") and user_input:
        response = llm.invoke(user_input) if llm else "Model is not initialized."
        st.write("Response:", response)
    
if __name__ == "__main__":
    main()
