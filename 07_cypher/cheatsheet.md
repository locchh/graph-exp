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

### 3. Using WITH clause for variables

The `WITH` clause allows you to pass variables from one part of the query to another, making your queries more readable and reusable.

```cypher
WITH 'Tom Hanks' AS actorName
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name = actorName
RETURN m.title AS movies
```

```cypher
WITH  'toy story' AS mt, 'Tom Hanks' AS actorName
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WITH m, toLower(m.title) AS movieTitle
WHERE p.name = actorName
AND movieTitle CONTAINS mt
RETURN m.title AS movies, movieTitle
```

Limiting the results

```cypher
WITH  'Tom Hanks' AS theActor
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name = theActor
WITH m  LIMIT 2
// possibly do more with the two m nodes
RETURN m.title AS movies
```

Ordering results

```cypher
WITH  'Tom Hanks' AS theActor
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name = theActor
WITH m ORDER BY m.year LIMIT 5
// possibly do more with the five m nodes in a particular order
RETURN m.title AS movies, m.year AS yearReleased
```

Using map projections in a WITH clause

```cypher
MATCH (n:Movie)
WHERE n.imdbRating IS NOT NULL
AND n.poster IS NOT NULL
WITH n {
  .title,
  .year,
  .languages,
  .plot,
  .poster,
  .imdbRating,
  directors: [ (n)<-[:DIRECTED]-(d) | d { tmdbId:d.imdbId, .name } ]
}
ORDER BY n.imdbRating DESC LIMIT 4
RETURN collect(n)
```

### 4. Finding Relationships

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

### 8. Multi MATCH clause

```cypher
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
WHERE m.year > 2000
MATCH (m)<-[:DIRECTED]-(d:Person)
RETURN a.name, m.title, d.name
```

An alternative to using multiple MATCH clauses is to specify multiple patterns:

```cypher
MATCH (a:Person)-[:ACTED_IN]->(m:Movie),
      (m)<-[:DIRECTED]-(d:Person)
WHERE m.year > 2000
RETURN a.name, m.title, d.name
```

Or using a single pattern:

```cypher
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(d:Person)
WHERE m.year > 2000
RETURN a.name, m.title, d.name
```

In general, using a single MATCH clause will perform better than multiple MATCH clauses. This is because relationship uniqueness is enforced so there are fewer relationships traversed.

### 9. OPTIONAL MATCH

Regular `MATCH` must find a match or the row is excluded. `OPTIONAL MATCH` if it finds a match, great. If not, returns null but keeps the row

```cypher
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
WHERE g.name = 'Film-Noir'
OPTIONAL MATCH (m)<-[:RATED]-(u:User)
RETURN m.title, u.name
```

## Understanding Query

### 1. EXPLAIN

Shows the logical execution plan without actually running the query. Helps you understand how Neo4j would execute the query.

```cypher
EXPLAIN
MATCH (p:Person)-[:KNOWS]->(friend)
WHERE p.name = 'Alice'
RETURN friend.name
```

### 2. PROFILE

Executes the query and shows the actual runtime execution plan. Includes full runtime metrics.

```cypher
PROFILE MATCH (p:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(p)
WHERE  p.name = 'Tom Hanks'
RETURN  m.title
```

### 3. Subqueries with CALL { }

Subqueries allow you to organize complex queries by running inner queries and using their results in outer queries.

```cypher
CALL {
   MATCH (m:Movie) WHERE m.year = 2000
   RETURN m ORDER BY m.imdbRating DESC LIMIT 10
}
MATCH  (:User)-[r:RATED]->(m)
RETURN m.title, avg(r.rating)
```

Passing variables into a subquery:

```cypher
MATCH (m:Movie)
CALL {
    WITH m
    MATCH (m)<-[r:RATED]-(u:User)
     WHERE r.rating = 5
    RETURN count(u) AS numReviews
}
RETURN m.title, numReviews
ORDER BY numReviews DESC
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

### 4. Shortest path

```cypher
MATCH p = shortestPath((p1:Person)-[*]-(p2:Person))
WHERE p1.name = "Eminem"
AND p2.name = "Charlton Heston"
RETURN  p
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

## Controlling Results

### 1. Ordering results

Whether you return results as nodes or as properties of nodes, you can specify a property value for the ordering. Strings are ordered by their text values. Boolean true comes before false when ordered. Numeric data (including date and datetime properties) are ordered by their numeric value.


