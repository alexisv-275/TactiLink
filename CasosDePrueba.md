# **Casos de Prueba \- Transcriptor Braille**

Este documento detalla los casos de prueba (CP) basados en los Requerimientos Generales (RG) del cliente, desglosados para asegurar la correcta implementación de la lógica de transcripción y el formato de señalética.

## **I. Desglose de Requerimientos**

| ID Requerimiento | Requerimiento General (RG) | Requerimiento Específico (RE) |
| :---- | :---- | :---- |
| **RG-1** | Transcribir textos de español a braille incluyendo números, abecedario, vocales acentuadas, y signos básicos. | **RE-1.1:** Transcribir la Primera Serie (a-j). |
|  |  | **RE-1.2:** Transcribir la Segunda Serie (k-t). |
|  |  | **RE-1.3:** Transcribir la Tercera Serie y Letras Adicionales (u, v, x, y, z, ñ, ü, w). |
|  |  | **RE-1.4:** Transcribir Vocales Acentuadas (á, é, í, ó, ú). |
|  |  | **RE-1.5:** Transcribir Números (0-9) con el signo de número. |
|  |  | **RE-1.6:** Transcribir Signos Básicos (punto, coma, mayúscula). |
| **RG-2** | Generar señalética Braille a partir de textos en español. | **RE-2.1:** Generar una imagen vectorial (SVG) del Braille con dimensiones escalables. |
|  |  | **RE-2.2:** Asegurar que el formato de salida sea una imagen vectorial de alta calidad. |




## **II. Casos de Prueba**

### **A. Pruebas de Transcripción (RG-1)**

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.1.01 |
| **Requisito Asociado** | RE-1.1: Transcribir la Primera Serie (a-j) |
| **Objetivo** | Verificar la transcripción correcta de la letra 'e'. |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar el carácter minúscula **e**. 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille: **15**. |
| **Resultado Obtenido** |  |
| **Estado** |  |
| **Análisis (Si Falla)** |  |
| **ID del Caso** | CP-1.2.02 |
| **Requisito Asociado** | RE-1.2: Transcribir la Segunda Serie (k-t) |
| **Objetivo** | Verificar la transcripción correcta de la letra 'm'. |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar el carácter minúscula **m**. 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille: **134**. |
| **Resultado Obtenido** |  |
| **Estado** |  |
| **Análisis (Si Falla)** |  |
| **ID del Caso** | CP-1.3.03 |
| **Requisito Asociado** | RE-1.3: Transcribir la Tercera Serie y Letras Adicionales |
| **Objetivo** | Verificar la transcripción correcta de la letra 'ñ'. |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar el carácter minúscula **ñ**. 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille: **12456**. |
| **Resultado Obtenido** |  |
| **Estado** |  |
| **Análisis (Si Falla)** |  |
| **ID del Caso** | CP-1.4.04 |
| **Requisito Asociado** | RE-1.4: Transcribir Vocales Acentuadas |
| **Objetivo** | Verificar la transcripción correcta de la vocal acentuada 'í'. |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar el carácter **í**. 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille: **34**. |
| **Resultado Obtenido** |  |
| **Estado** |  |
| **Análisis (Si Falla)** |  |
| **ID del Caso** | CP-1.5.05 |
| **Requisito Asociado** | RE-1.5: Transcribir Números (0-9) |
| **Objetivo** | Verificar la transcripción correcta del número '7' con el signo numérico. |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar el número **7**. 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille (Signo de Número \+ Letra g): **\#1245** |
| **Resultado Obtenido** |  |
| **Estado** |  |
| **Análisis (Si Falla)** |  |
| **ID del Caso** | CP-1.6.06 |
| **Requisito Asociado** | RE-1.6: Transcribir Signos Básicos |
| **Objetivo** | Verificar la transcripción de la coma (,) y el punto (.). |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar el texto **,.**. 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille: **2** seguido de **256**. |
| **Resultado Obtenido** |  |
| **Estado** |  |
| **Análisis (Si Falla)** |  |
| **ID del Caso** | CP-1.6.07 |
| **Requisito Asociado** | RE-1.6: Transcribir Signos Básicos |
| **Objetivo** | Verificar la transcripción correcta de una mayúscula ('A'). |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar el texto **A**. 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille (Signo de Mayúscula \+ Letra a): **6** seguido de **1**. |
| **Resultado Obtenido** |  |
| **Estado** |  |
| **Análisis (Si Falla)** |  |

### **B. Pruebas de Generación de Señalética (RG-2)**

Estos casos verifican la correcta salida de datos en formato vectorial (SVG) para la impresión de señalética, asumiendo que el Frontend/API se encargará de esto.

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-2.1.01 |
| **Requisito Asociado** | RE-2.1: Generar una imagen vectorial (SVG) |
| **Objetivo** | Verificar que la API responda con un formato SVG al solicitar señalética. |
| **Precondiciones** | El servicio de generación de señalética (/api/generar\_senaletica) está activo. |
| **Pasos de Ejecución** | 1\. Enviar una solicitud POST al endpoint /api/generar\_senaletica con el texto "hola". 2\. Verificar los encabezados de la respuesta. |
| **Resultado Esperado** | La respuesta debe tener el encabezado Content-Type: image/svg+xml. |
| **Resultado Obtenido** |  |
| **Estado** |  |
| **Análisis (Si Falla)** |  |
| **ID del Caso** | CP-2.2.02 |
| **Requisito Asociado** | RE-2.2: Asegurar el formato de alta calidad (escalabilidad) |
| **Objetivo** | Verificar que el contenido SVG generado sea correcto y contenga todos los puntos Braille para una palabra simple. |
| **Precondiciones** | El servicio de generación de señalética está activo. |
| **Pasos de Ejecución** | 1\. Enviar una solicitud con el texto **b**. 2\. Verificar el cuerpo de la respuesta. |
| **Resultado Esperado** | El cuerpo de la respuesta SVG debe contener una etiqueta de imagen/dibujo (ej., \<circle\> o \<path\>) para los puntos **1** y **2** (correspondientes a la 'b') y el texto en tinta 'b'. |
| **Resultado Obtenido** |  |
| **Estado** |  |
| **Análisis (Si Falla)** |  |

