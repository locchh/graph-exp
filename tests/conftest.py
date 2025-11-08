"""
Pytest configuration and shared fixtures for Neo4j tests.
"""
import pytest
from neo4j import GraphDatabase

# Neo4j connection settings
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # Should match your Makefile

@pytest.fixture(scope="session")
def neo4j_driver():
    """Session-scoped fixture for Neo4j driver."""
    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
        max_connection_lifetime=1000,
        connection_timeout=30,  # seconds
        connection_acquisition_timeout=30  # seconds
    )
    
    # Verify the connection works
    try:
        with driver.session() as session:
            session.run("RETURN 1").single()
    except Exception as e:
        pytest.skip(f"Could not connect to Neo4j: {e}")
    
    yield driver
    
    # Cleanup
    driver.close()

@pytest.fixture(autouse=True)
def clean_neo4j(neo4j_driver):
    """Clean the database between tests.
    
    This ensures tests don't interfere with each other.
    """
    # Run before each test
    with neo4j_driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    
    yield  # This is where the test runs
    
    # Cleanup after each test
    with neo4j_driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
