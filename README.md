# MongoDB and Neo4j Graph Database Integration with GDS

## Overview

This project demonstrates how to integrate MongoDB with Neo4j, and utilize Neo4j Graph Data Science (GDS) algorithms for advanced graph analytics and visualization. It involves:

1. **Inserting Data into MongoDB**: Sample data for people and relationships is inserted into MongoDB.
2. **Transferring Data to Neo4j**: Data from MongoDB is transferred to a Neo4j graph database.
3. **Applying GDS Algorithms**: Neo4j's GDS algorithms are used to analyze the graph.
4. **Visualizing Results in Neo4j Bloom**: Graph visualizations and algorithm results are explored using Neo4j Bloom.

## Prerequisites

- Python 3.x
- MongoDB
- Neo4j Desktop (with Neo4j database)
- Neo4j Bloom (comes with Neo4j Desktop)

## Setup

1. **Install Required Python Packages**:
   ```bash
   pip install pymongo neo4j
   ```

2. **MongoDB Setup**:
   - Ensure MongoDB is running locally or adjust the URI in the script if using a remote instance.

3. **Neo4j Setup**:
   - Start Neo4j Desktop and create a new database.
   - Ensure Neo4j Bloom is installed and accessible.

## Usage

### 1. Insert Data into MongoDB

Run the `insert_data.py` script to insert sample data into MongoDB:
```bash
python insert_data.py
```

### 2. Transfer Data to Neo4j

Run the `transfer_data.py` script to transfer data from MongoDB to Neo4j:
```bash
python transfer_data.py
```

### 3. Apply GDS Algorithms in Neo4j

In Neo4j Desktop, use the following Cypher queries to project the graph and run GDS algorithms:

**Project the Graph**:
```cypher
CALL gds.graph.project(
    'myGraph',
    'Person',
    {
        FRIENDS: { type: 'FRIENDS', orientation: 'UNDIRECTED' },
        COLLEAGUES: { type: 'COLLEAGUES', orientation: 'UNDIRECTED' },
        FAMILY: { type: 'FAMILY', orientation: 'UNDIRECTED' }
    }
)
```

**Run PageRank Algorithm**:
```cypher
CALL gds.pageRank.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score
ORDER BY score DESC
```

### 4. Visualize in Neo4j Bloom

1. Open Neo4j Bloom from Neo4j Desktop.
2. Use the search bar to visualize nodes and relationships. For example:
   - `MATCH (p:Person) RETURN p` to visualize all people.
   - `MATCH (a)-[r:FRIENDS]->(b) RETURN a, r, b` to visualize FRIENDS relationships.
3. Explore the results of the PageRank algorithm by using the saved search.

