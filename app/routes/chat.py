from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.dependencies import VerifyShop, Verify_jwt_token
from langfuse.callback import CallbackHandler  
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 🌟 1. นำเข้าไลบรารีของ Supabase และ Config มาใช้งาน
from supabase import create_client, Client
from app.config import settings

router = APIRouter(prefix="/chat", tags=["chat"])

# ประกาศตัวแปรเชื่อมต่อระบบภายนอกทั้งหมดไว้ด้านบน
langfuse_handler = CallbackHandler(
    public_key=settings.LANGFUSE_PUBLIC_KEY,
    secret_key=settings.LANGFUSE_SECRET_KEY,
    host=settings.LANGFUSE_BASE_URL,
)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
)

# 🌟 2. เปิดประตูล็อกอินฝั่ง Supabase Client
# ใส่ URL และ Key จริงจากเว็บ Supabase ของคุณลงไปดื้อๆ แบบนี้เลยครับ
supabase_client: Client = create_client(
    "https://mihtnzzfnzbaqivspicc.supabase.co/rest/v1/", 
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1paHRuenpmbnpiYXFpdnNwaWNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA4NzU5OTIsImV4cCI6MjA5NjQ1MTk5Mn0.Klcn7yYGeYzFDJKnwqeAcpmv3nzW7B3PeyrfX-OLoSA"
)
class chatRequest(BaseModel):
    message: str
    session_id: str | None = None

@router.post("/send-message")
async def chat_endpoint(
    payload: chatRequest,
    shop_id: str = Depends(VerifyShop),
    user_data: dict = Depends(Verify_jwt_token)
):
    # 1. สร้างโปรมต์และสั่ง AI คิดคำตอบตามปกติ
    prompt = ChatPromptTemplate.from_template("คุณคือผู้ช่วยร้านค้า SME จงตอบคำถามนี้อย่างสุภาพ: {question}")
    chain = prompt | llm

    response = chain.invoke(
        {"question": payload.message},
        config={
            "callbacks": [langfuse_handler],
            "run_name": f"SME_Chat_Shop_{shop_id}"  
        }
    )

    # 🌟 3. สั่งเซฟข้อมูลและ Status ลง Supabase ตาราง agent_logs ที่เราสร้างไว้
    try:
        supabase_client.table("agent_logs").insert({
            "shop_id": shop_id,
            "user_message": payload.message,
            "ai_reply": response.content,
            "status": "success" # บันทึกสถานะว่าทำงานสำเร็จ
        }).execute()
    except Exception as e:
        # ดักเผื่อเซฟไม่ผ่าน แอปจะได้ไม่ล่ม แต่พ่นเออร์เรอร์บอกเราใน Log แทน
        print(f"❌ Supabase Logging Error: {e}")

    return {"reply": response.content}