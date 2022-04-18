import json
import db

neo4j = db.Factory("settings.json").create_neo4j()

db.Filler.fill_neo4j(neo4j)

result_group = []

with neo4j.session() as ctx:
  result = ctx.run("MATCH (g:Group) RETURN g AS group")
  groups = [record["group"]["Name"] for record in result]
  
  

  for group in groups:
    n_students = ctx.run("MATCH (s)-[:PARTOF]->(g) "
                         "WHERE g.Name = $gname "
                         "RETURN COUNT(s)", gname=group).single()[0]
    
    n_add_students = ctx.run("MATCH (s)-[:LEARN]->(l:Lesson { Name: \"AdditionalLesson\" }) WITH s "
                             "MATCH (s)-[:PARTOF]->(g) WHERE g.Name = $gname RETURN COUNT(s)", gname=group).single()[0]
    
    if n_add_students * 100 / n_students < 70:
      result_group.append(group)

print(result_group)

