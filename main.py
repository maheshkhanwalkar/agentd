from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

class ChatMessage(BaseModel):
    message: str

@app.post("/chat", response_class=StreamingResponse)
async def chat(msg: ChatMessage) -> AsyncIterable[str]:
    # TODO implement the functionality
    yield msg.message
    yield "\n"
    yield msg.message
