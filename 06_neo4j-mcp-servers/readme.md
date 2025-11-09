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

Related:

- [Data Modeling Assistant Demo](https://github.com/neo4j-field/data-modeling-assistant-demo/tree/main)

- [Arrows App](https://arrows.app)

Example: *I need to import data from the CSV files @data into my empty Neo4j database. Please use the appropriate MCP server to help me with this task.*

### 📦 Resources

The server provides these resources:

#### Schema 

- `resource://schema/node`
   - Get the JSON schema for a Node object
   - Returns: JSON schema defining the structure of a Node

- `resource://schema/relationship`
   - Get the JSON schema for a Relationship object
   - Returns: JSON schema defining the structure of a Relationship

- `resource://schema/property`
   - Get the JSON schema for a Property object
   - Returns: JSON schema defining the structure of a Property

- `resource://schema/data_model`
   - Get the JSON schema for a DataModel object
   - Returns: JSON schema defining the structure of a DataModel

#### Example Data Models

- `resource://examples/patient_journey_model`
   - Get a real-world Patient Journey healthcare data model in JSON format
   - Returns: JSON DataModel for tracking patient encounters, conditions, medications, and care plans

- `resource://examples/supply_chain_model`
   - Get a real-world Supply Chain data model in JSON format
   - Returns: JSON DataModel for tracking products, orders, inventory, and locations

- `resource://examples/software_dependency_model`
   - Get a real-world Software Dependency Graph data model in JSON format
   - Returns: JSON DataModel for software dependency tracking with security vulnerabilities, commits, and contributor analysis

- `resource://examples/oil_gas_monitoring_model`
   - Get a real-world Oil and Gas Equipment Monitoring data model in JSON format
   - Returns: JSON DataModel for industrial monitoring of oil and gas equipment, sensors, alerts, and maintenance

- `resource://examples/customer_360_model`
   - Get a real-world Customer 360 data model in JSON format
   - Returns: JSON DataModel for customer relationship management with accounts, contacts, orders, tickets, and surveys

- `resource://examples/fraud_aml_model`
   - Get a real-world Fraud & AML data model in JSON format
   - Returns: JSON DataModel for financial fraud detection and anti-money laundering with customers, transactions, alerts, and compliance

- `resource://examples/health_insurance_fraud_model`
   - Get a real-world Health Insurance Fraud Detection data model in JSON format
   - Returns: JSON DataModel for healthcare fraud detection tracking investigations, prescriptions, executions, and beneficiary relationships


#### Ingest

- `resource://neo4j_data_ingest_process`
   - Get a detailed explanation of the recommended process for ingesting data into Neo4j using the data model
   - Returns: Markdown document explaining the ingest process


### 🛠️ Tools

The server offers these core tools:

#### ✅ Validation Tools
- `validate_node`
   - Validate a single node structure
   - Input:
     - `node` (Node): The node to validate
   - Returns: True if valid, raises ValueError if invalid

- `validate_relationship`
   - Validate a single relationship structure
   - Input:
     - `relationship` (Relationship): The relationship to validate
   - Returns: True if valid, raises ValueError if invalid

- `validate_data_model`
   - Validate the entire data model structure
   - Input:
     - `data_model` (DataModel): The data model to validate
   - Returns: True if valid, raises ValueError if invalid

#### 👁️ Visualization Tools
- `get_mermaid_config_str`
   - Generate a Mermaid diagram configuration string for the data model, suitable for visualization in tools that support Mermaid
   - Input:
     - `data_model` (DataModel): The data model to visualize
   - Returns: Mermaid configuration string representing the data model

#### 🔄 Import/Export Tools

These tools provide integration with **[Arrows](https://arrows.app/)** - a graph drawing web application for creating detailed Neo4j data models with an intuitive visual interface.

- `load_from_arrows_json`
   - Load a data model from Arrows app JSON format
   - Input:
     - `arrows_data_model_dict` (dict): JSON dictionary from Arrows app export
   - Returns: DataModel object

- `export_to_arrows_json`
   - Export a data model to Arrows app JSON format
   - Input:
     - `data_model` (DataModel): The data model to export
   - Returns: JSON string compatible with Arrows app

- `load_from_owl_turtle`
   - Load a data model from OWL Turtle format
   - Input:
     - `owl_turtle_str` (str): OWL Turtle string representation of an ontology
   - Returns: DataModel object with nodes and relationships extracted from the ontology
   - Note: **This conversion is lossy** - OWL Classes become Nodes, ObjectProperties become Relationships, and DatatypeProperties become Node properties.

- `export_to_owl_turtle`
   - Export a data model to OWL Turtle format
   - Input:
     - `data_model` (DataModel): The data model to export
   - Returns: String representation of the data model in OWL Turtle format
   - Note: **This conversion is lossy** - Relationship properties are not preserved since OWL does not support properties on ObjectProperties

#### 📚 Example Data Model Tools

These tools provide access to pre-built example data models for common use cases and domains.

- `list_example_data_models`
   - List all available example data models with descriptions
   - Input: None
   - Returns: Dictionary with example names, descriptions, node/relationship counts, and usage instructions

- `get_example_data_model`
   - Get an example graph data model from the available templates
   - Input:
     - `example_name` (str): Name of the example to load ('patient_journey', 'supply_chain', 'software_dependency', 'oil_gas_monitoring', 'customer_360', 'fraud_aml', or 'health_insurance_fraud')
   - Returns: ExampleDataModelResponse containing DataModel object and Mermaid visualization configuration

#### 📝 Cypher Ingest Tools

These tools may be used to create Cypher ingest queries based on the data model. These queries may then be used by other MCP servers or applications to load data into Neo4j.

- `get_constraints_cypher_queries`
   - Generate Cypher queries to create constraints (e.g., unique keys) for all nodes in the data model
   - Input:
     - `data_model` (DataModel): The data model to generate constraints for
   - Returns: List of Cypher statements for constraints

- `get_node_cypher_ingest_query`
   - Generate a Cypher query to ingest a list of node records into Neo4j
   - Input:
     - `node` (Node): The node definition (label, key property, properties)
   - Returns: Parameterized Cypher query for bulk node ingestion (using `$records`)

- `get_relationship_cypher_ingest_query`
   - Generate a Cypher query to ingest a list of relationship records into Neo4j
   - Input:
     - `data_model` (DataModel): The data model containing nodes and relationships
     - `relationship_type` (str): The type of the relationship
     - `relationship_start_node_label` (str): The label of the start node
     - `relationship_end_node_label` (str): The label of the end node
   - Returns: Parameterized Cypher query for bulk relationship ingestion (using `$records`)

### 💡 Prompts

- `create_new_data_model`
   - Provide a structured parameterized prompt for generating a new graph data model
   - Input:
     - `data_context` (str): Description of the data and any specific details to focus on
     - `use_cases` (str): List of use cases for the data model to address
     - `desired_nodes` (str, optional): Node labels to include in the data model
     - `desired_relationships` (str, optional): Relationship types to include in the data model
   - Returns: Structured prompt that guides the agent through a 3-step process: analysis of sample data and examples, generation of the data model with validation, and presentation of results with visualization 