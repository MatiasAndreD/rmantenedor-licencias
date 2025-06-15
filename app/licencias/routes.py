from flask import Blueprint, render_template, redirect, url_for, flash, request

from .. import db
from ..models import Licencia, Ejecutivo
from .forms import LicenciaForm, DeleteForm

licencias_bp = Blueprint('licencias', __name__, url_prefix='/licencias')


@licencias_bp.route('/')
def listar():
    """Lista todas las licencias."""
    licencias = Licencia.query.join(Ejecutivo).all()
    return render_template('licencias/list.html', licencias=licencias)


@licencias_bp.route('/nueva', methods=['GET', 'POST'])
def crear():
    """Crear una nueva licencia."""
    form = LicenciaForm()
    form.ejecutivo_id.choices = [(e.id, e.nombre) for e in Ejecutivo.query.all()]
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
    form.ejecutivo_id.choices = [(e.id, e.nombre) for e in Ejecutivo.query.all()]
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
