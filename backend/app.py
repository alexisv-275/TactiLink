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

BRAILLE_MAP = {
    'a': '1', 'b': '12', 'c': '14', 'd': '145', 'e': '15',
    'f': '124', 'g': '1245', 'h': '125', 'i': '24', 'j': '245',
    'k': '13', 'l': '123', 'm': '134', 'n': '1345', 'o': '135',
    'p': '1234', 'q': '12345', 'r': '1235', 's': '234', 't': '2345',
    'u': '136', 'v': '1236', 'x': '1346', 'y': '13456', 'z': '1356',
    'ñ': '12456', 'ü': '1256', 'w': '2456',
    # Vocales acentuadas
    'á': '12356', 'é': '2346', 'í': '34', 'ó': '346', 'ú': '23456',
}



def transcribir_character(character: str) -> str:
    """Mapea un carácter individual a su representación en código Braille numérico.

    Args:
        character (str): Carácter a transcribir.

    Returns:
        str: Código Braille numérico o el carácter original si no está mapeado.

    Examples:
        >>> transcribir_character('a')
        '1'
        >>> transcribir_character('z')
        'z'
    """
    char_lower = character.lower()
    return BRAILLE_MAP.get(char_lower, character)

def transcribir_texto_completo(texto: str) -> str:
    """Transcribe una cadena de texto completa a código Braille numérico.

    Procesa cada carácter del texto de entrada y los separa con espacios
    en la salida.

    Args:
        texto (str): Texto a transcribir.

    Returns:
        str: Cadena con códigos Braille separados por espacios.

    Examples:
        >>> transcribir_texto_completo('hola')
        '125 135 123 1'
    """
    resultado_braille = []
    for char in texto:
        braille_char = transcribir_character(char)
        resultado_braille.append(braille_char)
    return ' '.join(resultado_braille)



@app.route('/api/transcribe', methods=['POST'])
def transcribe_text():
    """Endpoint para transcripción de texto a código Braille numérico (RG-1).

    Recibe un JSON con el campo 'text' y devuelve su representación en
    código Braille numérico.

    Request JSON:
        text (str): Texto en español a transcribir.

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
    """
    if not request.json or 'text' not in request.json:
        return jsonify({"error": "No se proporcionó texto de entrada."}), 400
    
    input_text = request.json['text'].lower()
    braille_output = transcribir_texto_completo(input_text)
    
    return jsonify({
        "input": request.json['text'],
        "braille_codes": braille_output
    })



@app.route('/api/generar_senaletica', methods=['POST'])
def generar_senaletica():
    """Endpoint para generación de señalética Braille en formato SVG (RG-2).

    Recibe un JSON con el campo 'text' y devuelve una representación
    visual SVG de la señalética Braille.

    Request JSON:
        text (str): Texto a convertir en señalética.

    Returns:
        flask.Response: Documento SVG con la representación visual de la 
            señalética Braille. Content-Type: image/svg+xml.

    Note:
        Esta funcionalidad está en desarrollo (WIP). Actualmente retorna
        un placeholder SVG con el texto de entrada.

    Examples:
        Request:
            >>> {
            ...     "text": "Salida"
            ... }

        Response (SVG):
            <svg width="200" height="100" ...>
                <rect width="200" height="100" fill="#f0f0f0"/>
                <text>Señalética SVG - WIP</text>
                <text>Texto: Salida</text>
            </svg>
    """
    text = request.json.get('text', 'N/A') if request.json else 'N/A'
    
    # Esta función debería usar la lógica de transcripción y luego
    # generar el string SVG que dibuje los puntos Braille.

    # POR AHORA, devuelve solo un placeholder:
    svg_placeholder = f"""<svg width="200" height="100" viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
        <rect width="200" height="100" fill="#f0f0f0"/>
        <text x="10" y="30" font-family="Arial" font-size="20">Señalética SVG - WIP</text>
        <text x="10" y="60" font-family="Arial" font-size="16">Texto: {text}</text>
    </svg>"""
    
    # IMPORTANTE: Se devuelve el MIME type correcto para SVG
    return app.response_class(response=svg_placeholder, status=200, mimetype='image/svg+xml')

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