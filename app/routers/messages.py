# app/routers/messages.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models import Message
from app.repositories.messages_repo import MessagesRepo
from app.repositories.users_repo import UsersRepo

router = APIRouter(prefix="/messages", tags=["messages"])

def get_messages_repo(request: Request) -> MessagesRepo:
    return MessagesRepo(request.app.state.mongo)

def get_users_repo(request: Request) -> UsersRepo:
    return UsersRepo(request.app.state.mongo)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=Message)
async def send_message(
    msg: Message,
    repo: MessagesRepo = Depends(get_messages_repo),
    users_repo: UsersRepo = Depends(get_users_repo)
):
    """
    Envía un mensaje de sender_id a receiver_id y lo guarda en MongoDB.
    Body JSON debe incluir: { "sender_id": "<oid>", "receiver_id": "<oid>", "content": "..." }
    Retorna el Message guardado.
    """
    # 1) Validar que ambos usuarios existan en MongoDB
    try:
        await users_repo.get(str(msg.sender_id))
        await users_repo.get(str(msg.receiver_id))
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 2) Guardar el mensaje
    sent_msg = await repo.send(msg)
    return sent_msg

@router.get("/inbox/{user_id}", response_model=List[Message])
async def list_inbox(
    user_id: str,
    skip: int = 0,
    limit: int = 50,
    repo: MessagesRepo = Depends(get_messages_repo),
    users_repo: UsersRepo = Depends(get_users_repo)
):
    """
    Obtiene los mensajes recibidos por user_id. 
    Parámetros query: skip (número a saltar), limit (límite).
    """
    # 1) Verificar existencia de user_id
    try:
        await users_repo.get(user_id)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 2) Devolver los mensajes de la bandeja de entrada
    return await repo.list_inbox(user_id, skip, limit)

@router.get("/sent/{user_id}", response_model=List[Message])
async def list_sent(
    user_id: str,
    skip: int = 0,
    limit: int = 50,
    repo: MessagesRepo = Depends(get_messages_repo),
    users_repo: UsersRepo = Depends(get_users_repo)
):
    """
    Obtiene los mensajes enviados por user_id.
    Parámetros: skip, limit.
    """
    # 1) Verificar existencia de user_id
    try:
        await users_repo.get(user_id)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 2) Devolver los mensajes enviados
    return await repo.list_sent(user_id, skip, limit)

@router.get("/conversation/{user_a}/{user_b}", response_model=List[Message])
async def get_conversation(
    user_a: str,
    user_b: str,
    skip: int = 0,
    limit: int = 50,
    repo: MessagesRepo = Depends(get_messages_repo),
    users_repo: UsersRepo = Depends(get_users_repo)
):
    """
    Obtiene el histórico de mensajes entre user_a y user_b (bidireccional).
    Parámetros: skip, limit.
    """
    # 1) Verificar existencia de ambos usuarios
    try:
        await users_repo.get(user_a)
        await users_repo.get(user_b)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 2) Devolver la conversación
    return await repo.get_conversation(user_a, user_b, skip, limit)

@router.delete("/{msg_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    msg_id: str,
    repo: MessagesRepo = Depends(get_messages_repo)
):
    """
    Elimina el mensaje con id msg_id (si existe) en MongoDB.
    """
    await repo.delete(msg_id)
    return
