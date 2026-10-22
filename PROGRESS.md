# PROGRESS — session log (the agent appends one entry at the end of each session)

## 2026-09-28 — agent harness setup
- Done: git re-rooted at the project root (`site/.git` → repo root, `site/` now a
  subfolder); installed the adapted harness (`scripts/check.sh`, `.githooks/`,
  `.github/workflows/`, `AGENTS.md`, `docs/architecture.md`, `features.json`).
- Decisions: no lint/type/test toolchain (see `docs/decisions/0001-baseline.md`);
  `check.sh` is syntax/JSON only; GitHub Pages must switch to Actions (site/ is no
  longer the deploy root).
- To watch: the live site will 404 until Settings → Pages → Source = "GitHub Actions".
  `cv.pdf` and `assets/video/lepotager.mp4` are still missing content TODOs.

## 2026-09-28 — static site generator (0002)
- Done: added `tools/build_site.py` + `site-src/` (layout, partials, pages.json,
  page bodies); regenerated `site/*.html`; added `tools/test_site.py` (stdlib
  unittest) and two check.sh steps (generated-site freshness + tests).
- Decisions: zero-dependency generator, generated HTML stays committed
  (see `docs/decisions/0002-site-generator.md`). Project pages gained a
  meta description and Open Graph tags.
- Verified: `index.html` reproduced byte-for-byte; project pages gained exactly
  3 metadata lines each. `./scripts/check.sh` green.
- To watch: never hand-edit `site/*.html`; edit `site-src/` then rebuild.

## 2026-09-28 — contenu du portfolio (site-content.md)
- Fait : home réécrite selon le spec (Hero, Now, Selected work, Earlier work,
  Papers, Contact) ; les 4 pages projet réécrites depuis Part 3 et renommées en
  `capra.body.html` / `dagobert.body.html` (ex-`cart-docking` / `english-to-arm`,
  supprimées) ; `pages.json` mis à jour (descriptions, `css_version` 13) ;
  CSS minimal ajouté (`.entries`, `.entry`, `.prose`) sans toucher l'art direction.
- Décisions : valeurs connues remplies (email, github, linkedin, cv.pdf) ; les
  autres `{{...}}` restent visibles pour l'owner. `tools/test_site.py` ignore
  désormais les hrefs contenant `{{` (placeholder de contenu, même rôle que
  `KNOWN_MISSING`), sur accord explicite de l'owner.
- Vérifié : `./scripts/check.sh` vert (5 pages générées, 4 tests OK).
- À surveiller : placeholders à remplir (`{{LAMAIN_GITHUB_URL}}`,
  `{{LEPOTAGER_VIDEO_URL}}`, `{{LEPOTAGER_CODE_URL}}`, `{{ETTC_PAPER_TITLE}}`,
  `{{ETTC_PAPER_URL}}`, `{{INSA_PAPER_TITLE}}`, `{{INSA_PAPER_URL}}`,
  `{{UPDATED_DATE}}`) ; slots média encore en boîtes pointillées.

## 2026-09-28 — home v2 (spec complète)
- Fait : home reconstruite selon la spec v2. Hero plein écran (nav Work/Research/
  Background/CV en haut à droite, « Selected work ↓ » en bas, nom + h1 fluides),
  Selected work (table drawing list + 4 sheets avec grande image), Research and
  papers (2 colonnes), Other projects (grille de 4 cartes), Background (2 tables
  Experience/Education), Contact. Ancienne section « Now » et ancienne table
  « Other sheets » supprimées. Ordre des pages projet passé à LaMain, Capra,
  LePotager, DagoBERT (pagers mis à jour). Paragraphe ajouté à Capra « Building
  the dataset ». CSS réécrit (tokens fluides --h1/--lead/--body/--section, hero
  100svh, plus de fade-in au scroll), art direction conservée. `css_version` 14.
- Décisions : la spec v2 dit de garder les `{{...}}` ; tous les placeholders sont
  donc laissés visibles (y compris email/github/linkedin/cv). Les pages projet
  gardent la mise en page actuelle (titleblock, prose + slots image, pager) ; pas
  de table de résultats, la v2 ne fournit pas de contenu pour elle. `site-content.md`
  (v1) n'a pas été touché, la v2 le remplace.
- Vérifié : `./scripts/check.sh` vert (5 pages, 4 tests OK) ; aucun « : », tiret
  cadratin ou demi-cadratin dans le texte visible ; les 12 placeholders présents.
