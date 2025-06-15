from flask import Blueprint, render_template

from .models import Licencia

licencias_bp = Blueprint('licencias', __name__, url_prefix='/licencias')


@licencias_bp.route('/')
def index():
    """Muestra todas las licencias registradas."""
    licencias = Licencia.query.all()
    return render_template('licencias/index.html', licencias=licencias)
