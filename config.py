# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Reads GROQ_API_KEY from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise Exception("❌ GROQ_API_KEY missing! Add it to .env file.")

# Safe fallback models
MODEL_FALLBACKS = [
    "llama-3.3-70b-versatile",   # recommended by Groq
    "llama3-70b-8192",
    "llama3-8b-8192",
]