- À surveiller : `site-content.md` est encore la v1, à remplacer ou supprimer.

## 2026-09-28 — hero proportions
- Fait : le hero était trop grand (titre et dessin massifs, liens sous la ligne
  de flottaison). Réduction de `--h1` (34-60px), `--lead` (16-20px), `--pad`
  (max 96px), du padding vertical du hero et de la largeur du dessin
  (`min(36vw, 56svh)`). `css_version` 15.
- Vérifié : screenshots Chrome 1280x720, 1920x1080 et 390x844, rendu équilibré
  et hero complet sur un écran. `./scripts/check.sh` vert.

## 2026-09-28 — integration de la version temporary
- Fait : l'accueil et le CSS sont portés depuis `temporary/portfolio-lamain`
  (hero régulier, nav Work/Research/Background/CV, scroll cue, `cv-table`,
  cartes 4 colonnes, `papers`, `article-lead`). Les 4 pages projet reprennent
  les textes/champs de temporary (Capra « March to September 2026 », figures,
  pager LaMain → Capra → LePotager → DagoBERT). `docs/01`-`05` remplacés par
  ceux de temporary et `docs/00-site-content.md` ajouté. `temporary/` supprimé.
  Architecture conservée (`site-src/` + `tools/build_site.py`), bouton de thème
  conservé.
- Décisions : deux corrections par rapport à temporary, gardées pour un vrai
  site. (1) `.note` servait à la fois à l'intro et aux annotations SVG
  (`opacity: 0`), la note « Looking for an end-of-studies internship » était
  invisible : les règles d'annotations sont scopées à `.hand__notes .note`.
  (2) le label « Sheet 0X » passait sous le bouton de thème fixe : `.topbar`
  reçoit `padding-right: 48px` et `.hero-nav` est décalé de 48px.
- Assets : `lamain-lines-backing.png` et `crosses-accent.svg` supprimés (plus
  utilisés). `site.js` réduit au seul toggle. `css_version` 18, `js_version` 11.
- Vérifié : `./scripts/check.sh` vert ; rendu Chrome 1280x720, 1440x900,
  1920x1080, 390x844 (hero = 1 écran, pas de scroll horizontal, label dégagé) ;
  12 placeholders présents ; aucun « : » ni tiret cadratin/demi-cadratin.
- À surveiller : `site-content.md` à la racine est encore l'ancienne v1, à
  supprimer ou remplacer.

## 2026-09-28 — restauration du halo tactile
- Fait : effet de halo bleu des croix restauré. `site.js` récupère le suivi
  souris `--mx`/`--my` (gardé par `(hover: hover) and (pointer: fine)`), le CSS
  récupère `body::before` masqué par un `radial-gradient` de 140px et
  `body { position: relative }` pour rester ancré au document.
