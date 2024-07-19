from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri, dbname):
        self.client = MongoClient(uri)
        self.db = self.client[dbname]

    def insert_person(self, name, age, occupation):
        self.db.people.insert_one({"name": name, "age": age, "occupation": occupation})
        print(f"Inserted person: {name}, {age}, {occupation}")

    def insert_relationship(self, name1, name2, relation):
        self.db.relationships.insert_one({"name1": name1, "name2": name2, "relation": relation})
        print(f"Inserted relationship: {name1} - {relation} - {name2}")

if __name__ == "__main__":
    mongo_uri = "mongodb://localhost:27017/"
    mongo_dbname = "mydatabase"
    mongo = MongoDB(mongo_uri, mongo_dbname)

    # Inserting data into MongoDB
    people_data = [
        ("Alice", 30, "Software Engineer"),
        ("Bob", 35, "Data Scientist"),
        ("Charlie", 25, "Product Manager"),
        ("David", 40, "CEO"),
        ("Eva", 28, "UX Designer")
    ]
    for person in people_data:
        mongo.insert_person(*person)

    relationships_data = [
        ("Alice", "Bob", "FRIENDS"),
        ("Bob", "Charlie", "COLLEAGUES"),
        ("Charlie", "David", "FAMILY"),
        ("Eva", "Alice", "FRIENDS"),
        ("Eva", "Bob", "COLLEAGUES")
    ]
    for relationship in relationships_data:
        mongo.insert_relationship(*relationship)
