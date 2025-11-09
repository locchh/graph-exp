# MCP Servers

**Run Neo4j**

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

## [mcp-neo4j-cypher](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-cypher)

A Model Context Protocol server that allow LLM to interact with Neo4j database.

Config MCP:

```json
{
  "mcpServers": {
    "neo4j-cypher": {
      "command": "uvx",
      "args": [
        "mcp-neo4j-cypher@0.2.3",
        "--transport",
        "stdio"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "password",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

**Command Structure**

Always split commands into separate pieces. Instead of one long string: `uvx mcp-neo4j-cypher --transport stdio`

Use separate command and arguments:

```json
{"command": "uvx", "args": ["mcp-neo4j-cypher@0.2.3", "--transport", "stdio"]}
```

Use this question to check available tools: *Which MCP tools are available?  List their ID and description.*

- `get_neo4j_schema`: List all nodes, their attributes, and their relationships to other nodes in the Neo4j database. If this fails with a message that includes "Neo.ClientError.Procedure.ProcedureNotFound", suggest that the user install and enable the APOC plugin.


    *Describe the data model*

    *What node labels and relationship types are available in the database?*

    *How are Person and Movie related?*

    *What outgoing relationships does the User node have?*


- `read_neo4j_cypher`: Used to read data from the database. It does not have permissions to create, update, or delete data.

    *What are the top 10 movies by revenue?*

    *Who directed the movie "The Matrix"?*


- `write_neo4j_cypher`: Allows an agent to write data to the Neo4j database. This tool can create, update, or delete data in your database. It’s perfect for non-technical users who want to modify data using natural language instead of learning Cypher.

    *Create a new user named Sarah*

    *Add a 5-star rating from John to The Godfather*


## [mcp-neo4j-memory](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-memory)

A Model Context Protocol server that provides persistent memory capabilities through Neo4j graph database integration. The server offers these core tools.

Config MCP:

```json
{
  "mcpServers": {
    "neo4j-memory": {
      "command": "uvx",
      "args": [
        "mcp-neo4j-memory@0.2.0"
      ],
      "env": {
        "NEO4J_URL": "bolt://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "password",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

### 🔎 Query Tools
- `read_graph`
   - Read the entire knowledge graph
   - No input required
   - Returns: Complete graph with entities and relations

- `search_nodes`
   - Search for nodes based on a query
   - Input:
     - `query` (string): Search query matching names, types, observations
   - Returns: Matching subgraph

- `find_nodes`
   - Find specific nodes by name
   - Input:
     - `names` (array of strings): Entity names to retrieve
   - Returns: Subgraph with specified nodes

### ♟️ Entity Management Tools
- `create_entities`
   - Create multiple new entities in the knowledge graph
   - Input:
     - `entities`: Array of objects with:
       - `name` (string): Name of the entity
       - `type` (string): Type of the entity  
       - `observations` (array of strings): Initial observations about the entity
   - Returns: Created entities

- `delete_entities` 
   - Delete multiple entities and their associated relations
   - Input:
     - `entityNames` (array of strings): Names of entities to delete
   - Returns: Success confirmation

### 🔗 Relation Management Tools
- `create_relations`
   - Create multiple new relations between entities
   - Input:
     - `relations`: Array of objects with:
       - `source` (string): Name of source entity
       - `target` (string): Name of target entity
       - `relationType` (string): Type of relation
   - Returns: Created relations

- `delete_relations`
   - Delete multiple relations from the graph
   - Input:
     - `relations`: Array of objects with same schema as create_relations
   - Returns: Success confirmation

### 📝 Observation Management Tools
- `add_observations`
   - Add new observations to existing entities
   - Input:
     - `observations`: Array of objects with:
       - `entityName` (string): Entity to add to
       - `contents` (array of strings): Observations to add
   - Returns: Added observation details

- `delete_observations`
   - Delete specific observations from entities
   - Input:
     - `deletions`: Array of objects with:
       - `entityName` (string): Entity to delete from
       - `observations` (array of strings): Observations to remove
   - Returns: Success confirmation



## [mcp-neo4j-data-modeling](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-data-modeling)

Config:

```json
{
  "mcpServers": {
    "mcp-data-modeling": {
      "command": "uvx",
      "args": [
        "mcp-neo4j-data-modeling@0.1.1"
      ]
    },
    "mcp-cypher": {
      "command": "uvx",
      "args": [
        "mcp-neo4j-cypher@0.2.3"
      ],
      "env": {
        "NEO4J_URL": "bolt://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "password",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

[Data Modeling Assistant Demo](https://github.com/neo4j-field/data-modeling-assistant-demo/tree/main)

[Arrows App](https://arrows.app)