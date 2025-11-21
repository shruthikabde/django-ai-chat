from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from chatapp import views as chat_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
     path('register/', chat_views.register, name='register'),  # 👈 new

    path('', chat_views.chat_page, name='chat'),

    path('api/chat/', chat_views.chat_api, name='chat_api'),
]

