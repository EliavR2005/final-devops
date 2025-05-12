# final-devops

Este es mi proyecto final de DevOps para la materia Fundamentos de DevOps en Universidad Tecmilenio.  
Aquí encontrarás la aplicación **SecureApp**, un sistema de gestión de usuarios con:

- **Backend** en Python y Flask  
- **Base de datos** MySQL con información cifrada (cryptography.fernet)  
- **Autenticación y roles** (Flask-Login)  
- **Monitorización** con Prometheus y Grafana en Docker  
- **Infrastructure as Code** con Docker Compose  

---

## Estructura del repositorio

- `app.py` – Código principal de Flask  
- `encrypt_utils.py` / `key_manager.py` – Cifrado y manejo de claves  
- `prometheus.yml` / `docker-compose.monitor.yml` – Configuración de Prometheus y Grafana  
- `templates/` & `static/` – Frontend (HTML, CSS)  
- `schema.sql` – Definición de la base de datos  
- `.gitignore` – Excluye archivos sensibles (.env, cachés, IDE settings)  

---

## Cómo ejecutar

1. Clona el repositorio  
   ```bash
   git clone https://github.com/EliavR2005/final-devops.git
   cd final-devops
