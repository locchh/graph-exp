# Setup

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

## Import data

- Add person node `persons.csv` file.

- Add movie node `movies.csv` file.

- Setting the unique ID for the Movie node to movieId, a unique constraint named `movieId_Movie_uniq` is created against the movieId property.

- An index is created automatically for the unique ID property. For example, the index movieId_Movie_uniq will be created for the movieId property on the Movie node.

- Create relationship `acted_in.csv` file.

- Create relationship `directed.csv` file.

- Add  `ratings.csv` file.