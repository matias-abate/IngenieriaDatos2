# app/routers/friends.py
from fastapi import APIRouter, Depends, Request, status
from app.repositories.friends_repo import FriendsRepo
from app.repositories.users_repo   import UsersRepo
from app.repositories.friends_graph_repo import FriendsGraphRepo  

router = APIRouter(prefix="/friends", tags=["friends"])

def repo(request: Request) -> FriendsRepo:
    return FriendsRepo(request.app.state.mongo)

def users_repo(request: Request) -> UsersRepo:
    return UsersRepo(request.app.state.mongo)

def graph_repo(request: Request) -> FriendsGraphRepo:
    return FriendsGraphRepo(request.app.state.neo)   # futuro

@router.post("/{uid}/{fid}", status_code=status.HTTP_201_CREATED)
async def add_friend(
    uid: str,
    fid: str,
    fr: FriendsRepo         = Depends(repo),
    ur: UsersRepo           = Depends(users_repo),
    gr: FriendsGraphRepo    = Depends(graph_repo)    # Neo4j inyectado aquí
):
    # 1) Verifico que ambos usuarios existan en MongoDB
    await ur.get(uid)
    await ur.get(fid)

    # 2) Agrego la amistad en MongoDB (almacén principal “relacional”)
    await fr.add(uid, fid)

    # 3) Agrego la relación bidireccional en Neo4j
    await gr.add(uid, fid)

    return {"detail": "ok"}


@router.delete("/{uid}/{fid}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_friend(
    uid: str,
    fid: str,
    fr: FriendsRepo         = Depends(repo),
    gr: FriendsGraphRepo    = Depends(graph_repo)
):
    # Elimino la relación en MongoDB
    await fr.remove(uid, fid)
    # Y la elimino bidireccionalmente en Neo4j
    await gr.remove(uid, fid)
    return


@router.get("/{uid}", response_model=list[str])
async def list_friends(uid: str, fr: FriendsRepo = Depends(repo)):
    return await fr.list(uid)

@router.get("/suggestions/{uid}", response_model=list[str])
async def suggestions(uid: str,
                      gr: FriendsGraphRepo = Depends(graph_repo)):
    return await gr.suggestions(uid)

