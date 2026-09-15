# -*- coding: utf-8 -*-
"""Generatore delle pagine statiche di ginopizza.it.
Scrive file HTML puri: nessuna dipendenza esterna, nessun passaggio di compilazione.
Si esegue con: python3 costruisci.py
"""
import os, datetime, hashlib

CARTELLA = os.path.dirname(os.path.abspath(__file__))
SITO = "https://ginopizza.it"
RICOGNIZIONE = "14 settembre 2026"

VOCI = [
    ("polizia-rurale.html",       "\U0001F69C", "Polizia rurale",                  "In vigore"),
    ("sicurezza-territorio.html", "\U0001F441️", "Sicurezza e vademecum truffe", "Attivo"),
    ("viabilita.html",            "\U0001F697", "Viabilità e parcheggi rosa",  "In corso"),
]

# Nome breve di ogni pagina e sua pagina madre: serve alle briciole di
# navigazione e alla mappa del sito, che si costruiscono da soli.
NOMI = {
    "index.html":                    ("Home", None),
    "polizia-rurale.html":           ("Polizia rurale", None),
    "polizia-rurale-diffida.html":   ("La diffida amministrativa", "polizia-rurale.html"),
    "polizia-rurale-obblighi.html":  ("Gli obblighi", "polizia-rurale.html"),
    "polizia-rurale-fuochi.html":    ("I fuochi nei fondi", "polizia-rurale.html"),
    "polizia-rurale-distanze.html":  ("Le distanze", "polizia-rurale.html"),
    "polizia-rurale-novita.html":    ("Le novità del testo", "polizia-rurale.html"),
    "sicurezza-territorio.html":     ("Sicurezza", None),
    "controllo-di-vicinato.html":    ("Controllo di vicinato", "sicurezza-territorio.html"),
    "vademecum-antitruffa.html":     ("Il vademecum antitruffa", "sicurezza-territorio.html"),
    "viabilita.html":                ("Viabilità", None),
    "permesso-rosa.html":            ("Il permesso rosa", "viabilita.html"),
    "controlli-velocita.html":       ("I controlli di velocità", "viabilita.html"),
    "contatti.html":                 ("Ricevimento e contatti", None),
}


def impronta(nome):
    """Breve impronta del file, da accodare all'indirizzo: costringe il browser a
    riscaricare foglio di stile e script appena cambiano, invece di tenere in cache
    per dieci minuti una versione vecchia."""
    percorso = os.path.join(CARTELLA, nome)
    if not os.path.exists(percorso):
        return ""
    with open(percorso, "rb") as f:
        return "?v=" + hashlib.sha1(f.read()).hexdigest()[:8]


def briciole(file_html):
    """Percorso di navigazione, mostrato solo nelle pagine figlie."""
    nome, madre = NOMI.get(file_html, (None, None))
    if not madre:
        return ""
    nome_madre = NOMI[madre][0]
    return """<nav class="briciole non-stampare" aria-label="Percorso">
  <div class="briciole__interno">
    <a href="index.html">Home</a>
    <span aria-hidden="true">&rsaquo;</span>
    <a href="{m}">{nm}</a>
    <span aria-hidden="true">&rsaquo;</span>
    <span class="briciole__qui" aria-current="page">{n}</span>
  </div>
</nav>""".format(m=madre, nm=nome_madre, n=nome)


def scheda(file_html, numero, occhiello, emoji, titolo, riassunto, punti=()):
    """Riquadro dell'indice: titolo, riassunto e, se serve, tre righe di che cosa c'è dentro."""
    elenco = ""
    if punti:
        elenco = "<ul>" + "".join("<li>%s</li>" % p for p in punti) + "</ul>"
    return """      <a class="manifesto" href="{f}">
        <div class="manifesto__cima">
          <span class="manifesto__numero">{n}</span>
          <span class="manifesto__occhiello">{o}</span>
          <span class="manifesto__emoji" aria-hidden="true">{e}</span>
        </div>
        <div class="manifesto__corpo">
          <h3>{t}</h3>
          <p>{r}</p>
          {el}
          <span class="manifesto__vai">Apri la scheda &rarr;</span>
        </div>
      </a>
""".format(f=file_html, n=numero, o=occhiello, e=emoji, t=titolo, r=riassunto, el=elenco)


NASTRO = ("APPROVATO DALL'ASSESSORE ★ IN VIGORE SUBITO ★ POCHE PIZZE ★ "
          "ZERO ANANAS, SOLO FATTI ★ DELIBERE, NON CHIACCHIERE ★ ")


def barra(corrente):
    def attivo(f):
        return ' aria-current="page"' if f == corrente else ''
    voci_tendina = "".join(
        '<a href="{f}"{a}><span class="tendina__emoji" aria-hidden="true">{e}</span>{t}'
        '<span class="tendina__stato">{s}</span></a>'.format(f=f, a=attivo(f), e=e, t=t, s=s)
        for f, e, t, s in VOCI)
    voci_cassetto = "".join(
        '<a href="{f}"{a}><span aria-hidden="true">{e}</span>{t}</a>'.format(f=f, a=attivo(f), e=e, t=t)
        for f, e, t, _ in VOCI)
    return """<header class="barra">
  <div class="barra__interno">
    <a class="marchio" href="index.html">
      <img src="sigillo.svg%SIGILLO%" alt="Sigillo GinoPizza, Repubblica delle cose fatte" width="52" height="52">
      <span class="marchio__testo">GinoPizza.it<small>Assessorato operativo</small></span>
    </a>
    <nav class="menu" aria-label="Navigazione principale">
      <a class="menu__voce menu__voce--casa" href="index.html"{casa}>
        <span aria-hidden="true">⌂</span> Home</a>
      <div class="tendina" data-tendina data-aperta="no">
        <button class="tendina__bottone" type="button" aria-expanded="false" aria-haspopup="true">
          Atti &amp; deleghe <span aria-hidden="true">▾</span></button>
        <div class="tendina__pannello">{tendina}</div>
      </div>
      <a class="menu__voce menu__voce--contatti" href="contatti.html"{cont}>Ricevimento &amp; contatti</a>
    </nav>
    <button class="panino" type="button" data-panino aria-expanded="false" aria-label="Apri il menù">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="cassetto" data-cassetto data-aperto="no">
    <a class="casa" href="index.html"><span aria-hidden="true">⌂</span> Home</a>
    {cassetto}
    <a class="contatti" href="contatti.html"><span aria-hidden="true">✉</span> Ricevimento &amp; contatti</a>
  </div>
</header>""".format(tendina=voci_tendina, cassetto=voci_cassetto,
                    casa=attivo("index.html"),
                    cont=attivo("contatti.html")).replace("%SIGILLO%", impronta("sigillo.svg"))


def condivisione(titolo, file_html):
    url = SITO + "/" + ("" if file_html == "index.html" else file_html)
    testo = titolo.replace('"', "'")
    import urllib.parse as up
    q = up.quote(testo + " " + url)
    qu = up.quote(url)
    qt = up.quote(testo)
    return """<div class="condivisione non-stampare">
  <div class="condivisione__interno">
    <span class="condivisione__etichetta">Diffondi l'atto</span>
    <button type="button" class="principale" data-condividi="{t}">
      <span aria-hidden="true">▶</span> Condividi atto</button>
    <a href="https://wa.me/?text={q}" target="_blank" rel="noopener">WhatsApp</a>
    <a href="https://t.me/share/url?url={qu}&amp;text={qt}" target="_blank" rel="noopener">Telegram</a>
    <a href="https://www.facebook.com/sharer/sharer.php?u={qu}" target="_blank" rel="noopener">Facebook</a>
    <a href="https://twitter.com/intent/tweet?url={qu}&amp;text={qt}" target="_blank" rel="noopener">X</a>
    <button type="button" data-copia-indirizzo>
      <span aria-hidden="true">⧉</span> Copia collegamento diretto</button>
  </div>
</div>""".format(t=testo, q=q, qu=qu, qt=qt)


CHIUSURA = """<footer class="chiusura">
  <div class="contenitore">
    <p class="chiusura__frase obliquo">Cercavi la pizza margherita? Sbagliato indirizzo: vai nelle pizzerie
      del paese. Cercavi risposte per il comune? Qui non si dorme.</p>
    <div class="chiusura__griglia">
      <div>
        <h4>Atti &amp; deleghe</h4>
        <ul>
          <li><a href="polizia-rurale.html">Polizia rurale</a></li>
          <li><a href="sicurezza-territorio.html">Sicurezza e truffe</a></li>
          <li><a href="viabilita.html">Viabilit&agrave; e parcheggi rosa</a></li>
        </ul>
      </div>
      <div>
        <h4>Il municipio</h4>
        <ul>
          <li>Comune di Roveredo in Piano</li>
          <li>Via G. Carducci, 11</li>
          <li>33080 Roveredo in Piano (PN)</li>
          <li>Telefono <a href="tel:+390434388611">0434 388611</a></li>
        </ul>
      </div>
      <div>
        <h4>Altrove</h4>
        <ul>
          <li><a href="contatti.html">Ricevimento e contatti</a></li>
          <li><a href="contatti.html#privacy">Cookie e dati: nessuno</a></li>
          <li><a href="https://costalonga.org" target="_blank" rel="noopener">costalonga.org</a></li>
          <li><a href="https://costalonga.org/truffe/" target="_blank" rel="noopener">Vademecum truffe</a></li>
          <li><a href="https://wa.me/393283692227" target="_blank" rel="noopener">Scrivimi su WhatsApp</a></li>
        </ul>
      </div>
    </div>
    <p class="chiusura__nota">Sito personale di Guido Costalonga, assessore alla Sicurezza, Protezione Civile,
      Patrimonio e Mobilit&agrave; Sostenibile del Comune di Roveredo in Piano (Pordenone). Iniziativa di
      trasparenza amministrativa senza scopo di lucro: nessuna pubblicit&agrave;, nessuna raccolta di dati
      personali, nessun contributo pubblico impiegato. Non &egrave; il sito istituzionale del Comune: gli atti
      che fanno fede sono quelli pubblicati all'albo pretorio del Comune di Roveredo in Piano.
      Il tono &egrave; satirico soltanto sul soprannome: i provvedimenti citati sono reali e verificabili.
      Ultima ricognizione dei contenuti: %s. &copy; 2026 Guido Costalonga.</p>
  </div>
</footer>
<div class="avviso" data-avviso data-visibile="no" role="status" aria-live="polite"></div>
<script src="sito.js{vjs}"></script>""" % RICOGNIZIONE


def pagina(file_html, titolo_scheda, descrizione, corpo, emoji_og="\U0001F355"):
    url = SITO + "/" + ("" if file_html == "index.html" else file_html)
    return """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>/* Chi arriva in chiaro viene portato subito sulla versione cifrata. */
if(location.protocol==='http:'&&/(^|\.)ginopizza\.it$/.test(location.hostname)){{
location.replace('https://'+location.host+location.pathname+location.search+location.hash);}}</script>
<title>{ts}</title>
<meta name="description" content="{d}">
<meta name="author" content="Guido Costalonga">
<meta name="theme-color" content="#0038ff">
<link rel="canonical" href="{u}">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="GinoPizza.it">
<meta property="og:title" content="{ts}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{s}/anteprima.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="GinoPizza.it: s&igrave;, il sito &egrave; ginopizza.it. No, non &egrave; una pizzeria.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ts}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{s}/anteprima.png">
<link rel="icon" href="sigillo.svg{vsvg}" type="image/svg+xml">
<link rel="stylesheet" href="stile.css{vcss}">
</head>
<body>
{barra}
{bric}
{cond}
{corpo}
{chiusura}
</body>
</html>
""".format(ts=titolo_scheda, d=descrizione, u=url, s=SITO,
           vcss=impronta("stile.css"), vjs=impronta("sito.js"), vsvg=impronta("sigillo.svg"),
           barra=barra(file_html), bric=briciole(file_html),
           cond=condivisione(titolo_scheda, file_html),
           corpo=corpo, chiusura=CHIUSURA.replace("{vjs}", impronta("sito.js")))


def nastro(classe="nastro--blu"):
    return '<div class="nastro {c}" aria-hidden="true"><p>{t}</p></div>'.format(c=classe, t=NASTRO)


def scrivi(nome, contenuto):
    with open(os.path.join(CARTELLA, nome), "w", encoding="utf-8") as f:
        f.write(contenuto)
    print("scritto", nome, len(contenuto), "caratteri")

