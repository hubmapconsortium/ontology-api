import connexion
from openapi_server import encoder

options = {"swagger_ui": False}
app = connexion.App(__name__, specification_dir='openapi_server/openapi/', options=options)

app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml', arguments={'title': 'Ontology API'}, pythonic_params=True)

# Expose global WSGI application object
application = app.app
