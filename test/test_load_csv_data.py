'''
Created on Nov 15, 2020

@author: chb69
'''
import unittest
import os
import types
from neo4j import GraphDatabase, TransactionError, CypherError


class TestLoadCsvData(unittest.TestCase):

    """cypher queries for testing.  This is returns codes with missing terms:
    here are some results: 3727 for MATCH (a:Code{SAB:‘UBERON’}) where size((a)--(:Term)) = 0 RETURN count(distinct a)
    
    10075 for MATCH (a:Code{SAB:‘UBERON’}) where size((a)--(:Term)) = 0 RETURN count(distinct a)
    
    another good test: compare record counts in SQL versus counts in neo4j (ex: codes table count vs code node counts) 
    maybe compare with file line counts
    
    """

    config = {}
    driver = None
    
    @staticmethod
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

    def get_driver(self):
        if self.driver.closed():
            self.driver = GraphDatabase.driver(self.config['NEO4J_SERVER'], auth=(self.config['NEO4J_USERNAME'], self.config['NEO4J_PASSWORD']), encrypted=False)
        return self.driver


    def setUp(self):
        file_path = '/home/chb69/git/ontology-api/src/neo4j_loader'
        file_name = 'app.cfg'
        self.config = TestLoadCsvData.load_config(file_path, file_name)
        self.driver = GraphDatabase.driver(self.config['NEO4J_SERVER'], auth=(self.config['NEO4J_USERNAME'], self.config['NEO4J_PASSWORD']), encrypted=False)

    def tearDown(self):
        if self.driver != None:
            if self.driver.closed() == False:
                self.driver.close()
        self.driver = None
            


    def testCCFCodesMatchUberon(self):
        driver = self.get_driver()
        with driver.session() as session:
            try:
                stmt = """MATCH (code1:Code {SAB: 'CCF'})-[r1:CODE]-(c:Concept)-[r2:CODE]-(code2:Code {SAB: 'UBERON'})  WHERE r1 is null and r2 is null RETURN COUNT(code1) AS data_count"""
                for record in session.run(stmt):
                    self.assertEqual(int(record['data_count']), 0)

            except ConnectionError as ce:
                print('A connection error occurred: ', str(ce.args[0]))
                raise ce
            except ValueError as ve:
                print('A value error occurred: ', ve.value)
                raise ve
            except CypherError as cse:
                print('A Cypher error was encountered: ', cse.message)
                raise cse
            except:
                print('A general error occurred: ')
            finally:
                driver.close()



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()