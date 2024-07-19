from pymongo import MongoClient
from neo4j import GraphDatabase

class MongoDB:
    def __init__(self, uri, dbname):
        self.client = MongoClient(uri)
        self.db = self.client[dbname]

    def get_people(self):
        return list(self.db.people.find())

    def get_relationships(self):
        return list(self.db.relationships.find())

class Neo4jDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_person(self, name, age, occupation):
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_person, name, age, occupation)
            print(f"Created person in Neo4j: {name}, {age}, {occupation}")

    @staticmethod
    def _create_and_return_person(tx, name, age, occupation):
        query = (
            "CREATE (p:Person {name: $name, age: $age, occupation: $occupation}) "
            "RETURN p"
        )
        result = tx.run(query, name=name, age=age, occupation=occupation)
        return result.single()["p"]

    def create_relationship(self, name1, name2, relation):
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_relationship, name1, name2, relation)
            print(f"Created relationship in Neo4j: {name1} - {relation} - {name2}")

    @staticmethod
    def _create_and_return_relationship(tx, name1, name2, relation):
        query = (
            "MATCH (a:Person {name: $name1}), (b:Person {name: $name2}) "
            "CREATE (a)-[r:" + relation + " {name: $relation}]->(b) "
            "RETURN type(r)"
        )
        result = tx.run(query, name1=name1, name2=name2, relation=relation)
        return result.single()["type(r)"]

def transfer_data(mongo, neo4j):
    people = mongo.get_people()
    relationships = mongo.get_relationships()

    print("Transferring people data from MongoDB to Neo4j...")
    for person in people:
        neo4j.create_person(person["name"], person["age"], person["occupation"])

    print("Transferring relationships data from MongoDB to Neo4j...")
    for relationship in relationships:
        neo4j.create_relationship(relationship["name1"], relationship["name2"], relationship["relation"])

if __name__ == "__main__":
    mongo_uri = "mongodb://localhost:27017/"
    mongo_dbname = "mydatabase"
    mongo = MongoDB(mongo_uri, mongo_dbname)

    neo4j_uri = "bolt://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "12345678"
    neo4j = Neo4jDB(neo4j_uri, neo4j_user, neo4j_password)

    transfer_data(mongo, neo4j)
    neo4j.close()
