from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Quiz, MCQ, Submission, UserAnswer
from django.contrib.auth.decorators import login_required , user_passes_test
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods

def home_view(request):
    return render(request, 'index.html')


def about_us(request):
    return render(request, 'about-us.html')

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Create/update profile info
#             user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
#             user.profile.phone_number = form.cleaned_data.get('phone_number')
#             user.profile.gender = form.cleaned_data.get('gender')
#             user.profile.save()
            
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}! You can now log in.')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'register.html', {'form': form})

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.ser.profile)
        
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, 'Your profile has been updated!')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
    
#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }
#     return render(request, 'profile.html', context)
# @login_required
# def profile_view(request):
#     user = request.user
#     profile = user.profile  

#     if request.method == 'POST':
#         if 'update_profile' in request.POST:
#             username = request.POST.get('username', '').strip()
#             email = request.POST.get('email', '').strip()
#             first_name = request.POST.get('first_name', '').strip()
#             last_name = request.POST.get('last_name', '').strip()

#             # Check uniqueness for username and email
#             if User.objects.exclude(pk=user.pk).filter(username=username).exists():
#                 messages.error(request, "Username already taken.")
#             elif User.objects.exclude(pk=user.pk).filter(email=email).exists():
#                 messages.error(request, "Email already in use.")
#             else:
#                 user.username = username
#                 user.email = email
#                 user.first_name = first_name
#                 user.last_name = last_name
#                 user.save()
#                 messages.success(request, "Profile updated successfully!")

#         elif 'update_photo' in request.POST and 'image' in request.FILES:
#             profile.image = request.FILES['image']
#             profile.save()
#             messages.success(request, "Profile photo updated!")

#         return redirect('profile')

#     return render(request, 'profile.html', {
#         'user': user,
#         'profile': profile,
#     })



# @require_http_methods(["GET", "POST"])
# def register_view(request):
#     if request.method == 'POST':
#         # Get form data
#         username = request.POST.get('username', '').strip()
#         email = request.POST.get('email', '').strip().lower()
#         password = request.POST.get('password', '')
#         confirm_password = request.POST.get('cpassword', '')

        
#         if not all([username, email, password, confirm_password]):
#             messages.error(request, 'All fields are required.')
#         elif password != confirm_password:
#             messages.error(request, 'Passwords do not match.')
#         elif User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already exists.')
#         elif User.objects.filter(email=email).exists():
#             messages.error(request, 'Email already used.')
#         else:
#             try:
                
#                 validate_password(password)

                
#                 user = User.objects.create_user(
#                     username=username,
#                     email=email,
#                     password=password
#                 )

               
#                 messages.success(request, 'Registration successful! You can now log in.')
#                 return redirect('login')  

#             except ValidationError as e:
#                 for error in e:
#                     messages.error(request, error)

#     return render(request, 'register.html')


# @require_http_methods(["GET", "POST"])
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '').strip()
#         password = request.POST.get('password', '')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:  
#             login(request, user) 
            
#             if user.is_superuser:
#                 return redirect('home')
#             else:
#                 return redirect('home')

#         else:
#             messages.error(request, 'Invalid username or password.')

#     return render(request, 'login.html')



# @login_required
# def profile_view(request):
#     user = request.user
#     profile_image = user.profile_image.url if hasattr(user, 'profile_image') and user.profile_image else "https://via.placeholder.com/120"

#     context = {
#         "full_name": user.get_full_name(),
#         "email": user.email,
#         "username": user.username,
#         "phone": getattr(user, 'phone', 'Not provided'),
#         "dob": getattr(user, 'dob', 'Not provided'),
#         "role": getattr(user, 'role', 'user').capitalize(),
#         "profile_image": profile_image,
#         "is_admin": user.is_superuser,
#     }
#     return render(request, 'profile.html', context)




def is_admin(user):
    return user.is_superuser 


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


# List all courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

def add_courses(request):
    return render(request, 'addcourse.html')

@login_required
def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Course.objects.create(
            name=name,
            description=description,
            image=image
        )
        messages.success(request, 'Course added successfully!')
        return redirect('courses')
    
    return render(request, 'addcourse.html')

# def update_course_view(request, course_id):
#     course = get_object_or_404(Course, id=course_id)

