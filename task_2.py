import json
import db

redis = db.Factory("settings.json").create_redis()

db.Filler.fill_redis(redis)

students = []

for group in ["group_1", "group_2", "group_3"]:
  b_students = redis.zrange(group, 0, -1)

  for b_student in b_students:
    students.append(json.loads(b_student.decode()))

students = sorted(students, key=lambda student: student["AgeInDays"], reverse=True)

for i in range(1, 4):
  print(students[i])