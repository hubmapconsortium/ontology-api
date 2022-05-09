import neo4j
import configparser
from typing import List
import re

from openapi_server.models.codes_codes_obj import CodesCodesObj  # noqa: E501
from openapi_server.models.concept_detail import ConceptDetail  # noqa: E501
from openapi_server.models.concept_term import ConceptTerm  # noqa: E501
from openapi_server.models.qqst import QQST  # noqa: E501
from openapi_server.models.sab_definition import SabDefinition  # noqa: E501
from openapi_server.models.sab_relationship_concept_prefterm import SabRelationshipConceptPrefterm  # noqa: E501
from openapi_server.models.semantic_stn import SemanticStn  # noqa: E501
from openapi_server.models.sty_tui_stn import StyTuiStn  # noqa: E501
from openapi_server.models.termtype_code import TermtypeCode  # noqa: E501

cypher_tail: str = \
    " CALL apoc.when(rel = []," \
    "  'RETURN concept AS related_concept, NULL AS rel_type, NULL AS rel_sab'," \
    "  'MATCH (concept)-[matched_rel]->(related_concept)" \
    "   WHERE any(x IN rel WHERE x IN [[Type(matched_rel),matched_rel.SAB],[Type(matched_rel),\"*\"],[\"*\",matched_rel.SAB],[\"*\",\"*\"]])" \
    "   RETURN related_concept, Type(matched_rel) AS rel_type, matched_rel.SAB AS rel_sab'," \
    "  {concept:concept,rel:rel})" \
    " YIELD value" \
    " WITH matched, value.related_concept AS related_concept, value.rel_type AS rel_type, value.rel_sab AS rel_sab" \
    " MATCH (code:Code)<-[:CODE]-(related_concept:Concept)-[:PREF_TERM]->(prefterm:Term)" \
    " WHERE (code.SAB IN $sab OR $sab = [])" \
    " OPTIONAL MATCH (code:Code)-[code2term]->(term:Term)" \
    " WHERE (code2term.CUI = related_concept.CUI) AND (Type(code2term) IN $tty OR $tty = [])" \
    " WITH *" \
    " CALL apoc.when(term IS NULL," \
    "  'RETURN \"PREF_TERM\" AS tty, prefterm as term'," \
    "  'RETURN Type(code2term) AS tty, term'," \
    "  {term:term,prefterm:prefterm,code2term:code2term})" \
    " YIELD value" \
    " WITH *, value.tty AS tty, value.term AS term" \
    " RETURN DISTINCT matched, rel_type, rel_sab, code.CodeID AS code_id, code.SAB AS code_sab," \
    "  code.CODE AS code_code, tty, term.name AS term, related_concept.CUI AS concept" \
    " ORDER BY size(term), code_id, tty DESC, rel_type, rel_sab, concept, matched"

cypher_head: str = \
    "CALL db.index.fulltext.queryNodes(\"Term_name\", '\\\"'+$queryx+'\\\"')" \
     " YIELD node" \
     " WITH node AS matched_term" \
     " MATCH (matched_term)" \
     " WHERE size(matched_term.name) = size($queryx)" \
     " WITH matched_term" \
     " OPTIONAL MATCH (matched_term:Term)<-[relationship]-(:Code)<-[:CODE]-(concept:Concept)" \
     " WHERE relationship.CUI = concept.CUI" \
     " OPTIONAL MATCH (matched_term:Term)<-[:PREF_TERM]-(concept:Concept)"


def rel_str_to_array(rels: List[str]) -> List[List]:
    rel_array: List[List] = []
    for rel in rels:
        m = re.match(r'([^[]+)\[([^]]+)\]', rel)
        rel = m[1]
        sab = m[2]
        rel_array.append([rel, sab])
    return rel_array


# Each 'rel' list item is a string of the form 'Type[SAB]' which is translated into the array '[Type(t),t.SAB]'
# The Type or SAB can be a wild card '*', so '*[SAB]', 'Type[*]', 'Type[SAB]' and even '*[*]' are valid
def parse_and_check_rel(rel: List[str]) -> List[List]:
    try:
        rel_list: List[List] = rel_str_to_array(rel)
    except TypeError:
        raise Exception(f"The rel optional parameter must be of the form 'Type[SAB]', 'Type[*]', '*[SAB], or '*[*]'", 400)
    for r in rel_list:
        if not re.match(r"\*|[a-zA-Z_]+", r[0]):
            raise Exception(f"Invalid Type in rel optional parameter list", 400)
        if not re.match(r"\*|[a-zA-Z_]+", r[1]):
            raise Exception(f"Invalid SAB in rel optional parameter list", 400)
    return rel_list


