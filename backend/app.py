"""Módulo principal de la API TactiLink para transcripción de texto a Braille.

Este módulo proporciona endpoints REST para convertir texto en español
a código Braille numérico y viceversa, cumpliendo con los estándares del proyecto.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. MAPEO DE CARACTERES (Siguiendo el PDF de la materia)
BRAILLE_MAP = {
    # Letras a-z (Sin cambios, son estándar)
    'a': '1', 'b': '12', 'c': '14', 'd': '145', 'e': '15',
    'f': '124', 'g': '1245', 'h': '125', 'i': '24', 'j': '245',
    'k': '13', 'l': '123', 'm': '134', 'n': '1345', 'o': '135',
    'p': '1234', 'q': '12345', 'r': '1235', 's': '234', 't': '2345',
    'u': '136', 'v': '1236', 'w': '2456', 'x': '1346', 'y': '13456',
    'z': '1356',
    
    # Vocales acentuadas y Ñ (Según tu imagen del PDF)
    'á': '12356', 'é': '2346', 'í': '34', 'ó': '346', 'ú': '23456',
    'ü': '1256', 'ñ': '12456',
    
    # Signos de puntuación CORREGIDOS según tu imagen
    '=': '2356', # El signo igual
    '¿': '26',     # Corregido: punto 2 y 6
    '?': '26',     # En español Braille, abrir y cerrar pregunta es igual
    '¡': '235',    # Corregido: puntos 2, 3 y 5
    '!': '235',    # En español Braille, abrir y cerrar admiración es igual
    '"': '236',   # Comillas dobles
    '_': '36',    # Guion bajo
    '÷': '256',   # Signo de división
    '.': '3', ',': '2', ';': '23', ':': '25', '-': '36',
    '(': '126', ')': '345', '+': '235', ' ': ' '
}

# Mapeo específico para números (puntos de la 'a' a la 'j')
NUM_BRAILLE_MAP = {
    '1': '1', '2': '12', '3': '14', '4': '145', '5': '15',
    '6': '124', '7': '1245', '8': '125', '9': '24', '0': '245'
}

# 2. GENERACIÓN DE MAPAS INVERSOS CON PRIORIDAD (Evita colisión ú/¡)
def _generar_reverse_map():
    rev_map = {}
    # Primero agregamos símbolos (tienen menor prioridad)
    for k, v in BRAILLE_MAP.items():
        if not k.isalnum() and k not in 'áéíóúüñ':
            rev_map[v] = k
    # Luego agregamos letras (sobrescriben a los símbolos si el código es igual)
    for k, v in BRAILLE_MAP.items():
        if k.isalpha() or k in 'áéíóúüñ':
            if v != ' ': rev_map[v] = k
    return rev_map

REVERSE_BRAILLE_MAP = _generar_reverse_map()
REVERSE_NUMBER_MAP = {v: k for k, v in BRAILLE_MAP.items() if k.isdigit()}

# --- FUNCIONES DE APOYO ---

def es_numero(caracter: str) -> bool:
    return caracter.isdigit()

def generar_celda_braille_svg(codigo_braille: str, x: float, y: float) -> str:
    codigos_especiales = {'#': '3456', '6': '6'}
    if codigo_braille in codigos_especiales:
        codigo_braille = codigos_especiales[codigo_braille]
    
    dot_radius = 3
    dot_spacing_horizontal = 10
    dot_spacing_vertical = 10
    dot_positions = {
        '1': (x, y), '2': (x, y + dot_spacing_vertical), '3': (x, y + 2 * dot_spacing_vertical),
        '4': (x + dot_spacing_horizontal, y), '5': (x + dot_spacing_horizontal, y + dot_spacing_vertical),
        '6': (x + dot_spacing_horizontal, y + 2 * dot_spacing_vertical)
    }
    svg_circles = []
    for pos in ['1', '2', '3', '4', '5', '6']:
        px, py = dot_positions[pos]
        color = "#000" if pos in codigo_braille else "#e0e0e0"
        stroke = "#999" if pos not in codigo_braille else "none"
        svg_circles.append(f'<circle cx="{px}" cy="{py}" r="{dot_radius}" fill="{color}" stroke="{stroke}" stroke-width="0.5"/>')
    return '\n'.join(svg_circles)

# --- LÓGICA DE TRADUCCIÓN ---

def transcribir_texto_completo(texto: str) -> str:
    """Español -> Braille con puntos correctos para números."""
    resultado = []
    modo_numerico = False
    
    for char in texto:
        c = char.lower()
        
        if c.isdigit():
            if not modo_numerico:
                resultado.append('3456') # Signo de número
                modo_numerico = True
            # IMPORTANTE: Usamos NUM_BRAILLE_MAP para obtener los PUNTOS, no el dígito
            resultado.append(NUM_BRAILLE_MAP.get(c, ''))
        
        elif c == ' ':
            resultado.append(' ')
            modo_numerico = False
            
        else:
            modo_numerico = False
            if char.isupper():
                resultado.append('46') # Signo de mayúscula
            resultado.append(BRAILLE_MAP.get(c, c))

    # Unión final con espacios entre celdas
    return " ".join(resultado)

def reverse_transcribe(braille_codes_str: str) -> str:
    """Braille -> Español: Diferencia entre letras y números tras el signo #."""
    # IMPORTANTE: No eliminamos los elementos vacíos aquí
    raw_codes = braille_codes_str.strip().split(' ')
    resultado = []
    i = 0
    modo_numerico = False
    
    REVERSE_NUM_MAP = {v: k for k, v in NUM_BRAILLE_MAP.items()}
    REVERSE_LETRA_MAP = REVERSE_BRAILLE_MAP 

    while i < len(raw_codes):
        code = raw_codes[i]
        
        # 1. SI EL CÓDIGO ESTÁ VACÍO: Significa que hay un espacio (o doble espacio en la entrada)
        if code == '':
            resultado.append(' ')
            modo_numerico = False # El espacio rompe el modo numérico
            i += 1
            continue

        # 2. Detectar signo de número
        if code == '3456':
            modo_numerico = True
            i += 1
            continue
            
        # 3. Traducir según el modo activo
        if modo_numerico:
            num = REVERSE_NUM_MAP.get(code)
            if num:
                resultado.append(num)
            else:
                modo_numerico = False
                resultado.append(REVERSE_LETRA_MAP.get(code, '?'))
        else:
            # Manejo de mayúsculas (Prefijo 46)
            if code == '46' and i + 1 < len(raw_codes):
                siguiente_codigo = raw_codes[i+1]
                # Si lo que sigue es un espacio, solo ignoramos el prefijo o ponemos error
                if siguiente_codigo == '':
                    resultado.append(' ')
                    i += 1
                else:
                    letra = REVERSE_LETRA_MAP.get(siguiente_codigo, '?')
                    resultado.append(letra.upper())
                    i += 2
                continue
            
            # Traducción normal de letras y símbolos
            resultado.append(REVERSE_LETRA_MAP.get(code, '?'))
        
        i += 1
        
    # Limpiamos espacios dobles accidentales al final y unimos
    return ''.join(resultado).replace('  ', ' ')
