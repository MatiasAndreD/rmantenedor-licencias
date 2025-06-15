from flask import Blueprint, g, request, current_app

auth_bp = Blueprint('auth', __name__)


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
