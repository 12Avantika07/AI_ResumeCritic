"""
Groq API Client for AI Resume Critic
Uses Groq's LLM API with retry logic, timeout handling, and fallback models.
"""

import os
import json
import re
import time
from dotenv import load_dotenv

# Load .env file BEFORE anything else
load_dotenv()

import streamlit as st
from groq import Groq

# Fallback models in order of preference
MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

# Config
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
TIMEOUT = 120    # seconds


def get_groq_client():
    """Initialize and return Groq client using secrets or env vars."""
    api_key = None
    try:
        api_key = st.secrets.get("GROQ_API_KEY", None)
    except Exception:
        pass
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", None)
    if not api_key:
        return None
    return Groq(api_key=api_key, timeout=TIMEOUT)


def call_groq(prompt: str, system_prompt: str, model: str = None) -> str:
    """
    Call Groq API with retry logic and fallback models.
    Retries on timeout, rate limit, and server errors.
    """
    client = get_groq_client()
    if client is None:
        raise ValueError(
            "Groq API key not found. Please set GROQ_API_KEY in your "
            ".env file or Streamlit secrets."
        )

    if model is None:
        model = MODELS[0]

    last_error = None

    for attempt in range(MAX_RETRIES):
        for current_model in (MODELS if attempt > 0 else [model]):
            try:
                response = client.chat.completions.create(
                    model=current_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=4096,
                    top_p=0.9,
                )
                return response.choices[0].message.content

            except Exception as e:
                error_str = str(e).lower()
                last_error = e

                # Don't retry on auth errors
                if "authentication" in error_str or "invalid api key" in error_str or "unauthorized" in error_str:
                    raise RuntimeError("Invalid Groq API key. Please check your GROQ_API_KEY.")

                # On timeout or rate limit, wait and retry
                if "timeout" in error_str or "timed out" in error_str or "rate" in error_str or "overloaded" in error_str or "503" in error_str or "500" in error_str:
                    wait = RETRY_DELAY * (attempt + 1)
                    time.sleep(wait)
                    continue

                # On model not found, skip to next model
                if "not found" in error_str or "decommissioned" in error_str or "does not exist" in error_str:
                    continue

                # Other errors — retry once more
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue

                break

    # All retries failed
    if last_error:
        error_msg = str(last_error)
        if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            raise RuntimeError(
                "⏰ Groq API is taking too long to respond. "
                "Please try again in a moment. "
                "Tip: If this happens often, try a shorter resume or job description."
            )
        elif "rate" in error_msg.lower():
            raise RuntimeError(
                "🚦 Groq API rate limit reached. "
                "Please wait 30 seconds and try again."
            )
        else:
            raise RuntimeError(
                f"⚠️ AI service error. Please try again. "
                f"(If the problem persists, Groq might be temporarily down)"
            )
    raise RuntimeError("⚠️ AI service error. Please try again.")


def call_groq_json(prompt: str, system_prompt: str, model: str = None) -> dict:
    """
    Call Groq API and parse response as JSON.
    Retries on parse failures with explicit JSON instruction.
    """
    raw_response = call_groq(prompt, system_prompt, model)

    # Try to extract JSON
    json_str = _extract_json(raw_response)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Retry with explicit JSON instruction
        retry_prompt = (
            prompt
            + "\n\nIMPORTANT: You MUST respond ONLY with valid JSON. "
            "No markdown, no explanation, just the JSON object."
        )
        raw_retry = call_groq(retry_prompt, system_prompt, model)
        json_str_retry = _extract_json(raw_retry)
        try:
            return json.loads(json_str_retry)
        except json.JSONDecodeError:
            # Last resort: try to fix common JSON issues
            try:
                fixed = json_str_retry.replace("'", '"').replace("\n", " ")
                return json.loads(fixed)
            except Exception:
                raise ValueError(
                    "AI returned an invalid response format. Please try again."
                )


def _extract_json(text: str) -> str:
    """Extract JSON from text, handling markdown code blocks and extra text."""
    json_patterns = [
        r'```(?:json)?\s*\n?(.*?)\n?\s*```',
        r'\{.*\}',
        r'\[.*\]',
    ]
    for pattern in json_patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip() if '```' in pattern else match.group(0).strip()
    return text.strip()


def check_api_key() -> bool:
    """Check if Groq API key is configured."""
    try:
        api_key = st.secrets.get("GROQ_API_KEY", None)
    except Exception:
        api_key = os.environ.get("GROQ_API_KEY", None)
    return api_key is not None and len(api_key.strip()) > 0