# ============================================================
# 1. index.html - Il manifesto GinoPizza
# ============================================================
CORPO_INDEX = """
<main>
""" + nastro("nastro--blu") + """
<section class="sezione">
  <div class="contenitore">
    <div class="annuncio annuncio--ritratto obliquo">
      <div class="annuncio__testo">
        <h1>S&igrave;, il sito &egrave; ginopizza.it.<br>No, non &egrave; una pizzeria.</h1>
        <p>Qui non si sforna niente. Si firmano atti, si fissano date e si risponde di quello che si &egrave;
           fatto. La pizza la fanno meglio in paese: qui si fa il resto.</p>
      </div>
      <img class="ritratto" src="ritratto.jpg""" + impronta("ritratto.jpg") + """" width="900" height="687"
           alt="Ritratto a fumetto di Guido Costalonga: testa pelata, barba, occhiali dalla montatura spessa, giacca blu con la coccarda tricolore. Alle spalle un televisore a tubo catodico con le antenne, un mobiletto e una parete di legno.">
    </div>

    <div style="text-align:center;margin:-14px 0 34px">
      <span class="timbro timbro--blu timbro--obliquo"><span aria-hidden="true">&#127829;&#128683;</span>
        Bollino: zero ananas, solo fatti</span>
      <span class="timbro timbro--nero"><span aria-hidden="true">&#9989;</span> Sicurezza</span>
      <span class="timbro timbro--nero"><span aria-hidden="true">&#9989;</span> Decoro urbano</span>
      <span class="timbro timbro--nero"><span aria-hidden="true">&#9989;</span> Viabilit&agrave;</span>
      <span class="timbro timbro--nero"><span aria-hidden="true">&#9989;</span> Patrimonio</span>
      <span class="timbro timbro--nero"><span aria-hidden="true">&#9989;</span> Protezione civile</span>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--nero">
        <h3><span aria-hidden="true">&#128224;</span> Il paradosso trentennale</h3>
        <p>Nel 1994 c'era un modem che occupava la linea di casa e un fratello che urlava dall'altra stanza.
           Serviva un soprannome per entrare nelle chiacchierate in rete e ne uscì
           <strong>GinoPizza</strong>. Sembrava geniale. Aveva vent'anni, quindi no, non lo era.</p>
        <p>Da allora sono passati pi&ugrave; di trent'anni. Il soprannome &egrave; rimasto attaccato addosso
           come una croce personale: &egrave; finito sulle caselle di posta, sui profili, sui documenti
           di mezza vita. A un certo punto cambiarlo sarebbe stato pi&ugrave; ridicolo che tenerlo.</p>
        <p><strong>Quindi eccolo qui, in bella vista.</strong> Con sopra gli atti veri.</p>
      </div>
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#9878;</span> L'assunzione di responsabilit&agrave;</h3>
        <p class="sigillo-grande" style="margin-bottom:16px">Fermezza s&igrave;, allarmismi no</p>
        <p>A vent'anni ci si inventano soprannomi ridicoli. Da amministratori si risponde con la
           disciplina dei fatti.</p>
        <p>Su questo sito non ci sono promesse: ci sono provvedimenti, date e collegamenti alle fonti.
           Quello che non &egrave; ancora deciso non viene raccontato come se lo fosse, e per gli atti
           formali il rimando &egrave; sempre al sito del Comune.</p>
        <p>Il rispetto per chi lavora, cio&egrave; dipendenti comunali, Polizia Locale, forze dell'ordine e
           volontari di Protezione Civile, non &egrave; satira: quello &egrave; sacro.</p>
      </div>
    </div>
  </div>
</section>

""" + nastro("nastro--giallo") + """

<section class="sezione sezione--scura">
  <div class="contenitore">
    <h2 class="sezione__titolo" style="color:#facc15"><span aria-hidden="true">&#128203;</span> Bacheca dei provvedimenti</h2>
    <p class="sezione__sotto">Tre fronti aperti, tre pagine. Ognuna con che cosa si fa, quando si
       fa e che cosa serve al cittadino per starci dentro.</p>

    <div class="griglia griglia--3">
      <a class="manifesto" href="polizia-rurale.html">
        <div class="manifesto__cima">
          <span class="manifesto__numero">01</span>
          <span style="font-size:.72rem;letter-spacing:.1em;font-family:Oswald,Impact,sans-serif">
            Atto ufficiale &middot; In vigore dal 13 settembre 2026</span>
          <span class="manifesto__emoji" aria-hidden="true">&#128668;</span>
        </div>
        <div class="manifesto__corpo">
          <h3>Regolamento di polizia rurale</h3>
          <p>Ottantaquattro articoli approvati all'unanimit&agrave; dal Consiglio comunale il 22 giugno 2026.
             La novit&agrave;: prima si diffida, poi semmai si sanziona.</p>
          <div><span class="timbro timbro--blu"><span aria-hidden="true">&#128668;</span>
            Atto ufficiale: polizia rurale</span></div>
          <span class="manifesto__vai">Leggi il regolamento &rarr;</span>
        </div>
      </a>

      <a class="manifesto" href="sicurezza-territorio.html">
        <div class="manifesto__cima">
          <span class="manifesto__numero">02</span>
          <span style="font-size:.72rem;letter-spacing:.1em;font-family:Oswald,Impact,sans-serif">
            Protocollo con la Prefettura</span>
          <span class="manifesto__emoji" aria-hidden="true">&#128065;</span>
        </div>
        <div class="manifesto__corpo">
          <h3>Controllo di vicinato e truffe</h3>
          <p>Occhi aperti e nessuna ronda: come funziona il protocollo con la Prefettura di Pordenone.
             E il vademecum antitruffa completo, con il numero unico di emergenza 112.</p>
          <div><span class="timbro"><span aria-hidden="true">&#128065;</span>
            Vigilanza civica: occhi aperti</span>
          <span class="timbro timbro--blu"><span aria-hidden="true">&#128680;</span>
            Allerta truffe</span></div>
          <span class="manifesto__vai">Vai al vademecum &rarr;</span>
        </div>
      </a>

      <a class="manifesto" href="viabilita.html">
        <div class="manifesto__cima">
          <span class="manifesto__numero">03</span>
          <span style="font-size:.72rem;letter-spacing:.1em;font-family:Oswald,Impact,sans-serif">
            Rilevatori &middot; In funzione</span>
          <span class="manifesto__emoji" aria-hidden="true">&#128663;</span>
        </div>
        <div class="manifesto__corpo">
          <h3>Parcheggi rosa e velocit&agrave;</h3>
          <p>Il permesso rosa: chi lo chiede, che cosa serve, quanto dura la sosta. E i rilevatori di
             velocit&agrave; rimessi in funzione, segnalati e non nascosti.</p>
          <div><span class="timbro"><span aria-hidden="true">&#9889;</span>
            Velocit&agrave; moderata o multa garantita</span></div>
          <span class="manifesto__vai">Vai alla viabilit&agrave; &rarr;</span>
        </div>
      </a>

    </div>
  </div>
</section>

""" + nastro("nastro--blu") + """

<section class="sezione">
  <div class="contenitore">
    <div class="griglia griglia--3">
      <div class="riquadro">
        <h4><span aria-hidden="true">&#128269;</span> Come si legge questo sito</h4>
        <p>Ogni pagina dice che cosa si fa, da quando e con quale articolo. Niente numeri arrotondati e
           niente date messe l&igrave; per riempire: se una cosa non &egrave; decisa, non sta scritta.</p>
      </div>
      <div class="riquadro">
        <h4><span aria-hidden="true">&#128233;</span> Le segnalazioni si leggono tutte</h4>
        <p>Chi vive un problema lo conosce meglio di chi lo amministra. Un fosso ostruito, un ramo sulla
           strada, un palo spento: scrivilo. Arriva a chi pu&ograve; intervenire.</p>
        <p><a class="bottone bottone--blu" href="https://wa.me/393283692227" target="_blank" rel="noopener">
          Scrivi su WhatsApp</a></p>
      </div>
      <div class="riquadro">
        <h4><span aria-hidden="true">&#128196;</span> Dove stanno gli atti veri</h4>
        <p>Questo non &egrave; il sito istituzionale del Comune. I testi che fanno fede sono quelli
           pubblicati all'albo pretorio del Comune di Roveredo in Piano.</p>
        <p><a class="bottone bottone--bianco" href="https://comune.roveredoinpiano.pn.it/"
              target="_blank" rel="noopener">Sito del Comune</a></p>
      </div>
    </div>
  </div>
</section>
</main>
"""

scrivi("index.html", pagina(
    "index.html",
    "GinoPizza.it | Sì, è ginopizza.it. No, non è una pizzeria",
    "Il sito dell'assessore Guido Costalonga, Roveredo in Piano. Polizia rurale, controllo di vicinato, "
    "vademecum antitruffa, parcheggi rosa, controlli di velocità e Protezione Civile. Atti e date, non promesse.",
    CORPO_INDEX))

# ============================================================
# 2. Polizia rurale: indice e schede
# ============================================================

def ritorno(file_html, testo):
    return """
<section class="sezione">
  <div class="contenitore">
    <a class="ritorno" href="{f}"><span aria-hidden="true">&larr;</span> {t}</a>
  </div>
</section>""".format(f=file_html, t=testo)


RITORNO_RURALE = ritorno("polizia-rurale.html", "Torna al regolamento di polizia rurale")

# ---------- Indice ----------
CORPO_RURALE = """
<main>
<header class="testata">
  <div class="contenitore">
    <span class="testata__occhiello">Atto ufficiale &middot; In vigore dal 13 settembre 2026</span>
    <h1><span aria-hidden="true">&#128668;</span> Regolamento<br>di polizia rurale</h1>
    <p class="testata__sommario">Ottantaquattro articoli, dodici capi, quattro allegati. Approvato
       all'unanimit&agrave; dal Consiglio comunale il 22 giugno 2026, manda in archivio il regolamento
       del 2006 ed &egrave; in vigore dal 13 settembre 2026.</p>
  </div>
</header>

""" + nastro("nastro--giallo") + """

<section class="sezione">
  <div class="contenitore">
    <div>
      <span class="timbro timbro--blu timbro--obliquo"><span aria-hidden="true">&#128668;</span>
        Atto ufficiale: polizia rurale</span>
      <span class="timbro timbro--nero"><span aria-hidden="true">&#9989;</span>
        In vigore dal 13 settembre 2026</span>
      <span class="timbro"><span aria-hidden="true">&#129309;</span> Approvato all'unanimit&agrave;</span>
    </div>

    <div class="tabella-guscio" style="margin-top:20px">
      <table>
        <thead><tr><th scope="col" colspan="2">L'atto in sintesi</th></tr></thead>
        <tbody>
          <tr><td><strong>Organo</strong></td><td>Consiglio comunale di Roveredo in Piano</td></tr>
          <tr><td><strong>Seduta</strong></td><td>22 giugno 2026, approvato <strong>all'unanimit&agrave;</strong></td></tr>
          <tr><td><strong>Entrata in vigore</strong></td><td><strong>13 settembre 2026</strong>
            (articolo 84: il giorno successivo all'avvenuta esecutivit&agrave; della deliberazione)</td></tr>
          <tr><td><strong>Che cosa sostituisce</strong></td><td>Il regolamento di polizia rurale del 2006,
            superato da vent'anni di cambiamenti nelle pratiche agricole, nella tutela della salute pubblica
            e nella normativa nazionale e regionale</td></tr>
          <tr><td><strong>Struttura</strong></td><td>84 articoli, 12 capi, 4 allegati, con nove tavole
            grafiche che illustrano le distanze</td></tr>
          <tr><td><strong>Chi lo applica</strong></td><td>Ufficiali e Agenti di Polizia Locale, e gli
            Ufficiali e Agenti di Polizia Giudiziaria dell'articolo 57 del codice di procedura penale
            (articolo 3)</td></tr>
        </tbody>
      </table>
    </div>

    <div class="riquadro riquadro--nero">
      <h3>In due righe</h3>
      <p>Un fosso ostruito non &egrave; un problema estetico: &egrave; acqua che, quando piove forte,
         finisce in strada e nelle case. Un ramo sporgente non &egrave; un dettaglio: &egrave; un mezzo
         agricolo che non passa e un ciclista che non si vede. Il regolamento mette per iscritto
         manutenzioni che i proprietari seri fanno gi&agrave; da sempre, e d&agrave; alla Polizia Locale
         uno strumento ordinato per intervenire su chi non le fa.</p>
    </div>
  </div>
</section>

<section class="sezione sezione--scura">
  <div class="contenitore">
    <h2 class="sezione__titolo" style="color:#facc15">Che cosa c'&egrave; dentro</h2>
    <p class="sezione__sotto">Cinque schede. Ognuna sta in piedi da sola e ha il suo collegamento,
       cos&igrave; puoi mandarne una sola a chi serve.</p>
    <div class="griglia griglia--2">
""" + scheda("polizia-rurale-diffida.html", "01", "Articolo 4", "&#129309;",
             "La diffida amministrativa",
             "La novit&agrave; che cambia il metodo: davanti a molte violazioni il primo passo non &egrave; "
             "il verbale, ma un invito a sistemare entro dieci giorni.",
             ("Vale una volta sola, non si proroga",
              "Se non si ottempera: da 25 a 150 euro in pi&ugrave;",
              "Perch&eacute; &egrave; un cambiamento culturale")) \
  + scheda("polizia-rurale-obblighi.html", "02", "Gli articoli che toccano tutti", "&#128221;",
           "Gli obblighi, articolo per articolo",
           "Sfalci, fossi, siepi, deflusso delle acque e arature: chi deve fare che cosa, entro quando "
           "e quanto costa non farlo.",
           ("Tre sfalci l'anno: 15 maggio, 30 luglio, 30 settembre",
            "Rami sotto i cinque metri sulla carreggiata",
            "Il metodo in quattro passaggi")) \
  + scheda("polizia-rurale-fuochi.html", "03", "Articolo 14", "&#128293;",
           "I fuochi nei fondi",
           "L'articolo su cui arrivano pi&ugrave; segnalazioni, e quello dove sbagliare costa caro. "
           "Nel centro abitato non si accende, fuori si pu&ograve; ma con regole precise.",
           ("Solo da ottobre a marzo, dalle 7 alle 20",
            "Cento metri da case, strade e boschi",
            "Mai sopra il grado 3 della scala Beaufort")) \
  + scheda("polizia-rurale-distanze.html", "04", "Articoli 22, 34, 39, 49 e 57", "&#128207;",
           "Le distanze, in tabella",
           "Tredici misure raccolte in un posto solo, ricavate dagli articoli e dalle nove tavole "
           "grafiche allegate al regolamento.",
           ("Fossi, alberi, siepi e arbusti dal confine",
            "Apiari, ricoveri, vigneti e frutteti",
            "La finestra per tagliare: 15 ottobre, 15 aprile")) \
  + scheda("polizia-rurale-novita.html", "05", "Come &egrave; nato", "&#127968;",
           "Le altre novit&agrave; e la storia del testo",
           "Il patto di buon vicinato sui nuovi impianti, i prati stabili resi pi&ugrave; semplici, "
           "e un percorso cominciato da un'amministrazione e finito da un'altra.",
           ("Siepi, distanze e compensazioni",
            "Niente obbligo di sfalcio sui prati stabili",
            "Approvato all'unanimit&agrave; da due commissioni")) + """    </div>
  </div>
</section>

<section class="sezione">
  <div class="contenitore">
    <div class="riquadro">
      <h3>Segnala un punto critico</h3>
      <p>Un fosso ostruito, un ramo che sporge su una curva cieca, un cumulo abbandonato lungo una strada
         di campagna. Se lo vedi, dillo: la segnalazione arriva a chi pu&ograve; intervenire.</p>
      <p>Indica il punto nel modo pi&ugrave; preciso possibile, cio&egrave; via, altezza civico o
         riferimento visibile, e se puoi allega una fotografia.</p>
      <div class="fila-bottoni">
        <a class="bottone bottone--blu" href="https://wa.me/393283692227" target="_blank" rel="noopener">
          Segnala su WhatsApp</a>
        <a class="bottone bottone--bianco" href="contatti.html">Tutti i recapiti</a>
        <a class="bottone bottone--bianco" href="https://comune.roveredoinpiano.pn.it/"
           target="_blank" rel="noopener">Albo pretorio del Comune</a>
      </div>
    </div>
  </div>
</section>
</main>
"""

scrivi("polizia-rurale.html", pagina(
    "polizia-rurale.html",
    "Regolamento di polizia rurale | GinoPizza.it",
    "Il regolamento di polizia rurale di Roveredo in Piano, in vigore dal 13 settembre 2026: 84 articoli "
    "approvati all'unanimità il 22 giugno 2026. Diffida amministrativa, obblighi, fuochi, distanze.",
    CORPO_RURALE))


# ---------- 2.1 La diffida amministrativa ----------
CORPO_DIFFIDA = """
<main>
<header class="testata testata--nera">
  <div class="contenitore">
    <span class="testata__occhiello">Polizia rurale &middot; Articolo 4</span>
    <h1><span aria-hidden="true">&#129309;</span> La diffida<br>amministrativa</h1>
    <p class="testata__sommario">Prima si tende la mano. Poi, semmai, si sanziona. Davanti a molte
       violazioni il primo passo non &egrave; pi&ugrave; il verbale, ma un invito a sistemare la situazione
       entro un tempo ragionevole.</p>
  </div>
</header>

""" + nastro("nastro--blu") + """

<section class="sezione">
  <div class="contenitore">
    <div class="riquadro">
      <h3>Come funziona, in concreto</h3>
      <ul class="elenco-timbri">
        <li><span class="icona" aria-hidden="true">&#128221;</span>
          <div><strong>Si applica quando la violazione &egrave; materialmente sanabile entro dieci
          giorni.</strong> L'invito &egrave; contenuto nel verbale di ispezione, notificato agli
          interessati, e indica il termine entro cui uniformarsi alle prescrizioni.</div></li>
        <li><span class="icona" aria-hidden="true">&#9203;</span>
          <div><strong>Il termine non supera i dieci giorni</strong> dalla notifica del verbale.</div></li>
        <li><span class="icona" aria-hidden="true">&#128683;</span>
          <div><strong>Non &egrave; rinnovabile n&eacute; prorogabile</strong>, e non &egrave; ammessa
          quando il trasgressore &egrave; gi&agrave; stato diffidato per la stessa violazione. Vale una
          volta sola: la seconda volta si va dritti al verbale.</div></li>
        <li><span class="icona" aria-hidden="true">&#128101;</span>
          <div><strong>Se il trasgressore non &egrave; presente</strong>, la diffida va notificata
          all'obbligato in solido ai sensi della legge 689 del 1981. Se i proprietari interessati sono
          pi&ugrave; di uno, basta notificarla a un solo obbligato in solido.</div></li>
        <li><span class="icona" aria-hidden="true">&#9878;</span>
          <div><strong>Se non si ottempera</strong> si redige il verbale di accertamento e, oltre alla
          sanzione prevista per l'articolo violato, scatta un'ulteriore somma <strong>da 25 euro a
          150 euro</strong>, in misura ridotta <strong>50 euro</strong>, oltre alle spese di
          procedimento.</div></li>
      </ul>
    </div>

    <div class="riquadro riquadro--giallo">
      <p class="sigillo-grande" style="margin-bottom:14px">Un cambiamento culturale</p>
      <p>&laquo;&Egrave; un cambiamento culturale prima ancora che giuridico: un'amministrazione che prima
         di punire tende la mano. La sanzione resta ferma per chi non vuole adeguarsi, ma diamo a tutti la
         possibilit&agrave; di fare la cosa giusta.&raquo;</p>
      <p style="font-size:.9rem"><strong>Guido Costalonga</strong>, assessore alla Sicurezza,
         comunicato del 23 giugno 2026.</p>
    </div>

    <div class="riquadro riquadro--nero">
      <h3>Su quali articoli si applica</h3>
      <p>Il regolamento richiama espressamente la diffida per lo sfalcio dei terreni (articolo 7), la
         gestione di fossi e canali privati (articolo 40), la manutenzione dei fossi a bordo strada
         (articolo 44), le siepi e gli alberi che si protendono sulle strade (articolo 48), il deflusso
         delle acque meteoriche dalle case rurali (articolo 27) e le misure contro la proliferazione dei
         colombi (articolo 21).</p>
      <p><a href="polizia-rurale-obblighi.html">Vai alla tabella degli obblighi &rarr;</a></p>
    </div>
  </div>
</section>
""" + RITORNO_RURALE + """
</main>
"""

