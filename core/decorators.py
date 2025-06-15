from django.shortcuts import redirect

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.role == 'teacher':
            return view_func(request, *args, **kwargs)
        return redirect('not_authorized')
    return wrapper

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.userprofile.role == 'student':
            return view_func(request, *args, **kwargs)
        return redirect('not_authorized')
    return wrapper
