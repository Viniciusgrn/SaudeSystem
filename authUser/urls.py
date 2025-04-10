from django.urls import path

from django.contrib.auth import views as auth_views
from .views import PerfilUpdate, PasswordsChangeView, UsuarioCreate

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='auth/login.html '), name="userLogin"),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name="userLogin"),
    path('userCreate/', UsuarioCreate.as_view(), name="userCreate"),
    path('logout/', auth_views.LogoutView.as_view(), name='userLogout'),
    path('perfilupdate/', PerfilUpdate.as_view(), name='userInfo'),
    path('change/', PasswordsChangeView.as_view(template_name='auth/form.html'), name='changePassword'),
    path('change-complete/', auth_views.PasswordChangeDoneView.as_view(template_name='auth/success_change.html'), name='changedonePassword'),
    # path('change/', auth_views.PasswordChangeView.as_view(template_name='auth/form1.html'), name='changePassword'),
    # path('login/', views.LoginView.as_view(template_name='auth/form.html '), name="userLogin"),
    # path('logout/', views.LogoutView.as_view(), name='userLogout'),
    # path('login/', views.login, name="userLogin"),
    # path('logout/', views.logout, name='userLogout'),
]