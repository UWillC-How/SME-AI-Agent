from fastapi import APIRouter, Request, status, BackgroundTasks
from langchain_google_genai import ChatGoogleGenerativeAI

# เพิ่มตัวนี้เข้าไปด้านบนของไฟล์ webhook.py ให้เหมือนใน chat.py
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.post("/line")
async def line_webhook(request: Request, background_tasks: BackgroundTasks):

    body = await request.body()
    signature = request.headers.get("X-Line-Signature")

    return {"status" : "ok"}
    