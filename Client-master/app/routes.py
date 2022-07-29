
from importlib_metadata import re
from app import app
from flask import redirect, render_template, request, flash
from app.forms import DepartmentAdd, SectionAdd, CourseAdd, StudentAdd, InstructorAdd, Section_course
import requests
import json

base_url = 'http://127.0.0.1:5000/'

@app.route('/')
def first_page():
  return render_template('start_page.html')

@app.route('/home')
def index():
  return render_template('home1.html')


# Get student details
@app.route('/students', methods=['GET', 'POST'])
def students():

  # API calls to retrive data
  students = requests.get(base_url+'/api/students').json()
  departments = requests.get(base_url+'/api/departments').json()
  sections = requests.get(base_url+'/api/sections').json()

  # Checking if the data recieved back is not None
  if departments and students and sections:

    # Creating dictionaries for each table
    department_names = {departments[dept]["dept_id"] : departments[dept]["name"] for dept in departments.keys()} 
    semesters = {sections[section]["section_id"] : sections[section]["semester"] for section in sections.keys()}
    years = {sections[section]["section_id"] : sections[section]["year"] for section in sections.keys()}

    # render template student.html with all nessasary dictionaries
    return render_template('student_home.html', students=students, department_names=department_names, semesters=semesters, years=years)
  else:
    return "sorry"


