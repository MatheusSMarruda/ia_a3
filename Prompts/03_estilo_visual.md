# 03 — ESTILO VISUAL

> Especificação visual da apresentação. Tema **espacial escuro**, sem alternância para tema claro. Toda a estilização deve ficar inline no `<style>` do HTML único.

---

## 1. Paleta de cores (use exatamente estes tokens)

```css
:root {
  /* Fundo */
  --bg-deep:       #03061a;   /* azul-marinho quase preto — fundo principal */
  --bg-panel:      #0a1130;   /* azul escuro — cards, tabelas */
  --bg-elevated:   #131a44;   /* azul médio escuro — destaques de card */

  /* Texto */
  --text-primary:  #e8ecff;   /* branco azulado — corpo */
  --text-muted:    #8892c4;   /* cinza azulado — captions, labels */
  --text-dim:      #5a6296;   /* mais apagado — rodapés */

  /* Accent (cor principal de destaque — neon) */
  --accent:        #5eead4;   /* turquesa neon — títulos, números, borders */
  --accent-glow:   rgba(94, 234, 212, 0.4);

  /* Alerta / PHA */
  --danger:        #ff4d6d;   /* vermelho coral — usado para PHA, falsos negativos */
  --danger-glow:   rgba(255, 77, 109, 0.45);

  /* Acento secundário */
  --warning:       #ffb454;   /* âmbar — atenção, métricas medianas */
}
```

- Contraste mínimo `--text-primary` sobre `--bg-deep`: ~16:1 (ok).
- Não use cores fora da paleta. Se precisar de uma variação, derive com `color-mix()` ou opacidade.

## 2. Tipografia

- **Títulos (h1, h2):** `'Orbitron', sans-serif`, peso 600/800, `letter-spacing: 0.04em`, **maiúsculas só para o `<h1>` da capa** (resto preserva capitalização normal).
- **Corpo:** `'Space Mono', monospace`, peso 400. Pesos 700 para destaques.
- **Tamanhos (rem-based, base 16px):**
  - `h1` capa: `clamp(2.5rem, 6vw, 5rem)`
  - `h2` títulos de slide: `clamp(1.8rem, 3.5vw, 3rem)`
  - `h3` subtítulos / cards: `1.4rem`
  - corpo: `clamp(1rem, 1.4vw, 1.25rem)`
  - small / caption: `0.85rem`
- **Line-height:** 1.5 corpo, 1.2 títulos.

## 3. Layout dos slides

```css
#deck {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.slide {
  position: absolute;
  inset: 0;
  padding: clamp(2rem, 5vh, 5rem) clamp(2rem, 6vw, 6rem);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  opacity: 0;
  visibility: hidden;
  transition: opacity 350ms ease, transform 350ms ease;
  transform: translateY(20px);
  pointer-events: none;
}

.slide.active {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  pointer-events: auto;
}
```

- **Apenas o slide ativo é visível.** Use a classe `.active` controlada por JS.
- Transição: fade + leve slide vertical (20px). Duração 350ms.
- Em `prefers-reduced-motion: reduce`, zere a transição e o transform.

## 4. Fundo estrelado animado

Use um `<canvas id="stars-bg">` posicionado `fixed` cobrindo a viewport, atrás de tudo (`z-index: -1`).

Implementação 2D simples:
- Gere ~180 estrelas com posição (x, y), raio (0.4 a 1.8px), brilho base (0.3 a 1.0) e fase de twinkle (`Math.random() * Math.PI * 2`).
- A cada frame, `requestAnimationFrame`: para cada estrela, brilho = `base + 0.3 * Math.sin(t + fase)`. Desenhe como círculos brancos com `globalAlpha = brilho`.
- A cada 30s, escolha uma estrela aleatória e dispare uma "shooting star" (linha curta com gradiente) — discreto, no máximo 1 por slide.
- Sob `prefers-reduced-motion`: não anime; renderize estrelas estáticas uma vez.
- Quando o modal de simulação 3D abre: pause este loop (`cancelAnimationFrame`).

## 5. Cards e tabelas

```css
.card {
  background: var(--bg-panel);
  border: 1px solid color-mix(in srgb, var(--accent) 20%, transparent);
  border-radius: 12px;
  padding: 1.5rem 1.75rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(94, 234, 212, 0.05) inset;
}

.card--accent {
  border-color: var(--accent);
  box-shadow: 0 0 32px var(--accent-glow);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Space Mono', monospace;
}
th {
  background: var(--bg-elevated);
  color: var(--accent);
  text-align: left;
  padding: 0.75rem 1rem;
  font-weight: 700;
  border-bottom: 2px solid var(--accent);
}
td {
  padding: 0.65rem 1rem;
  border-bottom: 1px solid rgba(94, 234, 212, 0.1);
}
tr.highlight td {
  background: rgba(94, 234, 212, 0.08);
  color: var(--accent);
  font-weight: 700;
}
```

- Linha destacada na tabela de métricas (slide 10) usa `.highlight`.

## 6. Botões

```css
.btn {
  font-family: 'Orbitron', sans-serif;
  font-weight: 600;
  letter-spacing: 0.06em;
  background: transparent;
  color: var(--accent);
  border: 1.5px solid var(--accent);
  padding: 0.7rem 1.4rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 200ms ease;
  text-transform: uppercase;
}
.btn:hover {
  background: var(--accent);
  color: var(--bg-deep);
  box-shadow: 0 0 24px var(--accent-glow);
}

.btn--giant {
  font-size: 1.5rem;
  padding: 1.2rem 2.4rem;
  border-width: 2px;
  box-shadow: 0 0 32px var(--accent-glow);
  animation: pulse-glow 2.4s ease-in-out infinite;
}
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 24px var(--accent-glow); }
  50%      { box-shadow: 0 0 48px var(--accent-glow); }
}
```

