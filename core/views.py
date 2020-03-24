from django.conf import settings
from django.views import generic
from django.views.generic import TemplateView
from .models import Post, Monkey, Comment
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm, GuestForm, LoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from captcha.fields import CaptchaField
from django.contrib.auth import authenticate, login, logout
import os
import io

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'index.html'

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

class AboutPage(TemplateView):
    template_name = "about.html"

def PenumbraPage(request):
    return render(request, "penumbra.html")

def ContactPage(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "contact.html", {'form': form})

def SuccessPage(request):
    return render(request, "success.html")

def GiveBanana(request):
    if Monkey.objects.first() == None:
        new_monkey = Monkey()
        new_monkey.save()
    m = Monkey.objects.first()
    m.bananas += 1
    goal = 25
    if m.bananas < 25:
        m.level = 1
        goal = 25
        last_goal = 0
    elif m.bananas < 100:
        m.level = 2
        goal = 100
        last_goal = 25
    elif m.bananas < 250:
        m.level = 3
        goal = 250
        last_goal = 100
    elif m.bananas < 500:
        m.level = 4
        goal = 500
        last_goal = 250
    elif m.bananas < 1000:
        m.level = 5
        goal = 1000
        last_goal = 500
    m.save()
    remaining = goal - m.bananas
    progress = ((m.bananas - last_goal) * 100) / (goal - last_goal)
    return render(request, "banana.html", {'bananas': m.bananas, 'level': m.level, 'goal': remaining, 'progress': progress})

def GuestbookPage(request):
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            new_comment = Comment(name = request.POST['name'], comment = request.POST['comment'])
            new_comment.save()
            return redirect('guestbook')
    else:
        form = GuestForm()
    comments = Comment.objects.all().order_by('-date_added')
    return render(request, 'guestbook.html', { 'form': form, 'comments': comments })

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'access.html', { 'result': 1 })
                else:
                    return render(request, 'access.html', { 'result': 2 })
            else:
                return render(request, 'access.html', { 'result': 0 })
    else:
        form = LoginForm()
    return render(request, 'access.html', { 'result': 2 })

def Logout(request):
    logout(request)
    return render(request, 'access.html', { 'result': 3 })

def CodexIndex(request, file):
    files = os.listdir(os.path.join(settings.BASE_DIR, 'codex/'))
    md = io.open(os.path.join(settings.BASE_DIR, 'codex\\')+file, mode="r", encoding="utf-8")
    string = md.read()
    md.close()

    return render(request, 'codex.html', {'md':string, 'name': file, 'files': files})
