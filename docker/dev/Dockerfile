# Parent image
FROM hubmap/ontology-api:latest

LABEL description="Neo4j dev version for HuBMAP Ontology" \
	version="1.0"

# Change to directory that contains the Dockerfile
WORKDIR /usr/src/app

# Copy from host to image
COPY . .
COPY neo4j.conf /usr/src/app/neo4j/conf/neo4j.conf

# Make the start script executable
RUN chmod +x start.sh
    
# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime. 
# EXPOSE does not make the ports of the container accessible to the host.
EXPOSE 7474 7687

# Start the neo4j server when container spins up
CMD ["./start.sh"]
