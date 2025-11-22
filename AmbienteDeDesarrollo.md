# Flujo de Trabajo del Proyecto

Este documento define las herramientas y la metodología de trabajo para el desarrollo del proyecto de transcripción a Braille.

## 1. Herramientas Seleccionadas

### Herramientas Generales

* **Editor de Código:** Visual Studio Code
* **Control de Versiones:** Git y GitHub
* **Contenerización:** Docker Desktop

### Stack Tecnológicos

* **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
* **Backend:** Python (con Flask o FastAPI)
* **Servidor:** Nginx (para servir estáticos en Docker)

## 2. Estrategia de Ramificación (Feature Branching)

Se utilizará una estrategia simple de *Feature Branching* para mantener la rama `main` limpia y estable.

### Ramas Principales

1.  **`main`**:
    * Esta rama refleja la versión estable y probada del código.
    * **REGLA:** Está **prohibido** realizar `git push` directamente a `main`. Todo el código debe integrarse a través de un *Pull Request*.

2.  **`documentacion`**:
    * Esta rama es independiente y contiene únicamente los entregables de documentación (Manuales, diagramas, casos de prueba, etc.).
    * **REGLA:** Esta rama **nunca** debe ser fusionada con `main`.

### Flujo de Trabajo para Nuevas Tareas

Todo el desarrollo se realiza en ramas `feature`.

1.  **Crear la Rama:** Antes de comenzar una nueva tarea (ej. "añadir números"), el desarrollador debe crear una nueva rama **basada en `main`**:
    ```bash
    # El desarrollador se sitúa en main y trae la última versión
    git checkout main
    git pull
    
    # Se crea la nueva rama de trabajo
    git checkout -b feature/traduccion-numeros
    ```

2.  **Trabajar y Hacer Commits:** El trabajo se realiza en la rama `feature/...` y se guardan los cambios con *commits* que tengan mensajes claros.
    ```bash
    git add .
    git commit -m "Agrega la lógica para transcribir dígitos del 1 al 9"
    ```

3.  **Subir la Rama:** El desarrollador sube su rama al repositorio remoto (GitHub).
    ```bash
    git push origin feature/traduccion-numeros
    ```

4.  **Crear Pull Request (PR):**
    * El desarrollador debe ir a GitHub y crear un **Pull Request (PR)** para fusionar su rama `feature/traduccion-numeros` en la rama `main`.
    * Se debe asignar a un compañero de equipo para que revise el código.

5.  **Revisar y Fusionar:**
    * El equipo revisa el código, las pruebas y deja comentarios.
    * Una vez aprobado, el PR se fusiona (merge) con `main`.
    * Después de la fusión, la rama `feature` puede ser eliminada.
