# FitLife - Sistema de Gestión de Gimnasio

## Descripción

FitLife es una aplicación web desarrollada con Django para gestionar membresías, pagos, reservas de clases y control de acceso de un gimnasio.

Proyecto académico de Desarrollo Backend.

## Tecnologías

- Python y Django
- Django REST Framework (dependencia instalada)
- PostgreSQL
- HTML y CSS
- Gunicorn y Nginx
- AWS EC2
- Git

## Funcionalidades

### Membresías y pagos
- Administración de planes y membresías.
- Estados ACTIVA, VENCIDA y CONGELADA.
- Registro y consulta de pagos.

### Control de acceso
- Simulación de lectura QR mediante códigos de identificación.
- Validación de membresía vigente y pago confirmado.
- Registro de entradas y salidas permitidas o denegadas.

### Reservas de clases
- Reserva y cancelación de cupos.
- Control de capacidad.
- Lista de espera y asignación automática de cupos liberados.

### Dashboard de aforo
- Cantidad de clientes presentes.
- Identificación de clientes dentro del gimnasio.
- Actualización automática cada 10 segundos.
- Acceso restringido al personal administrativo.

## Aplicaciones Django

- accounts: usuarios y perfiles.
- membresias: planes, membresías y pagos.
- accesos: validación de ingresos y salidas.
- clases: clases, reservas y lista de espera.
- dashboard: inicio y aforo.

## Instalación

1. Clonar el repositorio de GitHub.
2. Crear y activar un entorno virtual de Python.
3. Instalar dependencias con pip install -r requirements.txt.
4. Configurar PostgreSQL y las variables de entorno requeridas.
5. Ejecutar python manage.py migrate.
6. Crear un administrador con python manage.py createsuperuser.
7. Configurar los hosts permitidos y ejecutar Django.

La configuración exacta de las variables de entorno debe revisarse en fitlife/settings.py.

## Despliegue AWS

El proyecto está desplegado en una instancia EC2 con Ubuntu, PostgreSQL, Gunicorn y Nginx.

Dirección pública actual:
http://3.83.236.76/

La IP puede cambiar al reiniciar la instancia si no se utiliza una Elastic IP.

## Seguridad

- Autenticación de usuarios.
- Restricción de acceso administrativo.
- Protección CSRF.
- Variables de entorno para credenciales.
- Exclusión de archivos privados mediante .gitignore.

El despliegue académico utiliza HTTP y no está preparado para almacenar credenciales reales de producción.

## Inteligencia artificial

Se utilizó asistencia de inteligencia artificial durante el desarrollo, depuración y documentación.

Consultar prompts_ia.md para el registro correspondiente.
