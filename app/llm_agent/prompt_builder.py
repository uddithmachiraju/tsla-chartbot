def build_prompt(user_question, summary_dict):
    summary_lines = [f"{k}: {v}" for k, v in summary_dict.items()]
    summary_text = "\n".join(summary_lines)
    return f"""
        You are a financial analyst chatbot for Tesla (TSLA) stock data.

        Here's a summary of the stock data:
        {summary_text}

        Now answer the following user question in a helpful and concise manner:
        {user_question}
    """.strip()
