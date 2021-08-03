FROM neo4j:4.2

ENV USER=neo4j
ENV PASSWD=HappyG0at
ENV BOLT_URL=bolt://neo4j:7687

ENV IMPORT=/usr/src/neo4j/import
RUN mkdir -p ${IMPORT}

COPY load_constraints.sh ${IMPORT}
RUN chmod +x ${IMPORT}/load_constraints.sh
COPY set_constraints.cypher ${IMPORT}

CMD ${IMPORT}/load_constraints.sh ${USER} ${PASSWD} ${BOLT_URL} ${IMPORT}
