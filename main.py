import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from google.genai import types
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import Request

# Load environment variables
load_dotenv()

# System prompt for Gemini

system_prompt = """
You are an expert AI and modern tools recommender.

IMPORTANT: Always respond ONLY in valid JSON array format, no extra text or explanation.

JSON format to output:
[
  {
    "name": "Tool Name",
    "year": 2024,
    "strengths": "1-line strength",
    "website": "https://example.com"
  }
]

Rules:
1. Output 5–7 tools.
2. Always prioritise AI-first and cloud-based tools (2023-2025).
3. If no good AI tools exist, include simple non-AI tools and mark them with (Non-AI).
4. NEVER add any text, commentary, or markdown outside the JSON. """



# Request model
class ChatRequest(BaseModel):
    message: str

class RecommendRequest(BaseModel):
    query: str

# FastAPI app
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to ["http://localhost:8501"] if you want to restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint to fetch recommendations from Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY environment variable not set."}

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=request.message
    )
    return {"response": response.text}

@app.post("/recommend")
async def recommend_endpoint(request: RecommendRequest):
    """Recommend endpoint to fetch tool recommendations from Gemini and return as a list of tools."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY environment variable not set."}

    client = genai.Client(api_key=api_key)
    prompt = f"""{system_prompt}\n\nUser query: {request.query}\nRespond ONLY as a JSON list of tools, each with keys: name, year, strengths, website."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=prompt
    )
    print('Gemini raw response:', response.text)  # Debug print
    # Try to parse the response as JSON
    import json
    try:
        tools = json.loads(response.text)
        if not isinstance(tools, list):
            raise ValueError
    except Exception:
        # Fallback: return the raw text in a single tool
        tools = [{
            "name": "Could not parse Gemini response",
            "year": "N/A",
            "strengths": response.text,
            "website": "#"
        }]
    return {"tools": tools}

@app.get("/")
async def read_root():
    return {"message": "hello world"}
