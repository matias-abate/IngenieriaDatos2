# app/routers/messages.py
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.models import Message
from app.storage import messages, users

router = APIRouter(prefix="/messages", tags=["messages"])


# ---------- Helpers internos ----------
def _check_user_exists(user_id: str) -> None:
    if user_id not in users:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")


# ---------- Endpoints ----------
@router.post("", status_code=status.HTTP_201_CREATED, response_model=Message)
def send_message(msg: Message):
    """
    Crea y guarda un mensaje `msg` en la “base” in-memory.
    El cliente debe enviar `sender_id`, `receiver_id` y `body`.
    """
    _check_user_exists(msg.sender_id)
    _check_user_exists(msg.receiver_id)

    messages[msg.id] = msg
    return msg


@router.get("/inbox/{user_id}", response_model=List[Message])
def list_inbox(user_id: str):
    """Mensajes recibidos por `user_id` (orden cronológico asc)."""
    _check_user_exists(user_id)
    return sorted(
        (m for m in messages.values() if m.receiver_id == user_id),
        key=lambda m: m.sent_at,
    )


@router.get("/sent/{user_id}", response_model=List[Message])
def list_sent(user_id: str):
    """Mensajes enviados por `user_id`."""
    _check_user_exists(user_id)
    return sorted(
        (m for m in messages.values() if m.sender_id == user_id),
        key=lambda m: m.sent_at,
    )


@router.get("/conversation/{user_a}/{user_b}", response_model=List[Message])
def conversation(user_a: str, user_b: str):
    """
    Devuelve el chat entre `user_a` y `user_b`, combinando ida y vuelta.
    """
    _check_user_exists(user_a)
    _check_user_exists(user_b)

    return sorted(
        (
            m
            for m in messages.values()
            if {m.sender_id, m.receiver_id} == {user_a, user_b}
        ),
        key=lambda m: m.sent_at,
    )


@router.delete("/{msg_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(msg_id: str):
    """
    Elimina (si existe) el mensaje con id `msg_id`.
    """
    messages.pop(msg_id, None)
