'''
Created on Oct 20, 2020

@author: chb69
'''

import sys
import os
import types
import mysql.connector
from mysql.connector import errorcode
import csv
import argparse


"""
        this list includes the prefixes for several informatics resources found in the PheKnowLator mapping data.
        This might be useful in the future: 
        bto: is BRENDA Tissue ontology (human brain related)
        fbbt: Flybase
        caro: Common Anatomy Reference Ontology
        xao: Frog
        zfa: Zebrafish
        ma: mouse anatomy
        wbbt: Wormbase
        fao: fungal anatomy ontology
        https://ncit.nci.nih.gov/ncitbrowser/conceptreport.jsp?dictionary=nci_thesaurus&code=<code> resolves to NCI terms might be able to map these**
        vsao: Vertebrate Skeletal Anatomy Ontology
        kupo: Kidney and Urinary Pathway Ontology
        mp: mouse phenotype
        emapa: Mouse Developmental Anatomy Ontology
        caloha:ts- an ontology of human anatomy and human cell types
        pmid: PubMed
        mat: Minimal Anatomy Terminology
        miaa: ???
        efo: ??? (found Experimental Factor Ontology but that doesn't look right)
        ehdaa: Human Developmental Anatomy Ontology
        vhog: Vertebrate Homologous Ontology Group
        pba: ???
        bams: BAMS Neuroanatomical Ontology
        mba: ???
        ev: eVOC (Expressed Sequence Annotation for Humans)
        dhba: ???
        http://www.snomedbrowser.com/codes/details/<code> resolves to SNOMED terms.  We might be able to import these
        nlxanat: a NIF ontology http://uri.neuinfo.org/nif/nifstd/nlx_anat
        aao: Amphibian Gross Anatomy Ontology
        tao: Teleost Anatomy Ontology
        tgma: Mosquito Gross Anatomy Ontology
        hao: Hymenoptera Anatomy Ontology
"""

config = {}

def load_config(root_path, filename):
    '''This method was heavily borrowed from the flask config.py file's from_pyfile method.
    It reads a file containing python constants and loads it into a dictionary.

    :param root_path: the path leading to the config file
    :param filename: the filename of the config relative to the
                     root path.
    '''
    filename = os.path.join(root_path, filename)
    d = types.ModuleType("config")
    d.__file__ = filename
    return_dict = {}
    try:
        with open(filename, mode="rb") as config_file:
            exec(compile(config_file.read(), filename, "exec"), d.__dict__)
        for config_key in d.__dict__:
            if str(config_key).startswith('__') == False:
                return_dict[config_key] = d.__dict__[config_key]
    except OSError as e:
        e.strerror = f"Unable to load configuration file ({e.strerror})"
        raise
    return return_dict

def create_database(config):
    ''' Create the initial database.  This method uses the SQL script found in
    the TABLE_CREATE_SQL_FILEPATH of the config file to build the database.
    
        :param dict config: The configuration settings 
    '''    
    connection = None
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'])
        cursor = connection.cursor()
        with open(config['TABLE_CREATE_SQL_FILEPATH'], encoding="utf-8") as f:
            commands = f.read().split(';')
            for command in commands:
                if str(command).strip() != "":
                    print('Executing: ' + command)
                    cursor.execute(command)
        print ("Done creating database tables.")
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        if connection != None:
            connection.close()        

def create_indices(config):
    ''' Create the indices in the mysql database to improve performance in the 
    transform step.  There is a set of default indices that need to be created.
    These are found in the config parameter INDEX_CREATE_SQL_FILEPATH.  After these
    are created, a series of custom indices need to be added to the various tables
    created from the other config parameters.
    
        :param dict config: The configuration settings 
    '''
    connection = None
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'])
        cursor = connection.cursor()
        
        """
        with open(config['INDEX_CREATE_SQL_FILEPATH'], encoding="utf-8") as f:
            # this code creates the "default" indices
            commands = f.read().split(';')
            for command in commands:
                if str(command).strip() != "":
                    print('Executing: ' + command)
                    cursor.execute(command)
        """
                    
        # the code below creates the indices for the tables created from entries in the 
        # app.cfg file
        for table_info in config['NODE_METADATA_FILE_TABLE_INFO']:
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_ontology_uri_idx (ontology_uri(500))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_node_label_idx (node_label(500))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_codeid_idx (codeid(500))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_sab_idx (sab(50))".format(table_name=table_info['table_name'])
            cursor.execute(sql)

        for table_info in config['EDGE_LIST_FILE_TABLE_INFO']:
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_subject_idx (subject(50))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_predicate_idx (predicate(100))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_object_idx (object(100))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_sab_idx (sab(50))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
 
        for table_info in config['DBXREF_FILE_TABLE_INFO']:
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_ontology_uri_idx (ontology_uri(50))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD FULLTEXT INDEX {table_name}_dbxrefs_idx (dbxrefs(700))".format(table_name=table_info['table_name'])
            cursor.execute(sql)

        for table_info in config['RELATIONS_FILE_TABLE_INFO']:
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_relation_id_idx (relation_id(100))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_relation_label_idx (relation_label(50))".format(table_name=table_info['table_name'])
            cursor.execute(sql)            
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_inverse_relation_label_idx (inverse_relation_label(50))".format(table_name=table_info['table_name'])
            cursor.execute(sql)  
            
        for table_info in config['SYNONYM_LIST_FILE_TABLE_INFO']:
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_ontology_uri_idx (ontology_uri(500))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_synonym_idx (synonym(500))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
            sql = "ALTER TABLE {table_name} ADD INDEX {table_name}_sab_idx (sab(50))".format(table_name=table_info['table_name'])
            cursor.execute(sql)
        print ("Done creating database indices.")
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        if connection != None:
            connection.close()        


def load_edge_list(config):
    '''
    Load all of the edge_list CSV files into a series of mysql tables.
    
    param dict config: the configuration data for this application
    '''
    edge_list_list = config['EDGE_LIST_FILE_TABLE_INFO']
    connection = None
    sql = ''
    record_count = 0
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        for table_data in edge_list_list:
            # walk through the list of edge_list files found in the config file.
            # for each entry, read the corresponding file and load it into the referenced
            # mysql table.
            table_name = table_data['table_name']
            file_name = table_data['file_name']
            sab = table_data['sab']
            drop_table_sql = "DROP TABLE IF EXISTS {table_name}".format(table_name=table_name)
            cursor.execute(drop_table_sql)
            table_create_sql = """CREATE TABLE {table_name} (
                id INT NOT NULL AUTO_INCREMENT,
                subject VARCHAR(2048) NOT NULL,
                predicate VARCHAR(2048) NOT NULL,
                object VARCHAR(2048) NOT NULL,
                sab VARCHAR(50),
                PRIMARY KEY(id)
            )""".format(table_name=table_name)
            # this is the generic SQL to create the edge_list tables
            cursor.execute(table_create_sql)
            connection.commit()
            print("Created table: " + table_name)
            file_path = os.path.join(config['ONTOLOGY_SOURCE_DIR'], file_name)
            load_file(config, file_path, table_name)
            sql = "UPDATE {table_name} SET sab = '{sab}'".format(table_name=table_name,sab=sab)
            # add the SAB for all records in table
            cursor.execute(sql)
            connection.commit()
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()    

