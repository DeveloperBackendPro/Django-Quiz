from home.utils import send_code
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from home.forms import StudentSignUpForm, UserUpdateForm, CodeForm
from django.core.paginator import (Paginator, PageNotAnInteger, EmptyPage)
from home.models import Student, Course, Question, Answers, Ready, Information, User
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout

class register(CreateView):
    template_name = 'Authenticate/register_students.html'
    form_class = StudentSignUpForm
    success_url = reverse_lazy('loading_page')
    success_message = "Вы успешно зарегистрировались"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        info = Information.objects.all()[:1]
        kwargs['info'] = info
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid
def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_student:
            request.session['pk'] = user.pk
            return redirect('verify_code')
        else:
            return redirect('login_form')
    info = Information.objects.all().order_by('-id')[:1]
    context = {
        'info':info,
    }
    return render(request, 'Authenticate/login-dark.html', context)

def verify_code(request):
    info = Information.objects.all().order_by('-id')[:1]
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.code}"
        if not request.POST:
           print(code_user)
           send_code(code_user, user.email)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                login(request,user)
                return redirect('student')
            else:
               return redirect('verify_code')
    return render(request, 'verify.html', {'form':form, 'info':info})

@login_required(login_url='login_form')
def update(request):
    info = Information.objects.all().order_by('-id')[:1]
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        user_manager = UserUpdateForm(request.POST, instance=request.user)
        if user_manager.is_valid():
            user_manager.save()
            return redirect('student')
        else:
            return redirect("update")
    else:
        user_manager = UserUpdateForm(instance=request.user)
        context = {
            'info':info,
            'student':student,
            'user_manager': user_manager,
        }
        return render(request, 'student_update.html', context)

@login_required(login_url='login_form')
def password(request):
    info = Information.objects.all().order_by('-id')[:1]
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('student')
        else:
            return redirect('password')
    else:
        form = PasswordChangeForm(request.user)
        context = {
            'info':info,
            'student':student,
            'form': form,
        }
        return render(request, 'change_password.html', context)
def logout_student(request):
    logout(request)
    return redirect('login_form')

@login_required(login_url='login_form')
def student(request):
    info = Information.objects.all().order_by('-id')[:1]
    student = Student.objects.get(user=request.user)
    response_native = Answers.objects.filter(student=student).order_by('-id')
    response = Answers.objects.filter(student=student).values('course')
    course = Course.objects.filter(status='Open').exclude(id__in=response)
    course_count = course.count()
    response_count = response_native.count()
    paginator = Paginator(course, 5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        course = paginator.page(page)
    except PageNotAnInteger:
        course = paginator.page(1)
    except EmptyPage:
        course = paginator.page(paginator.num_pages)
    context = {
        'info':info,
        'student':student,
        'response':response,
        'response_native':response_native,
        'course':course,
        'course_count':course_count,
        'response_count':response_count,
    }
    return render(request, 'student-dashboard.html', context)

@login_required(login_url='login_form')
def course_detail(request, code):
    info = Information.objects.all().order_by('-id')[:1]
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(code=code)
    ready = Ready.objects.filter(question__course__code=code, student=student)
    quiz = Question.objects.filter(course__code=code).order_by('?')
    context = {
        'info':info,
        'student':student,
        'course':course,
        'quiz':quiz,
        'ready':ready
    }
    return render(request, 'course_detail.html', context)

@login_required(login_url='login_form')
def ready_to_test(request, code):
    info = Information.objects.all().order_by('-id')[:1]
    student = Student.objects.get(user=request.user)
    course_detail = Course.objects.get(code=code)
    ready = Ready.objects.filter(question__course__code=code, student=student)
    context = {
        'info':info,
        'student':student,
        'course_detail':course_detail,
        'ready':ready,
    }
    return render(request, 'ready_to_test.html', context)

def post_exam_two(request, id):
    student = Student.objects.get(user=request.user)
    if request.method == 'POST':
        questions = Question.objects.filter(course__question=id)
        score = 0
        for item in questions:
            if item.ans == request.POST.get(item.question):
                score += item.score
            selected_answer = request.POST.get(item.question)
            Ready.objects.create(student=student, course_id=id, question=item,  true_answer=selected_answer)
        percent = score
        rezult = Answers()
        rezult.total_score = percent
        rezult.student = student
        rezult.course_id = id
        rezult.save()
        return redirect('student')
    else:
        return redirect('student')


def loading_page(request):
    return render(request, 'Authenticate/loading_page.html')


def outside_404_not_found(request,exception):
    return render(request, 'error/outside.html',)

def request_500(request):
    return render(request, 'error/500_request.html',)


def request_502_error(request):
    return render(request, 'error/502_home_request.html',)