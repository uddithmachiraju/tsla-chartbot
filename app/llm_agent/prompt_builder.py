
def build_prompt(question: str, df_summary: dict) -> str:
    """
    Builds a prompt string incorporating summary data and user question
    """
    summary_text = "\n".join([f"{k}: {v}" for k,v in df_summary.items()])
    prompt = f"Given the TSLA stock data summary:\n{summary_text}\nAnswer this question:\n{question}"
    return prompt
