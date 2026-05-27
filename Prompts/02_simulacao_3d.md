# 02 — SIMULAÇÃO 3D (Three.js)

> Especificação técnica do conteúdo do **modal de simulação** acionado no slide 11. Inspiração visual: `https://www.spacereference.org/` — mas com asteroides **sintéticos** (não dados reais do CSV), porque o foco é didático, não cartográfico.

---

## 1. Objetivo didático da simulação

Tornar visualmente óbvio para a banca **por que classificar PHA é difícil**:

1. Mostrar o sistema solar interior com os planetas em escala (não realista — escala didática).
2. Povoar o Cinturão Principal entre Marte e Júpiter com **muitos asteroides em cinza** (caso fácil — longe da Terra).
3. Colocar **alguns asteroides PHA em vermelho**, com órbitas excêntricas que **cruzam a vizinhança da Terra**.
4. Quando um PHA entra na **zona de risco da Terra (MOID < 0,05 UA)**, ele **pisca / deixa rastro vermelho** — torna concreto o critério usado no modelo.

## 2. Stack

- **Three.js r160+** via CDN (ES module preferido):
  ```html
  <script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
      }
    }
  </script>
  ```
  Depois, no script principal: `import * as THREE from 'three'; import { OrbitControls } from 'three/addons/controls/OrbitControls.js';`
- Sem outras libs.

## 3. Quando inicializar

- **Não** crie a cena no carregamento da página.
- Crie tudo **dentro de uma função `initSimulation()`** chamada apenas no `click` do botão `▶ INICIAR SIMULAÇÃO 3D` do slide 11.
- Quando o usuário fecha o modal: pare o `requestAnimationFrame` (não destrua a cena — guarde a referência para reabrir rápido).
- Quando o usuário sai do slide 11 (navega para outro slide): pause também.

## 4. Cena (estrutura)

### 4.1. Renderer / Camera / Controls
- `WebGLRenderer({ antialias: true, alpha: true })` — fundo transparente para o fundo estrelado do `body` aparecer atrás.
- `PerspectiveCamera(60, w/h, 0.1, 5000)`, posição inicial `(0, 80, 120)`, olhando para `(0, 0, 0)`.
- `OrbitControls`: `enableDamping = true`, `dampingFactor = 0.05`, `minDistance = 20`, `maxDistance = 400`.
- Background: cor `0x000510` ou transparente (preferir transparente — o fundo estrelado HTML aparece).

### 4.2. Luzes
- `AmbientLight(0x404060, 0.4)` — luz ambiente fraca azulada.
- `PointLight(0xfff2cc, 2.0, 0, 2)` no Sol (posição `0,0,0`) — luz amarelada, atenuação física.
- Opcional: `DirectionalLight` muito fraca para dar volume aos planetas.

### 4.3. Sol
- `SphereGeometry(4, 32, 32)` (raio em unidades de cena — NÃO em UA reais).
- `MeshBasicMaterial({ color: 0xffcc55 })` (não recebe sombra, ele é a fonte de luz).
- Adicione um `Sprite` com `MeshBasicMaterial` aditivo para um "halo" leve.

### 4.4. Planetas (representação didática, não em escala real)

| Planeta | Raio cena | Raio órbita (UA → unidades) | Cor | Velocidade orbital (rad/frame @ 60fps) |
|---|---|---|---|---|
| Mercúrio | 0.5 | 8 | 0xa0a0a0 | 0.0048 |
| Vênus | 0.9 | 14 | 0xe0c890 | 0.0035 |
| **Terra** | 1.0 | 20 | 0x4a90e2 | 0.0029 |
| Marte | 0.7 | 28 | 0xc1440e | 0.0023 |
| Júpiter | 2.5 | 60 | 0xd2a86b | 0.0013 |

(Conversão: 1 UA ≈ 20 unidades de cena. Júpiter está em 5,2 UA reais → 104 unidades, mas comprimimos para 60 para caber na vista — declare isso como **escala didática** em um pequeno `<small>` no canto do modal.)

