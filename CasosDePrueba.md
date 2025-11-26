# **Casos de Prueba \- Transcriptor Braille**

Este documento detalla los casos de prueba (CP) basados en los Requerimientos Generales (RG) del cliente, desglosados para asegurar la correcta implementación de la lógica de transcripción y el formato de señalética.

## **I. Desglose de Requerimientos**

| ID Requerimiento | Requerimiento General (RG) | Requerimiento Específico (RE) |
| :---- | :---- | :---- |
| **RG-1** | Transcribir textos de español a braille incluyendo números, abecedario, vocales acentuadas, y signos básicos. | **RE-1.1:** Transcribir la Primera Serie (a-j). |
|  |  | **RE-1.2:** Transcribir la Segunda Serie (k-t). |
|  |  | **RE-1.3:** Transcribir la Tercera Serie y Letras Adicionales (u, v, x, y, z, ñ, ü, w). |
|  |  | **RE-1.4:** Transcribir Vocales Acentuadas (á, é, í, ó, ú). |
|  |  | **RE-1.5:** Transcribir Números (0-9) Y signos bàsicos |
|  |  | **RE-1.6:** Transcribir Signos Adicionales y mayùsuclas. |
| **RG-2** | Generar señalética Braille a partir de textos en español. |  |


## **II. Casos de Prueba**

### **A. Pruebas de Transcripción (RG-1)**

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.1.01 |
| **Requisito Asociado** | RE-1.1: Transcribir la Primera Serie (a-j) |
| **Objetivo** | Verificar la transcripción de toda la Primera Serie (a a j). |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1. Ingresar la cadena abcdefghij. 2. Presionar "Transcribir" |
| **Resultado Esperado** | Representación Braille esperada (separada por espacios): 1 12 14 145 15 124 1245 125 24 245 |
| **Resultado Obtenido** | 1 12 14 145 15 124 1245 125 24 245 | 
| **Estado** | PASSED  |
| **Análisis (Si Falla)** |  | 



| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.2.01 |
| **Requisito Asociado** | RE-1.2: Transcribir la Segunda Serie (k-t) |
| **Objetivo** | Verificar la transcripción de toda la Segunda Serie (k a t). |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1. Ingresar la cadena klmnopqrst. 2. Presionar "Transcribir". |
| **Resultado Esperado** | Representación Braille esperada: 13 123 134 1345 135 1234 12345 1235 234 2345 |
| **Resultado Obtenido** | 13 123 134 1345 135 1234 12345 1235 234 2345 |
| **Estado** | PASSED | 
| **Análisis (Si Falla)** |  |


| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.3.01 |
| **Requisito Asociado** | RE-1.3: Transcribir la Tercera Serie y Letras Adicionales |
| **Objetivo** | Verificar la transcripción de u, v, x, y, z, ñ, ü, w. |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** |1. Ingresar la cadena uvxyzñüw. 2. Presionar "Transcribir".|
| **Resultado Esperado** | Representación Braille esperada: 136 1236 1346 13456 1356 12456 2456 2346|
| **Resultado Obtenido** | 136 1236 1346 13456 1356 12456 2456 2346 |
| **Estado** | PASSED |
| **Análisis (Si Falla)** |  |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.4.01 |
| **Requisito Asociado** | RE-1.4: Transcribir Vocales Acentuadas |
| **Objetivo** | Verificar la transcripción de todas las vocales acentuadas. |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1. Ingresar la cadena áéíóú. 2. Presionar "Transcribir". |
| **Resultado Esperado** | Representación Braille esperada: 1 2 34 12356 2346 |
| **Resultado Obtenido** | 1 2 34 12356 2346 |
| **Estado** | PASSED |
| **Análisis (Si Falla)** |  |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.5.01 |
| **Requisito Asociado** | RE-1.5: Transcribir Números (0-9) |
| **Objetivo** | Verificar una secuencia numérica ('0123456789'), donde el signo solo se pone al inicio. |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1. Ingresar la cadena 0123456789. 2. Presionar "Transcribir". |
| **Resultado Esperado** | Representación Braille esperada: # 245 1 12 14 145 15 124 1245 125 24|
| **Resultado Obtenido** | # 245 1 12 14 145 15 124 1245 125 24 |  
| **Estado** | PASSED |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.5.02 |
| **Requisito Asociado** | RE-1.5: Transcribir Signos Básicos |
| **Objetivo** | Verificar la transcripción de la coma (,) y el punto (.) en contexto textual y numérico. |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | **Textual** 1.Ingresar el texto Hola, mundo. 2.Presionar el botón "Transcribir".**Numérico** 1. Ingresar la cadena 2.329,724. 2. Presionar "Transcribir". |
| **Resultado Esperado** | Representación Braille esperada: **Textual**  125 135 123 1 2 134 136 1345 145 135 3 **Numérico** #12 3 145 12 145 2 1245 12 145 3|
| **Resultado Obtenido** | **Textual:** 6 125 135 123 1 2   134 136 1345 145 135 3 **Numérica:** # 12 3 14 12 24 2 1245 12 145 3 |
| **Estado** | PASSED |
| **Análisis (Si Falla)** |  |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.6.06 |
| **Requisito Asociado** | RE-1.6: Transcribir Signos Adicionales|
| **Objetivo** | Verificar la transcripción correcta de signos adicionales|
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar: ;:_""!¡¿?()+x=÷- 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille: 23 25 456 456 2356 235 2356 235 2356 235 2356 235 26 |
| **Resultado Obtenido** | 23 25 456 456 2356 235 2356 235 2356 235 2356 235 26 2356 26 5 126 5 346 346 5 236 2356 2356 256 256 1346 2356 256 36 | 
| **Estado** | PASSED |
| **Análisis (Si Falla)** |  |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.6.07 |
| **Requisito Asociado** | RE-1.6: Transcribir Signos Adicionales |
| **Objetivo** | Verificar la transcripción correcta de una mayúscula ('A'). |
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar el texto **A**. 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille (Signo de Mayúscula \+ Letra a): **6** seguido de **1**. |
| **Resultado Obtenido** | 6 1 |
| **Estado** | PASSED |
| **Análisis (Si Falla)** |  |

### **B. Pruebas de Generación de Señalética (RG-2)**

Estos casos verifican la correcta salida de datos en formato vectorial (SVG) para la impresión de señalética, asumiendo que el Frontend/API se encargará de esto.

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-2.1.01 |
| **Requisito Asociado** | RG-2: Generar señalética Braille a partir de textos en español.|
| **Objetivo** | Verificar la generación exitosa de una imagen vectorial (SVG). |
| **Precondiciones** | El servicio de generación de señalética (/api/generar_senaletica) y la lógica de transcripción están activos. |
| **Pasos de Ejecución** | 1. Enviar una solicitud al endpoint de generación de señalética con el texto "2". 2. El sistema devuelve una respuesta al navegador para descargar o mostrar el archivo. 3. Verificar los encabezados y el contenido de la respuesta. 4. Ampliar visualmente el archivo SVG generado. |
| **Resultado Esperado** | 1. La respuesta debe tener el encabezado Content-Type: image/svg+xml. 2. El archivo descargado debe ser un SVG válido que contenga la representación del número 2 (es decir, el signo de número # seguido de la letra b: #12). 3. Al ampliar el SVG, los elementos gráficos (círculos y texto en tinta) deben permanecer nítidos (no pixelados). |
| **Resultado Obtenido** | senaletica_braile_2.svg |
| **Estado** | PASSED |
| **Análisis (Si Falla)** |  |


