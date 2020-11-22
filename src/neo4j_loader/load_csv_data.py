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


"""
        this list includes the prefixes for several informatics resources found in the mapping data: 
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
    """This method was heavily borrowed from the flask config.py file's from_pyfile method.
    It reads a file containing python constants and loads it into a dictionary.

    :param root_path: the path leading to the config file
    :param filename: the filename of the config relative to the
                     root path.
    """
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
    connection = None
    try:
        connection = mysql.connector.connect(
            host=config['MYSQL_HOSTNAME'],
            user=config['MYSQL_USERNAME'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DATABASE_NAME'])
        cursor = connection.cursor()
        with open(config['INDEX_CREATE_SQL_FILEPATH'], encoding="utf-8") as f:
            commands = f.read().split(';')
            for command in commands:
                if str(command).strip() != "":
                    print('Executing: ' + command)
                    cursor.execute(command)
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

def load_ccf_nodes_and_edges(config):
    """Adding the SAB column to edge_list, node_metadata
    The SAB in the edge_list allows us to track the source of the edge
    The SAB in node_metadata allows us to create a duplicate code (ex: an UBERON code from UBERON and one from CCF)
    """
    file_path = '/home/chb69/umls_data/ccf/ccf.nt'

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

        print("Removing CCF data from edge_list")
        sql = "DELETE FROM edge_list WHERE sab = 'CCF'"
        cursor.execute(sql)
        connection.commit()

        print("Removing CCF data from node_metadata")
        sql = "DELETE FROM node_metadata WHERE sab = 'CCF'"
        cursor.execute(sql)
        connection.commit()

        print("Loading CCF data into edge_list and node_metadata", end='', flush=True)

        with open(file_path) as triple_data:  
            for triple in triple_data:
                triple_elements = str(triple).split('> ')
                subject = triple_elements[0]
                if str(subject).startswith('<'):
                    subject = subject.replace('<','')
                predicate = triple_elements[1]
                if str(predicate).startswith('<'):
                    predicate = predicate.replace('<','')
                object = triple_elements[2]
                if str(object).startswith('<'):
                    object = object.replace('<','')
                if str(object).startswith('"'):
                    object = object[:-3].replace('"','')

                if 'UBERON' in subject and 'UBERON' in object and 'ccf_part_of' in predicate:
                    sql = "INSERT INTO edge_list (subject,predicate,object,sab) VALUES ('{subject}','{predicate}','{object}','{sab}')".format(subject=subject,predicate='http://purl.obolibrary.org/obo/BFO_0000050',object=object,sab='CCF')
                    cursor.execute(sql)
                    record_count = record_count + 1

                if 'UBERON' in subject and 'rdf-schema#label' in predicate:
                    sql = "INSERT INTO node_metadata (node_id,node_label,node_definition,sab) VALUES ('{subject}',\"{object}\",'None','{sab}')".format(subject=subject,object=object,sab='CCF')
                    cursor.execute(sql)
                    record_count = record_count + 1

                #commit every 10,000 records
                if record_count % 10000 == 0:
                    print('.', end='', flush=True)
                    connection.commit()
        print('') # do this to disable the 'end' flag in prior print statements
        connection.commit()
        print ("Done loading the CCF data.")
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


def load_pkl_edge_list(config):
    file_path = '/home/chb69/umls_data/PheKnowLator/PheKnowLatorResultsFromDropbox/PheKnowLator_Subclass_OWLNETS_edge_list_16OCT2020.txt'
    table_name = 'edge_list'
    load_file(config, file_path, table_name)

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

        sql = "UPDATE edge_list SET sab = 'UBERON' WHERE subject LIKE 'http://purl.obolibrary.org/obo/UBERON\_%' AND object LIKE 'http://purl.obolibrary.org/obo/UBERON\_%'"
        cursor.execute(sql)
        connection.commit()
        sql = "UPDATE edge_list SET sab = 'CL' WHERE subject LIKE 'http://purl.obolibrary.org/obo/CL\_%' AND object LIKE 'http://purl.obolibrary.org/obo/CL\_%'"
        cursor.execute(sql)
        connection.commit()
        print ("Done loading the edge_list data.")
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

def load_pkl_node_metadata(config):
    '''
    Load the PheKnowLator Node Metadata file.  This file does not get processed like the other files because it 
    contains non-ASCII characters  like this:
    http://purl.obolibrary.org/obo/UBERON_0002203   vasculature of eye|眼部血管系统 Vasculature that is part of the eye region.|是眼部区域一部分的血管系统。  
    In this case, we want to import the ASCII data portion of the record into mysql while excluding the other parts. 
    '''
    file_path = '/home/chb69/umls_data/PheKnowLator/PheKnowLatorResultsFromDropbox/PheKnowLator_Subclass_OWLNETS_NodeMetadata_16OCT2020.txt'
    table_name = 'node_metadata'
    
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

        with open(file_path) as csvfile:
            myCSVReader = None
            if file_path.endswith('.txt'):
                myCSVReader = csv.DictReader(csvfile, delimiter='\t')
            else:
                myCSVReader = csv.DictReader(csvfile)
            field_names = myCSVReader.fieldnames
            field_list_str = '%s' % ', '.join(map(str, field_names))
            field_list_str = field_list_str.replace(':ID', '')
            field_list_str = field_list_str.replace(':', '')
            value_list_str = ''
            for field in field_names:
                value_list_str += '%({field})s, '.format(field=field)
            value_list_str = value_list_str[:-2]
            sql = """INSERT INTO {table_name}({field_list})
                        VALUE ({value_list})""".format(table_name=table_name, field_list=field_list_str, value_list=value_list_str)
            print("Loading data from {file_name} into table {table_name}".format(file_name=file_path, table_name=table_name), end='', flush=True)
            for row in myCSVReader:

                if isascii(str(row)):
                    # use row directly when csv headers match column names.
                    if None in row.keys():
                        row.pop(None)
                    cursor.execute(sql, row)
                else:
                    """Handle the case where the row contains non-ASCII data like this:
                    http://purl.obolibrary.org/obo/UBERON_0002203   vasculature of eye|眼部血管系统 Vasculature that is part of the eye region.|是眼部区域一部分的血管系统。  """
                    if '|' in str(row['node_label']):
                        # split the node_label column using '|'
                        # then determine which part of the column is ASCII and use that for the node_label value
                        node_label_list = str(row['node_label']).split('|')
                        new_node_label = node_label_list[0]
                        if isascii(node_label_list[1]):
                            new_node_label = node_label_list[1]
                        row['node_label'] = new_node_label
                    if '|' in str(row['node_definition']):
                        # split the node_definition column using '|'
                        # then determine which part of the column is ASCII and use that for the node_definition value
                        node_def_list = str(row['node_definition']).split('|')
                        new_node_def = node_def_list[0]
                        if isascii(node_def_list[1]):
                            new_node_def = node_def_list[1]
                        row['node_definition'] = new_node_def
                    cursor.execute(sql, row)
                record_count = record_count + 1
                #commit every 200,000 records
                if record_count % 200000 == 0:
                    print('.', end='', flush=True)
                    connection.commit()
                    
        print('') # do this to disable the 'end' flag in prior print statements
        connection.commit()
        print ("Done loading the {table_name} table.".format(table_name=table_name))

        # Set the SAB value for the data in the node_metadata table
        sql = "UPDATE node_metadata SET sab = 'UBERON' WHERE node_id LIKE 'http://purl.obolibrary.org/obo/UBERON\_%'"
        cursor.execute(sql)
        connection.commit()
        sql = "UPDATE node_metadata SET sab = 'CL' WHERE node_id LIKE 'http://purl.obolibrary.org/obo/CL\_%'"
        cursor.execute(sql)
        connection.commit()
        print ("Done loading the node_metadata data.")
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
    