- Assets : `crosses-accent.svg` recréé et `lamain-lines-backing.png` restauré.
- Décisions : correctif anti-bavure sur la main repris aussi (`.hand` en
  `z-index: 1; isolation: isolate`, plaque `.hand::before`, `.hand__lines` en
  `color-mix` au lieu d'`opacity: 0.72`), sinon le halo traverse les traits.
  `css_version` 19, `js_version` 12.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-28 — titre discret, liens entreprises, MSc cohérent
- Fait : le h1 du hero passe de `clamp(34px, 4vw, 64px)` à `clamp(23px, 2vw, 31px)`
  en `font-weight: 700` (discret, proche des h2). Liens ajoutés vers Safran Data
  Systems, Capra Robotics, Blue Frog Robotics dans le hero, la table expérience,
  la feuille DagoBERT et les titleblocks projet ; liens aussi vers Sorbonne,
  INSA Lyon et Université de Toulon. « master's/M2 » remplacé partout par
  « MSc in Robotics (ex-UPMC) » (hero, table éducation, label recherche, meta
  description, docs/00).
- Décisions : URLs vérifiées (caprarobotics.com, safran-group.com/companies/
  safran-data-systems, bluefrogrobotics.com, sorbonne-universite.fr,
  insa-lyon.fr, univ-tln.fr). `css_version` 20.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-28 — suppression des petits titres du home
- Fait : retiré la ligne spec du hero (« Most Creative Project, LeRobot
  hackathon 2026 · Co-author, ETTC 2025 »), les quatre en-têtes de section
  (`section-head`: « Drawing list / Selected work », « Research / Research and
  papers », « Also / Other projects », « Background / Experience and
  education ») et leur `aria-labelledby` devenu orphelin, ainsi que les labels
  des feuilles (« Sheet 01 · building », « Sheet 02 · on real robots », …).
  Les h3 de projet (LaMain, Capra Robotics, …) sont conservés.
- Décisions : les labels Sheet 0X ont aussi été retirés, comme demandé dans le
  message ; facile à restaurer si non voulu. `.section-head` reste dans le CSS
  (plus utilisé sur le home).
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — retrait du scroll cue « Selected work ↓ »
- Fait : supprimé le lien scroll-cue en bas du hero (« Selected work ↓ »,
  `href="#work"`). `.scroll-cue` reste dans le CSS (plus utilisé).
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — statuts animés, table remontée, MSc (ex-UPMC)
- Fait : la table « Selected work » remonte (`#work { padding-top: clamp(32px,
  4vh, 56px) }`). Statuts : LaMain « ● Building » clignote lentement
  (`is-live--pulse`, 3s, coupé en `prefers-reduced-motion`) ; Capra
  « ● Running », LePotager « ● Won Most Creative Project », DagoBERT
  « ● Presented at the European Test and Telemetry Conference », tous en bleu
  (`is-live`) sans clignotement. Majuscules en début de statut. Hero : MSc en
  gras retiré, « (ex-UPMC) » déplacé après Sorbonne Université (idem table
  éducation, meta description, docs/00).
- Décisions : « Winned most creative proejt » écrit « Won Most Creative
  Project ». `css_version` 21.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — encart skills, R&D Capra, retouches hero
- Fait : les specs sous les images des 4 feuilles (« 5 DOF · FlexiTac · LeRobot
  · 2026 », etc.) sont déplacées dans un encart encadré `.sheet__tags` (mono,
  bordure bleue) au-dessus du lien « Read the full sheet ». Hero : « six months
  in R&D at Capra Robotics », « LaMain, a hand with touch sensors for the SO-101
  arm », et suppression de « with a view to staying on. » dans la note. Meta
  description et docs/00 alignés.
- Décisions : encart en bleu sur la gauche (`align-self: flex-start`), pour
  rester dans la direction artistique (papier, croix, bleu). `css_version` 22.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — table allégée, textes projets, skills techniques
- Fait : colonne des numéros retirée de la table (et règle CSS `td:first-child`),
  textes projets rendus plus naturels (« an open-source robot hand with touch
  for the SO-101 arm », « computer vision and localisation on autonomous mobile
  robots », « a robot arm that sorts fruit by touch », « programming flight-test
  hardware in plain English »). Année DagoBERT « 2023 to 2025 » pour l'ETTC.
  Encart skills : plus de points `·`, chaque skill est un `<span>` espacé ;
  retiré les dates/lieux/non-skills (2026, Copenhagen, Safran Data Systems).
- Décisions : skills purement techniques (5 DOF, FlexiTac, LeRobot ; SegFormer,
  YOLOX, ROS 2, Jetson Orin Nano, OAK-D ; ACT, SO-101, piezoresistive sensor ;
  Llama 3, GNU Radio, C++, ARM). `css_version` 23.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — RoboCup : fiabilité mécanique, pas design chassis
- Fait : carte RoboCup, « designed their chassis » remplacé par « ensured their
  mechanical reliability » (index.body.html + docs/00).
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — majuscules après virgule dans la table
- Fait : après le nom de projet dans la table, la première lettre du complément
  est passée en majuscule (« LaMain, An open-source… », etc.).
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — plus d'articles dans la table
- Fait : retiré les articles en tête de description de projet (« An »/« A »),
  ex. « LaMain, Open-source robot hand with touch for the SO-101 arm ».
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — lead au même corps de texte
- Fait : `.intro .lead` passe de `var(--lead)` (18-22px) à `var(--body)`
  (17-19px), comme les autres paragraphes du hero. `css_version` 24.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — encart specs du prototype LaMain
- Fait : la ligne de la légende du prototype est scindée : les specs (5 DOF,
  under 200 g, under €200) passent dans un encart encadré `.hand-caption__tags`
  (même style que `.sheet__tags`, partagé par le sélecteur), et la créditation
  devient une ligne à part « Mechanical design with Julien Navet ».
  `css_version` 25.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — specs prototype en ligne, à droite
- Fait : l'encadré `.hand-caption__tags` est retiré ; les valeurs (5 DOF, under
  200 g, under €200) sont maintenant sur la même ligne que « LaMain prototype
  v1 », alignées à droite (`justify-content: space-between`), en mono muted, sans
  bordure ni point séparateur. `.hand-caption__tags` a son propre style (plus
  partagé avec `.sheet__tags`). `css_version` 26.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — toolbox réparti, specs LaMain en tags
