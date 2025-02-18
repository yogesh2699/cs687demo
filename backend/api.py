from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from pydantic import BaseModel
from src.agent import app as langgraph_app
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from typing import List, Dict, Any
import logging
import logging_config

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Agentic Customer Service API", description="API for interacting with the LangGraph-based agentic customer service.")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],  # Allow OPTIONS method for preflight requests
    allow_headers=["*"],
)

# Define a Pydantic model for the input request
class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_thread"

# Define a Pydantic model for the output response
class ChatResponse(BaseModel):
    response: str

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    try:
        # Stream the response from the LangGraph app
        response = ""
        for event in langgraph_app.stream(
            {"messages": [{"content": request.message, "type": "human"}]},
            config={"configurable": {"thread_id": request.thread_id}},
        ):
            if "agent" in event:
                msg = event["agent"]["messages"][-1].content
                if msg:
                    response = msg

        return {"response": response}
    except Exception as e:
        logger.error(f"Error in chat_with_agent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy"}