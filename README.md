# 🔤 TactiLink

<div align="center">
  
**Sistema de Transcripción Bidireccional Texto ↔ Braille**


[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?logo=nginx&logoColor=white)](https://nginx.org/)

</div>

---

## 📋 Contenidos

- [El Problema](#-el-problema)
- [Diseño del Sistema](#%EF%B8%8F-diseño-del-sistema)
- [Flujo de datos](#flujo-de-datos)
- [Decisiones Técnicas y Trade-offs](#-decisiones-técnicas-y-trade-offs)
- [Instalación y Uso](#-instalación-y-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
---

## 🎯 El Problema

En el mundo actual, **más de 39 millones de personas son ciegas** y **246 millones tienen discapacidad visual moderada o grave** (OMS, 2021). La señalética en espacios públicos, documentos educativos y materiales informativos siguen siendo predominantemente visuales, creando barreras de acceso sistemáticas.

La producción de material en Braille es costosa, requiere hardware especializado y conocimiento técnico específico. Los diseñadores gráficos y educadores necesitan iterar constantemente entre prototipos físicos para validar señalética accesible, incrementando tiempos y costos.

**TactiLink elimina esta fricción** ofreciendo una plataforma web que permite convertir texto español a código Braille de forma instantánea, generar archivos SVG listos para impresión 3D o grabado láser, y previsualizar el resultado sin necesidad de producción física previa. Así, cualquier persona —desde un estudiante hasta un profesional de diseño— puede crear contenido inclusivo en minutos, no en días.

---

## 🏗️ Diseño del Sistema

### Arquitectura General

<img width="2567" height="1184" alt="ArqTactiLink" src="https://github.com/user-attachments/assets/6e243054-0183-44b4-96ca-2329260d949e" />

*Diagrama mostrando la comunicación entre Frontend, Nginx, Backend, Red Docker y Cliente*

### Flujo de Datos

El sistema implementa una arquitectura de **microservicios containerizados** con separación clara de responsabilidades:

| Etapa | Componente | Acción | Protocolo/Tecnología |
|-------|-----------|--------|---------------------|
| **1. Entrada del Usuario** | Frontend (Navegador) | Usuario ingresa texto en español o código Braille | JavaScript (DOM Events) |
| **2. Solicitud HTTP** | Frontend → Nginx | `POST /api/transcribe` con payload JSON | HTTP/1.1, Content-Type: application/json |
| **3. Reverse Proxy** | Nginx → Backend | Reenvío de petición a `http://backend:5000/api/transcribe` | Proxy Pass, DNS interno Docker |
| **4. Procesamiento** | Backend (Flask) | Mapeo de caracteres usando diccionarios predefinidos según estándar Braille español | Python, Algoritmo de transcripción |
| **5. Generación SVG** | Backend | Construcción de archivo SVG con puntos Braille posicionados matemáticamente | svgwrite library |
| **6. Respuesta** | Backend → Nginx → Frontend | JSON con texto convertido y SVG en base64 | HTTP Response 200 OK |
| **7. Renderizado** | Frontend | Actualización dinámica del DOM, previsualización SVG y habilitación de descarga | JavaScript, Blob API |

**Características clave del flujo:**
- **Comunicación asíncrona**: `fetch API` con manejo de errores robusto
- **Debouncing**: Evita solicitudes excesivas durante escritura continua (500ms)
- **Validación bidireccional**: Tanto frontend como backend validan formatos de entrada
- **Health checks**: Docker monitorea la salud del backend cada 30 segundos

---

## 🧠 Decisiones Técnicas y Trade-offs

### 1️⃣ **Containerización con Docker vs Despliegue Tradicional**

**Decisión:** Implementar toda la infraestructura con Docker Compose.

**Contexto:**
La alternativa era un despliegue tradicional instalando Python, Nginx y dependencias directamente en el sistema operativo host.

**Por qué Docker:**

| Ventaja | Impacto Real |
|---------|--------------|
| **Reproducibilidad absoluta** | Eliminación del "en mi máquina funciona". El mismo `docker-compose up` despliega idénticamente en Windows, macOS o Linux |
| **Aislamiento de dependencias** | Python 3.11-slim con Flask corre independiente de la versión de Python del sistema. Evita conflictos de librerías |
| **Ambientes idénticos Dev/Prod** | El Dockerfile garantiza que desarrollo, staging y producción usen exactamente las mismas versiones de librerías |

**Evidencia:**
```yaml
# Un solo comando despliega todo el stack:
docker-compose up -d

# vs alternativa tradicional que requeriría:
# - Instalar Python 3.11
# - Crear virtualenv
# - pip install requirements
# - Configurar systemd/supervisor
# - Instalar Nginx
# - Configurar nginx.conf manualmente
# - Gestionar logs en múltiples ubicaciones
