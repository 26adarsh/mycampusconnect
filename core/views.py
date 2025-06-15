from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse
from .models import UserProfile, Course, Post, Comment, ChatMessage
from .forms import PostForm, UserProfileForm, CourseForm
from django.contrib.auth.models import User

# Basic
class HomeView(TemplateView):
    template_name = 'home.html'

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from .models import UserProfile  # make sure this import is correct

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            role = request.POST.get('role')
            roll_no = request.POST.get('roll_no')
            department = request.POST.get('department')
            profile_pic = request.FILES.get('profile_pic')

            if not username or not email or not password1 or not password2:
                return render(request, 'register.html', {'error': "All fields are required."})

            if password1 != password2:
                return render(request, 'register.html', {'error': "Passwords do not match."})

            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': "Username already exists."})

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)

            # Create profile
            profile = UserProfile.objects.create(
                user=user,
                role=role,
                roll_no=roll_no,
                department=department,
                profile_pic=profile_pic
            )

            login(request, user)
            return redirect('home')

        except Exception as e:
            print("REGISTER ERROR:", e)
            return render(request, 'register.html', {'error': str(e)})



# Profile
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        return context

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(instance=profile)
        return render(request, 'edit_profile.html', {'form': form})

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'edit_profile.html', {'form': form})

# Courses
class CourseListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if hasattr(user, 'userprofile') and user.userprofile.role == 'student':
            courses = Course.objects.filter(students=user)
        else:
            courses = Course.objects.all()
        return render(request, 'course_list.html', {'courses': courses})

class EnrollCourseView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'student':
            return redirect('home')
        course = get_object_or_404(Course, id=course_id)
        course.students.add(request.user)
        return redirect('course_list')

class UnenrollCourseView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'student':
            return redirect('home')
        course = get_object_or_404(Course, id=course_id)
        course.students.remove(request.user)
        return redirect('course_list')

from django.utils.decorators import method_decorator
from .decorators import teacher_required, student_required

@method_decorator(teacher_required, name='dispatch')
class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'create_course.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.userprofile.role != 'teacher':
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('course_list')

# Announcements
class AnnouncementsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'announcements.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

from .forms import CommentForm

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()  # <-- Add this line
        return context


from .forms import CommentForm

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        return redirect('post_detail', post_id=post_id)


# Chat
class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'chat.html'

class GetMessagesView(LoginRequiredMixin, View):
    def get(self, request):
        messages = ChatMessage.objects.order_by('-timestamp')[:20][::-1]
        data = [
            {
                'sender': msg.sender.username,
                'message': msg.message,
                'timestamp': msg.timestamp.strftime('%b %d %H:%M')
            } for msg in messages
        ]
        return JsonResponse(data, safe=False)

class SendMessageView(LoginRequiredMixin, View):
    def post(self, request):
        msg = request.POST.get('message')
        if msg:
            ChatMessage.objects.create(sender=request.user, message=msg)
        return JsonResponse({'status': 'ok'})

# Teacher Panel
class TeacherPanelView(LoginRequiredMixin, View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'teacher':
            return redirect('home')
        form = PostForm()
        students = UserProfile.objects.filter(role='student')
        posts = Post.objects.filter(author=request.user).order_by('-created_at')
        return render(request, 'teacher_panel.html', {
            'form': form,
            'students': students,
            'posts': posts
        })

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'teacher':
            return redirect('home')
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return redirect('teacher_panel')

# Search
class SearchAnnouncementsView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q')
        author_filter = request.GET.get('author')

        posts = Post.objects.all()
        if query:
            posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
        if author_filter:
            posts = posts.filter(author__username=author_filter)
        authors = User.objects.filter(post__isnull=False).distinct()
        return render(request, 'search_announcements.html', {
            'posts': posts,
            'authors': authors,
            'query': query,
            'author_filter': author_filter
        })

class SearchUsersView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q')
        users = User.objects.filter(username__icontains=query) if query else []
        return render(request, 'search_users.html', {
            'users': users,
            'query': query
        })
