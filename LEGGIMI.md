# ginopizza.it

Sito statico multipagina di Guido Costalonga, assessore alla Sicurezza, Protezione Civile,
Patrimonio e Mobilità Sostenibile del Comune di Roveredo in Piano (Pordenone).
Stile satirico istituzionale sul soprannome, sostanza amministrativa rigorosa sui contenuti.

Ricognizione dei contenuti: **14 settembre 2026**.

> La pagina sulla Protezione Civile è stata rimossa su richiesta e potrà essere
> reintrodotta in seguito. La delega resta e continua a essere citata dove descrive
> il ruolo dell'assessore.

## Che cosa contiene

Quattordici pagine: la pagina principale, tre indici, otto schede e i contatti.
Ogni scheda ha un indirizzo suo, così si può condividere da sola.

| File | Pagina |
|---|---|
| `index.html` | Manifesto, paradosso del modem del 1994, bacheca dei provvedimenti |
| `polizia-rurale.html` | **Indice.** L'atto in sintesi e le cinque schede |
| `polizia-rurale-diffida.html` | La diffida amministrativa, articolo 4 |
| `polizia-rurale-obblighi.html` | Gli obblighi, articolo per articolo, con le sanzioni |
| `polizia-rurale-fuochi.html` | I fuochi nei fondi, articoli 14 e 15 |
| `polizia-rurale-distanze.html` | Le tredici distanze, dagli articoli e dalle tavole |
| `polizia-rurale-novita.html` | Le altre novità e la storia del testo |
| `sicurezza-territorio.html` | **Indice.** Fermezza sì, allarmismi no, e le due schede |
| `controllo-di-vicinato.html` | Il protocollo con la Prefettura di Pordenone |
| `vademecum-antitruffa.html` | Il vademecum completo: truffe alla porta, fuori casa, segnali, cosa fare, numeri utili. Una pagina sola, da stampare intera |
| `viabilita.html` | **Indice.** Il filo che tiene insieme le due schede |
| `permesso-rosa.html` | Il permesso rosa: requisiti, documenti, uso, sanzioni |
| `controlli-velocita.html` | I rilevatori di velocità tornati in funzione |
| `contatti.html` | Recapiti del municipio e della Polizia Locale, appuntamenti |

Più `stile.css`, `sito.js`, `sigillo.svg`, `ritratto.jpg`, `anteprima.png`,
`inter.woff2`, `oswald.woff2`, `costruisci.py`, `trasmissione.svg`, `accendi.py`
e i file di servizio `CNAME`, `robots.txt`, `sitemap.xml`, `.nojekyll`.

I due caratteri stanno nel repository e non su un sito di terzi: aprendo una
pagina il navigatore non contatta nessun indirizzo fuori da ginopizza.it, e di
chi legge non resta traccia da nessuna parte. Sono Inter e Oswald, caratteri
variabili (un file solo per tutti i pesi), distribuiti con la SIL Open Font
License 1.1.

`ritratto.jpg` è il disegno intero, con il televisore e il mobile alle spalle,
in apertura della prima pagina: sta dentro una cornice nera spessa con l'ombra
dura, come tutti gli altri riquadri del sito. Il televisore alle spalle è acceso e
manda in onda una mano che porge una pizza, sotto la fascia con il nome: la
luce e la scena sono cotte dentro l'immagine, non sono pezzi della pagina.

Le due cose che le costruiscono stanno nel repository. `trasmissione.svg`
disegna la scena, già nelle coordinate del ritratto intero, su fondo
trasparente; va composta dal navigatore perché il carattere Oswald lo sa
leggere lui. `accendi.py` fa il resto: riconosce il vetro dello schermo con un
riempimento che parte da dentro e si ferma sul tratto nero, così testa e
occhiali, che stanno davanti, restano fuori dalla maschera; poi accende il
vetro, ci mette le righe del tubo catodico, il riflesso obliquo e l'alone che
lo schermo butta su quello che ha intorno, e infine appoggia la scena dentro
alla maschera. È per questo che il braccio, invece di finire con un taglio
netto, sparisce dietro alla testa. `anteprima.png` è la scheda
1200 per 630 che compare quando un collegamento del sito viene condiviso.

Le schede figlie hanno le briciole di navigazione in alto (Home, indice, scheda)
e il tasto di ritorno all'indice in fondo. Il registro `NOMI` dentro `costruisci.py`
tiene insieme nomi brevi, gerarchia, briciole e mappa del sito: per aggiungere una
scheda basta registrarla lì.

## Come si modifica

Le pagine **non si modificano a mano**: si modifica `costruisci.py` e si rigenera.

