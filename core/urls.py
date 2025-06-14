from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views  # your DRF-based views

router = DefaultRouter()
router.register(r'api/courses', api_views.CourseViewSet)
router.register(r'api/posts', api_views.PostViewSet)
router.register(r'api/comments', api_views.CommentViewSet)
router.register(r'api/chat', api_views.ChatMessageViewSet)
router.register(r'api/profiles', api_views.UserProfileViewSet)


urlpatterns = [
    # HTML Views with CBVs
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),

    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/enroll/<int:course_id>/', views.EnrollCourseView.as_view(), name='enroll_course'),
    path('courses/unenroll/<int:course_id>/', views.UnenrollCourseView.as_view(), name='unenroll_course'),

    path('announcements/', views.AnnouncementsView.as_view(), name='announcements'),
    path('announcements/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('announcements/<int:post_id>/comment/', views.AddCommentView.as_view(), name='add_comment'),

    path('chat/', views.ChatView.as_view(), name='chat'),
    path('chat/get/', views.GetMessagesView.as_view(), name='get_messages'),
    path('chat/send/', views.SendMessageView.as_view(), name='send_message'),

    path('teacher/panel/', views.TeacherPanelView.as_view(), name='teacher_panel'),

    path('announcements/search/', views.SearchAnnouncementsView.as_view(), name='search_announcements'),
    path('users/search/', views.SearchUsersView.as_view(), name='search_users'),

    # API Views
    path('', include(router.urls)),

    # JWT Token Auth
    path('api/token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', api_views.MyTokenRefreshView.as_view(), name='token_refresh'),
]
