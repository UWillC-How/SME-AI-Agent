from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.dependencies import VerifyShop, Verify_jwt_token

router = APIRouter(prefix="/chat", tags=["chat"])

class chatRequest(BaseModel):
    message: str
    session_id: str | None = None

@router.post("/chat")
async def chat_endpoint(
    payload: chatRequest,
    shop_id: str = Depends(VerifyShop),
    auth_payload: dict = Depends(Verify_jwt_token)
):
    return {"shop id": shop_id,
            "reply": f"message received: {payload.message} in session {payload.session_id}",
            "status": "processing"
            }