- Geometria: `SphereGeometry(raio, 24, 24)`.
- Material: `MeshStandardMaterial({ color, roughness: 0.8, metalness: 0.1 })`.
- Cada planeta orbita o Sol em órbita **circular** (simplificação). Calcule posição com `x = R·cos(θ)`, `z = R·sin(θ)`, `y = 0`.
- Para a **Terra**: desenhe um anel `RingGeometry` extra de raio `20 ± 1.0` (representa a zona de **MOID < 0,05 UA** — exagerada para visibilidade), com material translúcido vermelho `0xff3030` opacidade 0,15. Este é o **anel de risco**.

### 4.5. Órbitas (linhas de referência)

- Para cada planeta, desenhe a órbita circular como `Line` ou `LineLoop` (geometria de 128 vértices). Cor cinza-escuro `0x404060`, opacidade 0,3.
- Toggle "Mostrar órbitas" no painel de controles (default: ligado).

### 4.6. Asteroides do Cinturão Principal (não-PHA, ilustrativos)

- Quantidade: **~600 asteroides**.
- Para performance: use **`InstancedMesh`** (não `Mesh` individual).
- Geometria base: `SphereGeometry(0.1, 6, 6)` (low-poly).
- Cor: cinza variando entre `0x707080` e `0x9090a0`.
- Distribuição:
  - Semi-eixo maior `a`: aleatório uniforme entre **2,2 UA e 3,3 UA** (escala cena: 44 a 66).
  - Excentricidade `e`: aleatório entre 0 e 0,2 (órbitas quase circulares).
  - Inclinação `i`: aleatório entre −10° e +10° (próximo do plano eclíptico).
  - Fase orbital inicial: uniforme `[0, 2π)`.
- Movimento: cada asteroide percorre uma elipse aproximada. Para simplificar, **aproxime por órbita circular** no semi-eixo maior (a banca não vai checar mecânica Kepleriana exata). Velocidade angular ∝ `1 / a^1.5` (Kepler) — basta um fator multiplicador comum.

### 4.7. Asteroides PHA (estrelas do show — sintéticos, vermelhos)

- Quantidade: **20 PHAs**.
- Geometria base: `SphereGeometry(0.18, 8, 8)` (um pouco maiores que os do cinturão).
- Cor base: `0xff4040` (vermelho vivo).
- Material: `MeshBasicMaterial` (auto-iluminado, não precisa receber luz para destacar).
- Órbita: elíptica **com cruzamento da órbita da Terra**.
  - Para cada PHA, sorteie:
    - `q` (periélio em UA): aleatório entre 0,5 e 0,98 (todos passam dentro da órbita da Terra) → em unidades cena: 10 a 19,6.
    - `Q` (afélio em UA): aleatório entre 1,3 e 3,5 → em unidades cena: 26 a 70.
    - Calcule `a = (q+Q)/2`, `e = (Q-q)/(Q+q)`.
    - Inclinação `i`: aleatório entre −30° e +30°.
    - Fase inicial `M0`: uniforme.
  - **Use órbita elíptica de verdade** (não circular) — desenhe a elipse com `EllipseCurve` ou parametrize manualmente:
    - `r(θ) = a·(1−e²) / (1 + e·cos(θ))`
    - Posicione o foco da elipse no Sol (origem).
    - Aplique a inclinação rotacionando o plano da órbita em torno do eixo X.
- Desenhe a **trajetória de cada PHA** como uma linha de cor vermelho-escuro `0x802020`, opacidade 0,4, sempre visível (não só quando o PHA passa por ali).

### 4.8. Lógica de "cruzamento de zona de risco"

A cada frame, para cada PHA:
1. Calcule a posição da Terra `pT` e do PHA `pA` neste frame.
2. Distância 3D `d = |pA − pT|`.
3. Se `d < 1.5` (unidades cena — corresponde a ~0,075 UA, levemente exagerado para ser visível): ative **modo perigo** no PHA:
   - Cor pisca entre `0xff4040` e `0xffaa00` a 4Hz.
   - Adicione um halo (Sprite aditivo) ao redor do PHA durante 1s após sair da zona.
   - Emita uma trilha (`BufferGeometry` com últimas N posições) por 2s.
4. Quando sai da zona, volta ao estado normal.

