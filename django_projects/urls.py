"""django_projects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from users.views import register,profile
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('blog/',include('blog.urls')),
    path('admin/', admin.site.urls),
    path('register/',register, name = 'users-register'),
    path('login/',auth_views.LoginView.as_view(template_name = 'users/login.html'),name = 'users-login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='users-logout'),

    # - PasswordResetView sends the mail
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'),
         name='password_reset'),

    # - PasswordResetDoneView shows a success message for the above
    path('password_reset_done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/reset_password_done.html'),
         name='password_reset_done'),

    # - PasswordResetConfirmView checks the link the user clicked and prompts for a new password
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    # - PasswordResetCompleteView shows a success message for the above
    path('password_reset_complete/',
             auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
             name='password_reset_complete'),


    path('profile/',profile, name = 'users-profile'),

]

if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)