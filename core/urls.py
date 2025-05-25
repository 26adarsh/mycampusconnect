from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('courses/unenroll/<int:course_id>/', views.unenroll_course, name='unenroll_course'),

    path('announcements/', views.announcements, name='announcements'),
    path('announcements/<int:post_id>/', views.post_detail, name='post_detail'),
    path('announcements/<int:post_id>/comment/', views.add_comment, name='add_comment'),

    path('chat/', views.chat_view, name='chat'),
    path('chat/get/', views.get_messages, name='get_messages'),
    path('chat/send/', views.send_message, name='send_message'),

    path('teacher/panel/', views.teacher_panel, name='teacher_panel'),

    path('announcements/search/', views.search_announcements, name='search_announcements'),

    path('users/search/', views.search_users, name='search_users'),





]
