# Mantenedor de Licencias

Este proyecto contiene una base mínima para iniciar una aplicación Flask
encargada de mantener las licencias de ejecutivos bancarios.

## Uso

1. Crear un entorno virtual e instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar la aplicación de desarrollo:
   ```bash
   FLASK_ENV=development FORCED_USER=usuario python run.py
   ```

La aplicación usa SQLite por defecto y permite forzar un usuario autenticado
mediante la variable `FORCED_USER` cuando se ejecuta en modo *debug*.
