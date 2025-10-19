## Setup

- Neo4j:

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

- Config MCP:

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

## MCP Servers

**Command Structure**

Always split commands into separate pieces. Instead of one long string: `uvx mcp-neo4j-cypher --transport stdio`

Use separate command and arguments:

```json
{"command": "uvx", "args": ["mcp-neo4j-cypher@0.2.3", "--transport", "stdio"]}
```

### [mcp-neo4j-cypher](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-cypher)

*Which MCP tools are available?  List their ID and description.*

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


### [mcp-neo4j-memory](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-memory)



### [mcp-neo4j-data-modeling](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-data-modeling)