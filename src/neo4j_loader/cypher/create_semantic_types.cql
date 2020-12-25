MATCH (a:Concept)-[:CODE]->(:Code)<-[:CODE]-(:Concept)-[:STY]->(b:Semantic)
WHERE SIZE((a)-[:STY]->(:Semantic)) = 0
MERGE (a)-[:STY]->(b);

MATCH (a:Code)<--(b:Concept) WHERE 
a.SAB IN ['UBERON','CL','CCF'] AND SIZE((b)-->(:Semantic)) = 0
CALL { WITH b
MATCH p=((b)-[:subclass_of*1..4]->(c:Concept)-->(d:Semantic)) 
RETURN LENGTH(p), d.STN, b AS Cncpt, d AS Smntc ORDER BY LENGTH(p), d.STN DESCENDING LIMIT 1 }
CREATE (Cncpt)-[:STY]->(Smntc);

MATCH (a:Code)<--(b:Concept) WHERE 
a.SAB IN ['UBERON','CL','CCF'] AND SIZE((b)-->(:Semantic)) = 0
CALL { WITH b
MATCH p=((b)-[:subclass_of|part_of*1..2]-(c:Concept)-->(d:Semantic)) 
RETURN LENGTH(p), d.STN, b AS Cncpt, d AS Smntc ORDER BY LENGTH(p), d.STN DESCENDING LIMIT 1 }
CREATE (Cncpt)-[:STY]->(Smntc);
