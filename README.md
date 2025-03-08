# AI-Data-Science-Tutor

A Streamlit application powered by Google's Gemini 1.5 Pro model that serves as a conversational data science tutor. The application is designed to help users understand data science concepts, techniques, methodologies, and tools through an interactive chat interface.

## Features

- **Conversational Memory**: The application maintains conversation context using LangChain's ConversationBufferMemory
- **Data Science Focus**: Specialized in answering data science-related questions only
- **Friendly UI**: Clean Streamlit interface for easy interaction
- **Contextualized Responses**: Provides responses based on the entire conversation history

## Setup Instructions

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Replace `"YOUR_GOOGLE_API_KEY"` in the code with your actual Google API key
4. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Type your data science-related questions in the chat input
2. The AI tutor will respond with relevant explanations, examples, and code snippets when appropriate
3. The conversation history is maintained throughout the session
4. Use the "Clear Conversation" button in the sidebar to start a new conversation

## Example Questions

- "Can you explain what random forests are?"
- "How do I handle missing data in pandas?"
- "What's the difference between classification and regression?"
- "Explain the concept of overfitting and how to prevent it"
- "What Python libraries should I use for time series analysis?"

The tutor will only respond to data science-related questions and will politely guide users back to data science topics if asked about unrelated subjects.
