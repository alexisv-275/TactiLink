# Introducción al Sistema 

El sistema TactiLink es una herramienta web diseñada para transcribir textos del español al sistema de lectoescritura Braille y generar señalética lista para la impresión vectorial. Su objetivo principal es facilitar la creación de material accesible para personas con discapacidad visual.

# Guía de Uso

Para usar TactiLink, solo necesita un navegador web actualizado (como Chrome, Firefox, o Edge).

## Enlace de Acceso: 
Abra su navegador y diríjase a la dirección de la aplicación.
Si está usando la versión de desarrollo local: http://localhost
## Interfaz:
La pantalla principal mostrará un área de entrada de texto y dos botones principales.

<img width="764" height="603" alt="imagen" src="https://github.com/user-attachments/assets/c40d7e2b-4eaf-4b02-b240-bc2b37a64bed" />

La aplicación ofrece dos funciones principales: Transcribir (obtener el código de puntos) y Generar Señalética (obtener el archivo vectorial SVG).

### Transcribir a Código Braille

Esta es la función para obtener la secuencia de números que representan los puntos Braille (ej. 1 12 145).
1. Escribe el texto en español que necesites.
2. Presiona el botón "Transcribir" (el botón verde).
3. El resultado aparecerá justo debajo, mostrando el código de puntos para cada letra o signo.

### Generar Señalética SVG
Esta función crea el archivo de imagen vectorial que necesitas para mandar a imprimir o fabricar la señalética.
1. Asegúrate de que el texto deseado esté en la caja de entrada.
2. Presiona el botón "Generar Señalética" (el botón azul).
3. El sistema procesará el texto, creará la imagen vectorial y tu navegador descargará automáticamente el archivo .svg.



