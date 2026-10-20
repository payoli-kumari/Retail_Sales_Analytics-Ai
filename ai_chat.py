"""AI Feature 1 + 3: 'Ask the Data' (text-to-pandas) and 'Auto Insights'."""
import pandas as pd
from llm import chat

# Words that must not appear in AI-generated code (basic safety check)
BANNED = ["import", "open(", "os.", "sys.", "eval", "exec", "__",
          "subprocess", "input(", "globals", "locals"]

# Only these harmless built-in functions are allowed inside the generated code
SAFE_BUILTINS = {"len": len, "round": round, "sorted": sorted, "min": min,
                 "max": max, "sum": sum, "abs": abs, "list": list,
                 "dict": dict, "str": str, "int": int, "float": float,
                 "range": range, "enumerate": enumerate, "zip": zip}


def _schema(df: pd.DataFrame) -> str:
    """Describe the data to the AI: column names, types and 3 sample rows."""
    cols = "\n".join(f"- {c} ({t})" for c, t in df.dtypes.astype(str).items())
    return f"Columns:\n{cols}\n\nSample rows:\n{df.head(3).to_string()}"


def ask_data(question: str, df: pd.DataFrame):
    """Returns (explanation, code, result)."""
    system = (
        "You are a data analyst. A pandas DataFrame named df is already loaded.\n"
        + _schema(df) + "\n\nRules: reply with ONLY python code, no markdown, "
        "no explanation. Use only pandas (pd) and df. "
        "Store the final answer in a variable named result. "
        "Never import anything, never read/write files, never use network."
    )
    # 1) Ask the AI to write pandas code, then strip markdown fences if present
    code = chat(system, question).replace("```python", "").replace("```", "").strip()

    # 2) Safety check before running anything
    if any(b in code for b in BANNED):
        return "Safety check fail hua, sawal dusre tareeke se poochho.", code, None

    # 3) Run the code on a copy of the data with limited built-ins
    scope = {"__builtins__": SAFE_BUILTINS, "df": df.copy(), "pd": pd}
    try:
        exec(code, scope)
        result = scope.get("result")
    except Exception as e:
        return f"Code run nahi hua: {e}", code, None

    # 4) Ask the AI to explain the result in simple words
    explain = chat(
        "You explain data results simply.",
        f"Question: {question}\nResult:\n{result}\n"
        "Explain in 2-3 simple lines, same language as the question.")
    return explain, code, result


def auto_insights(summary: str) -> str:
    """summary = text with the dashboard's filtered numbers."""
    return chat(
        "You are a senior retail data analyst. Use ONLY the numbers given. "
        "Do not invent numbers.",
        f"Data summary:\n{summary}\n\nGive 5 key insights and 3 business "
        "recommendations in simple Hinglish bullet points.",
        max_tokens=2500)