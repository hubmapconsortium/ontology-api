# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class TermtypeTerm(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, termtype=None, term=None):  # noqa: E501
        """TermtypeTerm - a model defined in OpenAPI

        :param termtype: The termtype of this TermtypeTerm.  # noqa: E501
        :type termtype: str
        :param term: The term of this TermtypeTerm.  # noqa: E501
        :type term: str
        """
        self.openapi_types = {
            'termtype': str,
            'term': str
        }

        self.attribute_map = {
            'termtype': 'termtype',
            'term': 'term'
        }

        self._termtype = termtype
        self._term = term

    @classmethod
    def from_dict(cls, dikt) -> 'TermtypeTerm':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TermtypeTerm of this TermtypeTerm.  # noqa: E501
        :rtype: TermtypeTerm
        """
        return util.deserialize_model(dikt, cls)

    @property
    def termtype(self):
        """Gets the termtype of this TermtypeTerm.


        :return: The termtype of this TermtypeTerm.
        :rtype: str
        """
        return self._termtype

    @termtype.setter
    def termtype(self, termtype):
        """Sets the termtype of this TermtypeTerm.


        :param termtype: The termtype of this TermtypeTerm.
        :type termtype: str
        """

        self._termtype = termtype

    @property
    def term(self):
        """Gets the term of this TermtypeTerm.


        :return: The term of this TermtypeTerm.
        :rtype: str
        """
        return self._term

    @term.setter
    def term(self, term):
        """Sets the term of this TermtypeTerm.


        :param term: The term of this TermtypeTerm.
        :type term: str
        """

        self._term = term
