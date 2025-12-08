## Understanding the MCP Python SDK

The MCP Python SDK is a comprehensive library that implements the full Model Context Protocol specification for Python applications. It provides both client and server implementations, making it easy to create MCP servers that expose custom functionality to AI agents.

The SDK includes two main approaches for building servers:

- **FastMCP**: A high-level, decorator-based approach that makes it simple to create servers quickly

- **Low-level server**: A more flexible approach that gives you full control over the MCP protocol

## Core MCP Features

MCP servers expose three types of features to clients.

### 1. Tools

Tools are functions that LLMs can call to perform actions or retrieve data. Tools are perfect for tasks that LLMs struggle with, like counting or complex calculations.

**Characteristics:**

- Called by the LLM (model-controlled)

- Can have side effects (create, update, delete)

- Can perform computation

- Return structured results

**Use tools when:**

- You need to execute code or query a database

- The action depends on user input or context

- You want the LLM to decide when to use it

- You need deterministic results

Here’s a simple example of a tool that helps LLMs with counting - a task they typically struggle with:

```python
@mcp.tool()
def count_letters(text: str, search: str) -> int:
    """
    Count occurrences of a letter in the text.
    Use this tool when you need to find how many times a substring appears in a text.
    """
    return text.lower().count(search.lower())
```

The code sample uses decorators to register functions as MCP features. The `@mcp.tool()` decorator tells the server that the count_letters function should be used as an MCP tool. Reflection is then used to infer metadata about the tool.

1. The tool has two inputs: `text` and `search`, both of which are typed as strings.

2. The output of the tool is an int

3. The string in the opening line is used to describe what the tool does and and when it should be used.

The `@mcp.tool()` decorator accepts a number of optional arguments, which you will learn about later in the course.

### 2. Resources

Resources expose data that can be loaded into the LLM’s context, similar to a REST API endpoint.

**Characteristics:**

- Accessed by the client application (application-controlled)

- Read-only (no side effects)

- Typically static or parameterized URIs

- Provide context for the LLM

**Use resources when:**

- You want to expose data that doesn’t change often

- The client decides what to load (not the LLM)

- You’re providing reference information or documentation

- You need to expose specific entities by ID

```python
@mcp.resource("greeting://{who}")
def get_greeting(who: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {who}!"
```

### 3. Prompts

Prompts are pre-defined templates that help users interact with your server effectively.

**Characteristics:**

- Invoked by the user (user-controlled)

- Provide reusable templates

- Can accept parameters

- Guide the conversation

**Use prompts when:**

- You want to provide common workflows

- Users need help formulating requests

- You want to standardize interactions

- You need to ensure consistent input format

```python
@mcp.prompt(title="Count Letters")
def count_letters_prompt(text: str, search: str) -> str:
    """Template for counting letter occurrences."""
    return f"Count the occurrences of the letter '{search}' in the text:\n\n{text}"
```

## Putting It All Together

Here’s a complete example showing all three features working together. This code demonstrates:

1. Creating a FastMCP server instance

2. A tool that performs deterministic counting

3. A resource that provides parameterized data

4. A prompt that helps users formulate requests


```python
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Text Analysis Server")  # (1)

# Tool for deterministic counting
@mcp.tool()  # (2)
def count_letters(text: str, search: str) -> int:
    """Count occurrences of a letter in the text."""
    return text.lower().count(search.lower())

# Resource for reference data
@mcp.resource("greeting://{who}")  # (3)
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {who}!"

# Prompt template for common task
@mcp.prompt(title="Count Letters")  # (4)
def count_letters_prompt(text: str, search: str) -> str:
    """Template for letter counting task."""
    return f"Count the occurrences of the letter '{search}' in the text:\n\n{text}"


if __name__ == "__main__":
    mcp.run()
```

**Using the fastmcp command**

You can also run the server from the command line using the `fastmcp` command.

```bash
fastmcp run server.py
```

**VS Code Agent Mode**

