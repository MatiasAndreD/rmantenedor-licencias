from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional


class LicenciaForm(FlaskForm):
    ejecutivo_id = SelectField('Ejecutivo', coerce=int, validators=[DataRequired()])
    fecha_inicio = DateField('Fecha inicio', validators=[DataRequired()])
    fecha_termino = DateField('Fecha término', validators=[Optional()])
    extendida = BooleanField('Licencia extendida')
    submit = SubmitField('Guardar')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        if self.extendida.data:
            # fecha_termino se ignora si extendida
            return True
        return True


class DeleteForm(FlaskForm):
    submit = SubmitField('Eliminar')
