# Client Programs

These are programs that use the OpenAPI client interface to the server.
The client is built (or rebuilt) at the same time as the server is built by the
'server/build_server.py -c' script when the create client '-c' option is given.
The client "module" is then placed in 'server/hu-bmap-ontoloty-api-client'.
The build process creates a general 'README.md' file which is of some use,
but it is not completely instructive. The scripts located in this directory
should serve as further examples as to how to process results returned
by the sever.

## Getting Started

The following is some tips on getting started using the endpoints.

### Include the Module

Since the 'hu-bmap-ontoloty-api-client' is not an official module and so
can't be included in the 'requirements.txt' file you will need to specify
its in order for it to be found like this.
```python
sys.path.append('../hu-bmap-ontology-api-client')
from hu_bmap_ontology_api_client import Client
from hu_bmap_ontology_api_client.types import Response, Unset
```
You should minimally include the 'Client' class which allows you to call the server after instantiating it,
the 'Response' object for retrieving the response from the server, and the 'Unset' object which allow you to determine if the instance
returned has an attribute that is not specified in the database. Remember
that Neo4j will omit attributes that have not been specified, but that the
Results contain instances of the return object that will contain all attributes associated with
that object.

In the following we will include an endpoint that will be called, and the object in which the response data is contained.
```python
from hu_bmap_ontology_api_client.api.default import terms_term_id_terms_get
from hu_bmap_ontology_api_client.models.term_resp_obj import TermRespObj
```

A connection to the client is created by instantiating the server
```python
client = Client(base_url="http://0.0.0.0:8080")
```

It is important to note that the default timeout for accessing the rest endpoints is 5 seconds.
This may not be enough time for some of the Neo4j queries that are executed by the server to complete, so you should up the timeout.
In this example the timeout for access to the client MSAPI endpoint is set to 30 seconds.
```python
client = client.with_timeout(30)
```

There are a number of ways of calling the endpoint which are outlined in the
'../hu-bmap-ontology-api-client/README.md' file but here we will be calling them so that
they return a 'Response' object which contains a 'response.status_code', and a 'response.parsed' entry which
contains the response data parsed into objects declared in the OpenAPI file; in this case
a List of TermRespObjs.
```python
response: Response[List[TermRespObj]] = terms_term_id_terms_get.sync_detailed(client=client, term_id=term_id)
```

## Example Client Programs

This is a list of the current client programs that can serve as an example
of how to use the api, and a description of that they do.

### terms_term_id_term.py

Please use the '-h' optional parameter to this program to print an
explanation and of its use and the available parameters. In general,
it will take a list of terms form a text file (one term per line),
and query the 'terms_term_id_terms_get' endpoint from the
'../ontology-api-spec.yml' OpenAPI definition file for each line
in the input file and write the line where result.matches == term_id
to stdout. So the general approach to running this is
```python
$ ./terms_term_id_terms.py test.txt > output_test.txt
```

If the '-v' option is used additional output will be produced, but it will go to stderr.

The '-t term_id' is used to run the program on only the term_id given with the optional parameter,
and in this case the input file will not be required and if given ignored.

The '-s SEP' optional parameter is use to specify the separator for the output file.
It defaults to a comma, but can be specified as a tab or any other character.

The '-u URL' optional parameter specifies the URL of the Ontology API Server to call.
