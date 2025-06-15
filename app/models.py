from . import db


agente_ejecutivo = db.Table(
    'agente_ejecutivo',
    db.Column('agente_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('ejecutivo_id', db.Integer, db.ForeignKey('ejecutivo.id')),
)


class Usuario(db.Model):
    """Usuario del sistema."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)

    ejecutivos = db.relationship(
        "Ejecutivo",
        secondary=agente_ejecutivo,
        backref="agentes",
    )


class Ejecutivo(db.Model):
    """Representa a un ejecutivo asociado a una sucursal."""

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    sucursal = db.Column(db.String(100))
    modelo_atencion = db.Column(db.String(100))


class Licencia(db.Model):
    """Licencias asociadas a un ejecutivo."""

    id = db.Column(db.Integer, primary_key=True)
    ejecutivo_id = db.Column(db.Integer, db.ForeignKey("ejecutivo.id"), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_termino = db.Column(db.Date)
    extendida = db.Column(db.Boolean, default=False)

    ejecutivo = db.relationship("Ejecutivo", backref="licencias")
