from app.config import config
from neo4j import GraphDatabase

# Singleton instance for Neo4j driver
_driver = None


def get_neo4j_driver():
    global _driver
    if _driver is None:
        driver = GraphDatabase.driver(
            config["Database"]["NEO4J_URI"],
            auth=(
                config["Database"]["NEO4J_USERNAME"],
                config["Database"]["NEO4J_PASSWORD"],
            ),
        )
        _driver = driver

    return _driver
