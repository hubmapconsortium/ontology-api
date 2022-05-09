# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.codes_codes_obj import CodesCodesObj  # noqa: E501
from openapi_server.models.concept_detail import ConceptDetail  # noqa: E501
from openapi_server.models.concept_term import ConceptTerm  # noqa: E501
from openapi_server.models.qqst import QQST  # noqa: E501
from openapi_server.models.sab_definition import SabDefinition  # noqa: E501
from openapi_server.models.sab_relationship_concept_prefterm import SabRelationshipConceptPrefterm  # noqa: E501
from openapi_server.models.semantic_stn import SemanticStn  # noqa: E501
from openapi_server.models.sty_tui_stn import StyTuiStn  # noqa: E501
from openapi_server.models.termtype_code import TermtypeCode  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_codes_code_id_codes_get(self):
        """Test case for codes_code_id_codes_get

        Returns a list of {Concept, Code} dictionaries associated with the code_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/codes/{code_id}/codes'.format(code_id='SNOMEDCT_US 254837009'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_codes_code_id_concepts_get(self):
        """Test case for codes_code_id_concepts_get

        Returns a list of {Concept, Prefterm} dictionaries associated with the code_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/codes/{code_id}/concepts'.format(code_id='SNOMEDCT_US 254837009'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_concepts_concept_id_codes_get(self):
        """Test case for concepts_concept_id_codes_get

        Returns a distinct list of codes associated with the concept_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/concepts/{concept_id}/codes'.format(concept_id='C0678222'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_concepts_concept_id_concepts_get(self):
        """Test case for concepts_concept_id_concepts_get

        Returns a list of {Sab, Relationship, Concept, Prefterm} dictionaries associated with the concept_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/concepts/{concept_id}/concepts'.format(concept_id='C0006142'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_concepts_concept_id_definitions_get(self):
        """Test case for concepts_concept_id_definitions_get

        Returns a list of {Sab, Definition} dictionaries associated with the concept_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/concepts/{concept_id}/definitions'.format(concept_id='C0006142'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_concepts_concept_id_semantics_get(self):
        """Test case for concepts_concept_id_semantics_get

        Returns a list of {Sty, Tui, Stn} dictionaries associated with the concept_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/concepts/{concept_id}/semantics'.format(concept_id='C0304055'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_semantics_semantic_id_semantics_get(self):
        """Test case for semantics_semantic_id_semantics_get

        Returns a list of {queryTUI, querySTN ,semantic, TUI_STN} dictionaries associated with the concept_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/semantics/{semantic_id}/semantics'.format(semantic_id='Physical Object'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terms_term_id_codes_get(self):
        """Test case for terms_term_id_codes_get

        Returns a list of {TermType, Code} dictionaries associated with the term_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/terms/{term_id}/codes'.format(term_id='Breast cancer'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terms_term_id_concepts_get(self):
        """Test case for terms_term_id_concepts_get

        Returns a list of Terms associated with the concept_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/terms/{term_id}/concepts'.format(term_id='lidocaine 0.05 MG/MG Medicated Patch'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terms_term_id_concepts_terms_get(self):
        """Test case for terms_term_id_concepts_terms_get

        Returns a list of {Concept, Term} dictionaries associated with the term_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/terms/{term_id}/concepts/terms'.format(term_id='Breast cancer'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tui_tui_id_semantics_get(self):
        """Test case for tui_tui_id_semantics_get

        Returns a list of {semantic, STN} dictionaries associated with the tui_id
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/tui/{tui_id}/semantics'.format(tui_id='T200'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
