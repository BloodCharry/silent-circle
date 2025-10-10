from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_session

router = APIRouter()


@router.get("/me")
async def get_current_user(session: AsyncSession = Depends(get_session)):
    # TODO: вернуть текущего пользователя
    return {"user": "placeholder"}
