Iniciar el proyecto 
uvicorn app.main:app --reload

Iniciar MongoDB
brew services start mongodb-community
mongosh
use mini_social
db.users.find().limit(5)
CRTL + D -> Stop service


Iniciar Neo4j
neo4j start


Ver datos en MongoDB
mongosh
# dentro de mongosh:
use mini_social
db.users.find().limit(10)
db.posts.find().limit(10)
db.messages.find().limit(10)


Ver datos en Neo4j
cypher-shell -u neo4j -p 12345678
# luego, por ejemplo:
MATCH (n) RETURN n LIMIT 25;


Limpiar datos en MongoDB
mongosh
use mini_social
db.users.deleteMany({})
db.posts.deleteMany({})
db.messages.deleteMany({})

Limpiar datos en Neo4j
cypher-shell -u neo4j -p 12345678
MATCH (n) DETACH DELETE n;


trar nickname de ussers
