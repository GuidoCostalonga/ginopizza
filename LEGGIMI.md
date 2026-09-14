# ginopizza.it

Sito statico multipagina di Guido Costalonga, assessore alla Sicurezza, Protezione Civile,
Patrimonio e Mobilità Sostenibile del Comune di Roveredo in Piano (Pordenone).
Stile satirico istituzionale sul soprannome, sostanza amministrativa rigorosa sui contenuti.

Ricognizione dei contenuti: **14 settembre 2026**.

> La pagina sulla Protezione Civile è stata rimossa su richiesta e potrà essere
> reintrodotta in seguito. La delega resta e continua a essere citata dove descrive
> il ruolo dell'assessore.

## Che cosa contiene

| File | Pagina |
|---|---|
| `index.html` | Manifesto, paradosso del modem del 1994, bacheca dei provvedimenti |
| `polizia-rurale.html` | Regolamento di polizia rurale: fossi, rami, fondi agricoli, incuria |
| `sicurezza-territorio.html` | Controllo di vicinato (protocollo con la Prefettura) e vademecum antitruffa |
| `viabilita.html` | Permesso rosa e rilevatori di velocità |
| `contatti.html` | Recapiti del municipio, appuntamenti, protocollo, contatto diretto |
| `stile.css` | Identità visiva: blu elettrico, nero, bianco, giallo allerta, bordi spessi, ombre nette. Il rosso resta solo per la marcatura «da verificare» e per il tocco tricolore |
| `sito.js` | Tendina, cassetto per telefono, condivisione, copia negli appunti, stampa |
| `sigillo.svg` | Sigillo araldico: «Repubblica delle cose fatte», trancio di pizza e stivale |
| `costruisci.py` | Generatore delle pagine. Unica fonte da modificare |
| `CNAME`, `robots.txt`, `sitemap.xml`, `.nojekyll` | File di servizio per la pubblicazione |

## Come si modifica

Le pagine **non si modificano a mano**: si modifica `costruisci.py` e si rigenera.

```
python3 costruisci.py
```

Barra di navigazione, barra di condivisione, piè di pagina e schede di anteprima sono definiti una
volta sola nel generatore, così restano identici su tutte le pagine.

## Come si mette in linea

Il sito è statico: sei file HTML, un foglio di stile, uno script e un'immagine vettoriale.
Non serve alcun programma sul server, nessun database, nessuna compilazione.
Basta copiare il contenuto di questa cartella nella radice del sito.

Le tre strade possibili, in ordine di comodità:

1. **Pagine GitHub.** È già la strada usata per costalonga.org e funziona. Quattro passi:

   1. Creare un repository pubblico vuoto, per esempio `GuidoCostalonga/ginopizza`,
      senza file iniziali.
   2. Caricare il contenuto di questa cartella nella radice del repository, sul ramo `main`.
   3. Nelle impostazioni del repository, sezione Pages, attivare la pubblicazione dal ramo `main`,
      cartella radice, e impostare il dominio personalizzato su `ginopizza.it`.
      Il file `CNAME` è già presente e contiene il dominio.
   4. Presso il gestore del dominio, sostituire il record che punta a 146.59.63.161 con i record
      delle Pagine GitHub qui sotto, e aggiungere il sottodominio `www`.

   Record da impostare sul dominio `ginopizza.it` (verificati il 14 settembre 2026 risolvendo
   costalonga.org, che è già pubblicato con le Pagine GitHub):

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

   Dopo la propagazione, attivare nelle impostazioni delle Pagine la voce che impone il
   collegamento cifrato.
2. **Trasferimento diretto sull'attuale servizio.** Il dominio `ginopizza.it` risolve
   sull'indirizzo 146.59.63.161 e risponde con un errore 503. Servono le credenziali FTP o SFTP
   di quel servizio per caricare i file nella cartella pubblica.
3. **Servizio di pubblicazione statica** (Netlify, Vercel, Cloudflare Pages). Serve un accesso
   all'account e il collegamento del dominio.

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
