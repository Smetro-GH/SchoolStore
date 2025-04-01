# SchoolStore - Sistema de Tienda Escolar

Sistema de tienda escolar desarrollado con Flask que permite la gestión de productos, pedidos y pagos.

## Características

- Sistema de autenticación de usuarios
- Panel de administración
- Catálogo de productos
- Carrito de compras
- Sistema de pagos (efectivo y tarjeta)
- Gestión de inventario
- Seguimiento de pedidos

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd SchoolStore
```

2. Crear y activar un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Configuración

1. Crear un archivo `.env` en la raíz del proyecto:
```
SECRET_KEY=tu-clave-secreta-aqui
```

## Uso

1. Iniciar la aplicación:
```bash
python main.py
```

2. Acceder a la aplicación en el navegador:
```
http://localhost:5000
```

## Credenciales de Administrador

- Nombre de Usuario: admin
- Contraseña: Anglo123

## Estructura del Proyecto

```
SchoolStore/
├── instance/           # Base de datos SQLite
├── website/           # Código principal de la aplicación
│   ├── static/       # Archivos estáticos (CSS, JS, imágenes)
│   ├── templates/    # Plantillas HTML
│   ├── __init__.py   # Inicialización de la aplicación
│   ├── admin.py      # Rutas de administración
│   ├── auth.py       # Rutas de autenticación
│   ├── models.py     # Modelos de la base de datos
│   └── views.py      # Rutas principales
├── main.py           # Punto de entrada de la aplicación
├── requirements.txt  # Dependencias del proyecto
└── README.md        # Este archivo
```

## Seguridad

- Las contraseñas se almacenan de forma segura usando PBKDF2 con SHA256
- Protección contra CSRF
- Validación de datos en formularios
- Control de acceso basado en roles

## Soporte

Para reportar problemas o solicitar nuevas características, por favor crear un issue en el repositorio.