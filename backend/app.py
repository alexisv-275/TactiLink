"""Módulo principal de la API TactiLink para transcripción de texto a Braille.

Este módulo proporciona endpoints REST para convertir texto en español
a código Braille numérico y generar representaciones SVG de señalética Braille.

Attributes:
    BRAILLE_MAP (dict): Diccionario de mapeo de caracteres a código Braille numérico.
        Cada clave representa un carácter y su valor el código Braille correspondiente.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mapeo completo de caracteres a código Braille numérico
BRAILLE_MAP = {
    # Letras a-z
    'a': '1', 'b': '12', 'c': '14', 'd': '145', 'e': '15',
    'f': '124', 'g': '1245', 'h': '125', 'i': '24', 'j': '245',
    'k': '13', 'l': '123', 'm': '134', 'n': '1345', 'o': '135',
    'p': '1234', 'q': '12345', 'r': '1235', 's': '234', 't': '2345',
    'u': '136', 'v': '1236', 'w': '2456', 'x': '1346', 'y': '13456',
    'z': '1356',
    
    # Vocales acentuadas
    'á': '12356', 'é': '2346', 'í': '34', 'ó': '346', 'ú': '23456',
    'ü': '1256',
    
    # Ñ
    'ñ': '12456',
    
    # Números (precedidos por signo #) (CP-1.5.01)
    '#': '#',  # Indicador numérico
    '0': '245', '1': '1', '2': '12', '3': '14', '4': '145',
    '5': '15', '6': '124', '7': '1245', '8': '125', '9': '24',
    
    # Signos de puntuación básicos
    '.': '3',
    ',': '2',
    ';': '23',
    ':': '25',
    
    # Signos adicionales (CP-1.6.06)
    '_': '36',
    '"': '236',
    '!': '235', 
    '¡': '23456', 
    '¿': '2356',  
    '?': '26',  
    '(': '126',
    ')': '345', 
    '+': '235',   
    '=': '2356',  
    '÷': '256',   
    '-': '36',    
    
    # Espacio
    ' ': ' '
}

# Diccionario inverso para transcripción Braille → Texto
# Se construye una vez al iniciar el módulo para eficiencia
REVERSE_BRAILLE_MAP = {
    v: k for k, v in BRAILLE_MAP.items() 
    if k not in ['#', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and v not in ['#', ' ']
}

# Diccionario específico para números (después del prefijo #)
REVERSE_NUMBER_MAP = {
    '1': '1', '12': '2', '14': '3', '145': '4', '15': '5',
    '124': '6', '1245': '7', '125': '8', '24': '9', '245': '0'
}

# Códigos especiales que requieren secuencias



def es_numero(caracter: str) -> bool:
    """Verifica si un carácter es un dígito numérico."""
    return caracter.isdigit()


def generar_celda_braille_svg(codigo_braille: str, x: float, y: float) -> str:
    """Genera el SVG de una celda Braille con sus puntos correspondientes.

    Una celda Braille estándar tiene 6 posiciones de puntos organizadas en 
    dos columnas de 3 puntos cada una:
    
    Posiciones:  1  4
                 2  5
                 3  6

    Args:
        codigo_braille (str): Código numérico Braille (ej: '1', '12', '145', '#', '6').
        x (float): Coordenada X de inicio de la celda.
        y (float): Coordenada Y de inicio de la celda.

    Returns:
        str: Fragmento SVG con los círculos que representan los puntos activos.

    Examples:
        >>> generar_celda_braille_svg('1', 0, 0)
        # Retorna SVG con un círculo en posición 1
        >>> generar_celda_braille_svg('145', 10, 20)
        # Retorna SVG con círculos en posiciones 1, 4 y 5
    """
    # Mapeo de códigos especiales a sus representaciones numéricas
    codigos_especiales = {
        '#': '3456',  # Prefijo numérico
        '46': '46',   # Prefijo de mayúscula (puntos 4 y 6)
    }
    
    # Convertir códigos especiales a sus dígitos correspondientes
    if codigo_braille in codigos_especiales:
        codigo_braille = codigos_especiales[codigo_braille]
    
    # Dimensiones de la celda Braille estándar
    dot_radius = 3
    dot_spacing_horizontal = 10
    dot_spacing_vertical = 10
    
    # Posiciones de los 6 puntos en la celda Braille
    dot_positions = {
        '1': (x, y),
        '2': (x, y + dot_spacing_vertical),
        '3': (x, y + 2 * dot_spacing_vertical),
        '4': (x + dot_spacing_horizontal, y),
        '5': (x + dot_spacing_horizontal, y + dot_spacing_vertical),
        '6': (x + dot_spacing_horizontal, y + 2 * dot_spacing_vertical)
    }
    
    svg_circles = []
    
    # Dibujar todos los puntos en gris claro (inactivos)
    for pos in ['1', '2', '3', '4', '5', '6']:
        px, py = dot_positions[pos]
        svg_circles.append(f'<circle cx="{px}" cy="{py}" r="{dot_radius}" fill="#e0e0e0" stroke="#999" stroke-width="0.5"/>')
    
    # Dibujar puntos activos en negro
    for digit in codigo_braille:
        if digit in dot_positions:
            px, py = dot_positions[digit]
            svg_circles.append(f'<circle cx="{px}" cy="{py}" r="{dot_radius}" fill="#000"/>')
    
    return '\n        '.join(svg_circles)


def transcribir_character(character: str, anterior_es_numero: bool = False, 
                         siguiente_es_numero: bool = False) -> list:
    """Mapea un carácter individual a su representación en código Braille numérico.

    Args:
        character (str): Carácter a transcribir.
        anterior_es_numero (bool): Indica si el carácter anterior era un número.
        siguiente_es_numero (bool): Indica si el siguiente carácter es un número.

    Returns:
        list: Lista de códigos Braille para el carácter.
    """
    char_lower = character.lower()
    
    
    # Manejar números: agregar # solo antes del primer número de una secuencia
    if es_numero(char_lower):
        if not anterior_es_numero:
            # Primer número de la secuencia, agregar signo #
            return ['#', BRAILLE_MAP.get(char_lower, char_lower)]
        else:
            # Número subsecuente, no agregar #
            return [BRAILLE_MAP.get(char_lower, char_lower)]
    
    # Manejar 'x' en contexto numérico (multiplicación)
    if char_lower == 'x' and (anterior_es_numero or siguiente_es_numero):
        return ['236']  # Código especial para multiplicación en contexto numérico
    
    # Manejar punto y coma en contexto numérico
    if char_lower in '.,':
        # Si está entre números o después de un número, mantener en modo numérico
        if anterior_es_numero or siguiente_es_numero:
            return [BRAILLE_MAP.get(char_lower, char_lower)]
    
    # Manejar mayúsculas: agregar prefijo '46' antes de la letra
    if character.isalpha() and character.isupper():
        return ['46', BRAILLE_MAP.get(char_lower, char_lower)]
    
    # Caracteres normales
    return [BRAILLE_MAP.get(char_lower, char_lower)]

def transcribir_texto_completo(texto: str) -> str:
    """Transcribe una cadena de texto completa a código Braille numérico.

    Args:
        texto (str): Texto a transcribir.

    Returns:
        str: Cadena con códigos Braille separados por espacios.
    """
    resultado_braille = []
    
    for i, char in enumerate(texto):
        # Determinar contexto numérico considerando punto y coma
        anterior_es_numero = (i > 0 and (es_numero(texto[i-1]) or texto[i-1] in '.,'))
        siguiente_es_numero = (i < len(texto)-1 and (es_numero(texto[i+1]) or texto[i+1] in '.,'))
        
        # Transcribir carácter
        braille_codes = transcribir_character(char, anterior_es_numero, siguiente_es_numero)
        resultado_braille.extend(braille_codes)
    
    return ' '.join(resultado_braille)


def reverse_transcribe(braille_codes_str: str) -> str:
    """Transcribe código Braille numérico a texto español.

    Procesa una secuencia de códigos Braille y los convierte a texto,
    manejando prefijos especiales para mayúsculas (#46) y números (#).

    Args:
        braille_codes_str (str): Códigos Braille separados por espacios.
            Ejemplo: "46 125 135 123 1" o "# 12 14"

    Returns:
        str: Texto en español resultante de la transcripción inversa.

    Examples:
        >>> reverse_transcribe("125 135 123 1")
        'hola'
        
        >>> reverse_transcribe("46 125 135 123 1")
        'Hola'
        
        >>> reverse_transcribe("# 12 14")
        '23'
        
        >>> reverse_transcribe("46 125 135 123 1 2 134 136 1345 145 135 3")
        'Hola, mundo.'
    """
    codes = braille_codes_str.strip().split()
    resultado = []
    i = 0
    modo_numerico = False
    
    while i < len(codes):
        code = codes[i]
        
        # Detectar prefijo de mayúscula '46'
        if code == '46' and i + 1 < len(codes):
            next_code = codes[i + 1]
            char = REVERSE_BRAILLE_MAP.get(next_code, '?')
            if char != '?':
                resultado.append(char.upper())
            else:
                resultado.append('?')
            i += 2
            continue
        
        # Detectar prefijo numérico '#'
        if code == '#':
            modo_numerico = True
            i += 1
            continue
        
        # Si estamos en modo numérico
        if modo_numerico:
            # Verificar si el código es un número
            numero = REVERSE_NUMBER_MAP.get(code, None)
            if numero:
                resultado.append(numero)
                i += 1
                continue
            # Si no es número ni signo numérico, salir del modo numérico
            elif code not in ['2', '3']:  # coma y punto en contexto numérico
                modo_numerico = False
                # Procesar como carácter normal (caer al siguiente bloque)
            else:
                # Es un signo de puntuación en contexto numérico
                char = REVERSE_BRAILLE_MAP.get(code, '?')
                resultado.append(char)
                i += 1
                continue
        
        # Espacio
        if code == ' ':
            resultado.append(' ')
            i += 1
            continue
        
        # Carácter normal (letra o signo)
        char = REVERSE_BRAILLE_MAP.get(code, '?')
        resultado.append(char)
        i += 1
    
    return ''.join(resultado)



@app.route('/api/transcribe', methods=['POST'])
def transcribe_text():
    """Endpoint para transcripción de texto a código Braille numérico (RG-1).

    Recibe un JSON con el campo 'text' y devuelve su representación en
    código Braille numérico. Soporta letras (a-z), números (0-9) y signos
    básicos de puntuación (coma y punto) en contextos textuales y numéricos.

    Request JSON:
        text (str): Texto en español a transcribir. Puede contener letras,
            números, espacios y signos de puntuación (coma y punto).

    Returns:
        tuple: JSON response con los siguientes campos:
            - input (str): Texto original recibido.
            - braille_codes (str): Códigos Braille separados por espacios.
        
        Status code: 200 si es exitoso, 400 si no se proporciona texto.

    Raises:
        400: Si no se proporciona el campo 'text' en el JSON.

    Examples:
        Request:
            >>> {
            ...     "text": "hola"
            ... }

        Response:
            >>> {
            ...     "input": "hola",
            ...     "braille_codes": "125 135 123 1"
            ... }

        Request con signos básicos (contexto textual):
            >>> {
            ...     "text": "Hola, mundo."
            ... }

        Response:
            >>> {
            ...     "input": "Hola, mundo.",
            ...     "braille_codes": "6 125 135 123 1 2 134 136 1345 145 135 3"
            ... }

        Request con mayúscula:
            >>> {
            ...     "text": "A"
            ... }

        Response:
            >>> {
            ...     "input": "A",
            ...     "braille_codes": "6 1"
            ... }

        Request con números y signos (contexto numérico):
            >>> {
            ...     "text": "2.329,724"
            ... }

        Response:
            >>> {
            ...     "input": "2.329,724",
            ...     "braille_codes": "#12 3 14 12 145 2 1245 12 145"
            ... }
    """
    if not request.json or 'text' not in request.json:
        return jsonify({"error": "No se proporcionó texto de entrada."}), 400
    
    input_text = request.json['text']
    braille_output = transcribir_texto_completo(input_text)
    
    return jsonify({
        "input": request.json['text'],
        "braille_codes": braille_output
    })



@app.route('/api/reverse-transcribe', methods=['POST'])
def reverse_transcribe_text():
    """Endpoint para transcripción inversa de Braille a texto español (RG-3).

    Recibe un JSON con códigos Braille numéricos y devuelve el texto en español
    correspondiente. Soporta mayúsculas (prefijo 46), números (prefijo #),
    y todos los caracteres del BRAILLE_MAP.

    Request JSON:
        braille_codes (str): Códigos Braille separados por espacios.
            Ejemplo: "125 135 123 1" o "46 125 135 123 1"

    Returns:
        tuple: JSON response con los siguientes campos:
            - input (str): Códigos Braille originales recibidos.
            - spanish_text (str): Texto en español resultante.
        
        Status code: 200 si es exitoso, 400 si no se proporcionan códigos.

    Raises:
        400: Si no se proporciona el campo 'braille_codes' en el JSON.

    Examples:
        Request (texto simple):
            >>> {
            ...     "braille_codes": "125 135 123 1"
            ... }

        Response:
            >>> {
            ...     "input": "125 135 123 1",
            ...     "spanish_text": "hola"
            ... }

        Request (con mayúscula):
            >>> {
            ...     "braille_codes": "46 125 135 123 1"
            ... }

        Response:
            >>> {
            ...     "input": "46 125 135 123 1",
            ...     "spanish_text": "Hola"
            ... }

        Request (con números):
            >>> {
            ...     "braille_codes": "# 12 14"
            ... }

        Response:
            >>> {
            ...     "input": "# 12 14",
            ...     "spanish_text": "23"
            ... }

        Request (texto completo):
            >>> {
            ...     "braille_codes": "46 125 135 123 1 2 134 136 1345 145 135 3"
            ... }

        Response:
            >>> {
            ...     "input": "46 125 135 123 1 2 134 136 1345 145 135 3",
            ...     "spanish_text": "Hola, mundo."
            ... }
    """
    if not request.json or 'braille_codes' not in request.json:
        return jsonify({"error": "No se proporcionaron códigos Braille de entrada."}), 400
    
    braille_codes = request.json['braille_codes']
    spanish_output = reverse_transcribe(braille_codes)
    
    return jsonify({
        "input": braille_codes,
        "spanish_text": spanish_output
    })


@app.route('/api/generar_senaletica', methods=['POST'])
def generar_senaletica():
    """Endpoint para generación de señalética Braille en formato SVG (RG-2).

    Recibe un JSON con el campo 'text' y devuelve una representación
    visual SVG de la señalética Braille con puntos táctiles y texto en tinta.
    
    El SVG generado incluye:
    - Representación visual de celdas Braille con puntos activos e inactivos
    - Texto en tinta (texto original) encima de la representación Braille
    - Formato vectorial escalable sin pérdida de calidad

    Request JSON:
        text (str): Texto a convertir en señalética. Soporta letras, números,
            mayúsculas y signos básicos (coma y punto).

    Returns:
        flask.Response: Documento SVG con la representación visual de la 
            señalética Braille. Content-Type: image/svg+xml.

    Examples:
        Request:
            >>> {
            ...     "text": "2"
            ... }

        Response (SVG):
            <svg width="..." height="..." viewBox="..." xmlns="http://www.w3.org/2000/svg">
                <!-- Texto en tinta -->
                <text>2</text>
                <!-- Representación Braille del prefijo numérico # -->
                <circle .../> <!-- Puntos para # -->
                <!-- Representación Braille del número 2 -->
                <circle .../> <!-- Puntos para 2 (código 12) -->
            </svg>

        Request:
            >>> {
            ...     "text": "Hola"
            ... }

        Response (SVG):
            SVG con representación Braille de "6 125 135 123 1" 
            (prefijo mayúscula + h + o + l + a)
    """
    if not request.json or 'text' not in request.json:
        return jsonify({"error": "No se proporcionó texto de entrada."}), 400
    
    text = request.json['text']
    
    # Transcribir el texto a códigos Braille
    braille_codes = transcribir_texto_completo(text)
    codes_list = braille_codes.split()
    
    # Dimensiones de la señalética
    cell_width = 25
    cell_height = 35
    margin = 20
    text_height = 30
    
    # Calcular dimensiones totales del SVG
    total_width = len(codes_list) * cell_width + 2 * margin
    total_height = cell_height + text_height + 2 * margin
    
    # Iniciar el SVG
    svg_parts = [
        f'<svg width="{total_width}" height="{total_height}" viewBox="0 0 {total_width} {total_height}" xmlns="http://www.w3.org/2000/svg">',
        f'    <!-- Fondo -->',
        f'    <rect width="{total_width}" height="{total_height}" fill="#ffffff" stroke="#cccccc" stroke-width="1"/>',
        f'    ',
        f'    <!-- Texto en tinta -->',
        f'    <text x="{total_width/2}" y="{margin + 15}" font-family="Arial, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#000">{text}</text>',
        f'    ',
        f'    <!-- Representación Braille -->'
    ]
    
    # Generar cada celda Braille
    for i, code in enumerate(codes_list):
        cell_x = margin + i * cell_width + 5
        cell_y = margin + text_height + 5
        
        # Generar la celda Braille
        braille_cell = generar_celda_braille_svg(code, cell_x, cell_y)
        svg_parts.append(f'    <!-- Celda {i+1}: código {code} -->')
        svg_parts.append(f'    {braille_cell}')
    
    svg_parts.append('</svg>')
    
    svg_output = '\n'.join(svg_parts)
    
    return app.response_class(response=svg_output, status=200, mimetype='image/svg+xml')

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check para verificación de estado del servicio.

    Este endpoint es utilizado por Docker Compose para monitorear la salud
    del contenedor backend.

    Returns:
        tuple: JSON response con los siguientes campos y status code 200:
            - status (str): Estado del servicio (healthy).
            - service (str): Nombre del servicio (tactilink-backend).

    Examples:
        Response:
            >>> {
            ...     "status": "healthy",
            ...     "service": "tactilink-backend"
            ... }
    """
    return jsonify({'status': 'healthy', 'service': 'tactilink-backend'}), 200

if __name__ == '__main__':
    # Solo para desarrollo local (NO se usa en Docker - Docker usa Gunicorn)
    app.run(debug=True, host='0.0.0.0', port=5000)