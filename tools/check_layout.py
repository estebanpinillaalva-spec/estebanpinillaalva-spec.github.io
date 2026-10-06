"""Abre cada página a 1280 y 390 px, detecta desplazamiento horizontal y guarda capturas."""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.check_site import iter_html  # noqa: E402

ANCHOS = (1280, 390)


def main() -> int:
    out = ROOT / "tools" / "capturas"
    out.mkdir(parents=True, exist_ok=True)
    fallos = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for html in iter_html(ROOT):
            nombre = html.relative_to(ROOT).as_posix().replace("/", "_").removesuffix(".html")
            for ancho in ANCHOS:
                page = browser.new_page(viewport={"width": ancho, "height": 900})
                page.goto(html.as_uri())
                page.wait_for_load_state("networkidle")
                sw, iw = page.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
                if sw > iw:
                    fallos.append(f"{nombre} a {ancho}px: scrollWidth {sw} > {iw}")
                page.screenshot(path=str(out / f"{nombre}-{ancho}.png"), full_page=True)
                page.close()
        browser.close()
    print("\n".join(fallos) if fallos else "check_layout: sin desplazamiento horizontal")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