def load_synonym_list(config):
    '''
    Load all of the synonym CSV files into a series of mysql tables.
    
    param dict config: the configuration data for this application
    '''
    synonym_list = config['SYNONYM_LIST_FILE_TABLE_INFO']
    connection = None
    sql = ''
    record_count = 0
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        for table_data in synonym_list:
            # walk through the list of synonym files found in the config file.
            # for each entry, read the corresponding file and load it into the referenced
            # mysql table.
            table_name = table_data['table_name']
            file_name = table_data['file_name']
            sab = table_data['sab']
            drop_table_sql = "DROP TABLE IF EXISTS {table_name}".format(table_name=table_name)
            cursor.execute(drop_table_sql)
            table_create_sql = """CREATE TABLE {table_name} (
                id INT NOT NULL AUTO_INCREMENT,
                ontology_uri VARCHAR(2048) NOT NULL,
                codeid VARCHAR(2048) NOT NULL,
                synonym VARCHAR(2048) NOT NULL,
                sab VARCHAR(50),
                PRIMARY KEY(id)
            )""".format(table_name=table_name)
            # this is the generic SQL to create a synonym table
            cursor.execute(table_create_sql)
            connection.commit()
            print("Created table: " + table_name)
            file_path = os.path.join(config['ONTOLOGY_SOURCE_DIR'], file_name)
            load_file(config, file_path, table_name)
            sql = "UPDATE {table_name} SET sab = '{sab}'".format(table_name=table_name,sab=sab)
            # add the SAB for all records in table
            cursor.execute(sql)
            connection.commit()
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()    

def load_relations(config):
    '''
    Load all of the relations CSV files into a series of mysql tables.
    
    param dict config: the configuration data for this application
    '''
    node_metadata_list = config['RELATIONS_FILE_TABLE_INFO']
    connection = None
    sql = ''
    record_count = 0
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        for table_data in node_metadata_list:
            # walk through the list of relations files found in the config file.
            # for each entry, read the corresponding file and load it into the referenced
            # mysql table.
            table_name = table_data['table_name']
            file_name = table_data['file_name']
            sab = table_data['sab']
            drop_table_sql = "DROP TABLE IF EXISTS {table_name}".format(table_name=table_name)
            cursor.execute(drop_table_sql)
            table_create_sql = """CREATE TABLE {table_name} (
                id INT NOT NULL AUTO_INCREMENT,
                relation_id VARCHAR(2048) NOT NULL,
                relation_label VARCHAR(2048) NOT NULL,
                inverse_relation_label VARCHAR(2048),
                PRIMARY KEY(id)
            )""".format(table_name=table_name)
            # this is the generic create relations SQL statement
            cursor.execute(table_create_sql)
            connection.commit()
            print("Created table: " + table_name)
            file_path = os.path.join(config['ONTOLOGY_SOURCE_DIR'], file_name)
            load_file(config, file_path, table_name)
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()    
            
            
def create_missing_codeids(config):
    node_metadata_list = config['NODE_METADATA_FILE_TABLE_INFO']
    connection = None
    sql = ''
    record_count = 0
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        for table_data in node_metadata_list:
            table_name = table_data['table_name']
            sql = """UPDATE {table_name}  
            SET codeid = REPLACE(REPLACE(ontology_uri, 'http://purl.obolibrary.org/obo/',''), '_', ' ')
            WHERE codeid IS NULL""".format(table_name=table_name)
            # add a codeid for all records in table
            cursor.execute(sql)
            connection.commit()
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        

def fix_dbxrefs(config):
    connection = None
    sql = ''
    record_count = 0
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        table_name = 'dbxrefs'
        sql = """UPDATE {table_name}  
        SET xref = UPPER(xref)""".format(table_name=table_name)
        # uppercase all dbxrefs data in table
        cursor.execute(sql)
        connection.commit()

        sql = """UPDATE {table_name}  
        SET xref = REPLACE(xref, 'NCIT:', 'NCI:') WHERE xref LIKE 'NCIT:%'""".format(table_name=table_name)
        # convert all the NCI codes
        cursor.execute(sql)
        connection.commit()

        sql = """UPDATE {table_name}  
        SET xref = REPLACE(xref, 'HTTP://WWW.SNOMEDBROWSER.COM/CODES/DETAILS/', 'SNOMEDCT_US:') WHERE xref LIKE 'HTTP://WWW.SNOMEDBROWSER.COM/CODES/DETAILS/%'""".format(table_name=table_name)
        # convert all the SNOMED codes
        cursor.execute(sql)
        connection.commit()

        sql = """UPDATE {table_name}  
        SET xref = REPLACE(xref, 'MESH:', 'MSH:') WHERE xref LIKE 'MESH:%'
        AND instr(xref, 'MESH:D') > 0
        AND instr(xref, 'MESH:D24') = 0""".format(table_name=table_name)
        # convert all the MeSH codes
        cursor.execute(sql)
        connection.commit()
        
        sql = """UPDATE {table_name}  
        SET xref = REPLACE(xref, ':', ' ')""".format(table_name=table_name)
        # replace all remaining colons with spaces dbxrefs data in table
        cursor.execute(sql)
        connection.commit()
        
            
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        
    
def load_node_metadata(config):
    '''
    Load all of the node_metadata CSV files into a series of mysql tables.
    
    param dict config: the configuration data for this application
    '''
    
    node_metadata_list = config['NODE_METADATA_FILE_TABLE_INFO']
    connection = None
    sql = ''
    record_count = 0
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        for table_data in node_metadata_list:
            # walk through the list of node_metadata files found in the config file.
            # for each entry, read the corresponding file and load it into the referenced
            # mysql table.
            table_name = table_data['table_name']
            file_name = table_data['file_name']
            sab = table_data['sab']
            drop_table_sql = "DROP TABLE IF EXISTS {table_name}".format(table_name=table_name)
            cursor.execute(drop_table_sql)
            table_create_sql = """CREATE TABLE {table_name} (
            id INT NOT NULL AUTO_INCREMENT,
            ontology_uri VARCHAR(2048) NOT NULL,
            codeid VARCHAR(2048),
            node_label VARCHAR(2048) NOT NULL,
            node_definition VARCHAR(2048) NOT NULL,
            sab VARCHAR(50),
            PRIMARY KEY(id)
            )""".format(table_name=table_name)
            # this SQL creates the generic node_metadata table
            cursor.execute(table_create_sql)
            connection.commit()
            print("Created table: " + table_name)
            file_path = os.path.join(config['ONTOLOGY_SOURCE_DIR'], file_name)
            load_file(config, file_path, table_name)
            sql = "UPDATE {table_name} SET sab = '{sab}'".format(table_name=table_name,sab=sab)
            # add the SAB for all records in table
            cursor.execute(sql)
            connection.commit()
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        

def load_dbxref(config):
    '''
    Load all of the dbxref CSV files into a series of mysql tables.
    
    param dict config: the configuration data for this application
    '''
    dbxref_list = config['DBXREF_FILE_TABLE_INFO']
    connection = None
    sql = ''
    record_count = 0
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        for table_data in dbxref_list:
            # walk through the list of dbxref files found in the config file.
            # for each entry, read the corresponding file and load it into the referenced
            # mysql table.
            table_name = table_data['table_name']
            file_name = table_data['file_name']
            sab = table_data['sab']
            drop_table_sql = "DROP TABLE IF EXISTS {table_name}".format(table_name=table_name)
            cursor.execute(drop_table_sql)
            table_create_sql = """CREATE TABLE {table_name} (
            id INT NOT NULL AUTO_INCREMENT,
            ontology_uri VARCHAR(2048) NOT NULL,
            dbxrefs VARCHAR(5120) NOT NULL,
            sab VARCHAR(50),
            PRIMARY KEY(id)
            )""".format(table_name=table_name)
            # this is the SQL to create a generic dbxref table
            cursor.execute(table_create_sql)
            connection.commit()
            print("Created table: " + table_name)
            file_path = os.path.join(config['ONTOLOGY_SOURCE_DIR'], file_name)
            load_file(config, file_path, table_name)
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        
        
def load_umls_codes(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'CODEs.csv')
    table_name = 'umls_codes'
    load_file(config, file_path, table_name)

