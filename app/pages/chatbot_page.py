
import streamlit as st
from app.llm_agent.gemini_agent import GeminiAgent
from app.llm_agent.prompt_builder import build_prompt
from app.llm_agent.qa_templates import TEMPLATE_QUESTIONS
from app.core.data_loader import load_tsla_data
from app.core.indicators import count_bullish_days

def render():
    st.title("🤖 TSLA Chatbot")

    # Load data and create summary for prompt context
    df = load_tsla_data("data/tsla_data.csv")
    bullish_days = count_bullish_days(df)
    df_summary = {
        "Total bullish days": bullish_days,
        "Total data points": len(df),
        "Average Close Price": round(df['close'].mean(), 2),
    }

    api_key = st.text_input("Enter Gemini API Key:", type="password")
    user_question = st.text_input("Ask a question about TSLA stock data:")

    if st.button("Get Answer") and api_key and user_question:
        agent = GeminiAgent(api_key=api_key)
        prompt = build_prompt(user_question, df_summary)
        answer = agent.query(prompt)
        st.markdown(f"**Answer:** {answer}")

    with st.expander("Example questions"):
        for q in TEMPLATE_QUESTIONS:
            st.write(f"- {q}")