Este efeito é o **clímax didático** da simulação. Garanta que aconteça pelo menos uma vez por minuto (ajuste velocidades para que isso seja frequente).

### 4.9. Cinturão de asteroides — destaque visual opcional
- Renderize um disco translúcido (`RingGeometry(44, 66, 64)`) no plano XZ, opacidade 0,06, cor `0xaaaaaa`. Apenas ajuda o olho a localizar o cinturão.

## 5. Painel de controles (HTML overlay sobre o canvas)

Posicionar no canto inferior do modal. Estilo coerente com `03_estilo_visual.md`.

```
┌─────────────────────────────────────────────────────────┐
│  [▶ Play / ⏸ Pause]                                     │
│  Velocidade: [─────●─────] (slider, 0.1x a 10x)         │
│  ☑ Mostrar órbitas    ☑ Mostrar zona de risco          │
│  [📷 Vista de cima]  [📷 Vista lateral]  [📷 Resetar]  │
│  PHAs ativos na zona de risco: 0                       │
└─────────────────────────────────────────────────────────┘
```

- **Play/Pause:** alterna `clock.running` ou um flag `simRunning`. Default: rodando.
- **Slider de velocidade:** multiplicador `simSpeed` aplicado ao avanço temporal (`dt`). Default: 1x.
- **Toggles** controlam visibilidade dos grupos `THREE.Group` correspondentes.
- **Botões de câmera:**
  - "Vista de cima": câmera vai para `(0, 200, 0.001)` olhando origem, suave (`lerp` em 1s).
  - "Vista lateral": `(0, 5, 150)`.
  - "Resetar": `(0, 80, 120)`.
- **Contador de PHAs na zona:** atualizado a cada frame, mostra o número de PHAs com `d < 1.5` agora.

## 6. Botão de fechar

- Botão `✕ Fechar simulação (ESC)` no canto superior direito do modal.
- Tecla `ESC` também fecha.
- Ao fechar: `cancelAnimationFrame`, oculta modal (`display: none`), libera atalhos de slides.

## 7. Responsividade

- O canvas Three.js deve ocupar **100% do modal**.
- Listener de `resize` ajusta `renderer.setSize()` e `camera.aspect`.
- Em tela do projetor (geralmente 1920×1080 ou 1280×720), nada deve cortar.

## 8. Performance — alvos

- **60 FPS** com 600 asteroides do cinturão + 20 PHAs + 5 planetas, em hardware modesto (notebook integrado).
- `InstancedMesh` obrigatório para os 600 do cinturão.
- Para os 20 PHAs, `Mesh` individual está ok (precisam de animação/cor independente).
- Use `BufferGeometryUtils` se for fazer trilhas — não recrie buffers a cada frame.

## 9. Loop de animação (esqueleto)

```js
const clock = new THREE.Clock();
let simRunning = true;
let simSpeed = 1.0;

function animate() {
  rafId = requestAnimationFrame(animate);
  controls.update();

  if (simRunning) {
    const dt = clock.getDelta() * simSpeed;
    t += dt;
    updatePlanets(t);
    updateBeltAsteroids(t);
    updatePHAs(t);   // inclui detecção de zona de risco
    updateRiskCounter();
  }

  renderer.render(scene, camera);
}
```

## 10. Mensagens em português dentro da simulação

- Tooltip ao passar mouse num PHA (opcional, se for fácil): `"Asteroide PHA sintético #N"`.
- Texto fixo no canto inferior esquerdo:
  > Simulação didática — escala visual ajustada. Dados sintéticos coerentes com a literatura. Asteroides PHA em vermelho cruzam a vizinhança da Terra (MOID simulado < 0,05 UA).

## 11. Não fazer

- **Não** carregue texturas externas de planetas (deixa pesado e quebra offline). Use cores sólidas + iluminação.
- **Não** use `PointsMaterial` para os asteroides do cinturão — perde profundidade. Use `InstancedMesh` com esferas low-poly.
- **Não** implemente colisões físicas, gravidade real, ou propagação Kepleriana exata. É didático.
- **Não** misture unidades reais (km, kg, segundos) com unidades de cena. Use só unidades de cena e declare a escala.
