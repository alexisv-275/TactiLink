from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración CORS para desarrollo (permite al frontend acceder)
# En un entorno de producción con Nginx, esto no siempre es necesario
# pero es útil para pruebas locales fuera de Docker.
from flask_cors import CORS
CORS(app) 

# Diccionario de mapeo Braille: Primera Serie a-j (Ejemplo Inicial)
# Aquí es donde se expandirá toda la lógica de los Casos de Prueba (CP-1.1 a CP-1.6)
BRAILLE_MAP = {
    'a': '1', 'b': '12', 'c': '14', 'd': '145', 'e': '15', 
    '1': '#1', '2': '#12', 
    '.': '256', ',': '2',
    ' ': ' ' # Espacio en blanco
}

# 1. Endpoint para Transcripción (RG-1)
@app.route('/api/transcribe', methods=['POST'])
def transcribe_text():
    """Recibe texto en español y devuelve la representación en código numérico Braille."""
    if not request.json or 'text' not in request.json:
        return jsonify({"error": "No se proporcionó texto de entrada."}), 400

    input_text = request.json['text'].lower() # Usar minúsculas para simplificar el mapeo inicial
    
    braille_output = []
    
    # Aquí iría toda la lógica compleja para iterar sobre input_text 
    # y aplicar las reglas de mapeo de las series, acentos, y reglas numéricas.
    
    for char in input_text:
        # Lógica de ejemplo MUY simple:
        code = BRAILLE_MAP.get(char, '??') # Usa '??' si no lo encuentra
        braille_output.append(code)

    return jsonify({
        "input": request.json['text'],
        "braille_codes": " ".join(braille_output)
    })

# 2. Endpoint para Generación de Señalética (RG-2)
@app.route('/api/generar_senaletica', methods=['POST'])
def generate_signage():
    """Recibe texto y devuelve la representación en formato SVG (Image/Vectorial)."""
    # Esta función debería usar la lógica de transcripción y luego
    # generar el string SVG que dibuje los puntos Braille.
    
    # POR AHORA, devuelve solo un placeholder:
    
    svg_placeholder = f"""
    <svg width="200" height="100" viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
        <rect width="200" height="100" fill="#f0f0f0"/>
        <text x="10" y="30" font-family="Arial" font-size="20">Señalética SVG - WIP</text>
        <text x="10" y="60" font-family="Arial" font-size="16">Texto de entrada: {request.json.get('text', 'N/A')}</text>
    </svg>
    """
    
    # IMPORTANTE: Se devuelve el MIME type correcto para SVG
    return app.response_class(
        response=svg_placeholder,
        status=200,
        mimetype='image/svg+xml'
    )


if __name__ == '__main__':
    # Usado solo para pruebas locales (fuera de docker)
    app.run(host='0.0.0.0', port=5000, debug=True)