- Fait : la ligne toolbox en fin de Background est supprimée. Ses technologies
  sont réparties dans les encarts `.sheet__tags` des 4 feuilles : LaMain
  (+PyTorch, Python, C/C++, Fusion 360), Capra (+Nav2, OpenVINO, ONNX, Docker,
  Python, C/C++), LePotager (+PyTorch, LeRobot, Python), DagoBERT (+Python,
  Docker). Les langues (French native · English C2) déplacées dans le pied de
  page contact. Valeurs du prototype LaMain : passées en petits tags encadrés
  (`border: hair`, uppercase mono) à droite du titre, sans points.
  `.toolbox` retiré du CSS. `css_version` 27.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — crédit sous les tags LaMain
- Fait : la légende LaMain passe en colonne droite `.hand-caption__side`
  (tags puis crédit, alignés à droite), remontée au sommet du titre
  (`align-items: flex-start`). Le crédit « Mechanical design with Julien Navet »
  est donc sous les tags `5 DOF · under 200 g · under €200`. `css_version` 28.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — bloc LaMain aligné bas à droite
- Fait : `.hand-caption__title` passe en `align-items: flex-end`, donc le bloc
  tags + crédit s'aligne sur la ligne « prototype v1 » (le plus bas = prototype
  v1), à sa droite, arrangement interne inchangé. `css_version` 29.
- Vérifié : `./scripts/check.sh` vert (4 tests OK).

## 2026-09-29 — carte LaMain en deux colonnes
- Fait : la légende LaMain est découpée en deux moitiés invisibles (grille 1fr 1fr,
  fond blanc, sans séparateur) : à gauche `LaMain` / `prototype v1` / description
  « Open-source hand with touch sensors for the SO-101 » ; à droite les tags
  `5 DOF · under 200 g · under €200` puis le crédit « Mechanical design with
  Julien Navet ». `.hand-caption__title`/`__sub` remplacés par `__grid`/`__left`/
  `__right`/`__proto`/`__desc`. `css_version` 35. Diagnostiqué via capture Chrome
  headless (carte ≈653px ; le bloc specs ne tenait pas à droite du nom complet).
- Vérifié : `./scripts/check.sh` vert (4 tests OK). Non commité (à la demande).

## 2026-09-29 — « prototype v1 » en noir, description retirée
- Fait : `.hand-caption__proto` passe de `var(--muted)` à `var(--ink)` (noir en
  thème clair) ; la ligne `<span class="hand-caption__desc">Open-source hand with
  touch sensors for the SO-101</span>` est supprimée de l'accueil, ainsi que la
  règle CSS `.hand-caption__desc` devenue inutile. `.hand-caption__grid` passe de
  `align-items: start` à `end`, donc le bloc tags + crédit descend au niveau de
  « prototype v1 ». `css_version` 36.
- Vérifié : `./scripts/check.sh` vert (4 tests OK). Capture Chrome headless OK.
  Non commité (à la demande).

## 2026-09-29 — liens papier ETTC et rapport BioMAÉ
- Fait : `{{ETTC_PAPER_URL}}` remplacé par l'URL du programme détaillé ETTC 2025
  (`index.body.html`, `projects/dagobert.body.html`). `{{INSA_PAPER_URL}}` remplacé
  par le PDF local `assets/documents/B6_D_tection_reconnaissance_gammares-2.pdf`
  (accueil). Titres `{{ETTC_PAPER_TITLE}}` / `{{INSA_PAPER_TITLE}}` laissés en
  placeholders (non fournis).
- Vérifié : `./scripts/check.sh` vert (4 tests OK). Non commité (à la demande).

## 2026-09-29 — « ● Currently building » clignote
- Fait : le label de légende LaMain passe en `label is-live--pulse` et réutilise
  l'animation `status-pulse` existante (même clignotement lent que « ● Building »
  du tableau, désactivé sous `prefers-reduced-motion`). Pas de changement CSS.
- Vérifié : `./scripts/check.sh` vert (4 tests OK). Non commité (à la demande).

