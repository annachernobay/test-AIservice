from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class CreateSessionRequest(BaseModel):
    model: str = Field(default="gpt-4o-mini", description="Назва моделі AI")


class SessionResponse(BaseModel):
    id: str
    model: str
    total_prompt_tokens: int
    total_completion_tokens: int
    total_cost_usd: float
    created_at: datetime

    class Config:
        from_attributes = True


class CreateMessageRequest(BaseModel):
    content: str = Field(..., min_length=1, description="Текст повідомлення користувача")


class MessageResponse(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class SessionDetailResponse(SessionResponse):
    messages: List[MessageResponse] = []