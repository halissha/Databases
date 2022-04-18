import json
import db

def flatten(t):
  return [item for sublist in t for item in sublist]

def two_hobbies_less_than_two_months(student):
  return sum(1 for hobby in student["Hobbies"] if hobby["DurationInMonths"] < 2) == 2

DBNAME = "db"

mongo = db.Factory("settings.json").create_mongodb()

db.Filler.fill_mongodb(mongo, DBNAME)

db = mongo[DBNAME]

groups = db.groups.find()

students = flatten([group["Students"] for group in groups])

students = [student for student in students if two_hobbies_less_than_two_months(student)]

for student in students:
  print(student)