def load_pkl_ontology_dbxref(config):
    file_path = '/home/chb69/umls_data/PheKnowLator/PheKnowLatorResultsFromDropbox/PheKnowLator_Subclass_OWLNETS_Ontology_DbXRef_16OCT2020.txt'
    table_name = 'ontology_dbxref'
    load_file(config, file_path, table_name)
    
def load_pkl_relations(config):
    file_path = '/home/chb69/umls_data/PheKnowLator/PheKnowLatorResultsFromDropbox/PheKnowLator_Subclass_OWLNETS_relations_16OCT2020.txt'
    table_name = 'relations'
    load_file(config, file_path, table_name)

def load_umls_codes(config):
    file_path = '/home/chb69/umls_data/umls_data/CODEs.csv'
    table_name = 'codes'
    load_file(config, file_path, table_name)

def load_umls_defs(config):
    file_path = '/home/chb69/umls_data/umls_data/DEFs.csv'
    table_name = 'defs'
    load_file(config, file_path, table_name)

def load_umls_suis(config):
    file_path = '/home/chb69/umls_data/umls_data/SUIs.csv'
    table_name = 'suis'
    load_file(config, file_path, table_name)

def load_umls_cuis(config):
    file_path = '/home/chb69/umls_data/umls_data/CUIs.csv'
    table_name = 'cuis'
    load_file(config, file_path, table_name)

