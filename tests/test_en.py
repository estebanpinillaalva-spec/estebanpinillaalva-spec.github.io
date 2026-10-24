"""La versión en inglés (en/) debe existir para cada página y llevar las mismas cifras."""
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

# página en español -> página en inglés
PARES = {
    "index.html": "en/index.html",
    "automatizacion.html": "en/automation.html",
    "casos/aludec-kpis.html": "en/cases/aludec-kpis.html",
    "casos/tfg-kart.html": "en/cases/tfg-kart.html",
    "casos/planos-2d.html": "en/cases/planos-2d.html",
    "casos/jarvis.html": "en/cases/jarvis.html",
}

# Las mismas cifras que comprueba test_site.py, en formato inglés.
CIFRAS_EN = {
    "en/cases/aludec-kpis.html": ["15–20 min", "~2 min", "1,370", "MTBF", "MTTR", "Aludec", "with help from Claude"],
    "en/cases/tfg-kart.html": ["112%", "17.81°", "14.81°", "127%", "253%", "−0.89°", "~24°", "Martín", "8.5",
                               "AI agent", "https://github.com/estebanpinillaalva-spec/tfg-kart-direccion"],
    "en/cases/planos-2d.html": ["in progress", "8/8", "deterministic", "Directing Codex and Claude"],
    "en/cases/jarvis.html": ["FatihMakes", "https://github.com/FatihMakes/Mark-XXXIX-OR", "14,335", "566"],
}


def _leer(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


@pytest.mark.parametrize("es,en", PARES.items())
def test_cada_pagina_enlaza_su_traduccion(es, en):
    a_en = os.path.relpath(en, Path(es).parent).replace("\\", "/")
    a_es = os.path.relpath(es, Path(en).parent).replace("\\", "/")
    assert f'class="idioma" href="{a_en}"' in _leer(es)
    assert f'class="idioma" href="{a_es}"' in _leer(en)
    for html in (_leer(es), _leer(en)):
        assert f'hreflang="es" href="https://estebanpinillaalva-spec.github.io/{es}"' in html
        assert f'hreflang="en" href="https://estebanpinillaalva-spec.github.io/{en}"' in html


@pytest.mark.parametrize("en", PARES.values())
def test_paginas_en_ingles_marcadas_como_ingles(en):
    html = _leer(en)
    assert '<html lang="en">' in html
    assert "<!-- sources: English version of" in html


@pytest.mark.parametrize("en,textos", CIFRAS_EN.items())
def test_cifras_y_autoria_en_ingles(en, textos):
    html = _leer(en)
    for texto in textos + ['id="result"']:
        assert texto in html, texto
    assert "from scratch" not in html.lower()


def test_tfg_en_sin_resultados_invalidos():
    html = _leer("en/cases/tfg-kart.html")
    for invalido in ["360%", "279%", "212%", "RMSE"]:
        assert invalido not in html
