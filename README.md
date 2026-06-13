# 🏠 Focus Salas Backend

Sigue estos pasos para ejecutar el proyecto en tu máquina:

1. Clonar repositorio
git clone https://github.com/jose18042006/focus_salas_mobile.git

2. Crear entorno virtual
python -m venv .venv

3. Activar entorno virtual
Windows: `.venv\Scripts\activate`  
Mac/Linux: `source .venv/bin/activate`

4. Configurar .env
Crea un archivo `.env` y añade la URL de Neon.tech: `DATABASE_URL=postgresql+asyncpg://tu_usuario:tu_pass@tu_host.neon.tech/tu_db?sslmode=require`

5. Instalar dependencias (con el venv activo)
pip install -r requirements.txt

6. Ejecutar migraciones
alembic revision --autogenerate -m "creacion inicial salas"
alembic upgrade head

7. Ejecutar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload





Flujo completo

DM (Profesor)


Inicia sesión → obtiene JWT con rol dm
Crea sala desde la app → POST /api/v1/rooms
El servidor genera automáticamente un código de 8 caracteres y un QR
La app muestra el QR en pantalla


Estudiante


Inicia sesión → obtiene JWT con rol student
Escanea el QR con la app → obtiene el invitation_code
App hace POST /api/v1/rooms/{room_id}/join con el código
Estudiante queda registrado en la sala


Documentación API

Con el servidor corriendo, accede al swagger en:

http://127.0.0.1:8000/schema/swagger
