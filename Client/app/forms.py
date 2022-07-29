from wsgiref import validate
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired


class DepartmentAdd(Form):
    name = StringField('Name', validators=[DataRequired()])
    budget = IntegerField('Budget', validators=[DataRequired()])

class SectionAdd(Form):
    semester  = IntegerField('Semester', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    instructors = SelectMultipleField('Instructors', choices=[], validate_choice=False)

class CourseAdd(Form):
    title = StringField('Course Title', validators=[DataRequired()])
    credits = StringField('Course Credits', validators=[DataRequired()])
    dept_id = SelectField('Department', choices=[], validate_choice=False)

class StudentAdd(Form):
    name = StringField('Name', validators=[DataRequired()])
    credits = IntegerField('Credits', validators=[DataRequired()])
    dept_id = SelectField('Department', choices=[], coerce=int, validate_choice=False)
    sec_id = SelectField('Section', choices=[], coerce=int, validate_choice=False)


class InstructorAdd(Form):
    name = StringField('Name', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired()])
    dept_id = SelectField('Department', choices=[], validate_choice=False)

class Section_course(Form):
    course_id = SelectField('Course', validate_choice=False, choices=[])
    sec_id = IntegerField('Section', validators=[DataRequired()])
