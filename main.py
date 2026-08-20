from fastapi import Depends, FastAPI, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

import database
import models
import openai_service
import pricing
import schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Chat Service API")


@app.get("/", response_class=HTMLResponse)
async def get_chat_ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post(
    "/sessions",
    response_model=schemas.SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_session(
    req: schemas.CreateSessionRequest, db: Session = Depends(database.get_db)
):
    if req.model not in pricing.PRICING_CONFIG:
        return JSONResponse(
            status_code=400,
            content={
                "error": "INVALID_MODEL",
                "message": f"Модель '{req.model}' не підтримується.",
            },
        )
    new_session = models.Session(model=req.model)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


@app.post(
    "/sessions/{session_id}/messages", response_model=schemas.MessageResponse
)
def send_message(
    session_id: str,
    req: schemas.CreateMessageRequest,
    db: Session = Depends(database.get_db),
):
    session = (
        db.query(models.Session)
        .filter(models.Session.id == session_id)
        .first()
    )
    if not session:
        return JSONResponse(
            status_code=404,
            content={
                "error": "SESSION_NOT_FOUND",
                "message": f"Сесію з ідентифікатором '{session_id}' не знайдено.",
            },
        )

    history = (
        db.query(models.Message)
        .filter(models.Message.session_id == session_id)
        .order_by(models.Message.created_at.asc())
        .all()
    )

    formatted_messages = [
        {"role": msg.role, "content": msg.content} for msg in history
    ]
    formatted_messages.append({"role": "user", "content": req.content})

    try:
        ai_content, prompt_tokens, completion_tokens = (
            openai_service.generate_response(session.model, formatted_messages)
        )
    except Exception as e:
        print(f"\n[OPENROUTER ERROR]: {e}\n")
        return JSONResponse(
            status_code=502,
            content={"error": "EXTERNAL_API_ERROR", "message": str(e)},
        )

    cost = pricing.calculate_cost(
        session.model, prompt_tokens, completion_tokens
    )

    try:
        user_msg = models.Message(
            session_id=session_id, role="user", content=req.content
        )
        assistant_msg = models.Message(
            session_id=session_id, role="assistant", content=ai_content
        )

        db.add(user_msg)
        db.add(assistant_msg)

        session.total_prompt_tokens += prompt_tokens
        session.total_completion_tokens += completion_tokens
        session.total_cost_usd = round(session.total_cost_usd + cost, 6)

        db.commit()
        db.refresh(assistant_msg)
        return assistant_msg
    except Exception as err:
        db.rollback()
        print(f"\n[DATABASE ERROR]: {err}\n")
        return JSONResponse(
            status_code=500,
            content={
                "error": "DATABASE_ERROR",
                "message": "Помилка збереження даних у БД.",
            },
        )


@app.get(
    "/sessions/{session_id}", response_model=schemas.SessionDetailResponse
)
def get_session(session_id: str, db: Session = Depends(database.get_db)):
    session = (
        db.query(models.Session)
        .filter(models.Session.id == session_id)
        .first()
    )
    if not session:
        return JSONResponse(
            status_code=404,
            content={
                "error": "SESSION_NOT_FOUND",
                "message": f"Сесію з ідентифікатором '{session_id}' не знайдено.",
            },
        )
    return session