from neo4j import Driver


def execute_query(driver: Driver, query: str, parameters: dict = None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return result
