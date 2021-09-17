FROM hubmap/neo4j-image:4.2.5
# https://github.com/hubmapconsortium/neo4j-docker/blob/master/neo4j-image/Dockerfile

# Change directory
WORKDIR /usr/src/app

# Copy files from host to image
COPY start.sh .
COPY set_constraints.cypher .
COPY neo4j.conf /usr/src/app/neo4j/conf

# Set the environment variable for all subsequent instructions in the build stage
ENV IMPORT=/usr/src/app/neo4j/import

# Load the .csv files to populate neo4j before starting it up.
# This will take some time, but the data will be there when the constraints are run
# in the next docker_compose step 'neo4j-constraints'.
# NOTE: in the repository the 'import/' directory contains one of more directries which contain the UMLS Graph Extracts.
# These change from time to time, and so the .csv files need to be augmented with other onthologies (see 'scipts/').
# So, 'current/' is actually a sybolic link to the current UMLS directory (e.g., 'import/UMLS-Graph-Extracts-2021AA/').
# BIG NOTE: Nice idea, but Docker does not follow symbolic links, so you need to make the link to 'current/' a HARD one
# (e.g., cd import; mv UMLS-Graph-Extracts-2021AA current).
COPY import/current/*.csv ${IMPORT}/

# Change directory
WORKDIR /usr/src/app/neo4j/bin

# Import the CSV files into the ontology database using --database
# The default database is neo4j if no --database being used
# NOTE: The NDC nodes (NDCs.csv), and relationships (NDCrel.csv) are not imported at this time.
RUN ./neo4j-admin import --verbose --database=ontology --nodes=Semantic="${IMPORT}/TUIs.csv" --nodes=Concept="${IMPORT}/CUIs.csv" --nodes=Code="${IMPORT}/CODEs.csv" --nodes=Term="${IMPORT}/SUIs.csv" --nodes=Definition="${IMPORT}/DEFs.csv" --relationships=ISA_STY="${IMPORT}/TUIrel.csv" --relationships=STY="${IMPORT}/CUI-TUIs.csv" --relationships="${IMPORT}/CUI-CUIs.csv" --relationships=CODE="${IMPORT}/CUI-CODEs.csv" --relationships="${IMPORT}/CODE-SUIs.csv" --relationships=PREF_TERM="${IMPORT}/CUI-SUIs.csv" --relationships=DEF="${IMPORT}/DEFrel.csv" --skip-bad-relationships --skip-duplicate-nodes

# - Install curl
# - Make the start script executable
# - Remove those big CSV files
RUN yum install -y curl && \
    chmod +x /usr/src/app/start.sh && \
    rm -rf ${IMPORT}/*

# The EXPOSE instruction informs Docker that the container 
# listens on the specified network ports at runtime
EXPOSE 7474 7687

# Start the neo4j server when container spins up
CMD ["/usr/src/app/start.sh"]
