from neo4j import GraphDatabase

class Neo4jDemo:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def drop_existing_graph(self):
        with self.driver.session() as session:
            session.execute_write(self._drop_existing_graph)

    @staticmethod
    def _drop_existing_graph(tx):
        query = """
        CALL gds.graph.exists('myGraph') YIELD exists
        WHERE exists
        CALL gds.graph.drop('myGraph') YIELD graphName
        RETURN graphName
        """
        tx.run(query)

    def create_graph_projection(self):
        with self.driver.session() as session:
            session.execute_write(self._create_graph_projection)

    @staticmethod
    def _create_graph_projection(tx):
        query = """
        CALL gds.graph.project(
            'myGraph',
            ['Person'], // Specify node labels directly
            {
                FRIENDS: { type: 'FRIENDS' },
                COLLEAGUES: { type: 'COLLEAGUES' },
                FAMILY: { type: 'FAMILY' }
            }
        )
        """
        tx.run(query)

    def run_pagerank(self):
        with self.driver.session() as session:
            session.execute_write(self._run_pagerank)

    @staticmethod
    def _run_pagerank(tx):
        query = """
        CALL gds.pageRank.stream('myGraph')
        YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).name AS name, score
        ORDER BY score DESC
        """
        result = tx.run(query)
        for record in result:
            print(f"{record['name']}: {record['score']}")

if __name__ == "__main__":
    neo4j_demo = Neo4jDemo("bolt://localhost:7687", "neo4j", "12345678")
    
    # Drop the existing graph if it exists
    neo4j_demo.drop_existing_graph()
    
    # Create graph projection and run PageRank
    neo4j_demo.create_graph_projection()
    neo4j_demo.run_pagerank()
    neo4j_demo.close()
