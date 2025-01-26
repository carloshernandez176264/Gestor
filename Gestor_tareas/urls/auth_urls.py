from django.urls import path
from django.contrib.auth import views as auth_views

from Gestor_tareas.views.auth_views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

]
