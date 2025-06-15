from flask import Blueprint, g, request, current_app

from ..models import Usuario

def get_current_user() -> Usuario | None:
    """Return the Usuario instance for the logged user."""
    username = g.get("current_user")
    if not username:
        return None
    return Usuario.query.filter_by(username=username).first()


def is_admin() -> bool:
    """Return True if the current user has rol admin."""
    user = get_current_user()
    return user is not None and user.role == "admin"

auth_bp = Blueprint('auth', __name__)


@auth_bp.app_context_processor
def inject_user():
    """Expose user information in templates."""
    return {
        'current_user': get_current_user(),
        'is_admin': is_admin(),
    }


@auth_bp.before_app_request
def load_user():
    """Carga el usuario autenticado o el usuario forzado en modo debug."""
    username = None
    if current_app.config.get('FORCED_USER'):
        username = current_app.config['FORCED_USER']
    else:
        # En producción se espera que IIS establezca REMOTE_USER
        username = request.environ.get('REMOTE_USER')
    g.current_user = username
    # In debug it is convenient to create/update the forced user role
    forced_role = current_app.config.get("FORCED_ROLE")
    if username and forced_role:
        user = Usuario.query.filter_by(username=username).first()
        if not user:
            user = Usuario(username=username, role=forced_role)
            current_app.logger.info("Creating forced user %s with role %s", username, forced_role)
            from .. import db

            db.session.add(user)
            db.session.commit()
        elif user.role != forced_role:
            user.role = forced_role
            from .. import db

            db.session.commit()
