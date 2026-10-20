"""Call any AI provider from one place. Switching provider = changing .env only."""
import os

try:  # read keys from the .env file
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()  # groq | gemini | claude | ollama
MODEL = os.getenv("LLM_MODEL", "")  # optional: override the model name

DEFAULT_MODELS = {  # names can become outdated; if you get an error, set LLM_MODEL in .env
    "groq": "openai/gpt-oss-20b",
    "gemini": "gemini-2.5-flash",
    "claude": "claude-sonnet-5-5",
    "ollama": "qwen2.5:7b",
}

# Force English output and no currency symbols for every AI call
LANGUAGE_RULE = (
    "\n\nIMPORTANT: Reply in English only. Never use Hindi, Devanagari or Hinglish. "
    "Never add currency symbols; the dataset has no currency."
)


def chat(system: str, user: str, max_tokens: int = 2000) -> str:
    system = system + LANGUAGE_RULE  # apply the rule to every AI call
    model = MODEL or DEFAULT_MODELS[PROVIDER]
    messages = [{"role": "system", "content": system},
                {"role": "user", "content": user}]

    if PROVIDER == "ollama":  # runs on your laptop: free, no limits
        from openai import OpenAI
        client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
        r = client.chat.completions.create(
            model=model, max_tokens=max_tokens, temperature=0, messages=messages)
        return r.choices[0].message.content or ""

    if PROVIDER == "groq":  # free tier (has rate limits), OpenAI-compatible
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("GROQ_API_KEY"),
                        base_url="https://api.groq.com/openai/v1")
        r = client.chat.completions.create(
            model=model, max_tokens=max_tokens, temperature=0, messages=messages)
        return r.choices[0].message.content or ""

    if PROVIDER == "gemini":  # free tier (has rate limits)
        from google import genai
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        r = client.models.generate_content(
            model=model, contents=user,
            config={"system_instruction": system, "temperature": 0})
        return r.text

    if PROVIDER == "claude":  # paid
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        r = client.messages.create(
            model=model, max_tokens=max_tokens, system=system,
            messages=[{"role": "user", "content": user}])
        return r.content[0].text

    raise ValueError("LLM_PROVIDER must be one of: groq, gemini, claude, ollama")