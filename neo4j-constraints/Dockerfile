FROM hubmap/neo4j-image:4.2.5

WORKDIR /usr/src/app

# Copy files from host to image
COPY . .

# Make the script executable
RUN chmod +x load_constraints.sh

# Export the path for running cypher-shell in load_constraints.sh
ENV PATH=/usr/src/app/neo4j/bin:$PATH

CMD ["./load_constraints.sh"]
