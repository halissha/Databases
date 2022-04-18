import json
import db

es = db.Factory("settings.json").create_elasticsearch()

db.Filler.fill_elasticsearch(es)

'''
{
  "query": {
    "bool" : {
      "must" : { "match_all": {} },
      "filter": {
        "bool": {
          "must_not": [
            { "term": { "Langs": "HTML" } }
          ]    
        }
      }
    }
  }
}
'''

query = {
  "bool" : {
    "must" : { "match_all": {} },
    "filter": {
      "bool": {
        "must_not": [
          { "term": { "Langs": "HTML" } }
        ]    
      }
    }
  }
}

res = es.search(index="student", query=query)

print(res["hits"])