"""Módulo principal de la API TactiLink para transcripción de texto a Braille.

Este módulo proporciona endpoints REST para convertir texto en español
a código Braille numérico y generar representaciones SVG de señalética Braille.
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
    'u': '136', 'v': '1236', 'w': '2456', 'x': '1346', 'y': '13456', 'z': '1356',
    
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
    '_': '456',  # Subrayado (nota: se repite dos veces)
    '"': '2356',  # Comillas (apertura y cierre usan códigos especiales)
    '!': '26',    # Exclamación (con prefijos)
    '¡': '5',     # Apertura de exclamación (prefijo)
    '¿': '5',     # Apertura de interrogación (prefijo)
    '?': '346',   # Interrogación de cierre
    '(': '5',     # Paréntesis de apertura (prefijo)
    ')': '2356',  # Paréntesis de cierre
    '+': '256',   # Más
    '=': '2356',  # Igual
    '÷': '256',   # División
    '-': '36',    # Guión/menos
    
    # Espacio
    ' ': ' '
}

# Códigos especiales que requieren secuencias
SPECIAL_SEQUENCES = {
    '_': ['456', '456'],  # Subrayado
    '"': ['2356', '235', '2356', '235'],  # Comillas dobles (apertura y cierre)
    '!': ['26', '2356', '26'],  # Exclamación completa
    '¡': ['5', '126'],  # Apertura exclamación
    '¿': ['5', '346'],  # Apertura interrogación
    '(': ['5', '236'],  # Paréntesis apertura
    ')': ['2356', '2356'],  # Paréntesis cierre
    '+': ['256', '256'],  # Suma
}


def es_numero(caracter: str) -> bool:
    """Verifica si un carácter es un dígito numérico."""
    return caracter.isdigit()


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
    
    # Manejar secuencias especiales
    if char_lower in SPECIAL_SEQUENCES:
        return SPECIAL_SEQUENCES[char_lower]
    
    # Manejar números: agregar # solo antes del primer número de una secuencia
    if es_numero(char_lower):
        if not anterior_es_numero:
            # Primer número de la secuencia, agregar signo #
            return ['#', BRAILLE_MAP.get(char_lower, char_lower)]
        else:
            # Número subsecuente, no agregar #
            return [BRAILLE_MAP.get(char_lower, char_lower)]
    
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
        # Determinar contexto
        anterior_es_numero = (i > 0 and es_numero(texto[i-1]))
        siguiente_es_numero = (i < len(texto)-1 and es_numero(texto[i+1]))
        
        # Transcribir carácter
        braille_codes = transcribir_character(char, anterior_es_numero, siguiente_es_numero)
        resultado_braille.extend(braille_codes)
    
    return ' '.join(resultado_braille)


@app.route('/api/transcribe', methods=['POST'])
def transcribe_text():
    """Endpoint para transcripción de texto a código Braille numérico (RG-1)."""
    if not request.json or 'text' not in request.json:
        return jsonify({"error": "No se proporcionó texto de entrada."}), 400
    
    input_text = request.json['text']
    braille_output = transcribir_texto_completo(input_text)
    
    return jsonify({
        "input": request.json['text'],
        "braille_codes": braille_output
    })


@app.route('/api/generar_senaletica', methods=['POST'])
def generar_senaletica():
    """Endpoint para generación de señalética Braille en formato SVG (RG-2)."""
    text = request.json.get('text', 'N/A') if request.json else 'N/A'
    
    svg_placeholder = f"""<svg width="200" height="100" viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
        <rect width="200" height="100" fill="#f0f0f0"/>
        <text x="10" y="30" font-family="Arial" font-size="20">Señalética SVG - WIP</text>
        <text x="10" y="60" font-family="Arial" font-size="16">Texto: {text}</text>
    </svg>"""
    
    return app.response_class(response=svg_placeholder, status=200, mimetype='image/svg+xml')


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check para verificación de estado del servicio."""
    return jsonify({'status': 'healthy', 'service': 'tactilink-backend'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)