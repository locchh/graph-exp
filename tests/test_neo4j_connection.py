import pytest
from neo4j import GraphDatabase
from pathlib import Path
import os

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Neo4j connection settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # Default password from your Makefile

@pytest.fixture(scope="module")
def neo4j_driver():
    """Fixture to provide a Neo4j driver for testing."""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    yield driver
    driver.close()

def test_neo4j_connection(neo4j_driver):
    """Test basic connection to Neo4j database."""
    # Simple query to verify the connection
    with neo4j_driver.session() as session:
        result = session.run("RETURN 'Hello, Neo4j!' AS greeting")
        record = result.single()
        assert record["greeting"] == "Hello, Neo4j!"

def test_neo4j_version(neo4j_driver):
    """Test that we can get the Neo4j server version."""
    with neo4j_driver.session() as session:
        result = session.run("CALL dbms.components() YIELD name, versions RETURN name, versions[0] as version")
        record = result.single()
        assert record["name"] == "Neo4j Kernel"
        assert record["version"]  # Just check that we got a version string

def test_neo4j_write_read(neo4j_driver):
    """Test writing and reading data from Neo4j."""
    test_data = {"name": "Test Node", "value": 42}
    
    with neo4j_driver.session() as session:
        # Create a test node
        create_result = session.run(
            "CREATE (n:TestNode $props) RETURN n",
            props=test_data
        )
        created_node = create_result.single()["n"]
        node_id = created_node.id
        
        # Read it back
        read_result = session.run(
            "MATCH (n) WHERE id(n) = $id RETURN n",
            id=node_id
        )
        read_node = read_result.single()["n"]
        
        # Verify the data
        assert read_node["name"] == test_data["name"]
        assert read_node["value"] == test_data["value"]
        
        # Clean up
        session.run("MATCH (n) WHERE id(n) = $id DELETE n", id=node_id)