# Add Students to the Database using the API
@app.route('/students/add', methods=['GET', 'POST'])
def add_students():
  form = StudentAdd(request.form)
  
  #API calls to the server
  departments = requests.get(base_url+'/api/departments').json()
  sections = requests.get(base_url+'/api/sections').json()

  if departments and sections:
    department_names = [(departments[dept]["dept_id"], departments[dept]["name"]) for dept in departments.keys()]
    semesters = [(sections[section]["section_id"], sections[section]["semester"]) for section in sections.keys()]
    years = [(sections[section]["section_id"], sections[section]["semester"]) for section in sections.keys()]
    form.dept_id.choices = department_names
    print(form.dept_id.choices)
    form.sec_id.choices = semesters

  if request.method == 'POST' and form.validate():
    print(form.name.data, form.dept_id.data)
    data={"name":form.name.data, "credits":form.credits.data, "dept_id":form.dept_id.data, "sec_id":form.sec_id.data}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/students'
    student = requests.post(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/students')
  
  elif request.method == 'POST' and not form.validate():
    print(form.errors)
    print(form.dept_id.data)
    flash(form.errors)
    return "sorry not valid"

  return render_template('add_students.html', form=form)


# Create a page for individual student
@app.route('/students/<int:id>', methods=['GET', 'POST', 'PUT'])
def student_page(id):

  #api calls to the database
  student = requests.get(base_url+'/api/students/'+str(id)).json()
  departments = requests.get(base_url+'/api/departments').json()
  sections = requests.get(base_url+'/api/sections').json()
  print(student)

  #on response
  if student and departments and sections:
    department_names = {departments[dept]["dept_id"] : departments[dept]["name"] for dept in departments.keys()} #dictionary of department names
    semesters = {sections[section]["section_id"] : sections[section]["semester"] for section in sections.keys()} #dictionary of semesters
    years = {sections[section]["section_id"] : sections[section]["year"] for section in sections.keys()} # dictionary of years

    return render_template("student_page.html", student=student, department_names=department_names, semesters=semesters, years=years)


# Modify student records
@app.route('/students/<int:id>/edit', methods=['GET', 'POST', 'PUT'])
def student_edit(id):
  student = requests.get(base_url+'/api/students/'+str(id)).json()
  departments = requests.get(base_url+'/api/departments').json()
  sections = requests.get(base_url+'/api/sections').json()
  form = StudentAdd(request.form)

  if departments and sections and student:
    print(student, departments, sections)
    department_names = {departments[dept]["dept_id"]: departments[dept]["name"] for dept in departments.keys()}
    department_names_choices = [(departments[dept]["dept_id"], departments[dept]["name"]) for dept in departments.keys()]

    department_ids = [departments[dept]["dept_id"] for dept in departments.keys()]
    section_ids = [sections[sec]["section_id"] for sec in sections.keys()]

    semesters = {sections[section]["section_id"]: sections[section]["semester"] for section in sections.keys()}
    semesters_choices = [(sections[section]["section_id"], sections[section]["semester"]) for section in sections.keys()]

    years = [(sections[section]["section_id"], sections[section]["semester"]) for section in sections.keys()]
    
    form.dept_id.choices = department_names_choices
    form.sec_id.choices = semesters_choices

  if request.method == 'POST' and form.validate():
    print(form.name.data, form.dept_id.data)
    data={"name":form.name.data, "credits":form.credits.data, "dept_id":form.dept_id.data, "sec_id":form.sec_id.data}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/students/'+str(id)
    student = requests.put(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/students')
  
  elif request.method == 'POST' and not form.validate():
    print(form.errors)
    print(form.dept_id.data)
    flash(form.errors)
    return "sorry not valid"
  
  form.name.data = student["student_name"]
  if student["dept_id"] in department_ids:
    form.dept_id.data  = (student["dept_id"], department_names[student["dept_id"]])
  else:
    form.dept_id.choices.append((-1, "unassigned"))
    form.dept_id.data = (-1, "unassigned")

  form.credits.data = student["credits"]
  if student["sec_id"] in section_ids:
    form.sec_id.data = (student["sec_id"], semesters[student["sec_id"]])
  else:
    form.sec_id.choices.append((-1, "assigned"))
    form.sec_id.data = (-1, "assigned")

  return render_template('edit_student.html', form=form, student=student, department_names=department_names, semesters=semesters, years=years)

# Delete a student
@app.route('/students/<int:id>/delete', methods=['GET', 'POST'])
def delete_student(id):
  response = requests.delete(base_url+'/api/students/'+str(id))
  student = response.json()
  print(student)
  if student:
    return redirect('/students')
  else:
    return "sorry"


# Get department details
@app.route('/departments', methods=['GET', 'POST'])
def departments():
  response = requests.get(base_url+'/api/departments')
  departments = response.json()
  print(departments)
  if departments:
    return render_template("department_home.html", departments=departments)
  else:
    return "sorry"


# Get individual department details
@app.route('/departments/<int:id>')
def department_page(id):
  response = requests.get(base_url+'/api/departments/'+str(id))
  department = response.json()
  if department:
    student_response = requests.get(base_url+'/api/students')
    course_response = requests.get(base_url+'/api/students')
    return render_template('department_page.html', department=department, students=student_response, courses=course_response)
  else:
    return "sorry"

# Add new Departments
@app.route('/departments/add', methods=['GEt', 'POST'])
def add_department():
  form = DepartmentAdd(request.form)
  if request.method == 'POST' and form.validate():
    print(form.name.data, form.budget.data)
    data = {"name":form.name.data, "budget":form.budget.data}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/departments'
    department = requests.post(url, headers=headers, json=json.dumps(data))
    return redirect('/departments')
  elif request.method == 'POST' and not form.validate():
    flash(form.errors)
  
  return render_template('add_departments.html', form=form)

# Modify a department's data
@app.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
def edit_department(id):

  form = DepartmentAdd(request.form)
  response = requests.get(base_url+'/api/departments/'+str(id))
  department = response.json()
  print(department)
  if request.method == 'POST' and form.validate():
    print(form.name.data, form.budget.data)
    data={"name":form.name.data, "budget":form.budget.data}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/departments/'+str(id)
    department = requests.put(url, headers=headers, json=json.dumps(data))
    flash("Sucess")
    return redirect('/departments')
  else:
    flash(form.errors)
  
  if department:
    form.name.data = department["name"]
    form.budget.data = department["dept_budget"]
    return render_template('edit_department.html', department=department, form=form)
  else:
    return "sorry"


# Delete a department
@app.route('/departments/<int:id>/delete', methods=['GET', 'POST','DELETE'])
def delete_department(id):
  response = requests.delete(base_url+'/api/departments/'+str(id))
  department = response.json()
  print(department)
  if department:
    return redirect('/departments')
  else:
    return "sorry"


# Get instructor details
@app.route('/instructors', methods=['GET', 'POST'])
def instructors():
  instructors = requests.get(base_url+'/api/instructors').json()
  departments = requests.get(base_url+'/api/departments').json()

  if departments:
    department_names = {departments[dept]["dept_id"]: departments[dept]["name"] for dept in departments.keys()}
    return render_template('instructor_home.html', instructors=instructors, department_names=department_names) 
  else:
    return "sorry"

# Add instructors
@app.route('/instructors/add', methods=['GET', 'POST'])
def add_instructors():
  form = InstructorAdd(request.form)
  departments = requests.get(base_url+'/api/departments').json()
  if departments:
    department_names = {departments[dept]["dept_id"]: departments[dept]["name"] for dept in departments.keys()}
    department_names_choices = [(departments[dept]["dept_id"], departments[dept]["name"]) for dept in departments.keys()]

    form.dept_id.choices = department_names_choices
  
  if request.method == 'POST' and form.validate():
    data={"instructor_name":form.name.data, "salary":form.salary.data, "dept_id":form.dept_id.data}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/instructors'
    Instructor = requests.post(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/instructors')
  
  if request.method == 'POST' and not form.validate():
    print(form.errors)
    return "sorry"
  
  return render_template('add_instructors.html', form=form)

# Modify instructor details
@app.route('/instructors/<int:id>/edit', methods=['GET', 'POST'])
def edit_instructors(id):

  form = InstructorAdd(request.form)
  instructor = requests.get(base_url+'/api/instructors/'+str(id)).json()
  departments = requests.get(base_url+'/api/departments').json()
  department_names = {departments[dept]["dept_id"]: departments[dept]["name"] for dept in departments.keys()}
  department_ids = [departments[dept]["dept_id"] for dept in departments.keys()]
    
  
  if departments and instructor:
    print(departments, instructor)

    department_names = {departments[dept]["dept_id"]: departments[dept]["name"] for dept in departments.keys()}
    department_names_choices = [(departments[dept]["dept_id"], departments[dept]["name"]) for dept in departments.keys()]

    form.dept_id.choices = department_names_choices
    if instructor["dept_id"] not in department_ids:
      form.dept_id.choices.append((-1, "unassigned"))

  if request.method == 'POST' and form.validate():
    print(form.name.data, form.dept_id.data)
    data={"instructor_name":form.name.data, "salary":form.salary.data, "dept_id":form.dept_id.data}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/instructors/'+str(id)
    student = requests.put(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/instructors')
  
  elif request.method == 'POST' and not form.validate():
    print(form.errors)
    print(form.dept_id.data)
    flash(form.errors)
    return "sorry not valid"

  form.name.data = instructor["instructor_name"]
  if instructor["dept_id"] not in department_ids:
    form.dept_id.data = (-1, "unassigned")
  form.dept_id.data  = (instructor["dept_id"], department_names[instructor["dept_id"]])
  form.salary.data = instructor["salary"]
  return render_template('edit_instructor.html', form=form, department_names=department_names, instructor=instructor)

# Delete instructors
@app.route('/instructors/<int:id>/delete', methods=['GET', 'POST'])
def delete_instructor(id):
  instructor = requests.delete(base_url+'/api/instructors/'+str(id)).json()
  print(instructor)
  if instructor:
    return redirect('/instructors')
  else:
    return "sorry"

# Get course details
@app.route('/courses', methods=['GET', 'POST'])
def courses():
  courses = requests.get(base_url+'/api/courses').json()
  departments = requests.get(base_url+'/api/departments').json()
  instructors = requests.get(base_url+'/api/instructors').json()
  print(courses, departments, instructors)
  if departments:
    department_names = {departments[dept]["dept_id"]: departments[dept]["name"] for dept in departments.keys()}
    department_names_choices = [(departments[dept]["dept_id"], departments[dept]["name"]) for dept in departments.keys()]
    
    # instructor_names = {instructors[inst]["instructor_id"]: instructors[inst]["instructor_name"] for inst in instructors.keys()}
    # instructor_names_choices = [(instructors[inst]["instructor_id"], instructors[inst]["instructor_name"]) for inst in departments.keys()]

    return render_template('course_home.html', courses=courses, department_names=department_names)    
  else:
    return "sorry"

# Add Courses
@app.route('/courses/add', methods=['GET', 'POST'])
def add_courses():
  form = CourseAdd(request.form)
  departments = requests.get(base_url+'/api/departments').json()

  if departments:
    department_names = {departments[dept]["dept_id"]: departments[dept]["name"] for dept in departments.keys()}
    department_names_choices = [(departments[dept]["dept_id"], departments[dept]["name"]) for dept in departments.keys()]
    
    form.dept_id.choices = department_names_choices

  if request.method == 'POST' and form.validate():
    data={"course_title":form.title.data, "credits":form.credits.data, "dept_id":form.dept_id.data}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/courses'
    student = requests.post(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/courses')
  
  elif request.method == 'POST' and not form.validate():
    print(form.errors)
    print(form.dept_id.data)
    flash(form.errors)
    return "sorry not valid"

  return render_template('add_courses.html', form=form)

# Edit Courses
@app.route('/courses/<int:id>/edit', methods=['GET', 'POST'])
def edit_courses(id):

  form = CourseAdd(request.form)
  departments = requests.get(base_url+'/api/departments').json()
  course = requests.get(base_url+'/api/courses/'+str(id)).json()

  if departments and course:
    print(course, departments)

    department_names = {departments[dept]["dept_id"]: departments[dept]["name"] for dept in departments.keys()}
    department_names_choices = [(departments[dept]["dept_id"], departments[dept]["name"]) for dept in departments.keys()]
    department_ids = [departments[dept]["dept_id"] for dept in departments.keys()]

    form.dept_id.choices = department_names_choices
    
    if course['dept_id'] not in department_ids:
      form.dept_id.choices.append((-1, "unassigned"))

  if request.method == 'POST' and form.validate():
    data={"course_title":form.title.data, "credits":form.credits.data, "dept_id":form.dept_id.data}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/courses/'+str(id)
    student = requests.put(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/courses')
  
  elif request.method == 'POST' and not form.validate():
    print(form.errors)
    print(form.dept_id.data)
    flash(form.errors)
    return "sorry not valid"

  form.title.data = course["course_title"]
  form.credits.data = course["course_credits"]
  if course["dept_id"] in department_ids:
      form.dept_id.data  = (course["dept_id"], department_names[course["dept_id"]])
  else:
    form.dept_id.choices.append((-1, "unassigned"))
  return render_template('edit_course.html', form=form, course=course)


# Delete Courses
@app.route('/courses/<int:id>/delete', methods=['GET', 'POST','DELETE'])
def delete_course(id):
  response = requests.delete(base_url+'/api/courses/'+str(id))
  course = response.json()
  print(course)
  if course:
    return redirect('/courses')
  else:
    return "sorry"

# Get section details
@app.route('/sections', methods=['GET'])
def sections():
  sections = requests.get(base_url+'/api/sections').json()
  courses = requests.get(base_url+'/api/courses').json()
  instructors = requests.get(base_url+'/api/instructors').json()
  students = requests.get(base_url+'/api/students').json()
  print(courses, departments, instructors)
  if  instructors:    
    instructor_names = {instructors[inst]["instructor_id"]: instructors[inst]["instructor_name"] for inst in instructors.keys()}
    instructor_names_choices = [(instructors[inst]["instructor_id"], instructors[inst]["instructor_name"]) for inst in instructors.keys()]

    return render_template('section_home.html', sections=sections, instructor_names=instructor_names)    
  else:
    return "sorry"

# Edit sections
@app.route('/sections/<int:id>/edit', methods=['GET', 'POST'])
def edit_sections(id):
  form = SectionAdd(request.form)
  section = requests.get(base_url+'/api/sections/'+str(id)).json()
  print(section)
  if request.method == 'POST' and form.validate():
    data={"semester":form.semester.data, "year":form.year.data}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/sections/'+str(id)
    student = requests.put(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/sections')
  
  elif request.method == 'POST' and not form.validate():
    print(form.errors)

  form.semester.data = section['0']['semester']
  form.year.data = section['0']['year']
  return render_template('edit_section.html', form=form, section=section)
  

# Add new Sections
@app.route('/sections/add', methods=['GET', 'POST'])
def add_sections():
  form = SectionAdd(request.form)
  instructors = requests.get(base_url+'/api/instructors').json()

  if instructors:
    instructor_names = {instructors[inst]["instructor_id"]: instructors[inst]["instructor_name"] for inst in instructors.keys()}
    instructor_names_choices = [(instructors[inst]["instructor_id"], instructors[inst]["instructor_name"]) for inst in instructors.keys()]
    print(instructor_names_choices)
    form.instructors.choices = instructor_names_choices

  if request.method == 'POST' and form.validate():
    instructor_user_choices = {int(choice): instructor_names[int(choice)] for choice in form.instructors.data}
    data={"semester":form.semester.data, "year":form.year.data, "instructors":instructor_user_choices}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+'/api/sections'
    student = requests.post(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/sections')
  
  elif request.method == 'POST' and not form.validate():
    print(form.errors)

  return render_template('add_sections.html', form=form)


# Individual Section details
@app.route('/sections/<int:id>', methods=['GET', 'POST'])
def section_home(id):
  section = requests.get(base_url + '/api/sections/'+str(id)).json()['0']
  section_courses = requests.get(base_url +'/api/sec_courses/'+str(id)).json()
  section_course_ids = [section_courses[c]['course_id'] for c in section_courses.keys()]
  courses = {}
  i = 0
  for ids in section_course_ids:
    k = requests.get(base_url+'/api/courses/'+str(ids)).json()
    courses[i] = k
    i += 1
  print(courses)

  if section:
    return render_template("section_page.html", section=section, courses=courses)
  
  return "sorry"

# Add Instructors to Sections
@app.route('/sections/<int:id>/add/instructors', methods=['GET', 'POST'])
def add_instructors_to_section(id):

  section = requests.get(base_url+'/api/sections/'+str(id)).json()['0']
  section_instructors = section['instructors']
  instructors = requests.get(base_url + '/api/instructors').json()

  section_instructor_ids = set([section_instructors[s]['instructor_id'] for s in section_instructors.keys()])
  instructor_ids = set([instructors[i]['instructor_id'] for i in instructors.keys()])
  instructor_option_ids = list(instructor_ids - section_instructor_ids)
  instructor_options = [(instructors[i]['instructor_id'], instructors[i]['instructor_name']) for i in instructors.keys() if instructors[i]['instructor_id'] in instructor_option_ids]
  instructor_names = {instructors[i]['instructor_id']:instructors[i]['instructor_name'] for i in instructors if instructors[i]['instructor_id'] in instructor_option_ids}
  print(instructor_names)
  print(instructor_options)

  form = SectionAdd(request.form)
  form.instructors.choices = instructor_options
  form.semester.data = section['semester']
  form.year.data = section['year']

  if request.method == 'POST' and form.validate():
    print(form.instructors.data)
    instructor_user_choices = {int(choice): instructor_names[int(choice)] for choice in form.instructors.data}
    data={"semester":form.semester.data, "year":form.year.data, "instructors":instructor_user_choices}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+ '/api/sec_instructors/' + str(id)
    student = requests.post(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/sections/'+str(id))
  
  elif request.method == 'POST' and not form.validate():
    print(form.errors)
  
  return render_template('add_instructor_to_sections.html', form=form, section=section)

# Remove instructors from Sections
@app.route('/sections/<int:id>/delete/instructor/<int:iid>', methods=['GET', 'POST'])
def remove_instructors_from_sections(id, iid):
  print(iid)
  data = {"instructor_id":iid}
  response = requests.delete(base_url+'/api/sec_instructors/'+str(id), json=json.dumps(data)).json()
  print(response)
  if response:
    return redirect(f'/sections/{id}')
  else:
    return "sorry"


# Add courses to sections
@app.route('/sections/<int:id>/add/courses', methods=['GET', 'POST'])
def add_courses_to_sections(id):
  section = requests.get(base_url+'/api/sections/'+str(id)).json()['0']
  section_courses = requests.get(base_url + '/api/sec_courses/'+str(id)).json()
  courses = requests.get(base_url+'/api/courses').json()
  print(courses)
  section_course_ids = set([section_courses[s]['course_id'] for s in section_courses.keys()])
  course_ids = set([courses[i]['course_id'] for i in courses.keys()])
  course_option_ids = list(course_ids - section_course_ids)
  course_options = [(courses[i]['course_id'], courses[i]['course_title']) for i in courses.keys() if courses[i]['course_id'] in course_option_ids]
  course_names = {courses[i]['course_id']:courses[i]['course_title'] for i in courses if courses[i]['course_id'] in course_option_ids}
  print(course_names)
  print(course_options)

  form = Section_course(request.form)
  form.course_id.choices = course_options
  form.sec_id.data = id 
  
  if request.method == 'POST' and form.validate():
    print(form.course_id.data)
    course_user_choices = {int(choice): course_names[int(choice)] for choice in form.course_id.data}
    data={"sec_id":form.sec_id.data, "course_id":course_user_choices}
    headers = {'content-type': 'application/json'}
    print(data)
    url = base_url+ '/api/sec_courses/' + str(id)
    student = requests.post(url, headers=headers, json=json.dumps(data))
    flash("Success!!")
    return redirect('/sections/'+str(id))
  
  elif request.method == 'POST' and not form.validate():
    print(form.errors)
  
  return render_template('add_course_to_sections.html', form=form, section=section)


@app.route('/sections/<int:id>/delete/course/<int:cid>', methods=['GET', 'POST'])
def remove_courses_from_sections(id, cid):
  print(cid)
  data = {"course_id":cid}
  response = requests.delete(base_url+'/api/sec_courses/'+str(id), json=json.dumps(data)).json()
  print(response)
  if response:
    return redirect(f'/sections/{id}')
  else:
    return "sorry"


@app.route('/sections/<int:id>/delete', methods=['GET', 'POST'])
def delete_sections(id):
  response = requests.delete(base_url+'/api/sections/'+str(id)).json()
  print(response)
  if response:
    return redirect('/sections')
  else:
    return "sorry"