```cypher
MATCH (p:Person)
WHERE p.born.year = 1980
RETURN p.name AS name,
p.born AS birthDate
ORDER BY p.born
```

Ordering multiple results:

```cypher
MATCH (p:Person)-[:DIRECTED | ACTED_IN]->(m:Movie)
WHERE p.name = 'Tom Hanks'
OR p.name = 'Keanu Reeves'
RETURN  m.year, m.title
ORDER BY m.year DESC , m.title
```


### 2. Limiting results

Although you can filter queries to reduce the number of results returned, you may also want to limit the number of results returned.

```cypher
MATCH (m:Movie)
WHERE m.released IS NOT NULL
RETURN m.title AS title,
m.released AS releaseDate
ORDER BY m.released DESC LIMIT 100
```

### 3. Skipping some results

In an ordered result set, you may want to control what results are returned. This is useful in an application where pagination is required.

```cypher
MATCH (p:Person)
WHERE p.born.year = 1980
RETURN  p.name as name,
p.born AS birthDate
ORDER BY p.born SKIP 40 LIMIT 10
```

### 4. Eliminating duplicate

```cypher
MATCH (p:Person)-[:DIRECTED | ACTED_IN]->(m:Movie)
WHERE p.name = 'Tom Hanks'
RETURN DISTINCT m.title, m.released
ORDER BY m.title
```

### 5. Changing data returned

You can always change the data that is returned by performing string or numeric operations on the data.

```cypher
MATCH (m:Movie)<-[:ACTED_IN]-(p:Person)
WHERE m.title CONTAINS 'Toy Story' AND
p.died IS NULL
RETURN m.title AS movie,
p.name AS actor,
p.born AS dob,
date().year - p.born.year AS ageThisYear
```

Here is an example where we concatenate string data returned:

```cypher
MATCH (m:Movie)<-[:ACTED_IN]-(p:Person)
WHERE m.title CONTAINS 'Toy Story' AND p.died IS NULL
RETURN 'Movie: ' + m.title AS movie,
p.name AS actor,
p.born AS dob,
date().year - p.born.year AS ageThisYear
```

Conditionally changing data returned

```cypher
MATCH (m:Movie)<-[:ACTED_IN]-(p:Person)
WHERE p.name = 'Henry Fonda'
RETURN m.title AS movie,
CASE
WHEN m.year < 1940 THEN 'oldies'
WHEN 1940 <= m.year < 1950 THEN 'forties'
WHEN 1950 <= m.year < 1960 THEN 'fifties'
WHEN 1960 <= m.year < 1970 THEN 'sixties'
WHEN 1970 <= m.year < 1980 THEN 'seventies'
WHEN 1980 <= m.year < 1990 THEN 'eighties'
WHEN 1990 <= m.year < 2000 THEN 'nineties'
ELSE  'two-thousands'
END
AS timeFrame
```

## Aggregation in Cypher

### 1. Using count() to aggregate data

```cypher
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(d:Person)
RETURN a.name AS actorName,
d.name AS directorName,
count(*) AS numMovies
ORDER BY numMovies DESC
```

### 2. Returning a list

```cypher
MATCH (p:Person)
RETURN p.name, [p.born, p.died] AS lifeTime
LIMIT 10
```

### 3. Using collect() to create a list

```cypher
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
RETURN a.name AS actor,
count(*) AS total,
collect(m.title) AS movies
ORDER BY total DESC LIMIT 10
```