## 2026-09-29 — titres des deux papiers
- Fait : à l'accueil (section Papers), `{{ETTC_PAPER_TITLE}}` remplacé par le titre
  ETTC exact « Facilitating Advanced Real-Time Data Processing Through Auto-Coding:
  An Application of Large Language Models for Intelligent Flight Test
  Instrumentation » ; `{{INSA_PAPER_TITLE}}` remplacé par la traduction anglaise du
  rapport BioMAÉ « Detection and recognition of gammarids » (titre original FR
  « DÉTECTION ET RECONNAISSANCE DE GAMMARES »).
- Vérifié : `./scripts/check.sh` vert (4 tests OK). Non commité (à la demande).

## 2026-09-29 — section Research, tags et label Papers
- Fait : le spec du projet de recherche passe du texte `·` à un bloc encadré
  `.sheet__tags` (même format que les fiches projet) ; « Sorbonne Université »
  retiré ; termes ajoutés `Set Transformer`, `CMA-ES`, `sim-to-real`. Ajout d'un
  label `Papers` au-dessus de la liste des papiers (colonne droite encadrée dans
  `.research__block`). Aucun changement CSS.
- Vérifié : `./scripts/check.sh` vert (4 tests OK). Capture Chrome OK. Non commité.

## 2026-09-29 — navigation des fiches et colonne centrée
- Fait : dans le topbar des quatre fiches, le lien « Drawing list » devient
  « ← Work » et le label « Sheet 0X » est supprimé. Dans le pager bas, « Drawing
  list » devient « ← Work ». `.article-lead` et `.prose` reçoivent
  `margin-inline: auto` : la colonne de texte (max 720px) est centrée
  horizontalement. `css_version` 37.
- Vérifié : `./scripts/check.sh` vert (4 tests OK). Capture Chrome OK. Non commité.

## 2026-09-28 — médias des projets, nettoyage des emplacements
- Fait : les 14 emplacements `.media` (8 accueil, 6 fiches) sont remplis ou
  retirés. LaMain : `main-ouverte.png` (CAO) + `lamain-mouvement.gif` (webm
  converti) ; LePotager : `sensing.gif` + `pipeline.gif` ; Capra :
  `capra-segmentation.mp4` (seule image gardée ; les figures anonymisation et
  docking, sans média, sont retirées) ; DagoBERT :
  `dagobert-01-chaine-complete.png`. Accueil : les 4 feuilles et les 4 cartes
  (gammarides, Buddy, RoboCup, vidéo compétition école). Liens remplis : email,
  github, linkedin, et le CV (`assets/documents/cv_arthurmourgue.pdf`) ;
  `{{UPDATED_DATE}}` → « September 2026 ». Liens projet fournis par l'owner :
  LaMain (`github.com/Arthur-Mourgue/LaMain`), LePotager
  (`github.com/Arthur-Mourgue/LePotager`), et le dépôt gammarides
  (`github.com/Arthur-Mourgue/biomae-gammarus`) ajouté à la carte Water quality.
- Médias : GIF et vidéos réencodés pour le web (`pipeline.gif` 6,4→3,2 Mo,
  `sensing.gif` 2,3→1,9 Mo, `capra-segmentation.mp4` 5,6→2,4 Mo, vidéo école
  2,9→1,7 Mo, GIF mouvement LaMain 1,0 Mo) ; JPG RoboCup 968→277 Ko ; PNG
  optimisés (optipng). Fichier renommé sans espace (`main-ouverte.png`).
