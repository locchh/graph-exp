# Graph Data Modeling

## What is Graph Data Modeling?

If you use a Neo4j graph to support part or all of your application, you must collaboratively work with your stakeholders to design a graph that will:

- Answer the key use cases for the application.
- Provide the best Cypher statement performance for the key use cases.

The Neo4j components that are used to define the graph data model are:

- Nodes
- Labels
- Relationships
- Properties


## Data modeling process

Here are the steps to create a graph data model:

1. Understand the domain and define specific use cases (questions) for the application.


    - Identify the stakeholders and developers of the application.

    - With the stakeholders and developers:

        - Describe the application in detail.

        - Identify the users of the application (people, systems).

        - Agree upon the use cases for the application.

        - Rank the importance of the use cases.


2. Develop the initial graph data model:

    - Model the nodes (entities).
    - Model the relationships between nodes.

3. Test the use cases against the initial data model.

4. Create the graph (instance model) with test data using Cypher.

5. Test the use cases, including performance against the graph.

6. Refactor (improve) the graph data model due to a change in the key use cases or for performance reasons.

7. Implement the refactoring on the graph and retest using Cypher.

Graph data modeling is an iterative process. Your initial graph data model is a starting point, but as you learn more about the use cases or if the use cases change, the initial graph data model will need to change. In addition, you may find that especially when the graph scales, you will need to modify the graph (refactor) to achieve the best performance for your key use cases.

Refactoring is very common in the development process. A Neo4j graph has an optional schema which is quite flexible, unlike the schema in an RDBMS. A Cypher developer can easily modify the graph to represent an improved data model.

## Types of models

When performing the graph data modeling process for an application, you will need at least two types of models:

- Data model
- Instance model

### Data model

The data model describes the labels, relationships, and properties for the graph. It does not have specific data that will be created in the graph. There is nothing that uniquely identifies a node with a given label. A graph data model, however is important because it defines the names that will be used for labels, relationship types, and properties when the graph is created and used by the application.

### Style guidelines for modeling

As you begin the graph data modeling process, it is important that you agree upon how labels, relationship types, and property keys are named. Labels, relationship types, and property keys are case-sensitive, unlike Cypher keywords which are case-insensitive.

A Neo4j best practice is to use the following when you name the elements of the graph, but you are free to use any convention for your application.

- A label is a single identifier that begins with a capital letter and can be PascalCase.

    Examples: Person, Company, GitHubRepo

- A relationship type is a single identifier that is in all capital letters with the underscore character.

    Examples: FOLLOWS, MARRIED_TO

- A property key for a node or a relationship is a single identifier that begins with a lower-case letter and can be camelCase.

    Examples: deptId, firstName

**Note:** Property key names need not be unique. For example, a Person node and a Movie node, each can have the property key of tmdbId.

### Instance model

An important part of the graph data modeling process is to test the model against the use cases. To do this, you need to have a set of sample data that you can use to see if the use cases can be answered with the model. In this instance model, we have created some instances of Person and Movie nodes, as well as their relationships. Having this type of instance model will help us to test our use cases.

## Why refactor?

Refactoring is the process of changing the data model and the graph.

There are three reasons why you would refactor:

- The graph as modeled does not answer all of the use cases.

- A new use case has come up that you must account for in your data model.

- The Cypher for the use cases does not perform optimally, especially when the graph scales

### Steps for refactoring

To refactor a graph data model and a graph, you must:

- Design the new data model.

- Write Cypher code to transform the existing graph to implement the new data model.

- Retest all use cases, possibly with updated Cypher code.

## Avoid These Labels

### Semantically orthogonal labels

“Semantically orthogonal” is a fancy term that means that labels should have nothing to do with one another. You should be careful not to use the same type of label in different contexts. For example, using the region for all types of nodes is not useful for most queries.

### Representing class hierarchies

You also want to avoid labeling your nodes to represent hierarchies.

## Eliminating Duplicate Data

You should take care to avoid duplicating data in your graph. Where some databases require a form of denormalization to improve the speed of a set of queries, this is not always the case with a graph database. De-duplicating data gives you the added benefit of allowing you to query through a node - for example, finding other customers who have purchased a particular product, or finding similar movies based on the rating of other users.

In addition, duplicating data in the graph increases the size of the graph and the amount of data that may need to be retrieved for a query.

## Eliminating Complex Data in Nodes

Since nodes are used to store data about specific entities, you may have initially modeled, for example, a Production node to contain the details of the address for the production company. Storing complex data in the nodes may not be beneficial for a couple of reasons:

- Duplicate data. Many nodes may have production companies in a particular location and the data is repeated in many nodes.

- Queries related to the information in the nodes require that all nodes be retrieved.

## Intermediate nodes

You sometimes find cases where you need to connect more data to a relationship than can be fully captured in the properties. In other words, you want a relationship that connects more than two nodes. Mathematics allows this, with the concept of a hyperedge. A solution to hyperedges in Neo4j is to create intermediate nodes.

You create intermediate nodes when you need to:

- Connect more than two nodes in a single context.

- Hyperedges (n-ary relationships)

- Relate something to a relationship.

- Share data in the graph between entities.