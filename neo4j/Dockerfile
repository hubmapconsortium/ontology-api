FROM hubmap/neo4j-image:4.2.5

# Change directory
WORKDIR /usr/src/app

# Set the environment variable for all subsequent instructions in the build stage 
ENV IMPORT=/usr/src/app/neo4j/import

# Copy files from host to image
COPY start.sh .

# Load the .csv files to populate neo4j before starting it up.
# This will take some time, but the data will be there when the constrarings are run
# in the next docker_compose setp 'neo4j-constraints'.
COPY import/*.csv ${IMPORT}/

# Change directory
WORKDIR /usr/src/app/neo4j/bin

# Import the CSV files into the ontology database using --database
# The default database is neo4j if no --database being used
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
