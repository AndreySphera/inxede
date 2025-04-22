from flask import Flask, render_template, request, redirect, url_for
from models import db, Student, Course, Teacher

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    all_students = Student.query.all()          # Было: students → all_students
    all_teachers = Teacher.query.all()         # Было: teachers → all_teachers
    all_courses = Course.query.all()           # Было: courses → all_courses
    return render_template('index.html', teachers=all_teachers, students=all_students, courses=all_courses)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_name = request.form['name']     # Было: name → student_name
        student = Student(name=student_name)   # Было: new_student → student
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        teacher_name = request.form['name']     # Было: name → teacher_name
        teacher = Teacher(name=teacher_name)   # Было: new_teacher → teacher
        db.session.add(teacher)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_teacher.html')

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    available_teachers = Teacher.query.all()    # Было: teachers → available_teachers
    if request.method == 'POST':
        course_name = request.form['name']      # Было: name → course_name
        selected_teacher_id = request.form['teacher_id']  # Было: teacher_id → selected_teacher_id
        course = Course(name=course_name, teacher_id=selected_teacher_id)  # Было: new_course → course
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_course.html', teachers=available_teachers)

if __name__ == '__main__':
    app.run(debug=True)
