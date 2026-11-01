from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def personal_requerido(vista):
    @wraps(vista)
    def protegida(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path(),
                login_url='login'
            )

        if not request.user.is_active or not request.user.is_staff:
            raise PermissionDenied(
                "No tienes permisos para acceder a esta sección."
            )

        return vista(request, *args, **kwargs)

    return protegida


def cliente_requerido(vista):
    @wraps(vista)
    def protegida(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path(),
                login_url='login'
            )

        if not request.user.is_active or request.user.is_staff:
            raise PermissionDenied(
                "Esta sección es exclusiva para clientes."
            )

        return vista(request, *args, **kwargs)

    return protegida
