# Registro de uso de inteligencia artificial - FitLife

## Objetivo

Documentar la utilización de inteligencia artificial como herramienta de apoyo durante el desarrollo del proyecto académico FitLife.

Los ejemplos de prompts presentados son representativos de las consultas realizadas y no necesariamente transcripciones literales.

## 1. Diseño del proyecto

Prompt representativo:
¿Cómo organizar un proyecto Django para gestionar membresías, pagos, reservas de clases y control de acceso de un gimnasio?

Aplicación:
Se organizó el proyecto en las aplicaciones accounts, membresias, accesos, clases y dashboard.

## 2. Base de datos y modelos

Prompt representativo:
¿Cómo implementar modelos relacionados para planes, membresías, pagos, clases, reservas y listas de espera utilizando Django y PostgreSQL?

Aplicación:
Se desarrollaron modelos Django, relaciones entre entidades y migraciones de base de datos.

## 3. Gestión de reservas

Prompt representativo:
¿Cómo controlar la capacidad de una clase y administrar automáticamente una lista de espera cuando se libera un cupo?

Aplicación:
Se implementaron reservas, cancelaciones y asignación automática de cupos disponibles.

## 4. Control de acceso

Prompt representativo:
¿Cómo simular la lectura de un código QR, validar una membresía vigente y registrar entradas y salidas?

Aplicación:
Se desarrolló una función de validación de acceso y un formulario administrativo para registrar movimientos.

## 5. Dashboard de aforo

Prompt representativo:
¿Cómo calcular cuántos clientes están dentro del gimnasio utilizando el último movimiento permitido de cada usuario?

Aplicación:
Se implementó un servicio de consulta y un dashboard que actualiza su información cada 10 segundos.

## 6. Administración Django

Prompt representativo:
¿Cómo personalizar Django Admin para mostrar columnas, filtros y búsquedas en los modelos del gimnasio?

Aplicación:
Se configuraron las vistas administrativas de usuarios, membresías, pagos, accesos, clases y reservas.

## 7. Despliegue en AWS

Prompt representativo:
¿Cómo desplegar una aplicación Django con PostgreSQL, Gunicorn y Nginx en una instancia AWS EC2?

Aplicación:
Se configuró el entorno de ejecución, la base de datos y el servidor web. También se diagnosticaron problemas de conexión y cambios de dirección IP pública.

## 8. Pruebas y depuración

Prompt representativo:
¿Cómo verificar que las rutas administrativas estén protegidas y que los movimientos de acceso se registren correctamente?

Aplicación:
Se ejecutaron comprobaciones de Django, pruebas con el cliente de pruebas y consultas a PostgreSQL.

## 9. Documentación y Git

Prompt representativo:
¿Cómo preparar un repositorio GitHub para entregar un proyecto Django sin publicar contraseñas ni archivos privados?

Aplicación:
Se configuró .gitignore, se generó requirements.txt y se preparó la documentación.

## Consideraciones

La inteligencia artificial se utilizó como herramienta de orientación técnica y apoyo en la resolución de problemas.

Las propuestas se aplicaron progresivamente y se comprobaron mediante comandos, consultas a la base de datos y pruebas de funcionamiento.

El proyecto incluye un mecanismo de QR simulado y una actualización periódica del dashboard, no un lector físico de QR ni una comunicación instantánea mediante WebSockets.
