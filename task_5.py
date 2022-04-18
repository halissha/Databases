import json
import db

def flatten(t):
  return [item for sublist in t for item in sublist]

def less_than_three_hobbies(student):
  return len(student["Hobbies"]) < 3

DBNAME = "db"

mongo = db.Factory("settings.json").create_mongodb()

db.Filler.fill_mongodb(mongo, DBNAME)

db = mongo[DBNAME]

groups = db.groups.find()

students = flatten([group["Students"] for group in groups])

students = [student for student in students if less_than_three_hobbies(student)]

for student in students:
  print(student)

