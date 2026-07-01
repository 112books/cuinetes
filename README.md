# Cuinetes

Bloc de receptes en català. Hugo static site → GitHub Pages.

**Producció:** https://cuinetes.linuxbcn.com  
**Local:** `hugo server -D` → http://localhost:1313

---

## Afegir una recepta nova

### 1. Crea el fitxer

```bash
hugo new receptes/nom-de-la-recepta.md
```

O copia un fitxer existent de `content/receptes/` i canvia el nom.

### 2. Edita el front matter

```yaml
---
title: "Patates al forn amb romero"
date: 2024-03-15
draft: false
categories: ["guarnicions"]
tags: ["patates", "forn", "vegetarià"]
dificultat: "fàcil"       # fàcil | mitjana | avançada
temps: "45 min"
racions: 4
image: "/images/receptes/patates-al-forn.jpg"
lead: "Crujents per fora i tendres per dins."
---
```

**Categories disponibles:** `entrants` · `primers` · `segons` · `guarnicions` · `postres` · `brunch` · `begudes`

**Tags:** ingredients principals en singular (`patata`, `ou`, `tomàquet`), tècniques (`forn`, `vapor`), restriccions (`vegetarià`, `vegà`, `sense-gluten`), temporades (`tardor`, `hivern`, `primavera`, `estiu`)

### 3. Afegeix la imatge

Copia la foto a `static/images/receptes/` amb el mateix nom que poses al camp `image`.

Format recomanat: JPG, 1200×800px mínim.

### 4. Escriu el contingut

```markdown
## Ingredients

- 800 g de patates
- 3 branques de romero fresc
- Oli d'oliva verge extra

## Elaboració

1. Preescalfa el forn a 200 °C.
2. ...

## Notes

Pots substituir el romero per farigola.
```

### 5. Publica

```bash
./sync-cuinetes.sh
# → opció 2 → escriu el missatge de commit
```

El GitHub Action desplegarà el site automàticament en 1-2 minuts.

---

## Gestió del site

```bash
./sync-cuinetes.sh
```

| Opció | Acció |
|-------|-------|
| 1 | Status del repo |
| 2 | Sync (commit + push) |
| 3 | Servidor local |
| 4 | Build local |
| 5 | Deploy producció |
| r | Nova recepta |

---

## Estructura

```
content/receptes/       → fitxers Markdown de cada recepta
static/images/receptes/ → fotos de les receptes
static/admin/           → dashboard d'estadístiques (/admin/)
themes/cuinetes/        → tema custom (CSS, layouts, JS)
```

---

## Dashboard d'estadístiques

Accessible a https://cuinetes.linuxbcn.com/admin/  
Protegit per contrasenya (mateixa que els altres projectes linuxbcn).

Requereix secret `GOATCOUNTER_TOKEN` a GitHub → Settings → Secrets.
