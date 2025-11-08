# Import data into Neo4j

## Setup Neo4j

```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_PLUGINS='["apoc"]' \
  -e NEO4J_apoc_export_file_enabled=true \
  -e NEO4J_apoc_import_file_enabled=true \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

## Source data

When you import data into Neo4j, you typically start with a set of source files. You may have exported this source data from:

- Relational databases
- Web APIs
- Public data directories
- BI tools
- Spreadsheets (e.g. Excel or Google Sheets)

Before you start the import process, you should:

- Understand the data in the source CSV files.
- Inspect and clean (if necessary) the data in the source data files.
- Understand the graph data model you will be implementing during the import.

The import involves creating Cypher code to:

- Read the source data.
- Transform the data as needed.
- Create nodes, relationships, and properties to create the graph.

## Import data

- Create Nodes
- Create Relationships
- Create Properties
- Create Constraints

### Guide

- Add person node `persons.csv` file.

- Add movie node `movies.csv` file.

- Setting the unique ID for the Movie node to movieId, a unique constraint named `movieId_Movie_uniq` is created against the movieId property.

- An index is created automatically for the unique ID property. For example, the index movieId_Movie_uniq will be created for the movieId property on the Movie node.

- Create relationship `acted_in.csv` file.

- Create relationship `directed.csv` file.

- Add  `ratings.csv` file.

### Casting

All data loaded using LOAD CSV will be returned as strings - you need to cast the data to an appropriate data type before being written to a property.

The types of data that you can store as properties in Neo4j include:

- String
- Integer
- Float (decimal values)
- Boolean
- Date/Datetime
- Point (spatial)
- Lists of values

What is a Multi-value property?

All values in a list must have the same data type. For example:

```
["Apple", "Banana, "Orange"]

[100, 55, 4]
```

Cypher functions to cast data include:

| Function | Description |
|----------|-------------|
| `toBoolean()` | Converts a string to a boolean value |
| `toFloat()` | Converts a string to a float value |
| `toInteger()` | Converts a string to an integer value |
| `toString()` | Converts a value to a string |
| `date()` | Converts a string to a date value |
| `datetime()` | Converts a string to a date and time value |

### Full Cypher Query

```cypher
MATCH (p:Person) DETACH DELETE p;
MATCH (m:Movie) DETACH DELETE m;

DROP CONSTRAINT Person_tmdbId IF EXISTS;
DROP CONSTRAINT Movie_movieId IF EXISTS;

CREATE CONSTRAINT Person_tmdbId IF NOT EXISTS
FOR (x:Person)
REQUIRE x.tmdbId IS UNIQUE;

CREATE CONSTRAINT Movie_movieId IF NOT EXISTS
FOR (x:Movie)
REQUIRE x.movieId IS UNIQUE;

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
m.languages = split(row.languages, '|');

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
```

## Normalized Data

**Definition:** Data is organized to minimize redundancy by separating it into multiple related tables (in relational databases) or nodes (in graph databases).

**Characteristics:**
- Minimizes data duplication
- Reduces update anomalies (insert, update, delete)
- Maintains data integrity through relationships
- Requires joins/relationships to reconstruct complete information

```cypher
# Normalized Tables
CUSTOMERS (customer_id, name, email)
ORDERS (order_id, customer_id, order_date)
ORDER_ITEMS (order_id, product_id, quantity)
PRODUCTS (product_id, name, price)
```

Example in Graph Database (Normalized):

```cypher
(customer:Customer {id: 1, name: "John"})-[:PLACED]->(order:Order {id: 101, date: "2023-11-08"})
(order)-[:CONTAINS]->(product:Product {id: 1001, name: "Laptop", price: 999})
```

## Denormalized Data

**Definition:** Data is stored with some redundancy to optimize read performance, often by duplicating data across multiple records.

**Characteristics:**

- Improves read performance by reducing joins
- Increases storage requirements
- Can lead to update anomalies if not managed carefully
- Simplifies queries by keeping related data together

Example in Document Database:

```json
{
  "order_id": 101,
  "customer": {
    "name": "John",
    "email": "john@example.com"
  },
  "items": [
    {
      "product_name": "Laptop",
      "price": 999,
      "quantity": 1
    }
  ]
}
```

Example in Graph Database (Denormalized):

```cypher
// Some properties duplicated for faster access
(order:Order {
  id: 101, 
  date: "2023-11-08",
  customer_name: "John",  // Denormalized from Customer
  total: 999
})-[:CONTAINS]->(product:Product {id: 1001, name: "Laptop"})
```