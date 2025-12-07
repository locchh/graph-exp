# Constraints and Indexes in Neo4j

## Constraints in Neo4j

A constraint is implemented internally as an index and is used to constrain what is added to the graph. There are three types of constraints you can define:

- Uniqueness for a single node property value.
- Existence for a property of a node or relationship.
- Existence and uniqueness for a set of node property values (called a Node key).

A best practice is to create constraints before you load your data.


## Indexes in Neo4j

An index in Neo4j is a data structure that allows the graph engine to retrieve data quickly. All indexes in Neo4j require more storage in the graph, so you must ensure that you do not index everything!

After the data is loaded, you create indexes to make your queries perform faster. Using indexes makes writing data slower, but retrieving it faster.

The types of indexes in Neo4j include:

- RANGE
- LOOKUP
- TEXT
- POINT
- Full-text

You can create an index on multiple properties or relationships. This type of index is called a Composite index.

## Identifying What Constraints and Indexes to Create

### Step 1: Identify constraints

You use constraints to:

- Uniquely identify a node.

- Ensure a property exists for a node or relationship.

- Ensure a set of properties is unique and exists for a node (Node key).


### Step 2: Create constraints

Next you create the constraints per your analysis.

### Step 3: Load the data

You typically load the data for your application and ensure that all data loaded correctly adhering to the constraints defined. If a constraint is violated, the Cypher load will fail.

A best practice is to always use `MERGE` for creating nodes and relationships. `MERGE` first does a lookup (using the uniqueness constraint which is an index), then creates the node if it does not exist.

You can use `LOAD CSV` to load data or you can use the Neo4j Data Importer App. The Neo4j Data Importer App actually creates the uniqueness constraints for you.

### Step 4: Identify indexes

Identifying the indexes for your graph depends on the most important use cases (queries) of your application.

### Step 5: Create indexes

After you have loaded the data and identified the indexes you will need, you create the indexes.

As you test your application, an important part is testing the performance of the queries. Use cases for the application may change so the identifying and creating indexes to improve query performance will be an ongoing process during the lifecycle of your application.