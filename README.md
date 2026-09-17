# Mamá Resuelve — landing page

Página de vendas de um produto digital (guia de 200 receitas de merenda infantil + 5 bónus),
vendido via Hotmart. Público-alvo: mães na Colômbia. Conteúdo em espanhol latino-americano.

## Estrutura

```
index.html                      página principal — HTML + CSS + JS num só ficheiro,
                                as imagens são carregadas de ./assets
mama-resuelve-standalone.html   GERADO — a mesma página com as imagens em base64 (~4,3 MB)
politica-privacidad.html        GERADO ┐
terminos-condiciones.html       GERADO ├ páginas legais (Colômbia), todas com noindex
politica-reembolso.html         GERADO ┘
404.html                        página de erro (GitHub Pages usa-a sozinho)
build-standalone.py             gera o standalone a partir do index.html
build-legal.py                  gera as três políticas a partir de um template comum
robots.txt, sitemap.xml         para motores de busca
site.webmanifest                nome, cores e ícones quando se adiciona ao ecrã inicial
assets/                         imagens optimizadas usadas pela página
assets/icons/                   favicons 16/32, apple-touch-icon 180, ícones 192/512
assets/og-mama-resuelve.jpg     miniatura de partilha 1200×630 (WhatsApp, Facebook)
hf_*.png, Print*.png, Create-*  imagens originais, tal como saíram do gerador
.claude/launch.json             configuração do servidor de pré-visualização local
```

Os ficheiros marcados como GERADO não se editam à mão:

```bash
python3 build-legal.py && python3 build-standalone.py
```

## Ver a página localmente

```bash
python3 -m http.server 4317
```

Depois abre <http://localhost:4317>. O `mama-resuelve-standalone.html` também abre
directamente com duplo clique, sem servidor.

## Design

- **Tipografia:** Fraunces (títulos, eixo variável `SOFT`) + Figtree (corpo), via Google Fonts.
- **Paleta:** terracota `#C2542C` dominante, verde-sálvia `#7D8F6E`, creme `#FBF3E6`, tinta `#2A2119`.
- **Cartões:** borda definida de 2px com sombra sólida deslocada — sem sombras difusas.
- **Layout:** mobile-first, hero assimétrico, sem overflow horizontal de 320px a 1600px.
- Animações de entrada respeitam `prefers-reduced-motion`.

## Funil

Todos os CTAs ao longo da página rolam até à secção de planos (`#pricing`).
Os únicos links externos são os dois botões dos planos:

| Plano | Preço | Checkout |
|---|---|---|
| Básico — 200 receitas, 7 categorias | 5,90 USD | `pay.hotmart.com/O107566662Y` |
| Completo — Básico + 5 bónus | 11,90 USD | `pay.hotmart.com/I107569605E` |

## Notas sobre os assets

Os ficheiros em `assets/` não são cópias directas dos originais:

- As 5 capas de bónus vieram do gerador com **o quadriculado de transparência gravado
  como pixels reais** (`hasAlpha: no`). Foi removido por flood-fill a partir da margem,
  preservando a sombra do livro como preto transparente. Se chegarem capas novas da
  mesma fonte, é preciso repetir o processo.
- O mockup 3D da caixa tinha fundo creme `#FFF4E2` chapado, recortado da mesma forma.
- Os screenshots de receitas (`receta-*.jpg`) foram renderizados a partir dos PDFs
  reais do produto, não são mockups.

O `mama-resuelve-standalone.html` é **gerado** a partir do `index.html` — ao editar a
página, editar sempre o `index.html` e regenerar o standalone, nunca o contrário.

## Robustez

Os blocos que aparecem com animação ao fazer scroll só ficam escondidos quando há
JavaScript: um script no `<head>` põe a classe `js` no `<html>`, e o CSS só esconde
`.js .reveal`. Se o script principal falhar, ao fim de 2,5 s a classe é retirada e
tudo fica visível. Sem JS, a página lê-se inteira.

## Origem das vendas (Hotmart)

Os botões dos planos levam `?src=landing` por omissão. Se a página for aberta com
parâmetros — por exemplo `.../?utm_source=instagram&utm_campaign=lanzamiento` — o
script passa `src`, `sck` e os `utm_*` para o checkout, e a origem aparece nos
relatórios da Hotmart. Sem `src` explícito, usa-se o `utm_source`.

## Ao mudar de domínio

A URL pública `https://elevora01.github.io/mama-resuelve/` está escrita por extenso
onde tem de ser absoluta. Ao passar para o domínio definitivo, trocar em:

- `index.html` — `canonical`, `og:url`, `og:image`, `twitter:image` e o bloco JSON-LD
- `robots.txt` e `sitemap.xml`
- `404.html` — favicon e botão de voltar (são absolutos de propósito: a 404 é servida
  em qualquer caminho partido)

Depois, correr `python3 build-standalone.py`.

```bash
grep -rl "elevora01.github.io" --include="*.html" --include="*.txt" --include="*.xml" .
```

