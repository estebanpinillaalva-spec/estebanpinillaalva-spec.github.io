# Portfolio de Esteban Pinilla Álvarez

Web personal con mis casos de ingeniería mecánica e industrial y de automatización con IA.

**Web:** https://estebanpinillaalva-spec.github.io

## Qué contiene

| Página | De qué trata |
|---|---|
| [Portada](index.html) | Presentación, los cuatro casos, otros proyectos y contacto |
| [Caso 01 · Aludec](casos/aludec-kpis.html) | Automatización del cálculo semanal de MTBF y MTTR en un departamento de mantenimiento de automoción: de 15–20 min a ~2 min |
| [Caso 02 · TFG](casos/tfg-kart.html) | Diagnóstico y rediseño de la dirección de un kart en Simscape Multibody: Ackermann del 253 % al 112 % verificado en CAD |
| [Caso 03 · Planos 2D](casos/planos-2d.html) | Motor en Python que genera planos de fabricación a través de la API de SolidWorks (en desarrollo) |
| [Caso 04 · JARVIS](casos/jarvis.html) | Ampliación de un asistente de voz open source con memoria local, correo, calendario y agentes |
| [Automatización para empresas](automatizacion.html) | Cómo abordo la automatización de procesos repetitivos |

Cada caso indica qué parte es mía y qué parte se hizo en equipo o con ayuda de IA.

## Cómo está hecha

- **HTML y CSS escritos a mano**, sin frameworks ni paso de compilación. Se abre con doble clic y se publica tal cual en GitHub Pages.
- **Estilo "cuaderno de ingeniería":** cuadrícula de papel de plano, IBM Plex Sans e IBM Plex Mono, azul marino y granate.
- **Verificación automática en Python:**
  - `tools/check_site.py`: enlaces rotos, rutas absolutas, imágenes sin texto alternativo, ficheros que no deben publicarse (hojas de cálculo, CAD) y peso de imágenes y vídeos.
  - `tools/check_layout.py`: abre cada página con Playwright a 1280 y a 390 px, detecta desplazamiento horizontal y guarda capturas.
  - `tests/`: pruebas con pytest sobre el verificador y sobre el contenido (por ejemplo, que las cifras del TFG sean las de la memoria entregada).

## Ejecutar las comprobaciones

```bash
pip install pytest pillow pymupdf playwright
python -m playwright install chromium
python -m pytest -q
python tools/check_site.py
python tools/check_layout.py
```

## Contacto

estebanpinillaalva@gmail.com