scrivi("polizia-rurale-diffida.html", pagina(
    "polizia-rurale-diffida.html",
    "La diffida amministrativa | GinoPizza.it",
    "L'articolo 4 del regolamento di polizia rurale di Roveredo in Piano: dieci giorni per sanare, una "
    "volta sola, e che cosa succede a chi non ottempera.",
    CORPO_DIFFIDA))


# ---------- 2.2 Gli obblighi ----------
CORPO_OBBLIGHI = """
<main>
<header class="testata">
  <div class="contenitore">
    <span class="testata__occhiello">Polizia rurale &middot; Gli articoli che toccano tutti</span>
    <h1><span aria-hidden="true">&#128221;</span> Gli obblighi,<br>articolo per articolo</h1>
    <p class="testata__sommario">Sintesi divulgativa degli articoli che riguardano il maggior numero di
       persone. Il testo che fa fede &egrave; il regolamento approvato e pubblicato all'albo pretorio.
       Gli importi sono minimo, massimo e pagamento in misura ridotta.</p>
  </div>
</header>

""" + nastro("nastro--giallo") + """

<section class="sezione">
  <div class="contenitore">
    <div class="tabella-guscio">
      <table>
        <thead>
          <tr><th scope="col">Articolo</th><th scope="col">Che cosa si chiede</th>
              <th scope="col">A chi</th><th scope="col">Sanzione</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Art. 7</strong><br>Sfalcio dei terreni</td>
            <td>Sfalcio almeno <strong>tre volte l'anno: entro il 15 maggio, il 30 luglio e il
                30 settembre</strong>. Prima, se l'erba supera i 40 centimetri e ci sono problemi di
                zanzare, bisce o ratti. Vale per giardini, orti, campi, lotti inedificati e terreni
                incolti.</td>
            <td>Proprietari e conduttori a qualsiasi titolo</td>
            <td>Diffida, poi da <strong>50 a 300 euro</strong>, ridotta <strong>100 euro</strong></td>
          </tr>
          <tr>
            <td><strong>Art. 40</strong><br>Fossi e canali privati</td>
            <td>Tenere i fossi spurgati e sgombri dalla vegetazione; sfalciare <strong>tre volte
                l'anno</strong> le erbe dei fossi prospicienti le strade pubbliche, con le stesse
                scadenze, e riconsolidare le scarpate; mantenere espurgate chiaviche e paratoie;
                rimuovere alberi, tronchi e rami caduti nei corsi d'acqua.
                <strong>Vietato sopprimere fossi, canali e terrazzamenti.</strong></td>
            <td>Proprietari dei fossi o loro aventi causa</td>
            <td>Diffida, poi da <strong>75 a 450 euro</strong>, ridotta <strong>150 euro</strong></td>
          </tr>
          <tr>
            <td><strong>Art. 44</strong><br>Fossi a bordo strada</td>
            <td>Manutenzione <strong>ogni volta che la capacit&agrave; di deflusso risulta
                limitata</strong>. I fossi delle strade vicinali sono tenuti in manutenzione dai
                frontisti. In caso di inadempienza il Comune fa eseguire i lavori
                <strong>a spese dell'inadempiente</strong>.</td>
            <td>Frontisti delle strade vicinali; le amministrazioni per le proprie strade</td>
            <td>Diffida, poi da <strong>75 a 450 euro</strong>, ridotta <strong>150 euro</strong></td>
          </tr>
          <tr>
            <td><strong>Art. 48</strong><br>Siepi e alberi sulle strade</td>
            <td>Tagliare i rami che si protendono sulla sede stradale <strong>a quote inferiori a cinque
                metri</strong>; non ostacolare segnaletica, illuminazione e infrastrutture; rimuovere
                <strong>nel pi&ugrave; breve tempo possibile</strong> alberi e rami caduti; recidere le
                radici che alterano la pavimentazione; tenere puliti marciapiede, cunetta, banchina e
                caditoie da fogliame e rami.</td>
            <td>Proprietari e conduttori dei fondi confinanti, condomini compresi</td>
            <td>Diffida, poi da <strong>75 a 450 euro</strong>, ridotta <strong>150 euro</strong></td>
          </tr>
          <tr>
            <td><strong>Art. 43</strong><br>Deflusso delle acque</td>
            <td>Non impedire il libero deflusso delle acque dai fondi superiori; niente piantagioni,
                costruzioni o movimenti di terra che riducano la sezione di deflusso; impedire che l'acqua
                di pioggia o di irrigazione finisca sulla sede stradale.</td>
            <td>Proprietari dei terreni</td>
            <td>Da <strong>75 a 450 euro</strong>, ridotta <strong>150 euro</strong></td>
          </tr>
          <tr>
            <td><strong>Art. 47</strong><br>Arature a bordo strada</td>
            <td>Fascia di rispetto, la <strong>capezzagna</strong>: almeno <strong>1 metro</strong> dal
                ciglio se l'aratura &egrave; parallela alla strada, <strong>1,50 metri</strong> se c'&egrave;
                dislivello, <strong>3 metri</strong> se &egrave; perpendicolare, per le manovre dei mezzi
                agricoli. Fascia tampone lungo i corsi d'acqua pubblici: <strong>5 metri</strong> per
                vigneti e frutteti sotto i 3 metri, <strong>10 metri</strong> per alberi di alto fusto,
                <strong>4 metri</strong> in presenza di argine.</td>
            <td>Chi lavora il fondo</td>
            <td>Da <strong>75 a 450 euro</strong>, ridotta <strong>150 euro</strong></td>
          </tr>
          <tr>
            <td><strong>Art. 45</strong><br>Scarico nei fossi</td>
            <td>&Egrave; vietato convogliare <strong>qualsiasi sostanza diversa dalle acque
                meteoriche</strong> nei fossi delle strade, nei canali di scolo e nelle cunette.</td>
            <td>Chiunque</td>
            <td>Sanzioni del decreto legislativo 152 del 2006</td>
          </tr>
          <tr>
            <td><strong>Art. 5</strong><br>Sanzione residuale</td>
            <td>Per le violazioni del regolamento che non hanno una sanzione propria. Pagamento in misura
                ridotta entro <strong>60 giorni</strong> dalla contestazione o dalla notifica.</td>
            <td>Chiunque</td>
            <td>Da <strong>25 a 500 euro</strong>, ridotta <strong>50 euro</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#9888;</span> Se il danno c'&egrave; gi&agrave; stato</h3>
        <p>Oltre alla sanzione, chi provoca danni a beni comuni &egrave; tenuto al <strong>rimborso di tutte
           le spese di ripristino</strong>. Quando il verbale impone di rimettere a posto i luoghi, il
           termine &egrave; di <strong>30 giorni</strong>: scaduto quello, il Comune emette ordinanza e poi
           esegue d'ufficio a spese dell'obbligato, recuperando le somme con ordinanza ingiunzione, che
           &egrave; titolo esecutivo. Nei casi previsti scatta anche il deferimento all'Autorit&agrave;
           Giudiziaria ai sensi dell'articolo 650 del codice penale.</p>
      </div>
      <div class="riquadro riquadro--nero">
        <h3>Il metodo, in quattro passaggi</h3>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128226;</span>
            <div><strong>Informazione.</strong> Il regolamento va conosciuto prima di essere applicato.
            Chi non sa non pu&ograve; adeguarsi.</div></li>
          <li><span class="icona" aria-hidden="true">&#128221;</span>
            <div><strong>Sopralluogo e diffida.</strong> La Polizia Locale accerta e indica che cosa
            sistemare, con un termine non superiore a dieci giorni.</div></li>
          <li><span class="icona" aria-hidden="true">&#9878;</span>
            <div><strong>Sanzione.</strong> Solo per chi, avvisato, decide di non fare niente. E la
            diffida vale una volta sola.</div></li>
          <li><span class="icona" aria-hidden="true">&#128295;</span>
            <div><strong>Esecuzione in danno.</strong> Quando c'&egrave; pericolo per la circolazione o
            per il deflusso delle acque, il Comune interviene e addebita il costo.</div></li>
        </ul>
        <p><a href="polizia-rurale-diffida.html">Come funziona la diffida &rarr;</a></p>
      </div>
    </div>
  </div>
</section>
""" + RITORNO_RURALE + """
</main>
"""

scrivi("polizia-rurale-obblighi.html", pagina(
    "polizia-rurale-obblighi.html",
    "Gli obblighi del regolamento di polizia rurale | GinoPizza.it",
    "Sfalci, fossi e canali, siepi e alberi sulle strade, deflusso delle acque e arature a Roveredo in "
    "Piano: chi deve fare che cosa, entro quando e quanto costa non farlo.",
    CORPO_OBBLIGHI))


# ---------- 2.3 I fuochi nei fondi ----------
CORPO_FUOCHI = """
<main>
<header class="testata testata--nera">
  <div class="contenitore">
    <span class="testata__occhiello">Polizia rurale &middot; Articolo 14</span>
    <h1><span aria-hidden="true">&#128293;</span> I fuochi<br>nei fondi</h1>
    <p class="testata__sommario">&Egrave; l'articolo su cui arrivano pi&ugrave; segnalazioni, ed &egrave;
       anche quello dove l'errore costa caro. Nel centro abitato non si accende. Fuori si pu&ograve;, ma
       con regole precise.</p>
  </div>
</header>

""" + nastro("nastro--giallo") + """

<section class="sezione">
  <div class="contenitore">
    <div class="griglia griglia--2">
      <div class="riquadro riquadro--blu">
        <h3><span aria-hidden="true">&#10060;</span> Nel centro abitato: vietato</h3>
        <p>Nei centri abitati come definiti dal Codice della Strada e riportati nel Piano Regolatore
           &egrave; <strong>vietato accendere fuochi</strong> per smaltire sterpaglia, residui di potatura,
           residui del taglio delle siepi e residui colturali.</p>
        <p>Lo smaltimento avviene con il conferimento secondo le indicazioni del Comune, cio&egrave; benne e
           centri di raccolta, oppure con triturazione e aspersione sul terreno.</p>
      </div>
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#9989;</span> Fuori dal centro abitato: si pu&ograve;, con regole</h3>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128197;</span><div>Solo <strong>da ottobre a marzo
            compresi</strong>, con residui secchi.</div></li>
          <li><span class="icona" aria-hidden="true">&#128336;</span><div>Solo <strong>dalle 7.00 alle
            20.00</strong>.</div></li>
          <li><span class="icona" aria-hidden="true">&#128230;</span><div>Piccoli cumuli, non oltre
            <strong>tre metri steri per ettaro al giorno</strong>, nel luogo di produzione.</div></li>
          <li><span class="icona" aria-hidden="true">&#128207;</span><div>Almeno <strong>100 metri</strong>
            da qualsiasi fabbricato, dalle strade pubbliche, dai luoghi pubblici, dalle ferrovie e dagli
            ambiti boscati o di tutela ambientale.</div></li>
          <li><span class="icona" aria-hidden="true">&#128065;</span><div><strong>Presidio ininterrotto</strong>
            di almeno una persona maggiorenne fino al completo spegnimento.</div></li>
          <li><span class="icona" aria-hidden="true">&#127788;</span><div><strong>Mai con vento superiore
            al grado 3 della scala Beaufort.</strong></div></li>
        </ul>
      </div>
    </div>

    <div class="riquadro">
      <h3>Che cosa non si brucia, mai</h3>
      <p><strong>Teli, legacci non vegetali, sacchi, imballaggi e rifiuti di qualsiasi natura</strong>
         non sono un fuoco agricolo: sono smaltimento di rifiuti non autorizzato, punito ai sensi del
         decreto legislativo 152 del 2006 e dell'articolo 674 del codice penale.</p>
      <p>Resta consentita l'accensione per cuocere cibi o riscaldare persone all'addiaccio, purch&eacute;
         controllata e confinata, con legna, carbone o loro derivati.</p>
      <p>Violazioni dell'articolo 14: da <strong>75 a 450 euro</strong>, in misura ridotta
         <strong>150 euro</strong>.</p>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--nero">
        <h3><span aria-hidden="true">&#127881;</span> I fal&ograve; epifanici</h3>
        <p>Sono consentiti nel rispetto della normativa di settore e delle eventuali ordinanze sindacali
           sull'inquinamento atmosferico. La richiesta di accensione deve pervenire al protocollo comunale
           <strong>almeno sette giorni prima</strong> dell'evento.</p>
      </div>
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#127807;</span> A fini fitosanitari, articolo 15</h3>
        <p>L'abbruciamento di materiale vegetale prodotto nel fondo &egrave; ammesso
           <strong>tutto l'anno, anche dentro il centro abitato</strong>, ma solo per necessit&agrave;
           fitosanitarie accertate dal Servizio fitosanitario e chimico dell'ERSA FVG, con le stesse
           cautele: cumulo a 100 metri da strade, luoghi pubblici, ferrovie e abitazioni, presidio
           continuo, niente vento sopra il grado 3.</p>
        <p>Stessa sanzione: da <strong>75 a 450 euro</strong>, ridotta <strong>150 euro</strong>.</p>
      </div>
    </div>

    <div class="riquadro riquadro--blu">
      <h3><span aria-hidden="true">&#9888;</span> Il Comune pu&ograve; fermare tutto</h3>
      <p>Il Comune e le altre amministrazioni competenti in materia ambientale possono
         <strong>sospendere, differire o vietare</strong> la combustione quando le condizioni
         meteorologiche, climatiche o ambientali sono sfavorevoli, o quando ne possono derivare rischi
         per l'incolumit&agrave; e per la salute, con particolare riferimento al Piano d'Azione Comunale
         contro gli episodi acuti di inquinamento atmosferico.</p>
    </div>
  </div>
</section>
""" + RITORNO_RURALE + """
</main>
"""

scrivi("polizia-rurale-fuochi.html", pagina(
    "polizia-rurale-fuochi.html",
    "I fuochi nei fondi | GinoPizza.it",
    "Articolo 14 del regolamento di polizia rurale di Roveredo in Piano: dove e quando si può accendere "
    "un fuoco agricolo, con quali distanze e cautele, e che cosa non si brucia mai.",
    CORPO_FUOCHI))