def load_umls_defs(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'DEFs.csv')
    table_name = 'umls_defs'
    load_file(config, file_path, table_name)

def load_umls_suis(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'SUIs.csv')
    table_name = 'umls_suis'
    load_file(config, file_path, table_name)

def load_umls_cuis(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'CUIs.csv')
    table_name = 'umls_cuis'
    load_file(config, file_path, table_name)

def load_umls_tuis(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'TUIs.csv')
    table_name = 'umls_tuis'
    load_file(config, file_path, table_name)

def load_umls_code_suis(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'CODE-SUIs.csv')
    table_name = 'umls_code_suis'
    load_file(config, file_path, table_name)

def load_umls_cui_codes(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'CUI-CODEs.csv')
    table_name = 'umls_cui_codes'
    load_file(config, file_path, table_name)

def load_umls_cui_cuis(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'CUI-CUIs.csv')
    table_name = 'umls_cui_cuis'
    load_file(config, file_path, table_name)

def load_umls_cui_suis(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'CUI-SUIs.csv')
    table_name = 'umls_cui_suis'
    load_file(config, file_path, table_name)

def load_umls_cui_tuis(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'CUI-TUIs.csv')
    table_name = 'umls_cui_tuis'
    load_file(config, file_path, table_name)
                                
def load_umls_def_rel(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'DEFrel.csv')
    table_name = 'umls_def_rel'
    load_file(config, file_path, table_name)
                                
def load_umls_tui_rel(config):
    file_path = os.path.join(config['UMLS_SOURCE_DIR'],'TUIrel.csv')
    table_name = 'umls_tui_rel'
    load_file(config, file_path, table_name)
  
def build_xref_table(config):
    '''
    Build the dbxrefs table by reading the ontology_dbxref table.  The ontology_dbxref table contains a column dbxrefs.
    This method takes dbxrefs, a pipe-delimited list of xrefs, and splits it into separate entries (ex: xref1|xref2|xref3).
    Each individual xref becomes a new row in the dbxrefs table.  
    
    :param dict config: The configuration settings 
    '''
    dbxref_list = config['DBXREF_FILE_TABLE_INFO']

    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)
        drop_table_sql = "DROP TABLE IF EXISTS dbxrefs"
        cursor.execute(drop_table_sql)
        create_table_sql = """CREATE TABLE dbxrefs (
                id INT NOT NULL AUTO_INCREMENT,
                ontology_uri VARCHAR(2048) NOT NULL,
                xref VARCHAR(2048) NOT NULL,
                PRIMARY KEY(id)
                );"""
        cursor.execute(create_table_sql)
        for table_data in dbxref_list:
            table_name = table_data['table_name']
            sab = table_data['sab']
    
            cursor.execute("SELECT ontology_uri, dbxrefs FROM {table_name}".format(table_name=table_name))
            print("Loading {sab} data into table {table_name}".format(table_name="dbxrefs", sab=sab), end='', flush=True)
            result = cursor.fetchall()
            record_count = 0
            for row in result:
                ontology_uri = row['ontology_uri']
                all_xrefs = row['dbxrefs']
                xref_list = all_xrefs.split('|')
                # For each row in the ontology_dbxref table, split the dbxrefs column into a list
                for ref in xref_list:
                    # for each xref in the list, insert a new row into the dbxrefs table
                    ref = ref.replace("'","''")
                    sql = "INSERT INTO dbxrefs (ontology_uri, xref) VALUES ('{ontology_uri}','{ref}')".format(ontology_uri=ontology_uri, ref=ref)
                    cursor.execute(sql)
                
                    record_count = record_count + 1
                    #commit every 10,000 records
                    if record_count % 10000 == 0:
                        print('.', end='', flush=True)
                        connection.commit()
                        
            print('') # do this to disable the 'end' flag in prior print statements
            connection.commit()
            print ("Done loading the {table_name} table.".format(table_name="dbxrefs"))
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        
                      
def load_file(config, file_path, table_name):
    '''
    Load a CSV or tab-delimited file into a mysql table.
    
    param dict config: the configuration data for this application
    param str file_path: the full path to the CSV or tab-delimited file that will be loaded
    param str table_name: the name of the table in the database that will contain the data from file_path
    
    '''
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor()
        record_count = 0
        with open(file_path) as csvfile:
            myCSVReader = None
            if file_path.endswith('.txt'):
                # this code determines whether we are loading a CSV or tab-delimited file
                myCSVReader = csv.DictReader(csvfile, delimiter='\t')
            else:
                myCSVReader = csv.DictReader(csvfile)
            field_names = myCSVReader.fieldnames
            # the following statements remove some extra columns from the UMLS exported files
            if 'name_lc' in field_names:
                field_names.remove('name_lc') 
            if 'REL' in field_names:
                field_names.remove('REL') 
            if 'RELA' in field_names:
                field_names.remove('RELA')
            if (file_path.endswith('CUI-SUIs.csv') or 
                    file_path.endswith('CUI-TUIs.csv') or 
                    file_path.endswith('DEFrel.csv') or 
                    file_path.endswith('TUIrel.csv')):
                # add a field for type if the UMLS file contains relationship data
                field_names.append('type')
            field_list_str = '%s' % ', '.join(map(str, field_names))
            # the next two lines "cleanup" the column names from the file into a SQL compliant column name
            field_list_str = field_list_str.replace(':ID', '')
            field_list_str = field_list_str.replace(':', '')
            value_list_str = ''
            for field in field_names:
                # Build a list of column names for the insert SQL statement
                value_list_str += '%({field})s, '.format(field=field)
            value_list_str = value_list_str[:-2]
            sql = """INSERT INTO {table_name}({field_list})
                        VALUE ({value_list})""".format(table_name=table_name, field_list=field_list_str, value_list=value_list_str)
            print("Loading data from {file_name} into table {table_name}".format(file_name=file_path, table_name=table_name), end='', flush=True)
            for row in myCSVReader:
                # for some of the files, specify the 'type' column
                if file_path.endswith('CUI-SUIs.csv'):
                    row['type'] = 'PREF_TERM'
                if file_path.endswith('CUI-TUIs.csv'):
                    row['type'] = 'STY' 
                if file_path.endswith('DEFrel.csv'):
                    row['type'] = 'DEF'
                if file_path.endswith('TUIrel.csv'):
                    row['type'] = 'ISA_STY'

                # use row directly when csv headers match column names.
                # remove data from a row if the column header is None
                if table_name == 'suis':
                    if None in row.keys():
                        row.pop(None)
                if None in row.keys():
                    row.pop(None)
                cursor.execute(sql, row)
                
                    
                record_count = record_count + 1
                #commit every 200,000 records
                if record_count % 200000 == 0:
                    print('.', end='', flush=True)
                    connection.commit()
        print('') # do this to disable the 'end' flag in prior print statements
        connection.commit()
        print ("Done loading the {table_name} table.".format(table_name=table_name))
    
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        

def extract_non_umls(config):
    load_node_metadata(config)
    load_relations(config)
    load_dbxref(config)
    load_edge_list(config)
    load_synonym_list(config)

    # This code is temporary.  It should be moved to a pre-processing step
    create_missing_codeids(config)
    # END This code is temporary.  It should be moved to a pre-processing step
    
def extract(config):
    '''
    The extract method loads the CSV and tab-delimited files into mysql tables mirroring their file structure.
    
    param dict config: The configuration data for this application 
    '''
    create_database(config)
    load_node_metadata(config)
    load_relations(config)
    load_dbxref(config)
    load_edge_list(config)
    load_synonym_list(config)
    load_umls_codes(config)
    load_umls_defs(config)
    load_umls_suis(config)
    load_umls_cuis(config)
    load_umls_tuis(config)
    load_umls_cui_codes(config)
    load_umls_code_suis(config)
    load_umls_cui_cuis(config)
    load_umls_cui_suis(config)
    load_umls_cui_tuis(config)
    load_umls_def_rel(config)
    load_umls_tui_rel(config)
    
    # This code is temporary.  It should be moved to a pre-processing step
    create_missing_codeids(config)
    # END This code is temporary.  It should be moved to a pre-processing step
    
    
    create_indices(config)
    print("Done with extract process")

