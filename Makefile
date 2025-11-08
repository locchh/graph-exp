.PHONY: up down clean

# Start Neo4j container with APOC plugin and default credentials
up:
	docker run -d \
	  --name neo4j \
	  -p 7474:7474 \
	  -p 7687:7687 \
	  -e NEO4J_PLUGINS='["apoc"]' \
	  -e NEO4J_apoc_export_file_enabled=true \
	  -e NEO4J_apoc_import_file_enabled=true \
	  -e NEO4J_AUTH=neo4j/password \
	  neo4j:latest

# Stop and remove Neo4j container and its volumes
down:
	docker stop neo4j || true
	docker rm neo4j -v || true

# Alias for neo4j-down (for convenience)
clean: down
