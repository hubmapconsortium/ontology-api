FROM hubmap/neo4j-image:4.2.5

ENV USER=neo4j
ENV PASSWD=HappyG0at

# ontology-neo4j is the container's hostname
ENV BOLT_URL=bolt://ontology-neo4j:7687

ENV IMPORT=/usr/src/app/neo4j/import

COPY load_constraints.sh ${IMPORT}
RUN chmod +x ${IMPORT}/load_constraints.sh
COPY set_constraints.cypher ${IMPORT}

# Export the path for running cypher-shell in load_constraints.sh
ENV PATH=/usr/src/app/neo4j/bin:$PATH

RUN echo $PATH

CMD ${IMPORT}/load_constraints.sh ${USER} ${PASSWD} ${BOLT_URL} ${IMPORT}
