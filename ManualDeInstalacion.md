# Manual de Instalación (Ambiente de Desarrollo Local)

Este manual explica cómo poner a funcionar la aplicación TactiLink en tu computadora local usando Docker.

## 1. Requisitos Necesarios

Para que la instalación funcione sin problemas, debes tener estos programas instalados:

  - Git: Es necesario para poder descargar el código del repositorio (GitHub).

  - Docker Desktop: Es el software clave. Lo necesitamos para crear y correr los contenedores del Backend y Frontend.

  - Una Terminal o CMD: Para escribir los comandos.
    
## 2. Pasos de Instalación
Sigue estos cuatro pasos en tu terminal (CMD o terminal de VS Code):

### Paso 1: Obtener el Código

Abre tu terminal y navega hasta la carpeta donde guardas tus proyectos.

Usa el comando git clone seguido del enlace de tu repositorio para descargar el proyecto:

    Bash

    git clone [ENLACE_A_TU_REPOSITORIO_DE_GITHUB]

Entra a la carpeta del proyecto que acabas de descargar:

    Bash

    cd TactiLink

(Asegúrate de estar en la carpeta donde ves frontend, backend y docker-compose.yaml).

### Paso 2: Activar Docker Desktop

Abre la aplicación Docker Desktop en tu computadora y asegúrate de que esté ejecutándose (activa y lista para recibir comandos).

### Paso 3: Construir y Encender la Aplicación

Estando en la carpeta principal de TactiLink (del paso 1), ejecuta este comando. Esto hará todo el trabajo pesado: construirá los contenedores (Frontend y Backend) e instalará las librerías necesarias.

    Bash

    docker-compose up --build

### Paso 4: Verificación Final

Espera a que el comando termine de ejecutarse y veas que tanto el tactilink-backend como el tactilink-frontend están activos en la terminal.

Abre tu navegador web.

Escribe la dirección local para acceder a la interfaz:

    http://localhost
    
Si la página de transcripción carga, ¡la instalación ha sido un ÉXITO!