# ---------- 2.4 Le distanze ----------
CORPO_DISTANZE = """
<main>
<header class="testata">
  <div class="contenitore">
    <span class="testata__occhiello">Polizia rurale &middot; Articoli 22, 34, 39, 49 e 57</span>
    <h1><span aria-hidden="true">&#128207;</span> Le distanze,<br>in tabella</h1>
    <p class="testata__sommario">Le nove tavole grafiche allegate al regolamento illustrano questi valori
       disegno per disegno. Qui sono raccolti in una tabella sola, per non doverli cercare.</p>
  </div>
</header>

""" + nastro("nastro--giallo") + """

<section class="sezione">
  <div class="contenitore">
    <div class="tabella-guscio">
      <table>
        <thead><tr><th scope="col">Che cosa</th><th scope="col">Distanza minima</th>
            <th scope="col">Riferimento</th></tr></thead>
        <tbody>
          <tr><td>Nuovo fosso o canale dal confine di propriet&agrave;</td>
              <td>Pari alla profondit&agrave; del fosso, <strong>mai meno di 1 metro</strong></td>
              <td>Art. 39, comma 1</td></tr>
          <tr><td>Nuovo fosso o canale dal confine stradale</td>
              <td><strong>Mai meno di 3 metri</strong> dal confine demaniale</td>
              <td>Art. 39, comma 2</td></tr>
          <tr><td>Alberi lungo il demanio stradale, fuori dal centro abitato</td>
              <td>Non meno dell'altezza massima raggiungibile a fine ciclo vegetativo e comunque
                  <strong>non meno di 6 metri</strong></td>
              <td>Art. 39, comma 5</td></tr>
          <tr><td>Viti, siepi e arbusti a forma libera dal confine</td>
              <td><strong>50 centimetri</strong></td><td>Tavola 01, articolo 892 del codice civile</td></tr>
          <tr><td>Alberi a capitozza, altezza inferiore a 3 metri</td>
              <td><strong>1,50 metri</strong></td><td>Tavola 01, articolo 892 del codice civile</td></tr>
          <tr><td>Alberi di alto fusto, altezza superiore a 3 metri</td>
              <td><strong>3 metri</strong></td><td>Tavola 01, articolo 892 del codice civile</td></tr>
          <tr><td>Apiari dalle strade di pubblico transito</td>
              <td><strong>10 metri</strong> con il predellino d'involo</td><td>Art. 22, comma 2</td></tr>
          <tr><td>Apiari dai confini di propriet&agrave;</td>
              <td><strong>5 metri</strong></td><td>Art. 22, comma 2</td></tr>
          <tr><td>Nuovi vigneti e frutteti dal confine stradale</td>
              <td><strong>6 metri</strong> con siepe verde pi&ugrave; alta di almeno 1 metro rispetto alla
                  coltura, <strong>10 metri</strong> senza siepe</td>
              <td>Art. 49, comma 4</td></tr>
          <tr><td>Nuovi vigneti e frutteti dalle abitazioni altrui e dalle aree sensibili</td>
              <td><strong>30 metri</strong>, con 10 metri dal confine di propriet&agrave;, riducibili a
                  5 metri con siepe o con irroratrice antideriva</td>
              <td>Art. 49, comma 5</td></tr>
          <tr><td>Fascia a riposo dai corsi d'acqua individuati come corridoi ecologici</td>
              <td><strong>30 metri</strong></td><td>Art. 49, comma 2</td></tr>
          <tr><td>Fascia a riposo dai corpi idrici superficiali e dai bacini</td>
              <td><strong>15 metri</strong></td><td>Art. 49, comma 2</td></tr>
          <tr><td>Nuovi ricoveri zootecnici dalle abitazioni e dai confini altrui</td>
              <td><strong>20 metri</strong></td><td>Art. 34, comma 2</td></tr>
        </tbody>
      </table>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--nero">
        <h3><span aria-hidden="true">&#127795;</span> Una data da segnare: 15 ottobre</h3>
        <p>Il taglio delle specie arboree deve avvenire <strong>in periodo di riposo vegetativo, tra il
           15 ottobre e il 15 aprile</strong>, avendo cura di mantenere vitale la capacit&agrave;
           vegetativa delle piante (articolo 57). Fuori da quella finestra non si taglia.</p>
      </div>
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#128221;</span> Prima di piantare, avvisa</h3>
        <p>L'impianto o il reimpianto di colture arboree permanenti a bordo strada, cio&egrave; frutteti,
           pioppeti, vigneti, arboreti da legna e biomassa, &egrave; subordinato a
           <strong>preventiva comunicazione all'ufficio comunale competente</strong>, corredata dagli
           elementi informativi dell'impianto (articolo 46).</p>
        <p>Chi non la fa: da <strong>50 a 300 euro</strong>, ridotta <strong>100 euro</strong>.</p>
      </div>
    </div>
  </div>
</section>
""" + RITORNO_RURALE + """
</main>
"""

scrivi("polizia-rurale-distanze.html", pagina(
    "polizia-rurale-distanze.html",
    "Le distanze del regolamento di polizia rurale | GinoPizza.it",
    "Tredici distanze minime del regolamento di polizia rurale di Roveredo in Piano: fossi, alberi, siepi, "
    "apiari, vigneti e frutteti, ricoveri zootecnici, con l'articolo di riferimento.",
    CORPO_DISTANZE))


# ---------- 2.5 Le novità del testo ----------
CORPO_NOVITA = """
<main>
<header class="testata testata--gialla">
  <div class="contenitore">
    <span class="testata__occhiello">Polizia rurale &middot; Come &egrave; nato</span>
    <h1><span aria-hidden="true">&#127968;</span> Le altre novit&agrave;<br>e la storia del testo</h1>
    <p class="testata__sommario">Oltre alla diffida amministrativa, il regolamento porta due cambiamenti
       che si vedono sul territorio: un patto di buon vicinato sui nuovi impianti e i prati stabili resi
       finalmente convenienti.</p>
  </div>
</header>

""" + nastro("nastro--blu") + """

<section class="sezione">
  <div class="contenitore">
    <div class="griglia griglia--2">
      <div class="riquadro">
        <h3><span aria-hidden="true">&#127968;</span> Un patto di buon vicinato</h3>
        <p>Il regolamento introduce misure di mitigazione per i nuovi impianti di frutteti e vigneti, a
           protezione delle abitazioni, delle scuole e delle aree dove giocano i bambini: siepi arboree e
           arbustive con piante autoctone lungo il confine, distanze maggiorate, opere di compensazione non
           inferiori al <strong>5 per cento</strong> della superficie coltivata.</p>
        <p>&laquo;Non &egrave; un atto contro l'agricoltura, che resta una ricchezza fondamentale del nostro
           territorio. &Egrave; un patto di buon vicinato: chi coltiva pu&ograve; continuare a farlo, e chi
           abita accanto ai campi pu&ograve; farlo con maggiore serenit&agrave;.&raquo;</p>
        <p><a href="polizia-rurale-distanze.html">Le distanze esatte &rarr;</a></p>
      </div>
      <div class="riquadro">
        <h3><span aria-hidden="true">&#127807;</span> Prati stabili, meno ostacoli</h3>
        <p>I prati stabili naturali sono patrimonio di biodiversit&agrave; e di paesaggio, tutelati dalla
           legge regionale 29 aprile 2005, n. 9. Il nuovo testo semplifica le condizioni e rimuove gli
           ostacoli che rendevano complicato e poco conveniente realizzarne di nuovi.</p>
        <p>Per i prati stabili, e per i terreni che il proprietario ha dichiarato alla Regione di voler
           trasformare in prato stabile, <strong>non vale l'obbligo dei tre sfalci</strong> dell'articolo 7:
           si applica la normativa regionale.</p>
        <p>Perch&eacute; &laquo;fare la cosa giusta per l'ambiente sia non solo possibile, ma anche
           conveniente&raquo;.</p>
      </div>
    </div>
  </div>
</section>

<section class="sezione sezione--scura">
  <div class="contenitore">
    <h2 class="sezione__titolo" style="color:#facc15">Un lavoro di due amministrazioni</h2>
    <div class="riquadro">
      <p>Il percorso &egrave; stato avviato nella scorsa legislatura e portato a compimento dall'attuale.
         Le due commissioni hanno approvato il testo all'unanimit&agrave;, e cos&igrave; ha fatto il
         Consiglio comunale nella seduta del 22 giugno 2026.</p>
      <p>Il ringraziamento dell'assessore &egrave; andato a chi ha avviato il percorso, l'allora assessore
         <strong>Igor Barbariol</strong>, ai comandanti della Polizia Locale che si sono succeduti alla
         guida del Corpo, <strong>Angelo Segatto</strong>, che ha impostato il lavoro, e
         <strong>Cristiano Ciletti</strong>, che lo ha condotto al traguardo, a tutti gli operatori e ai
         portatori di interesse coinvolti, e al Sindaco <strong>Paolo Nadal</strong>, per i correttivi
         suggeriti e per avere aiutato a tenere i piedi per terra.</p>
      <p>&laquo;Questo regolamento non &egrave; il lavoro di una sola persona, n&eacute; di una sola
         stagione amministrativa. &Egrave; una storia di continuit&agrave;: un'amministrazione ha iniziato,
         un'altra ha completato. &Egrave; il modo in cui le istituzioni dovrebbero funzionare, mettendo
         davanti a tutto il bene della comunit&agrave;, al di l&agrave; di chi taglia il nastro.&raquo;</p>
    </div>
    <div class="riquadro riquadro--blu">
      <p style="font-family:Oswald,Impact,sans-serif;text-transform:uppercase;font-size:1.4rem;line-height:1.25;margin:0">
        &laquo;Non &egrave; il regolamento di una maggioranza o di un assessore:<br>
        &egrave; il regolamento di Roveredo in Piano.&raquo;</p>
    </div>
  </div>
</section>
""" + RITORNO_RURALE + """
</main>
"""

scrivi("polizia-rurale-novita.html", pagina(
    "polizia-rurale-novita.html",
    "Le novità del regolamento di polizia rurale | GinoPizza.it",
    "Il patto di buon vicinato sui nuovi impianti di vigneti e frutteti, i prati stabili resi più semplici, "
    "e la storia di un testo cominciato da un'amministrazione e finito da un'altra.",
    CORPO_NOVITA))


# ============================================================
# 3. Sicurezza: indice e schede
# ============================================================
RITORNO_SICUREZZA = ritorno("sicurezza-territorio.html", "Torna a sicurezza e truffe")

CORPO_SICUREZZA = """
<main>
<header class="testata testata--nera">
  <div class="contenitore">
    <span class="testata__occhiello">Delega sicurezza</span>
    <h1><span aria-hidden="true">&#128065;</span> Sicurezza<br>del territorio</h1>
    <p class="testata__sommario">Due cose insieme: cittadini che imparano a guardare nel modo giusto e un
       vademecum che smonta i raggiri uno per uno. Niente ronde, niente paura: solo occhi aperti e numeri
       giusti da chiamare.</p>
  </div>
</header>

""" + nastro("nastro--blu") + """

<section class="sezione">
  <div class="contenitore">
    <div>
      <span class="timbro timbro--nero timbro--obliquo"><span aria-hidden="true">&#128065;</span>
        Vigilanza civica: occhi aperti</span>
      <span class="timbro timbro--blu"><span aria-hidden="true">&#128680;</span>
        Allerta truffe: vademecum costalonga.org</span>
    </div>

    <div class="riquadro riquadro--giallo" style="margin-top:20px">
      <h3><span aria-hidden="true">&#9878;</span> Fermezza s&igrave;, allarmismi no</h3>
      <p>Le truffe sono un fenomeno molto diffuso e prendono di mira soprattutto le persone fragili o
         anziane. Non colpiscono per caso: seguono copioni collaudati, quasi sempre gli stessi.
         <strong>Chi li conosce li riconosce, e chi li riconosce non ci casca.</strong></p>
      <p>Si pu&ograve; uscire di casa, rispondere al telefono e comprare in rete. Basta sapere dove
         guardare.</p>
      <div class="fila-bottoni">
        <a class="bottone bottone--blu" href="tel:112">In emergenza: 112</a>
        <a class="bottone bottone--bianco" href="https://costalonga.org/truffe/"
           target="_blank" rel="noopener">Vademecum completo in 24 punti</a>
      </div>
    </div>
  </div>
</section>

<section class="sezione sezione--scura">
  <div class="contenitore">
    <h2 class="sezione__titolo" style="color:#facc15">Che cosa c'&egrave; dentro</h2>
    <p class="sezione__sotto">Due schede. Il vademecum &egrave; pensato per essere stampato tutto intero e
       appeso vicino al telefono, oppure mandato cos&igrave; com'&egrave; a un genitore anziano.</p>
    <div class="griglia griglia--2">
""" + scheda("controllo-di-vicinato.html", "01", "Protocollo con la Prefettura", "&#128101;",
             "Il controllo di vicinato",
             "Un gruppo di volontari chiede alla Polizia Locale di aderire, nomina un coordinatore e "
             "segnala quello che stona. Nessuna ronda, nessun pattugliamento: &egrave; scritto nero su bianco.",
             ("Come si fa domanda e si costituisce un gruppo",
              "Che cosa si segnala, voce per voce",
              "I compiti del coordinatore")) \
  + scheda("vademecum-antitruffa.html", "02", "Ministero dell'Interno, Polizia Postale, Carabinieri",
           "&#128680;",
           "Il vademecum antitruffa",
           "Tutti i raggiri in una pagina sola, da stampare e tenere vicino al telefono: come funzionano, "
           "il segnale che li smaschera, cosa fare subito e cosa non fare mai.",
           ("Quattro truffe alla porta di casa",
            "Sei truffe fuori casa, al telefono, allo sportello",
            "I segnali, cosa fare se &egrave; gi&agrave; successo, i numeri utili")) + """    </div>
  </div>
</section>

<section class="sezione">
  <div class="contenitore">
    <div class="riquadro riquadro--nero">
      <h3>Le fonti</h3>
      <p>Tutti i contenuti sulle truffe sono ripresi dal vademecum pubblicato su
         <a href="https://costalonga.org/truffe/" target="_blank" rel="noopener">costalonga.org/truffe</a>,
         che a sua volta raccoglie soltanto quanto scrivono tre fonti ufficiali: il
         <strong>Ministero dell'Interno</strong>, la <strong>Polizia Postale e delle Comunicazioni</strong>
         e l'<strong>Arma dei Carabinieri</strong>. Nessun dato aggiunto, nessuna statistica inventata.</p>
    </div>
  </div>
</section>
</main>
"""

scrivi("sicurezza-territorio.html", pagina(
    "sicurezza-territorio.html",
    "Sicurezza del territorio | GinoPizza.it",
    "Controllo di vicinato a Roveredo in Piano e vademecum antitruffa: le truffe alla porta, quelle fuori "
    "casa, i segnali di allarme e cosa fare se è già successo. Numero unico di emergenza 112.",
    CORPO_SICUREZZA))


