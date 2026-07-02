from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.models import ChatRequest, ChatResponse
from app.chat import chat

app = FastAPI(title="SHL Assessment Recommendation Agent API")

# CORS configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chatbot(request: ChatRequest):
    result = chat(
        [m.model_dump() for m in request.messages]
    )
    return result