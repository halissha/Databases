import json
import redis
import pymongo
import elasticsearch
import neo4j
import random

class Factory():
  def __init__(self, file_settings):
    with open(file_settings, 'r') as file:
      self.settings = json.load(file)
  
  def get_host_and_port(self, db):
    s = self.settings[db]
    return s["host"], s["port"]
  
  def create_redis(self):
    return redis.Redis(*self.get_host_and_port("redis"))
  
  def create_mongodb(self):
    return pymongo.MongoClient(*self.get_host_and_port("mongodb"))
  
  def create_elasticsearch(self):
    host, port = self.get_host_and_port("elasticsearch")
    return elasticsearch.Elasticsearch(host=host, port=port)
  
  def create_neo4j(self):
    host, port = self.get_host_and_port("neo4j")
    s = self.settings["neo4j"]
    login, passw = s["login"], s["passw"]
    return neo4j.GraphDatabase.driver("bolt://{0}:{1}".format(host, port), auth=(login, passw))



class Filler():
  def get_point_in_interval(interval_begin, interval_end, points_in_interval):
    interval = random.randint(interval_begin, interval_end)
    extra_points = random.randint(0, points_in_interval - 1)
    return interval * points_in_interval + extra_points

  @staticmethod
  def fill_redis(redis_client):
    redis_client.flushdb()
    
    for group_id in range(1, 4):
      group = "group_{0}".format(group_id)

      score = 1
      for student_id in range(1, random.randint(20, 30)):
        student = {
          "Surname": "Surname_{0}_{1}".format(group_id, student_id),
          "Name": "Name_{0}_{1}".format(group_id, student_id),

          # intreval_begin - min age in years
          # interval_end - max age in years
          # points_in_interval - days in year
          "AgeInDays": Filler.get_point_in_interval(interval_begin=16, interval_end=25, points_in_interval=365)
        }

        redis_client.zadd(group, { json.dumps(student): score })
        score = score + 1
  
  @staticmethod
  def fill_mongodb(mongodb_client, dbname):
    mongodb_client.drop_database(dbname)

    db = mongodb_client[dbname]

    for group_id in range(1, 4):
      group = {
        "Name": "Group_{0}".format(group_id),
        "Students": []
      }

      for student_id in range(1, random.randint(20, 30)):
        student = {
          "Surname": "Surname_{0}_{1}".format(group_id, student_id),
          "Name": "Name_{0}_{1}".format(group_id, student_id),
          "Hobbies": []
        }

        for hobby_id in range(1, random.randint(2, 5)):
          hobby = {
            "Name": "Hobby_{0}".format(hobby_id),
            # intreval_begin - min durtation in years
            # interval_end - max durtation in years
            # points_in_interval - months in year
            "DurationInMonths": Filler.get_point_in_interval(interval_begin=0, interval_end=4, points_in_interval=12)
          }
          student["Hobbies"].append(hobby)
        
        if (random.randint(0, 3) == 2):
          hobby = {
            "Name": "Hobby_5",
            "DurationInMonths": 1
          }
          student["Hobbies"].append(hobby)

        group["Students"].append(student)
          
      db.groups.insert_one(group)

  @staticmethod
  def fill_elasticsearch(es_client):
    if es_client.indices.exists(index="group"):
      es_client.indices.delete(index="group")
    
    if es_client.indices.exists(index="student"):
      es_client.indices.delete(index="student")
    
    es_client.indices.create(index="group")
    es_client.indices.create(index="student")

    group_mapping = {
      "properties": {
        "GroupName": { "type": "keyword" },
      }
    }

    student_mapping = {
      "properties": {
        "Surname": { "type": "keyword" },
        "Name": { "type": "keyword" },
        "Langs": { "type": "keyword" }
      }
    }

    es_client.indices.put_mapping(index="group", doc_type="_doc", body=group_mapping)
    es_client.indices.put_mapping(index="student", doc_type="_doc", body=student_mapping)

    LANGS = ["C#", "HTML", "Python", "PHP", ".NET", "JAVA"]

    for group_id in range(1, 4):
      group = { "GroupName": "Group_{0}".format(group_id) }
      es_client.index(index="group", id=group_id, document=group)

      for student_id in range(1, random.randint(20, 30)):
        student = {
          "Surname": "Surname_{0}_{1}".format(group_id, student_id),
          "Name": "Name_{0}_{1}".format(group_id, student_id),
          "Langs": random.sample(LANGS, random.randint(0, 3)),
          "GroupId": group_id
        }
        es_client.index(index="student", document=student)
  
  @staticmethod
  def fill_neo4j(neo4j_client):
    # clear database
    with neo4j_client.session() as ctx:
      ctx.run("MATCH (s)-[r1:LEARN]->(l) DELETE r1")
      ctx.run("MATCH (s)-[r2:PARTOF]->(g) DELETE r2")
      ctx.run("MATCH (l:Lesson) DELETE l")
      ctx.run("MATCH (g:Group) DELETE g")
      ctx.run("MATCH (s:Student) DELETE s")
    
    with neo4j_client.session() as ctx:
      for lesson_id in range(1, 7):
        lesson_name = "Lesson_{0}".format(lesson_id)
        ctx.run("CREATE (l:Lesson { Name: '" + lesson_name + "' })")  

      l_id = ctx.run("CREATE (l:Lesson { Name: 'AdditionalLesson' }) RETURN id(l)").single()[0] 

      for group_id in range(1, 4):
        group_name = "Group_{0}".format(group_id)

        g_id = ctx.run("CREATE (g:Group { Name: '" + group_name + "' }) "
                       "RETURN id(g)").single()[0]

        for student_id in range(1, random.randint(20, 30)):
          s_surname = "Surname_{0}_{1}".format(group_id, student_id)
          s_name = "Name_{0}_{1}".format(group_id, student_id)

          s_id = ctx.run("CREATE (s:Student { Surname: '" + s_surname + "', Name: '" + s_name + "' }) "
                         "RETURN id(s)").single()[0]

          ctx.run("MATCH (s:Student) WHERE id(s) = $sid "
                  "MATCH (g:Group) WHERE id(g) = $gid "
                  "CREATE (s)-[:PARTOF]->(g)", sid=s_id, gid=g_id)
          
          ctx.run("MATCH (s:Student) WHERE id(s) = $sid "
                  "MATCH (l:Lesson) WHERE id(l) <> $lid "
                  "CREATE (s)-[:LEARN]->(l)", sid=s_id, lid=l_id)

          if random.randint(0, 10) <= 3:
            ctx.run("MATCH (s:Student) WHERE id(s) = $sid "
                    "MATCH (l:Lesson) WHERE id(l) = $lid "
                    "CREATE (s)-[:LEARN]->(l)", sid=s_id, lid=l_id)

      
      




    

