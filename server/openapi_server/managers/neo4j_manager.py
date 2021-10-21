import neo4j
import configparser
from typing import List
import re

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


def rel_str_to_array(rels: List[str]) -> List[List]:
    rel_array: List[List] = []
    for rel in rels:
        m = re.match(r'([^[]+)\[([^]]+)\]', rel)
        rel = m[1]
        sab = m[2]
        rel_array.append([rel, sab])
    return rel_array


# Each 'rel' list item is a string of the form 'Type[SAB]' which is translated into the array '[Type(t),t.SAB]'
def parse_and_check_rel(rel: List[str]) -> List[List]:
    rel_list: List[List] = rel_str_to_array(rel)
    for r in rel_list:
        if not re.match(r"\*|[a-zA-Z_]+", r[0]):
            raise Exception(f"Invalid relation in rel optional parameter list", 400)
        if not re.match(r"[a-zA-Z_]+", r[1]):
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

    def codes_code_id_codes_get(self, code_id: str, sab: List[str])\
            -> List[CodesCodesObj]:
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
                ' MATCH (a:Code)<-[:CODE]-(b:Concept)-[:PREF_TERM]->(c:Term)' \
                ' WHERE a.CodeID IN query' \
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

    def codes_code_id_description_get(self, code_id: str) -> List[SabCodeTerm]:
        sabCodeTerms: List[SabCodeTerm] = []
        query = 'WITH [$code_id] as query' \
                ' MATCH (c:Code)<--(e:Concept)' \
                ' WHERE c.CodeID = query' \
                '  WITH c, e' \
                '  MATCH p = ((e:Concept)<-[:isa|CHD|subclass_of|part_of*0..5]-(l:Concept))' \
                ' WHERE ALL (y IN relationships(p)' \
                ' WHERE y.SAB = c.SAB) ' \
                '  WITH c, l ' \
                '  MATCH (n:Code)<--(l:Concept)-[:PREF_TERM]->(v:Term)' \
                ' WHERE n.SAB = c.SAB' \
                ' RETURN DISTINCT n.SAB AS SAB, n.CODE as code, v.name as term' \
                ' ORDER BY SAB, code, size(term)'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, code_id=code_id)
            for record in recds:
                try:
                    sabCodeTerm: SabCodeTerm = SabCodeTerm(record.get('SAB'), record.get('code'), record.get('term'))
                    sabCodeTerms.append(sabCodeTerm)
                except KeyError:
                    pass
        return sabCodeTerms

    def codes_code_id_terms_get(self, code_id: str, sab: List[str], tty: List[str], rel: List[List]) -> List[TermRespObj]:
        print(f"Original; code_id: '{code_id}'; sab: {sab}; tty: {tty}; rel: {rel}")
        try:
            rel = parse_and_check_rel(rel)
        except Exception as e:
            msg, code = e.args
            return msg, code
        termRespObjs: List[TermRespObj] = []
        query = "WITH $code_id AS code_id" \
                " MATCH (:Code{CodeID:code_id})<-[:CODE]-(c:Concept)" \
                " WITH c, $rel AS rel" \
                " CALL apoc.when($rel = []," \
                "  'MATCH (c)" \
                "    RETURN c AS d, NULL AS rel_type, NULL AS rel_sab'," \
                "  'MATCH (c)-[t]->(d)" \
                "    WHERE [Type(t),t.SAB] IN rel OR [Type(t),\"*\"] IN rel OR [\"*\",t.SAB] IN rel" \
                "    RETURN d, Type(t) AS rel_type, t.SAB AS rel_sab'," \
                "  {c:c,rel:rel}" \
                ")" \
                " YIELD value" \
                " WITH value.d AS d, value.rel_type AS rel_type, value.rel_sab AS rel_sab" \
                " OPTIONAL MATCH (d:Concept)-[:PREF_TERM]->(e:Term)" \
                " OPTIONAL MATCH (d:Concept)-[:CODE]->(f:Code)-[s]->(g:Term)" \
                " WHERE s.CUI = d.CUI AND (f.SAB IN $sab OR $sab = []) AND (Type(s) IN $tty OR $tty = [])" \
                " RETURN DISTINCT $code_id AS code_id, rel_type, rel_sab, f.CodeID AS code2_id, f.SAB AS code2_sab," \
                "  f.CODE AS code2_code, Type(s) AS tty, g.name AS term, d.CUI AS concept, e.name AS prefterm"
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, code_id=code_id, sab=sab, tty=tty, rel=rel)
            for record in recds:
                try:
                    termRespObj: TermRespObj =\
                        TermRespObj(record.get('code2_id'), record.get('code2_sab'), record.get('code2_code'),
                                    record.get('concept'), record.get('tty'), record.get('term'), record.get('perfterm'),
                                    record.get('rel_type'), record.get('rel_sab'))
                    termRespObjs.append(termRespObj)
                except KeyError:
                    pass
        return termRespObjs

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
                ' MATCH (a:Term)<-[:PREF_TERM]-(b:Concept)-[c]-(d:Concept)-[:PREF_TERM]->(e:Term)' \
                ' WHERE b.CUI IN query' \
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

    def concepts_concept_id_terms_get(self, concept_id: str) -> List[str]:
        concepts: [str] = []
        query = 'WITH [$concept_id] AS query' \
                ' MATCH (a:Term)<-[:PREF_TERM]-(b:Concept)-[:CODE]->(c:Code)-[d]->(e:Term)' \
                ' WHERE b.CUI IN query AND b.CUI = d.CUI' \
                ' WITH b,COLLECT(e.name)+[a.name] AS x' \
                ' WITH * UNWIND(x) AS Term' \
                ' RETURN DISTINCT b.CUI AS Concept, Term' \
                ' ORDER BY Term ASC'
        with self.driver.session() as session:
            recds: neo4j.Result = session.run(query, concept_id=concept_id)
            for record in recds:
                try:
                    concept: str = record.get('Term')
                    concepts.append(concept)
                except KeyError:
                    pass
        return concepts

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

    def full_capacity_paremeterized_term_get(self, term: str, sab: List[str], tty: List[str], semantic: List[str], contains: bool, case: bool)\
            -> List[FullCapacityTerm]:
        print(f"term: '{term}'; sab: {sab}; tty: {tty}; semantic: {semantic}; contains: {contains}; case: {case}")
        fullCapacityTerms: List[FullCapacityTerm] = []
        query = "WITH $term AS query" \
                "  CALL apoc.when($CASE = 'true'," \
                "    'MATCH (node:Term) WHERE node.name CONTAINS query RETURN node'," \
                "    'CALL db.index.fulltext.queryNodes(\"Term_name\", \"\"+query+\"\") YIELD node RETURN node'," \
                "    {query:query})" \
                "  YIELD value" \
                "  WITH query, value.node AS node" \
                "  MATCH (node)" \
                "    CALL apoc.when($CONTAINS = 'true'," \
                "      'WHERE toLower(node.name) CONTAINS toLower(query) RETURN node'," \
                "      'WHERE toLower(node.name) = toLower(query) RETURN node'," \
                "      {query:query, node:node})" \
                "    YIELD value" \
                "  WITH node" \
                "  OPTIONAL MATCH (node)<-[r]-(:Code)<-[:CODE]-(d:Concept)" \
                "  WHERE r.CUI = d.CUI" \
                "    OPTIONAL MATCH (node)<-[:PREF_TERM]-(d:Concept)" \
                "    WITH d" \
                "    MATCH (d:Concept)-[:PREF_TERM]->(e:Term)," \
                "          (f:Semantic)<-[:STY]-(d:Concept)-[:CODE]->(a:Code)-[s]->(b:Term)" \
                "    WHERE s.CUI = d.CUI AND" \
                "          (a.SAB IN $SAB OR $SAB = []) AND" \
                "          (Type(s) IN $TTY OR $TTY = []) AND" \
                "          (f.name IN $semantic OR $semantic = [])" \
                "  RETURN DISTINCT b.name as term, Type(s) as TTY, a.CodeID AS code, " \
                "                  d.CUI AS concept, e.name AS prefterm, f.name AS semantic"
        with self.driver.session() as session:
            recds: neo4j.Result =\
                session.run(query, term=term, SAB=sab, TTY=tty, semantic=semantic, CONTAINS=contains, CASE=case)
            for record in recds:
                try:
                    fullCapacityTerm: FullCapacityTerm =\
                        FullCapacityTerm(record.get('term'), record.get('TTY'), record.get('code'), record.get('concept'),
                                         record.get('prefterm'), record.get('semantic'))
                    fullCapacityTerms.append(fullCapacityTerm)
                except KeyError:
                    pass
        return fullCapacityTerms
