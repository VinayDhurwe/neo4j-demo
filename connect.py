from neo4j import GraphDatabase

class Neo4jDemo:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_person(self, name):
        with self.driver.session() as session:
            if not session.execute_read(self._person_exists, name):
                session.execute_write(self._create_and_return_person, name)

    @staticmethod
    def _person_exists(tx, name):
        query = "MATCH (p:Person {name: $name}) RETURN p.name AS name"
        result = tx.run(query, name=name)
        return result.single() is not None

    @staticmethod
    def _create_and_return_person(tx, name):
        query = (
            "CREATE (p:Person { name: $name }) "
            "RETURN p.name AS name"
        )
        result = tx.run(query, name=name)
        return result.single()["name"]

    def create_relationship(self, name1, name2, relation):
        with self.driver.session() as session:
            session.execute_write(self._create_and_return_relationship, name1, name2, relation)

    @staticmethod
    def _create_and_return_relationship(tx, name1, name2, relation):
        query = (
            "MATCH (a:Person {name: $name1}), (b:Person {name: $name2}) "
            f"CREATE (a)-[r:{relation}]->(b) "
            "RETURN type(r) as type"
        )
        result = tx.run(query, name1=name1, name2=name2)
        return result.single()["type"]

    def find_person(self, name):
        with self.driver.session() as session:
            result = session.execute_read(self._find_and_return_person, name)
            self._process_result(result)

    @staticmethod
    def _find_and_return_person(tx, name):
        query = "MATCH (p:Person {name: $name}) RETURN p.name AS name"
        result = tx.run(query, name=name)
        return [record["name"] for record in result]

    @staticmethod
    def _process_result(result):
        for name in result:
            print(name)

if __name__ == "__main__":
    neo4j_demo = Neo4jDemo("bolt://localhost:7687", "neo4j", "12345678")
    neo4j_demo.create_person("Vinay")
    neo4j_demo.create_person("Yash")
    neo4j_demo.create_relationship("Vinay", "Yash", "KNOWS")
    neo4j_demo.find_person("Vinay")
    neo4j_demo.close()
