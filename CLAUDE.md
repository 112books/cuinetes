# CLAUDE.md — cuinetes.linuxbcn.com

> Guia operativa per a Claude Code en aquest projecte.

## Projecte

**Cuinetes** — bloc de receptes en català. Migració de WordPress.org a Hugo (static site generator). Senzill, net i ràpid. Sense JavaScript innecessari, sense frameworks CSS externs.

- **Producció:** `https://cuinetes.linuxbcn.com` → GitHub Pages (branca `main`)
- **Local:** `hugo server -D` → `http://localhost:1313`
- **DNS:** gestionat des de Dinahosting
- **Origen:** exportació de WordPress (fitxer XML a `_wordpress-export/`)

---

## Stack tècnic

| Capa | Tecnologia |
|------|-----------|
| SSG | Hugo v0.159+ extended |
| Tema | Custom `themes/cuinetes/` |
| CSS | Vanilla CSS amb custom properties (cap framework) |
| JS | Cap (o mínim: cercador estàtic) |
| Idioma | CA (català) — únic idioma, sense selector |
| Analytics | GoatCounter (sense cookies, GDPR) |
| DNS/Domini | Dinahosting |
| Hosting | GitHub Pages |

**Fonts (autoallotjades a `static/fonts/`):**  
Per definir — candidates: `Lora` (títols, serifada elegant) + `Inter` o `Source Sans` (cos del text)

---

## Entorns

### Local
```bash
hugo server -D              # amb drafts
hugo server -D --port 1314  # si 1313 ocupat
```

### Producció (branca main)
```bash
git push origin main        # activa GitHub Action → GitHub Pages
```

### Build de producció
```bash
hugo --minify
```

---

## Estructura de directoris

```
cuinetes.linuxbcn.com/
├── .github/workflows/         # CI/CD GitHub Actions
├── themes/cuinetes/           # tema custom
│   ├── assets/css/main.css    # tots els estils
│   ├── assets/js/             # mínim o buit
│   └── layouts/
│       ├── _default/          # baseof.html, list.html, single.html
│       ├── receptes/          # list i single de recepta
│       ├── index.html         # portada
│       └── partials/          # head, header, footer, recepta-card
├── content/
│   └── receptes/              # totes les receptes en Markdown
├── data/                      # llistes estàtiques (temporades, etc.)
├── i18n/
│   └── ca.yaml                # strings UI (butons, labels, etc.)
├── static/
│   ├── fonts/                 # woff2 autoallotjades
│   ├── images/
│   │   └── receptes/          # fotos de cada recepta
│   └── CNAME                  # cuinetes.linuxbcn.com
├── archetypes/
│   └── receptes.md            # plantilla per a recepta nova
├── _wordpress-export/         # fitxer XML original + scripts de migració
├── scripts/
│   └── wp-to-hugo.py          # script de migració WordPress → Markdown
├── hugo.toml                  # configuració principal
└── CLAUDE.md                  # aquest fitxer
```

---

## Configuració Hugo (`hugo.toml`)

```toml
baseURL = "https://cuinetes.linuxbcn.com/"
title   = "Cuinetes"
theme   = "cuinetes"
defaultContentLanguage = "ca"
enableRobotsTXT = true
summaryLength   = 60

[params]
  author          = "Joan Martínez i Serres"
  description     = "Receptes casolanes. Senzilles, bones i en català."
  goatcounterSite = "cuinetes"

[taxonomies]
  categoria = "categories"
  tag       = "tags"

[outputs]
  home    = ["HTML", "RSS"]
  section = ["HTML", "RSS"]
```

---

## Tipus de contingut: Recepta

Cada recepta és un fitxer Markdown a `content/receptes/`.

### Front matter
```yaml
---
title: "Patates al forn amb romero"
date: 2024-03-15
draft: false
categories: ["guarnicions"]
tags: ["patates", "forn", "vegetarià"]
dificultat: "fàcil"          # fàcil | mitjana | avançada
temps: "45 min"
racions: 4
image: "/images/receptes/patates-al-forn.jpg"
lead: "Crujents per fora i tendres per dins. Una guarnició que no falla mai."
---
```

### Cos del document
```markdown
## Ingredients

- 800 g de patates
- 3 branques de romero fresc
- Oli d'oliva verge extra
- Sal i pebre

## Elaboració

1. Preescalfa el forn a 200 °C.
2. ...

## Notes

Pots substituir el romero per farigola o sàlvia.
```

---

## Taxonomies

Dos sistemes de classificació independents, ambdós amb pàgina de llistat automàtica Hugo:

### Categories (tipus de plat)
Navegació principal. Cada recepta pertany a **una sola** categoria:
- `entrants` — amanides, cremes, aperitius
- `primers` — arrossos, pastes, llegums, sopes
- `segons` — carn, peix, ou
- `guarnicions` — verdures, patates
- `postres` — dolços, fruita, gelats
- `brunch` — esmorzars i berenars
- `begudes` — sucs, infusions, còctels sense alcohol

