# app/repositories/friends_graph_repo.py
class FriendsGraphRepo:
    """
    Envuelve el driver de Neo4j para manejar relaciones de amistad
    y sugerencias de amigos de amigos.
    """
    def __init__(self, driver):
        self.driver = driver

    # ── Crear relación bidireccional ──────────────────────────────
    async def add(self, uid: str, fid: str):
        cypher = """
        MERGE (u1:User {id:$u1})
        MERGE (u2:User {id:$u2})
        MERGE (u1)-[:FRIENDS_WITH]->(u2)
        MERGE (u2)-[:FRIENDS_WITH]->(u1)
        """
        async with self.driver.session() as s:
            await s.run(cypher, u1=uid, u2=fid)

    # ── Eliminar relación bidireccional ───────────────────────────
    async def remove(self, uid: str, fid: str):
        cypher = """
        MATCH (a:User {id:$u1})-[r:FRIENDS_WITH]->(b:User {id:$u2}) DELETE r
        """
        async with self.driver.session() as s:
            await s.run(cypher, u1=uid, u2=fid)
            await s.run(cypher, u1=fid, u2=uid)

    # ── Sugerencias de amigos de amigos ───────────────────────────
    async def suggestions(self, uid: str, limit: int = 10) -> list[str]:
        cypher = """
        MATCH (me:User {id:$uid})-[:FRIENDS_WITH]->(:User)-[:FRIENDS_WITH]->(fof)
        WHERE NOT (me)-[:FRIENDS_WITH]->(fof) AND me <> fof
        RETURN DISTINCT fof.id AS id
        LIMIT $limit
        """
        async with self.driver.session() as s:
            result = await s.run(cypher, uid=uid, limit=limit)
            return [rec["id"] async for rec in result]
