import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Page configuration
st.set_page_config(page_title="Data Science Tutor", page_icon="📊")
st.title("Data Science Tutor 📊")
st.subheader("Ask me about data science concepts, techniques, or tools!")

# Initialize session state for conversation history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# Configure the LLM
@st.cache_resource
def load_llm():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyDPqddRi-U9PM2p2ZIPappjnwVtjNSZDoM")
    return llm

# Configure the prompt template with data science focus and memory
system_prompt = """You are a helpful, conversational Data Science Tutor. Your purpose is to help users understand data science concepts, 
techniques, methodologies, and tools. Only answer questions related to data science.

If the user asks about topics unrelated to data science, politely guide them back to data science topics.

When explaining data science concepts:
- Break down complex ideas into simpler parts
- Provide examples when helpful
- Include Python code snippets when relevant
- Reference common libraries like pandas, numpy, scikit-learn, etc.
- Mention best practices and potential pitfalls

Always maintain a conversational, friendly tone while being informative and precise.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Create the conversation chain with memory
@st.cache_resource
def get_conversation_chain(_llm):
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(
        llm=_llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    return conversation

# Load LLM and create conversation chain
llm = load_llm()
conversation = get_conversation_chain(llm)

# Display chat history
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Chat input
if user_input := st.chat_input("Ask me about data science..."):
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=user_input))
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Update memory with the latest conversation
            for msg in st.session_state.messages:
                if isinstance(msg, HumanMessage):
                    st.session_state.memory.chat_memory.add_user_message(msg.content)
                else:
                    st.session_state.memory.chat_memory.add_ai_message(msg.content)
                    
            # Get response from LLM with memory context
            response = conversation.predict(input=user_input)
            
            # Display AI response
            st.markdown(response)
            
            # Add AI message to chat history
            st.session_state.messages.append(AIMessage(content=response))

# Sidebar with information
with st.sidebar:
    st.title("About Data Science Tutor")
    st.markdown("""
    This AI Data Science Tutor can help you with:
    
    - Data analysis and visualization
    - Machine learning algorithms
    - Statistical concepts
    - Data preprocessing techniques
    - Model evaluation
    - Python libraries for data science
    - Best practices in data science
    
    The tutor maintains conversation context to provide more relevant responses.
    """)
    
    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.memory.clear()
        st.experimental_rerun()
