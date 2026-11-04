
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os
import time

from router import classify_query
from calculator import calculate_from_query
from weather import get_weather, get_weather_forecast, extract_city


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# INITIALIZE FASTAPI
# ==========================================

app = FastAPI(
    title="NEXUS AI",
    description="Intelligent AI Personal Assistant",
    version="1.0.0"
)


# ==========================================
# INITIALIZE GEMINI
# ==========================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


# ==========================================
# SHORT-TERM MEMORY
# ==========================================

chat_history = {}


# ==========================================
# REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


# ==========================================
# HOME ROUTE
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Welcome to NEXUS AI",
        "status": "Running"
    }


# ==========================================
# HEALTH ROUTE
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ==========================================
# CHAT ROUTE
# ==========================================

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        start_time = time.time()

        # ----------------------------------
        # IDENTIFY USER INTENT
        # ----------------------------------

        intent = classify_query(request.message)

        session_id = request.session_id

        # ----------------------------------
        # GET PREVIOUS CONVERSATION
        # ----------------------------------

        if session_id not in chat_history:
            chat_history[session_id] = []

        history = chat_history[session_id]

        # ----------------------------------
        # CREATE CONVERSATION CONTEXT
        # ----------------------------------

        conversation = ""

        for item in history:

            conversation += f"User: {item['user']}\n"
            conversation += f"Assistant: {item['assistant']}\n"

        conversation += f"User: {request.message}\n"
        conversation += "Assistant:"

        print("CONVERSATION CONTEXT:", conversation)

        # ----------------------------------
        # INTELLIGENT TOOL SELECTION
        # ----------------------------------

        if intent == "CALCULATOR":

            answer = calculate_from_query(request.message)

        elif intent == "WEATHER":

            city = extract_city(request.message)

            if city:

                answer = get_weather(city)

            else:

                answer = "Please specify a city name."
        elif intent == "WEATHER_FORECAST":

            city = extract_city(request.message)

            if city:
                   answer = get_weather_forecast(city)
            else:
                answer = "Please specify a city name for the weather forecast."

        else:

            interaction = client.interactions.create(
                model="gemini-3.5-flash",
                input=conversation
            )

            answer = interaction.output_text

        # ----------------------------------
        # SAVE CONVERSATION IN MEMORY
        # ----------------------------------

        history.append({
            "user": request.message,
            "assistant": answer
        })

        # Keep only last 10 conversation turns
        chat_history[session_id] = history[-10:]

        print("SAVED MEMORY:", chat_history)

        # ----------------------------------
        # EXECUTION TIME
        # ----------------------------------

        execution_time = round(time.time() - start_time, 2)

        print("Execution Time:", execution_time, "seconds")

        # ----------------------------------
        # RETURN RESPONSE
        # ----------------------------------

        return {
            "question": request.message,
            "answer": answer,
            "intent": intent,
            "memory": "enabled",
            "execution_time": execution_time,
            "session_id": session_id
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
