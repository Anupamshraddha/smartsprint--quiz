from flask import Flask, render_template, redirect, request, url_for, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from functools import wraps
from werkzeug.utils import secure_filename
import random
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config["SECRET_KEY"] = "Your secret key"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User model
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), unique=True,nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Dummy course and quiz storage
courses = []
reviews = []
class Course:
    def __init__(self, id, name, description, image_filename):
        self.id = id
        self.name = name
        self.description = description
        self.image_filename = image_filename
        self.quizzes = []

class Quiz:
    def __init__(self, name, questions=None):
        self.name = name
        self.questions = []

class Question:

    _id_counter = 1
    def __init__(self, question, options, correct_option):
        self.question = question
        self.options = options
        self.id = Question._id_counter
        self.correct_option = correct_option
# Admin decorator
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash("Access denied!", "danger")
            return redirect(url_for("home"))
        return func(*args, **kwargs)
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")
import random

import random

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            otp = random.randint(100000, 999999)
            session['reset_otp'] = str(otp)
            session['otp_email'] = user.email
            flash(f'Your OTP is: {otp}', 'info')  # Temporary display
            return redirect(url_for('verify_otp'))
        flash("Email not found", 'danger')
    return render_template('reset_request.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        input_otp = request.form['otp']
        if input_otp == session.get('reset_otp'):
            session['otp_verified'] = True
            flash("OTP verified successfully. You can now reset your password.", 'success')
            return redirect(url_for('reset_password'))
        else:
            flash("Invalid OTP", 'danger')
    return render_template('verify_otp.html')

@app.route('/resend-otp')
def resend_otp():
    if 'otp_email' in session:
        import random
        otp = random.randint(100000, 999999)
        session['reset_otp'] = str(otp)
        flash(f'New OTP sent: {otp}', 'info')  # Show new OTP in alert
    else:
        flash("Session expired. Please start over.", 'danger')
        return redirect(url_for('reset_password_request'))
    
    return redirect(url_for('verify_otp'))
@app.route('/reset-password-final', methods=['GET', 'POST'])
def reset_password():
    if not session.get('otp_verified'):
        flash("Unauthorized access", 'danger')
        return redirect(url_for('reset_password_request'))

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        if new_password != confirm_password:
            flash("Passwords do not match", 'warning')
        else:
            user = User.query.filter_by(email=session.get('otp_email')).first()
            if user:
                user.set_password(new_password)  # Your password hash function
                db.session.commit()
                session.clear()
                flash("Password reset successfully. Please log in.", 'success')
                return redirect(url_for('login'))

    return render_template('reset_password_final.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Store form data in the reviews list
        reviews.append({
            'username': username,
            'email': email,
            'subject': subject,
            'message': message
        })

        flash('Message sent successfully!', 'success')
        return redirect(url_for('reviews_page'))

    return render_template('contact.html')


@app.route('/reviews')
def reviews_page():
    return render_template('reviews.html', reviews=reviews)




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        mobile = request.form.get("mobile")
        role = request.form.get("role")

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        new_user = User(name=name, email=email, mobile=mobile, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route('/courses')
def view_courses():
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
@login_required
@admin_required
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            course_id = len(courses) + 1
            new_course = Course(id=course_id, name=name, description=description, image_filename=filename)
            courses.append(new_course)
            flash('Course added successfully!', 'success')
            return redirect(url_for('view_courses'))
        else:
            flash('Image is required!', 'danger')

    return render_template('add_course.html')

@app.route('/course/<int:course_id>/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz(course_id):
    course = next((c for c in courses if c.id == course_id), None)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('view_courses'))

    if request.method == 'POST':
        quiz_name = request.form['quiz_name']

        # Create the quiz
        new_quiz = Quiz(name=quiz_name)
        course.quizzes.append(new_quiz)
        flash(f'Quiz "{quiz_name}" created.', 'success')

        # Redirect to add_question page
        return redirect(url_for('view_quizzes', course_id=course_id, quiz_name=quiz_name))

    return render_template('create_quiz.html', course=course)

@app.route('/course/<int:course_id>/quiz/<quiz_name>/add_question', methods=['GET', 'POST'])
@login_required
def add_question(course_id, quiz_name):
    course = next((c for c in courses if c.id == course_id), None)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('view_courses'))

    quiz = next((q for q in course.quizzes if q.name == quiz_name), None)
    if not quiz:
        flash('Quiz not found.', 'danger')
        return redirect(url_for('view_quizzes', course_id=course_id))

    if request.method == 'POST':
        question_text = request.form['question']
        options = [
            request.form['option1'],
            request.form['option2'],
            request.form['option3'],
            request.form['option4'],
        ]
        correct_index = int(request.form['correct']) - 1
        question = Question(question=question_text, options=options, correct_option=options[correct_index])
        quiz.questions.append(question)
        flash('Question added successfully!', 'success')

        # Stay on same page to add more
        return redirect(url_for('add_question', course_id=course_id, quiz_name=quiz_name))

    return render_template('add_question.html', course=course, quiz=quiz)

@app.route('/course/<int:course_id>/quizzes')
@login_required
def view_quizzes(course_id):
    course = next((c for c in courses if c.id == course_id), None)
    if not course or not course.quizzes:
        flash('No quizzes available for this course.', 'warning')
        return redirect(url_for('view_courses'))

    return render_template('list_quizzes.html', course=course)

@app.route('/course/<int:course_id>/quiz/<quiz_name>', methods=['GET', 'POST'])
@login_required
def show_quiz(course_id, quiz_name):
    course = next((c for c in courses if c.id == course_id), None)
    
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('view_courses'))

    quiz = next((q for q in course.quizzes if q.name == quiz_name), None)

    if not quiz:
        flash('Quiz not found.', 'danger')
        return redirect(url_for('view_courses'))

    if not quiz.questions:
        flash('No questions in this quiz.', 'warning')
        return redirect(url_for('view_quizzes', course_id=course_id))

    if request.method == 'POST':
        user_answers = request.form
        correct_count = 0

        for question in quiz.questions:
            selected = user_answers.get(f'question_{question.id}')
            if selected == question.correct_option:
                correct_count += 1

        return render_template('quiz_result.html', score=correct_count, total=len(quiz.questions),quiz=quiz,user_answers=user_answers)


    return render_template('quiz.html', quiz=quiz, course=course)

@app.route('/enroll/<int:course_id>')
@login_required
def enroll_course(course_id):
    course = next((c for c in courses if c.id == course_id), None)
    if not course:
        flash("Course not found.", "danger")
        return redirect(url_for("view_courses"))

    if course.quizzes:
        return redirect(url_for('view_quizzes', course_id=course_id))
    else:
        flash("No quiz available for this course.", "warning")
        return redirect(url_for('view_courses'))

@app.route('/course/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    global courses
    course = next((c for c in courses if c.id == course_id), None)
    
    if not course:
        return "Course not found", 404

    courses = [c for c in courses if c.id != course_id]
    return redirect(url_for('view_courses'))

@app.route('/course/<int:course_id>/quiz/<quiz_name>/delete', methods=['POST'])
@login_required
def delete_quiz(course_id, quiz_name):
    course = next((c for c in courses if c.id == course_id), None)
    if not course:
        return "Course not found", 404

    quiz = next((q for q in course.quizzes if q.name == quiz_name), None)
    if not quiz:
        return "Quiz not found", 404

    course.quizzes.remove(quiz)
    return redirect(url_for('view_quizzes', course_id=course_id))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")



# ✅ API: Submit a new review (POST)
@app.route('/api/reviews', methods=['POST'])
def api_submit_review():
    data = request.get_json()
    required_fields = ['username', 'email', 'subject', 'message']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields in request'}), 400

    reviews.append({
        'username': data['username'],
        'email': data['email'],
        'subject': data['subject'],
        'message': data['message']
    })

    return jsonify({'message': 'Review submitted successfully'}), 201

# ✅ API: Get all reviews (GET)
@app.route('/api/reviews', methods=['GET'])
def api_get_reviews():
    return jsonify(reviews), 200


from flask import jsonify, request
from werkzeug.utils import secure_filename
import os

# GET API to list all courses
@app.route('/api/courses', methods=['GET'])
def api_get_courses(): 
    return jsonify([
        {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'image_url': url_for('static', filename='uploads/' + course.image_filename, _external=True)
        }
        for course in courses
    ]), 200


@app.route('/api/add_course', methods=['POST'])
@login_required
@admin_required
def api_add_course():
    name = request.form.get('name')
    description = request.form.get('description')
    image = request.files.get('image')

    if not name or not description or not image:
        return jsonify({'error': 'Name, description, and image are required'}), 400

    try:
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        course_id = len(courses) + 1
        new_course = Course(id=course_id, name=name, description=description, image_filename=filename)
        courses.append(new_course)

        return jsonify({'message': 'Course added successfully!', 'course_id': course_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
