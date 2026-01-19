/**
 * TactiLink - Script Principal
 * Lógica de transcripción bidireccional Braille ↔ Español
 * y generación de señalética SVG
 */

document.addEventListener("DOMContentLoaded", () => {
  // ========== ELEMENTOS DEL DOM ==========
  const brailleInput = document.getElementById('braille-input');
  const spanishInput = document.getElementById('spanish-input');
  const btnClear = document.getElementById('btn-clear');
  const btnDownloadSVG = document.getElementById('btn-download-svg');
  const btnGenerateEspejo = document.getElementById('btn-generate-espejo');
  const btnDownloadEspejo = document.getElementById('btn-download-espejo');
  const visualPreview = document.getElementById('visual-preview');
  const espejoPreview = document.getElementById('espejo-preview');

  // Variables globales para almacenar SVGs
  let currentSvgNormal = null;
  let currentSvgEspejo = null;
  let debounceTimer = null;
  let debounceTimerBraille = null;

  // ========== FUNCIONES AUXILIARES ==========

  /**
   * Función genérica para hacer peticiones POST a la API
   * @param {string} endpoint - Ruta del endpoint (ej: '/api/transcribe')
   * @param {object} data - Datos a enviar en el body
   * @returns {Promise<Response|null>} - Respuesta del fetch o null si hay error
   */
  const fetchAPI = async (endpoint, data) => {
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      return response;
    } catch (error) {
      console.error(`Error al comunicarse con ${endpoint}:`, error);
      alert(`ERROR: No se pudo conectar con el servicio. Verifica que Docker esté ejecutándose.`);
      return null;
    }
  };

  /**
   * Descarga un archivo desde contenido de texto
   * @param {string} content - Contenido del archivo
   * @param {string} filename - Nombre del archivo a descargar
   * @param {string} mimeType - Tipo MIME del archivo
   */
  const downloadFile = (content, filename, mimeType) => {
    try {
      const blob = new Blob([content], { type: mimeType });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      
      a.href = url;
      a.download = filename;
      a.style.display = 'none';
      
      document.body.appendChild(a);
      a.click();
      
      setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }, 100);
    } catch (error) {
      console.error('Error al descargar archivo:', error);
      alert('Error al descargar el archivo.');
    }
  };

  /**
   * Limpia el nombre de archivo removiendo caracteres no permitidos
   * @param {string} text - Texto a limpiar
   * @returns {string} - Texto limpio para nombre de archivo
   */
  const cleanFilename = (text) => {
    return text.replace(/[^a-zA-Z0-9áéíóúñü]/g, '_').substring(0, 50);
  };

  /**
   * Muestra un mensaje de placeholder en un contenedor
   * @param {HTMLElement} container - Contenedor donde mostrar el mensaje
   * @param {string} message - Mensaje a mostrar
   */
  const showPlaceholder = (container, message) => {
    container.innerHTML = `<p class="text-text-secondary-light dark:text-text-secondary-dark text-sm">${message}</p>`;
  };

  // ========== A1: TRANSCRIPCIÓN TEXTO → BRAILLE ==========

  /**
   * Transcribe texto español a código Braille numérico
   */
  const transcribeTextToBraille = async () => {
    const text = spanishInput.value.trim();
    
    if (!text) {
      // Si no hay texto, limpiar todo
      brailleInput.value = '';
      currentSvgNormal = null;
      currentSvgEspejo = null;
      showPlaceholder(visualPreview, 'Vista previa de Braille aparecerá aquí.');
      showPlaceholder(espejoPreview, 'Vista espejo aparecerá aquí.');
      return;
    }

    // Mostrar estado de carga
    brailleInput.value = 'Transcribiendo...';
    showPlaceholder(visualPreview, 'Generando vista previa...');
    
    // Limpiar el espejo anterior
    currentSvgEspejo = null;
    showPlaceholder(espejoPreview, 'Vista espejo aparecerá aquí.');

    const response = await fetchAPI('/api/transcribe', { text });
    
    if (!response) {
      brailleInput.value = '';
      showPlaceholder(visualPreview, 'Error al transcribir.');
      return;
    }

    const data = await response.json();
    
    if (data.error) {
      brailleInput.value = '';
      alert(`Error de API: ${data.error}`);
      showPlaceholder(visualPreview, 'Error en la transcripción.');
    } else {
      // Mostrar códigos Braille en el textarea
      brailleInput.value = data.braille_codes || 'No se pudo generar código.';
      
      // Generar SVG automáticamente para vista previa
      await generateSVGPreview(text);
    }
  };

  /**
   * Transcribe automáticamente en tiempo real con debounce
   */
  const autoTranscribe = () => {
    // Limpiar el timer anterior
    clearTimeout(debounceTimer);
    
    // Establecer un nuevo timer para ejecutar después de 500ms sin cambios
    debounceTimer = setTimeout(() => {
      transcribeTextToBraille();
    }, 500);
  };

  // ========== A1.5: TRANSCRIPCIÓN INVERSA BRAILLE → ESPAÑOL ==========

  /**
   * Transcribe código Braille numérico a texto español
   */
