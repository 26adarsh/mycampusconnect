from django import forms
from .models import UserProfile, Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    roll_no = forms.CharField(required=False)
    department = forms.CharField(required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role', 'roll_no', 'department', 'profile_pic']


# Optional: for editing user profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['roll_no', 'department', 'profile_pic']


from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description']
