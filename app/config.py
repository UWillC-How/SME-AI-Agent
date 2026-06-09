from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ปรับตรงนี้ให้ดึงค่าจากระบบตรง ๆ โดยไม่ต้องใส่ตัวอย่างหลอกไว้ในโค้ด
    SUPABASE_URL: str
    SUPABASE_KEY: str
    JWT_SECRET: str
    
    SUPABASE_SERVICE_ROLE_KEY: str | None = None

    # ดึงค่าโมเดลเสริม (ใส่ค่าเริ่มต้นดักไว้ให้)
    GEMINI_API_KEY: str | None = None
    LANGFUSE_PUBLIC_KEY: str | None = None
    LANGFUSE_SECRET_KEY: str | None = None
    LANGFUSE_BASE_URL: str = "https://cloud.langfuse.com"

    # บอกให้ Pydantic รู้ว่าให้ไปอ่านจากไฟล์ .env ในเครื่องได้ด้วยเวลาเทสโลคอล
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()