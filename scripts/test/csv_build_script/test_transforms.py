import unittest

from scripts.csv_build_script.transforms import Transforms

class TestTransforms(unittest.TestCase):

    def setUp(self):
        self.transforms = Transforms()

    def test_file_from_uri(self):
        result = self.transforms.file_from_uri("http://purl.obolibrary.org/obo/UBERON_0010580")
        self.assertEqual(result, "UBERON_0010580")

    def test__dbxref_to_codeid_default(self):
        result = self.transforms._dbxref_to_codeid("SAB", "C123")
        self.assertEqual(result, "SAB C123")

    def test__dbxref_to_codeid_go(self):
        result = self.transforms._dbxref_to_codeid("GO", "C123")
        self.assertEqual(result, "GO GO:C123")

    def test__dbxref_to_codeid_case(self):
        result = self.transforms._dbxref_to_codeid("go", "c123")
        self.assertEqual(result, "GO GO:C123")

    def test_node_dbxref_to_codeid_default(self):
        result = self.transforms.node_dbxref_to_codeid("umls:c0026973")
        self.assertEqual(result, "UMLS C0026973")

    def test_node_dbxref_to_codeid_go(self):
        result = self.transforms.node_dbxref_to_codeid("go:0043209")
        self.assertEqual(result, "GO GO:0043209")

    def test_node_id_to_codeid_default(self):
        result = self.transforms.node_id_to_codeid("http://purl.obolibrary.org/obo/UBERON_0001106")
        self.assertEqual(result, "UBERON 0001106")

    def test_node_id_to_codeid_go(self):
        result = self.transforms.node_id_to_codeid("http://purl.obolibrary.org/obo/GO_0007623")
        self.assertEqual(result, "GO GO:0007623")

    def test_new_codeid_line_from_codeid(self):
        result = self.transforms.new_codeid_line_from_codeid("GO GO:0007623")
        self.assertEqual(result, '"GO GO:0007623","GO","GO:0007623"')
