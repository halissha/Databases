import json
import db

DBNAME = "db"

mongo = db.Factory("settings.json").create_mongodb()

db.Filler.fill_mongodb(mongo, DBNAME)

db = mongo[DBNAME]

students = db.groups.find({ "Students.Hobbies.DurationInMonths": { "$gt": 36 } }, { "Students.$": 1 })

for student in students:
  print(student)