# ---------- 3.1 Controllo di vicinato ----------
CORPO_VICINATO = """
<main>
<header class="testata">
  <div class="contenitore">
    <span class="testata__occhiello">Sicurezza &middot; Protocollo con la Prefettura di Pordenone</span>
    <h1><span aria-hidden="true">&#128101;</span> Il controllo<br>di vicinato</h1>
    <p class="testata__sommario">Il Comune ha sottoscritto il protocollo d'intesa con la Prefettura di
       Pordenone. Un gruppo di volontari chiede alla Polizia Locale di aderire, nomina un coordinatore e da
       l&igrave; segnala quello che stona. &Egrave; una forma di <strong>partecipazione
       passiva</strong>: si guarda e si riferisce, nient'altro.</p>
  </div>
</header>

""" + nastro("nastro--giallo") + """

<section class="sezione">
  <div class="contenitore">
    <div class="doppia-colonna" style="margin-bottom:24px">
      <div class="colonna-fare">
        <h4><span aria-hidden="true">&#9989;</span> Che cos'&egrave;</h4>
        <ul>
          <li><strong>Un gruppo di cittadini volontari che fa domanda alla Polizia Locale</strong> per
              aderire al progetto. Non ci si arruola da soli: le adesioni le vaglia il Comune.</li>
          <li>Una volta costituito, il gruppo <strong>nomina un proprio coordinatore</strong>, che &egrave;
              l'unico tramite con la Polizia Locale e con le forze dell'ordine.</li>
          <li>Da l&igrave; in avanti, attenzione consapevole alla propria via e un canale ordinato di
              segnalazione, che passa sempre dal coordinatore.</li>
          <li>Cartelli che comunicano che il vicinato &egrave; attento a quello che avviene nella zona:
              i molti occhi dei residenti sono un deterrente contro i furti.</li>
          <li>Reciproca assistenza fra vicini: sorveglianza delle case, attenzione ai vicini anziani e soli,
              ritiro della posta per assenze prolungate.</li>
        </ul>
      </div>
      <div class="colonna-mai">
        <h4><span aria-hidden="true">&#10060;</span> Che cosa non &egrave;, mai</h4>
        <ul>
          <li><strong>Non sono ronde.</strong> Il progetto si dissocia totalmente da quel concetto.</li>
          <li><strong>Con l'adesione &egrave; vietata qualunque forma di pattugliamento</strong> del
              territorio, personale, individuale o collettiva.</li>
          <li>Non presuppone atti eroici, non ha funzioni repressive e <strong>non invita a fermare i
              malviventi</strong>.</li>
          <li>&Egrave; un sistema di prevenzione: serve a evitare che i reati avvengano.</li>
        </ul>
      </div>
    </div>

    <div class="riquadro riquadro--blu">
      <h3><span aria-hidden="true">&#128226;</span> Che cosa si segnala</h3>
      <p>Sono le situazioni inusuali e i comportamenti sospetti elencati dal protocollo:</p>
      <div class="doppia-colonna">
        <div class="colonna-fare">
          <ul>
            <li>Mezzi di trasporto o persone palesemente sospetti.</li>
            <li>Fuga sospetta di mezzi o persone.</li>
            <li>Auto, motociclette o velocipedi in luogo pubblico che si sospettano rubati.</li>
            <li>Persone in stato confusionale o in evidente difficolt&agrave;.</li>
            <li>Ostacoli sulle vie di comunicazione.</li>
            <li>Interruzione dei servizi di fornitura di energia.</li>
          </ul>
        </div>
        <div class="colonna-fare">
          <ul>
            <li>Situazioni significative di degrado urbano e disagio.</li>
            <li>Atti vandalici.</li>
            <li>Gravi fenomeni di bullismo.</li>
            <li>Utilizzo indebito di spazi pubblici.</li>
            <li>Luoghi di ritrovo per sospetto spaccio di sostanze stupefacenti.</li>
          </ul>
        </div>
      </div>
      <p style="margin-top:14px"><strong>Attenzione: le urgenze non passano dal gruppo.</strong> Solo in
         presenza di situazioni che richiedono l'immediato intervento delle forze di Polizia, per esempio
         furti, rapine e aggressioni, i componenti del gruppo chiamano direttamente il
         <strong>numero unico di emergenza 112</strong>.</p>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#128101;</span> Come si costituisce un gruppo</h3>
        <p>Il Comune, tramite la Polizia Locale, mette a disposizione i moduli con cui costituire un gruppo,
           creare una chiacchierata telefonica di zona e raccogliere i dati della propria area.</p>
        <p><strong>Ogni gruppo nomina un coordinatore</strong>, che fa da tramite con le forze
           dell'ordine e ha quattro compiti:</p>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128269;</span>
            <div>Filtrare le segnalazioni prima di inviarle alle forze dell'ordine.</div></li>
          <li><span class="icona" aria-hidden="true">&#128233;</span>
            <div>Diffondere nel gruppo gli avvisi ricevuti dalle forze di Polizia.</div></li>
          <li><span class="icona" aria-hidden="true">&#128064;</span>
            <div>Stimolare il gruppo a prestare attenzione a quello che avviene nella zona, aiutando a
            individuare fattori di rischio e vulnerabilit&agrave;.</div></li>
          <li><span class="icona" aria-hidden="true">&#129309;</span>
            <div>Invitare altri cittadini ad aderire.</div></li>
        </ul>
      </div>
      <div class="riquadro">
        <h3><span aria-hidden="true">&#127963;</span> Che cosa fa il Comune</h3>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128226;</span>
            <div>Realizza incontri di presentazione del controllo di vicinato alla cittadinanza.</div></li>
          <li><span class="icona" aria-hidden="true">&#128203;</span>
            <div>Vaglia le adesioni, ascolta e valuta proposte e richieste dei cittadini.</div></li>
          <li><span class="icona" aria-hidden="true">&#128681;</span>
            <div>Installa i cartelli informativi nelle zone dove i gruppi sono costituiti.</div></li>
          <li><span class="icona" aria-hidden="true">&#128222;</span>
            <div>Tramite la Polizia Locale mantiene i contatti con i coordinatori.</div></li>
          <li><span class="icona" aria-hidden="true">&#128680;</span>
            <div>Organizza incontri per informare sui comportamenti corretti da tenere per evitare raggiri
            e furti.</div></li>
        </ul>
      </div>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#128101;</span> Chi pu&ograve; aderire</h3>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128100;</span>
            <div>Singoli cittadini maggiorenni interessati al benessere della propria
            comunit&agrave;.</div></li>
          <li><span class="icona" aria-hidden="true">&#127978;</span>
            <div>Commercianti ed esercenti attivi nel quartiere o nella frazione.</div></li>
          <li><span class="icona" aria-hidden="true">&#129309;</span>
            <div>Gruppi di cittadini organizzati che vogliono partecipare in modo coordinato.</div></li>
        </ul>
        <p style="margin-top:12px">Gli incontri di presentazione alla cittadinanza li organizza il Comune,
           e le date vengono annunciate sui canali ufficiali. Per sapere quando parte il prossimo, o per
           chiedere i moduli e costituire un gruppo nella tua via, il riferimento &egrave; la Polizia
           Locale, qui a fianco.</p>
      </div>
      <div class="riquadro riquadro--nero">
        <h3><span aria-hidden="true">&#128110;</span> A chi chiedere informazioni</h3>
        <p><strong>Corpo del Distretto di Polizia Locale</strong><br>
           Porcia, Prata di Pordenone, Roveredo<br>
           <strong>Presidio di Roveredo in Piano</strong><br>
           Piazza Roma 8, Roveredo in Piano</p>
        <p>Telefono <a href="tel:+390434388670">0434 388670</a><br>
           polizia.municipale@comune.roveredo.pn.it</p>
        <div class="fila-bottoni">
          <button type="button" class="bottone bottone--giallo non-stampare"
            data-copia="polizia.municipale@comune.roveredo.pn.it"
            data-avviso-testo="Indirizzo della Polizia Locale copiato!">
            <span aria-hidden="true">&#10697;</span> Copia l'indirizzo</button>
          <a class="bottone bottone--bianco" href="contatti.html">Altri recapiti</a>
        </div>
      </div>
    </div>
  </div>
</section>
""" + RITORNO_SICUREZZA + """
</main>
"""

scrivi("controllo-di-vicinato.html", pagina(
    "controllo-di-vicinato.html",
    "Il controllo di vicinato | GinoPizza.it",
    "Il controllo di vicinato a Roveredo in Piano, con il protocollo d'intesa con la Prefettura di "
    "Pordenone: che cosa si segnala, come si costituisce un gruppo, i compiti del coordinatore. "
    "Nessuna ronda, nessun pattugliamento.",
    CORPO_VICINATO))


