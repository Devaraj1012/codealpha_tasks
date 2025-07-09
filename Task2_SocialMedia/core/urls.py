from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),  # Homepage
    path('like/<int:post_id>/', views.like_post, name='like_post'),
path('comment/<int:post_id>/', views.add_comment, name='add_comment'),

]