```
python3 costruisci.py
```

Barra di navigazione, barra di condivisione, piè di pagina e schede di anteprima sono definiti una
volta sola nel generatore, così restano identici su tutte le pagine.

## Stato della pubblicazione

**Il sito è in linea su https://ginopizza.it** dal 14 settembre 2026.

| Elemento | Stato |
|---|---|
| Repository | `GuidoCostalonga/ginopizza`, ramo `main` |
| Pubblicazione | Pagine GitHub, sorgente `main` cartella radice |
| Dominio | `ginopizza.it`, con il file `CNAME` nel repository |
| Certificato | Let's Encrypt, valido per `ginopizza.it` |
| Sottodominio | `www.ginopizza.it` rimanda alla radice |

Verificato il 14 settembre 2026: tutte le pagine rispondono, foglio di stile,
script e sigillo si caricano, nessun errore JavaScript, nessuno scorrimento orizzontale
a 390 pixel.

### Rimane da spuntare: collegamento cifrato obbligatorio

Nelle impostazioni del repository, sezione **Pages**, la voce **Enforce HTTPS** non è
ancora attiva: `http://ginopizza.it` serve il sito in chiaro invece di rimandare alla
versione cifrata. Ora che il certificato è stato emesso la casella è selezionabile.

### Come si aggiorna il sito

```
python3 costruisci.py
git add -A && git commit -m "..." && git push
```

Le Pagine GitHub ripubblicano da sole a ogni invio sul ramo `main`.

### Record DNS in uso

| Tipo | Nome | Valore |
|---|---|---|
| A | @ | 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153 |
| CNAME | www | guidocostalonga.github.io. |

## Come il sito si fa trovare

Ogni pagina porta in testa quello che serve ai motori di ricerca.

| Cosa | Dove |
|---|---|
| Titolo e descrizione, diversi su ogni pagina | `<title>` e `<meta name="description">` |
| Indirizzo ufficiale della pagina, contro i doppioni | `<link rel="canonical">` |
| Permesso di indicizzare, con anteprima grande | `<meta name="robots" content="index, follow, max-image-preview:large">` |
| Scheda per le reti sociali | `og:` e `twitter:`, con `anteprima.png` 1200 per 630 |
| Dati strutturati | `<script type="application/ld+json">` |
| Elenco delle pagine | `sitemap.xml`, dichiarata in `robots.txt` |

I titoli sono scritti per come si cerca davvero: l'argomento davanti e il
nome del paese dopo, perché chi cerca scrive «regolamento polizia rurale
Roveredo in Piano», non il nome del sito. Le descrizioni stanno sotto i 165
caratteri, che è quanto Google ne mostra.

I dati strutturati li costruisce `dati_strutturati()` dentro `costruisci.py`.
Dichiarano quattro cose: il sito, la persona che lo firma con la sua carica e
il Comune, la pagina che si sta leggendo, e il filo delle briciole che ci
porta, ricavato dal registro `NOMI`. Le briciole di Google vengono da lì:
sono le stesse che si vedono in alto nelle schede.

Per collegare il sito a **Google Search Console** serve un codice di verifica.
Si incolla nella costante `VERIFICA_GOOGLE` in cima a `costruisci.py` e si
rigenera: finché resta vuota, la riga non viene nemmeno scritta nelle pagine.

## Regola sui dati

Su questo sito non si scrive un dato che non sia stato letto su una fonte ufficiale.
Quando un'informazione non è ancora decisa o non è disponibile, **non si stima e non si
arrotonda: semplicemente non si scrive**, e al suo posto c'è il rimando al sito del Comune.

Questo non è il sito istituzionale del Comune di Roveredo in Piano. Numeri di deliberazione,
elenchi di stalli, calendari e orari di sportello stanno sui canali ufficiali, ed è lì che
la pagina manda il lettore. Il piè di pagina lo dice in chiaro: gli atti che fanno fede sono
quelli pubblicati all'albo pretorio.

La classe `.da-verificare` resta nel foglio di stile, in corsivo rosso su pastiglia chiara,
per quando servirà marcare un dato incerto invece di ometterlo.

### Informazioni volutamente non pubblicate

Non sono buchi: sono scelte. Il lettore viene mandato alla fonte istituzionale.

| Pagina | Informazione | Dove si trova |
|---|---|---|
| `polizia-rurale.html` | Numero della deliberazione di Consiglio comunale | Albo pretorio del Comune |
| `sicurezza-territorio.html` | Date degli incontri di presentazione del controllo di vicinato | Canali del Comune e Polizia Locale |
| `viabilita.html` | Numero e collocazione degli stalli rosa, estremi del regolamento permessi rosa | Sito del Comune |
| `viabilita.html` | Calendario dei controlli di velocità e tratti interessati | Resi noti in anticipo dal Comune |
| `contatti.html` | Orari fissi di ricevimento e di apertura dello sportello | Su appuntamento, sito del Comune |

