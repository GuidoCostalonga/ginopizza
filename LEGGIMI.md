# ginopizza.it

Sito statico multipagina di Guido Costalonga, assessore alla Sicurezza, Protezione Civile,
Patrimonio e Mobilità Sostenibile del Comune di Roveredo in Piano (Pordenone).
Stile satirico istituzionale sul soprannome, sostanza amministrativa rigorosa sui contenuti.

Ricognizione dei contenuti: **14 settembre 2026**.

> La pagina sulla Protezione Civile è stata rimossa su richiesta e potrà essere
> reintrodotta in seguito. La delega resta e continua a essere citata dove descrive
> il ruolo dell'assessore.

## Che cosa contiene

Sedici pagine: la pagina principale, tre indici, dieci schede e i contatti.
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
| `sicurezza-territorio.html` | **Indice.** Fermezza sì, allarmismi no, e le quattro schede |
| `controllo-di-vicinato.html` | Il protocollo con la Prefettura di Pordenone |
| `truffe-alla-porta.html` | Le quattro truffe alla porta di casa, da stampare |
| `truffe-fuori-casa.html` | Sei truffe fuori casa, al telefono e allo sportello |
| `truffe-cosa-fare.html` | I segnali, cosa fare se è già successo, numeri utili |
| `viabilita.html` | **Indice.** Il filo che tiene insieme le due schede |
| `permesso-rosa.html` | Il permesso rosa: requisiti, documenti, uso, sanzioni |
| `controlli-velocita.html` | I rilevatori di velocità tornati in funzione |
| `contatti.html` | Recapiti del municipio e della Polizia Locale, appuntamenti |

Più `stile.css`, `sito.js`, `sigillo.svg`, `costruisci.py` e i file di servizio
`CNAME`, `robots.txt`, `sitemap.xml`, `.nojekyll`.

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

Il codice è **online** nel repository dedicato `GuidoCostalonga/ginopizza`, ramo `main`:
https://github.com/GuidoCostalonga/ginopizza

Restano due passaggi che richiedono un accesso non disponibile in automatico.

### 1. Attivare le Pagine GitHub

Impostazioni del repository, sezione **Pages**: sorgente **Deploy from a branch**,
ramo `main`, cartella `/ (root)`, poi Salva. Il file `CNAME` è già nel repository e
contiene `ginopizza.it`, quindi il dominio personalizzato viene riconosciuto da solo.

Dopo qualche minuto il sito risponde su https://guidocostalonga.github.io/ginopizza/

### 2. Puntare il dominio

Presso il gestore del dominio, sostituire il record che punta a 146.59.63.161 con i
record delle Pagine GitHub, e aggiungere il sottodominio `www`.

Record verificati il 14 settembre 2026 risolvendo costalonga.org, che è già pubblicato
con le Pagine GitHub:

| Tipo | Nome | Valore |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |
| CNAME | www | guidocostalonga.github.io. |

A propagazione avvenuta, attivare nelle impostazioni delle Pagine la voce che impone il
collegamento cifrato.

### Strade alternative

Il sito è statico: cinque file HTML, un foglio di stile, uno script e un'immagine
vettoriale. Non serve alcun programma sul server, nessun database, nessuna compilazione.
Basta copiare il contenuto della cartella nella radice del sito. Quindi restano possibili
anche il trasferimento diretto per FTP o SFTP sul servizio attuale, che risponde
sull'indirizzo 146.59.63.161, oppure un servizio di pubblicazione statica.

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

- Struttura HTML di tutte e sei le pagine: nessun tag non chiuso.
- Tutti i collegamenti relativi puntano a file esistenti.
- Nessun errore JavaScript in console su nessuna pagina.
- Nessuno scorrimento orizzontale a 1280 pixel né a 390 pixel.
- Tendina, cassetto per telefono, copia negli appunti con avviso a comparsa, condivisione e
  tasto di stampa: tutti provati e funzionanti.