def build_ambiguous_codes_table(config):
    '''
    Construct a table called temp_ambiguous_codes (ontology_uri, codeid).  This table contains a subset of
    the codes that map to more than one CUI.  These codes are "ambiguous" because we cannot use them in our automated
    processing.  Our code cannot decide which of the CUIs should be assigned the preferred term from the data we are loading.
    Also, these connections tend to conflate items (ex: left hand, right hand, and hand are all the same). 
    
    We will use this table to "filter out" some of the data during the ETL process.
    
    param dict config: The configuration data for this application. 
    '''   
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        drop_table_sql = "DROP TABLE IF EXISTS temp_ambiguous_codes"
        cursor.execute(drop_table_sql)
        create_table_sql = """CREATE TABLE temp_ambiguous_codes (
                id INT NOT NULL AUTO_INCREMENT,
                ontology_uri VARCHAR(2048) NOT NULL,
                codeid VARCHAR(2048),
                PRIMARY KEY(id)
                );"""
        cursor.execute(create_table_sql)
        print("Created table temp_ambiguous_codes")
        sql = """INSERT INTO temp_ambiguous_codes (ontology_uri, codeid) 
        SELECT DISTINCT ontology_uri, xref as codeid
        FROM dbxrefs, umls_cui_codes as rel
        WHERE xref = rel.end_id
        GROUP BY ontology_uri, xref
        HAVING COUNT(DISTINCT rel.start_id) > 1"""
        """This query builds the temp_ambiguous_codes table.  It inserts codes with
        more than 1 CUI into the temp_ambiguous_codes table.
        """

        cursor.execute(sql)
        connection.commit()
        print("Loaded codes into table temp_ambiguous_codes")
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        
        