You can also test your MCP server directly in VS Code by configuring it in .vscode/mcp.json and using the Chat window in Agent mode. This allows you to interact with your tools conversationally.

```json
{
  "servers": {
    "strawberry": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## Connecting to Neo4j

Now that you have a working MCP server, it’s time to connect it to a database.

In this lesson, you will learn how to connect your MCP server to Neo4j using FastMCP’s lifespan management feature to properly handle database connections.

```python
from neo4j import GraphDatabase

@mcp.tool()
def get_movies() -> list[dict]:
    """Get a list of movies"""
    # Creating a new driver for every tool call!
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run("MATCH (m:Movie) RETURN m LIMIT 10")
        return [record.data() for record in result]
    driver.close()
```

This approach has several problems:

- **Performance**: Creating a new driver connection for every tool call is slow and inefficient

- **Resource leaks**: If the tool fails, the driver may not be closed properly

- **Connection pooling**: Neo4j drivers maintain connection pools that should be reused across requests

- **Best practices**: The Neo4j driver should be created once and closed when the server shuts down

### Introducing Lifespan Management

FastMCP provides a lifespan feature that allows you to:

1. **Initialize resources** when the server starts (e.g., create database connections)

2. **Clean up resources** when the server shuts down (e.g., close connections)

3. **Share resources** across all tools and resources in your server

**The Lifespan Context Manager**

To share objects across the server, we can create a function that initializes resources when the server starts and cleans them up when it shuts down.

The function yields an object that contains the FastMCP server will make available to any tools and resources that request it.

```python
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from neo4j import AsyncGraphDatabase, AsyncDriver
from mcp.server.fastmcp import Context, FastMCP


# 1. Define a context class to hold your resources
# The context class holds all resources that should be shared across your server.
@dataclass
class AppContext:
    """Application context with shared resources."""
    driver: AsyncDriver
    database: str


