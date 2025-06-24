# **Sistema Administrativo "Cafés Marloy"**

Este repositorio contiene el backend del sistema administrativo para "Cafés Marloy", diseñado para gestionar máquinas expendedoras de café, control de insumos, proveedores, clientes, técnicos, consumos y mantenimientos. La aplicación está desarrollada en Python, utilizando el microframework FastAPI y una base de datos MySQL, sin la utilización de ningún ORM.

## **📋 Requisitos del Entregable Cubiertos**

Este proyecto cumple con los siguientes requisitos del trabajo obligatorio, según la consigna "BD1 \- Obligatorio 2025":

* **Script completo SQL para creación de base de datos y datos maestros:** Incluido en init.sql, que define la estructura de la base de datos y la pobla con datos iniciales.  
* **Aplicación funcional en Python (sin uso de ORM):** El backend está desarrollado en Python con FastAPI, interactuando directamente con MySQL mediante consultas SQL, sin el uso de Object-Relational Mappers.  
* **Validación de datos en backend:** Implementada rigurosamente mediante Pydantic en los schemas de FastAPI para las solicitudes y respuestas HTTP, asegurando la integridad de los datos.  
* **Documentación e instructivo para correr la aplicación localmente:** Detallado en la sección [Configuración y Ejecución Local](#bookmark=id.rg6jp9mfd3vg) de este mismo README.  
* **Dockerización del sistema con docker-compose (app \+ base de datos):** Permite un empaquetado, despliegue y desarrollo simplificado de la aplicación y su base de datos en entornos aislados.  
* **Base de datos relacional (MySQL preferentemente):** Se utiliza MySQL 8.0 como sistema de gestión de base de datos relacional.  
* **No se debe utilizar ningún ORM:** Todas las interacciones con la base de datos se realizan directamente con SQL puro a través del conector mysql-connector-python.  
* **El backend debe estar desarrollado en Python.**  
* **Uso de repositorios públicos (GitHub):** El código fuente se aloja en este repositorio público de GitHub.  
* **Uso de nombres de tabla y campos claros y significativos:** Se han utilizado nombres descriptivos para facilitar la comprensión y el mantenimiento del esquema de la base de datos.

## **🚀 Funcionalidades Implementadas**

El sistema permite gestionar las siguientes entidades y procesos, cubriendo los requerimientos funcionales de la consigna:

### **1\. ABM (Alta, Baja, Modificación)**

* **Proveedores:** Gestión completa de la información de los proveedores de insumos. (Acceso restringido a **Administradores**).  
* **Insumos:** Control de los diferentes tipos de insumos utilizados en las máquinas (café, leche en polvo, chocolate, etc.).  
* **Clientes:** Registro y gestión de la información de los clientes donde se instalan las máquinas expendedoras.  
* **Máquinas:** Alta, modificación y baja de las máquinas expendedoras, incluyendo su modelo, cliente asociado, ubicación específica dentro del cliente y costo de alquiler mensual. (Acceso restringido a **Administradores**).  
* **Técnicos:** Gestión de la información de los técnicos encargados de los mantenimientos. (Acceso restringido a **Administradores**).  
* **Mantenimientos:** Registro de los mantenimientos preventivos y asistencias técnicas realizadas a las máquinas, incluyendo el tipo, fecha, técnico asignado y observaciones.

### **2\. Operaciones Específicas**

* **Registro de Consumos de Insumos:** Capacidad de registrar el consumo de insumos por máquina y fecha, lo cual es fundamental para el cálculo de los cobros mensuales a los clientes.  
* **Registro de Alquiler Mensual Fijo por Máquina:** El costo de alquiler mensual se gestiona directamente en la tabla de maquinas.  
* **Autenticación de Usuarios:** Endpoint de login para usuarios del sistema (login table), con roles de administrador (es\_administrador: TRUE) y usuario normal (es\_administrador: FALSE). Este es el pilar para la implementación de la autorización a los endpoints protegidos.

### **3\. Restricciones Respetadas**

* **Asignación de Máquinas:** Una máquina solo puede estar asignada a un cliente y una ubicación a la vez (validado por una restricción UNIQUE en la base de datos).  
* **Registro de Consumos con Fecha:** Los consumos se registran con fecha para permitir el cálculo de facturación mensual.  
* **Mantenimientos Simultáneos:** Un técnico no puede estar asignado a dos mantenimientos simultáneos (en el mismo día y hora, si se registra), validado por una restricción UNIQUE en la base de datos.

### **4\. Consultas para Reportes (Planificadas/A desarrollar)**

Los siguientes reportes, aunque no completamente implementados como endpoints en esta fase, están contemplados en el diseño de la base de datos y serán desarrollados en fases futuras para cumplir con los requerimientos de la consigna:

* Total mensual a cobrar a cada cliente (suma de alquiler de máquinas más costo de insumos consumidos).  
* Insumos con mayor consumo y costos asociados.  
* Técnicos con más mantenimientos realizados.  
* Clientes con más máquinas instaladas.

## **🛠️ Tecnologías Utilizadas**

* **Backend:** Python 3.11+  
  * **Framework Web:** FastAPI (para construir la API RESTful)  
  * **Validación de Datos:** Pydantic (para la definición de schemas y validación de entrada/salida)  
  * **Autenticación/Autorización:** JWT (python-jose) para la generación y verificación de tokens.  
  * **Hashing de Contraseñas:** passlib\[bcrypt\] (para almacenar contraseñas de forma segura).  
  * **Conector MySQL:** mysql-connector-python (para la interacción directa con la base de datos).  
* **Base de Datos:** MySQL 8.0 (sistema de gestión de base de datos relacional).  
* **Contenedorización:** Docker y Docker Compose (para empaquetar y orquestar la aplicación y la base de datos).

## **🚀 Configuración y Ejecución Local**

Sigue estos pasos para poner en marcha el sistema en tu entorno de desarrollo local usando Docker Compose.

### **Prerrequisitos**

* **Docker Desktop:** Asegúrate de tener Docker y Docker Compose instalados en tu sistema. Puedes descargarlo desde [docker.com](https://www.docker.com/products/docker-desktop/).

### **Pasos**

1. Clonar el Repositorio:  
   Abre tu terminal y clona este repositorio:  
   ```git clone https://github.com/felieppe/marloy-api```
   ```cd marloy-api```
2. Inicializamos la instancia de Docker: 
   ```docker compose up –build```
3. Verificar el Estado de los Contenedores:  
   Puedes verificar que los servicios (app y db) estén corriendo correctamente con:  
   ```docker-compose ps```

   Deberías ver ambos servicios con estado Up.  
4. Acceder a la API:  
   Una vez que los contenedores estén en funcionamiento, tu API de FastAPI estará disponible en:  
   http://localhost:8000/

   Puedes acceder a la **documentación interactiva de Swagger UI** (generada automáticamente por FastAPI) en:  
   http://localhost:8000/docs

   Desde aquí, podrás explorar y probar todos los endpoints definidos en la API.  
5. Detener los Contenedores:  
   Para detener y remover los contenedores (conservando los datos de la base de datos en un volumen persistente):  
   ```docker-compose down```

   Si deseas detener y remover los contenedores, redes y **eliminar los volúmenes de datos** (lo que borrará permanentemente la base de datos):  
   docker-compose down \-v

## **📐 Diseño de la Base de Datos**

El diseño de la base de datos se adhiere a un modelo relacional y se implementa en MySQL. La estructura de las tablas, sus campos, claves primarias y foráneas, así como las restricciones de integridad, se definen en el script init.sql. El diseño busca la normalización para asegurar la integridad y consistencia de los datos, reflejando las entidades y relaciones descritas en la consigna.

### **Tablas Principales:**

* login: Almacena las credenciales de los usuarios del sistema y su rol (es\_administrador).  
* proveedores: Contiene la información de los proveedores de insumos.  
* insumos: Detalla los diferentes tipos de insumos (café, leche, chocolate, etc.), su precio unitario y proveedor.  
* clientes: Guarda los datos de los clientes donde se instalan las máquinas.  
* maquinas: Registra las máquinas expendedoras, su modelo, el cliente al que están asignadas, su ubicación específica y el costo de alquiler mensual.  
* registro\_consumo: Historial de uso de insumos por cada máquina en una fecha determinada.  
* tecnicos: Almacena la información de los técnicos de mantenimiento.  
* mantenimientos: Registra las intervenciones de mantenimiento realizadas en las máquinas, incluyendo el técnico asignado, tipo y fecha.

## **🌐 Estructura del Proyecto**

El proyecto está organizado de forma modular para facilitar la mantenibilidad y escalabilidad:

```
├── app/  
│   ├── api/                   \# Contiene los routers de la API, organizados por versión y endpoint.  
│   │   ├── v1/  
│   │   │   └── endpoints/  
│   │   │       ├── auth.py    \# Endpoint de autenticación (login).  
│   │   │       ├── clientes.py \# Endpoints CRUD para clientes.  
│   │   │       ├── insumos.py  \# Endpoints CRUD para insumos.  
│   │   │       ├── maquinas.py \# Endpoints CRUD para máquinas.  
│   │   │       ├── mantenimientos.py \# Endpoints CRUD para mantenimientos.  
│   │   │       ├── proveedores.py \# Endpoints CRUD para proveedores.  
│   │   │       ├── registros\_consumo.py \# Endpoints CRUD para registros de consumo.  
│   │   │       └── tecnicos.py \# Endpoints CRUD para técnicos.  
│   ├── config.py              \# Centraliza las configuraciones de la aplicación (DB, JWT, etc.).  
│   ├── crud/                  \# Contiene las funciones para las operaciones CRUD directas a la base de datos (SQL puro).  
│   │   └── (archivos por entidad, ej. login.py, cliente.py, insumo.py)  
│   ├── database.py            \# Gestión de la conexión a la base de datos MySQL.  
│   ├── dependencies.py        \# Funciones de dependencia de FastAPI (ej. obtener conexión DB, verificar token).  
│   ├── main.py                \# Punto de entrada principal de la aplicación FastAPI, donde se registran los routers.  
│   ├── schemas/               \# Define los modelos Pydantic para la validación de entrada y serialización de salida de la API.  
│   │   ├── common.py          \# Schemas genéricos de respuesta (APIResponse, ErrorDetail, MessageResponse).  
│   │   └── (archivos por entidad, ej. login.py, cliente.py, insumo.py)  
│   └── utils/                 \# Contiene utilidades varias (ej. auth\_utils.py para JWT y hashing de contraseñas).  
├── .env                       \# Archivo para las variables de entorno (NO subir a Git).  
├── .dockerignore              \# Define archivos y directorios a ignorar al construir la imagen Docker.  
├── Dockerfile                 \# Instrucciones para construir la imagen Docker de la aplicación.  
├── docker-compose.yml         \# Archivo de orquestación para definir y ejecutar los servicios (aplicación y base de datos).  
├── init.sql                   \# Script SQL para la creación inicial de la base de datos y datos maestros.  
├── requirements.txt           \# Lista las dependencias de Python del proyecto.  
├── tests/                     \# Directorio para las pruebas unitarias y de integración (a implementar).  
└── README.md                  \# Este archivo de documentación.
```

## **💡 Mejoras y Extensiones Propuestas**

Para futuras fases de desarrollo, se proponen las siguientes mejoras y extensiones:

* **Sistema de Autorización Completo:** Implementar la validación y decodificación de JWT en los endpoints protegidos para asegurar que solo usuarios autenticados y con el rol adecuado (ej. es\_administrador) puedan acceder a ciertas funcionalidades. Esto se logrará mediante dependencias de FastAPI.  
* **Pool de Conexiones a Base de Datos:** Para entornos de producción, implementar un pool de conexiones a la base de datos para manejar eficientemente la concurrencia y el rendimiento de las solicitudes.  
* **Tests Unitarios e Integración:** Desarrollar un conjunto robusto de pruebas unitarias y de integración utilizando pytest para asegurar la calidad y el correcto funcionamiento de la API.  
* **Manejo de Errores Detallado:** Ampliar los códigos de error y los mensajes de las respuestas para ofrecer un feedback más específico y útil a los clientes de la API.  
* **Contraseñas Seguras:** Asegurar que el proceso de alta de usuarios (ABM de login) siempre hashee las contraseñas antes de almacenarlas en la base de datos, y que la función de login las verifique correctamente.  
* **Logging:** Implementar un sistema de logging estructurado para el monitoreo de la aplicación en producción, facilitando la depuración y el análisis de rendimiento.  
* **Rate Limiting:** Añadir límites de tasa a los endpoints para prevenir abusos y ataques de fuerza bruta.  
* **Interfaz Frontend:** Desarrollar una interfaz de usuario web o móvil (utilizando un framework libre como React, Angular, Vue.js, etc.) que consuma esta API para ofrecer una experiencia completa al usuario final.

## **📅 Bitácora de Trabajo**

*(Esta sección debe ser completada por los integrantes del grupo. Detalla las fechas, tareas realizadas, decisiones clave, problemas encontrados y sus soluciones, y cualquier otro hito relevante del proyecto.)*

## **📚 Bibliografía**

* Documentación Oficial de FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)  
* Documentación Oficial de Pydantic: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)  
* Documentación Oficial de Docker: [https://docs.docker.com/](https://docs.docker.com/)  
* Documentación Oficial de MySQL: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)  
* Librería python-jose (para JWT): [https://python-jose.readthedocs.io/](https://python-jose.readthedocs.io/)  
* Librería passlib (para hashing de contraseñas): [https://passlib.readthedocs.io/](https://passlib.readthedocs.io/)

**Desarrollado por:**

* \[Felipe Cabrera\]  
