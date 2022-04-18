import json
import db

neo4j = db.Factory("settings.json").create_neo4j()

db.Filler.fill_neo4j(neo4j)

result_group = []

with neo4j.session() as ctx:

  for group in groups:
    n_students = ctx.run("MATCH (s)-[:LEARN]->(l) "
                         "WHERE l.Name ", gname=group).single()[0]
    
    if n_students == 0:
      result_group.append(group)

print(result_group)