# ---------- 3.2 Il vademecum antitruffa ----------
CORPO_VADEMECUM = """
<main>
<header class="testata testata--gialla">
  <div class="contenitore">
    <span class="testata__occhiello">Sicurezza &middot; Ministero dell'Interno, Polizia Postale, Arma dei Carabinieri</span>
    <h1><span aria-hidden="true">&#128680;</span> Il vademecum<br>antitruffa</h1>
    <p class="testata__sommario">Le truffe non colpiscono per caso: seguono copioni collaudati, quasi sempre
       gli stessi. Chi li conosce li riconosce, e chi li riconosce non ci casca. Questa pagina raccoglie
       soltanto quello che scrivono le tre fonti ufficiali, ed &egrave; fatta per essere stampata tutta
       intera e appesa vicino al telefono.</p>
  </div>
</header>

""" + nastro("nastro--blu") + """

<section class="sezione">
  <div class="contenitore">
    <div class="fila-bottoni non-stampare" style="margin-top:0;margin-bottom:0">
      <button type="button" class="bottone bottone--blu" data-stampa>
        <span aria-hidden="true">&#128424;</span> Stampa tutto il vademecum</button>
      <a class="bottone bottone--bianco" href="tel:112">Chiama il 112</a>
    </div>
  </div>
</section>

<section class="sezione" style="padding-top:0">
  <div class="contenitore">
    <h2 class="sezione__titolo">Alla porta di casa</h2>
    <p class="sezione__sotto">Qui il truffatore si fa vedere: suona alla porta, oppure ti prepara con una telefonata. Quattro copioni, sempre gli stessi.</p>
    
  </div>
</section>
<section class="sezione">
  <div class="contenitore">

    <div class="allerta">
      <div class="allerta__cima">
        <span class="allerta__icona" aria-hidden="true">&#128680;</span>
        <h3>Allarme truffa: finto avvocato o finte forze dell'ordine</h3>
      </div>
      <p><strong>Come funziona.</strong> Una telefonata di un finto appartenente alle forze dell'ordine o di
         un finto avvocato fa credere che un parente sia rimasto coinvolto in un incidente stradale o che sia
         stato arrestato. Viene chiesta una somma di denaro per fornirgli assistenza sanitaria o legale. Se la
         persona accetta, l'interlocutore comunica che di l&igrave; a breve un assistente o un carabiniere in
         borghese passer&agrave; a ritirare il contante.</p>
      <div class="doppia-colonna">
        <div class="colonna-fare">
          <h4><span aria-hidden="true">&#9989;</span> Cosa fare subito</h4>
          <ul>
            <li>Prendi tempo. Non decidere mentre sei al telefono.</li>
            <li>Chiama il <strong>112</strong>.</li>
            <li>Telefona direttamente al parente, al numero che gi&agrave; conosci.</li>
          </ul>
        </div>
        <div class="colonna-mai">
          <h4><span aria-hidden="true">&#10060;</span> Cosa non fare mai</h4>
          <ul>
            <li>Non consegnare denaro a nessuno: <strong>le forze dell'ordine non chiedono mai denaro
                per assistere i cittadini</strong>.</li>
            <li>Non aprire la porta a sconosciuti.</li>
            <li>Non fidarti del solo tesserino di riconoscimento: non basta.</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="allerta">
      <div class="allerta__cima">
        <span class="allerta__icona" aria-hidden="true">&#128680;</span>
        <h3>Allarme truffa: finti tecnici del gas o dell'acqua, la truffa del congelatore</h3>
      </div>
      <p><strong>Come funziona.</strong> I truffatori, travestiti da tecnici dell'acqua o del gas, si
         presentano alla porta dicendo che in casa c'&egrave; un grave problema da risolvere subito.
         Sfruttando l'ansia, invitano la vittima a mettere al sicuro i beni preziosi in un sacchetto dentro
         il congelatore, che poi sottraggono.</p>
      <div class="doppia-colonna">
        <div class="colonna-fare">
          <h4><span aria-hidden="true">&#9989;</span> Cosa fare subito</h4>
          <ul>
            <li>Ricorda che le aziende di gas, luce, acqua e telefono <strong>annunciano sempre</strong>
                il loro arrivo con avvisi al condominio, molto tempo prima.</li>
            <li>Se hai gi&agrave; fatto entrare sconosciuti, non farti distrarre e, senza perdere la calma,
                invitali con decisione a uscire.</li>
            <li>Chiama il <strong>112</strong> se la persona &egrave; ancora nei paraggi.</li>
          </ul>
        </div>
        <div class="colonna-mai">
          <h4><span aria-hidden="true">&#10060;</span> Cosa non fare mai</h4>
          <ul>
            <li>Non mettere mai denaro o gioielli dove ti dice uno sconosciuto.</li>
            <li>Non pagare nulla a domicilio: <strong>nessun ente o societ&agrave; manda i propri dipendenti
                a casa a riscuotere pagamenti</strong>.</li>
            <li>Non lasciare mai una persona estranea sola in una stanza.</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="allerta">
      <div class="allerta__cima">
        <span class="allerta__icona" aria-hidden="true">&#128680;</span>
        <h3>Allarme truffa: finti rappresentanti di luce, acqua e gas</h3>
      </div>
      <p><strong>Come funziona.</strong> Il truffatore si presenta a casa spacciandosi per rappresentante di
         una compagnia di fornitura e annuncia nuove condizioni contrattuali pi&ugrave; vantaggiose. Con
         questo stratagemma raccoglie i dati della persona, poi usati per aprire contratti a suo nome senza
         il suo consenso.</p>
      <div class="doppia-colonna">
        <div class="colonna-fare">
          <h4><span aria-hidden="true">&#9989;</span> Cosa fare subito</h4>
          <ul>
            <li>Contatta la compagnia <strong>ai numeri stampati sulle bollette</strong>.</li>
            <li>Chiedi consiglio a una persona di fiducia pi&ugrave; esperta.</li>
            <li>Se il contratto &egrave; gi&agrave; stato attivato, invia un reclamo scritto al fornitore con
                raccomandata con avviso di ricevimento oppure con PEC (posta elettronica certificata).</li>
          </ul>
        </div>
        <div class="colonna-mai">
          <h4><span aria-hidden="true">&#10060;</span> Cosa non fare mai</h4>
          <ul>
            <li>Alla porta <strong>non firmare nulla</strong>.</li>
            <li>Non chiamare i numeri forniti dallo sconosciuto sull'uscio.</li>
            <li>Non consegnare bollette, documenti o codici cliente.</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="allerta">
      <div class="allerta__cima">
        <span class="allerta__icona" aria-hidden="true">&#128680;</span>
        <h3>Allarme truffa: il finto nipote</h3>
      </div>
      <p><strong>Come funziona.</strong> La telefonata comincia con una frase trabocchetto del tipo
         &laquo;indovina un po' chi parla&raquo; oppure &laquo;zia, ti ricordi di me&raquo;. Serve a farsi
         dire il nome di un parente. Fingendo di essere quella persona, il truffatore racconta di avere
         urgente bisogno di denaro e annuncia che passer&agrave; un amico a ritirarlo, oppure chiede un
         bonifico.</p>
      <div class="doppia-colonna">
        <div class="colonna-fare">
          <h4><span aria-hidden="true">&#9989;</span> Cosa fare subito</h4>
          <ul>
            <li>Riattacca e chiama quel parente al numero che gi&agrave; conosci.</li>
            <li>Chiama il <strong>112</strong>.</li>
            <li>Se un figlio scrive da un numero nuovo dicendo di avere il telefono rotto, verifica prima.</li>
          </ul>
        </div>
        <div class="colonna-mai">
          <h4><span aria-hidden="true">&#10060;</span> Cosa non fare mai</h4>
          <ul>
            <li>Non fare tu il nome per primo: &egrave; il truffatore a doverselo far dire.</li>
            <li>Non consegnare denaro a un &laquo;amico&raquo; mandato da qualcuno.</li>
            <li>Non fare bonifici sotto pressione.</li>
          </ul>
        </div>
      </div>
    </div>
    </div>
</section>
<section class="sezione sezione--scura" style="padding-bottom:0">
  <div class="contenitore">
    <h2 class="sezione__titolo" style="color:#facc15">Fuori casa, al telefono, allo sportello</h2>
    <p class="sezione__sotto">Per strada, in auto, davanti al bancomat, al telefono e in rete. Sei
       casistiche, con il segnale che smaschera ciascuna.</p>
  </div>
</section>
<section class="sezione sezione--scura" style="padding-top:24px">
  <div class="contenitore">

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#128680;</span> Truffa del falso amico</h3>
        <p>Ti abbraccia per strada fingendo di conoscerti, di solito come amico dei figli o dei nipoti, e ti
           trattiene in una lunga conversazione per distrarti. Poi racconta di un debito e chiede contante
           o gioielli.</p>
        <p><strong>Il segnale:</strong> l'abbraccio arriva <em>prima</em> del riconoscimento. Quando esci non
           portare grosse somme con te e, quando paghi al bar, non mostrare denaro o oggetti di valore.
           Cammina in zone illuminate e frequentate.</p>
      </div>
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#128680;</span> Truffa dello specchietto</h3>
        <p>Senti un colpo secco sulla fiancata, provocato in realt&agrave; con un sasso o un bastone. Ti
           chiedono di risolvere subito in contanti per evitare l'assicurazione, anche con toni aggressivi.</p>
        <p><strong>Cosa fare:</strong> resta in auto senza scendere, chiudi i finestrini posteriori e quello
           lato passeggero per evitare che eventuali complici prendano i tuoi oggetti, e pretendi da subito
           di chiamare la Polizia Locale o il <strong>112</strong>.</p>
      </div>
      <div class="riquadro">
        <h3><span aria-hidden="true">&#128680;</span> Truffa del bancomat</h3>
        <p>Lo sportello viene alterato con un lettore abusivo, una microtelecamera o una finta tastiera, per
           clonare la carta e memorizzare il codice PIN (numero di identificazione personale, il codice
           segreto della carta). I malfattori sono appostati nei dintorni, in contatto visivo.</p>
        <p><strong>Ispeziona prima di usarlo:</strong> microtelecamere sopra o accanto alla tastiera; la
           fessura della tessera che si muove o si stacca; la tastiera non ben fissa, con un gradino di un
           paio di millimetri. Nel dubbio non inserire la tessera, allontanati e chiama le forze dell'ordine.
           Copri sempre il tastierino con il palmo mentre digiti.</p>
      </div>
      <div class="riquadro">
        <h3><span aria-hidden="true">&#128680;</span> Banconote bloccate</h3>
        <p>Al momento del prelievo alcune banconote restano incastrate nell'erogatore. Non &egrave; un guasto:
           il truffatore ha inserito un oggetto metallico e torner&agrave; a prenderle appena ti sarai
           allontanato.</p>
        <p><strong>Cosa fare:</strong> <strong>resta davanti allo sportello</strong> e contatta subito il
           servizio clienti della banca oppure il <strong>112</strong>.</p>
      </div>
      <div class="riquadro">
        <h3><span aria-hidden="true">&#128680;</span> Truffa del centro assistenza</h3>
        <p>Ti telefonano fingendo di essere un centro di assistenza e fanno domande banali costruite per
           farti rispondere &laquo;s&igrave;&raquo;. Quel &laquo;s&igrave;&raquo; viene estratto dalla
           registrazione e usato come assenso per attivare un contratto mai voluto. Te ne accorgi alla prima
           bolletta.</p>
        <p><strong>Il segnale:</strong> chi chiama non si fa identificare con chiarezza e insiste con domande
           che chiedono solo una conferma. Fai domande tu ed evita di fornire dati personali. Ricorda che il
           numero che compare sullo schermo pu&ograve; essere falsificato.</p>
      </div>
      <div class="riquadro">
        <h3><span aria-hidden="true">&#128680;</span> Raggiri sentimentali in rete</h3>
        <p>Un profilo falso, foto rubate dalla rete, una presenza costante e premurosa, false affinit&agrave;
           e progetti di vita. Poi arrivano le richieste di denaro per motivi di salute, viaggi o questioni
           legali. Ottenuta la prima somma, le richieste continuano, fino a somme molto ingenti.</p>
        <p><strong>Il segnale:</strong> non si fa mai incontrare di persona. Cerca nome e immagini del profilo
           su un motore di ricerca e verifica se ci sono gi&agrave; segnalazioni di altri. Se &egrave;
           successo: denuncia e smetti di pagare qualsiasi somma.</p>
      </div>
    </div>

    <div class="riquadro riquadro--nero">
      <h3><span aria-hidden="true">&#128179;</span> Per chi ha un negozio</h3>
      <p>Il terminale POS (il punto vendita, cio&egrave; l'apparecchio che accetta i pagamenti con carta)
         pu&ograve; essere manomesso per catturare i dati delle carte dei clienti, anche approfittando di
         furti o intrusioni notturne.</p>
      <p><strong>Cosa fare:</strong> controllare l'apparecchio con frequenza e, dopo un furto o
         un'intrusione, farlo verificare da personale specializzato. Per i pagamenti con carta di credito,
         verificare il documento di identit&agrave; del cliente.</p>
    </div>
  </div>
</section>
<section class="sezione">
  <div class="contenitore">

    <div class="riquadro riquadro--giallo">
      <h3>Nove segnali che valgono per tutte</h3>
      <ul class="elenco-timbri">
        <li><span class="icona" aria-hidden="true">&#9203;</span><div><strong>L'urgenza.</strong>
          Chi ha troppa fretta di concludere non merita fiducia.</div></li>
        <li><span class="icona" aria-hidden="true">&#128181;</span><div><strong>La richiesta di contante.</strong>
          Nessun ente manda dipendenti a domicilio a riscuotere, e le forze dell'ordine non chiedono mai
          denaro per assistere i cittadini.</div></li>
        <li><span class="icona" aria-hidden="true">&#127890;</span><div><strong>Il solo tesserino.</strong>
          Alla porta di casa non &egrave; una prova di identit&agrave;.</div></li>
        <li><span class="icona" aria-hidden="true">&#128273;</span><div><strong>La richiesta di dati o
          credenziali.</strong> Non si risponde mai a messaggi, chiamate o posta elettronica che chiedono
          dati personali, codici di sicurezza o dati delle carte di pagamento.</div></li>
        <li><span class="icona" aria-hidden="true">&#127991;</span><div><strong>Il prezzo troppo
          conveniente.</strong> Quando &egrave; troppo lontano dal mercato, non &egrave; un affare.</div></li>
        <li><span class="icona" aria-hidden="true">&#128279;</span><div><strong>Il collegamento da
          toccare.</strong> L'indirizzo a cui rimanda differisce sempre, anche se di poco, da quello
          originale.</div></li>
        <li><span class="icona" aria-hidden="true">&#128260;</span><div><strong>L'invito a uscire dalla
          piattaforma.</strong> Chi chiede di essere contattato altrove va messo in dubbio.</div></li>
        <li><span class="icona" aria-hidden="true">&#128683;</span><div><strong>Il pagamento non
          tracciabile.</strong> Le carte prepagate danno al truffatore disponibilit&agrave; immediata della
          somma: si usano solo metodi tracciabili.</div></li>
        <li><span class="icona" aria-hidden="true">&#128176;</span><div><strong>L'anticipo chiesto a chi deve
          ricevere.</strong> Non si anticipa mai denaro quando sei tu a doverlo incassare.</div></li>
      </ul>
    </div>
  </div>
</section>
<section class="sezione sezione--scura">
  <div class="contenitore">
    <h2 class="sezione__titolo" style="color:#facc15">Se la truffa &egrave; gi&agrave; avvenuta</h2>
    <p class="sezione__sotto">Le prime ore contano. Queste sono le azioni indicate dalle fonti ufficiali,
       nell'ordine in cui vanno fatte.</p>
    <div class="riquadro">
      <ol class="elenco-numerato">
        <li><strong>Blocca gli strumenti di pagamento.</strong> Contatta subito il tuo istituto bancario.</li>
        <li><strong>Cambia le parole di accesso</strong> e attiva la verifica in due passaggi.</li>
        <li><strong>Conserva le prove.</strong> Ricevute di pagamento e immagini delle conversazioni:
            servono alla denuncia.</li>
        <li><strong>Non versare altro denaro.</strong> Nei raggiri sentimentali la Polizia Postale &egrave;
            netta: denunciare, astenendosi dal pagare qualsiasi somma.</li>
        <li><strong>Controlla i movimenti del conto</strong> e segnala alla societ&agrave; emittente ogni
            operazione sconosciuta.</li>
        <li><strong>Segnala alla Polizia Postale</strong> su
            <a href="https://www.commissariatodips.it" target="_blank" rel="noopener">commissariatodips.it</a>.</li>
        <li><strong>Chiama il 112</strong> e presenta denuncia. Senza vergogna e senza aspettare.</li>
        <li><strong>Chiedi un parere a una persona di fiducia.</strong> Le fonti lo raccomandano
            espressamente, sia prima sia dopo.</li>
      </ol>
    </div>
    <div class="riquadro riquadro--giallo">
      <h3>Non c'&egrave; nulla di cui vergognarsi</h3>
      <p>Molte vittime aspettano troppo perch&eacute; si vergognano. Il senso di colpa &egrave; il secondo
         danno, e spesso pesa pi&ugrave; del primo. Non &egrave; colpa di chi subisce: i truffatori sfruttano
         apposta la sensibilit&agrave; e la fragilit&agrave; delle persone. <strong>Ogni giorno di silenzio
         &egrave; un giorno regalato al truffatore.</strong></p>
    </div>
  </div>
</section>
<section class="sezione">
  <div class="contenitore">
    <div class="emergenza">
      <span style="font-family:Oswald,Impact,sans-serif;letter-spacing:.14em;font-size:.9rem">
        Numero unico di emergenza</span>
      <span class="emergenza__numero">112</span>
      <p>Chiamalo quando il truffatore &egrave; alla porta o nei paraggi, quando hai un dubbio su chi ti sta
         contattando, quando le banconote restano bloccate allo sportello automatico e in ogni caso
         di necessit&agrave;.</p>
      <div class="fila-bottoni non-stampare" style="justify-content:center">
        <a class="bottone bottone--giallo" href="tel:112">Chiama il 112</a>
      </div>
    </div>

    <div class="tabella-guscio">
      <table>
        <thead><tr><th scope="col">Recapito</th><th scope="col">A che cosa serve</th></tr></thead>
        <tbody>
          <tr><td><strong>112</strong></td><td>Numero unico di emergenza.</td></tr>
          <tr><td><strong>114</strong></td>
              <td>Emergenza infanzia, attivo 24 ore su 24 tutti i giorni, gratuito, da telefono fisso e
                  mobile. Sito: www.114.it</td></tr>
          <tr><td><strong>commissariatodips.it</strong></td>
              <td>Commissariato di pubblica sicurezza in rete della Polizia Postale: da qui chiunque
                  pu&ograve; inviare segnalazioni.</td></tr>
          <tr><td><strong>800 151616</strong></td><td>Servizi interbancari, blocco carta.</td></tr>
          <tr><td><strong>06 72900347</strong></td><td>American Express Italia, blocco carta.</td></tr>
          <tr><td><strong>800 26392279</strong></td><td>American Express dall'estero, blocco carta.</td></tr>
          <tr><td><strong>800 900910</strong></td><td>Top Card, blocco carta.</td></tr>
          <tr><td><strong>800 864064</strong></td><td>Diner's, blocco carta.</td></tr>
          <tr><td><strong>800 822056</strong></td><td>Agos Itafinco, blocco carta.</td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size:.92rem">Per ogni altra carta e per il conto corrente si chiama il numero del proprio
       istituto bancario. Per le forniture di acqua, luce e gas si usano soltanto i numeri stampati sulle
       bollette.</p>

    <div class="riquadro riquadro--nero">
      <h3>Le tre fonti ufficiali</h3>
      <ul class="elenco-timbri">
        <li><span class="icona" aria-hidden="true">&#127963;</span><div><strong>Ministero dell'Interno.</strong>
          Difendersi dalle trappole del commercio elettronico.<br>
          <a href="https://www.interno.gov.it/it/notizie/difendersi-dalle-trappole-commerce"
             target="_blank" rel="noopener">interno.gov.it</a></div></li>
        <li><span class="icona" aria-hidden="true">&#128421;</span><div><strong>Polizia Postale e delle
          Comunicazioni.</strong> Commissariato di pubblica sicurezza in rete, sezione Consigli.<br>
          <a href="https://www.commissariatodips.it/consigli/index.html"
             target="_blank" rel="noopener">commissariatodips.it</a></div></li>
        <li><span class="icona" aria-hidden="true">&#128737;</span><div><strong>Arma dei Carabinieri.</strong>
          Pillole di prevenzione, contro le truffe.<br>
          <a href="https://www.carabinieri.it/in-vostro-aiuto/consigli/pillole-di-prevenzione/contro-le-truffe"
             target="_blank" rel="noopener">carabinieri.it</a></div></li>
      </ul>
      <p><a href="https://costalonga.org/truffe/" target="_blank" rel="noopener">Il vademecum completo in
         24 punti su costalonga.org &rarr;</a></p>
    </div>
  </div>
</section>
""" + RITORNO_SICUREZZA + """
</main>
"""

scrivi("vademecum-antitruffa.html", pagina(
    "vademecum-antitruffa.html",
    "Il vademecum antitruffa | GinoPizza.it",
    "Tutte le truffe in una pagina: alla porta di casa, per strada, in auto, allo sportello, al telefono e "
    "in rete. I segnali di allarme, cosa fare se \u00e8 gi\u00e0 successo, il 112 e i numeri per bloccare "
    "la carta. Da stampare.",
    CORPO_VADEMECUM))


# ============================================================
# 4. Viabilità: indice e schede
# ============================================================
RITORNO_VIABILITA = ritorno("viabilita.html", "Torna alla viabilità")