- `.btn--giant` é o botão **"INICIAR SIMULAÇÃO 3D"** do slide 11.

## 7. Barra de navegação inferior

```css
#controls {
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: rgba(10, 17, 48, 0.7);
  backdrop-filter: blur(10px);
  padding: 0.5rem 1.25rem;
  border-radius: 999px;
  border: 1px solid rgba(94, 234, 212, 0.2);
  z-index: 10;
}
#controls button {
  background: transparent;
  border: none;
  color: var(--accent);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.4rem 0.7rem;
}
#counter {
  font-family: 'Space Mono', monospace;
  color: var(--text-muted);
  font-size: 0.9rem;
}
```

## 8. Barra de progresso superior

```css
#progress-bar {
  position: fixed;
  top: 0; left: 0;
  width: 100%;
  height: 3px;
  background: rgba(94, 234, 212, 0.08);
  z-index: 10;
}
#progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), #a78bfa);
  width: 0%;
  transition: width 300ms ease;
  box-shadow: 0 0 8px var(--accent-glow);
}
```

- Largura = `(slide_atual / total) * 100%`.

## 9. Imagens dos gráficos

```css
.figure {
  background: var(--bg-panel);
  border: 1px solid rgba(94, 234, 212, 0.15);
  border-radius: 10px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.figure img {
  width: 100%;
  height: auto;
  border-radius: 6px;
  cursor: zoom-in;     /* indica que abre lightbox */
}
.figure figcaption {
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
}
```

## 10. Lightbox (para slide 10)

- Overlay `position: fixed; inset: 0; background: rgba(0,0,0,0.92); z-index: 100`.
- Imagem grande centralizada (`max-width: 90vw; max-height: 90vh`).
- Botão `✕` no canto superior direito + clique no overlay + ESC para fechar.
- Quando aberto: desativar atalhos de navegação de slides.

## 11. Modal da simulação 3D

```css
#simulation-modal {
  position: fixed;
  inset: 0;
  background: var(--bg-deep);
  z-index: 50;
  display: none;
}
#simulation-modal.open {
  display: block;
}
#three-canvas-wrapper {
  width: 100%;
  height: 100%;
}
#sim-controls {
  position: absolute;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(10, 17, 48, 0.85);
  backdrop-filter: blur(12px);
  padding: 1rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(94, 234, 212, 0.25);
  display: flex;
  gap: 1.25rem;
  align-items: center;
  flex-wrap: wrap;
  max-width: 90vw;
}
#close-sim {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  z-index: 51;
}
```

## 12. Animações de entrada do slide ativo

```css
@keyframes slide-in-up {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
.slide.active > * {
  animation: slide-in-up 500ms ease backwards;
}
.slide.active > *:nth-child(1) { animation-delay: 0ms; }
.slide.active > *:nth-child(2) { animation-delay: 80ms; }
.slide.active > *:nth-child(3) { animation-delay: 160ms; }
.slide.active > *:nth-child(4) { animation-delay: 240ms; }
.slide.active > *:nth-child(5) { animation-delay: 320ms; }
.slide.active > *:nth-child(6) { animation-delay: 400ms; }
```

- Efeito stagger nos filhos diretos do slide ativo: cada um aparece com 80ms de atraso.
- Desligado sob `prefers-reduced-motion`.

## 13. Responsividade mínima

- Alvo principal: **1920×1080** e **1280×720** (projetor).
- Notebook 13": testar em 1366×768 também.
- Para telas < 900px: as colunas de 2 colunas (slides 6, 7, 10) viram 1 coluna empilhada.
- Não otimize para mobile (não é o caso de uso).

## 14. Diretrizes de uso da cor accent

- `--accent` (turquesa neon) só em: títulos h1/h2, números importantes, bordas de cards destacados, botões, ícones, valores de tabela em destaque.
- **Não use** accent em parágrafos inteiros — perde força.
- `--danger` (vermelho) só em: PHA, falsos negativos, alerta.
- `--warning` (âmbar) só em: termos de atenção, valores medianos, ícones de alerta.

## 15. Detalhes finos

- `scroll-behavior: smooth` no `<html>`.
- `cursor: default` por padrão, `cursor: pointer` em elementos interativos.
- `user-select: none` na barra de navegação (evitar seleção acidental).
- `user-select: text` permitido no corpo dos slides (banca pode querer copiar números).
- `outline: 2px solid var(--accent)` no `:focus-visible` de botões e links — acessibilidade.

## 16. Checklist visual final

- [ ] Fonte Orbitron carrega e aplica nos h1/h2.
- [ ] Fonte Space Mono carrega e aplica no corpo.
- [ ] Fundo estrelado anima suavemente em todos os slides exceto durante a simulação 3D.
- [ ] Transição entre slides é fluida (fade + slide-up).
- [ ] Tabela do slide 10 tem linha destacada em accent.
- [ ] Botão "INICIAR SIMULAÇÃO 3D" pulsa.
- [ ] Sem flicker ao trocar de slide.
- [ ] Barra de progresso superior preenche conforme o slide avança.
- [ ] Contador `N / 12` legível.
