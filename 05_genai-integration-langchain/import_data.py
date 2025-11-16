import os

from dotenv import load_dotenv

load_dotenv()

import textwrap
from neo4j import GraphDatabase
from utils import execute_query

neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USERNAME")
neo4j_pass = os.getenv("NEO4J_PASSWORD")
neo4j_db = os.getenv("NEO4J_DATABASE")

neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))

cypher = textwrap.dedent("""
    MATCH (p:Person) DETACH DELETE p;
    MATCH (m:Movie) DETACH DELETE m;
    MATCH (u:User) DETACH DELETE u;
    MATCH (g:Genre) DETACH DELETE g;

    DROP CONSTRAINT Person_tmdbId IF EXISTS;
    DROP CONSTRAINT Movie_movieId IF EXISTS;
    DROP CONSTRAINT User_userId IF EXISTS;
    DROP CONSTRAINT Genre_name IF EXISTS;

    CREATE CONSTRAINT Person_tmdbId IF NOT EXISTS
    FOR (x:Person)
    REQUIRE x.tmdbId IS UNIQUE;

    CREATE CONSTRAINT Movie_movieId IF NOT EXISTS
    FOR (x:Movie)
    REQUIRE x.movieId IS UNIQUE;

    CREATE CONSTRAINT User_userId IF NOT EXISTS
    FOR (x:User)
    REQUIRE x.userId IS UNIQUE;

    CREATE CONSTRAINT Genre_name IF NOT EXISTS
    FOR (x:Genre)
    REQUIRE x.name IS UNIQUE;

    LOAD CSV WITH HEADERS
    FROM 'https://data.neo4j.com/importing-cypher/persons.csv' AS row
    MERGE (p:Person {tmdbId: toInteger(row.person_tmdbId)})
    SET
    p.imdbId = toInteger(row.person_imdbId),
    p.bornIn = row.bornIn,
    p.name = row.name,
    p.bio = row.bio,
    p.poster = row.poster,
    p.url = row.url,
    p.born = date(row.born),
    p.died = date(row.died);

    LOAD CSV WITH HEADERS
    FROM 'https://data.neo4j.com/importing-cypher/movies.csv' AS row
    MERGE (m:Movie {movieId: toInteger(row.movieId)})
    SET
    m.tmdbId = toInteger(row.movie_tmdbId),
    m.imdbId = toInteger(row.movie_imdbId),
    m.released = date(row.released),
    m.title = row.title,
    m.year = toInteger(row.year),
    m.plot = row.plot,
    m.budget = toInteger(row.budget),
    m.imdbRating = toFloat(row.imdbRating),
    m.poster = row.poster,
    m.runtime = toInteger(row.runtime),
    m.imdbVotes = toInteger(row.imdbVotes),
    m.revenue = toInteger(row.revenue),
    m.url = row.url,
    m.countries = split(row.countries, '|'),
    m.languages = split(row.languages, '|'),
    m.genres = split(row.genres, '|');

    LOAD CSV WITH HEADERS
    FROM 'https://data.neo4j.com/importing-cypher/acted_in.csv' AS row
    MATCH (p:Person {tmdbId: toInteger(row.person_tmdbId)})
    MATCH (m:Movie {movieId: toInteger(row.movieId)})
    MERGE (p)-[r:ACTED_IN]->(m)
    SET r.role = row.role;

    LOAD CSV WITH HEADERS
    FROM 'https://data.neo4j.com/importing-cypher/directed.csv' AS row
    MATCH (p:Person {tmdbId: toInteger(row.person_tmdbId)})
    MATCH (m:Movie {movieId: toInteger(row.movieId)})
    MERGE (p)-[r:DIRECTED]->(m);

    MATCH (p:Person)-[:ACTED_IN]->()
    WITH DISTINCT p SET p:Actor;

    MATCH (p:Person)-[:DIRECTED]->()
    WITH DISTINCT p SET p:Director;

    CALL () {
    LOAD CSV WITH HEADERS
    FROM 'https://data.neo4j.com/importing-cypher/ratings.csv' AS row
    WITH row
    WHERE row.movieId IS NOT NULL AND row.userId IS NOT NULL
    MERGE (u:User {userId: toInteger(row.userId)})
        ON CREATE SET u.name = row.name
        ON MATCH  SET u.name = coalesce(row.name, u.name)
    WITH u, row
    MATCH (m:Movie {movieId: toInteger(row.movieId)})
    MERGE (u)-[r:RATED]->(m)
    SET
        r.rating    = toFloat(row.rating),
        r.timestamp = toInteger(row.timestamp)
    } IN TRANSACTIONS OF 1000 ROWS;

    MATCH (m:Movie)
    UNWIND m.genres AS genreName
    WITH m, trim(genreName) AS genreName
    WHERE genreName <> ''
    MERGE (g:Genre {name: genreName})
    MERGE (m)-[:IN_GENRE]->(g);
    """)

# Split the Cypher script into individual statements
cypher_statements = [stmt.strip() for stmt in cypher.split(';') if stmt.strip()]

# Execute each statement individually
for i, statement in enumerate(cypher_statements, 1):
    print(f"Executing statement {i}/{len(cypher_statements)}...")
    try:
        res = execute_query(neo4j_driver, statement)
        print(f"Statement {i} completed successfully")
    except Exception as e:
        print(f"Error executing statement {i}: {e}")
        break


# Import movie plot embeddings
cypher = textwrap.dedent("""
LOAD CSV WITH HEADERS
FROM 'https://data.neo4j.com/rec-embed/movie-plot-embeddings-1k.csv'
AS row
MATCH (m:Movie {movieId: toInteger(row.movieId)})
CALL db.create.setNodeVectorProperty(
  m,
  'plotEmbedding',
  apoc.convert.fromJsonList(row.embedding)
);
""")

execute_query(neo4j_driver, cypher)

# Create vector index for movie plots
cypher = textwrap.dedent("""
CREATE VECTOR INDEX moviePlots IF NOT EXISTS
FOR (m:Movie)
ON m.plotEmbedding
OPTIONS {indexConfig: {
 `vector.dimensions`: 1536,
 `vector.similarity_function`: 'cosine'
}};
""")

execute_query(neo4j_driver, cypher)

neo4j_driver.close()