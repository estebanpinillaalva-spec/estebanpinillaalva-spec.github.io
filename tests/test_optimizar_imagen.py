from PIL import Image

from tools.optimizar_imagen import optimizar


def test_optimizar_reduce_ancho_y_peso(tmp_path):
    src = tmp_path / "grande.png"
    Image.effect_noise((3000, 2000), 80).convert("RGB").save(src)
    out = tmp_path / "salida.webp"
    size = optimizar(src, out, ancho_max=1600)
    with Image.open(out) as im:
        assert im.format == "WEBP"
        assert im.width <= 1600
    assert size == out.stat().st_size <= 300_000


def test_optimizar_no_amplia_imagenes_pequenas(tmp_path):
    src = tmp_path / "peq.png"
    Image.new("RGB", (400, 300), "white").save(src)
    out = tmp_path / "peq.webp"
    optimizar(src, out)
    with Image.open(out) as im:
        assert im.size == (400, 300)
