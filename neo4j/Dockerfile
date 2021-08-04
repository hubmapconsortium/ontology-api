FROM hubmap/neo4j-image:4.2.5

# Install curl to be used by Docker Healthcheck
RUN yum install -y curl 

ENV IMPORT=/usr/src/app/neo4j/import

# Load the .csv files to populate neo4j before starting it up.
# This will take some time, but the data will be there when the constrarings are run
# in the next docker_compose setp 'neo4j-constraints'.
COPY import/*.csv ${IMPORT}/

# Change directory
WORKDIR /usr/src/app/neo4j/bin

# Import the CSV files
RUN ./neo4j-admin import --verbose --nodes=Semantic="${IMPORT}/TUIs.csv" --nodes=Concept="${IMPORT}/CUIs.csv" --nodes=Code="${IMPORT}/CODEs.csv" --nodes=Term="${IMPORT}/SUIs.csv" --nodes=Definition="${IMPORT}/DEFs.csv" --nodes=NDC="${IMPORT}/NDCs.csv" --relationships=ISA_STY="${IMPORT}/TUIrel.csv" --relationships=STY="${IMPORT}/CUI-TUIs.csv" --relationships="${IMPORT}/CUI-CUIs.csv" --relationships=CODE="${IMPORT}/CUI-CODEs.csv" --relationships="${IMPORT}/CODE-SUIs.csv" --relationships=PREF_TERM="${IMPORT}/CUI-SUIs.csv" --relationships=DEF="${IMPORT}/DEFrel.csv" --relationships=NDC="${IMPORT}/NDCrel.csv" --skip-bad-relationships --skip-duplicate-nodes

# Remove those big CSV files
RUN rm -rf ${IMPORT}/*

# Set the password for native user `neo4j` (must be performed before starting up the database for the first time)
RUN ./neo4j-admin set-initial-password HappyG0at

EXPOSE 7474 7687

# Start the neo4j server when container spins up
# Use `console` instead of `start` to keep the terminal window stay open
CMD ["/usr/src/app/neo4j/bin/neo4j", "console"]
