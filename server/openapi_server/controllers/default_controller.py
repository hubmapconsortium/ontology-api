import connexion
import six

from openapi_server.models.codes_codes_obj import CodesCodesObj  # noqa: E501
from openapi_server.models.concept_detail import ConceptDetail  # noqa: E501
from openapi_server.models.concept_term import ConceptTerm  # noqa: E501
from openapi_server.models.full_capacity_term import FullCapacityTerm  # noqa: E501
from openapi_server.models.qqst import QQST  # noqa: E501
from openapi_server.models.sab_code_term import SabCodeTerm  # noqa: E501
from openapi_server.models.sab_definition import SabDefinition  # noqa: E501
from openapi_server.models.sab_relationship_concept_prefterm import SabRelationshipConceptPrefterm  # noqa: E501
from openapi_server.models.semantic_stn import SemanticStn  # noqa: E501
from openapi_server.models.sty_tui_stn import StyTuiStn  # noqa: E501
from openapi_server.models.term_resp_obj import TermRespObj  # noqa: E501
from openapi_server.models.termtype_code import TermtypeCode  # noqa: E501
from openapi_server import util
from openapi_server.managers.neo4j_manager import Neo4jManager


neo4jManager = Neo4jManager()


def codes_code_id_codes_get(code_id, sab=None):  # noqa: E501
    """Returns a list of {Concept, Code, Sab} associated with the code_id optionally restricted to SAB

     # noqa: E501

    :param code_id: The code identifier
    :type code_id: str
    :param sab: One or more SABs to search
    :type sab: List[str]

    :rtype: List[CodesCodesObj]
    """
    return neo4jManager.codes_code_id_codes_get(code_id, sab)


def codes_code_id_concepts_get(code_id):  # noqa: E501
    """Returns a list of {Concept, Prefterm} associated with the code_id

     # noqa: E501

    :param code_id: The code identifier
    :type code_id: str

    :rtype: List[ConceptDetail]
    """
    return neo4jManager.codes_code_id_concepts_get(code_id)


def codes_code_id_description_get(code_id):  # noqa: E501
    """Returns a list of {SAB, Code, Term} dictionaries associated with the code_id

     # noqa: E501

    :param code_id: The code identifier
    :type code_id: str

    :rtype: List[SabCodeTerm]
    """
    return neo4jManager.codes_code_id_description_get(code_id)


def codes_code_id_terms_get(code_id, sab=None, tty=None, rel=None):  # noqa: E501
    """Returns a list of TermRespObjs associated with the code_id as follows Code(code_id)&lt;--Concept-[rel.sab]-&gt;Concept--&gt;Code-[Type]-&gt;Term

     # noqa: E501

    :param code_id: The code identifier which is used to identify the initial Concept
    :type code_id: str
    :param sab: Restrict the ConceptI-[rel.sab]-&gt;ConceptR search to Relationships of this Sab
    :type sab: List[str]
    :param tty: Restrict the Code2-[Type]-&gt;Term search to one or more TTY types
    :type tty: List[str]
    :param rel: One or more TTYs to search
    :type rel: List[str]

    :rtype: List[TermRespObj]
    """
    return neo4jManager.codes_code_id_terms_get(code_id, sab, tty, rel)


def concepts_concept_id_codes_get(concept_id, sab=None):  # noqa: E501
    """Returns a distinct list of codes associated with the concept_id

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str
    :param sab: One or more SABs to search
    :type sab: List[str]

    :rtype: List[str]
    """
    return neo4jManager.concepts_concept_id_codes_get(concept_id, sab)


def concepts_concept_id_concepts_get(concept_id):  # noqa: E501
    """Returns a list of {Sab, Relationship, Concept, Prefterm} dictionaries associated with the concept_id

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[SabRelationshipConceptPrefterm]
    """
    return neo4jManager.concepts_concept_id_concepts_get(concept_id)


def concepts_concept_id_definitions_get(concept_id):  # noqa: E501
    """Returns a list of {Sab, Definition} dictionaries associated with the concept_id

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[SabDefinition]
    """
    return neo4jManager.concepts_concept_id_definitions_get(concept_id)


def concepts_concept_id_semantics_get(concept_id):  # noqa: E501
    """Returns a list of {Sty, Tui, Stn} dictionaries associated with the concept_id

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[StyTuiStn]
    """
    return neo4jManager.concepts_concept_id_semantics_get(concept_id)


