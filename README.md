# Mamá Resuelve — landing page

Página de vendas de um produto digital (guia de 200 receitas de merenda infantil + 5 bónus),
vendido via Hotmart. Público-alvo: mães na Colômbia. Conteúdo em espanhol latino-americano.

## Estrutura

```
index.html                      página principal — HTML + CSS + JS num só ficheiro,
                                as imagens são carregadas de ./assets
mama-resuelve-standalone.html   a mesma página com todas as imagens em base64;
                                ficheiro único e portátil (~4,3 MB), sem dependências locais
assets/                         imagens optimizadas usadas pela página (~3,2 MB)
hf_*.png, Print*.png            imagens originais, tal como saíram do gerador
.claude/launch.json             configuração do servidor de pré-visualização local
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