CORPO_VIABILITA = """
<main>
<header class="testata">
  <div class="contenitore">
    <span class="testata__occhiello">Delega viabilit&agrave;</span>
    <h1><span aria-hidden="true">&#128663;</span> Viabilit&agrave;</h1>
    <p class="testata__sommario">Due provvedimenti che vanno nella stessa direzione: restituire la strada
       a chi ci cammina, ci abita e ci porta i figli. Uno d&agrave; un posto a chi ne ha bisogno, l'altro
       toglie spazio a chi corre dove non si corre.</p>
  </div>
</header>

""" + nastro("nastro--giallo") + """

<section class="sezione sezione--scura">
  <div class="contenitore">
    <h2 class="sezione__titolo" style="color:#facc15">Che cosa c'&egrave; dentro</h2>
    <p class="sezione__sotto">Due schede, due collegamenti distinti. Quella sul permesso rosa si
       pu&ograve; mandare da sola a chi sta per diventare genitore.</p>
    <div class="griglia griglia--2">
""" + scheda("permesso-rosa.html", "01", "Regolamento comunale", "&#128118;",
             "Il permesso rosa",
             "Gli stalli riservati alle donne in gravidanza e ai genitori con un bambino fino a due anni. "
             "Chi lo chiede, che cosa serve, quanto dura la sosta.",
             ("Requisiti, documenti e marche da bollo",
              "Tre ore con disco orario, dalle 8 alle 20",
              "Le sanzioni dell'articolo 188 bis")) \
  + scheda("controlli-velocita.html", "02", "Comunicato del 10 agosto 2026", "&#9889;",
           "I controlli di velocit&agrave;",
           "I rilevatori sono tornati in funzione. Postazioni segnalate e non nascoste, calendario reso "
           "noto in anticipo, apparecchi omologati e tarati.",
           ("Perch&eacute; erano fermi e perch&eacute; ripartono",
            "Come e quando si controlla",
            "Le parole dell'assessore e del comandante")) + """    </div>
  </div>
</section>

<section class="sezione">
  <div class="contenitore">
    <div class="riquadro riquadro--blu">
      <h3><span aria-hidden="true">&#9888;</span> Il filo che le tiene insieme</h3>
      <p>Uno stallo rosa occupato da chi non ne ha diritto &egrave; un posto tolto a una donna incinta o a
         un genitore con un neonato in braccio. Un'auto che corre in mezzo alle case &egrave; un rischio
         per chi attraversa. In tutti e due i casi la strada viene tolta a qualcuno, e in tutti e due i casi
         si controlla e si sanziona. <strong>Senza eccezioni, nemmeno per gli amministratori.</strong></p>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--nero">
        <h3>Segnala un punto dove si corre</h3>
        <p>Indica la via, il tratto e l'orario in cui il problema si presenta. Le segnalazioni dei residenti
           servono a scegliere dove mettere le postazioni: sono il dato pi&ugrave; utile che c'&egrave;, e
           sono proprio quelle che hanno portato a questa decisione.</p>
        <div class="fila-bottoni">
          <a class="bottone bottone--giallo" href="https://wa.me/393283692227" target="_blank" rel="noopener">
            Segnala su WhatsApp</a>
        </div>
      </div>
      <div class="riquadro">
        <h3>Dove si chiede il permesso rosa</h3>
        <p>Presidio di Roveredo in Piano del Corpo del Distretto di Polizia Locale, Piazza Roma 8,
           telefono 0434 388670. Il modulo si scarica anche dal sito del Comune.</p>
        <div class="fila-bottoni">
          <a class="bottone bottone--blu" href="contatti.html">Recapiti completi</a>
          <a class="bottone bottone--bianco" href="https://comune.roveredoinpiano.pn.it/"
             target="_blank" rel="noopener">Sito del Comune</a>
        </div>
      </div>
    </div>
  </div>
</section>
</main>
"""

scrivi("viabilita.html", pagina(
    "viabilita.html",
    "Viabilità | GinoPizza.it",
    "Permesso rosa e controlli di velocità a Roveredo in Piano: gli stalli riservati a chi ne ha diritto e "
    "i rilevatori tornati in funzione, segnalati e non nascosti.",
    CORPO_VIABILITA))


# ---------- 4.1 Il permesso rosa ----------
CORPO_ROSA = """
<main>
<header class="testata testata--gialla">
  <div class="contenitore">
    <span class="testata__occhiello">Viabilit&agrave; &middot; Regolamento comunale</span>
    <h1><span aria-hidden="true">&#128118;</span> Il permesso<br>rosa</h1>
    <p class="testata__sommario">Uno stallo rosa non &egrave; una cortesia: &egrave; una misura di
       sicurezza. Scendere dall'auto con un seggiolino, una borsa e un bambino di un anno, in un parcheggio
       stretto e trafficato, &egrave; un rischio concreto.</p>
  </div>
</header>

""" + nastro("nastro--blu") + """

<section class="sezione">
  <div class="contenitore">
    <div class="griglia griglia--2">
      <div class="riquadro riquadro--giallo">
        <h3>Chi pu&ograve; chiederlo</h3>
        <p>Servono tutti e due i requisiti: la residenza e la condizione.</p>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#127968;</span>
            <div><strong>Residenza nel Comune di Roveredo in Piano.</strong></div></li>
          <li><span class="icona" aria-hidden="true">&#129328;</span>
            <div><strong>Donne in stato di gravidanza</strong>, con certificato medico in carta libera
            rilasciato da professionisti sanitari, pubblici o privati, per esempio il consultorio o lo
            specialista ginecologo.</div></li>
          <li><span class="icona" aria-hidden="true">&#128118;</span>
            <div><strong>Genitori residenti con un bambino di et&agrave; non superiore a due anni.</strong>
            Sono equiparati i genitori affidatari e adottivi.</div></li>
        </ul>
        <p style="margin-top:12px"><strong>Un solo contrassegno per ogni nascita</strong>, anche in caso
           di parto gemellare o plurigemellare.</p>
      </div>
      <div class="riquadro riquadro--nero">
        <h3>Che cosa portare</h3>
        <p>Modulo <strong>Allegato A</strong>, da ritirare allo sportello della Polizia Locale oppure da
           scaricare dal sito del Comune, compilato in ogni sua parte e sottoscritto, pena la non
           ammissibilit&agrave; della domanda.</p>
        <div class="tabella-guscio tabella-guscio--stretta" style="box-shadow:none;border:none;margin-bottom:0">
        <table>
          <thead><tr><th scope="col">Gestanti</th><th scope="col">Genitori</th></tr></thead>
          <tbody>
            <tr>
              <td>Certificato medico con lo stato di gravidanza e la data presunta del parto</td>
              <td>Certificato di nascita o dichiarazione sostitutiva ai sensi del d.P.R. 445 del 2000</td>
            </tr>
            <tr>
              <td>Documento di riconoscimento in corso di validit&agrave;</td>
              <td>Documento di riconoscimento in corso di validit&agrave;</td>
            </tr>
            <tr>
              <td><strong>Due marche da bollo da 16 euro</strong></td>
              <td><strong>Due marche da bollo da 16 euro</strong></td>
            </tr>
          </tbody>
        </table>
        </div>
      </div>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro">
        <h3><span aria-hidden="true">&#128228;</span> Dove si consegna</h3>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128110;</span>
            <div>Allo sportello dell'Ufficio di Polizia Locale, <strong>su appuntamento</strong>.</div></li>
          <li><span class="icona" aria-hidden="true">&#128203;</span>
            <div>All'Ufficio Protocollo del Comune.</div></li>
          <li><span class="icona" aria-hidden="true">&#9993;</span>
            <div>Per posta elettronica certificata a
            <strong>comune.roveredoinpiano@certgov.fvg.it</strong>.</div></li>
        </ul>
        <p style="margin-top:12px">Pu&ograve; presentarla l'interessato o una persona delegata.
           <strong>Il ritiro del permesso avviene alla sede della Polizia Locale</strong>, di persona o
           tramite delegato.</p>
      </div>
      <div class="riquadro riquadro--blu">
        <h3><span aria-hidden="true">&#9200;</span> Come si usa</h3>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128274;</span>
            <div><strong>&Egrave; personale e non cedibile.</strong> Non &egrave; legato a un veicolo
            preciso, ma la persona avente titolo deve essere <strong>a bordo</strong>: la donna in
            gravidanza, oppure un genitore insieme al bambino.</div></li>
          <li><span class="icona" aria-hidden="true">&#128196;</span>
            <div><strong>Va esposto in originale sul cruscotto</strong>, con in vista il lato che riporta
            numero e scadenza. Fotocopie e riproduzioni non valgono.</div></li>
          <li><span class="icona" aria-hidden="true">&#128336;</span>
            <div><strong>Massimo tre ore consecutive, dalle 8.00 alle 20.00</strong>, feriali e festivi,
            con l'orario di inizio segnalato dal disco orario. Serve a garantire la rotazione fra tutti
            gli aventi diritto.</div></li>
          <li><span class="icona" aria-hidden="true">&#10060;</span>
            <div><strong>Non vale per gli stalli riservati alle persone con disabilit&agrave;</strong> e
            non d&agrave; diritto alla sosta gratuita sulle strisce blu: l'agevolazione riguarda solo gli
            stalli rosa.</div></li>
          <li><span class="icona" aria-hidden="true">&#128205;</span>
            <div><strong>Vale su tutto il territorio comunale.</strong> A Roveredo sono accettati anche i
            permessi rosa rilasciati da altri Comuni; per usare il nostro altrove, si consulta il
            regolamento del Comune di destinazione.</div></li>
        </ul>
      </div>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#128197;</span> Quando scade</h3>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#129328;</span>
            <div>Chiesto in gravidanza: <strong>il trentesimo giorno dopo la data presunta del
            parto</strong>. Nato il bambino, si pu&ograve; chiedere un nuovo permesso valido fino ai due
            anni.</div></li>
          <li><span class="icona" aria-hidden="true">&#128118;</span>
            <div>Chiesto da genitore: <strong>il giorno in cui il figlio compie due anni</strong>.</div></li>
          <li><span class="icona" aria-hidden="true">&#128230;</span>
            <div>Se si trasferisce la residenza in un altro Comune, o se vengono meno i requisiti, il
            permesso va restituito <strong>entro trenta giorni</strong> all'ufficio che lo ha
            emesso.</div></li>
          <li><span class="icona" aria-hidden="true">&#128269;</span>
            <div>In caso di deterioramento, smarrimento o furto si chiede un duplicato con il modello
            <strong>Allegato B</strong>, allegando la denuncia: nuova numerazione, stessa scadenza.</div></li>
        </ul>
      </div>
      <div class="riquadro riquadro--nero">
        <h3><span aria-hidden="true">&#9878;</span> Le sanzioni</h3>
        <p><strong>Articolo 188 bis del Codice della Strada</strong>, decreto legislativo 30 aprile 1992,
           n. 285, introdotto dal decreto legge 10 settembre 2021, n. 121, convertito con modificazioni
           dalla legge 9 novembre 2021, n. 156.</p>
        <p>Chi usa gli stalli <strong>senza l'autorizzazione prescritta, o ne fa uso improprio</strong>:
           sanzione amministrativa <strong>da 87 euro a 344 euro</strong> (comma 3).</p>
        <p>Chi, <strong>pur avendone diritto</strong>, non osserva le condizioni e i limiti indicati
           nell'autorizzazione: <strong>da 42 euro a 173 euro</strong> (comma 4).</p>
        <p style="font-size:.88rem">Controllano gli organi di polizia stradale dell'articolo 12 del Codice
           della Strada. Testo letto su Normattiva il 14 settembre 2026.<br>
          <a href="https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:1992-04-30;285"
             target="_blank" rel="noopener">Codice della Strada su Normattiva</a></p>
      </div>
    </div>

    <div class="riquadro">
      <h3>Dove sono gli stalli</h3>
      <p>Gli stalli rosa sono individuati da provvedimenti di viabilit&agrave; e da deliberazioni di Giunta,
         e si riconoscono dalla segnaletica orizzontale e verticale dedicata. L'elenco aggiornato e il testo
         integrale del regolamento stanno sul sito del Comune.</p>
      <div class="fila-bottoni">
        <a class="bottone bottone--blu" href="https://comune.roveredoinpiano.pn.it/"
           target="_blank" rel="noopener">Sito del Comune</a>
      </div>
    </div>
  </div>
</section>
""" + RITORNO_VIABILITA + """
</main>
"""

scrivi("permesso-rosa.html", pagina(
    "permesso-rosa.html",
    "Il permesso rosa | GinoPizza.it",
    "Permesso rosa a Roveredo in Piano: chi può chiederlo, documenti e marche da bollo, dove si consegna e "
    "si ritira, limite di tre ore con disco orario, scadenze e sanzioni dell'articolo 188 bis.",
    CORPO_ROSA))


# ---------- 4.2 I controlli di velocità ----------
CORPO_VELOCITA = """
<main>
<header class="testata testata--nera">
  <div class="contenitore">
    <span class="testata__occhiello">Viabilit&agrave; &middot; Comunicato del 10 agosto 2026</span>
    <h1><span aria-hidden="true">&#9889;</span> I controlli<br>di velocit&agrave;</h1>
    <p class="testata__sommario">Piede pi&ugrave; leggero sull'acceleratore. &Egrave; questo, ridotto
       all'osso, quello che il Comune chiede a chi guida lungo le strade che tagliano il paese, dove il
       traffico di passaggio tende a correre pi&ugrave; del dovuto. Non un'operazione lampo: un presidio
       destinato a durare.</p>
  </div>
</header>

""" + nastro("nastro--giallo") + """

<section class="sezione">
  <div class="contenitore">
    <div class="griglia griglia--2">
      <div class="riquadro">
        <h3><span aria-hidden="true">&#128260;</span> Perch&eacute; si riprende solo adesso</h3>
        <p>Una sentenza aveva stabilito che gli apparecchi privi di regolare omologazione non potessero
           essere usati per elevare sanzioni. Questo aveva di fatto congelato i controlli un po' ovunque,
           non soltanto qui.</p>
        <p>Il nodo si &egrave; sciolto grazie all'intervento normativo del governo nazionale, che ha aperto
           la strada alla regolarizzazione degli strumenti. Una volta messi in regola i rilevatori, il
           Comune ha potuto rimetterli in funzione <strong>su basi solide, al riparo da
           contestazioni</strong>.</p>
      </div>
      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#128681;</span> Come funzionano i controlli</h3>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128197;</span>
            <div><strong>Calendario concordato con la Polizia Locale e reso noto in anticipo.</strong>
            Senza trappole.</div></li>
          <li><span class="icona" aria-hidden="true">&#128065;</span>
            <div><strong>Postazioni segnalate, non nascoste.</strong></div></li>
          <li><span class="icona" aria-hidden="true">&#128295;</span>
            <div><strong>Apparecchi omologati e tarati periodicamente</strong>, come prevede la
            normativa.</div></li>
          <li><span class="icona" aria-hidden="true">&#128336;</span>
            <div>Attenzione soprattutto sulle <strong>ore di punta</strong>: la mattina all'uscita di casa
            e nel tardo pomeriggio, senza escludere verifiche in altri momenti della giornata.</div></li>
          <li><span class="icona" aria-hidden="true">&#128226;</span>
            <div>Nelle prime settimane <strong>l'attenzione sar&agrave; soprattutto sul richiamo</strong>,
            perch&eacute; chi guida si abitui a tenere il piede leggero gi&agrave; prima di vedere la
            pattuglia.</div></li>
        </ul>
      </div>
    </div>

    <div class="griglia griglia--2">
      <div class="riquadro riquadro--blu">
        <h3>L'assessore</h3>
        <p>&laquo;Abbiamo aspettato che ci fossero le condizioni giuridiche per farlo bene, e ora ci sono.
           Non ci interessa fare cassa, ci interessa che i limiti vengano rispettati. Sulle vie principali si
           va troppo forte, e l&igrave; passano pedoni, ciclisti e ragazzini.
           <strong>Un rilevatore che convince un automobilista a togliere il piede vale pi&ugrave; di cento
           verbali.</strong>&raquo;</p>
        <p>&laquo;La sicurezza di chi attraversa la strada ogni giorno viene prima di ogni altra
           considerazione. Se serve a far rallentare, un rilevatore in pi&ugrave; &egrave; un rischio in
           meno.&raquo;</p>
        <p style="font-size:.9rem"><strong>Guido Costalonga</strong>, assessore alla Sicurezza.</p>
      </div>
      <div class="riquadro riquadro--nero">
        <h3>Il comandante della Polizia Locale</h3>
        <p>&laquo;<strong>Chi rispetta i limiti non se ne accorger&agrave; nemmeno.</strong>&raquo;</p>
        <p>Lo scopo dichiarato resta la deterrenza: far rallentare prima, non sanzionare dopo.</p>
        <p style="font-size:.9rem"><strong>Cristiano Ciletti</strong>, comandante della Polizia Locale.</p>
      </div>
    </div>

    <div class="riquadro riquadro--giallo">
      <h3>La regola, in una riga</h3>
      <p style="font-family:Oswald,Impact,sans-serif;text-transform:uppercase;font-size:1.5rem;line-height:1.2">
        Rispetti il limite, non paghi niente.<br>Corri in mezzo alle case, paghi.</p>
      <p>Non c'&egrave; una terza possibilit&agrave;. I limiti sono quelli dell'articolo 142 del Codice
         della Strada. Se a fine anno le multe saranno poche perch&eacute; la gente ha imparato ad andare
         piano, sar&agrave; il risultato migliore possibile.</p>
      <p style="font-size:.9rem">Il calendario dei controlli e i tratti interessati vengono resi noti in
         anticipo dal Comune: &egrave; una scelta, non un obbligo da aggirare.</p>
    </div>

    <div class="riquadro riquadro--nero">
      <h3>Segnala un punto dove si corre</h3>
      <p>Le segnalazioni dei residenti arrivano da tempo, e sono proprio quelle che hanno portato a questa
         decisione. Indica la via, il tratto e l'orario in cui il problema si presenta.</p>
      <div class="fila-bottoni">
        <a class="bottone bottone--giallo" href="https://wa.me/393283692227" target="_blank" rel="noopener">
          Segnala su WhatsApp</a>
      </div>
    </div>
  </div>
</section>
""" + RITORNO_VIABILITA + """
</main>
"""

