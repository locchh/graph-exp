
## Setup

- Neo4j:

```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

- Config MCP (Test by asking AI *Which MCP tools are available?  List their ID and description.*):

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

#### Tools

- `get_neo4j_schema`: List all nodes, their attributes, and their relationships to other nodes in the Neo4j database. If this fails with a message that includes "Neo.ClientError.Procedure.ProcedureNotFound", suggest that the user install and enable the APOC plugin.

- `read_neo4j_cypher`: Execute a read Cypher query on the Neo4j database.

- `write_neo4j_cypher`: Execute a write Cypher query on the Neo4j database.


### [mcp-neo4j-memory](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-memory)

### [mcp-neo4j-data-modeling](https://github.com/neo4j-contrib/mcp-neo4j/tree/main/servers/mcp-neo4j-data-modeling)

## References

https://neo4j.com/developer/genai-ecosystem/model-context-protocol-mcp/

https://neo4j.com/blog/developer/neo4j-data-modeling-mcp-server/

https://github.com/neo4j-contrib/mcp-neo4j

https://github.com/neo4j-graphacademy/importing-data

https://github.com/neo4j-graphacademy/llm-vectors-unstructured

https://github.com/neo4j-graphacademy/genai-fundamentals

https://github.com/neo4j-graphacademy/genai-integration-langchain

https://github.com/neo4j-graphacademy/llm-knowledge-graph-construction

https://github.com/neo4j-graphacademy/genai-mcp-neo4j-tools

https://kuzudb.github.io/docs/

https://docs.astral.sh/uv/

https://github.com/neo4j-graph-examples