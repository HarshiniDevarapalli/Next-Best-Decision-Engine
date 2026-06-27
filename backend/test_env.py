from dotenv import load_dotenv
import os

loaded = load_dotenv()

print("Loaded:", loaded)
print("Key:", os.getenv("GEMINI_API_KEY"))
print("Model:", os.getenv("LLM_MODEL"))