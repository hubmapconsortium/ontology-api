# Parent image
FROM hubmap/api-base-image:latest

LABEL description="HuBMAP Ontology API Service"

# Change to directory that contains the Dockerfile
WORKDIR /usr/src/app

# Copy from host to image
COPY . .

# Install dependencies with pip (pip3 also works)
RUN pip install -r requirements.txt

# The EXPOSE instruction informs Docker that the container listens on the specified network ports at runtime. 
# EXPOSE does not make the ports of the container accessible to the host.
EXPOSE 5000

# Set an entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Finally, we run uWSGI with the ini file
CMD [ "uwsgi", "--ini", "/usr/src/app/uwsgi.ini" ]