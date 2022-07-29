from app import API, db
from flask import request, jsonify, make_response
from flask_restful import Resource
from app.models import Student, Department, Section, Instructor, Course, teaches, sec_course
import json


def serialize_single(item):
  print(item)
  item.pop('_sa_instance_state')
  print(item)
  r = json.dumps(item).replace('null', '1')
  r = json.loads(r)
  return jsonify(r) 

def serialize_list(records):
  serialized_list = {}
  i=0
  for record in records:
    item = record.__dict__
    item.pop('_sa_instance_state')
    serialized_list[i] = item
    i += 1
  r = json.dumps(serialized_list).replace('null', '1')
  r = json.loads(r)
  print(r)
  return jsonify(r)

def serialize_list_without_jsonify(records):
  serialized_list = {}
  i=0
  for record in records:
    item = record.__dict__
    print(item)
    if '_sa_instance_state' in item.keys():
      item.pop('_sa_instance_state')
    serialized_list[i] = item
    i += 1
  print(serialized_list)
  return (serialized_list)

class Department_API(Resource):
    def get(self):
      records = Department.query.all()
      print(records)
      if records:
        print(records)
        return serialize_list(records)
      else:
        error_dict = {"message":"department id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response

    def post(self):
      print(request.json)
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)

      name = body['name']
      budget = body['budget']
      building = None
      if not building:
        building = 'Main Building'
      new_department = Department(name=name, dept_budget=budget, building=building)
      dict_copy = new_department.__dict__.copy()
      db.session.add(new_department)
      db.session.commit()
      print(new_department)
      return serialize_single(dict_copy)

