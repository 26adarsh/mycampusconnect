#reverse() acts like a smart URL generator:
#You give it the view's name, it gives you the correct path.


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    return render(request, 'home.html')

#register

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # after register, go to login page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

#student

from django.contrib.auth.decorators import login_required
from .models import StudentProfile
from .forms import StudentProfileForm

@login_required
def profile_view(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile = StudentProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

#course

from .models import Course
from django.contrib.auth.models import User

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.students.add(request.user)
    return redirect('course_list')

@login_required
def unenroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.students.remove(request.user)
    return redirect('course_list')


from .models import Post, Comment
from django.views.decorators.http import require_POST

@login_required
def announcements(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'announcements.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

@require_POST
@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    text = request.POST.get('comment')
    if text:
        Comment.objects.create(post=post, author=request.user, text=text)
    return redirect('post_detail', post_id=post_id)


from django.http import JsonResponse
from .models import ChatMessage

@login_required
def chat_view(request):
    return render(request, 'chat.html')

@login_required
def get_messages(request):
    messages = ChatMessage.objects.order_by('-timestamp')[:20]
    messages = reversed(messages)
    data = [
        {
            'sender': msg.sender.username,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%b %d %H:%M')
        }
        for msg in messages
    ]
    return JsonResponse(data, safe=False)

@login_required
def send_message(request):
    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            ChatMessage.objects.create(sender=request.user, message=msg)
    return JsonResponse({'status': 'ok'})

from .models import UserRole
from .forms import PostForm

@login_required
def teacher_panel(request):
    role = UserRole.objects.get(user=request.user)
    if not role.is_teacher:
        return redirect('home')  # or show error

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('announcements')
    else:
        form = PostForm()
    
    return render(request, 'teacher_panel.html', {'form': form})


from django.db.models import Q


@login_required
def search_announcements(request):
    query = request.GET.get('q')
    author_filter = request.GET.get('author')

    posts = Post.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    
    if author_filter:
        posts = posts.filter(author__username=author_filter)

    authors = User.objects.filter(post__isnull=False).distinct()

    return render(request, 'search_announcements.html', {
        'posts': posts,
        'authors': authors,
        'query': query,
        'author_filter': author_filter,
    })

@login_required
def search_users(request):
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query) if query else []

    return render(request, 'search_users.html', {
        'users': users,
        'query': query
    })
