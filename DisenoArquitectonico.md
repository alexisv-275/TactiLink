# Diseño Arquitectónico

El diseño arquitectónico es de dos contenedores desacoplados (Frontend y Backend) que se comunican dentro de una red Docker a la cual llamamos "net-tactilink".
Los cuales se detallan a continuación:

### Contenedor Frontend (Nginx)
Actúa como punto de entrada y servidor de archivos estáticos. Está expuesto al Host en el puerto 80.

### Contenedor Backend(Flask)
Contiene la lógica central de transcripción y genera los datos Braille. Escucha peticiones internamente en el puerto 5000.

El Nginx reenvía (proxy_pass) todas las peticiones de API (/api/*) a la dirección interna del servicio backend:5000. 

A continuación se muestra el diagrama para que quede más claro: 

<img width="870" height="543" alt="imagen" src="https://github.com/user-attachments/assets/43836261-91e4-497d-ae0b-d747d8111d5d" />

