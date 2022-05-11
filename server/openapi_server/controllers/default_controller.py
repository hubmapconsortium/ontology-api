import connexion
import six

from openapi_server.models.codes_codes_obj import CodesCodesObj  # noqa: E501
from openapi_server.models.concept_detail import ConceptDetail  # noqa: E501
from openapi_server.models.concept_prefterm import ConceptPrefterm  # noqa: E501
from openapi_server.models.concept_sab_rel import ConceptSabRel  # noqa: E501
from openapi_server.models.concept_sab_rel_depth import ConceptSabRelDepth  # noqa: E501
from openapi_server.models.concept_term import ConceptTerm  # noqa: E501
from openapi_server.models.path_item_concept_relationship_sab_prefterm import PathItemConceptRelationshipSabPrefterm  # noqa: E501
from openapi_server.models.qqst import QQST  # noqa: E501
from openapi_server.models.qconcept_tconcept_sab_rel import QconceptTconceptSabRel  # noqa: E501
from openapi_server.models.sab_definition import SabDefinition  # noqa: E501
from openapi_server.models.sab_relationship_concept_prefterm import SabRelationshipConceptPrefterm  # noqa: E501
from openapi_server.models.semantic_stn import SemanticStn  # noqa: E501
from openapi_server.models.sty_tui_stn import StyTuiStn  # noqa: E501
from openapi_server.models.termtype_code import TermtypeCode  # noqa: E501
from openapi_server import util
from openapi_server.managers.neo4j_manager import Neo4jManager


neo4jManager = Neo4jManager()


def codes_code_id_codes_get(code_id, sab=None):  # noqa: E501
    """Returns a list of code_ids {Concept, Code, SAB} that code the same concept(s) as the code_id, optionally restricted to source (SAB)

     # noqa: E501

    :param code_id: The code identifier
    :type code_id: str
    :param sab: One or more sources (SABs) to return
    :type sab: List[str]

    :rtype: List[CodesCodesObj]
    """
    return neo4jManager.codes_code_id_codes_get(code_id, sab)


def codes_code_id_concepts_get(code_id):  # noqa: E501
    """Returns a list of concepts {Concept, Prefterm} that the code_id codes

     # noqa: E501

    :param code_id: The code identifier
    :type code_id: str

    :rtype: List[ConceptDetail]
    """
    return neo4jManager.codes_code_id_concepts_get(code_id)


def concepts_concept_id_codes_get(concept_id, sab=None):  # noqa: E501
    """Returns a distinct list of code_id(s) that code the concept

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str
    :param sab: One or more sources (SABs) to return
    :type sab: List[str]

    :rtype: List[str]
    """
    return neo4jManager.concepts_concept_id_codes_get(concept_id, sab)


def concepts_concept_id_concepts_get(concept_id):  # noqa: E501
    """Returns a list of concepts {Sab, Relationship, Concept, Prefterm} related to the concept

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[SabRelationshipConceptPrefterm]
    """
    return neo4jManager.concepts_concept_id_concepts_get(concept_id)


def concepts_concept_id_definitions_get(concept_id):  # noqa: E501
    """Returns a list of definitions {Sab, Definition} of the concept

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[SabDefinition]
    """
    return neo4jManager.concepts_concept_id_definitions_get(concept_id)


def concepts_concept_id_semantics_get(concept_id):  # noqa: E501
    """Returns a list of semantic_types {Sty, Tui, Stn} of the concept

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[StyTuiStn]
    """
    return neo4jManager.concepts_concept_id_semantics_get(concept_id)


# https://github.com/OpenAPITools/openapi-generator/issues/6039
def concepts_expand_post():  # noqa: E501
    """concepts_expand_post

     # noqa: E501

    :rtype: List[ConceptPrefterm]
    """
    if connexion.request.is_json:
        concept_sab_rel_depth = ConceptSabRelDepth.from_dict(connexion.request.get_json())  # noqa: E501
    return neo4jManager.concepts_expand_post(concept_sab_rel_depth)


def concepts_path_post():  # noqa: E501
    """Return all paths of the relationship pattern specified within the selected sources

     # noqa: E501

    :rtype: List[PathItemConceptRelationshipSabPrefterm]
    """
    if connexion.request.is_json:
        concept_sab_rel = ConceptSabRel.from_dict(connexion.request.get_json())  # noqa: E501
    return neo4jManager.concepts_path_post(concept_sab_rel)


def concepts_shortestpaths_post():  # noqa: E501
    """Return all paths of the relationship pattern specified within the selected sources

     # noqa: E501

    :rtype: List[PathItemConceptRelationshipSabPrefterm]
    """
    if connexion.request.is_json:
        qconcept_tconcept_sab_rel = QconceptTconceptSabRel.from_dict(connexion.request.get_json())  # noqa: E501
    return neo4jManager.concepts_shortestpaths_post(qconcept_tconcept_sab_rel)


def concepts_trees_post():  # noqa: E501
    """Return all paths of the relationship pattern specified within the selected sources

     # noqa: E501

    :rtype: List[PathItemConceptRelationshipSabPrefterm]
    """
    if connexion.request.is_json:
        concept_sab_rel_depth = ConceptSabRelDepth.from_dict(connexion.request.get_json())  # noqa: E501
    return neo4jManager.concepts_trees_post(concept_sab_rel_depth)


def semantics_semantic_id_semantics_get(semantic_id):  # noqa: E501
    """Returns a list of semantic_types {queryTUI, querySTN ,semantic, TUI_STN} of the semantic type

     # noqa: E501

    :param semantic_id: The semantic identifier
    :type semantic_id: str

    :rtype: List[QQST]
    """
    return neo4jManager.semantics_semantic_id_semantics_get(semantic_id)


def terms_term_id_codes_get(term_id):  # noqa: E501
    """Returns a list of codes {TermType, Code} of the text string

     # noqa: E501

    :param term_id: The term identifier
    :type term_id: str

    :rtype: List[TermtypeCode]
    """
    return neo4jManager.terms_term_id_codes_get(term_id)


def terms_term_id_concepts_get(term_id):  # noqa: E501
    """Returns a list of concepts associated with the text string

     # noqa: E501

    :param term_id: The term identifier
    :type term_id: str

    :rtype: List[str]
    """
    return neo4jManager.terms_term_id_concepts_get(term_id)


def terms_term_id_concepts_terms_get(term_id):  # noqa: E501
    """Returns an expanded list of concept(s) and preferred term(s) {Concept, Term} from an exact text match

     # noqa: E501

    :param term_id: The term identifier
    :type term_id: str

    :rtype: List[ConceptTerm]
    """
    return neo4jManager.terms_term_id_concepts_terms_get(term_id)


def tui_tui_id_semantics_get(tui_id):  # noqa: E501
    """Returns a list of symantic_types {semantic, STN} of the type unique id (tui)

     # noqa: E501

    :param tui_id: The TUI identifier
    :type tui_id: str

    :rtype: List[SemanticStn]
    """
    return neo4jManager.tui_tui_id_semantics_get(tui_id)