# 2. Create the lifespan context manager
# The @asynccontextmanager decorator creates an async context manager. Code before yield runs at server startup, code in finally runs at server shutdown.
@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle."""

    # Startup: Read credentials from environment variables
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    database = os.getenv("NEO4J_DATABASE", "neo4j")

    # Initialize the Neo4j driver
    driver = AsyncGraphDatabase.driver(uri, auth=(username, password))

    try:
        # Yield the context with initialized resources
        yield AppContext(driver=driver, database=database)
    finally:
        # Shutdown: Clean up resources
        await driver.close()


# 3. Pass lifespan to the server
mcp = FastMCP("Movies GraphRAG Server", lifespan=app_lifespan)


# 4. Access the driver in your tools
@mcp.tool()
async def graph_statistics(ctx: Context) -> dict[str, int]:
    """Count the number of nodes and relationships in the graph."""

    # Access the driver from lifespan context
    driver = ctx.request_context.lifespan_context.driver

    # Use the driver to query Neo4j
    records, summary, keys = await driver.execute_query(
        "RETURN COUNT {()} AS nodes, COUNT {()-[]-()} AS relationships"
    )

    # Process the results
    if records:
        return dict(records[0])
    return {"nodes": 0, "relationships": 0}
```

**What else can Context be used for?**

Beyond accessing lifespan resources, the Context object can also be used to:

- **Access request metadata** - Information about the current tool invocation

- **Log messages** - Use `ctx.info()`, `ctx.warning()`, and `ctx.error()` to send log messages to the client

- **Send progress updates** - Keep the client informed during long-running operations

- **Access client information** - Metadata about the calling agent or application

### Benefits of Lifespan Management

Using lifespan management provides several advantages:

- **Performance**: Database connections are created once and reused across all tool calls

- **Reliability**: Resources are properly cleaned up when the server shuts down

- **Best practices**: Follows Neo4j driver best practices for connection management

- **Type safety**: The context object can be strongly typed for better IDE support

- **Testability**: Makes it easier to mock database connections in tests


## Using Context within Tools

In the previous lesson, you learned how to use lifespan management to initialize and share resources like the Neo4j driver across your MCP server.

But how do your tools actually access these resources? And how can you provide feedback to users during long-running operations?

This is where the **Context object** comes in.

### What is the Context Object?

The Context object is automatically injected into tools and resources that request it. It provides access to:

- **Lifespan resources** - Database connections, configuration, etc.

- **Logging methods** - Send messages to the client at different log levels

- **Progress reporting** - Show progress for long-running operations

- **Resource reading** - Access other resources from within tools

- **Session information** - Request metadata and client capabilities


To use the Context in a tool or resource, simply add a parameter with the Context type annotation:

```python
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("Movies GraphRAG Server")


@mcp.tool()
async def my_tool(query: str, ctx: Context) -> str:
    """A tool that uses the context."""

    # The context is automatically injected by FastMCP
    # The parameter can have any name, but must be type-annotated

    return await process_query(query, ctx)
```

A Complete Example:

```python
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("Movies GraphRAG Server")

@mcp.tool()
async def count_movie_nodes(ctx: Context) -> dict:
    """Count different types of nodes in the movie graph."""

    # Access the Neo4j driver from lifespan context
    driver = ctx.request_context.lifespan_context.driver

    # Initialize results
    results = {}

    # Define queries to run
    queries = [
        ("Person", "MATCH (p:Person) RETURN count(p) AS count"),
        ("Movie", "MATCH (m:Movie) RETURN count(m) AS count"),
        ("Genre", "MATCH (g:Genre) RETURN count(g) AS count"),
        ("User", "MATCH (u:User) RETURN count(u) AS count")
    ]

    # Log start of operation
    await ctx.info("Starting node count analysis...")

    # Execute each query and track progress
    for i, (label, query) in enumerate(queries):
        # Report progress (0-based index)
        await ctx.report_progress(
            progress=i,
            total=len(queries),
            message=f"Counting {label} nodes..."
        )

        # Execute query
        records, _, _ = await driver.execute_query(query)
        count = records[0]["count"]

        # Store and log result
        results[label] = count
        await ctx.info(f"Found {count} {label} nodes")

    # Report completion
    await ctx.report_progress(
        progress=len(queries),
        total=len(queries),
        message="Analysis complete!"
    )

    return results
```

### Understanding the Components

#### 1.Understanding the Components

```python
# Access Neo4j driver from the lifespan context
driver = ctx.request_context.lifespan_context.driver
```

#### 2. Logging

```python
await ctx.info("Starting node count analysis...")
await ctx.info(f"Found {count} {label} nodes")
```
The Context provides logging methods to keep users informed:

- **debug** - Detailed technical information

- **info** - General progress updates

- **warning** - Non-critical issues

- **error** - Error conditions

#### 1.Understanding the Components

```python
await ctx.report_progress(
    progress=i,
    total=len(queries),
    message=f"Counting {label} nodes..."
)
```

Progress reporting keeps users informed during long-running operations:

- **progress** - Current step (0-based)

- **total** - Total number of steps

- **message** - Optional status message


#### 4. Structured Results

```python
results = {}
# ...
results[label] = count
```

The tool returns a dictionary of results, which will be converted to structured output by the client.

### Common Usage Patterns

The Context object is useful when a server needs to run complex tasks and provide updates to the client:


- **Complex database operations** - When searching through movie relationships, use transactions to ensure data consistency while keeping users informed with progress updates

- **Meaningful feedback** - Use the Context’s logging methods to provide appropriate feedback: warnings for missing data and error messages for database issues

- **Tool composition** - One tool can invoke another through the Context, allowing you to build complex operations from simpler ones

- **User-friendly operations** - Combine error handling and progress reporting to create tools that are both powerful and informative


## Create a Movie Resource

```python
@mcp.resource("movie://{tmdb_id}")
async def get_movie(tmdb_id: str, ctx: Context) -> str:
    """
    Get detailed information about a specific movie by TMDB ID.

    Args:
        tmdb_id: The TMDB ID of the movie (e.g., "603" for The Matrix)

    Returns:
        Formatted string with movie details including title, plot, cast, and genres
    """
    await ctx.info(f"Fetching movie details for TMDB ID: {tmdb_id}")

    context = ctx.request_context.lifespan_context

    try:
        records, _, _ = await context.driver.execute_query(
            """
            MATCH (m:Movie {tmdbId: $tmdb_id})
            RETURN m.title AS title,
               m.released AS released,
               m.tagline AS tagline,
               m.runtime AS runtime,
               m.plot AS plot,
               [ (m)-[:IN_GENRE]->(g:Genre) | g.name ] AS genres,
               [ (p)-[r:ACTED_IN]->(m) | {name: p.name, role: r.role} ] AS actors,
               [ (d)-[:DIRECTED]->(m) | d.name ] AS directors
            """,
            tmdb_id=tmdb_id,
            database_=context.database
        )

        if not records:
            await ctx.warning(f"Movie with TMDB ID {tmdb_id} not found")
            return f"Movie with TMDB ID {tmdb_id} not found in database"

        movie = records[0].data()

        # Format the output
        output = []
        output.append(f"# {movie['title']} ({movie['released']})")
        output.append("")

        if movie['tagline']:
            output.append(f"_{movie['tagline']}_")
            output.append("")

        output.append(f"**Runtime:** {movie['runtime']} minutes")
        output.append(f"**Genres:** {', '.join(movie['genres'])}")

        if movie['directors']:
            output.append(f"**Director(s):** {', '.join(movie['directors'])}")

        output.append("")
        output.append("## Plot")
        output.append(movie['plot'])

        if movie['actors']:
            output.append("")
            output.append("## Cast")
            for actor in movie['actors']:
                if actor['role']:
                    output.append(f"- {actor['name']} as {actor['role']}")
                else:
                    output.append(f"- {actor['name']}")

        result = "\n".join(output)

        await ctx.info(f"Successfully fetched details for '{movie['title']}'")

        return result

    except Exception as e:
        await ctx.error(f"Failed to fetch movie: {str(e)}")
        raise
```

## Handling Large Datasets with Pagination

When working with large datasets in Neo4j, returning all data at once can be slow, consume excessive memory, and overwhelm clients. Pagination solves this by returning data in smaller, manageable chunks.

### Understanding Cursor-Based Pagination

Pagination allows you to fetch data in smaller **pages** or **batches**. MCP uses **cursor-based pagination**, where a cursor (opaque string) marks your position in the dataset.

**How it works:**

1. Client requests the first page (no cursor)

2. Server returns the first batch + a cursor to the next page

3. Client requests the next page using the cursor

4. Server returns the next batch + a new cursor

5. Process repeats until no cursor is returned (end of data)


### Implementing Pagination in Neo4j

To implement pagination in a Cypher query, use Neo4j’s `SKIP` and `LIMIT` clauses. The following query returns the first 100 movies:

```cypher
MATCH (m:Movie)
RETURN m.title
ORDER BY m.title
SKIP 0 LIMIT 100  // First page (0-99)
```

The following query skips the first 100 movies and returns the next 100 movies:

```cypher
MATCH (m:Movie)
RETURN m.title
ORDER BY m.title
SKIP 100 LIMIT 100  // Second page (100-199)
```

**The cursor** is simply the skip value encoded as a string.

Unfortunately, FastMCP doesn’t directly support pagination in its high-level decorator API. However, you can implement pagination manually by:


1. Accepting a page or cursor parameter in your tool

2. Converting the cursor to a skip value

3. Querying with SKIP and LIMIT

4. Returning both the data and the next cursor

**Pagination as a Tool**

Since FastMCP’s `@mcp.resource()` decorator doesn’t support pagination parameters, we can implement pagination as a tool instead:

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def list_movies_paginated(
    cursor: str = "0",
    page_size: int = 50,
    ctx: Context = None
) -> dict:
    """
    List movies with pagination support.

    Args:
        cursor: Pagination cursor (skip value as string, default "0")
        page_size: Number of movies per page (default 50)

    Returns:
        Dictionary with 'movies' list and 'next_cursor' for next page
    """

    # Convert cursor to skip value
    skip = int(cursor)

    await ctx.info(f"Fetching movies {skip} to {skip + page_size}...")

    # Access driver
    driver = ctx.request_context.lifespan_context.driver

    # Query with SKIP and LIMIT
    records, summary, keys = await driver.execute_query(
        """
        MATCH (m:Movie)
        RETURN m.title AS title, m.released AS released
        ORDER BY m.title
        SKIP $skip
        LIMIT $limit
        """,
        skip=skip,
        limit=page_size
    )

    movies = [record.data() for record in records]

    # Calculate next cursor
    # If we got a full page, there might be more data
    next_cursor = None
    if len(movies) == page_size:
        next_cursor = str(skip + page_size)

    await ctx.info(f"Returned {len(movies)} movies")

    return {
        "movies": movies,
        "next_cursor": next_cursor,
        "current_page": skip // page_size,
        "page_size": page_size
    }
```

### Best Practices for Pagination

1. **Consistent ordering** - Always use `ORDER BY` to ensure consistent results across pages

2. **Reasonable page sizes** - Default to 20-50 items per page for good user experience

3. **Include metadata** - Return page number, total pages (if known), and `has_more` flag

4. **Handle invalid cursors** - Validate cursor values and handle errors gracefully

5. **Optimize queries** - Use indexes on properties used in `ORDER BY` and `WHERE` clauses

6. **Consider total counts** - For some UIs, include total count (but this adds query overhead)

## Sampling: Dynamic LLM Interactions

Sampling allows your tools to call the LLM during execution. Instead of just returning data from the database, a tool can ask the LLM that powers the Agent to transform, explain, or enhance that data.

For example, a tool could retrieve movie information from Neo4j and then ask the LLM to convert the strctured data into a natural language description:

```python
@mcp.tool()
async def explain_movie_data(movie_title: str, ctx: Context) -> str:
    """Get a natural language explanation of movie data."""

    # Get movie data from Neo4j
    movie_data = await get_movie_details(movie_title, ctx)

    # Ask LLM to explain the data
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(
                    text=f"Describe {movie_data['title']} ({movie_data['released']}) " +
                         f"starring {', '.join(movie_data['actors'])}. " +
                         "Write 2-3 engaging sentences."
                )
            )
        ],
        max_tokens=200
    )

    return result.content.text if result.content.type == "text" else str(result.content)
```

Use sampling when you need:

- Natural language generation from structured data

- Dynamic summaries based on query results

- Content that adapts to the specific data retrieved

- Recommendations or insights derived from data


**Sampling Requirements**

Sampling requires client support and adds processing overhead. The client must support the sampling capability for this feature to work.

## Completions: Smart Parameter Suggestions

Completions provide autocomplete suggestions when users are filling in tool parameters or resource URIs. This helps users discover valid values without memorizing them.

For example, when a user starts typing a genre name, completions can suggest matching options from the database:

```python
@server.complete()
async def handle_completion(
    ref: types.PromptReference | types.ResourceReference,
    argument: types.CompleteArgument
) -> CompleteResult:
    """Provide genre completions."""

    if argument.name == "genre":
        records, _, _ = await driver.execute_query(
            """
            MATCH (g:Genre)
            WHERE g.name STARTS WITH $prefix
            RETURN g.name AS name
            ORDER BY name ASC LIMIT 10
            """,
            prefix=argument.value
        )

        return CompleteResult(
            completion=Completion(
                values=[record["label"] for record in records]
            )
        )

    return CompleteResult(completion=Completion(values=[]))
```

Use completions when:

- Users need to discover valid parameter values

- Your tools accept specific values from a dataset

- You want to improve user experience with suggestions

- Form-based interfaces benefit from autocomplete

**Using the Low-Level Server API**

Completions require using the low-level `Server` API instead of FastMCP’s decorator-based approach.