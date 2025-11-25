from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Diccionario de mapeo Braille
BRAILLE_MAP = {
    'a': '1', 'b': '12', 'c': '14', 'd': '145', 'e': '15',
    'f': '124', 'g': '1245', 'h': '125', 'i': '24', 'j': '245',
    'k': '13', 'l': '123', 'm': '134', 'n': '1345', 'o': '135',
    'p': '1234', 'q': '12345', 'r': '1235', 's': '234', 't': '2345',
}



def transcribir_character(character: str) -> str:
    """Mapea un carácter a código Braille."""
    char_lower = character.lower()
    return BRAILLE_MAP.get(char_lower, character)

def transcribir_texto_completo(texto: str) -> str:
    """Transcribe texto completo a Braille."""
    resultado_braille = []
    for char in texto:
        braille_char = transcribir_character(char)
        resultado_braille.append(braille_char)
    return ' '.join(resultado_braille)



@app.route('/api/transcribe', methods=['POST'])
def transcribe_text():
    """Transcribe texto a código Braille."""
    if not request.json or 'text' not in request.json:
        return jsonify({"error": "No se proporcionó texto de entrada."}), 400
    
    input_text = request.json['text'].lower()
    braille_output = transcribir_texto_completo(input_text)
    
    return jsonify({
        "input": request.json['text'],
        "braille_codes": braille_output
    })



# 2. Endpoint para Generación de Señalética (RG-2)
@app.route('/api/generar_senaletica', methods=['POST'])
def generar_senaletica():
    """Recibe texto y devuelve la representación en formato SVG (Image/Vectorial)."""
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

#para que el docker no se cierre solo
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    # Usado solo para pruebas locales (fuera de docker)
    app.run(debug=True, host='0.0.0.0', port=5000)