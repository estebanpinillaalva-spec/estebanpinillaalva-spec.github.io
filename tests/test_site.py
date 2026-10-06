from pathlib import Path

from tools.check_site import problems

ROOT = Path(__file__).resolve().parent.parent


def test_site_sin_problemas():
    assert problems(ROOT) == []


def test_css_tiene_fuentes_de_reserva():
    css = (ROOT / "assets/css/estilo.css").read_text(encoding="utf-8")
    assert '"IBM Plex Sans", "Segoe UI", Arial, sans-serif' in css
    assert '"IBM Plex Mono", Consolas, "Courier New", monospace' in css


CASOS = ["aludec-kpis", "tfg-kart", "planos-2d", "jarvis"]


def _caso(nombre: str) -> str:
    return (ROOT / "casos" / f"{nombre}.html").read_text(encoding="utf-8")


def test_aludec_cifras_y_sin_datos_reales():
    html = _caso("aludec-kpis")
    for texto in ["15–20 min", "~2 min", "1.370", "MTBF", "MTTR", "Aludec", 'id="resultado"', "<!-- fuentes:"]:
        assert texto in html
    assert ".xlsx" not in html


def test_tfg_resultados_validos_y_autoria():
    html = _caso("tfg-kart")
    for texto in ["112 %", "17,81°", "14,81°", "127 %", "253 %", "−0,89°", "~24°", "Martín", "8,5", 'id="resultado"', "<!-- fuentes:"]:
        assert texto in html
    for invalido in ["360 %", "279 %", "212 %", "360%", "279%", "212%", "RMSE"]:
        assert invalido not in html


def test_planos_en_desarrollo_y_principio():
    html = _caso("planos-2d")
    for texto in ["en desarrollo", "8/8", "determinista", "<!-- fuentes:"]:
        assert texto in html


def test_jarvis_credito_y_no_desde_cero():
    html = _caso("jarvis")
    for texto in ["FatihMakes", "https://github.com/FatihMakes/Mark-XXXIX-OR", "14.335", "566", "<!-- fuentes:"]:
        assert texto in html
    assert "desde cero" not in html.lower()


def test_portada_enlaza_todo():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    for ref in [f"casos/{c}.html" for c in CASOS] + ["automatizacion.html", "cv/CV-Esteban-Pinilla-ES.pdf",
                                                      "cv/CV-Esteban-Pinilla-EN.pdf", 'id="casos"', 'id="contacto"']:
        assert ref in html


def test_automatizacion_metodo_y_pruebas():
    html = (ROOT / "automatizacion.html").read_text(encoding="utf-8")
    for texto in ['class="pasos"', "casos/aludec-kpis.html#resultado", "casos/tfg-kart.html#resultado",
                  "casos/planos-2d.html#resultado", "casos/jarvis.html#resultado", "<!-- fuentes:"]:
        assert texto in html


def test_planos_declara_que_el_codigo_lo_implementan_agentes():
    html = _caso("planos-2d")
    assert "Escribí un motor" not in html
    assert "dirigiendo a Codex y Claude" in html


def test_tfg_comparativa_sin_panel_rmse():
    from PIL import Image
    with Image.open(ROOT / "assets/img/tfg/comparativa.webp") as im:
        # La original tiene tres paneles (% Ackermann, RMSE, singularidad), proporción ~1,69.
        # Sin el panel de RMSE quedan dos, proporción < 1,4.
        assert im.width / im.height < 1.4


def test_wat_marcado_en_pausa_y_como_framework():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    linea = next(l for l in html.splitlines() if "WAT" in l)
    assert "en pausa" in linea and "framework" in linea
    assert "Arquitectura WAT" not in html


def test_tfg_declara_que_los_scripts_se_hicieron_con_un_agente():
    html = _caso("tfg-kart")
    assert "Escribí scripts de MATLAB" not in html
    assert "agente de IA" in html


def test_aludec_declara_que_se_construyo_con_claude():
    html = _caso("aludec-kpis")
    assert "con ayuda de Claude" in html


def test_web_publica_sin_telefono():
    import fitz
    from tools.check_site import iter_html
    for html in iter_html(ROOT):
        texto = html.read_text(encoding="utf-8")
        assert "604" not in texto and "tel:" not in texto, html.name
    for pdf in (ROOT / "cv").glob("*.pdf"):
        assert "604" not in fitz.open(pdf)[0].get_text(), pdf.name


def test_portada_enlaza_github():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "https://github.com/estebanpinillaalva-spec" in html
