from app import db

class Department(db.Model):
  dept_id = db.Column(db.Integer, primary_key = True)
  dept_budget = db.Column(db.Integer)
  building = db.Column(db.String(64))
  name = db.Column(db.String(64), nullable=False)
  instructors = db.relationship('Instructor', backref='instructors', lazy='dynamic')
  dept_students = db.relationship('Student', backref='dept_students', lazy='dynamic')

class Instructor(db.Model):
  instructor_id = db.Column(db.Integer, primary_key=True)
  instructor_name = db.Column(db.String(64), nullable=False)
  salary = db.Column(db.Integer)
  dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'), nullable=True)

teachers = db.Table('teachers',
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.instructor_id'), primary_key=True),
    db.Column('section_id', db.Integer, db.ForeignKey('section.section_id'), primary_key=True)
)

class Section(db.Model):
  section_id = db.Column(db.Integer, primary_key=True)
  semester = db.Column(db.Integer)
  year = db.Column(db.Integer)
  students = db.relationship('Student', backref='section_students', lazy='dynamic')
  instructors = db.relationship('Instructor', secondary=teachers, lazy='subquery', backref=db.backref('sections', lazy=True))

class Student(db.Model):
  student_id = db.Column(db.Integer, primary_key=True)
  student_name = db.Column(db.String(64), nullable=False)
  credits = db.Column(db.Integer, nullable=False)
  dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'), nullable=True)
  sec_id = db.Column(db.Integer, db.ForeignKey('section.section_id'), nullable=True)

class Course(db.Model):
  course_id = db.Column(db.Integer, primary_key=True)
  course_title = db.Column(db.String(64))
  course_credits = db.Column(db.Integer)
  dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'), nullable=True)


class teaches(db.Model):
  teaches_id = db.Column(db.Integer, primary_key=True) 
  sec_id = db.Column(db.Integer, db.ForeignKey('section.section_id'))
  instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.instructor_id'))

class sec_course(db.Model):
  sec_course_id = db.Column(db.Integer, primary_key=True)
  sec_id = db.Column(db.Integer, db.ForeignKey('section.section_id'))
  course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))