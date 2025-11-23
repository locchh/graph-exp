# Cypher cheatsheet

[Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/?_gl=1*erbvw*_ga*MTkzMzgxNTk1LjE3NTcyNTg0MzQ.*_ga_DZP8Z65KK4*czE3NjM4NjAwNzQkbzUwJGcxJHQxNzYzODg4NDAxJGoyNiRsMCRoMA..*_gcl_au*MjEzNTI4NjkxNy4xNzU3MjU4NDMzLjc4MDQ1OTczLjE3NTg0MTY3NjUuMTc1ODQxNjc2NA..*_ga_DL38Q8KGQC*czE3NjM4NjAwNzQkbzUwJGcxJHQxNzYzODg4NDAxJGoyNiRsMCRoMA..)

[Neo4j Cypher Refcard](https://neo4j.com/docs/cypher-refcard/current/?_gl=1*erbvw*_ga*MTkzMzgxNTk1LjE3NTcyNTg0MzQ.*_ga_DZP8Z65KK4*czE3NjM4NjAwNzQkbzUwJGcxJHQxNzYzODg4NDAxJGoyNiRsMCRoMA..*_gcl_au*MjEzNTI4NjkxNy4xNzU3MjU4NDMzLjc4MDQ1OTczLjE3NTg0MTY3NjUuMTc1ODQxNjc2NA..*_ga_DL38Q8KGQC*czE3NjM4NjAwNzQkbzUwJGcxJHQxNzYzODg4NDAxJGoyNiRsMCRoMA..)

## Reading

### 1. Cypher pattern
```cypher
(m:Movie {title: 'Cloud Atlas'})<-[:ACTED_IN]-(p:Person)
```

### 2. Retrieving nodes

```cypher
MATCH (p:Person)
RETURN p
```

```cypher
MATCH (p:Person {name: 'Tom Hanks'})
RETURN p
```

```cypher
MATCH (p:Person {name: 'Tom Hanks'})
RETURN  p.born
```

```cypher
MATCH (p:Person)
WHERE p.name = 'Tom Hanks'
RETURN p.born
```

### 3. Finding Relationships

```cypher
MATCH (p:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(m)
RETURN m.title
```

```cypher
MATCH (p:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(m:Movie)
RETURN m.title
```

```cypher
MATCH (m:Movie)<-[:DIRECTED]-(p:Person) RETURN p.name
```

```cypher
MATCH (m:Movie {title:"Cloud Atlas"})<-[:DIRECTED]-(p:Director)
RETURN p.name;
```

## Filtering

### 1. Filtering by property values

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE m.released = 2008 OR m.released = 2009
RETURN p, m
```

### 2. Filtering by node labels

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE m.title='The Matrix'
RETURN p.name
```

```cypher
MATCH (p)-[:ACTED_IN]->(m)
WHERE p:Person AND m:Movie AND m.title='The Matrix'
RETURN p.name
```

### 3. Filtering using ranges

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE 2000 <= m.released <= 2003
RETURN p.name, m.title, m.released
```

### 4. Filtering by existence of a property

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name='Jack Nicholson' AND m.tagline IS NOT NULL
RETURN m.title, m.tagline
```

### 5. Filtering by partial strings

```cypher
MATCH (p:Person)-[:ACTED_IN]->()
WHERE p.name STARTS WITH 'Michael'
RETURN p.name
```

String tests are case-sensitive so you may need to use the `toLower()` or `toUpper()` functions to ensure the test yields the correct results. For example:

```cypher
MATCH (p:Person)-[:ACTED_IN]->()
WHERE toLower(p.name) STARTS WITH 'michael'
RETURN p.name
```

### 6. Filtering by patterns in the graph


```cypher
MATCH (p:Person)-[:WROTE]->(m:Movie)
WHERE NOT exists( (p)-[:DIRECTED]->(m) )
RETURN p.name, m.title
```

### 7. Filtering using lists

```cypher
MATCH (p:Person)
WHERE p.born IN [1965, 1970, 1975]
RETURN p.name, p.born
```

```cypher
MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
WHERE  'Neo' IN r.roles AND m.title='The Matrix'
RETURN p.name, r.roles
```

## Discovering

### 1. Discovering properties

You can discover the keys (properties) of the Person nodes in the graph by running this code:

```cypher
MATCH (p:Person)
RETURN p.name, keys(p)
```

Discovering relationship types

```cypher
MATCH (p:Person)-[r]->(m:Movie)
WHERE  p.name = 'Tom Hanks'
RETURN m.title AS movie, type(r) AS relationshipType
```

You can run this code to return all the property keys defined in the graph.

```cypher
CALL db.propertyKeys()
```

You can view the property types for nodes in the graph by executing this query:

```cypher
CALL db.schema.nodeTypeProperties()
```

You can view the property types for relationships in the graph by executing this query:

```cypher
CALL db.schema.relTypeProperties()
```

### 2. Discovering data model

You can view the data model by executing this query:

```cypher
CALL db.schema.visualization()
```

You can find out what labels exist in the graph with this code:

```cypher
CALL db.labels()
```

### 3. Discovering constraints

You can view the constraints for nodes in the graph by executing this query:

```cypher
SHOW CONSTRAINTS
```

## Writing

### 1. Creating nodes

```cypher
MERGE (p:Person {name: 'Michael Caine'})
```

**Note**: Note that when you use `MERGE` to create a node, you must specify at least one property that will be the unique primary key for the node.

Chain multiple `MERGE` clauses together within a single Cypher code block.

```cypher
MERGE (p:Person {name: 'Katie Holmes'})
MERGE (m:Movie {title: 'The Dark Knight'})
RETURN p, m
```

Cypher has a `CREATE` clause you can use for creating nodes. The benefit of using `CREATE` is that it does not look up the primary key before adding the node. You can use `CREATE` if you are sure your data is clean and you want greater speed during import. 

```cypher
CREATE (p:Person {name: 'Michael Caine'})
```

### 2. Creating relationships

Just like you can use `MERGE` to create nodes in the graph, you use `MERGE` to create relationships between two nodes. First you must have references to the two nodes you will be creating the relationship for. When you create a relationship between two nodes, it must have:
- Type
- Direction

```cypher
MATCH (p:Person {name: 'Michael Caine'})
MATCH (m:Movie {title: 'The Dark Knight'})
MERGE (p)-[:ACTED_IN]->(m)
```

**Note**: Notice also that you need not specify direction in the `MATCH` pattern since the query engine will look for all nodes that are connected, regardless of the direction of the relationship.

Creating nodes and relationships using multiple clauses

```cypher
MERGE (p:Person {name: 'Chadwick Boseman'})
MERGE (m:Movie {title: 'Black Panther'})
MERGE (p)-[:ACTED_IN]-(m)
```

Using `MERGE` to create nodes and a relationship in single clause

```cypher
MERGE (p:Person {name: 'Emily Blunt'})-[:ACTED_IN]->(m:Movie {title: 'A Quiet Place'})
RETURN p, m
```

## Updating

### 1. Adding properties for a node or relationship

Inline as part of the `MERGE` clause

```cypher
MATCH (p:Person {name: 'Michael Caine'})
MERGE (m:Movie {title: 'Batman Begins'})
MERGE (p)-[:ACTED_IN {roles: ['Alfred Penny']}]->(m)
RETURN p,m
```

Using the SET keyword for a reference to a node or relationship

```cypher
MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
WHERE p.name = 'Michael Caine' AND m.title = 'The Dark Knight'
SET r.roles = ['Alfred Penny']
RETURN p, r, m
```

### 2. Setting multiple properties

```cypher
MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
WHERE p.name = 'Michael Caine' AND m.title = 'The Dark Knight'
SET r.roles = ['Alfred Penny'], m.released = 2008
RETURN p, r, m
```

### 3. Updating properties

```cypher
MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
WHERE p.name = 'Michael Caine' AND m.title = 'The Dark Knight'
SET r.roles = ['Mr. Alfred Penny']
RETURN p, r, m
```

### 4. Removing properties

You can remove or delete a property from a node or relationship by using the `REMOVE` keyword, or setting the property to `null`.

```cypher
MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
WHERE p.name = 'Michael Caine' AND m.title = 'The Dark Knight'
REMOVE r.roles
RETURN p, r, m
```

```cypher
MATCH (p:Person)
WHERE p.name = 'Gene Hackman'
SET p.born = null
RETURN p
```

### 5. Customizing MERGE behavior

You can also specify behavior at runtime that enables you to set properties when the node is created or when the node is found. We can use the `ON CREATE SET` or `ON MATCH SET` conditions, or the `SET` keywords to set any additional properties.

```cypher
// Find or create a person with this name
MERGE (p:Person {name: 'McKenna Grace'})

// Only set the `createdAt` property if the node is created during this query
ON CREATE SET p.createdAt = datetime()

// Only set the `updatedAt` property if the node was created previously
ON MATCH SET p.updatedAt = datetime()

// Set the `born` property regardless
SET p.born = 2006

RETURN p
```

## Deleting

In a Neo4j database you can delete:

- nodes
- relationships
- properties
- labels

### 1. Deleting a node

```cypher
MATCH (p:Person {name: 'Jane Doe'})
DELETE p
```

### 2. Deleting a relationship

```cypher
MATCH (p:Person {name: 'Jane Doe'})-[r:ACTED_IN]->(m:Movie {title: 'The Matrix'})
DELETE r
RETURN p, m
```

### 3. Deleting a node and its relationships

```cypher
MATCH (p:Person {name: 'Jane Doe'})
DETACH DELETE p
```

### 4. Deleting everything

```cypher
MATCH (n)
DETACH DELETE n
```

### 5. Deleting labels

```cypher
MATCH (p:Person {name: 'Jane Doe'})
REMOVE p:Developer
RETURN p
```