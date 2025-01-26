from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'  # Archivo HTML para el formulario de inicio de sesión
    redirect_authenticated_user = True  # Redirigir si el usuario ya está autenticado

    def get_success_url(self):
        return reverse_lazy('listar_clientes')  # Redirigir a clientes tras el inicio de sesión


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirigir al login tras cerrar sesión
