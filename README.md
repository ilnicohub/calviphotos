# Portfolio Foto - Static Galleries

Questo repository contiene un sito statico (HTML/CSS/JS) che mostra le gallerie fotografiche.

Come funziona (automazione):
- Metti le tue foto in cartelle sotto `photos/`, ad esempio `photos/2025-11-23-Torneo/`
- A ogni push su `main` (o `master`) GitHub Actions esegue lo script `scripts/generate_galleries.py`:
  - genera thumbnails in `photos/<galleria>/thumbs/`
  - crea `photos/<galleria>/index.json` con l'elenco delle foto
  - crea `galleries.json` in root con le gallerie trovate
  - committa le modifiche (thumbnails e JSON) nel repo

Configurazione richiesta:
- Abilita GitHub Pages sulle impostazioni del repository (branch `main` e root `/`).

Struttura consigliata per upload delle foto:

```
photos/
  2025-11-23-Real-vs-Juventus/
    IMG_001.jpg
    IMG_002.jpg
    ...

  2025-11-30-Inter-vs-Milan/
    ...
```

Dopo il push su `main`:
- Action genera le thumbnail e i file `index.json`
- Apri la homepage (`index.html`) che userà `galleries.json` per creare le card
- Cliccando una card si apre `gallery.html?g=<folder>` con la galleria

Modifiche e personalizzazioni:
- Se vuoi generare localmente le thumbnails, esegui: `python3 scripts/generate_galleries.py` (richiede Python e `pip install -r requirements.txt`).
- Cambia dimensione dei thumbnails editando `scripts/generate_galleries.py` (parametro `width` nella funzione `make_thumb`).

Se vuoi, posso:
- aggiungere un deploy script automatico
- migliorare la visualizzazione (lazy-loading progressivo, categoria/filtri)