Rather than collecting the values of the title properties for movies, you can collect the nodes.

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name ='Tom Cruise'
RETURN collect(m) AS tomCruiseMovies
```

### 4. Eliminating duplication in lists

```cypher
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
WHERE m.year = 1920
RETURN  collect( DISTINCT m.title) AS movies,
collect( a.name) AS actors
```

### 5. Accessing elements of a list

```cypher
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
RETURN m.title AS movie,
collect(a.name)[0] AS castMember,
size(collect(a.name)) as castSize
```

You can also return a slice of a collection.

```cypher
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)
RETURN m.title AS movie,
collect(a.name)[2..] AS castMember,
size(collect(a.name)) as castSize
```

### 6. Other aggregating functions

- `min()`
- `max()`
- `avg()`
- `stddev()`
- `sum()`

You can either use `count()` to count the number of rows, or alternatively, you can return the size of the collected results. The `size()` function returns the number of elements in a list.

### 7. List comprehension

```cypher
MATCH (m:Movie)
RETURN m.title as movie,
[x IN m.countries WHERE x CONTAINS 'USA' OR x CONTAINS 'Germany']
AS country LIMIT 500
```

### 8. Pattern comprehension

```cypher
MATCH (m:Movie)
WHERE m.year = 2015
RETURN m.title,
[(dir:Person)-[:DIRECTED]->(m) | dir.name] AS directors,
[(actor:Person)-[:ACTED_IN]->(m) | actor.name] AS actors
```

Notice that for pattern comprehension we specify the list with the square braces to include the pattern followed by the pipe character to then specify what value will be placed in the list from the pattern. `[<pattern> | value]`

Here is another example of using pattern comprehension to create a list where we specify a filter for the pattern.

```cypher
MATCH (a:Person {name: 'Tom Hanks'})
RETURN [(a)-->(b:Movie)
WHERE b.title CONTAINS "Toy" | b.title + ": " + b.year]
AS movies
```

### 9. Working with maps

A Cypher map is list of key/value pairs where each element of the list is of the format 'key': value. A node or relationship can have a property that is a map.

```cypher
RETURN {Jan: 31, Feb: 28, Mar: 31, Apr: 30 ,
May: 31, Jun: 30 , Jul: 31, Aug: 31, Sep: 30,
Oct: 31, Nov: 30, Dec: 31}['Feb'] AS daysInFeb
```

Alternatively, you can access a value with the '.' notation:

```cypher
RETURN {Jan: 31, Feb: 28, Mar: 31, Apr: 30 ,
May: 31, Jun: 30 , Jul: 31, Aug: 31, Sep: 30,
Oct: 31, Nov: 30, Dec: 31}.Feb AS daysInFeb
```

And you can return a list of keys of a map as follows:

```cypher
RETURN keys({Jan: 31, Feb: 28, Mar: 31, Apr: 30 ,
May: 31, Jun: 30 ,Jul: 31, Aug: 31, Sep: 30,
Oct: 31, Nov: 30, Dec: 31}) AS months
```

### 10. Map projections

Map projections are when you can use retrieved nodes to create or return some of the information in the nodes.

```cypher
MATCH (m:Movie)
WHERE m.title CONTAINS 'Matrix'
RETURN m { .title, .released } AS movie
```

### 11. Using UNWIND to expand collections

The `UNWIND` clause expands a list into a sequence of rows, allowing you to work with individual elements of collections.

```cypher
MATCH (m:Movie)-[:ACTED_IN]-(a:Actor)
WHERE a.name = 'Tom Hanks'
UNWIND m.languages AS lang
RETURN m.title AS movie,
m.languages AS languages,
lang AS language
```

```cypher
MATCH (m:Movie)
UNWIND m.languages AS lang
WITH m, trim(lang) AS language
// this automatically, makes the language distinct because it's a grouping key
WITH language, collect(m.title) AS movies
RETURN language, movies[0..10]
```

## Date and Time

### 1. Working with date time data

Cypher has these basic formats for storing date and time data.

```cypher
RETURN date(), datetime(), time()
```

Create a node in the graph containing

```cypher
MERGE (x:Test {id: 1})
SET x.date = date(),
    x.datetime = datetime(),
    x.time = time()
RETURN x
```

### 2. Extracting components of a date or datetime

```cypher
MATCH (x:Test {id: 1})
RETURN x.date.day, x.date.year,
x.datetime.year, x.datetime.hour,
x.datetime.minute
```

### 3. Setting date values

```cypher
MATCH (x:Test {id: 1})
SET x.date1 = date('2022-01-01'),
    x.date2 = date('2022-01-15')
RETURN x
```

### 4. Setting datetime values

```cypher
MATCH (x:Test {id: 1})
SET x.datetime1 = datetime('2022-01-04T10:05:20'),
    x.datetime2 = datetime('2022-04-09T18:33:05')
RETURN x
```

### 5. Working with durations

```cypher
MATCH (x:Test {id: 1})
RETURN duration.between(x.date1,x.date2)
```

We can return the duration in days between two datetime values

```cypher
MATCH (x:Test {id: 1})
RETURN duration.inDays(x.datetime1,x.datetime2).days
```

We can add a duration of 6 months:

```cypher
MATCH (x:Test {id: 1})
RETURN x.date1 + duration({months: 6})
```

### 6. Using APOC to format dates and times

```cypher
MATCH (x:Test {id: 1})
RETURN x.datetime as Datetime,
apoc.temporal.format( x.datetime, 'HH:mm:ss.SSSS')
AS formattedDateTime
```