class Individual_Department_API(Resource):
    def get(self, id):
      record = Department.query.get(id)
      print(record)
      if record == None:
        error_dict = {"message":"department id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        return serialize_single(record.__dict__)
    
    def put(self, id):
      record = Department.query.get(id)
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)

      if record == None:
        error_dict = {"message":"Department id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        name = body['name']
        budget = body['budget']
        record.name = name
        record.dept_budget = budget
        updated_department_copy = record.__dict__.copy()
        db.session.commit()
        return serialize_single(updated_department_copy)
    
    def delete(self, id):
      record = Department.query.get(id)
      if record == None:
        error_dict = {"message":"Department id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        db.session.delete(record)
        db.session.commit()
        return serialize_single(record.__dict__)

class Student_API(Resource):
    def get(self):
      records = Student.query.all()
      return serialize_list(records)

    def post(self):
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)
      else:
        error_dict = {"message":"invalid response"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      name = body['name']
      credits = body['credits']
      dept_id = body['dept_id']
      sec_id = body['sec_id']
      new_student = Student(student_name=name, dept_id=dept_id, credits=credits, sec_id=sec_id)
      dict_copy = new_student.__dict__.copy()
      db.session.add(new_student)
      db.session.commit()
      return serialize_single(dict_copy)

class Individual_Student_API(Resource):
    def get(self, id):
      record = Student.query.get(id)
      if record == None:
        error_dict = {"message":"student id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        return serialize_single(record.__dict__)
    
    def put(self, id):
      record = Student.query.get(id)
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)
      if record == None:
        error_dict = {"message":"student id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        name = body['name']
        credits = body['credits']
        dept_id = body['dept_id']
        sec_id = body['sec_id']
        record.name = name
        record.credits = credits
        record.dept_id = dept_id
        record.sec_id = sec_id
        updated_student_copy = record.__dict__.copy()
        db.session.commit()
        return serialize_single(updated_student_copy)
    
    def delete(self, id):
      record = Student.query.get(id)
      if record == None:
        error_dict = {"message":"student id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        record_copy = record.__dict__.copy()
        db.session.delete(record)
        db.session.commit()
        return serialize_single(record_copy)

class Section_API(Resource):
    def get(self):
      records = Section.query.all()
      # print(records)
      # print()
      s1 = serialize_list_without_jsonify(records)
      print(s1)
      for i in s1.keys():
        # print(i)
        s1[i]['instructors'] = serialize_list_without_jsonify(s1[i]['instructors'])
      # print(s1)
      return jsonify(s1)

    def post(self):
      print(request.json)
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)
      semester = body['semester']
      year = body['year']
      instructors=[Instructor.query.get(int(i)) for i in body['instructors']]
      new_section = Section(semester=semester, year=year, instructors=instructors)
      # for i in body["instructors"].keys():
      #   a = Instructor.query.get(int(i))
      #   new_section.instructors.append(a)
      print(new_section.__dict__)
      db.session.add(new_section)
      db.session.commit()
      return jsonify({"message":"Success!"})

class Individual_Section_API(Resource):
    def get(self, id):
      record = Section.query.get(id)
      if record == None:
        error_dict = {"message":"instructor id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        r = []
        r.append(record)
        s1 = serialize_list_without_jsonify(r)
        s1[0]['instructors'] = serialize_list_without_jsonify(s1[0]['instructors'])
        print(s1)
        return jsonify(s1)
    
    def put(self, id):
      record = Section.query.get(id)
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)

      if record == None:
        error_dict = {"message":"Instructor id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        semester = body['semester']
        year = body['year']
        instructors=[Instructor.query.get(int(i)) for i in body['instructors']]
        record.semester = semester
        record.year = year
        record.instructors = instructors
        db.session.commit()
        return jsonify({"message":"success!!"})
    
    def delete(self, id):
      record = Section.query.get(id)
      if record == None:
        error_dict = {"message":"student id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        record_copy = record.__dict__.copy()
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message":"success!!"})



class Instructor_API(Resource):
    def get(self):
      records = Instructor.query.all()
      return serialize_list(records)

    def post(self):
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)
      name = body['instructor_name']
      salary = body['salary']
      dept_id = body['dept_id']
      new_instructor = Instructor(instructor_name=name, dept_id=dept_id, salary=salary)
      dict_copy = new_instructor.__dict__.copy()
      db.session.add(new_instructor)
      db.session.commit()
      return serialize_single(dict_copy)
    
    
      


class Individual_Instructor_API(Resource):
    def get(self, id):
      record = Instructor.query.get(id)
      if record == None:
        error_dict = {"message":"instructor id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        return serialize_single(record.__dict__)
    
    def put(self, id):
      record = Instructor.query.get(id)
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)

      if record == None:
        error_dict = {"message":"Instructor id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        name = body['instructor_name']
        dept_id = body['dept_id']
        salary = body['salary']
        record.instructor_name = name
        record.dept_id = dept_id
        record.salary = salary
        updated_instructor_copy = record.__dict__.copy()
        db.session.commit()
        return serialize_single(updated_instructor_copy)
    
    def delete(self, id):
      record = Instructor.query.get(id)
      if record == None:
        error_dict = {"message":"student id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        record_copy = record.__dict__.copy()
        db.session.delete(record)
        db.session.commit()
        return serialize_single(record_copy)


class Course_API(Resource):
    def get(self):
      records = Course.query.all()
      return serialize_list(records)

    def post(self):
      print(request.json)
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)
        print(body["credits"])
      else:
        error_dict = {"message":"invalid response"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      name = body['course_title']
      credits = body['credits']
      dept_id = body['dept_id']
      new_course = Course(course_title=name, dept_id=dept_id, course_credits=credits)
      dict_copy = new_course.__dict__.copy()
      db.session.add(new_course)
      db.session.commit()
      return serialize_single(dict_copy)

class Individual_Course_API(Resource):
    def get(self, id):
      record = Course.query.get(id)
      if record == None:
        error_dict = {"message":"course id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        return serialize_single(record.__dict__)
    
    def put(self, id):
      record = Course.query.get(id)
      print(request.json)
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)
        
      if record == None:
        error_dict = {"message":"student id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        name = body['course_title']
        credits = body['credits']
        dept_id = body['dept_id']
        record.course_title = name
        record.credits = credits
        record.dept_id = dept_id
        updated_student_copy = record.__dict__.copy()
        db.session.commit()
        return serialize_single(updated_student_copy)
    
    def delete(self, id):
      record = Course.query.get(id)
      if record == None:
        error_dict = {"message":"student id not found in the database"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      else:
        record_copy = record.__dict__.copy()
        db.session.delete(record)
        db.session.commit()
        return serialize_single(record_copy)

class Teaches_API(Resource):
    def get(self):
      records = teaches.query.all()
      return serialize_list(records)

    def post(self):
      print(request.json)
      if request.json:
        body = str(request.json)
        print(type(request.json))
        body = body.replace("\'", "\"")
        body = json.loads(body)
        print(body)
      else:
        error_dict = {"message":"invalid response"}
        response = make_response(jsonify(error_dict), 401)
        response.headers["Content-Type"] = "application/json"
        return response
      course_id = body['course_id']
      sec_id = body['sec_id']
      new_course = sec_course(course_id=course_id, sec_id=sec_id)
      dict_copy = new_course.__dict__.copy()
      db.session.add(new_course)
      db.session.commit()
      return serialize_single(dict_copy)

class Individual_Teaches_API(Resource):
    def get(self, id):
      records = sec_course.query.filter(sec_course.sec_id == id)
      return serialize_list(records)



class Section_Courses_API(Resource):
    def get(self):
      records = teaches.query.all()
      return serialize_list(records)
    






API.add_resource(Department_API, '/api/departments')
API.add_resource(Student_API, '/api/students')
API.add_resource(Instructor_API, '/api/instructors')
API.add_resource(Section_API, '/api/sections')
API.add_resource(Course_API, '/api/courses')

API.add_resource(Individual_Student_API, '/api/students/<int:id>')
API.add_resource(Individual_Instructor_API, '/api/instructors/<int:id>')
API.add_resource(Individual_Department_API, '/api/departments/<int:id>')
API.add_resource(Individual_Section_API, '/api/sections/<int:id>')
API.add_resource(Individual_Course_API, '/api/courses/<int:id>')