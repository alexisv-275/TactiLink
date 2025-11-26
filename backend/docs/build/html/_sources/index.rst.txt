.. Tactilink documentation master file, created by
   sphinx-quickstart on Wed Nov 26 14:20:26 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentación Técnica de TactiLink
===================================

Bienvenido a la documentación técnica de **TactiLink**, un sistema de transcripción de texto a Braille y generación de señalética Braille en formato SVG.

Descripción General
-------------------

TactiLink proporciona una API REST que permite:

- **Transcripción de texto a Braille**: Convierte texto en español a código Braille numérico
- **Generación de señalética**: Crea representaciones visuales en SVG de señalética Braille con puntos táctiles
- **Soporte multilingüe**: Maneja caracteres especiales del español (acentos, ñ, etc.)
- **Contexto numérico**: Detecta y maneja automáticamente secuencias de números

Características Principales
---------------------------

✓ API REST basada en Flask
✓ Soporte para letras (a-z), números (0-9) y signos de puntuación
✓ Generación de SVG escalable para señalética Braille
✓ Endpoints de salud para monitoreo
✓ CORS habilitado para integración con frontend

Contenidos
----------

.. toctree::
   :maxdepth: 2
   :caption: Referencia Técnica:

   source/api

Inicio Rápido
-------------

Para usar la API:

1. **Transcribir texto a Braille**:

   .. code-block:: bash

      curl -X POST http://localhost:5000/api/transcribe \
        -H "Content-Type: application/json" \
        -d '{"text": "Hola"}'

2. **Generar señalética SVG**:

   .. code-block:: bash

      curl -X POST http://localhost:5000/api/generar_senaletica \
        -H "Content-Type: application/json" \
        -d '{"text": "Hola"}'

3. **Verificar salud del servicio**:

   .. code-block:: bash

      curl http://localhost:5000/health

Requisitos
----------

- Python 3.8+
- Flask
- Flask-CORS
- svgwrite

Instalación
-----------

.. code-block:: bash

   pip install -r requirements.txt
   python app.py

Índice
------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