- Décisions : `object-fit: contain` pour les figures (rien n'est rogné),
  `cover` conservé pour les vignettes de cartes ; légendes `<figcaption>` en
  mono muted ; `css_version` 38. Tous les placeholders de lien sont remplis : la
  démo LePotager pointe désormais vers
  `assets/documents/LePotager/fullvideolepotager.mp4`.
- Vérifié : `./scripts/check.sh` vert (5 pages, 4 tests OK). Rendu vérifié par
  impression PDF headless (accueil + 4 fiches).
- À surveiller : médias non utilisés encore présents dans
  `site/assets/documents/` (séries Capra et Safran, `fail.gif`,
  `TrieurResistance.png`, vidéos sources) — à trier/supprimer plus tard.

## 2026-09-28 — encarts adaptatifs, cartes réordonnées
- Fait : les cadres `.media` épousent le format réel de l'image, du GIF ou de la
  vidéo (`aspect-ratio: auto`, plus d'aplat bleu) ; variante `.media--crop` pour
  garder un cadre paysage rempli (vidéo School robotics). Cartes « Other
  projects » réordonnées : Water quality, RoboCup, School, Buddy — les deux
  images verticales (Water quality, Buddy) aux extrémités et affichées en entier.
  `css_version` 39.
- Décisions : le hero de l'accueil garde le dessin technique + annotations (pas de
  GIF animé) ; le GIF de mouvement reste la 2e figure de la page LaMain.
- Vérifié : `./scripts/check.sh` vert ; rendu pleine page Chrome (grille des
  cartes + figures).

## 2026-09-28 — Safran, sous-titres cohérents, séparateur, images Capra/Safran
- Fait : DagoBERT renommé « Safran » partout dans le visible (table, feuille,
  fiche, title/og, pager) et le nom n'est plus cité dans le texte. Feuille LaMain
  de l'accueil remplacée par le GIF de mouvement, avec un léger zoom (recadrage
  du GIF). Sous-titres des cartes mini-projets uniformisés (Institution ·
  Période) : « INSA Lyon · 2026 », « Robot Club Toulon · 2022 to 2023 »,
  « Université de Toulon · 2022 », « Blue Frog Robotics · 2023 ». Séparateur
  vertical entre le projet de recherche et les papiers. Capra : figures
  anonymisation (pipeline dans la caméra + cadre flouté) et docking (séquence en
  6 étapes + photo robot). LePotager : `fail.gif` sur « What went wrong »,
  `pipeline.gif` sur « The result », sensing en `.media--narrow` (plus petit).
  Safran : étapes 02–04 dans « How it works », 05 dans « The results ».
  `css_version` 40.
- Vérifié : `./scripts/check.sh` vert ; rendu pleine page + PDF Chrome (accueil
  et fiches Capra/LePotager/Safran).

## 2026-09-28 — retouches images, tags et mention ETTC
- Fait : images des fiches réduites et centrées (`.media--narrow`, max 440px) :
  GIF LaMain de l'accueil, étapes Safran 02–05, images Capra (segmentation
  01/05/06/07/10/11, anonymisation et docking), sensing LePotager. Capra : images
  ajoutées pour le premier problème (trottoir, première version, modèle générique
  vs fine-tuné, profilage Nsight, carte d'élévation LiDAR) — la vidéo reste.
  Tags : Capra (OpenVINO → Transformer, ajout CNN et CUDA), Safran (ajout NLP,
  Llama 3 → Llama 3 8B). ETTC : mention « presented by me » (sous-titre + texte).
  Pied de page : « Paris · open to moving anywhere ». `css_version` 41.
- Vérifié : `./scripts/check.sh` vert ; rendu PDF Chrome (accueil + Capra, Safran,
  LePotager).

## 2026-09-28 — liens LinkedIn des coéquipiers
- Fait : les personnes citées sont nommées en entier et liées à leur LinkedIn :
  Julien Navet (accueil ×2, LaMain ×3), Doga Ozbek (LePotager ×3), Hakan Yanik
  (LePotager titleblock + intro), José Vasquez (LePotager titleblock + intro,
  Capra). « Akan » corrigé en « Hakan Yanik » (slug `hakanyanik`).
- Vérifié : `./scripts/check.sh` vert.

## 2026-09-28 — paires côte à côte, retrait de la vidéo Capra
- Fait : figure côte à côte (`.media-row`, 2 colonnes, empilée en mobile) pour
  les problèmes LiDAR de Capra — trottoir + palette (« ce que le LiDAR rate ») et
  pierre + rampe (« ce qu'il détecte à tort ») ; modèle générique + fine-tuné
  côte à côte. Pipeline « première version » remis en pleine largeur (plus
  grand). Vidéo de segmentation retirée de la fiche Capra (légende comprise).
  GIF LaMain de l'accueil repassé en `.media--medium` (580px, un peu plus grand).
  `css_version` 42.
- Vérifié : `./scripts/check.sh` vert ; rendu PDF Chrome (Capra).
- Commit + push de tout le travail média de la session.

## 2026-09-30 — barres de navigation collantes, papiers pleine largeur
- Fait : la nav de l'accueil (Work/Research/Background/CV) est sortie du hero et
  rendue collante (`position: sticky`) avec un fond papier (blanc/noir selon le
  thème) qui masque la grille de croix derrière les liens. Même traitement pour
  `.topbar` des fiches projet : le lien « ← Work » reste en haut pendant le
  défilement. `scroll-margin-top` des sections/fiches relevé pour compenser la
  barre. Section recherche : bloc « Local rules for robot swarms » retiré, la
  liste des papiers passe en pleine largeur (lien à gauche, référence à droite).
  `css_version` 43.
- Vérifié : `./scripts/check.sh` vert.

## 2026-09-30 — hero recentré sous la nav collante
- Fait : la barre de navigation collante de l'accueil prenait de la place dans le
  flux et poussait le hero vers le bas. Elle a maintenant une hauteur fixe
  (`--nav-h: 49px`) annulée par une marge basse négative, donc elle flotte
  au-dessus du hero au lieu de le décaler : le texte et le dessin LaMain
  retrouvent leur centrage vertical sur le premier écran (comme avant la barre).
  Liens en `white-space: nowrap` pour garantir une seule ligne. `css_version` 47.
- Vérifié : `./scripts/check.sh` vert ; capture Chrome (1440×900 et 390×844).

## 2026-10-05 — photo LaMain v0, titres de section, onde au clic
- Fait : la première image de la fiche LaMain est désormais le gif `lamainv0.gif`
  (la vraie main v0 montée sur un robot) à la place du rendu CAD `main-ouverte.png`.
  L'accueil gagne des titres de section mono uniformes (Selected work, Research and
  papers, Other projects, Background) avec un filet bleu sous chacun, pour bien
  délimiter les blocs ; l'ancien label « Papers » a été absorbé par le titre.
  Chaque clic fait apparaître une onde circulaire qui traverse la grille de croix
  (`.ripple`, `clip-path` qui grandit + fondu, masque croisillons teintés) ; le
  nœud est retiré à la fin de l'animation et l'effet est ignoré si
  `prefers-reduced-motion`. `css_version` 48, `js_version` 13.
- Vérifié : `./scripts/check.sh` vert ; captures Chrome (accueil, sections, fiche
  LaMain, onde au clic).

## 2026-10-05 — correctifs : onde sur la bonne grille, gif v0, titres
- Fait : (1) L'onde au clic dessinait sa propre grille de croix, décalée de
  celle du `body` (boîte de 1040px positionnée au clic) — double quadrillage
  visible. La couche `.ripple` couvre maintenant toute la page (`inset: 0`,
  même ancrage que le halo de survol) et son quadrillage 28px partage l'origine
  du fond du `body` : les croix bleues se posent sur les croix grises. Le cercle
  est un `clip-path` centré sur `--rx/--ry` (coords page mises par site.js).
  (2) Le gif v0 est aussi dans sheet-01 de l'accueil (la main avant « Read the
  full sheet »), comme demandé. (3) Titres de section en gros serif gras **noir**
  (`.section-head h2`, taille `var(--h2)`) ; sous-titres projets un peu plus
  petits et **bleus** (`.sheet__text h3`, `calc(var(--h2) * 0.82)`). « Research
  and papers » → « Papers ». `css_version` 49, `js_version` 14.
