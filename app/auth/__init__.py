from flask import Blueprint, g, request, current_app

def is_admin() -> bool:
    """Return True if the current user is an administrator."""
    admins = current_app.config.get('ADMIN_USERS', [])
    return g.get('current_user') in admins

auth_bp = Blueprint('auth', __name__)


@auth_bp.app_context_processor
def inject_user():
    """Expose user information in templates."""
    return {
        'current_user': g.get('current_user'),
        'is_admin': is_admin(),
    }


@auth_bp.before_app_request
def load_user():
    """Carga el usuario autenticado o el usuario forzado en modo debug."""
    user = None
    if current_app.config.get('FORCED_USER'):
        user = current_app.config['FORCED_USER']
    else:
        # En producción se espera que IIS establezca REMOTE_USER
        user = request.environ.get('REMOTE_USER')
    g.current_user = user
