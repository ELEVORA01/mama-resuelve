# -*- coding: utf-8 -*-
"""Gera mama-resuelve-standalone.html a partir de index.html.

Incrusta em base64 todas as imagens de assets/ (incluindo os favicons), para que
a página funcione como um único ficheiro. Editar sempre o index.html e voltar a
correr este script — nunca editar o standalone à mão.

    python3 build-standalone.py
"""
import base64, io, os, re

SRC, OUT = "index.html", "mama-resuelve-standalone.html"
MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}

def data_uri(path):
    assert os.path.exists(path), "falta o ficheiro: " + path
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return "data:%s;base64,%s" % (MIME[os.path.splitext(path)[1].lower()], b64)

html = io.open(SRC, encoding="utf-8").read()
html, n_img = re.subn(r'(src|href)="(assets/[^"]+\.(?:jpe?g|png))"',
                      lambda m: '%s="%s"' % (m.group(1), data_uri(m.group(2))), html)
# o manifesto aponta para ficheiros relativos que não existem ao lado de um ficheiro solto
html, n_man = re.subn(r'<link rel="manifest"[^>]*>\n?', "", html)
html = html.replace("<title>",
    "<!-- Versión autónoma generada por build-standalone.py: todas las imágenes van incrustadas.\n"
    "     Los enlaces legales del pie son relativos: mantén los .html de políticas junto a este archivo. -->\n"
    "<title>", 1)
io.open(OUT, "w", encoding="utf-8").write(html)
print("%s: %d imagens incrustadas, manifesto removido: %s, %.1f MB"
      % (OUT, n_img, "sim" if n_man else "não", os.path.getsize(OUT) / 1048576.0))
