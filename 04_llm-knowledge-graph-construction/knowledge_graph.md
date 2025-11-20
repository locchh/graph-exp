# Knowledge Graph

## What is a Knowledge Graph

*A knowledge graph is an organized representation of real-world entities and their relationships. *

Knowledge graphs provide a structured way to represent entities, their attributes, and their relationships, allowing for a comprehensive and interconnected understanding of the information.

Knowledge graphs can break down sources of information and integrate them, allowing you to see the relationships between the data.

This integration from diverse sources gives knowledge graphs a more holistic view and facilitates complex queries, analytics, and insights.

Knowledge graphs can readily adapt and evolve as they grow, taking on new information and structure changes.

## Organizing principles

* A knowledge graph stores data and relationships alongside frameworks known as organizing principles. *

The organizing principles are the rules or categories around the data that provide structure to the data. Organizing principles can range from simple data descriptions, for example, describing a GraphAcademy course as course → modules → lessons, to a complex vocabulary of the complete solution.

Knowledge graphs are inherently flexible, and you can change the organizing principles as the data grows and changes.

## Creating knowledge graphs

Creating knowledge graphs from unstructured data can be complex, involving multiple steps of data query, cleanse, and transform.

You can use the text analysis capabilities of Large Language Models (LLMs) to help automate knowledge graph creation.

## Benefits of knowledge graphs


- **Enhanced Data Integration and Interoperability**: Knowledge graphs facilitate data integration from disparate sources, creating a unified view.

- **Improved Search and Discovery**: Knowledge graphs enhance search capabilities by structuring data into entities and relationships. Instead of simple keyword-based searches, users can perform more nuanced queries that reflect real-world contexts and relationships.

- **Contextual Understanding**: Knowledge graphs help understand the context of information by capturing the relationships between entities.

- **Enhanced Decision Making**: Knowledge graphs enable better decision-making by providing a holistic view of interconnected data. Organizations can identify patterns and trends that might not be apparent from isolated data points.

## Challenges of knowledge graphs

- **Data Collection and Integration**: Data is often spread across various sources with different formats, structures, and standards.

- **Data Quality**: Ensuring data’s accuracy, consistency, and completeness is crucial.

- **Data Modeling & Schema Design**: Developing a flexible and robust schema that can accommodate a wide range of entities and relationships is challenging. The schema must be adaptable to evolving data requirements and scalable to handle large datasets.

- **Entity Resolution**: Identifying and merging duplicate entities from different sources (e.g., different representations of the same person or company).

- **Entity Linking & Relationships**: Accurately identifying and correctly associating entities with their corresponding entries in the knowledge graph is crucial for accuracy and understanding relationships.

## Knowledge Graph Use Cases

Some common use cases of knowledge graphs include:

- **Enhanced Data Integration and Interoperability**: Knowledge graphs unify disparate data sources by creating a structured representation of entities and their relationships, which facilitates seamless data integration and interoperability across various systems and domains.

- **Improved Search and Information Retrieval**: By leveraging the semantic relationships between data points, knowledge graphs enhance search capabilities, enabling more precise and context-aware information retrieval, thus improving the relevance and accuracy of search results.

- **Advanced Analytics and Insights Generation**: Knowledge graphs enable advanced analytics through complex querying and reasoning over interconnected data, allowing for the discovery of hidden patterns, insights, and trends that support informed decision-making and predictive analytics.

- **Personalized Recommendations and Content Discovery**: By capturing user preferences, behavior, and context in a knowledge graph, personalized recommendation systems can deliver tailored content, products, and services to users, enhancing user experience and engagement.


## How to Construct a Knowledge Graph with an LLM

### The construction process

Typically, you would follow these steps to construct a knowledge graph from unstructured text using an LLM:

1. Gather the data

2. Chunk the data

3. Vectorize the data

4. Pass the data to an LLM to extract nodes and relationships

5. Use the output to generate the graph

### Gather your data sources

The first step is to gather your unstructured data. The data can be in the form of text documents, PDFs, publicly available data, or any other source of information.

Depending on the format, you may need to reformat the data into a format (typically text) that the LLM can process.

The data sources should contain the information you want to include in your knowledge graph.

### Chunk the data

The next step is to break down the data into right-sized parts. This process is known as chunking.

The size of the chunks depends on the LLM you are using, the complexity of the data, and what you want to extract from the data.

You may not need to chunk the data if the LLM can process the entire document at once and it fits your requirements.

### Vectorize the data

Depending on your requirements for querying and searching the data, you may need to create **vector embeddings**. You can use any embedding model to create embeddings for each data chunk, but the same model must be used for all embeddings.

Placing these vectors into a [Vector index](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/?_gl=1*1i2o2lc*_gcl_au*MjEzNTI4NjkxNy4xNzU3MjU4NDMzLjc4MDQ1OTczLjE3NTg0MTY3NjUuMTc1ODQxNjc2NA..*_ga*MTkzMzgxNTk1LjE3NTcyNTg0MzQ.*_ga_DL38Q8KGQC*czE3NjM2MTQ1NzMkbzQ5JGcxJHQxNzYzNjIzMTI4JGo0MiRsMCRoMA..*_ga_DZP8Z65KK4*czE3NjM2MTQ1NzMkbzQ5JGcxJHQxNzYzNjIzMTI4JGo0MiRsMCRoMA..) allows you to perform semantic searches, similarity searches, and clustering on the data.

### Extract nodes and relationships

The next step is to pass the unstructured text data to the LLM to extract the nodes and relationships.

You should provide a suitable prompt that will instruct the LLM to:

- Identify the entities in the text.

- Extract the relationships between the entities.

- Format the output so you can use it to generate the graph, for example, as JSON or another structured format.

Optionally, you may also provide additional context or constraints for the extraction, such as the type of entities or relationships you are interested in extracting.

### Generate the graph

Finally, you can use the output from the LLM to generate the graph by creating the nodes and relationships within Neo4j.

The entity and relationship types would become labels and relationship types in the graph. The names would be the node and relationship identifiers.

You can view the current schema using the `db.schema.visualization()` function.

```cypher
CALL db.schema.visualization()
```

## Customize the schema

You can also customize:

- The prompt used to extract entities and relationships.

- The chunking strategy used to split the document into smaller pieces.

- Deleting disconnected nodes from the graph.

- De-duplicating nodes.

- Fine tuning any post processing of the graph.