#     if request.method == "POST":
#         name = request.POST.get('name')
#         image = request.FILES.get('image')
#         description = request.POST.get('description')


#         # Validation
#         if not name:
#             messages.error(request, "Course name is mandatory")
#         elif Course.objects.filter(name=name).exclude(course_id=course_id).exists():
#             messages.error(request, "Course Name is already registered")
#         else:
#             course.name = name
#             course.image = image
#             course.description = description
#             course.save()
#             messages.success(request, f"Course {name} updated successfully")
#             return redirect('addcourse')


#     return render(request, 'update.html', context={'course': course})



@login_required
def add_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        Quiz.objects.create(course=course, title=title)
        messages.success(request, 'Quiz created successfully!')
        return redirect('quiz_list', course_id=course.id)

    return render(request, 'addquiz.html', {'course': course})

@login_required
def add_mcq(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        question = request.POST.get('question')
        option_a = request.POST.get('option_a')
        option_b = request.POST.get('option_b')
        option_c = request.POST.get('option_c')
        option_d = request.POST.get('option_d')
        correct_option = request.POST.get('correct_option')

        MCQ.objects.create(
            quiz=quiz,
            question_text=question,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option
        )

        messages.success(request, 'MCQ added successfully!')
        return redirect('add_mcq', quiz_id=quiz.id)

    return render(request, 'addmcq.html', {'quiz': quiz})



@login_required
@user_passes_test(is_admin)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.image.delete()  # Delete the image from media folder
    course.delete()
    messages.success(request, 'Course deleted successfully.')
    return redirect('courses')  # Adjust to your actual course list page


# Show quizzes for a selected course
def quiz_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    quizzes = course.quizzes.all()
    return render(request, 'quiz.html', {'course': course, 'quizzes': quizzes})

@login_required
@user_passes_test(is_admin)
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    course_id = quiz.course.id
    quiz.delete()
    messages.success(request, 'Quiz deleted successfully.')
    return redirect('quiz_list', course_id=course_id)

# Take a quiz
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        submission = Submission.objects.create(user=request.user, quiz=quiz)
        score = 0

        for question in questions:
            selected_option = request.POST.get(str(question.id))
            is_correct = (selected_option == question.correct_option)
            if is_correct:
                score += 1
            UserAnswer.objects.create(
                submission=submission,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

        submission.score = score
        submission.save()
        messages.success(request, f'You scored {score} out of {questions.count()}!')
        return redirect('quiz_result', submission_id=submission.id)

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})

# Show result and leaderboard
# @login_required
# def quiz_result(request, submission_id):
#     submission = get_object_or_404(Submission, id=submission_id, user=request.user)
#     leaderboard = Submission.objects.filter(quiz=submission.quiz).order_by('-score', 'submitted_at')[:10]

#     return render(request, 'quiz_result.html', {
#         'submission': submission,
#         'leaderboard': leaderboard
#     })

@login_required
def quiz_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, user=request.user)
    quiz = submission.quiz
    questions_with_answers = []

    for question in quiz.questions.all():
        user_answer = submission.answers.filter(question=question).first()
        questions_with_answers.append({
            'question': question,
            'user_answer': user_answer.selected_option if user_answer else None,
            'correct_answer': question.correct_option
        })

    leaderboard = Submission.objects.filter(quiz=quiz).order_by('-score', 'submitted_at')

    context = {
        'submission': submission,
        'leaderboard': leaderboard,
        'questions_with_answers': questions_with_answers,
    }
    return render(request, 'quiz_result.html', context)
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import ProfilePic

@login_required
def upload_profile_pic(request):
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        pic_obj, created = ProfilePic.objects.get_or_create(user=request.user)
        pic_obj.image = request.FILES['profile_pic']
        pic_obj.save()
    return redirect('/profile/')  # or wherever your profile page lives

def edit_profile(request):
   return render(request, 'edit_profile.html')

import requests
from django.shortcuts import render


import requests
from django.shortcuts import render

def about_view(request):
    try:
        response = requests.get("http://127.0.0.1:5000/api/about")
        data = response.json()
    except Exception as e:
        data = {"error": str(e)}

    return render(request, "about.html", {"data": data})
