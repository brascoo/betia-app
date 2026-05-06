# BETIA Pro 🎯

BETIA Pro es una aplicación web diseñada para la gestión, seguimiento y análisis de apuestas deportivas (Picks y Parleys). Integra una interfaz moderna y características de inteligencia artificial para ayudar a los apostadores a tomar mejores decisiones y gestionar su bankroll de manera efectiva.

## Características Principales 🚀

*   **Gestión de Picks y Parleys:** Registra tus selecciones individuales y combinadas, indicando cuota, stake y confianza.
*   **Seguimiento de Bankroll:** Controla tus ganancias, pérdidas y la evolución de tu capital base.
*   **Análisis IA (Integración con Google Gemini):** Utiliza la inteligencia artificial para analizar enfrentamientos, ligas y encontrar valor en las cuotas basándose en contexto adicional.
*   **Resultados e Historial:** Visualiza la evolución de tu bankroll en un gráfico interactivo y mantén un registro de todas tus apuestas.
*   **Contexto y Metodología:** Consulta rápidamente los criterios de selección de apuestas y reglas para armar parleys de alta probabilidad.
*   **Soporte Multideporte:** Adaptado principalmente para Fútbol ⚽, Baloncesto 🏀 y Tenis 🎾, con soporte para otros deportes.
*   **Modo Claro / Oscuro:** Interfaz adaptable a tus preferencias visuales.

## Tecnologías 💻

Este proyecto es una aplicación web frontend pura contenida en un único archivo (`index.html`), construida con:

*   **HTML5**
*   **CSS3** (Variables CSS, Grid, Flexbox, Diseño Responsivo)
*   **JavaScript (Vanilla)**
*   No requiere dependencias externas ni backend. Utiliza `localStorage` para persistir los datos de manera local en tu dispositivo.

## Instalación y Uso 🛠️

1.  Clona el repositorio en tu máquina local:
    ```bash
    git clone https://github.com/brascoo/betia-app.git
    ```
2.  Navega a la carpeta del proyecto:
    ```bash
    cd betia-app
    ```
3.  Abre el archivo `index.html` directamente en tu navegador web preferido. ¡Eso es todo! No se requiere compilación ni ejecutar un servidor local de desarrollo.

## Configuración de la IA (Google Gemini) 🤖

Para habilitar la función de "Análisis IA" dentro de la aplicación:
1. Ve a la sección **Análisis IA**.
2. Ingresa tu API Key de Google Gemini en la configuración (puedes obtener una clave gratuita en [Google AI Studio](https://aistudio.google.com/app/apikey)).
3. Haz clic en "Guardar Key". Las consultas de análisis se realizarán directamente desde tu navegador utilizando esta clave.
