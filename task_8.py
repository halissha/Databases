import json
import db

es = db.Factory("settings.json").create_elasticsearch()

db.Filler.fill_elasticsearch(es)

'''
{
  "query": {
    "bool": {
        "should": [
          { "term": { "Langs": "Python" } },
          { "term": { "Langs": "PHP" } }
        ],
        "minimum_should_match": 1
    }
  }
}
'''

query = {
  "bool": {
    "should": [
      { "term": { "Langs": "Python" } },
      { "term": { "Langs": "PHP" } }
    ],
    "minimum_should_match": 1
  }
}

res = es.search(index="student", query=query)

print(res["hits"])