### Ingredients com a etiquetes (`tags`)
**Els ingredients principals de cada recepta s'afegeixen com a tags.** Això permet trobar totes les receptes que usen un ingredient concret (ex.: totes les de `carbassó`, `pollastre`, `llimona`).

Convencions de tagging:
- Ingredient en singular: `patata`, `ou`, `tomàquet`, `anxova`
- Tècnica culinària: `forn`, `vapor`, `crema`, `saltejat`
- Restricció dietètica: `vegetarià`, `vegà`, `sense-gluten`, `sense-lactosa`
- Temporada: `tardor`, `hivern`, `primavera`, `estiu`

Una recepta pot tenir tants tags com ingredients/tècniques rellevants. La pàgina `/tags/` servirà com a índex d'ingredients navegable.

---

## Sistema visual

### Logotip
- Fitxer: `Cuinetes-Logotip.png` a l'arrel → copiar a `static/images/logotip/`
- Composició: "LinuxBCN" en gris clar damunt, il·lustració botànica (flor), "Cuinetes" en negre gran sota
- Estètica: neta, orgànica, fons blanc — marca el to visual de tot el lloc

### Paleta (derivada del logotip)
```css
--bg:      #ffffff   /* blanc pur — fons principal */
--bg2:     #f7f5f2   /* crema molt suau — fons seccions alternes */
--fg:      #1a1a1a   /* negre gairebé pur — text principal */
--mid:     #888888   /* gris — text secundari, metadades (com "LinuxBCN" al logo) */
--line:    #e8e4df   /* separadors subtils */
--accent:  #3d6b3a   /* verd herba — accent principal (botànic) */
--accent2: #8b6914   /* daurat ocre — accent secundari / tags d'ingredients */
```

### Principis de disseny
- **Net i orgànic** — inspira el logotip: tipografia robusta + il·lustració delicada
- **Lleuger i llegible** — la recepta és el contingut, no el disseny
- **La foto mana** — imatge destacada gran a la capçalera de cada recepta
- **Tipografia clara** — cos de text prou gran (18px mínim), bona interlinea
- **Sense distraccions** — zero publicitat, zero popups, zero newsletter forçada
- **Mòbil primer** — la majoria de visites seran des del mòbil mentre es cuina

### Identitat visual — originalitat

**Cuinetes no ha de semblar un blog de receptes estàndard.** El logotip marca la diferència: tipografia robusta + botànica delicada. El lloc ha de tenir aquesta mateixa tensió.

Referents d'estètica (NO copiar, inspirar):
- Llibres d'Ottolenghi — editorial, tipografia gran, espai blanc generós
- Canal House — casolà però elegant, fotografies honestes
- Revistes com Lucky Peach o Fool — editorialisme, caràcter

**Decisions de disseny que fan la diferència:**
- Títols molt grans a la portada (3–5rem) — la tipografia com a element visual
- Il·lustracions botàniques SVG petites com a separadors o decoració de categoria (derivades del logotip)
- Les targes de recepta (`recepta-card`) amb tipografia gran, menys quadriculades — asimètriques, vives
- La pàgina de la recepta: ingredients en columna lateral (desktop) mentre s'elabora
- Tags d'ingredient amb pastilla de color subtil (--accent2) — navegables i visuals
- Fons blanc pur a la recepta, cremós a la portada i categories

### Disseny de la recepta (single)
1. Imatge de capçalera (full-width, gran — mínimo 60vh)
2. Títol gran + lead
3. Metadades en línia: temps · racions · dificultat
4. Tags d'ingredients (pastilles clicables → pàgina de l'ingredient)
5. Dos columnes (desktop): `ingredients` (sticky) | `elaboració` (scrollable)
6. Notes / variacions
7. Receptes relacionades (per categoria o per ingredient compartit)

---

## Migració des de WordPress

### Fitxers
- `_wordpress-export/cuinetes.WordPress.xml` — exportació XML original
- `scripts/wp-to-hugo.py` — script Python per convertir posts → Markdown

### Procés de migració
1. Exportar XML des de WordPress Admin → Eines → Exportar
2. Executar `python scripts/wp-to-hugo.py` → genera fitxers `.md` a `content/receptes/`
3. Revisar el front matter generat (categories, tags, dates)
4. Descarregar imatges del WordPress original → `static/images/receptes/`
5. Actualitzar les URLs d'imatges al Markdown (o usar un script)
6. Revisar i polir el contingut convertit (el HTML de WP pot deixar brutícia)

### Eines de migració útils
```bash
# wordpress-to-hugo-exporter (plugin PHP) — alternativa
# o: https://github.com/SchumacherFM/wordpress-to-hugo-exporter

# Per baixar imatges massivament:
wget -r -np -A jpg,jpeg,png,webp https://cuinetes.linuxbcn.com/wp-content/uploads/
```

---