const transcribeBrailleToSpanish = async () => {
    const brailleCodes = brailleInput.value.trim();
    
    if (!brailleCodes) {
      spanishInput.value = '';
      currentSvgNormal = null;
      currentSvgEspejo = null;
      showPlaceholder(visualPreview, 'Vista previa de Braille aparecerá aquí.');
      showPlaceholder(espejoPreview, 'Vista espejo aparecerá aquí.');
      return;
    }

    spanishInput.value = 'Traduciendo...';
    
    currentSvgEspejo = null;
    showPlaceholder(espejoPreview, 'Vista espejo aparecerá aquí.');

    // 1. URL correcta con guion bajo y enviando 'braille_codes'
    const response = await fetchAPI('http://localhost:5000/api/reverse-transcribe', { braille_codes: brailleCodes });
    
    if (!response) {
      spanishInput.value = '';
      return;
    }

    const data = await response.json();
    
    if (data.error) {
      spanishInput.value = '';
      alert(`Error de API: ${data.error}`);
    } else {
      const textoTraducido = data.text || 'No se pudo traducir.';
      spanishInput.value = textoTraducido;
      
      if (data.text) {
        await generateSVGPreview(textoTraducido);
      }
    }
};

  /**
   * Transcribe automáticamente Braille a Español en tiempo real con debounce
   */
  const autoTranscribeBraille = () => {
    // Limpiar el timer anterior
    clearTimeout(debounceTimerBraille);
    
    // Establecer un nuevo timer para ejecutar después de 500ms sin cambios
    debounceTimerBraille = setTimeout(() => {
      transcribeBrailleToSpanish();
    }, 500);
  };

  /**
   * Genera el SVG y lo muestra en la vista previa (sin descargar)
   * @param {string} text - Texto para generar el SVG
   */
  const generateSVGPreview = async (text) => {
    showPlaceholder(visualPreview, 'Generando SVG...');

    const response = await fetchAPI('/api/generar_senaletica', { text });
    
    if (!response) {
      showPlaceholder(visualPreview, 'Error al generar SVG.');
      return;
    }

    // El endpoint devuelve SVG como texto, no JSON
    const svgText = await response.text();
    
    // Guardar SVG para uso posterior
    currentSvgNormal = svgText;

    // Mostrar SVG en la vista previa
    visualPreview.innerHTML = svgText;
  };

  /**
   * Genera el SVG en espejo y lo muestra en la vista previa
   * @param {string} text - Texto para generar el SVG espejo
   */
  const generateSVGEspejo = async (text) => {
    if (!text) {
      text = spanishInput.value.trim();
    }

    if (!text) {
      alert('Por favor, ingresa texto en español para generar el espejo.');
      return;
    }

    showPlaceholder(espejoPreview, 'Generando SVG espejo...');

    const response = await fetchAPI('/api/generar_senaletica_espejo', { text });
    
    if (!response) {
      showPlaceholder(espejoPreview, 'Error al generar SVG espejo.');
      return;
    }

    // El endpoint devuelve SVG como texto
    const svgText = await response.text();
    
    // Guardar SVG espejo para uso posterior
    currentSvgEspejo = svgText;

    // Mostrar SVG en la vista previa de espejo
    espejoPreview.innerHTML = svgText;
  };

  // ========== A2: DESCARGA DE SVG NORMAL ==========

  /**
   * Descarga el SVG de la señalética normal
   * Si ya existe un SVG generado, lo descarga directamente
   * Si no, genera uno nuevo
   */
  const downloadSVGNormal = async () => {
    const text = spanishInput.value.trim();
    
    if (!text) {
      alert('Por favor, ingresa texto en español para generar el SVG.');
      return;
    }

    // Si no hay SVG generado, generarlo primero
    if (!currentSvgNormal) {
      await generateSVGPreview(text);
    }

    // Si después de intentar generar sigue sin SVG, salir
    if (!currentSvgNormal) {
      alert('No se pudo generar el SVG.');
      return;
    }

    // Descargar el SVG
    const filename = `senaletica_braille_${cleanFilename(text)}.svg`;
    downloadFile(currentSvgNormal, filename, 'image/svg+xml;charset=utf-8');
  };

  // ========== A3: DESCARGA DE SVG ESPEJO ==========

  /**
   * Descarga el SVG de la señalética en espejo
   * Si ya existe un SVG espejo generado, lo descarga directamente
   * Si no, genera uno nuevo
   */
  const downloadSVGEspejo = async () => {
    const text = spanishInput.value.trim();
    
    if (!text) {
      alert('Por favor, ingresa texto en español para generar el SVG espejo.');
      return;
    }

    // Si no hay SVG espejo generado, generarlo primero
    if (!currentSvgEspejo) {
      await generateSVGEspejo(text);
    }

    // Si después de intentar generar sigue sin SVG, salir
    if (!currentSvgEspejo) {
      alert('No se pudo generar el SVG espejo.');
      return;
    }

    // Descargar el SVG espejo
    const filename = `senaletica_braille_espejo_${cleanFilename(text)}.svg`;
    downloadFile(currentSvgEspejo, filename, 'image/svg+xml;charset=utf-8');
  };

  // ========== C1: LIMPIAR TODO ==========

  /**
   * Limpia todos los campos y vistas previas
   */
  const clearAll = () => {
    brailleInput.value = '';
    spanishInput.value = '';
    currentSvgNormal = null;
    currentSvgEspejo = null;
    
    // Restaurar placeholders
    showPlaceholder(visualPreview, 'Vista previa de Braille aparecerá aquí.');
    showPlaceholder(espejoPreview, 'Vista espejo aparecerá aquí.');
  };

  // ========== FUNCIÓN AUXILIAR: VISTA PREVIA ==========

  /**
   * Actualiza la vista previa visual de Braille (placeholder por ahora)
   * @param {string} brailleCodes - Códigos Braille separados por espacios
   */
  const updateVisualPreview = (brailleCodes) => {
    // Por ahora, solo mostrar un mensaje
    // La implementación completa de círculos Braille se hará después
    if (brailleCodes) {
      showPlaceholder(visualPreview, `Códigos Braille: ${brailleCodes.split(' ').length} celdas`);
    } else {
      showPlaceholder(visualPreview, 'Vista previa de Braille aparecerá aquí.');
    }
  };

  // ========== EVENT LISTENERS ==========

  // Traducción automática en tiempo real al escribir en español
  spanishInput.addEventListener('input', autoTranscribe);

  // Traducción automática en tiempo real al escribir en Braille
  brailleInput.addEventListener('input', autoTranscribeBraille);

  btnDownloadSVG.addEventListener('click', downloadSVGNormal);
  btnGenerateEspejo.addEventListener('click', async () => {
    const text = spanishInput.value.trim();
    if (text) {
      await generateSVGEspejo(text);
    } else {
      alert('Por favor, ingresa texto en español primero.');
    }
  });
  btnDownloadEspejo.addEventListener('click', downloadSVGEspejo);
  btnClear.addEventListener('click', clearAll);

  // Placeholders iniciales
  showPlaceholder(visualPreview, 'Vista previa de Braille aparecerá aquí.');
  showPlaceholder(espejoPreview, 'Vista espejo aparecerá aquí.');

  console.log('✅ TactiLink cargado correctamente');
});