def concepts_concept_id_terms_get(concept_id, sab=None, tty=None, rel=None):  # noqa: E501
    """Returns a list of TermRespObjs associated with the concept_id as follows Concept(concept_id)-[rel.sab]-&gt;Concept--&gt;Code-[Type]-&gt;Term

     # noqa: E501

    :param concept_id: The concept identifier which is used to identify the initial Concept
    :type concept_id: str
    :param sab: Restrict the ConceptI-[rel.sab]-&gt;ConceptR search to Relationships of this Sab
    :type sab: List[str]
    :param tty: Restrict the Code2-[Type]-&gt;Term search to one or more TTY types
    :type tty: List[str]
    :param rel: One or more TTYs to search
    :type rel: List[str]

    :rtype: List[TermRespObj]
    """
    return neo4jManager.concepts_concept_id_terms_get(concept_id, sab, tty, rel)


def full_capacity_paremeterized_term_get(term, sab=None, tty=None, semantic=None, contains=None, case=None):  # noqa: E501
    """Returns information associated with the term

     # noqa: E501

    :param term: The term
    :type term: str
    :param sab: One or more SABs to search
    :type sab: List[str]
    :param tty: One or more TTYs to search
    :type tty: List[str]
    :param semantic: One or more semanticss to search
    :type semantic: List[str]
    :param contains: True contains term. False equals term
    :type contains: bool
    :param case: True case sensitive. False case insensitive
    :type case: bool

    :rtype: List[FullCapacityTerm]
    """
    return neo4jManager.full_capacity_paremeterized_term_get(term, sab, tty, semantic, contains, case)


def nodes_node_id_terms_get(node_id, sab=None, tty=None, rel=None):  # noqa: E501
    """Returns a list of TermRespObjs associated with the node_id

     # noqa: E501

    :param node_id: The node (either code, concept, term) identifier which is used to identify the initial Concept
    :type node_id: str
    :param sab: Restrict the ConceptI-[rel.sab]-&gt;ConceptR search to Relationships of this Sab
    :type sab: List[str]
    :param tty: Restrict the Code2-[Type]-&gt;Term search to one or more TTY types
    :type tty: List[str]
    :param rel: One or more TTYs to search
    :type rel: List[str]

    :rtype: List[TermRespObj]
    """
    return neo4jManager.nodes_node_id_terms_get(node_id, sab, tty, rel)


def semantics_semantic_id_semantics_get(semantic_id):  # noqa: E501
    """Returns a list of {queryTUI, querySTN ,semantic, TUI_STN} dictionaries associated with the concept_id

     # noqa: E501

    :param semantic_id: The semantic identifier
    :type semantic_id: str

    :rtype: List[QQST]
    """
    return neo4jManager.semantics_semantic_id_semantics_get(semantic_id)


def terms_term_id_codes_get(term_id):  # noqa: E501
    """Returns a list of {TermType, Code} dictionaries associated with the term_id

     # noqa: E501

    :param term_id: The term identifier
    :type term_id: str

    :rtype: List[TermtypeCode]
    """
    return neo4jManager.terms_term_id_codes_get(term_id)


def terms_term_id_concepts_get(term_id):  # noqa: E501
    """Returns a list of Terms associated with the concept_id

     # noqa: E501

    :param term_id: The term identifier
    :type term_id: str

    :rtype: List[str]
    """
    return neo4jManager.terms_term_id_concepts_get(term_id)


def terms_term_id_concepts_terms_get(term_id):  # noqa: E501
    """Returns a list of {Concept, Term} dictionaries associated with the term_id

     # noqa: E501

    :param term_id: The term identifier
    :type term_id: str

    :rtype: List[ConceptTerm]
    """
    return neo4jManager.terms_term_id_concepts_terms_get(term_id)


def terms_term_id_terms_get(term_id, sab=None, tty=None, rel=None):  # noqa: E501
    """Returns a list of TermRespObjs associated with the term_id

     # noqa: E501

    :param term_id: The term identifier which is used to identify the initial Concept
    :type term_id: str
    :param sab: Restrict the ConceptI-[rel.sab]-&gt;ConceptR search to Relationships of this Sab
    :type sab: List[str]
    :param tty: Restrict the Code2-[Type]-&gt;Term search to one or more TTY types
    :type tty: List[str]
    :param rel: One or more TTYs to search
    :type rel: List[str]

    :rtype: List[TermRespObj]
    """
    return neo4jManager.terms_term_id_terms_get(term_id, sab, tty, rel)


def tui_tui_id_semantics_get(tui_id):  # noqa: E501
    """Returns a list of {semantic, STN} dictionaries associated with the tui_id

     # noqa: E501

    :param tui_id: The TUI identifier
    :type tui_id: str

    :rtype: List[SemanticStn]
    """
    return neo4jManager.tui_tui_id_semantics_get(tui_id)
