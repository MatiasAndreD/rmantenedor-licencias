from flask import Blueprint, render_template, redirect, url_for, flash, request

from .. import db
from ..models import Licencia, Ejecutivo
from ..auth import get_current_user
from .forms import LicenciaForm, DeleteForm

licencias_bp = Blueprint('licencias', __name__, url_prefix='/licencias')


@licencias_bp.route('/')
def listar():
    """Lista todas las licencias."""
    user = get_current_user()
    query = Licencia.query.join(Ejecutivo)
    if user and user.role == 'agente' and not request.args.get('all'):
        query = query.filter(Ejecutivo.id.in_([e.id for e in user.ejecutivos]))
    licencias = query.all()
    return render_template('licencias/list.html', licencias=licencias)


@licencias_bp.route('/nueva', methods=['GET', 'POST'])
def crear():
    """Crear una nueva licencia."""
    form = LicenciaForm()
    user = get_current_user()
    ejecutivos = Ejecutivo.query.all()
    if user and user.role == 'agente':
        ejecutivos = user.ejecutivos
    form.ejecutivo_id.choices = [(e.id, e.nombre) for e in ejecutivos]
    if form.validate_on_submit():
        lic = Licencia(
            ejecutivo_id=form.ejecutivo_id.data,
            fecha_inicio=form.fecha_inicio.data,
            fecha_termino=None if form.extendida.data else form.fecha_termino.data,
            extendida=form.extendida.data,
        )
        db.session.add(lic)
        db.session.commit()
        flash('Licencia creada')
        return redirect(url_for('licencias.listar'))
    return render_template('licencias/form.html', form=form, form_title='Nueva Licencia')


@licencias_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    """Editar una licencia existente."""
    lic = Licencia.query.get_or_404(id)
    form = LicenciaForm(obj=lic)
    user = get_current_user()
    ejecutivos = Ejecutivo.query.all()
    if user and user.role == 'agente':
        ejecutivos = user.ejecutivos
    form.ejecutivo_id.choices = [(e.id, e.nombre) for e in ejecutivos]
    if form.validate_on_submit():
        lic.ejecutivo_id = form.ejecutivo_id.data
        lic.fecha_inicio = form.fecha_inicio.data
        lic.fecha_termino = None if form.extendida.data else form.fecha_termino.data
        lic.extendida = form.extendida.data
        db.session.commit()
        flash('Licencia actualizada')
        return redirect(url_for('licencias.listar'))
    return render_template('licencias/form.html', form=form, form_title='Editar Licencia')


@licencias_bp.route('/<int:id>/eliminar', methods=['GET', 'POST'])
def eliminar(id):
    """Eliminar una licencia."""
    lic = Licencia.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(lic)
        db.session.commit()
        flash('Licencia eliminada')
        return redirect(url_for('licencias.listar'))
    return render_template('licencias/confirm_delete.html', form=form, licencia=lic)
