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
| **RG-3** | Implementar transcripción inversa de Braille a texto español. | **RE-3.1:** Validar entrada en formato Braille (números de puntos). |
|  |  | **RE-3.2:** Mapear representación Braille a caracteres en español. |
| **RG-4** | Generar SVG en modo espejo para escritura manual Braille. | **RE-4.1:** Invertir horizontalmente el SVG generado. |
|  |  | **RE-4.2:** Proporcionar opción de descarga para escritura manual. |


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
| **Resultado Esperado** | Representación Braille esperada: **Textual**  125 135 123 1 2 134 136 1345 145 135 3 **Numérico** # 12 3 14 12 24 2 1245 12 145 3|
| **Resultado Obtenido** | **Textual:** 125 135 123 1 2   134 136 1345 145 135 3 **Numérica:** # 12 3 14 12 24 2 1245 12 145 3 |
| **Estado** | PASSED |
| **Análisis (Si Falla)** |  |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-1.6.06 |
| **Requisito Asociado** | RE-1.6: Transcribir Signos Adicionales|
| **Objetivo** | Verificar la transcripción correcta de signos adicionales|
| **Precondiciones** | El servicio de transcripción está activo. |
| **Pasos de Ejecución** | 1\. Ingresar: ;:_""!¡¿?()+x=÷- 2\. Presionar el botón "Transcribir". |
| **Resultado Esperado** | La aplicación debe devolver la representación Braille: 23 25 456 456 2356 235 2356 235 2356 235 2356 235 26 2356 26 5 126 5 346 346 5 236 2356 2356 256 256 1346 2356 256 36 |
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

### **C. Pruebas de Transcripción Inversa (RG-3)**

Estos casos verifican la funcionalidad de conversión de Braille a texto español.

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-3.1.01 |
| **Requisito Asociado** | RE-3.1: Validar entrada en formato Braille |
| **Objetivo** | Verificar que el sistema rechaza entradas inválidas de Braille. |
| **Precondiciones** | El servicio de transcripción inversa (/api/reverse-transcribe) está activo. |
| **Pasos de Ejecución** | 1. Ingresar una cadena con formato inválido (ej: "abc" en lugar de números de puntos). 2. Presionar "Transcribir a Texto". |
| **Resultado Esperado** | El sistema devuelve un mensaje de error indicando que el formato de entrada no es válido. |
| **Resultado Obtenido** |  |
| **Estado** | PENDING |
| **Análisis (Si Falla)** |  |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-3.2.01 |
| **Requisito Asociado** | RE-3.2: Mapear representación Braille a caracteres en español |
| **Objetivo** | Verificar la transcripción inversa de Braille a texto incluyendo letras, mayúsculas y vocales acentuadas. |
| **Precondiciones** | El servicio de transcripción inversa está activo. |
| **Pasos de Ejecución** | 1. Ingresar la secuencia Braille: 1 12 14 145 15 124 1245 125 24 245 6 1 12356 2 34. 2. Presionar "Transcribir a Texto". |
| **Resultado Esperado** | El sistema devuelve el texto: abcdefghij Aóéí |
| **Resultado Obtenido** |  |
| **Estado** | PENDING |
| **Análisis (Si Falla)** |  |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-3.2.02 |
| **Requisito Asociado** | RE-3.2: Mapear representación Braille a caracteres en español |
| **Objetivo** | Verificar la transcripción inversa del mapeo de números y signos básicos. |
| **Precondiciones** | El servicio de transcripción inversa está activo. |
| **Pasos de Ejecución** | 1. Ingresar la secuencia Braille: # 1 12 14 2 3. 2. Presionar "Transcribir a Texto". |
| **Resultado Esperado** | El sistema devuelve el texto: 123,. |
| **Resultado Obtenido** |  |
| **Estado** | PENDING |
| **Análisis (Si Falla)** |  |

### **D. Pruebas de SVG en Modo Espejo (RG-4)**

Estos casos verifican la generación correcta de SVG invertido para escritura manual Braille.

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-4.1.01 |
| **Requisito Asociado** | RE-4.1: Invertir horizontalmente el SVG generado |
| **Objetivo** | Verificar que el SVG se genera con transformación espejo (lectura de derecha a izquierda). |
| **Precondiciones** | El servicio de generación de señalética en modo espejo está activo. |
| **Pasos de Ejecución** | 1. Ingresar el texto "abc". 2. Seleccionar opción "Modo escritura manual". 3. Presionar "Generar SVG". 4. Verificar el contenido del SVG generado. |
| **Resultado Esperado** | El archivo SVG debe contener la transformación transform="scale(-1, 1)" o las coordenadas X deben estar invertidas. La secuencia visual debe mostrar los caracteres de derecha a izquierda. |
| **Resultado Obtenido** |  |
| **Estado** | PENDING |
| **Análisis (Si Falla)** |  |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-4.2.01 |
| **Requisito Asociado** | RE-4.2: Proporcionar opción de descarga para escritura manual |
| **Objetivo** | Verificar que el botón de descarga para escritura manual funciona correctamente. |
| **Precondiciones** | La interfaz con el botón "Descargar para escritura manual" está implementada. |
| **Pasos de Ejecución** | 1. Ingresar el texto "Hola". 2. Presionar el botón "Descargar para escritura manual". 3. Verificar que se descarga el archivo. |
| **Resultado Esperado** | Se descarga un archivo SVG con nombre que indique el modo espejo (ej: senaletica_braille_Hola_espejo.svg). El archivo debe ser válido y contener la representación invertida. |
| **Resultado Obtenido** |  |
| **Estado** | PENDING |
| **Análisis (Si Falla)** |  |

| Componente | Detalle |
| :---- | :---- |
| **ID del Caso** | CP-4.2.02 |
| **Requisito Asociado** | RE-4.2: Proporcionar opción de descarga para escritura manual |
| **Objetivo** | Verificar que el SVG en modo espejo mantiene la calidad vectorial al ampliar. |
| **Precondiciones** | Se ha generado y descargado un SVG en modo espejo. |
| **Pasos de Ejecución** | 1. Abrir el archivo SVG descargado en un visor o navegador. 2. Ampliar la visualización al 300% o más. 3. Inspeccionar la nitidez de los círculos y texto en tinta. |
| **Resultado Esperado** | Los elementos gráficos (círculos Braille y texto) se mantienen nítidos sin pixelación, confirmando la naturaleza vectorial del archivo. |
| **Resultado Obtenido** |  |
| **Estado** | PENDING |
| **Análisis (Si Falla)** |  |


