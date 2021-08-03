FROM neo4j:4.2

ENV USER=neo4j
ENV PASSWD=HappyG0at
# https://neo4j.com/docs/operations-manual/current/docker/introduction/#docker-overview
ENV NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
ENV NEO4J_AUTH=${USER}/${PASSWD}

EXPOSE 7687
EXPOSE 7474

ENV IMPORT=/usr/src/neo4j/import
RUN mkdir -p ${IMPORT}

# Load the .csv files to populate neo4j before starting it up.
# This will take some time, but the data will be there when the constrarings are run
# in the next docker_compose setp 'neo4j-constraints'.
COPY import/*.csv ${IMPORT}/
RUN neo4j-admin import --nodes=Semantic="${IMPORT}/TUIs.csv" --nodes=Concept="${IMPORT}/CUIs.csv" --nodes=Code="${IMPORT}/CODEs.csv" --nodes=Term="${IMPORT}/SUIs.csv" --nodes=Definition="${IMPORT}/DEFs.csv" --nodes=NDC="${IMPORT}/NDCs.csv" --relationships=ISA_STY="${IMPORT}/TUIrel.csv" --relationships=STY="${IMPORT}/CUI-TUIs.csv" --relationships="${IMPORT}/CUI-CUIs.csv" --relationships=CODE="${IMPORT}/CUI-CODEs.csv" --relationships="${IMPORT}/CODE-SUIs.csv" --relationships=PREF_TERM="${IMPORT}/CUI-SUIs.csv" --relationships=DEF="${IMPORT}/DEFrel.csv" --relationships=NDC="${IMPORT}/NDCrel.csv" --skip-bad-relationships --skip-duplicate-nodes

RUN rm -rf ${IMPORT}

CMD [ "neo4j" ]
