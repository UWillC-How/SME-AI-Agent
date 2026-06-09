from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.dependencies import VerifyShop, Verify_jwt_token
from langfuse.callback import CallbackHandler  # นำเข้าตัวจับตาดูของ Langfuse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

router = APIRouter(prefix="/chat", tags=["chat"])

langfuse_handler = CallbackHandler()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class chatRequest(BaseModel):
    message: str
    session_id: str | None = None

@router.post("/send-message")
async def chat_endpoint(
    payload: chatRequest,
    shop_id: str = Depends(VerifyShop),
    user_data: dict = Depends(Verify_jwt_token)
):
    # 1. สร้างโปรมต์ (Prompt)
    prompt = ChatPromptTemplate.from_template("คุณคือผู้ช่วยร้านค้า SME จงตอบคำถามนี้อย่างสุภาพ: {question}")
    chain = prompt | llm

    # 2. สั่งรัน AI พร้อมแนบ Langfuse Callbacks ไปด้วย 🌟
    # เราสามารถตั้งชื่อโปรเจกต์แชท (trace_name) เพื่อให้ไปแยกดูในเว็บได้ง่ายขึ้น
    response = chain.invoke(
        {"question": payload.message},
        config={
            "callbacks": [langfuse_handler],
            "run_name": f"SME_Chat_Shop_{shop_id}"  # ตั้งชื่อให้รู้ว่าเป็นของร้านไหน
        }
    )

    return {"reply": response.content}