# https://editor.swagger.io/
class Neo4jManager(object):

    def __init__(self):
        config = configparser.ConfigParser()
        # [neo4j]
        # Server = bolt://localhost: 7687
        # Username = neo4j
        # Password = password
        config.read('openapi_server/resources/app.properties')
        neo4j_config = config['neo4j']
        server = neo4j_config.get('Server')
        username = neo4j_config.get('Username')
        password = neo4j_config.get('Password')
        self.driver = neo4j.GraphDatabase.driver(server, auth=(username, password))

    # https://neo4j.com/docs/api/python-driver/current/api.html
    def close(self):
        self.driver.close()

    def codes_code_id_codes_get(self, code_id: str, sab: List[str]) -> List[CodesCodesObj]:
        codesCodesObjs: List[CodesCodesObj] = []
        query = 'WITH [$code_id] AS query' \
                ' MATCH (a:Code)<-[:CODE]-(b:Concept)-[:CODE]->(c:Code)' \
                ' WHERE a.CodeID IN query AND (c.SAB IN $SAB OR $SAB = [])' \
                ' RETURN DISTINCT a.CodeID AS Code1, b.CUI as Concept, c.CodeID AS Code2, c.SAB AS Sab2' \
                ' ORDER BY Code1, Concept ASC, Code2, Sab2'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, code_id=code_id, SAB=sab)
            for record in recds:
                try:
                    codesCodesObj: CodesCodesObj =\
                        CodesCodesObj(record.get('Concept'), record.get('Code2'), record.get('Sab2'))
                    codesCodesObjs.append(codesCodesObj)
                except KeyError:
                    pass
        return codesCodesObjs

    def codes_code_id_concepts_get(self, code_id: str) -> List[ConceptDetail]:
        conceptDetails: List[ConceptDetail] = []
        query = 'WITH [$code_id] AS query' \
                ' MATCH (a:Code)<-[:CODE]-(b:Concept)' \
                ' WHERE a.CodeID IN query' \
                ' OPTIONAL MATCH (b)-[:PREF_TERM]->(c:Term)' \
                ' RETURN DISTINCT a.CodeID AS Code, b.CUI AS Concept, c.name as Prefterm' \
                ' ORDER BY Code ASC, Concept'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, code_id=code_id)
            for record in recds:
                try:
                    conceptDetail: ConceptDetail = ConceptDetail(record.get('Concept'), record.get('Prefterm'))
                    conceptDetails.append(conceptDetail)
                except KeyError:
                    pass
        return conceptDetails

    # https://neo4j.com/docs/api/python-driver/current/api.html#explicit-transactions
    def concepts_concept_id_codes_get(self, concept_id: str, sab: List[str]) -> List[str]:
        codes: List[str] = []
        query = 'WITH [$concept_id] AS query' \
                ' MATCH (a:Concept)-[:CODE]->(b:Code)' \
                ' WHERE a.CUI IN query AND (b.SAB IN $SAB OR $SAB = [])' \
                ' RETURN DISTINCT a.CUI AS Concept, b.CodeID AS Code, b.SAB AS Sab' \
                ' ORDER BY Concept, Code ASC'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, concept_id=concept_id, SAB=sab)
            for record in recds:
                try:
                    code = record.get('Code')
                    codes.append(code)
                except KeyError:
                    pass
        return codes

    def concepts_concept_id_concepts_get(self, concept_id: str) -> List[SabRelationshipConceptPrefterm]:
        sabRelationshipConceptPrefterms: [SabRelationshipConceptPrefterm] = []
        query = 'WITH [$concept_id] AS query' \
                ' MATCH (b:Concept)<-[c]-(d:Concept)' \
                ' WHERE b.CUI IN query' \
                ' OPTIONAL MATCH (b)-[:PREF_TERM]->(a:Term)' \
                ' OPTIONAL MATCH (d)-[:PREF_TERM]->(e:Term)' \
                ' RETURN DISTINCT a.name AS Prefterm1, b.CUI AS Concept1, c.SAB AS SAB, type(c) AS Relationship,' \
                '  d.CUI AS Concept2, e.name AS Prefterm2' \
                ' ORDER BY Concept1, Relationship, Concept2 ASC, Prefterm1, Prefterm2'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, concept_id=concept_id)
            for record in recds:
                try:
                    sabRelationshipConceptPrefterm: SabRelationshipConceptPrefterm =\
                        SabRelationshipConceptPrefterm(record.get('SAB'), record.get('Relationship'),
                                                       record.get('Concept2'), record.get('Prefterm2'))
                    sabRelationshipConceptPrefterms.append(sabRelationshipConceptPrefterm)
                except KeyError:
                    pass
        return sabRelationshipConceptPrefterms

    def concepts_concept_id_definitions_get(self, concept_id: str) -> List[SabDefinition]:
        sabDefinitions: [SabDefinition] = []
        query = 'WITH [$concept_id] AS query' \
                ' MATCH (a:Concept)-[:DEF]->(b:Definition)' \
                ' WHERE a.CUI in query' \
                ' RETURN DISTINCT a.CUI AS Concept, b.SAB AS SAB, b.DEF AS Definition' \
                ' ORDER BY Concept, SAB'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, concept_id=concept_id)
            for record in recds:
                try:
                    sabDefinition: SabDefinition = SabDefinition(record.get('SAB'), record.get('Definition'))
                    sabDefinitions.append(sabDefinition)
                except KeyError:
                    pass
        return sabDefinitions

    def concepts_concept_id_semantics_get(self, concept_id) -> List[StyTuiStn]:
        styTuiStns: [StyTuiStn] = []
        query = 'WITH [$concept_id] AS query' \
                ' MATCH (a:Concept)-[:STY]->(b:Semantic)' \
                ' WHERE a.CUI IN query' \
                ' RETURN DISTINCT a.CUI AS concept, b.name AS STY, b.TUI AS TUI, b.STN as STN'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, concept_id=concept_id)
            for record in recds:
                try:
                    styTuiStn: StyTuiStn = StyTuiStn(record.get('STY'), record.get('TUI'), record.get('STN'))
                    styTuiStns.append(styTuiStn)
                except KeyError:
                    pass
        return styTuiStns

    def semantics_semantic_id_semantics_get(self, semantic_id: str) -> List[QQST]:
        qqsts: [QQST] = []
        query = 'WITH [$semantic_id] AS query' \
                ' MATCH (a:Semantic)-[:ISA_STY]->(b:Semantic)' \
                ' WHERE (a.name IN query OR query = [])' \
                ' RETURN DISTINCT a.name AS querySemantic, a.TUI as queryTUI, a.STN as querySTN, b.name AS semantic,' \
                '  b.TUI AS TUI, b.STN as STN'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, semantic_id=semantic_id)
            for record in recds:
                try:
                    qqst: QQST = QQST(record.get('queryTUI'), record.get('querySTN'), record.get('semantic'), record.get('TUI'), record.get('STN'))
                    qqsts.append(qqst)
                except KeyError:
                    pass
        return qqsts

    def terms_term_id_codes_get(self, term_id: str) -> List[TermtypeCode]:
        termtypeCodes: [TermtypeCode] = []
        query = 'WITH [$term_id] AS query' \
                ' MATCH (a:Term)<-[b]-(c:Code)' \
                ' WHERE a.name IN query' \
                ' RETURN DISTINCT a.name AS Term, Type(b) AS TermType, c.CodeID AS Code' \
                ' ORDER BY Term, TermType, Code'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, term_id=term_id)
            for record in recds:
                try:
                    termtypeCode: TermtypeCode = TermtypeCode(record.get('TermType'), record.get('Code'))
                    termtypeCodes.append(termtypeCode)
                except KeyError:
                    pass
        return termtypeCodes

    def terms_term_id_concepts_get(self, term_id: str) -> List[str]:
        concepts: [str] = []
        query = 'WITH [$term_id] AS query' \
                ' OPTIONAL MATCH (a:Term)<-[b]-(c:Code)<-[:CODE]-(d:Concept)' \
                ' WHERE a.name IN query AND b.CUI = d.CUI' \
                ' OPTIONAL MATCH (a:Term)<--(d:Concept) WHERE a.name IN query' \
                ' RETURN DISTINCT a.name AS Term, d.CUI AS Concept' \
                ' ORDER BY Concept ASC'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, term_id=term_id)
            for record in recds:
                try:
                    concept: str = record.get('Concept')
                    concepts.append(concept)
                except KeyError:
                    pass
        return concepts

    def terms_term_id_concepts_terms_get(self, term_id: str) -> List[ConceptTerm]:
        conceptTerms: [ConceptTerm] = []
        query = 'WITH [$term_id] AS query' \
                ' OPTIONAL MATCH (a:Term)<-[b]-(c:Code)<-[:CODE]-(d:Concept)' \
                ' WHERE a.name IN query AND b.CUI = d.CUI' \
                ' OPTIONAL MATCH (a:Term)<--(d:Concept)' \
                ' WHERE a.name IN query WITH a,collect(d.CUI) AS next' \
                ' MATCH (f:Term)<-[:PREF_TERM]-(g:Concept)-[:CODE]->(h:Code)-[i]->(j:Term)' \
                ' WHERE g.CUI IN next AND g.CUI = i.CUI' \
                ' WITH a, g,COLLECT(j.name)+[f.name] AS x' \
                ' WITH * UNWIND(x) AS Term2' \
                ' RETURN DISTINCT a.name AS Term1, g.CUI AS Concept, Term2' \
                ' ORDER BY Term1, Term2'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, term_id=term_id)
            for record in recds:
                try:
                    conceptTerm: ConceptTerm = ConceptTerm(record.get('Concept'), record.get('Term2'))
                    conceptTerms.append(conceptTerm)
                except KeyError:
                    pass
        return conceptTerms

    def tui_tui_id_semantics_get(self, tui_id: str) -> List[SemanticStn]:
        semanticStns: [SemanticStn] = []
        query = 'WITH [$tui_id] AS query' \
                ' MATCH (a:Semantic)' \
                ' WHERE (a.TUI IN query OR query = [])' \
                ' RETURN DISTINCT a.name AS semantic, a.TUI AS TUI, a.STN AS STN1'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, tui_id=tui_id)
            for record in recds:
                try:
                    semanticStn: SemanticStn = SemanticStn(record.get('semantic'), record.get('STN1'))
                    semanticStns.append(semanticStn)
                except KeyError:
                    pass
        return semanticStns
