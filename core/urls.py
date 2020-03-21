from . import views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('contact/', views.ContactPage, name='contact'),
    path('guestbook/', views.GuestbookPage, name='guestbook'),
    path('penumbra/', views.PenumbraPage, name='penumbra'),
    path('success/', views.SuccessPage, name='success'),
    path('banana/', views.GiveBanana, name='banana'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]