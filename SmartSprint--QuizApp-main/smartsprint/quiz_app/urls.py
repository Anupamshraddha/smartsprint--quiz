from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    # path('register/', views.register_view, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    # path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('register/', views.register, name='register'),
    # path('profile/', views.profile, name='profile'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('courses/',views.course_list,name='courses'),
    path('courses/<int:course_id>/quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('submission/<int:submission_id>/result/', views.quiz_result, name='quiz_result'),
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('add-course/', views.add_course, name='add_course'),
    path('course/<int:course_id>/add-quiz/', views.add_quiz, name='add_quiz'),
    path('quiz/<int:quiz_id>/add-mcq/', views.add_mcq, name='add_mcq'),
    path('delete-quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('about/', views.about_view, name='about'),
    # path('profile/', views.profile_view, name='profile'),
    path('upload-profile-pic/', views.upload_profile_pic, name='upload_profile_pic'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    

]



