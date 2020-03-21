from django.views import generic
from django.views.generic import TemplateView
from .models import Post, Monkey, Comment
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm, GuestForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from captcha.fields import CaptchaField

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
    b = Monkey.objects.first()
    b.bananas += 1
    b.save()
    bananas = b.bananas
    return render(request, "banana.html", {'bananas': b.bananas})

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