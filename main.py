from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agent import ManagedAgent

app = FastAPI()

agent = ManagedAgent("ollama:carstenuhlig/omnicoder-2-9b")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

class ChatMessage(BaseModel):
    message: str

@app.post("/chat", response_class=StreamingResponse)
async def chat(msg: ChatMessage) -> AsyncIterable[str]:
    yield agent.invoke(msg.message)
