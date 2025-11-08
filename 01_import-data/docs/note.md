## Source data

When you import data into Neo4j, you typically start with a set of source files. You may have exported this source data from:

- Relational databases
- Web APIs
- Public data directories
- BI tools
- Spreadsheets (e.g. Excel or Google Sheets)

Before you start the import process, you should:

- Understand the data in the source CSV files.
- Inspect and clean (if necessary) the data in the source data files.
- Understand the graph data model you will be implementing during the import.

The import involves creating Cypher code to:

- Read the source data.
- Transform the data as needed.
- Create nodes, relationships, and properties to create the graph.

## Normalized Data

**Definition:** Data is organized to minimize redundancy by separating it into multiple related tables (in relational databases) or nodes (in graph databases).

**Characteristics:**
- Minimizes data duplication
- Reduces update anomalies (insert, update, delete)
- Maintains data integrity through relationships
- Requires joins/relationships to reconstruct complete information

```cypher
# Normalized Tables
CUSTOMERS (customer_id, name, email)
ORDERS (order_id, customer_id, order_date)
ORDER_ITEMS (order_id, product_id, quantity)
PRODUCTS (product_id, name, price)
```

Example in Graph Database (Normalized):

```cypher
(customer:Customer {id: 1, name: "John"})-[:PLACED]->(order:Order {id: 101, date: "2023-11-08"})
(order)-[:CONTAINS]->(product:Product {id: 1001, name: "Laptop", price: 999})
```

## Denormalized Data

**Definition:** Data is stored with some redundancy to optimize read performance, often by duplicating data across multiple records.

**Characteristics:**

- Improves read performance by reducing joins
- Increases storage requirements
- Can lead to update anomalies if not managed carefully
- Simplifies queries by keeping related data together

Example in Document Database:

```json
{
  "order_id": 101,
  "customer": {
    "name": "John",
    "email": "john@example.com"
  },
  "items": [
    {
      "product_name": "Laptop",
      "price": 999,
      "quantity": 1
    }
  ]
}
```

Example in Graph Database (Denormalized):

```cypher
// Some properties duplicated for faster access
(order:Order {
  id: 101, 
  date: "2023-11-08",
  customer_name: "John",  // Denormalized from Customer
  total: 999
})-[:CONTAINS]->(product:Product {id: 1001, name: "Laptop"})
```