from fastapi import APIRouter, Request, status, BackgroundTasks
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

# เพิ่มตัวนี้เข้าไปด้านบนของไฟล์ webhook.py ให้เหมือนใน chat.py
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
)

router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.post("/line")
async def line_webhook(request: Request, background_tasks: BackgroundTasks):

    body = await request.body()
    signature = request.headers.get("X-Line-Signature")

    return {"status" : "ok"}
    