### Dati verificati e loro fonte

| Dato | Fonte | Letto il |
|---|---|---|
| Regolamento di polizia rurale: 84 articoli, 12 capi, 4 allegati, 9 tavole grafiche, diffida amministrativa (art. 4), sanzioni, sfalci (art. 7), fossi e canali (artt. 40 e 44), siepi e alberi (art. 48), fuochi (art. 14), distanze (artt. 22, 34, 39, 49, 57), entrata in vigore (art. 84) | Regolamento_Polizia_rurale_Roveredo_in_Piano.pdf, 65 pagine, fornito dall'assessore | 14 settembre 2026 |
| Approvazione all'unanimità del Consiglio comunale il 22 giugno 2026, sostituzione del regolamento del 2006, le tre novità, i ringraziamenti, le citazioni | Comunicato stampa del Comune di Roveredo in Piano, 23 giugno 2026 | 14 settembre 2026 |
| Entrata in vigore del regolamento di polizia rurale: 13 settembre 2026 | Indicazione diretta dell'assessore | 14 settembre 2026 |
| Permesso rosa: requisiti, documenti e marche da bollo, presentazione e ritiro, limite di tre ore dalle 8.00 alle 20.00 con disco orario, scadenze, reciprocità fra Comuni, sanzioni | REGOLAMENTO_PERMESSI_ROSA.pdf, 7 pagine, 13 articoli, fornito dall'assessore | 14 settembre 2026 |
| Controllo di vicinato: protocollo con la Prefettura di Pordenone, chi può aderire, che cosa si segnala, divieto di ronde e di pattugliamento, ruolo del coordinatore e del Comune, recapiti della Polizia Locale | Controllo_di_Vicinato_Roveredo_in_Piano.pdf, 3 pagine, fornito dall'assessore | 14 settembre 2026 |
| Rilevatori di velocità: motivo della sospensione e della ripresa, postazioni segnalate, apparecchi omologati e tarati, fasce orarie, citazioni dell'assessore e del comandante Cristiano Ciletti | Comunicato stampa del Comune di Roveredo in Piano, 10 agosto 2026 | 14 settembre 2026 |
| Articolo 188 bis del Codice della Strada, commi 2, 3 e 4, con importi delle sanzioni | Normattiva, decreto legislativo 30 aprile 1992, n. 285 | 14 settembre 2026 |
| Indirizzo, telefono, fax, PEC, codice fiscale e partita IVA del Comune | comune.roveredoinpiano.pn.it | 14 settembre 2026 |
| Vademecum antitruffa: casistiche, segnali, cosa fare, numeri utili | costalonga.org/truffe (Ministero dell'Interno, Polizia Postale, Arma dei Carabinieri) | 14 settembre 2026 |
| Deleghe, biografia, recapito diretto | costalonga.org/chi-sono | 14 settembre 2026 |

### Refusi riscontrati nei documenti di partenza, non riportati sul sito

| Documento | Refuso | Che cosa è stato pubblicato |
|---|---|---|
| Comunicato stampa polizia rurale, 23 giugno 2026 | Dice «il regolamento di dieci anni fa» ma anche «del 2006» e «vent'anni»: le tre indicazioni non tornano | Solo «del 2006» e «vent'anni», che sono coerenti fra loro |
| Regolamento permessi rosa, art. 2 | Cita «Legge n. 121/2021 che ha convertito il Decreto Legge n. 12/2021», mentre l'art. 1 dello stesso regolamento indica correttamente il D.L. 121/2021 convertito dalla L. 156/2021 | La versione corretta dell'art. 1 |

## Verifiche eseguite

- Struttura HTML di tutte e quattordici le pagine: nessun tag non chiuso.
- Tutti i collegamenti relativi puntano a file esistenti.
- Nessun errore JavaScript in console su nessuna pagina.
- Nessuno scorrimento orizzontale a 1280 pixel né a 390 pixel.
- Tutte le immagini si caricano e nessuna resta schiacciata sotto i 40 pixel.
- Nessun testo dello stesso colore del proprio sfondo.
- Nessuna richiesta fuori da ginopizza.it, nessun cookie, nessuna memoria locale:
  verificato con il navigatore su una pagina completa.
- Tendina, cassetto per telefono, copia negli appunti con avviso a comparsa, condivisione e
  tasto di stampa: tutti provati e funzionanti.
