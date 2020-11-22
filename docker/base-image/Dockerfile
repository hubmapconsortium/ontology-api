# Parent image
FROM centos:8

LABEL description="Neo4j for HuBMAP" \
	version="1.0"

# Change to directory that contains the Dockerfile
WORKDIR /usr/src/app

# Copy from host to image
COPY apoc-4.1.0.0-all.jar /usr/src/app/
COPY start.sh /usr/src/app/


# Reduce the number of layers in image by minimizing the number of separate RUN commands
# 1 - Update the package listings
# 2 - Install wget and OpenJDK 11
# 3 - Download neo4j community server
# 4 - Extract neo4j tarball
# 5 - Rename folder to neo4j
# 6 - Move the apoc jar to neo4j plugins
# 7 - Remove the downloaded neo4j tarball
# 8 - Clean all yum cache

RUN yum update -y && \
    yum install -y wget java-11-openjdk-devel && \
    wget http://dist.neo4j.org/neo4j-community-4.1.4-unix.tar.gz && \
    tar -zxvf neo4j-community-4.1.4-unix.tar.gz && \
    mv neo4j-community-4.1.4 neo4j && \
    rm neo4j-community-4.1.4-unix.tar.gz && \
    yum clean all

# Make the start script executable
RUN chmod +x /usr/src/app/start.sh

# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime. 
# EXPOSE does not make the ports of the container accessible to the host.
EXPOSE 7474 7687

# Start the neo4j server when container spins up
CMD ["/usr/src/app/start.sh"]
