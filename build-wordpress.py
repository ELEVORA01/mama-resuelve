# -*- coding: utf-8 -*-
"""Gera o pacote para enviar para o alojamento (dist/mama-resuelve + .zip).

Copia só o que a página precisa e troca o endereço público do GitHub Pages pelo
endereço definitivo. Não inclui os ficheiros do repositório (README, scripts de
build, imagens originais, standalone) nem o robots.txt — dentro de uma subpasta
o robots.txt é ignorado, quem manda é o do domínio.

    python3 build-wordpress.py [https://elevora.online/mama-resuelve/]
"""
import io, os, re, shutil, sys, zipfile

# endereço actualmente escrito nas páginas (o <link rel="canonical"> do index)
ANTIGO = re.search(r'<link rel="canonical" href="([^"]+)"', io.open("index.html", encoding="utf-8").read()).group(1)
NOVO = sys.argv[1] if len(sys.argv) > 1 else ANTIGO
if not NOVO.endswith("/"):
    NOVO += "/"

PAGINAS = ["index.html", "politica-privacidad.html", "terminos-condiciones.html",
           "politica-reembolso.html", "404.html", "sitemap.xml", "site.webmanifest"]

DEST = os.path.join("dist", "mama-resuelve")
if os.path.exists(DEST):
    shutil.rmtree(DEST)
os.makedirs(DEST)

trocas = 0
for nome in PAGINAS:
    texto = io.open(nome, encoding="utf-8").read()
    texto, n = re.subn(re.escape(ANTIGO), NOVO, texto)
    trocas += n
    io.open(os.path.join(DEST, nome), "w", encoding="utf-8").write(texto)
    print("  %-28s %d endereço(s) trocado(s)" % (nome, n))

# imagens: só as que as páginas usam de facto
usadas = set()
for nome in PAGINAS:
    texto = io.open(os.path.join(DEST, nome), encoding="utf-8").read()
    usadas |= set(re.findall(r'assets/[\w./-]+\.(?:jpe?g|png)', texto))
for rel in sorted(usadas):
    destino = os.path.join(DEST, rel)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(rel, destino)

if NOVO != ANTIGO:
    junto = "".join(io.open(os.path.join(DEST, n), encoding="utf-8").read() for n in PAGINAS)
    assert ANTIGO.rstrip("/") not in junto, "ficaram endereços antigos por trocar"

# Os gestores de ficheiros dos alojamentos (cPanel, Hostinger) falham a extrair
# zips sem entradas de pasta. O zip do sistema cria-as; o zipfile do Python não,
# por isso em alternativa são escritas à mão.
zip_path = os.path.join("dist", "mama-resuelve-wordpress.zip")
if os.path.exists(zip_path):
    os.remove(zip_path)
if shutil.which("zip"):
    import subprocess
    subprocess.run(["zip", "-r", "-q", "-X", os.path.basename(zip_path), os.path.basename(DEST)],
                   cwd="dist", check=True)
    print("\nzip criado com o utilitário do sistema (inclui entradas de pasta)")
else:
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for raiz, _, ficheiros in os.walk(DEST):
            entrada = os.path.relpath(raiz, "dist") + "/"
            info = zipfile.ZipInfo(entrada)
            info.external_attr = (0o40755 << 16) | 0x10
            z.writestr(info, b"")
            for f in sorted(ficheiros):
                caminho = os.path.join(raiz, f)
                z.write(caminho, os.path.relpath(caminho, "dist"))

total = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(DEST) for f in fs)
print("\n%d páginas + %d imagens · %.1f MB · endereço: %s" % (len(PAGINAS), len(usadas), total / 1048576.0, NOVO))
print("zip: %s (%.1f MB)" % (zip_path, os.path.getsize(zip_path) / 1048576.0))
