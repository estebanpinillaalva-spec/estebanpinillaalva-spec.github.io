"""Verificador estático del portfolio: enlaces, rutas, alt, ficheros prohibidos y pesos."""
from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

EXCLUIDOS = {"docs", "tools", "tests", ".git", ".superpowers"}
EXTERNOS = ("http:", "https:", "mailto:", "tel:", "#")
PROHIBIDAS = {".xlsx", ".xls", ".xlsm", ".csv", ".sldprt", ".sldasm", ".slddrw", ".mat", ".slx"}
IMG = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
VIDEO = {".mp4", ".webm"}
MAX_IMG, MAX_VIDEO, MAX_TOTAL = 300_000, 8_000_000, 40_000_000


class _Refs(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[str] = []
        self.imgs: list[tuple[str, str | None]] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])
        if tag == "img":
            self.imgs.append((a.get("src") or "", a.get("alt")))


def _parse(html: Path) -> _Refs:
    p = _Refs()
    p.feed(html.read_text(encoding="utf-8"))
    return p


def _site_files(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and not (set(p.relative_to(root).parts[:1]) & EXCLUIDOS):
            yield p


def _rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def iter_html(root: Path) -> list[Path]:
    return sorted(p for p in _site_files(root) if p.suffix.lower() == ".html")


def local_refs(html: Path) -> list[str]:
    return [r for r in _parse(html).refs if not r.startswith(EXTERNOS)]


def _es_absoluta(ref: str) -> bool:
    return ref.startswith(("/", "file:")) or (len(ref) > 2 and ref[1] == ":" and ref[2] in "\\/")


def broken_refs(root: Path) -> list[tuple[str, str]]:
    out = []
    for html in iter_html(root):
        for ref in local_refs(html):
            if _es_absoluta(ref):
                continue
            target = (html.parent / ref.split("#")[0].split("?")[0]).resolve()
            if not target.exists():
                out.append((_rel(root, html), ref))
    return out


def absolute_refs(root: Path) -> list[tuple[str, str]]:
    return [(_rel(root, h), r) for h in iter_html(root) for r in local_refs(h) if _es_absoluta(r)]


def images_without_alt(root: Path) -> list[tuple[str, str]]:
    return [(_rel(root, h), src) for h in iter_html(root) for src, alt in _parse(h).imgs
            if not (alt and alt.strip())]


def forbidden_files(root: Path) -> list[str]:
    return [_rel(root, p) for p in _site_files(root) if p.suffix.lower() in PROHIBIDAS]


def _assets(root: Path):
    base = root / "assets"
    return [p for p in base.rglob("*") if p.is_file()] if base.exists() else []


def oversized_assets(root: Path) -> list[tuple[str, int]]:
    out = []
    for p in _assets(root):
        size, ext = p.stat().st_size, p.suffix.lower()
        if (ext in IMG and size > MAX_IMG) or (ext in VIDEO and size > MAX_VIDEO):
            out.append((_rel(root, p), size))
    return out


def total_assets_bytes(root: Path) -> int:
    return sum(p.stat().st_size for p in _assets(root))


def problems(root: Path) -> list[str]:
    out = [f"enlace roto en {pg}: {r}" for pg, r in broken_refs(root)]
    out += [f"ruta absoluta en {pg}: {r}" for pg, r in absolute_refs(root)]
    out += [f"imagen sin alt en {pg}: {r}" for pg, r in images_without_alt(root)]
    out += [f"fichero prohibido: {f}" for f in forbidden_files(root)]
    out += [f"asset demasiado grande: {f} ({s} bytes)" for f, s in oversized_assets(root)]
    if total_assets_bytes(root) > MAX_TOTAL:
        out.append("assets/ supera 40 MB")
    return out


def main() -> int:
    found = problems(Path.cwd())
    print("\n".join(found) if found else "check_site: sin problemas")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
