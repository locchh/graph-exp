- Vector retrieval:

```python
# Create Vector
plot_vector = Neo4jVector.from_existing_index(
    embedding_model,
    graph=graph,
    index_name="moviePlots",
    embedding_node_property="plotEmbedding",
    text_node_property="plot",
)

# Define functions for each step in the application

# Retrieve context 
def retrieve(state: State):
    # Use the vector to find relevant documents
    context = plot_vector.similarity_search(
        state["question"], 
        k=6
    )
    return {"context": context}
```

- vector + graph retrieval

```python
# Create Vector
plot_vector = Neo4jVector.from_existing_index(
    embedding_model,
    graph=graph,
    index_name="moviePlots",
    embedding_node_property="plotEmbedding",
    text_node_property="plot",
    retrieval_query=retrieval_query,
)

# Define functions for each step in the application

# Retrieve context 
def retrieve(state: State):
    # Use the vector to find relevant documents
    context = plot_vector.similarity_search(
        state["question"], 
        k=6,
    )
    return {"context": context}
```

- cypher retrieval

```python

# Create the Cypher QA chain
cypher_qa = GraphCypherQAChain.from_llm(
    graph=graph, 
    llm=model, 
    allow_dangerous_requests=True,
    return_direct=True,
)

# Define functions for each step in the application

# Retrieve context 
def retrieve(state: State):
    context = cypher_qa.invoke(
        {"query": state["question"]}
    )
    return {"context": context}
```