# --- ENDPOINTS API ---

@app.route('/api/transcribe', methods=['POST'])
def transcribe_text():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "No se proporcionó texto"}), 400
    return jsonify({"input": data['text'], "braille_codes": transcribir_texto_completo(data['text'])})

@app.route('/api/reverse-transcribe', methods=['POST', 'OPTIONS'])
def reverse_api():
    # Esto maneja errores de conexión previos
    if request.method == 'OPTIONS':
        return '', 200
        
    data = request.get_json()
    # Buscamos 'braille_codes' que es lo que envía tu script.js actual
    codigo = data.get('braille_codes')
    
    if not codigo:
        return jsonify({"error": "No hay datos", "text": "Formato incorrecto"}), 400
    
    resultado = reverse_transcribe(codigo)
    
    # IMPORTANTE: Devolvemos 'text' porque tu JS busca data.text
    return jsonify({
        "text": resultado,
        "braille_codes": codigo
    })

@app.route('/api/generar_senaletica', methods=['POST'])
def generar_senaletica():
    text = request.json.get('text', '')
    codes_list = transcribir_texto_completo(text).split()
    cell_w, cell_h, margin = 25, 35, 20
    total_w = len(codes_list) * cell_w + 2 * margin
    total_h = cell_h + 50
    svg = [f'<svg width="{total_w}" height="{total_h}" xmlns="http://www.w3.org/2000/svg">',
           f'<rect width="100%" height="100%" fill="white"/>']
    for i, code in enumerate(codes_list):
        svg.append(generar_celda_braille_svg(code, margin + i * cell_w, 45))
    svg.append('</svg>')
    return app.response_class(response='\n'.join(svg), status=200, mimetype='image/svg+xml')

@app.route('/api/generar_senaletica_espejo', methods=['POST'])
def generar_senaletica_espejo():
    text = request.json.get('text', '')
    codes_list = transcribir_texto_completo(text).split()
    # Invertir orden de celdas para lectura por detrás
    codes_list.reverse()
    
    # Mapeo de espejo: Columnas 1-2-3 se intercambian con 4-5-6
    mirror_map = {'1': '4', '4': '1', '2': '5', '5': '2', '3': '6', '6': '3'}
    mirror_codes = ["".join(sorted([mirror_map.get(d, d) for d in c])) for c in codes_list]

    cell_w, cell_h, margin = 25, 35, 20
    total_w = len(mirror_codes) * cell_w + 2 * margin
    total_h = cell_h + 50
    svg = [f'<svg width="{total_w}" height="{total_h}" xmlns="http://www.w3.org/2000/svg">',
           f'<rect width="100%" height="100%" fill="white"/>']
    for i, code in enumerate(mirror_codes):
        svg.append(generar_celda_braille_svg(code, margin + i * cell_w, 45))
    svg.append('</svg>')
    return app.response_class(response='\n'.join(svg), status=200, mimetype='image/svg+xml')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)