def load_umls_tuis(config):
    file_path = '/home/chb69/umls_data/umls_data/TUIs.csv'
    table_name = 'tuis'
    load_file(config, file_path, table_name)

def load_umls_code_suis(config):
    file_path = '/home/chb69/umls_data/umls_data/CODE-SUIs.csv'
    table_name = 'code_suis'
    load_file(config, file_path, table_name)

def load_umls_cui_codes(config):
    file_path = '/home/chb69/umls_data/umls_data/CUI-CODEs.csv'
    table_name = 'cui_codes'
    load_file(config, file_path, table_name)

def load_umls_cui_cuis(config):
    file_path = '/home/chb69/umls_data/umls_data/CUI-CUIs.csv'
    table_name = 'cui_cuis'
    load_file(config, file_path, table_name)

def load_umls_cui_suis(config):
    file_path = '/home/chb69/umls_data/umls_data/CUI-SUIs.csv'
    table_name = 'cui_suis'
    load_file(config, file_path, table_name)

def load_umls_cui_tuis(config):
    file_path = '/home/chb69/umls_data/umls_data/CUI-TUIs.csv'
    table_name = 'cui_tuis'
    load_file(config, file_path, table_name)
                                
def load_umls_def_rel(config):
    file_path = '/home/chb69/umls_data/umls_data/DEFrel.csv'
    table_name = 'def_rel'
    load_file(config, file_path, table_name)
                                
def load_umls_tui_rel(config):
    file_path = '/home/chb69/umls_data/umls_data/TUIrel.csv'
    table_name = 'tui_rel'
    load_file(config, file_path, table_name)
  
