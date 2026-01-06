import streamlit as st
import requests
import subprocess
import shlex
import json

# Simple Streamlit + Ollama demo chatbot
# Requirements:
# - Ollama running locally (https://ollama.ai/) OR ollama CLI installed
# - Python packages: streamlit, requests
# - Optional: langchain for deeper integration
# Install with: pip install streamlit requests langchain
# Install ollama on Windows with: 
# cmd: winget install Ollama.Ollama --source winget
# Set ollama app path if needed in windows system environment variables
# e.g. C:\Users\Admin\AppData\Local\Programs\Ollama\Ollama.exe
# close all powershell and reopen and check ollama version in cmd/powershell to confirm
# cmd: ollama --version
# should return the installed version,then start ollama server with:
# cmd: ollama serve
# Validate the server is running by visiting:
# http://localhost:11434/ in your browser
# pull model in terminal/cmd:
# cmd: ollama pull llama2
# anouther model example: mistral
# cmd: ollama pull mistral

OLLAMA_HTTP_URL = "http://localhost:11434/api/generate"


def call_ollama_http(prompt: str, model: str = "llama2", max_tokens: int = 512, temperature: float = 0.7) -> str:
    """Try to call a local Ollama HTTP API. Returns generated text on success, otherwise raises."""
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    try:
        r = requests.post(OLLAMA_HTTP_URL, json=payload, timeout=10)
        r.raise_for_status()
        # Ollama's HTTP response format can vary; try to extract common fields
        try:
            data = r.json()
            # Many endpoints return a top-level 'text' or 'output' or 'content'
            for key in ("text", "output", "content", "result"):
                if key in data:
                    return data[key]
            # try to find nested choices
            if isinstance(data, dict) and "choices" in data and data["choices"]:
                first = data["choices"][0]
                if isinstance(first, dict) and "text" in first:
                    return first["text"]
            # sometimes Ollama returns a single object with a 'response' field
            if isinstance(data, dict) and "response" in data:
                return data["response"]
            # fallback to raw text
            return r.text
        except ValueError:
            # Response may be a stream / NDJSON (multiple JSON objects concatenated).
            text = r.text
            try:
                import re
                parts = re.split(r'}\s*{', text)
                if len(parts) > 1:
                    objs = []
                    for i, p in enumerate(parts):
                        if i > 0:
                            p = '{' + p
                        if i < len(parts) - 1:
                            p = p + '}'
                        try:
                            objs.append(json.loads(p))
                        except Exception:
                            # skip parts that don't parse
                            continue
                    pieces = []
                    for o in objs:
                        if isinstance(o, dict):
                            # Ollama streaming chunks commonly use 'response'
                            for key in ("response", "text", "output", "content"):
                                if key in o and isinstance(o[key], str):
                                    pieces.append(o[key])
                                    break
                    if pieces:
                        return ''.join(pieces)
            except Exception:
                pass
            return text
    except Exception as exc:
        raise RuntimeError(f"HTTP call to Ollama failed: {exc}")


def call_ollama_cli(prompt: str, model: str = "llama2", max_tokens: int = 512, temperature: float = 0.7) -> str:
    """Fallback: call ollama via CLI. Requires 'ollama' to be on PATH and a model available.
    This tries to call: ollama generate <model> --prompt "..."
    """
    try:
        cmd = f"ollama generate {shlex.quote(model)} --temperature {temperature} --max-tokens {max_tokens} --prompt"
        # Use subprocess to send prompt through stdin for safety
        process = subprocess.run(shlex.split(cmd), input=prompt, text=True, capture_output=True, timeout=30)
        if process.returncode != 0:
            raise RuntimeError(process.stderr.strip() or "ollama CLI returned non-zero exit code")
        return process.stdout.strip()
    except FileNotFoundError:
        raise RuntimeError("ollama CLI not found on PATH. Please install ollama or run the Ollama server.")
    except Exception as exc:
        raise RuntimeError(f"ollama CLI invocation failed: {exc}")


def generate_response(prompt: str, model: str, max_tokens: int, temperature: float) -> str:
    """Try HTTP first, then CLI. Return best-effort response or a helpful error message."""
    # Try HTTP API
    try:
        return call_ollama_http(prompt, model=model, max_tokens=max_tokens, temperature=temperature)
    except Exception:
        # try CLI
        try:
            return call_ollama_cli(prompt, model=model, max_tokens=max_tokens, temperature=temperature)
        except Exception as exc:
            return f"Error generating response: {exc}\n\nMake sure Ollama is running (HTTP API) or ollama CLI is installed and a model is available.\nSee: https://ollama.ai/"


# LangChain integration removed for this simple demo; this script uses the
# Ollama `llama2` model directly via HTTP or the CLI.


# Streamlit UI
st.set_page_config(page_title="Ollama Demo Chatbot", layout="wide")
st.title("Ollama Demo Chatbot (Streamlit)")

with st.sidebar:
    st.header("Settings")
    st.write("Select model (must be pulled locally)")
    model = st.radio("Model", options=("llama2", "mistral"), index=0)
    max_tokens = st.slider("Max tokens", min_value=64, max_value=2048, value=512)
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)

if "messages" not in st.session_state:
    st.session_state.messages = []  # list of (role, text)

col1, col2 = st.columns([3, 1])

with col1:
    for role, text in st.session_state.messages:
        if role == "user":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**Bot:** {text}")

    user_input = st.text_area("Message", height=120)
    send = st.button("Send")

with col2:
    st.write("### Info")
    st.write(f"This demo calls the Ollama `{model}` model via HTTP at http://localhost:11434/api/generate.\nIf that fails it will try the `ollama` CLI on PATH.")

if send and user_input:
    st.session_state.messages.append(("user", user_input))
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("**Bot:** _Thinking..._")

    # Build a simple system prompt + conversation context
    conversation = ""
    for role, text in st.session_state.messages:
        conversation += f"{role}: {text}\n"
    prompt = f"The following is a conversation between a helpful assistant and a user.\n{conversation}\nAssistant:" 

    resp = generate_response(prompt, model=model, max_tokens=max_tokens, temperature=temperature)

    st.session_state.messages.append(("bot", resp))
    placeholder.empty()
    st.rerun()


# Dependency summary printed at bottom
st.sidebar.markdown("---")
st.sidebar.markdown("### Dependencies")
st.sidebar.markdown("- streamlit\n- requests\n- Ollama: the Ollama local server (HTTP API) or the `ollama` CLI must be installed and the `llama2` model pulled (see https://ollama.ai/)")
