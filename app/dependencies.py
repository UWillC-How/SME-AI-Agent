from typing import Annotated
from fastapi import Header, HTTPException, Depends
from jose import JWTError, jwt
from app.config import settings

async def VerifyShop(x_shop_id: Annotated[str | None, Header(alias="X-Shop-ID")]= None):

    if not x_shop_id:
        raise HTTPException(status_code=400, detail="X-Shop-ID header is required")
    
    return x_shop_id

async def Verify_jwt_token(authorization: Annotated[str | None, Header(alias = "Authorization")]= None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is required")
    
    try:
        token_type, token = authorization.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

        return payload
    except (ValueError, JWTError):
        raise HTTPException(status_code=401, detail="Invalid token")