## Archetip de recepta (`archetypes/receptes.md`)

```markdown
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
categories: []
tags: []
dificultat: "fàcil"
temps: ""
racions: 4
image: ""
lead: ""
---

## Ingredients

-

## Elaboració

1.

## Notes

```

### Crear recepta nova
```bash
hugo new receptes/nom-de-la-recepta.md
```

---

## Analytics (GoatCounter)

- Site: `cuinetes.goatcounter.com` (crear compte)
- Integrat al `<head>` via partial `head.html`
- Sense cookies, GDPR-compliant

```html
<script data-goatcounter="https://cuinetes.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

---

## Dashboard d'estadístiques (`/admin/`)

Dashboard idèntic al de `pocallum.cat` i `about.pocallum.cat`. Codi font a `../goatcounter-dashboard/`.

### Fitxers
```
static/
└── admin/
    ├── index.html        # dashboard HTML autocontingut, protegit per contrasenya SHA-256
    └── analytics.json    # dades generades cada hora per GitHub Actions
scripts/
├── build-analytics-json.py   # agrega les respostes de l'API GoatCounter
└── process-analytics.py      # transforma a analytics.json
.github/workflows/
└── fetch-analytics.yml       # cron cada hora → commit analytics.json
```

### Configuració del dashboard (`static/admin/index.html`)
Tres valors a canviar respecte la plantilla base del repositori `goatcounter-dashboard`:
```js
siteName: 'cuinetes.linuxbcn.com',
gcUrl:    'https://cuinetes.goatcounter.com',
pwHash:   'ec689a6b20231cab576cd7604ab478777e3e23bd4e4822dbc841779afa57fbbf',
```

**El `pwHash` és el mateix que a `pocallum.cat` i `about.pocallum.cat`** — mateixa contrasenya compartida.

### Secret requerit a GitHub
```
Nom del secret:  GOATCOUNTER_TOKEN
Valor:           token generat a cuinetes.goatcounter.com → Settings → API tokens
Permís:          Read stats ✓
```

### GitHub Action (`fetch-analytics.yml`)
Única diferència respecte about-pocallum: `GC_ACCOUNT: "cuinetes"`.
Copia el workflow de `../about-pocallum/.github/workflows/fetch-analytics.yml` i canvia aquesta variable.

### Contrasenya del dashboard
Hash SHA-256 ja configurat. Si mai cal canviar-la:
```bash
echo -n "nova_contrasenya" | shasum -a 256
```

### ⚠️ Compte: email GoatCounter verificat
L'email del compte GoatCounter ha d'estar verificat — sense verificació, l'API retorna 401 tot i que el token sembli correcte. El mail de verificació sol anar a l'spam.

### Repositori de referència
`../goatcounter-dashboard` — codi font del dashboard i wizard d'instal·lació (`bash scripts/setup.sh`)

---

## GitHub Actions (`.github/workflows/deploy.yml`)

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: 'latest'
          extended: true
      - name: Build
        run: hugo --minify
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
          cname: cuinetes.linuxbcn.com
```

---

## To i veu

- **Idioma:** català — sempre
- **To:** proper, casolà, sense pretensions — com una amiga que t'explica una recepta
- **Evitar:** tecnicismes innecessaris, anglicismes, to de restaurant gourmet, castellanismes
- **Exemple de veu:** "Fàcil, bo i sense complicar-se la vida."

---

## Fases del projecte

### Fase 1 — Base Hugo
- [ ] Inicialitzar repo Hugo amb tema custom bàsic
- [ ] `hugo.toml` amb taxonomies i paràmetres
- [ ] Layouts: `baseof`, `index`, `receptes/list`, `receptes/single`
- [ ] CSS base: tipografia, paleta, layout responsive
- [ ] GitHub Actions per a deploy automàtic
- [ ] Dashboard `/admin/` — copiar de `../goatcounter-dashboard`, adaptar `siteName`/`gcUrl`/`pwHash`
- [ ] GitHub Action `fetch-analytics.yml` (cron horari) + secret `GOATCOUNTER_TOKEN`

### Fase 2 — Migració de contingut
- [ ] Descarregar XML d'exportació de WordPress
- [ ] Script de migració WP → Markdown
- [ ] Migrar imatges a `static/images/receptes/`
- [ ] Revisar i netejar contingut migrat

### Fase 3 — Funcionalitats
- [ ] Pàgina d'índex per categoria
- [ ] Pàgina d'índex per tag
- [ ] Cercador estàtic (Pagefind o Fuse.js)
- [ ] RSS feed
- [ ] Sitemap

### Fase 4 — Tall
- [ ] DNS apunta a GitHub Pages
- [ ] Redireccionaments (si cal) des de URLs antigues de WP
- [ ] WordPress en mode manteniment o desactivat

---

## Fora d'abast (ara per ara)

- Comentaris (Disqus, etc.)
- Newsletter
- Multilingüe
- E-commerce / monetització
- Backend d'administració