scrivi("controlli-velocita.html", pagina(
    "controlli-velocita.html",
    "I controlli di velocità | GinoPizza.it",
    "I rilevatori di velocità di Roveredo in Piano sono tornati in funzione: perché erano fermi, come "
    "funzionano i controlli, postazioni segnalate e calendario reso noto in anticipo.",
    CORPO_VELOCITA))


# ============================================================
# 5. contatti.html
# ============================================================
CORPO_CONTATTI = """
<main>
<header class="testata testata--gialla">
  <div class="contenitore">
    <span class="testata__occhiello">Ricevimento &middot; Protocollo &middot; Recapiti</span>
    <h1><span aria-hidden="true">&#9993;</span> Ricevimento<br>e contatti</h1>
    <p class="testata__sommario">Nessun filtro, nessuna anticamera inutile. Qui ci sono i recapiti veri del
       municipio, il modo per prendere appuntamento e il numero personale su cui arrivano le segnalazioni.
       Si legge tutto.</p>
  </div>
</header>

""" + nastro("nastro--blu") + """

<section class="sezione">
  <div class="contenitore">
    <div class="griglia griglia--2">

      <div class="riquadro riquadro--nero">
        <h3><span aria-hidden="true">&#127963;</span> Il municipio</h3>
        <div class="tabella-guscio tabella-guscio--stretta" style="box-shadow:none;border:none;margin-bottom:0">
        <table>
          <tbody>
            <tr><td><strong>Ente</strong></td><td>Comune di Roveredo in Piano</td></tr>
            <tr><td><strong>Indirizzo</strong></td><td>Via G. Carducci, 11<br>33080 Roveredo in Piano (PN)</td></tr>
            <tr><td><strong>Telefono</strong></td><td><a href="tel:+390434388611">0434 388611</a></td></tr>
            <tr><td><strong>Fax</strong></td><td>0434 94207</td></tr>
            <tr><td><strong>PEC</strong></td>
                <td>comune.roveredoinpiano@certgov.fvg.it<br>
                <button type="button" class="bottone bottone--blu non-stampare" style="margin-top:8px;font-size:.8rem;padding:8px 12px"
                  data-copia="comune.roveredoinpiano@certgov.fvg.it"
                  data-avviso-testo="Indirizzo PEC copiato negli appunti!">
                  <span aria-hidden="true">&#10697;</span> Copia la PEC</button></td></tr>
            <tr><td><strong>Codice fiscale</strong></td><td>80000890931</td></tr>
            <tr><td><strong>Partita IVA</strong></td><td>00194640934</td></tr>
          </tbody>
        </table>
        </div>
        <p style="font-size:.86rem;margin-top:12px">Dati letti sul sito istituzionale del Comune di Roveredo
          in Piano il 14 settembre 2026.</p>
      </div>

      <div class="riquadro riquadro--blu">
        <h3><span aria-hidden="true">&#128197;</span> Appuntamento in municipio</h3>
        <p>Il ricevimento avviene su appuntamento, cos&igrave; chi arriva trova qualcuno che ha il tempo di
           ascoltarlo davvero e non cinque minuti fra una riunione e l'altra.</p>
        <p><strong>Due modi per fissarlo:</strong></p>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128222;</span>
            <div><strong>Centralino del municipio.</strong> Telefono 0434 388611, negli orari di apertura
            degli uffici.</div></li>
          <li><span class="icona" aria-hidden="true">&#128172;</span>
            <div><strong>Messaggio diretto.</strong> Scrivi su WhatsApp al numero qui sotto e si trova
            la data.</div></li>
        </ul>
        <p style="margin-top:14px">Non c'&egrave; un giorno fisso di ricevimento: si concorda di volta in
           volta, cos&igrave; l'orario si adatta a chi lavora e non il contrario. Scrivi e si trova
           il momento.</p>
      </div>

      <div class="riquadro riquadro--blu">
        <h3><span aria-hidden="true">&#128110;</span> La Polizia Locale</h3>
        <p>&Egrave; il presidio quotidiano del territorio. Qui si chiedono i moduli del controllo di
           vicinato, il permesso rosa e le informazioni sul regolamento di polizia rurale.</p>
        <div class="tabella-guscio tabella-guscio--stretta" style="box-shadow:none;border:none;margin-bottom:0">
        <table>
          <tbody>
            <tr><td><strong>Corpo</strong></td>
                <td>Corpo del Distretto di Polizia Locale<br>Porcia, Prata di Pordenone, Roveredo</td></tr>
            <tr><td><strong>Presidio</strong></td>
                <td>Roveredo in Piano<br>Piazza Roma 8</td></tr>
            <tr><td><strong>Telefono</strong></td>
                <td><a href="tel:+390434388670">0434 388670</a></td></tr>
            <tr><td><strong>Posta</strong></td>
                <td>polizia.municipale@comune.roveredo.pn.it<br>
                <button type="button" class="bottone bottone--giallo non-stampare" style="margin-top:8px;font-size:.8rem;padding:8px 12px"
                  data-copia="polizia.municipale@comune.roveredo.pn.it"
                  data-avviso-testo="Indirizzo della Polizia Locale copiato!">
                  <span aria-hidden="true">&#10697;</span> Copia l'indirizzo</button></td></tr>
          </tbody>
        </table>
        </div>
        <p style="font-size:.86rem;margin-top:12px">Lo sportello riceve <strong>su appuntamento</strong>:
          orari e modalit&agrave; aggiornati sono sul sito del Comune.</p>
      </div>

      <div class="riquadro riquadro--giallo">
        <h3><span aria-hidden="true">&#128172;</span> Contatto diretto</h3>
        <p>Per le segnalazioni: un fosso ostruito, un ramo sulla carreggiata, un palo spento, uno stallo
           rosa occupato, una via dove si corre. Arrivano direttamente a me e le leggo tutte.</p>
        <p style="font-family:Oswald,Impact,sans-serif;font-size:1.9rem;line-height:1;margin:14px 0">
          +39 328 369 2227</p>
        <div class="fila-bottoni">
          <a class="bottone bottone--blu" href="https://wa.me/393283692227" target="_blank" rel="noopener">
            Scrivi su WhatsApp</a>
          <button type="button" class="bottone bottone--bianco non-stampare"
            data-copia="+39 328 369 2227" data-avviso-testo="Numero copiato negli appunti!">
            <span aria-hidden="true">&#10697;</span> Copia il numero</button>
        </div>
        <p style="margin-top:14px;font-size:.9rem"><strong>Come scrivere una segnalazione utile:</strong>
          dove si trova il problema (via e riferimento visibile), che cosa si vede, da quanto tempo, e una
          fotografia se puoi farla in sicurezza.</p>
      </div>

      <div class="riquadro">
        <h3><span aria-hidden="true">&#9888;</span> Quando non scrivere a me</h3>
        <ul class="elenco-timbri">
          <li><span class="icona" aria-hidden="true">&#128680;</span>
            <div><strong>Pericolo immediato per le persone: chiama il 112.</strong> Un messaggio pu&ograve;
            restare non letto per ore. Il numero unico di emergenza no.</div></li>
          <li><span class="icona" aria-hidden="true">&#128203;</span>
            <div><strong>Istanze e pratiche formali:</strong> vanno al protocollo del Comune, tramite PEC
            o agli sportelli. Un messaggio non &egrave; un atto e non fa decorrere alcun termine.</div></li>
          <li><span class="icona" aria-hidden="true">&#127829;</span>
            <div><strong>Ordinazioni di pizze:</strong> qui non se ne fanno. Il paese ha pizzerie vere e
            sono molto meglio di questo sito.</div></li>
        </ul>
        <div class="fila-bottoni">
          <a class="bottone" href="tel:112">Chiama il 112</a>
        </div>
      </div>

    </div>
  </div>
</section>

""" + nastro("nastro--giallo") + """

<section class="sezione sezione--scura">
  <div class="contenitore">
    <h2 class="sezione__titolo" style="color:#facc15">Chi risponde</h2>
    <div class="griglia griglia--2">
      <div class="riquadro">
        <h3>Guido Costalonga</h3>
        <p>Assessore alla Sicurezza, Protezione Civile, Patrimonio e Mobilit&agrave; Sostenibile del Comune
           di Roveredo in Piano (Pordenone). Deleghe operative su sicurezza, decoro urbano, viabilit&agrave;,
           patrimonio e manutenzione, protezione civile. Su questo sito, per ora, trovi i primi tre
           fronti: gli altri arrivano.</p>
        <p>A Roveredo dal 2010, sposato con Stefania, padre di Giacomo, Caterina e Beatrice. Iscritto a
           Fratelli d'Italia dal primo giorno. Volontario, ma dietro le linee.</p>
        <p><em>&laquo;Fermezza s&igrave;, allarmismi no.&raquo;</em></p>
        <div class="fila-bottoni">
          <a class="bottone bottone--blu" href="https://costalonga.org/chi-sono/"
             target="_blank" rel="noopener">La storia per esteso</a>
        </div>
      </div>
      <div class="riquadro riquadro--giallo">
        <h3>E il soprannome?</h3>
        <p>Nato nel 1994 davanti a un modem, rimasto addosso per pi&ugrave; di trent'anni, oggi diventato
           l'indirizzo di questo sito. Sarebbe stato pi&ugrave; ridicolo cambiarlo che tenerlo.</p>
        <p>Chi vuole farci una battuta, faccia pure: &egrave; gratis e in genere fa ridere. Poi per&ograve;
           si torna agli atti, alle date e ai fossi da pulire.</p>
        <div style="margin-top:12px">
          <span class="timbro timbro--blu timbro--obliquo"><span aria-hidden="true">&#127829;&#128683;</span>
            Zero ananas, solo fatti</span>
        </div>
      </div>
    </div>

    <div class="riquadro riquadro--blu">
      <h3>Altri strumenti, tutti liberi da usare</h3>
      <ul class="elenco-timbri">
        <li><span class="icona" aria-hidden="true">&#128680;</span>
          <div><a href="https://costalonga.org/truffe/" target="_blank" rel="noopener">Vademecum
          antitruffa completo</a>, con le ventiquattro regole da stampare e appendere vicino al telefono.</div></li>
        <li><span class="icona" aria-hidden="true">&#128106;</span>
          <div><a href="https://costalonga.org/interventi-famiglia-fvg/" target="_blank" rel="noopener">Il
          Friuli Venezia Giulia per le famiglie</a>: le misure regionali con importi, requisiti e scadenze.</div></li>
        <li><span class="icona" aria-hidden="true">&#127968;</span>
          <div><a href="https://costalonga.org/vademecum-proloco/" target="_blank" rel="noopener">Vademecum
          Pro Loco</a>: contributi, agevolazioni fiscali e adempimenti, passo per passo.</div></li>
        <li><span class="icona" aria-hidden="true">&#127780;</span>
          <div><a href="https://costalonga.org/meteo/" target="_blank" rel="noopener">Meteo Friuli Venezia
          Giulia</a>: previsioni per tutti i Comuni della regione.</div></li>
      </ul>
    </div>

    <div class="riquadro riquadro--nero" id="privacy">
      <h3><span aria-hidden="true">&#128274;</span> Chi naviga qui non lascia traccia</h3>
      <p>Questo sito &egrave; fatto di pagine ferme: nessun programma gira dietro le quinte, non c'&egrave;
         nessun archivio e non c'&egrave; niente da riempire. In concreto:</p>
      <ul class="elenco-timbri">
        <li><span class="icona" aria-hidden="true">&#127850;</span>
          <div><strong>Nessun cookie.</strong> Non ne viene scritto nemmeno uno, n&eacute; tecnico
          n&eacute; di altro tipo. Per questo non c'&egrave; nessuna finestra che chiede il consenso:
          non c'&egrave; niente da consentire.</div></li>
        <li><span class="icona" aria-hidden="true">&#128202;</span>
          <div><strong>Nessuna statistica, nessun tracciamento.</strong> Niente Google Analytics,
          niente pixel delle reti sociali, niente pubblicit&agrave;, niente profilazione.</div></li>
        <li><span class="icona" aria-hidden="true">&#9997;</span>
          <div><strong>Nessun modulo da compilare.</strong> Non viene chiesto un indirizzo di posta,
          un numero di telefono o un nome: non c'&egrave; nessuna casella in cui scriverli.</div></li>
        <li><span class="icona" aria-hidden="true">&#127760;</span>
          <div><strong>Niente che arrivi da altri siti.</strong> Caratteri, immagini e stile stanno
          tutti qui dentro: aprendo una pagina il navigatore non contatta nessun altro indirizzo,
          quindi nessuno pu&ograve; vedere che cosa si sta leggendo.</div></li>
        <li><span class="icona" aria-hidden="true">&#128273;</span>
          <div><strong>Collegamento cifrato.</strong> Le pagine viaggiano cifrate, con certificato
          Let's Encrypt, e l'indirizzo comincia sempre con <strong>https</strong>.</div></li>
      </ul>
      <p style="margin-top:14px"><strong>L'unica cosa che resta registrata non dipende da questo sito:</strong>
         il servizio che lo ospita, GitHub Pages, tiene per un tempo limitato i registri tecnici delle
         connessioni, come fa qualunque server del mondo per funzionare e per difendersi dagli attacchi.
         Sono dati che l'assessore non riceve, non vede e non pu&ograve; usare.</p>
      <p>Se apri un collegamento verso l'esterno, per esempio il sito del Comune o WhatsApp, da quel
         momento in poi valgono le regole di quel sito, non pi&ugrave; queste.</p>
    </div>
  </div>
</section>
</main>
"""

scrivi("contatti.html", pagina(
    "contatti.html",
    "Ricevimento e contatti | GinoPizza.it",
    "Recapiti del Comune di Roveredo in Piano, prenotazione appuntamento in municipio, PEC, protocollo e "
    "contatto diretto dell'assessore Guido Costalonga per le segnalazioni.",
    CORPO_CONTATTI))


# ============================================================
# File di servizio
# ============================================================
PAGINE_MAPPA = [("" if f == "index.html" else f) for f in NOMI]
oggi = datetime.date.today().isoformat()
scrivi("sitemap.xml",
       '<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "".join('  <url>\n    <loc>%s/%s</loc>\n    <lastmod>%s</lastmod>\n'
                 '    <changefreq>monthly</changefreq>\n    <priority>%s</priority>\n  </url>\n'
                 % (SITO, p, oggi,
                    "1.0" if p == "" else ("0.8" if NOMI.get(p, ("", 1))[1] is None else "0.6"))
                 for p in PAGINE_MAPPA)
       + '</urlset>\n')

scrivi("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITO)
scrivi("CNAME", "ginopizza.it\n")
scrivi(".nojekyll", "")
