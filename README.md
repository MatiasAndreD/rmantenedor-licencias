# Mantenedor de Licencias

Esta aplicación Flask permite gestionar licencias de ejecutivos bancarios. El sistema funciona con autenticación integrada a IIS en producción y permite forzar un usuario en modo debug.

## Uso

1. Crear un entorno virtual e instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar en modo desarrollo con un usuario forzado y rol definido:
   ```bash
   FLASK_ENV=development FORCED_USER=usuario FORCED_ROLE=admin python run.py
   ```

La base de datos por defecto es SQLite (`data.db`). Para iniciar una base vacía se pueden crear las tablas desde un intérprete de Python:

```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
```

Para poblar la base con datos de ejemplo ejecute:

```bash
python seed.py
```
