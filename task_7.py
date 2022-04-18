import json
import db

es = db.Factory("settings.json").create_elasticsearch()

db.Filler.fill_elasticsearch(es)

'''
{
  "query": {
    "bool": {
      "must": [
        { "match": { "Langs": "HTML"} },
        { "match": { "Langs": "C#"} }
      ]
    }
  }
}
'''

query = {
  "bool": {
    "must": [
      { "match": { "Langs": "C#" } },
      { "match": { "Langs": "HTML" } }
    ]
  }
}

res = es.search(index="student", query=query)

print(res["hits"])