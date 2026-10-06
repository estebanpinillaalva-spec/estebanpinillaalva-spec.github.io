"""Redimensiona una imagen y la guarda como WebP de 300 KB como máximo."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

LIMITE = 300_000


def optimizar(origen: Path, destino: Path, ancho_max: int = 1600, calidad: int = 82) -> int:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(origen) as im:
        im = im.convert("RGB")
        ancho = min(im.width, ancho_max)
        while True:
            alto = round(im.height * ancho / im.width)
            img = im if ancho == im.width else im.resize((ancho, alto), Image.LANCZOS)
            q = calidad
            while True:
                img.save(destino, "WEBP", quality=q, method=6)
                size = destino.stat().st_size
                if size <= LIMITE or q <= 50:
                    break
                q -= 8
            if size <= LIMITE or ancho < 400:
                return size
            ancho = int(ancho * 0.8)


if __name__ == "__main__":
    ancho = int(sys.argv[3]) if len(sys.argv) > 3 else 1600
    print(optimizar(Path(sys.argv[1]), Path(sys.argv[2]), ancho))
