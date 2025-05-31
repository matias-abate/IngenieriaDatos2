# app/repositories/friends_graph_repo.py
class FriendsGraphRepo:
    def __init__(self, driver):
        self.driver = driver

    async def add(self, uid: str, fid: str):
        q = """
        MERGE (u1:User {id:$u1})
        MERGE (u2:User {id:$u2})
        MERGE (u1)-[:FRIENDS_WITH]->(u2)
        MERGE (u2)-[:FRIENDS_WITH]->(u1)
        """
        async with self.driver.session() as s:
            await s.run(q, u1=uid, u2=fid)

    async def remove(self, uid: str, fid: str):
        q = """
        MATCH (a:User {id:$u1})-[r:FRIENDS_WITH]->(b:User {id:$u2}) DELETE r
        """
        async with self.driver.session() as s:
            await s.run(q, u1=uid, u2=fid)
            await s.run(q, u1=fid, u2=uid)
