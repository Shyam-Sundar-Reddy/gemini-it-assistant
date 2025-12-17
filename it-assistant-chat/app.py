import os
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------------------------------------------
# Load env
# ---------------------------------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "it-assistant-chat"

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found in .env")
    st.stop()

# ---------------------------------------------------
# UI
# ---------------------------------------------------
st.set_page_config(page_title="IT Assistant Chat", layout="centered")

st.title("💬 IT Assistant Chat")
st.caption("A simple, useful chat assistant for developers & IT teams")

st.markdown("""
You can ask about:
- Programming concepts
- DevOps basics
- System design fundamentals
- Cloud & networking
- Debugging tips
""")

# Chat input
user_input = st.text_input("Ask your IT or developer question")

# ---------------------------------------------------
# Prompt
# ---------------------------------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful IT and software engineering assistant.
Explain concepts clearly and practically.
Keep answers concise and useful for developers."""
    ),
    ("user", "{question}")
])

# ---------------------------------------------------
# LLM
# ---------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.6,
    google_api_key=GOOGLE_API_KEY
)

chain = prompt | llm | StrOutputParser()

# ---------------------------------------------------
# Run
# ---------------------------------------------------
if user_input:
    with st.spinner("Thinking..."):
        response = chain.invoke({"question": user_input})
        st.markdown("### 🤖 Response")
        st.write(response)
