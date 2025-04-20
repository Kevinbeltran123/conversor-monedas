# Conversor de Monedas Multicontenedor

**Proyecto 03 – Infraestructura y Seguridad Computacional**

Una aplicación multicontenedor que convierte montos de una moneda a otra, orquestada con **Docker Compose** y publicada en **Docker Hub**.

---

## Descripción

Este sistema está compuesto por varios microservicios:

- **API (Flask)**: recibe solicitudes de conversión, consulta cache y guarda el historial en PostgreSQL.
- **UI (Flask)**: interfaz web donde el usuario selecciona monedas y monto, y ve el resultado al instante.
- **Scraper de Tasas**: servicio que consulta cada minuto una API pública de tasas y las almacena en Redis.
- **PostgreSQL**: base de datos relacional que guarda el historial de conversiones.
- **Redis**: almacén en memoria donde se cachean las tasas de cambio para respuestas rápidas.

Todo está conectado a través de la red Docker `app_net` y persiste datos de la BD en el volumen `pgdata`.

---

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/)
- Cuenta en [Docker Hub](https://hub.docker.com/)

---

## Estructura del Proyecto

```
conversor-monedas/
├── backend/          # API Flask
│   ├── Dockerfile
│   └── app.py
├── visualizador/     # UI Flask (Jinja)
│   ├── Dockerfile
│   ├── visual.py
│   └── templates/
│       └── index.html
├── procesador/       # Scraper de tasas
│   ├── Dockerfile
│   └── procesador.py
└── docker-compose.yml
```  

---

## Configuración de Puertos y Redes

| Servicio       | Puerto Host → Contenedor | Descripción                |
|----------------|--------------------------|----------------------------|
| API (backend)  | `5050:5000`              | Endpoints REST en Flask    |
| UI (visualizador) | `3000:5000`           | Formulario de conversión   |
| PostgreSQL     | `5432:5432`              | Base de datos relacional   |
| Redis          | `6379:6379`              | Cache de tasas             |

Todos los servicios comparten la red `app_net`, definida en el Compose.  
El volumen `pgdata` persiste los datos de PostgreSQL en `/var/lib/postgresql/data`.

---

## Uso Local (Build)

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Kevinbeltran123/conversor-monedas.git
   cd conversor-monedas
   ```
2. Construye y levanta los contenedores:
   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```
3. Abre en el navegador:
   - UI → `http://localhost:3000`
   - API → `http://localhost:5050`

---

## Despliegue desde Docker Hub

1. Ejecuta:
   ```bash
   docker-compose pull
   docker-compose up
   ```

Así se bajan las imágenes ya compiladas y se inicia todo en segundos.

---

## Repositorios en Docker Hub

- `kevinbelt/conversor_monedas_flask_ui-backend`  
- `kevinbelt/conversor_monedas_flask_ui-visualizador`  
- `kevinbelt/conversor_monedas_flask_ui-procesador`  


---

## Presentado a 

Ingeniero Carlos Andrés Díaz Santacruz, gracias por la guía en este proyecto.  
Equipo: Kevin Beltrán, Santiago Baena, Misael Gallo, Nelson Garzon, Carlos Bahamon.

---

## Nota sobre elaboración y referenciamiento

El contenido de este archivo README.md fue elaborado con apoyo de la herramienta de inteligencia artificial ChatGPT (OpenAI), basándose en los requisitos específicos del proyecto académico y bajo la supervisión del equipo desarrollador.