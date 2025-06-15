from datetime import date

from app import create_app, db
from app.models import Usuario, Ejecutivo, Licencia

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # Sucursales and executives
    e1 = Ejecutivo(nombre="Juan Perez", sucursal="Santiago Centro", modelo_atencion="Presencial")
    e2 = Ejecutivo(nombre="Maria Gomez", sucursal="Santiago Centro", modelo_atencion="Remoto")
    e3 = Ejecutivo(nombre="Pedro Fuentes", sucursal="Las Condes", modelo_atencion="Presencial")
    e4 = Ejecutivo(nombre="Carla Soto", sucursal="Las Condes", modelo_atencion="Remoto")
    db.session.add_all([e1, e2, e3, e4])

    # Users
    agente = Usuario(username="agente1", role="agente")
    agente.ejecutivos.extend([e1, e2])
    admin = Usuario(username="admin1", role="admin")
    db.session.add_all([agente, admin])

    # Licencias
    l1 = Licencia(ejecutivo=e1, fecha_inicio=date(2024, 1, 10), fecha_termino=date(2024, 1, 20))
    l2 = Licencia(ejecutivo=e2, fecha_inicio=date(2024, 2, 5), extendida=True)
    l3 = Licencia(ejecutivo=e3, fecha_inicio=date(2024, 3, 1), fecha_termino=date(2024, 3, 10))
    db.session.add_all([l1, l2, l3])

    db.session.commit()
    print("Base de datos inicializada con datos de ejemplo")