def build_xref_table(config):
    '''
    Build the dbxrefs table by reading the ontology_dbxref table.  The ontology_dbxref table contains a column dbxrefs.
    This method takes dbxrefs, a pipe-delimited list of xrefs, and splits it into separate entries (ex: xref1|xref2|xref3).
    Each individual xref becomes a new row in the dbxrefs table.  
    
    :param dict config: The configuration settings 
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
        drop_table_sql = "DROP TABLE IF EXISTS dbxrefs"
        cursor.execute(drop_table_sql)
        create_table_sql = """CREATE TABLE dbxrefs (
                id INT NOT NULL AUTO_INCREMENT,
                ontology_uri VARCHAR(2048) NOT NULL,
                xref VARCHAR(2048) NOT NULL,
                PRIMARY KEY(id)
                );"""
        cursor.execute(create_table_sql)
        cursor.execute("SELECT ontology_uri, dbxrefs FROM ontology_dbxref WHERE ontology_uri LIKE 'http://purl.obolibrary.org/obo/CL_%' OR ontology_uri LIKE 'http://purl.obolibrary.org/obo/UBERON_%'")
        print("Loading data into table {table_name}".format(table_name="dbxrefs"), end='', flush=True)
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

def extract(config):
    '''
    The extract method loads the CSV and tab-delimited files into mysql tables mirroring their file structure.
    
    param dict config: The configuration data for this application 
    '''
    create_database(config)
    load_pkl_node_metadata(config)
    load_pkl_relations(config)
    load_pkl_ontology_dbxref(config)
    load_pkl_edge_list(config)
    # load_ccf_nodes_and_edges(config)
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
    build_xref_table(config)
    create_indices(config)
    print("Done with extract process")

def build_ontology_uri_to_umls_map_table(config):
    '''
    Construct a table called ontology_uri_map (ontology_uri, cui, codeid, type, sab).  This table is a mapping
    between the PheKnowLator data and the UMLS data.  The table is built from dbxrefs (PheKnowLator) and cui_codes (ULMS)
    tables.  The ontology_uri is the primary key within the PheKnowLator data.  The cui and codeid are the main keys
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
                sab VARCHAR(50),
                PRIMARY KEY(id)
                );"""
        cursor.execute(create_table_sql)
        print("Created table ontology_uri_map")
        sql = """INSERT INTO ontology_uri_map (ontology_uri, cui) 
        SELECT DISTINCT ontology_uri, upper(substring(xref,instr(xref, ':')+1)) as CUI FROM dbxrefs
        WHERE substring_index(xref,':', 1) = 'umls'"""
        # This query loads all the ontology_uri's that map directly to a UMLS CUI according to the dbxrefs table
        # these records will have their codeid column set to NULL
        cursor.execute(sql)
        connection.commit()
        print("Loaded UMLS map into table ontology_uri_map")
        
        sql = """INSERT INTO ontology_uri_map (ontology_uri, codeid, cui, type, sab) 
        SELECT DISTINCT ontology_uri, CONCAT('FMA ',upper(substring(xref,instr(xref, ':')+1))) as codeid, rel.start_id as cui, 'PT' as type, 'FMA' as sab
        FROM dbxrefs, cui_codes as rel
        WHERE substring_index(xref,':', 1) = 'fma'
        AND CONCAT('FMA ',upper(substring(xref,instr(xref, ':')+1))) = rel.end_id"""
        # This query loads all the ontology_uri's that map directly to an FMA code according to the dbxrefs table
        cursor.execute(sql)
        connection.commit()
        print("Loaded FMA map into table ontology_uri_map")
        
        sql = """INSERT INTO ontology_uri_map (ontology_uri, codeid, cui, type, sab)
        SELECT DISTINCT ontology_uri, CONCAT('NCI ',upper(substring(xref,instr(xref, ':')+1))) as codeid, rel.start_id as cui, 'PT' as type, 'NCI' as sab
        FROM dbxrefs, cui_codes as rel
        WHERE substring_index(xref,':', 1) = 'ncit'
        AND CONCAT('NCI ',upper(substring(xref,instr(xref, ':')+1))) = rel.end_id"""
        # This query loads all the ontology_uri's that map directly to an NCI Thesaurus code according to the dbxrefs table
        cursor.execute(sql)
        connection.commit()
        print("Loaded NCIT map into table ontology_uri_map")
        
        sql = """INSERT INTO ontology_uri_map (ontology_uri, codeid, cui, type, sab)
        SELECT DISTINCT ontology_uri, CONCAT('MSH ',upper(substring(xref,instr(xref, ':')+1))) as codeid, rel.start_id as cui, 'PT' as type, 'MSH' as sab
        FROM dbxrefs, cui_codes as rel
        WHERE substring_index(xref,':', 1) = 'mesh'
        AND CONCAT('MSH ',upper(substring(xref,instr(xref, ':')+1))) = rel.end_id
        AND instr(xref, 'mesh:d') > 0
        AND instr(xref, 'mesh:d24') = 0"""
        # This query loads all the ontology_uri's that map directly to a MeSH code according to the dbxrefs table
        cursor.execute(sql)
        connection.commit()
        print("Loaded MESH map into table ontology_uri_map")
        
        sql = """INSERT INTO ontology_uri_map (ontology_uri, codeid, cui, type, sab)
        SELECT DISTINCT ontology_uri, CONCAT('SNOMEDCT_US ',upper(substring(xref,instr(xref, 'details/')+8))) as codeid, rel.start_id as cui, 'PT' as type, 'SNOMEDCT_US' as sab
        FROM dbxrefs, cui_codes as rel
        WHERE substring_index(xref,'details/', 1) = 'http://www.snomedbrowser.com/codes/'
        AND CONCAT('SNOMEDCT_US ',upper(substring(xref,instr(xref, 'details/')+8))) = rel.end_id"""
        # This query loads all the ontology_uri's that map directly to a SNOMED code according to the dbxrefs table
        cursor.execute(sql)
        connection.commit()
        print("Loaded SNOMED map into table ontology_uri_map")
        
        # add indices after loading to speed up the load
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_ontology_uri_idx(ontology_uri(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_cui_idx(cui(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_codeid_idx(codeid(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_type_idx(type(50))"
        cursor.execute(sql)
        sql = "ALTER TABLE ontology_uri_map ADD INDEX ontology_uri_map_sab_idx(sab(50))"
        cursor.execute(sql)
        print("Built indices for table ontology_uri_map")

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
    inserts data into the cui_cuis table.
    
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
        sql = """DELETE FROM cui_cuis WHERE sab = 'UBERON'"""
        cursor.execute(sql)
        connection.commit()
        print("Deleted UBERON map from table cui_cuis")


        sql = """INSERT INTO cui_cuis (start_id, type, end_id, sab)
        SELECT DISTINCT subject_table.cui as start_id, if(rel.relation_label='subclass of', 'isa',lower(replace(rel.relation_label,' ','_'))) as type, object_table.cui as end_id, 'UBERON' as sab
        FROM edge_list el, relations rel, ontology_uri_map subject_table, ontology_uri_map object_table
        WHERE rel.relation_id = el.predicate
        AND subject_table.ontology_uri = el.subject
        AND object_table.ontology_uri = el.object
        AND subject_table.cui != object_table.cui
        AND el.sab = 'UBERON'"""
        """
        This query needs some explanation.  Basically, the edge_list table is the central table in the query.  We use the edge_list
        table structure (subject, predicate, object) to find records where the edge_list contains relationships between
        UBERON subject and UBERON object.  This record will become a new relationship between 2 CUIs.  We take the UBERON subject and UBERON object
        and match them to their ontology_uri_map entries.  This allows us to determine their CUIs.  Lastly, we map from the
        edge_list relation_id to the "English" relation_label.  This becomes the label for the relationship in the CUI to CUI relationship.  
        """
        cursor.execute(sql)
        connection.commit()
        print("Loaded UBERON map into table cui_cuis")

        sql = """DELETE FROM cui_cuis WHERE sab = 'CL'"""
        cursor.execute(sql)
        connection.commit()
        print("Deleted CL map from table cui_cuis")

        # NOTE: I added sab to the edge_list table, so we can filter this query more easily on sab = 'CL'
        sql = """INSERT INTO cui_cuis (start_id, type, end_id, sab)
        SELECT DISTINCT subject_table.cui as start_id, if(rel.relation_label='subclass of', 'isa',lower(replace(rel.relation_label,' ','_'))) as type, object_table.cui as end_id, 'CL' as sab
        FROM edge_list el, relations rel, ontology_uri_map subject_table, ontology_uri_map object_table
        WHERE rel.relation_id = el.predicate
        AND subject_table.ontology_uri = el.subject
        AND object_table.ontology_uri = el.object
        AND subject_table.cui != object_table.cui
        AND el.sab = 'CL'"""
        # This query is basically the same as the UBERON query above except it finds CL to CL relationships
        cursor.execute(sql)
        connection.commit()
        print("Loaded CL map into table cui_cuis")

        sql = """DELETE FROM cui_cuis WHERE sab = 'CCF'"""
        """cursor.execute(sql)
        connection.commit()
        print("Deleted CCF map from table cui_cuis")"""

        sql = """INSERT INTO cui_cuis (start_id, type, end_id, sab)
        SELECT DISTINCT subject_table.cui as start_id, if(rel.relation_label='subclass of', 'isa',lower(replace(rel.relation_label,' ','_'))) as type, object_table.cui as end_id, 'CCF' as sab
        FROM edge_list el, relations rel, ontology_uri_map subject_table, ontology_uri_map object_table
        WHERE rel.relation_id = el.predicate
        AND subject_table.ontology_uri = el.subject
        AND object_table.ontology_uri = el.object
        AND subject_table.cui != object_table.cui
        AND el.sab = 'CCF'"""
        
        """
        cursor.execute(sql)
        connection.commit()
        print("Loaded CCF map into table cui_cuis")"""
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

def connect_existing_terms(config):
    #NOTE: THIS METHOD DEPENDS ON THE insert_new_terms METHOD TO BE RUN FIRST.  
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
        

        sql = """SELECT oum.cui AS cui, oum.codeid AS codeid,  su.sui as sui, nm.sab as sab
        FROM node_metadata nm, ontology_uri_map oum, suis_updated su
        where nm.node_id = oum.ontology_uri
        AND nm.node_label = su.name
        AND oum.codeid IS NOT NULL
        AND (oum.codeid, su.sui) not in (SELECT start_id, end_id FROM code_suis_updated)"""
        
        cursor.execute(sql)
        result = cursor.fetchall()
        print ("Loading existing data into tables suis_updated and code_suis_updated", end='', flush=True)
        record_count = 1 # start SUI numbering at one 
        for row in result:
            cui = row['cui']
            codeid = row['codeid']
            sui = row['sui']
            record_count = record_count + 1

            if str(codeid).count(' ') > 1:
                print("ERROR: this code '{codeid}' contains more than one space.  Stopping processing".format(codeid=codeid))
                sys.exit()
            
            sql = """INSERT INTO code_suis_updated (start_id, end_id, type, cui) VALUES ('{codeid}','{sui}','PT','{cui}')""".format(codeid=codeid,sui=sui,cui=cui)
            cursor.execute(sql)
            sql = """INSERT INTO cui_suis_updated (start_id, end_id, type) VALUES ('{cui}','{sui}','PREF_TERM')""".format(cui=cui,sui=sui)
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

def insert_new_terms(config):
    '''
    The method creates new labels (Term nodes) in the graph for each PheKnowLator item added to the graph.
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
        sql = """INSERT INTO cui_suis_updated SELECT * FROM cui_suis"""
        cursor.execute(sql)
        connection.commit()
        
        sql = "DROP INDEX suis_updated_sui_idx ON suis_updated"
        cursor.execute(sql)
        connection.commit()
        sql = "DROP INDEX suis_updated_name_idx ON suis_updated"
        cursor.execute(sql)
        connection.commit()

        print ("Copying suis INTO suis_updated")
        sql = """INSERT INTO suis_updated SELECT * FROM suis"""
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
        sql = """INSERT INTO code_suis_updated SELECT * FROM code_suis"""
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
        
        sql = """SELECT DISTINCT ontology_uri, cui, codeid, label, sab, sui FROM (
        SELECT oum.ontology_uri as ontology_uri, oum.cui AS cui, oum.codeid AS codeid,  nm.node_label AS label, nm.sab as sab, su.sui AS sui
                FROM node_metadata nm
                INNER JOIN ontology_uri_map oum
                ON nm.node_id = oum.ontology_uri
                LEFT OUTER JOIN suis_updated su
                ON nm.node_label = su.name
                WHERE nm.sab IN ('UBERON', 'CL')
                AND (oum.codeid is null OR oum.codeid NOT IN (select start_id FROM code_suis_updated))
        UNION ALL
        SELECT oum.ontology_uri as ontology_uri, oum.cui AS cui, replace(substring_index(oum.ontology_uri, '/',-1), '_', ' ') AS codeid,  nm.node_label AS label, nm.sab as sab, su.sui AS sui
                FROM node_metadata nm
                INNER JOIN ontology_uri_map oum
                ON nm.node_id = oum.ontology_uri
                LEFT OUTER JOIN suis_updated su
                ON nm.node_label = su.name
                WHERE replace(substring_index(oum.ontology_uri, '/',-1), '_', ' ') NOT IN (select start_id FROM code_suis_updated) ) source_table
        """
        """This query joins the ontology_uri_map data to the label from the node_metadata table.  The query only returns
        records where the codeid is NULL or the codeid is missing from the code_suis_updated table.  These represent
        records that need a new SUI minted."""
        cursor.execute(sql)
        result = cursor.fetchall()
        print ("Loading tables suis_updated, code_suis_updated, and new_sui_map", end='', flush=True)
        record_count = 1 # start SUI numbering at one 
        for row in result:
            cui = row['cui']
            codeid = row['codeid']
            label = row['label']

            if codeid == None:
                # if the codeid is None, construct it from the ontology_uri
                ontology_uri = row['ontology_uri']
                code = ontology_uri[ontology_uri.index('_')+1:]
                codeid = row['sab'] + ' ' + code 
            
            if codeid == 'UBERON 0000048' or codeid == 'UBERON 0000046':
                print("here")   

            sui = row['sui']
            if sui == None:                   
                sui = 'HS' + str(record_count).zfill(6)
                # mint a new SUI prefixed with 'HS'                
                sql = """INSERT INTO suis_updated (sui, name) VALUES ('{sui}',"{name}")""".format(sui=sui,name=label)
                cursor.execute(sql)
                sql = """INSERT INTO new_sui_map (codeid, sui, name) VALUES ('{codeid}','{sui}',"{name}")""".format(codeid=codeid,sui=sui,name=label)
                cursor.execute(sql)

            sql = """INSERT INTO code_suis_updated (start_id, end_id, type, cui) VALUES ('{codeid}','{sui}','PT','{cui}')""".format(codeid=codeid,sui=sui,cui=cui)
            cursor.execute(sql)

            if 'HC' in cui:
                sql = """INSERT INTO cui_suis_updated (start_id, end_id, type) VALUES ('{cui}','{sui}','PREF_TERM')""".format(cui=cui,sui=sui)
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
    Find every entry in the node_metadata table that is missing from the ontology_uri_map table.  This indicates an
    UBERON or Cell Ontology (CL) record that was not mapped to any existing UMLS code.  This means the record needs a 
    new CUI minted for it.
      
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
        sql = """INSERT INTO cuis_updated SELECT * FROM cuis"""
        cursor.execute(sql)
        connection.commit()
        
        print ("Deleting HuBMAP CUIs")
        sql = """DELETE FROM ontology_uri_map WHERE cui LIKE 'HC%'"""
        cursor.execute(sql)
        connection.commit()

        print ("Copying cuis INTO cui_codes_updated")
        sql = """INSERT INTO cui_codes_updated SELECT * FROM cui_codes"""
        cursor.execute(sql)
        connection.commit()

        print ("Deleting UBERON, CCF, and CL codes from codes")
        sql = """DELETE FROM codes WHERE sab IN ('UBERON','CL','CCF')"""
        cursor.execute(sql)
        connection.commit()


        sql = """select node_id as ontology_uri, sab as sab from node_metadata nm
        where nm.node_id NOT IN (select ontology_uri from ontology_uri_map)
        and (node_id like 'http://purl.obolibrary.org/obo/CL\_%' or node_id like 'http://purl.obolibrary.org/obo/UBERON\_%')"""
        """Find all the records in node_metadata that were not mapped to an UMLS terms."""
        cursor.execute(sql)
        result = cursor.fetchall()
        print ("Creating new HCUI's and codes")
        record_count = 1 # start HCUI numbering at one 
        for row in result:
            ontology_uri = row['ontology_uri']
            cui = 'HC' + str(record_count).zfill(6)
            record_count = record_count + 1

            current_sab = 'UBERON'

            if row['sab'] is not None:
                current_sab = row['sab']
            elif 'CL_' in ontology_uri:
                current_sab = 'CL'
            
            
            code = ontology_uri[ontology_uri.index('_')+1:]
            if current_sab == 'CCF':
                code = ontology_uri[ontology_uri.rindex('/')+1:]
                print("ERROR: encountered CCF data.  Stopping processing".format(codeid=codeid))
                sys.exit()
                
            codeid = current_sab + ' ' + code 
            if codeid == 'CCF 0002078':
                print("here")
            if str(codeid).count(' ') > 1:
                print("ERROR: this code '{codeid}' contains more than one space.  Stopping processing".format(codeid=codeid))
                sys.exit()

            
            sql = """INSERT INTO ontology_uri_map (ontology_uri,codeid,cui,sab) VALUES ('{ontology_uri}','{codeid}','{cui}','{sab}')""".format(codeid=codeid,cui=cui,ontology_uri=ontology_uri,sab=current_sab)
            cursor.execute(sql)
            sql = """INSERT INTO cuis_updated (cui) VALUES ('{cui}')""".format(cui=cui)
            cursor.execute(sql)
            connection.commit()

            sql = """INSERT INTO codes (codeid, sab,code) VALUES ('{codeid}','{sab}','{code}')""".format(codeid=codeid,sab=current_sab,code=code)
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

def insert_new_codes(config):
    '''    
    
      
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

        sql = """SELECT DISTINCT ontology_uri, cui, sab FROM (
        SELECT ontology_uri, cui, sab FROM ontology_uri_map oum
        WHERE codeid is not null
        AND sab NOT IN ('UBERON','CL','CCF')
        UNION ALL
        SELECT nm.node_id, oum.cui as cui, nm.sab as sab FROM node_metadata nm, ontology_uri_map oum
        WHERE nm.sab = 'CCF'
        AND oum.ontology_uri = nm.node_id) source_table"""
        cursor.execute(sql)
        result = cursor.fetchall()
        print ("Creating new codes")
        for row in result:
            ontology_uri = row['ontology_uri']
            cui = row['cui']

            current_sab = 'UBERON'
            if 'CL' in ontology_uri:
                current_sab = 'CL'
            code = ontology_uri[ontology_uri.index('_')+1:]
            codeid = current_sab + ' ' + code 
            """if row['sab'] == 'CCF':
                current_sab = row['sab']
                code = ontology_uri[ontology_uri.rindex('/')+1:]
                codeid = current_sab + ' ' + code
                if codeid == 'CCF 0002078':
                    print("here")
            else:
                code = ontology_uri[ontology_uri.index('_')+1:]
                codeid = current_sab + ' ' + code 
            """
            if str(codeid).count(' ') > 1:
                print("ERROR: this code '{codeid}' contains more than one space.  Stopping processing".format(codeid=codeid))
                sys.exit()

            sql = """INSERT INTO codes (codeid, sab,code) VALUES ('{codeid}','{sab}','{code}')""".format(codeid=codeid,sab=current_sab,code=code)
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
        

        print ("Copying defs INTO defs_updated")
        sql = """INSERT INTO defs_updated SELECT * FROM defs"""
        cursor.execute(sql)
        connection.commit()
        
        print ("Copying def_rel INTO def_rel_updated")
        sql = """INSERT INTO def_rel_updated SELECT * FROM def_rel"""
        cursor.execute(sql)
        connection.commit()

        sql = """SELECT cui, node_definition, IF(INSTR(oum.ontology_uri,'UBERON')>0,'UBERON','CL') as sab 
        FROM node_metadata nm, ontology_uri_map oum 
        WHERE nm.node_id = oum.ontology_uri
        AND node_definition <> 'None'
        AND node_definition <> '.'"""
        
        cursor.execute(sql)
        result = cursor.fetchall()
        print ("Loading tables defs_updated, def_rels_updated, and new_def_map", end='', flush=True)
        record_count = 1 # start SUI numbering at one 
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
    # re-order this.  Move CUI-CUI and HUI generation to end
    build_ontology_uri_to_umls_map_table(config)
    insert_new_cuis(config)
    insert_new_codes(config)
    insert_new_terms(config)
    #connect_existing_terms(config)
    insert_new_defs(config)
    insert_new_cui_cui_relations(config)
    print('') # do this to disable the 'end' flag in prior print statements
    print("Done with transform process")
    
def load(config):
    export_files(config)
    print('') # do this to disable the 'end' flag in prior print statements
    print("Done with load process")

def export_files(config):
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
        
        
        export_table_info = [{'table_name': 'codes', 'file_name':'CODEs.csv','sql_columns':['codeid','sab','code'],'file_columns':['CodeID:ID','SAB','CODE']},
                             {'table_name': 'tui_rel', 'file_name':'TUIrel.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']},
                             {'table_name': 'cui_tuis', 'file_name':'CUI-TUIs.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']},
                             {'table_name': 'cui_cuis', 'file_name':'CUI-CUIs.csv','sql_columns':['start_id','end_id','type','sab'],'file_columns':[':START_ID',':END_ID',':TYPE','SAB']},
                             {'table_name': 'cui_codes_updated', 'file_name':'CUI-CODEs.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']},
                             {'table_name': 'code_suis_updated', 'file_name':'CODE-SUIs.csv','sql_columns':['start_id','end_id','type','cui'],'file_columns':[':START_ID',':END_ID',':TYPE','CUI']},
                             {'table_name': 'cui_suis_updated', 'file_name':'CUI-SUIs.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']},
                             {'table_name': 'cuis_updated', 'file_name':'CUIs.csv','sql_columns':['cui'],'file_columns':['CUI:ID']},
                             {'table_name': 'suis_updated', 'file_name':'SUIs.csv','sql_columns':['sui','name'],'file_columns':['SUI:ID','name']},
                             {'table_name': 'tuis', 'file_name':'TUIs.csv','sql_columns':['tui','name','stn','def'],'file_columns':['TUI:ID','name','STN','DEF']},
                             {'table_name': 'defs_updated', 'file_name':'DEFs.csv','sql_columns':['atui','sab','def'],'file_columns':['ATUI:ID','SAB','DEF']},
                             {'table_name': 'def_rel_updated', 'file_name':'DEFrel.csv','sql_columns':['start_id','end_id'],'file_columns':[':START_ID',':END_ID']}]

        for export_info in export_table_info:
            table_name = export_info['table_name']
            file_name = export_info['file_name']
            sql_columns = export_info['sql_columns']
            file_columns = export_info['file_columns']
            
            file_path = config['OUTPUT_DIR'] + '/' + file_name
            
            sql = """SELECT DISTINCT {col_list} FROM {table_name}""".format(table_name=table_name,col_list=",".join(sql_columns))
            cursor.execute(sql)
            result = cursor.fetchall()
            print("")
            print ("Writing data from {table_name} to file {file_path}".format(table_name=table_name,file_path=file_path), end='', flush=True)
            
            f = open(file_path, 'w')
            record_count = 0
            writer = csv.writer(f,quoting=csv.QUOTE_ALL)
            writer.writerow(file_columns)
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
    file_path = '/home/chb69/git/ontology-api/src/neo4j_loader'
    file_name = 'app.cfg'
    config = load_config(file_path, file_name)
    #extract(config)
    #transform(config)
    load(config)

