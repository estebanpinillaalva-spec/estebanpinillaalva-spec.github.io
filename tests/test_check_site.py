from pathlib import Path

from tools import check_site as cs


def make_site(root: Path, files: dict[str, str | bytes]) -> Path:
    for rel, content in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            p.write_bytes(content)
        else:
            p.write_text(content, encoding="utf-8")
    return root


def test_iter_html_excluye_docs_tools_tests(tmp_path):
    make_site(tmp_path, {"index.html": "", "casos/a.html": "", "docs/x.html": "",
                         "tools/y.html": "", "tests/z.html": ""})
    names = sorted(p.relative_to(tmp_path).as_posix() for p in cs.iter_html(tmp_path))
    assert names == ["casos/a.html", "index.html"]


def test_local_refs_ignora_externos_y_anclas(tmp_path):
    make_site(tmp_path, {"index.html": '<a href="https://x.com">x</a><a href="mailto:a@b.c">m</a>'
                         '<a href="tel:+34">t</a><a href="#top">t</a><a href="casos/a.html">a</a>'
                         '<img src="assets/img/f.jpg" alt="f">'})
    assert cs.local_refs(tmp_path / "index.html") == ["casos/a.html", "assets/img/f.jpg"]


def test_broken_refs_detecta_ruta_inexistente_y_respeta_relativas(tmp_path):
    make_site(tmp_path, {"index.html": '<a href="casos/a.html">a</a><a href="casos/no.html">n</a>',
                         "casos/a.html": '<a href="../index.html">i</a>'})
    assert cs.broken_refs(tmp_path) == [("index.html", "casos/no.html")]


def test_broken_refs_ignora_fragmento(tmp_path):
    make_site(tmp_path, {"index.html": '<a href="casos/a.html#res">a</a>', "casos/a.html": ""})
    assert cs.broken_refs(tmp_path) == []


def test_absolute_refs(tmp_path):
    make_site(tmp_path, {"index.html": '<a href="/casos/a.html">a</a><img src="C:\\x\\f.png" alt="f">'
                         '<a href="file:///c/x.html">f</a><a href="casos/a.html">ok</a>'})
    assert [r for _, r in cs.absolute_refs(tmp_path)] == ["/casos/a.html", "C:\\x\\f.png", "file:///c/x.html"]


def test_images_without_alt(tmp_path):
    make_site(tmp_path, {"index.html": '<img src="a.png"><img src="b.png" alt=""><img src="c.png" alt="c">'})
    assert [r for _, r in cs.images_without_alt(tmp_path)] == ["a.png", "b.png"]


def test_forbidden_files(tmp_path):
    make_site(tmp_path, {"assets/datos.xlsx": b"x", "assets/m.CSV": b"x", "casos/p.SLDPRT": b"x",
                         "docs/ok.xlsx": b"x", "assets/img/ok.webp": b"x"})
    assert sorted(cs.forbidden_files(tmp_path)) == ["assets/datos.xlsx", "assets/m.CSV", "casos/p.SLDPRT"]


def test_oversized_assets_y_total(tmp_path):
    make_site(tmp_path, {"assets/img/grande.webp": b"0" * 300_001, "assets/img/ok.webp": b"0" * 300_000,
                         "assets/video/v.mp4": b"0" * 8_000_001})
    assert sorted(cs.oversized_assets(tmp_path)) == [("assets/img/grande.webp", 300_001),
                                                     ("assets/video/v.mp4", 8_000_001)]
    assert cs.total_assets_bytes(tmp_path) == 300_001 + 300_000 + 8_000_001


def test_problems_vacio_en_sitio_correcto(tmp_path):
    make_site(tmp_path, {"index.html": '<a href="casos/a.html">a</a><img src="assets/img/f.webp" alt="foto">',
                         "casos/a.html": '<a href="../index.html">i</a>', "assets/img/f.webp": b"x"})
    assert cs.problems(tmp_path) == []
