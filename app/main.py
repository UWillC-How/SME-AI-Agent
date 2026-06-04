from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, webhook

app = FastAPI(title="SME AGENT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.get("/health")
async def health():
    return {"status": "ok"}