def temp_build_ccf_code_cui_table(config):
   
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        drop_table_sql = "DROP TABLE IF EXISTS temp_ccf_cui_codes"
        cursor.execute(drop_table_sql)
        create_table_sql = """CREATE TABLE temp_ccf_cui_codes (
                id INT NOT NULL AUTO_INCREMENT,
                codeid VARCHAR(2048) NOT NULL,
                cui VARCHAR(2048),
                PRIMARY KEY(id)
                );"""
        cursor.execute(create_table_sql)
        print("Created table temp_ccf_cui_codes")
        sql = "ALTER TABLE temp_ccf_cui_codes ADD INDEX temp_ccf_cui_codes_codeid(codeid(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE temp_ccf_cui_codes ADD INDEX temp_ccf_cui_codes_cui_idx(cui(50))"
        cursor.execute(sql)
        cursor = connection.cursor()
        record_count = 0
        file_path = '/home/chb69/umls_data/ccf/CCF-CUI.csv'
        with open(file_path) as csvfile:
            myCSVReader = None
            if file_path.endswith('.txt'):
                # this code determines whether we are loading a CSV or tab-delimited file
                myCSVReader = csv.DictReader(csvfile, delimiter='\t')
            else:
                myCSVReader = csv.DictReader(csvfile)
            field_names = myCSVReader.fieldnames
            #a.name,b.CodeID,c.CUI,d.name
            print("Loading data from {file_name} into table {table_name}".format(file_name=file_path, table_name='temp_ccf_cui_codes'), end='', flush=True)
            for row in myCSVReader:
                sql = "INSERT INTO temp_ccf_cui_codes (codeid, cui) VALUES ('{codeid}','{cui}')".format(codeid=row['b.CodeID'],cui=row['c.CUI'])
                cursor.execute(sql)
            
        connection.commit()
        print ("Done loading the {table_name} table.".format(table_name="temp_ccf_cui_codes"))
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        
    
    
def build_ontology_uri_to_umls_map_table(config):
    '''
    Construct a table called ontology_uri_map (ontology_uri, cui, codeid, type, sab).  This table is a mapping
    between the dbxref data and the UMLS data.  The table is built from dbxrefs and cui_codes (ULMS)
    tables.  The ontology_uri is the primary key within the dbxref data.  The cui and codeid are the main keys
    within the UMLS data.  Each record in ontology_uri_map allows one to move between both systems.
    
    param dict config: The configuration data for this application. 
    '''
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)
        
        
                
        drop_table_sql = "DROP TABLE IF EXISTS ontology_uri_map"
        cursor.execute(drop_table_sql)
        create_table_sql = """CREATE TABLE ontology_uri_map (
                id INT NOT NULL AUTO_INCREMENT,
                ontology_uri VARCHAR(2048) NOT NULL,
                cui VARCHAR(2048),
                codeid VARCHAR(2048),
                type VARCHAR(50),
                mapping_type VARCHAR(50),
                sab VARCHAR(50),
                PRIMARY KEY(id)
                );"""
        cursor.execute(create_table_sql)
        print("Created table ontology_uri_map")
        sql = """INSERT INTO ontology_uri_map (ontology_uri, cui) 
        SELECT DISTINCT ontology_uri, substr(xref,6) as CUI FROM dbxrefs
        WHERE xref LIKE 'UMLS%'"""
        # This query loads all the ontology_uri's that map directly to a UMLS CUI according to the dbxrefs table
        # these records will have their codeid column set to NULL
        cursor.execute(sql)
        connection.commit()
        print("Loaded UMLS map into table ontology_uri_map")
        
        sql = """INSERT INTO ontology_uri_map (ontology_uri, codeid, cui, type, sab) 
        SELECT DISTINCT ontology_uri, xref as codeid, rel.start_id as cui, 'PT' as type, substring_index(xref,' ', 1) as sab
        FROM dbxrefs, umls_cui_codes as rel
        WHERE xref = rel.end_id
        AND (ontology_uri, xref) NOT IN (SELECT ontology_uri,codeid FROM temp_ambiguous_codes)"""
        # This query loads all the ontology_uri's that map to a code according to the dbxrefs table
        cursor.execute(sql)
        connection.commit()
        print("Loaded map into table ontology_uri_map")        

        # add indices after loading to speed up the load
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_ontology_uri_idx(ontology_uri(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_cui_idx(cui(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_codeid_idx(codeid(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_type_idx(type(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_mapping_type_idx(mapping_type(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_sab_idx(sab(50))"
        cursor.execute(sql)
        print("Built indices for table ontology_uri_map")

        sql = """UPDATE ontology_uri_map SET mapping_type = 'PRIMARY' where codeid is null AND ontology_uri IN (
        SELECT ontology_uri from (SELECT ontology_uri FROM ontology_uri_map
        where codeid is null
        group by ontology_uri
        having count(distinct cui) = 1) as table_one)"""
        # This query sets all the PRIMARY CUIs
        cursor.execute(sql)
        connection.commit()
        print("Loaded PRIMARY CUI map data into table ontology_uri_map")

    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        

def build_relations_table(config):
    '''
    Create a new table called relations.  This table will contains a superset of all relations
    loaded so far.  After this table is loaded, UPDATE it to add the inverse relations (if necessary).
    
    param dict config: the configuration data for this application
    '''
    relations_table_info = config['RELATIONS_FILE_TABLE_INFO']
    
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)

        drop_table_sql = "DROP TABLE IF EXISTS relations"
        cursor.execute(drop_table_sql)
        create_table_sql = """CREATE TABLE relations (
        id INT NOT NULL AUTO_INCREMENT,
        relation_id VARCHAR(2048) NOT NULL,
        relation_label VARCHAR(2048) NOT NULL,
        inverse_relation_label VARCHAR(2048),
        sab VARCHAR(50),
        PRIMARY KEY(id));"""
        # step 1: create the new relations table
        
        cursor.execute(create_table_sql)
        print("Created table relations")
    
        for table_info in relations_table_info:
            # step 2: for each entry in the RELATIONS_FILE_TABLE_INFO config entry,
            # insert the data from the table referenced by RELATIONS_FILE_TABLE_INFO into the relations table
            
            table_name = table_info['table_name']
            sab = table_info['sab']
            
            sql = """INSERT INTO relations (relation_id, relation_label, inverse_relation_label, sab) 
            SELECT relation_id, relation_label, inverse_relation_label, '{sab}' FROM {table_name}""".format(table_name=table_name, sab=sab)
            cursor.execute(sql)
            connection.commit()
            print("Loaded {sab} relations data into table relations".format(sab=sab))
            
            sql = """UPDATE relations r1
            LEFT JOIN relations r2
            ON r1.relation_id = r2.relation_id
            SET r1.inverse_relation_label = CONCAT('inverse ', r2.relation_label)
            WHERE r2.inverse_relation_label IS NULL"""
            """After the 'normal' or 'forward' relations are loaded, find any records in the relations table that
            have inverse_relation_label set to NULL.  For each record missing an inverse_relation_label, create an 
            inverse_relation_label equal to 'inverse ' + relation_label
            """
            cursor.execute(sql)
            connection.commit()
            print("Added inverse relations for {sab} data into table relations".format(sab=sab))
            

    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        
        
def insert_new_cui_cui_relations(config):
    '''
    Extract all relationships between two UMLS CUIs found in the PheKnowLator data.  This method only 
    inserts data into the cui_cuis table.  It does not create new CUIs.  It adds both the "regular" relations
    plus their inverse relations.
    
    param dict config: The configuration data for this application. 
    '''
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)
        
        edge_list_file_info = config['EDGE_LIST_FILE_TABLE_INFO']
        
        for edge_list_info in edge_list_file_info:
            # walk through all the existing edge_list tables and load the data into the
            # umls_cui_cuis table
            
            sab = edge_list_info['sab']
            table_name = edge_list_info['table_name']
            
            sql = """DELETE FROM umls_cui_cuis WHERE sab = '{sab}'""".format(sab=sab)
            cursor.execute(sql)
            connection.commit()
            print('')
            print("Deleted {sab} map from table umls_cui_cuis".format(sab=sab))


            sql = """INSERT INTO umls_cui_cuis (start_id, type, end_id, sab) 
            SELECT DISTINCT subject_table.cui as start_id, lower(replace(rel.relation_label,' ','_')) as type, object_table.cui as end_id, 'UBERON' as sab
            FROM {table_name} el, relations rel, ontology_uri_map subject_table, ontology_uri_map object_table
            WHERE rel.relation_id = el.predicate
            AND subject_table.ontology_uri = el.subject
            AND subject_table.mapping_type = 'PRIMARY'
            AND object_table.ontology_uri = el.object
            AND object_table.mapping_type = 'PRIMARY'
            AND subject_table.cui != object_table.cui
            AND el.sab = '{sab}'""".format(table_name=table_name,sab=sab)
            """
            This query needs some explanation.  Basically, the edge_list table is the central table in the query.  We use the edge_list
            table structure (subject, predicate, object) to find records where the edge_list contains relationships between
            the subject CUI and the object CUI.  This record will become a new relationship between 2 CUIs.  Lastly, we map from the
            edge_list relation_id to the "English" relation_label.  We replace the spaces in the relation_label with underscores ('_').
            This becomes the label for the relationship in the CUI to CUI relationship.  
            """
            cursor.execute(sql)
            connection.commit()
            print("Loaded {sab} map into table umls_cui_cuis".format(sab=sab))
    
            sql = """INSERT INTO umls_cui_cuis (start_id, type, end_id, sab) 
            SELECT DISTINCT object_table.cui as start_id, lower(replace(rel.inverse_relation_label,' ','_')) as type, subject_table.cui as end_id, 'UBERON' as sab
            FROM {table_name} el, relations rel, ontology_uri_map subject_table, ontology_uri_map object_table
            WHERE rel.relation_id = el.predicate
            AND subject_table.ontology_uri = el.subject
            AND subject_table.mapping_type = 'PRIMARY'
            AND object_table.ontology_uri = el.object
            AND object_table.mapping_type = 'PRIMARY'
            AND subject_table.cui != object_table.cui
            AND rel.inverse_relation_label IS NOT NULL
            AND el.sab = '{sab}'""".format(table_name=table_name,sab=sab)
            """
            This query is basically the same as the initial query above, but there are two important differences:
            - the relationship used is the inverse_relation_label from the pkl_relations table.
            - the subject and object are swapped since we are creating the inverse relationship  
            """
            cursor.execute(sql)
            connection.commit()
            print("Loaded {sab} inverse relation map into table umls_cui_cuis".format(sab=sab))
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        

def insert_new_terms(config):
    '''
    The method creates new labels (Term nodes) in the graph for each node_metadata table.
    Adding a Term node affects several tables: suis, code_suis, cui_suis, and new_sui_map.  The new_sui_map
    does not represent data in the graph, it merely tracks minted SUIs between application runs to avoid changing the
    SUI and losing its connection to the UMLS codes.
    
    param dict config: The configuration data for this application.
    '''
    connection = None
    sql = ''
    
    
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)
        
        truncate_table_sql = "TRUNCATE suis_updated"
        cursor.execute(truncate_table_sql)
        connection.commit()

        truncate_table_sql = "TRUNCATE code_suis_updated"
        cursor.execute(truncate_table_sql)
        connection.commit()
        
        truncate_table_sql = "TRUNCATE new_sui_map"
        cursor.execute(truncate_table_sql)
        connection.commit()
        
        truncate_table_sql = """TRUNCATE cui_suis_updated"""
        cursor.execute(truncate_table_sql)
        connection.commit()

        print ("Copying cui_suis INTO cui_suis_updated")
        sql = """INSERT INTO cui_suis_updated SELECT * FROM umls_cui_suis"""
        cursor.execute(sql)
        connection.commit()
        
        sql = "DROP INDEX suis_updated_sui_idx ON suis_updated"
        cursor.execute(sql)
        connection.commit()
        sql = "DROP INDEX suis_updated_name_idx ON suis_updated"
        cursor.execute(sql)
        connection.commit()

        print ("Copying suis INTO suis_updated")
        sql = """INSERT INTO suis_updated SELECT * FROM umls_suis"""
        cursor.execute(sql)
        connection.commit()

        sql = "ALTER TABLE suis_updated ADD INDEX suis_updated_sui_idx (sui(100))"
        cursor.execute(sql)
        connection.commit()
        sql = "ALTER TABLE suis_updated ADD INDEX suis_updated_name_idx (name(500))"
        cursor.execute(sql)
        connection.commit()
        
        sql = "DROP INDEX code_suis_updated_start_id_idx ON code_suis_updated"
        cursor.execute(sql)
        connection.commit()
        sql = "DROP INDEX code_suis_updated_end_id_idx ON code_suis_updated"
        cursor.execute(sql)
        connection.commit()
        sql = "DROP INDEX code_suis_updated_type_idx ON code_suis_updated"
        cursor.execute(sql)
        connection.commit()
        sql = "DROP INDEX code_suis_updated_cui_idx ON code_suis_updated"
        cursor.execute(sql)
        connection.commit()

        print ("Copying code_suis INTO code_suis_updated")
        sql = """INSERT INTO code_suis_updated SELECT * FROM umls_code_suis"""
        cursor.execute(sql)
        connection.commit()

        sql = "ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_start_id_idx (start_id(100))"
        cursor.execute(sql)
        connection.commit()
        sql = "ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_end_id_idx (end_id(100))"
        cursor.execute(sql)
        connection.commit()
        sql = "ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_type_idx (type(100))"
        cursor.execute(sql)
        connection.commit()
        sql = "ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_cui_idx (cui(100))"
        cursor.execute(sql)
        connection.commit()
        
        node_metadata_info = config['NODE_METADATA_FILE_TABLE_INFO']
        record_count = 1 # start SUI numbering at one 
        
        for table_info in node_metadata_info:
            # for each entry in the NODE_METADATA_FILE_TABLE_INFO config entry, query the node_metadata
            # table and find all missing terms.  Then add the missing terms to the appropriate database tables
            
            table_name = table_info['table_name']
            sab = table_info['sab']

            dict_new_suis = {}
            """ keep an in-memory list of the new SUIs generated
            The SQL includes a list of existing SUIs when it is initially executed.
            During execution, new SUIs are created but they are missing from the ones
            retrieved by the SQL (i.e. a "dirty read").  Therefore, the new SUIs are not found and will
            create duplicate SUIs with the same labels.  This in-memory list provides
            lookup services to avoid recreating the labels."""

            
            sql = """SELECT oum.ontology_uri as ontology_uri, oum.cui AS cui, IFNULL(oum.codeid,nm.codeid) AS codeid, nm.node_label AS label, '{sab}' as sab, su.sui AS sui, 'PT' AS term_type
                    FROM {table_name} nm
                    INNER JOIN ontology_uri_map oum
                    ON nm.ontology_uri = oum.ontology_uri
                    AND oum.mapping_type = 'PRIMARY'
                    LEFT OUTER JOIN suis_updated su
                    ON nm.node_label = su.name
                    WHERE oum.codeid is null OR oum.codeid NOT IN (select start_id FROM code_suis_updated)""".format(table_name=table_name,sab=sab)
                                
            """This query joins the ontology_uri_map data to the label from the node_metadata table.  The query only returns
            records where the codeid is NULL or the codeid is missing from the code_suis_updated table.  These represent
            records that need a new SUI minted."""
            cursor.execute(sql)
            result = cursor.fetchall()
            print("")
            print ("Loading tables suis_updated, code_suis_updated, and new_sui_map for SAB: {sab}".format(sab=sab), end='', flush=True)
            for row in result:
                ontology_uri = row['ontology_uri']
                cui = row['cui']
                codeid = row['codeid']
                code_list = str(codeid).split(' ')
                code = code_list[1]
                label = row['label']
                term_type = row['term_type']
    
                sui = row['sui']
                if sui == None:
                    if label in dict_new_suis.keys():
                        # if the label already exists, then use the existing SUI
                        sui = dict_new_suis[label]   
                    else: 
                        # if the label does not exist, then mint a new SUI               
                        sui = 'HS' + str(record_count).zfill(6)
                        # mint a new SUI prefixed with 'HS'                
                        sql = """INSERT INTO suis_updated (sui, name) VALUES ('{sui}',"{name}")""".format(sui=sui,name=label)
                        cursor.execute(sql)
                        sql = """INSERT INTO new_sui_map (codeid, sui, name) VALUES ('{codeid}','{sui}',"{name}")""".format(codeid=codeid,sui=sui,name=label)
                        cursor.execute(sql)
                        
                        dict_new_suis[label] = sui
                        # add the new SUI to the in memory list
    
                sql = """INSERT INTO code_suis_updated (start_id, end_id, type, cui) VALUES ('{codeid}','{sui}','{term_type}','{cui}')""".format(codeid=codeid,sui=sui,cui=cui,term_type=term_type)
                cursor.execute(sql)
    
                if 'HC' in cui and term_type == 'PT':
                    #insert a new HCUI into the cui_suis_updated table since it does not exist in the table yet.
                    sql = """INSERT INTO cui_suis_updated (start_id, end_id, type) VALUES ('{cui}','{sui}','PREF_TERM')""".format(cui=cui,sui=sui)
                    cursor.execute(sql)
    
                record_count = record_count + 1
    
                #commit every 10,000 records
                if record_count % 10000 == 0:
                    print('.', end='', flush=True)
                    connection.commit()
                
            connection.commit()
            print('')
            
        insert_new_synonyms(config, record_count)
        # after the for loop completes, add all the synonymous terms.  This is done outside of the for loop
        # because there is not necessarily a 1 to 1 relationship between the node_metadata entries and the synoymous files.
        # However, there is a dependency because the insert_new_synonym method needs to continue the SUI numbering.
        # This method is executed after the commit because then we do not need to worry about a situation where some of the 
        # terms have not yet been committed to the database.


    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()  
            
def insert_new_synonyms(config, record_count):
    '''
    The method creates new labels (Term nodes) in the graph for each synonym table.
    This method is basically identical to the insert_new_terms method.  The only differences are the 
    a) the config entry used (this uses SYNONYM_LIST_FILE_TABLE_INFO) and b) SQL used to find the synonyms  
    Adding a Term node affects several tables: suis, code_suis, cui_suis, and new_sui_map.  The new_sui_map
    does not represent data in the graph, it merely tracks minted SUIs between application runs to avoid changing the
    SUI and losing its connection to the UMLS codes.
    
    param dict config: The configuration data for this application.
    '''
    
    if 'SYNONYM_LIST_FILE_TABLE_INFO' not in config:
        #skip this method if there are no synonym files defined
        return
    
    synonym_list = config['SYNONYM_LIST_FILE_TABLE_INFO']
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)


        for table_info in synonym_list:
            sab = table_info['sab']
            table_name = table_info['table_name']

            dict_new_suis = {}
            """ keep an in-memory list of the new SUIs generated
            The SQL includes a list of existing SUIs when it is initially executed.
            During execution, new SUIs are created but they are missing from the ones
            retrieved by the SQL (i.e. a "dirty read").  Therefore, the new SUIs are not found and will
            create duplicate SUIs with the same labels.  This in-memory list provides
            lookup services to avoid recreating the labels."""

            sql = """SELECT DISTINCT oum.ontology_uri as ontology_uri, oum.cui AS cui,nm.codeid AS codeid,  nm.synonym AS label, '{sab}' as sab, su.sui AS sui, 'SY' AS term_type
                    FROM {table_name} nm
                    INNER JOIN ontology_uri_map oum
                    ON nm.ontology_uri = oum.ontology_uri
                    LEFT OUTER JOIN suis_updated su
                    ON nm.synonym = su.name""".format(table_name=table_name,sab=sab)
            
            """This query joins the ontology_uri_map data to the label from the node_metadata table.  The query only returns
            records where the codeid is NULL or the codeid is missing from the code_suis_updated table.  These represent
            records that need a new SUI minted."""
            cursor.execute(sql)
            result = cursor.fetchall()
            print ("Loading tables suis_updated, code_suis_updated, and new_sui_map for SAB: {sab}".format(sab=sab), end='', flush=True)
            for row in result:
                ontology_uri = row['ontology_uri']
                cui = row['cui']
                codeid = row['codeid']
                code_list = str(codeid).split(' ')
                code = code_list[1]
                label = row['label']
                term_type = row['term_type']
    
                sui = row['sui']
                if sui == None:
                    if label in dict_new_suis.keys():
                        # if the label already exists, then use the existing SUI
                        sui = dict_new_suis[label]   
                    else: 
                        # if the label does not exist, then mint a new SUI               
                        sui = 'HS' + str(record_count).zfill(6)
                        # mint a new SUI prefixed with 'HS'                
                        sql = """INSERT INTO suis_updated (sui, name) VALUES ('{sui}',"{name}")""".format(sui=sui,name=label)
                        cursor.execute(sql)
                        sql = """INSERT INTO new_sui_map (codeid, sui, name) VALUES ('{codeid}','{sui}',"{name}")""".format(codeid=codeid,sui=sui,name=label)
                        cursor.execute(sql)
                        
                        dict_new_suis[label] = sui
                        # add the new SUI to the in memory list
    
                sql = """INSERT INTO code_suis_updated (start_id, end_id, type, cui) VALUES ('{codeid}','{sui}','{term_type}','{cui}')""".format(codeid=codeid,sui=sui,cui=cui,term_type=term_type)
                cursor.execute(sql)
    
                record_count = record_count + 1
    
                #commit every 10,000 records
                if record_count % 10000 == 0:
                    print('.', end='', flush=True)
                    connection.commit()
                
            connection.commit()
            

    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        

def insert_new_cuis(config):
    '''    
    Find every entry in the node_metadata tables that is missing from the ontology_uri_map table.  This indicates a
    record that was not mapped to any existing UMLS code.  This means the record needs a new CUI minted for it.
      
    param dict config: The configuration data for this application.
    '''

    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)
    
        truncate_table_sql = "TRUNCATE cuis_updated"
        cursor.execute(truncate_table_sql)
        connection.commit()

        print ("Truncating cui_codes_updated")
        sql = """TRUNCATE cui_codes_updated"""
        cursor.execute(sql)
        connection.commit()

        print ("Copying cuis INTO cuis_updated")
        sql = """INSERT INTO cuis_updated SELECT * FROM umls_cuis"""
        cursor.execute(sql)
        connection.commit()
        
        print ("Deleting HuBMAP CUIs")
        sql = """DELETE FROM ontology_uri_map WHERE cui LIKE 'HC%'"""
        cursor.execute(sql)
        connection.commit()

        print ("Copying cuis INTO cui_codes_updated")
        sql = """INSERT INTO cui_codes_updated SELECT * FROM umls_cui_codes"""
        cursor.execute(sql)
        connection.commit()

        
        node_metadata_info = config['NODE_METADATA_FILE_TABLE_INFO']

        record_count = 1 # start HCUI numbering at one 
        print ("Creating new HCUI's and codes")
        
        for table_info in node_metadata_info:
            
            sab = table_info['sab']
            table_name = table_info['table_name']

            print ("Deleting {sab} codes from umls_codes".format(sab=sab))
            sql = """DELETE FROM umls_codes WHERE sab = '{sab}'""".format(sab=sab)
            # remove old records for the sab
            cursor.execute(sql)
            connection.commit()
            
            print("Loading node metadata for {sab}".format(sab=sab))
            sql = """SELECT ontology_uri AS ontology_uri, codeid AS codeid, sab AS sab FROM {table_name} nm
            WHERE nm.ontology_uri NOT IN (SELECT ontology_uri FROM ontology_uri_map WHERE mapping_type = 'PRIMARY')""".format(table_name=table_name)           
            """Find all the records in the current node_metadata table that were not mapped to an UMLS terms."""
            
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                ontology_uri = row['ontology_uri']
                cui = 'HC' + str(record_count).zfill(6)
                # mint a new CUI using the HC prefix
                
                record_count = record_count + 1
    
                current_sab = sab                
                
                codeid = row['codeid']
                
                code_list = str(codeid).split(' ')
                
                code = code_list[1]
                
                sql = """INSERT INTO ontology_uri_map (ontology_uri,codeid,cui,sab,mapping_type) VALUES ('{ontology_uri}','{codeid}','{cui}','{sab}','PRIMARY')""".format(codeid=codeid,cui=cui,ontology_uri=ontology_uri,sab=current_sab)
                # add the new HCUI to the ontology_uri_map
                cursor.execute(sql)
                sql = """INSERT INTO cuis_updated (cui) VALUES ('{cui}')""".format(cui=cui)
                # add the new HCUI to the cuis_updated table
                cursor.execute(sql)
                connection.commit()
    
                sql = """INSERT INTO umls_codes (codeid, sab,code) VALUES ('{codeid}','{sab}','{code}')""".format(codeid=codeid,sab=current_sab,code=code)
                # add the new Code information to umls_codes
                cursor.execute(sql)
                connection.commit()
                sql = """INSERT INTO cui_codes_updated (start_id, end_id) VALUES ('{cui}','{codeid}')""".format(cui=cui,codeid=codeid)
                # connect the new HCUI to its new Code
                cursor.execute(sql)
                connection.commit()

    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        
       

def insert_new_codes(config):
    '''    
    Create the new codes in the graph.  This code creates new codes plus connects them to the appropriate
    CUIs.
    
    Note: By the time this code executes, the insert_new_cuis method should have already inserted.
    So this code does not need to insert them.  This also means this method is dependent upon the insert_new_cuis method.
      
    param dict config: The configuration data for this application.
    '''
    
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)
        
        node_metadata_info = config['NODE_METADATA_FILE_TABLE_INFO']

        for table_info in node_metadata_info:
            
            table_name = table_info['table_name']
            current_sab = table_info['sab']
            
            sql = """SELECT nm.ontology_uri as ontology_uri, nm.codeid as codeid, oum.cui as cui, nm.sab as sab 
            FROM {table_name} nm, ontology_uri_map oum
            WHERE oum.ontology_uri = nm.ontology_uri
            and oum.codeid IS NOT NULL
            and nm.codeid not in (select codeid from umls_codes)""".format(table_name=table_name)
            # this SQL finds all the codes in the current node_metadata missing from the umls_codes table
            # these are the codes we need to add
            
            cursor.execute(sql)
            result = cursor.fetchall()
            print ("Creating new codes for sab: {sab}".format(sab=current_sab))
            for row in result:
                cui = row['cui']
                
                codeid = row['codeid']
                code_list = str(codeid).split(' ')
                code = code_list[1]
    
                sql = """INSERT INTO umls_codes (codeid, sab,code) VALUES ('{codeid}','{sab}','{code}')""".format(codeid=codeid,sab=current_sab,code=code)
                cursor.execute(sql)
                connection.commit()
                sql = """INSERT INTO cui_codes_updated (start_id, end_id) VALUES ('{cui}','{codeid}')""".format(cui=cui,codeid=codeid)
                cursor.execute(sql)
                connection.commit()

    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        
    
def insert_new_defs(config):
    '''
    Add the defintions from the PHeKnowLator data for the UBERON and CL nodes.

    param dict config: The configuration data for this application.
    '''
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)
        

        truncate_table_sql = "TRUNCATE defs_updated"
        cursor.execute(truncate_table_sql)
        connection.commit()

        truncate_table_sql = "TRUNCATE def_rel_updated"
        cursor.execute(truncate_table_sql)
        connection.commit()
        
        truncate_table_sql = "TRUNCATE new_def_map"
        cursor.execute(truncate_table_sql)
        connection.commit()
        
        print("")
        print ("Copying defs INTO defs_updated")
        sql = """INSERT INTO defs_updated SELECT * FROM umls_defs"""
        cursor.execute(sql)
        connection.commit()
        
        print ("Copying def_rel INTO def_rel_updated")
        sql = """INSERT INTO def_rel_updated SELECT * FROM umls_def_rel"""
        cursor.execute(sql)
        connection.commit()
        
        node_metadata_info = config['NODE_METADATA_FILE_TABLE_INFO']
        
        record_count = 1 # start SUI numbering at one
         
        for table_info in node_metadata_info:

            table_name = table_info['table_name']
            sab = table_info['sab']
            
            sql = """SELECT oum.cui, nm.node_definition, '{sab}' as sab 
            FROM {table_name} nm, ontology_uri_map oum 
            WHERE nm.ontology_uri = oum.ontology_uri
            AND oum.mapping_type = 'PRIMARY'
            AND node_definition <> 'None'
            AND node_definition <> '.'""".format(table_name=table_name,sab=sab)
            
            cursor.execute(sql)
            result = cursor.fetchall()
            print("")
            print ("Loading tables defs_updated, def_rels_updated, and new_def_map", end='', flush=True)
            for row in result:
                cui = row['cui']
                node_definition = row['node_definition']
                sab = row['sab']
                atui = 'HAT' + str(record_count).zfill(6)
                record_count = record_count + 1
                
                if '"' in node_definition:
                    node_definition = node_definition.replace('"','\\"')
                    
                
                sql = """INSERT INTO defs_updated (atui, sab, def) VALUES ('{atui}','{sab}',"{node_definition}")""".format(atui=atui,sab=sab,node_definition=node_definition)
                cursor.execute(sql)
                sql = """INSERT INTO def_rel_updated (start_id, end_id, type, sab) VALUES ('{cui}','{atui}','DEF','{sab}')""".format(atui=atui,sab=sab,cui=cui)
                cursor.execute(sql)
                sql = """INSERT INTO new_def_map (cui, atui, node_definition, sab) VALUES ('{cui}','{atui}',"{node_definition}", '{sab}')""".format(atui=atui,sab=sab,cui=cui,node_definition=node_definition)
                cursor.execute(sql)
    
                #commit every 10,000 records
                if record_count % 10000 == 0:
                    print('.', end='', flush=True)
                    connection.commit()
                
            connection.commit()
        

    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        

def transform(config):
    '''
    This coordinates the transform methods.  
    
    param dict config: The configuration data for this application.
    '''
    
    build_xref_table(config)
    
    # This code is temporary.  It should be moved to a pre-processing step
    fix_dbxrefs(config)
    # END This code is temporary.  It should be moved to a pre-processing step

    
    build_ambiguous_codes_table(config)
    build_ontology_uri_to_umls_map_table(config)
    build_relations_table(config)
    insert_new_cuis(config)
    insert_new_codes(config)
    insert_new_terms(config)
    insert_new_defs(config)
    insert_new_cui_cui_relations(config)
    print('') # do this to disable the 'end' flag in prior print statements
    print("Done with transform process")
    
def load(config):
    '''
    This method initiates the .CSV file export process.
    
    param dict config: The configuration data for this application.
    '''
    export_files(config)
    print('') # do this to disable the 'end' flag in prior print statements
    print("Done with load process")

def export_files(config):
    '''
    This method walks through the subset of mysql tables and generates a sets of .CSV files.  These
    .CSV files adhere to the Neo4j 'CSV file header format' found here:
    https://neo4j.com/docs/operations-manual/current/tools/import/file-header-format/
    This method matches the mysql table with a file_name and manages any column header adjustments
    that need to be made.
    
    param dict config: The configuration data for this application.
    '''
    connection = None
    sql = ''
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'],
            charset='utf8mb4',collation='utf8mb4_bin')
        cursor = connection.cursor(dictionary=True)
        
        
        export_table_info = [{'table_name': 'umls_codes', 'file_name':'CODEs.csv','sql_columns':['codeid','sab','code'],'file_columns':['CodeID:ID','SAB','CODE']},
                             {'table_name': 'umls_tui_rel', 'file_name':'TUIrel.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']},
                             {'table_name': 'umls_cui_tuis', 'file_name':'CUI-TUIs.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']},
                             {'table_name': 'umls_cui_cuis', 'file_name':'CUI-CUIs.csv','sql_columns':['start_id','end_id','type','sab'],'file_columns':[':START_ID',':END_ID',':TYPE','SAB']},
                             {'table_name': 'cui_codes_updated', 'file_name':'CUI-CODEs.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']},
                             {'table_name': 'code_suis_updated', 'file_name':'CODE-SUIs.csv','sql_columns':['start_id','end_id','type','cui'],'file_columns':[':START_ID',':END_ID',':TYPE','CUI']},
                             {'table_name': 'cui_suis_updated', 'file_name':'CUI-SUIs.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']},
                             {'table_name': 'cuis_updated', 'file_name':'CUIs.csv','sql_columns':['cui'],'file_columns':['CUI:ID']},
                             {'table_name': 'suis_updated', 'file_name':'SUIs.csv','sql_columns':['sui','name'],'file_columns':['SUI:ID','name']},
                             {'table_name': 'umls_tuis', 'file_name':'TUIs.csv','sql_columns':['tui','name','stn','def'],'file_columns':['TUI:ID','name','STN','DEF']},
                             {'table_name': 'defs_updated', 'file_name':'DEFs.csv','sql_columns':['atui','sab','def'],'file_columns':['ATUI:ID','SAB','DEF']},
                             {'table_name': 'def_rel_updated', 'file_name':'DEFrel.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']}]
        '''
        This method walks through the subset of mysql tables found in the export_table_info variable.  Each entry
        in export_table_info contains:
                                table_name: the mysql table name to export
                                file_name: the name of the .CSV file to be generated
                                sql_columns: a list of the columns to be includes in the SELECT statement
                                file_columns: a list of the column headers to use when writing the data to the .CSV files
                                    The sql_columns and file_columns should map 1:1.  For example in the table_name umls_codes and file_name CODEs.csv entry:
                                        codeid SQL column becomes -> CodeID:ID in the .CSV file
                                        sab SQL column becomes -> SAB in the .CSV file
                                        code SQL column becomes -> CODE in the .CSV file
        '''

        for export_info in export_table_info:
            # walk through all the entries in the export_table_info list
            table_name = export_info['table_name']
            file_name = export_info['file_name']
            sql_columns = export_info['sql_columns']
            file_columns = export_info['file_columns']
            
            file_path = os.path.join(config['OUTPUT_DIR'],file_name)
            # set the output file path
            
            sql = """SELECT DISTINCT {col_list} FROM {table_name}""".format(table_name=table_name,col_list=",".join(sql_columns))
            # build the SELECT statement from the sql_columns variable.  Also, apply a SQL 'DISTINCT' keyword to avoid duplicates 
            cursor.execute(sql)
            result = cursor.fetchall()
            print("")
            print ("Writing data from {table_name} to file {file_path}".format(table_name=table_name,file_path=file_path), end='', flush=True)
            
            f = open(file_path, 'w')
            record_count = 0
            writer = csv.writer(f,quoting=csv.QUOTE_ALL)
            writer.writerow(file_columns)
            # write the file_columns as the headers for the .CSV file
            
            data_rows = []
            for result_row in result:
                data_list = []
                for field in sql_columns:
                    data_list.append(result_row[field])
                data_rows.append(data_list)
                record_count = record_count + 1

                #write every 100,000 records
                if record_count % 100000 == 0:
                    print('.', end='', flush=True)
                    writer.writerows(data_rows)
                    # clear data_rows
                    data_rows = []
                
            writer.writerows(data_rows)
            f.close()        
        
    except mysql.connector.Error as err:
        print("Error in SQL: " + sql )
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        connection.rollback()
    finally:
        if connection != None:
            connection.close()        
        
        
        
# utility function
def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('commands', type=str, nargs='+',default='extract transform load')
    command_list = []
    try:
        args = parser.parse_args()
        command_list =  args.commands
    except:
        command_list = ['extract','extract_non_umls','transform','load']

    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
    #file_path = '/home/chb69/git/ontology-api/src/neo4j_loader'
    file_name = 'app.cfg'
    config = load_config(file_path, file_name)
    

    #extract_non_umls(config)
    #transform(config)
    #load(config)
    
    if 'extract_non_umls' in command_list:
        extract_non_umls(config)
    if 'extract' in command_list:
        extract(config)
    if 'transform' in command_list:
        transform(config)
    if 'load' in command_list:
        load(config)
    
    print("Done")


