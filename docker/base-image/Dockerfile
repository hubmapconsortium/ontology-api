# Parent image
FROM centos:7

LABEL description="Neo4j for HuBMAP" \
	version="1.0"

# Change to directory that contains the Dockerfile
WORKDIR /usr/src/app

# Copy from host to image
COPY . .

# Reduce the number of layers in image by minimizing the number of separate RUN commands
# 1 - Update the package listings
# 2 - Install wget and OpenJDK 8
# 3 - Download neo4j community server
# 4 - Extract neo4j tarball
# 5 - Rename folder to neo4j
# 6 - Move the apoc jar to neo4j plugins
# 7 - Remove the downloaded neo4j tarball
# 8 - Clean all yum cache
RUN yum update -y && \
    yum install -y wget java-1.8.0-openjdk && \
    wget http://dist.neo4j.org/neo4j-community-3.5.12-unix.tar.gz && \
    tar -zxvf neo4j-community-3.5.12-unix.tar.gz && \
    mv neo4j-community-3.5.12 neo4j && \
    mv apoc-3.5.0.5-all.jar neo4j/plugins && \
    rm neo4j-community-3.5.12-unix.tar.gz && \
    yum clean all
    
# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime. 
# EXPOSE does not make the ports of the container accessible to the host.
EXPOSE 7474 7687
