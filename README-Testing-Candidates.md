#  Testing Candidates

The following are a set of match [Cypher queries](https://neo4j.com/developer/cypher/) as candidates for testing the .owl to .csv generation fround in the './scripts' directory after loading them into a Neo4J database using [neof4-admin import](https://neo4j.com/docs/operations-manual/current/tutorial/neo4j-admin-import/). This is done in the Docker file in the './neo4j' directory in this project to build the database.

They may or may not be useful at some point. These are a set of notes, some of which will be codified into a set of tests to be run on the database.

## Checking for zero pref-terms
To see if not equal 1 is zero or more than 1. If there are none of those then it's a duplication problem which is less serious in a sense than a missing pref-term problem - either way, need to make a tiny adjustment to catch some duplication or catch some missing labels in node_metadata. Should not be a big deal, but will have to address.

```buildoutcfg
MATCH (a:Concept) WHERE size((a)-[:PREF_TERM]->(:Term))=0 RETURN COUNT(a)
```

## Substituting each new SAB being introduced

For CL the match isn’t perfect but it's perfect match for UBERON and PATO (possibly an issue with missing node_label).

```buildoutcfg
MATCH p=((a:Concept)-->(b:Code{SAB:“CL”})-[c:PT]->(:Term)) WHERE a.CUI = c.CUI RETURN COUNT(p),COUNT(DISTINCT b)
```

## Count total Codes in an SAB

The results should all match up with the three counts similar - they do for SNOMEDCT_US (which is pure UMLS) but they don’t precisely for UBERON, CL, or PATO so again they amount to the sum total of those in node_metadata without Labels.

Have to decide what to do about that - one approach is to recognize we’re taking as much information as we’re given so we build anyway even if no Labels whereas the other approach is to not allow an addition to the graph unless it has a Label.

```buildoutcfg
MATCH (a:Code{SAB:“CL”}) RETURN Count(a)
```