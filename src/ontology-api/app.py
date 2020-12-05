'''
Created on Dec 04, 2020

@author: chb69
'''
import sys
import os
from pathlib import Path
import requests
import argparse
from flask import Flask, jsonify, abort, request, session, redirect, json, Response
from flask_cors import CORS
from globus_sdk import AccessTokenAuthorizer, AuthClient, ConfidentialAppAuthClient

from hubmap_commons.hubmap_const import HubmapConst 
from hubmap_commons.neo4j_connection import Neo4jConnection
from hubmap_commons.hm_auth import AuthHelper, secured
from hubmap_commons.autherror import AuthError
from hubmap_commons.hubmap_error import HubmapError
from hubmap_commons.exceptions import HTTPException

import time
import logging

LOG_FILE_NAME = "../log/ontology-api-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".log" 
logger = None

# Specify the absolute path of the instance folder and use the config file relative to the instance path
app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'), instance_relative_config=True)
app.config.from_pyfile('app.cfg')

# Enable/disable CORS from configuration based on docker or non-docker deployment
if app.config['ENABLE_CORS']:
    CORS(app)

token_list = {}

# Initialize the AuthHelper
# This is used by the @secured decorator
if AuthHelper.isInitialized() == False:
    authcache = AuthHelper.create(
        app.config['APP_CLIENT_ID'], app.config['APP_CLIENT_SECRET'])
else:
    authcache = AuthHelper.instance()

@app.before_first_request
def init():
    global logger
    try:
        logger = logging.getLogger('ontology.service')
        logger.setLevel(logging.INFO)
        logFH = logging.FileHandler(LOG_FILE_NAME)
        logger.addHandler(logFH)
        logger.info("started")
    except Exception as e:
        print("Error opening log file during startup")
        print(str(e))


####################################################################################################
## Default Routes
####################################################################################################

# Default endpoint for testing with gateway
@app.route('/', methods = ['GET'])
def index():
    return "Hello! This is HuBMAP Ontology API service :)"


@app.route('/hello', methods=['GET'])
@secured(groups="HuBMAP-read")
def hello():
    return jsonify({'uuid': 'hello'}), 200


# Show status of neo4j connection
@app.route('/status', methods = ['GET'])
def status():
    response_data = {
        # Use strip() to remove leading and trailing spaces, newlines, and tabs
        'version': (Path(__file__).parent / 'VERSION').read_text().strip(),
        'build': (Path(__file__).parent / 'BUILD').read_text().strip(),
        'neo4j_connection': False
    }

    conn = Neo4jConnection(app.config['NEO4J_SERVER'], app.config['NEO4J_USERNAME'], app.config['NEO4J_PASSWORD'])
    driver = conn.get_driver()
    is_connected = conn.check_connection(driver)
    
    if is_connected:
        response_data['neo4j_connection'] = True

    return jsonify(response_data)
    