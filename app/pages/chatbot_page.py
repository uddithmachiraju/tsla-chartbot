import streamlit as st
from app.llm_agent.gemini_agent import GeminiAgent
from app.llm_agent.prompt_builder import build_prompt
from app.llm_agent.qa_templates import TEMPLATE_QUESTIONS
from app.core.summary import summarize_data  # NEW
from data.config import data
from dotenv import load_dotenv
import os

load_dotenv()

def render():
    st.title("🤖 TSLA Chatbot")

    # Load .env API key
    load_dotenv()
    api_key = os.getenv("API_KEY")

    # Summarize list data
    df_summary = summarize_data(data)

    user_question = st.text_input("Ask a question about TSLA stock data:")

    if st.button("Get Answer") and api_key and user_question:
        agent = GeminiAgent(api_key=api_key)
        prompt = build_prompt(user_question, df_summary)
        answer = agent.query(prompt)
        st.markdown(f"**Answer:** {answer}")

    with st.expander("Example questions"):
        for q in TEMPLATE_QUESTIONS:
            st.write(f"- {q}")
