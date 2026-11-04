
# NEXUS AI - Intelligent Query Router

def classify_query(message):

    message = message.lower()

    # Calculator Intent
    calculator_keywords = [
        "calculate", "multiply", "divide",
        "addition", "subtract", "square",
        "plus", "minus"
    ]

    if any(word in message for word in calculator_keywords):
        return "CALCULATOR"

    # Weather Forecast Intent
    forecast_keywords = [
        "forecast",
        "tomorrow",
        "next 7 days",
        "next week",
        "upcoming weather",
        "weather this week",
        "weather prediction"
    ]

    if any(word in message for word in forecast_keywords):
        return "WEATHER_FORECAST"

    # Current Weather Intent
    weather_keywords = [
        "weather",
        "temperature",
        "rain",
        "climate",
        "currently",
        "right now"
    ]

    if any(word in message for word in weather_keywords):
        return "WEATHER"

    # Document / RAG Intent
    document_keywords = [
        "pdf", "document", "uploaded file",
        "summarize this file", "according to the document"
    ]

    if any(word in message for word in document_keywords):
        return "DOCUMENT_QUERY"

    # Memory Intent
    memory_keywords = [
        "remember", "my name",
        "what did i tell you",
        "previous conversation"
    ]

    if any(word in message for word in memory_keywords):
        return "MEMORY"

    # Default Intent
    return "GENERAL_QUERY"