- Vérifié : `./scripts/check.sh` vert ; captures Chrome (titres, onde à deux
  instants de l'animation, zoom sur la grille).

## 2026-10-05 — plus de double barre, tableau sans en-tête, gif v0 agrandi
- Fait : les titres de section ne portent plus de filet bleu — le tableau ou la
  liste en dessous a déjà sa propre bordure, et deux lignes horizontales
  successives font doublon (`.section-head`, plus de `border-bottom` ;
  `.section-head--table` resserre l'écart quand un tableau suit). La ligne
  d'en-tête `Project / Year / Status` du tableau Selected work est retirée : les
  colonnes se lisent seules, les années et les statuts restent dans les cellules.
  Caption du sheet-01 raccourcie à « LaMain v0, the first prototype. » et
  « Fusion 360 » retiré des tags LaMain. Le gif v0 passe en `.media--wide`
  (520px, centré) : il ne suivait pas la colonne parce que `margin-inline: auto`
  sur un élément flex remplace l'étirement (le cadre se réduisait à la largeur
  intrinsèque de l'image, 256px) — d'où `width: 100%`. `css_version` 50.
- Vérifié : `./scripts/check.sh` vert ; captures Chrome ; largeur mesurée dans
  Chrome (520px au lieu de 256px).

## 2026-10-05 — zoom et redimensionnement du texte
- Fait : audit de zoom sur les 5 pages. Deux vrais défauts trouvés et corrigés.
  (1) La liste Papers débordait horizontalement (`.papers li .spec` en
  `flex: 0 0 auto` : la référence longue ne pouvait pas rétrécir et poussait la
  page plus large que le viewport → barre de défilement latérale sur écran étroit
  et sous zoom navigateur). `min-width: 0` + `flex: 0 1 auto` sur les deux
  enfants : la référence passe sous le titre et s'enroule.
  (2) Toutes les tailles de police étaient en `px`, donc le zoom **texte seul**
  (taille de police par défaut du navigateur / réglage utilisateur) ne changeait rien
  changer : mesuré, h1 restait à 28.8px avec la racine à 200%. Tout est passé en
  `rem` (échelle --h1/--lead/--body/--h2/--section, labels mono, cartes, CV,
  figcaptions, titre du hero) : rendu identique à la racine 16px par défaut, mais
  le texte suit maintenant le réglage utilisateur. `--nav-h` de la barre collante
  devient `calc(0.9625rem + 2rem + 2px)` : la barre et sa marge négative
  grandissent ensemble, donc le hero reste centré (49px → 73px → 97px à
  100/150/200%). `prefers-reduced-motion` était déjà couvert (balayage main,
  notes, pulsation des statuts, onde au clic). `css_version` 51.
- Vérifié : `./scripts/check.sh` vert ; débordement mesuré sur les 5 pages à
  485/768/1280 px (aucun) ; zoom texte mesuré à 100/150/200 %.

## 2026-10-22 — textes resserrés, thème clair unique, liens GitHub
- Fait : suppression du bouton de thème et du mode sombre, le site reste en clair
  (`color-scheme: light`, plus de `theme-toggle`, `crosses-dark.svg` retiré).
  Les fiches projet sont réécrites plus courtes, sans deux-points ni tirets
  cadratins, sans légendes de figures et sans la section « What I did not finish »
  de Capra. GNU Radio disparaît du texte et du nom de l'image Safran. Les liens
  GitHub de LaMain et LePotager sont ajoutés à côté de « Read the full sheet ».
  `css_version` 52, `js_version` 15.
- Vérifié : `./scripts/check.sh` vert (8 tests, dont thème clair, liens GitHub,
  absence de tiret cadratin et de deux-points dans les paragraphes).
- Problèmes / à surveiller : `site-content.md` et `docs/00-site-content.md`
  gardent l'ancien texte (GNU Radio, légendes) et ne sont pas utilisés par le
  build ; `README.md` est vide ; `features.json` est vide ; `og.png` manque.

## 2026-10-22 — vidéo LePotager en hero, ordre et contenus mis à jour
- Fait : le hero affiche une boucle vidéo LePotager à la place du dessin LaMain,
  avec le bloc « Currently building LaMain » juste en dessous. L'intro précise
  la recherche de stage de six mois entre mars et mai 2027 et les intérêts de
  recherche. Les specs LaMain passent à « designed for under 200 g » et
  « designed for under €200 ». Selected work et les fiches passent dans l'ordre
  LePotager, LaMain, Capra, Safran, avec les badges « On a real robot » et
  « Published at ETTC 2025 », les tags réduits et la phrase sur les
  démonstrations de récupération. La date Capra passe à « Mar. to Aug. 2026 »,
  le projet « School robotics competition » est retiré, les liens CV industry
  et CV research remplacent cv.pdf et la date passe à octobre 2026. Les deux
  vidéos embarquées sont compressées, sans audio, en autoplay/muet/boucle avec
  poster. La nav du hero passe sur plusieurs lignes en mobile.
- Vérifié : `./scripts/check.sh` vert (8 tests).
- Problèmes / à surveiller : les deux PDF CV sont pour l'instant des copies du
  CV existant, à remplacer par les vraies versions industry et research. Les
  GIF de LaMain et LePotager restent lourds (jusqu'à 8,4 Mo pour fail.gif).

## 2026-10-22 — animations discrètes et interactions
- Fait : halo bleu ambiant qui traverse lentement la grille de croix, entrée
  du hero en fondu, révélation au scroll des fiches, cartes, papiers, colonnes
  Background et bloc contact, balayage de surbrillance sur la main LaMain,
  survol qui soulève et éclaire les médias, les cartes, les lignes du tableau
  et les papiers, transitions de couleur sur les liens. L'animation ambiante
  est coupée en mobile et tout est désactivé sous `prefers-reduced-motion`.
  `css_version` 53, `js_version` 16.
- Vérifié : `./scripts/check.sh` vert (8 tests), syntaxe JS et CSS contrôlées.
- Problèmes / à surveiller : les changements de la demande précédente et
  ceux-ci ne sont pas encore commités.

## AAAA-MM-JJ — F001
- Fait : ...
- Décisions prises : ...
- Problèmes / à surveiller : ...
