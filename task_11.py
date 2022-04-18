import json
import db

es = db.Factory("settings.json").create_elasticsearch()

db.Filler.fill_elasticsearch(es)

'''
{
  "query": {
    "constant_score" : {
      "filter" : {
        "exists" : {
          "field" : "Langs"
        }
      }
    }
  }
}
'''

query = {
  "constant_score" : {
    "filter" : {
      "exists" : {
        "field" : "Langs"
      }
    }
  }
}

res = es.search(index="student", query=query)

print(res["hits"])