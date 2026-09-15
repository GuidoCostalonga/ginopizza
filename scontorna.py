# -*- coding: utf-8 -*-
"""Toglie lo sfondo a un ritratto a fumetto con contorno nero spesso.

Come funziona: lo sfondo viene riempito partendo dai bordi alto, sinistro e
destro, e la crescita si ferma sui pixel scuri, cioè sul contorno del disegno.
Il bordo basso non viene usato come partenza perché le spalle lo toccano.
Alla fine resta la sagoma più grande, che è il personaggio: tutto il resto,
televisore e mobile compresi, viene scartato.

Uso: python3 scontorna.py entrata.png uscita.png
"""
import sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

# Le misure in pixel qui sotto valgono per un disegno largo LARGHEZZA_BASE;
# su un disegno di dimensione diversa vengono riscalate in proporzione, così
# lo stesso programma lavora tanto sull'originale grande quanto su una copia
# ridotta.
LARGHEZZA_BASE = 2400
CORNICE = 45           # cornice scura da togliere prima di cominciare
BANDA = 35             # entro quanti pixel dai lati il nero è cornice e non disegno
EROSIONE = 5           # di quanto assottigliare per spezzare i fili sottili
ORLO = 50              # quanto vicino al bordo deve arrivare una zona per dirla sfondo
PELLE_CHIARA = 110     # sotto questa luce una zona calda \u00e8 legno, non pelle
SCURO_GIACCA = 55      # sopra questa luce una zona scura non \u00e8 la giacca
SOGLIA_SCURO = 40       # sotto questa luce si è nel contorno o in una parte scura del disegno
TOLLERANZA = 999        # il colore non vincola: a fermare il riempimento basta il contorno


# Il taglio a sinistra: lo sfondo di questo disegno sta a sinistra del
# personaggio, e il disegno chiude televisore e mobile con lo stesso tratto
# nero della testa, quindi nessun assottigliamento li stacca. Si taglia
# seguendo il bordo vero del soggetto, misurato riga per riga.
QUOTA_ARRIVO = 0.62     # fin dove cercare il soggetto, in frazione di larghezza
FILA_MINIMA = 10        # quanti pixel di seguito servono per dire "questa è pelle"
ROSSO_SU_BLU = 30       # quanto il rosso supera il blu nella pelle e nella barba
ROSSO_SU_VERDE = 14     # quanto il rosso supera il verde: il legno del mobile non ci arriva
SOGLIA_TRATTO = 70      # sotto questa luce si è dentro al tratto nero del contorno
CELLA_CHIUSA = 200      # larghezza massima di una cella chiusa dentro il disegno
CELLA_FREDDA = 25       # una cella da scavalcare non ha il rosso sopra il blu
BLU_GIACCA = 8          # di quanto il blu supera il rosso nella giacca scura
SALTI = 3               # quante celle chiuse di seguito si possono scavalcare
LISCIO = 40             # mezza finestra della statistica che liscia il bordo
QUANTILE = 50           # la mediana: regge anche cinquanta righe confuse di seguito
PUNTE = 40               # mezza finestra che spiana le punte rimaste verso sinistra


def chiazze(maschera):
    """Elenca le zone unite della maschera: (maschera della zona, riquadro)."""
    h, w = maschera.shape
    visto = np.zeros((h, w), bool)
    fuori = []
    for y0 in range(h):
        for x0 in range(w):
            if maschera[y0, x0] and not visto[y0, x0]:
                q = deque([(y0, x0)]); visto[y0, x0] = True
                punti = []
                while q:
                    y, x = q.popleft(); punti.append((y, x))
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w and maschera[ny, nx] and not visto[ny, nx]:
                            visto[ny, nx] = True; q.append((ny, nx))
                ys = [p[0] for p in punti]; xs = [p[1] for p in punti]
                m = np.zeros((h, w), bool)
                m[ys, xs] = True
                fuori.append((m, (min(ys), max(ys), min(xs), max(xs))))
    return fuori


def misura(valore, fattore, minimo=1):
    """Riscala una misura in pixel sulla larghezza vera del disegno."""
    return max(minimo, int(round(valore * fattore)))


def fasce(riga_scura):
    """Spezza una riga nelle sue fasce: (inizio, fine compreso, scura)."""
    out, x, w = [], 0, len(riga_scura)
    while x < w:
        s = bool(riga_scura[x]); i = x
        while x < w and bool(riga_scura[x]) == s:
            x += 1
        out.append((i, x - 1, s))
    return out


def bordo_del_soggetto(a, lum, fattore=1.0):
    """Per ogni riga dice dove comincia il soggetto, oppure -1 se non c'è.

    Il segno della pelle e della barba è il rosso che supera insieme il blu e
    il verde: il grigio del televisore non lo ha, e il legno del mobile ha sì
    il rosso sopra il blu ma non sopra il verde, quindi non viene scambiato
    per personaggio.

    Trovata la prima pelle si cammina verso sinistra di fascia in fascia. Il
    tratto nero si attraversa sempre, perché è il contorno del disegno. Una
    fascia chiara si attraversa solo se è stretta, fredda di colore e chiusa
    da un altro tratto: è il caso della lente degli occhiali, che lascia
    vedere lo sfondo ma appartiene al soggetto. Lo sfondo vero è largo, e il
    legno del mobile ha il rosso sopra il blu: lì il cammino si ferma.
    """
    h, w, _ = a.shape
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    pelle = ((r - b) > ROSSO_SU_BLU) & ((r - g) > ROSSO_SU_VERDE)
    # Sotto la barba il bordo non \u00e8 pelle ma la giacca: scura e tendente al blu.
    giacca = (lum < SCURO_GIACCA) & ((b - r) > BLU_GIACCA)
    pelle = pelle | giacca
    scuro = lum < SOGLIA_TRATTO
    arrivo = int(w * QUOTA_ARRIVO)
    fila_minima = misura(FILA_MINIMA, fattore)
    cella_chiusa = misura(CELLA_CHIUSA, fattore)
    liscio_meta = misura(LISCIO, fattore)
    bordo = np.full(h, -1)
    for y in range(h):
        x, fila = -1, 0
        for i in range(arrivo):
            if pelle[y, i]:
                fila += 1
                if fila >= fila_minima:
                    x = i - fila_minima + 1
                    break
            else:
                fila = 0
        if x < 0:
            continue
        fs = fasce(scuro[y])
        i = 0
        while i < len(fs) and fs[i][1] < x:
            i += 1
        while i >= 0 and not fs[i][2]:      # torna alla prima fascia scura
            i -= 1
        if i < 0:
            continue
        for _ in range(SALTI):
            if i - 1 < 0:
                break
            p, q, _s = fs[i - 1]
            freddo = int(np.mean(r[y, p:q + 1]) - np.mean(b[y, p:q + 1])) < CELLA_FREDDA
            if (q - p + 1) <= cella_chiusa and freddo and i - 2 >= 0:
                i -= 2                      # era una cella chiusa: si scavalca
            else:
                break                       # era lo sfondo: il bordo è questo
        bordo[y] = fs[i][0]
    # Una statistica mobile toglie i salti delle righe in cui il bordo passa
    # dietro a una linea scura dello sfondo. Non si prende la mediana ma il
    # primo quarto: in caso di dubbio il taglio resta più a sinistra, cioè
    # lascia un filo di sfondo invece di mangiare un pezzo di disegno.
    liscio = bordo.copy()
    for y in range(h):
        finestra = [v for v in bordo[max(0, y - liscio_meta):y + liscio_meta + 1] if v >= 0]
        if finestra and bordo[y] >= 0:
            liscio[y] = int(np.percentile(finestra, QUANTILE))
    # Qualche riga isolata scappa ancora a sinistra e lascia un filo di
    # televisore attaccato: si spiana tenendo, in una finestrella, il valore
    # pi\u00f9 a destra. Costa un paio di pixel di disegno, toglie le punte.
    punte = misura(PUNTE, fattore)
    spianato = liscio.copy()
    for y in range(h):
        finestra = [v for v in liscio[max(0, y - punte):y + punte + 1] if v >= 0]
        if finestra and liscio[y] >= 0:
            spianato[y] = max(finestra)
    return spianato


def scontorna(entrata, uscita, margine=14):
    im = Image.open(entrata).convert("RGB")
    fattore = im.width / float(LARGHEZZA_BASE)
    cornice = misura(CORNICE, fattore)
    banda = misura(BANDA, fattore)
    erosione = misura(EROSIONE, fattore, 2)
    margine = misura(margine, fattore)
    # L'immagine ha una cornice scura tutt'intorno: se non la si toglie,
    # il riempimento non ha da dove partire perché ogni bordo risulta contorno.
    if cornice:
        im = im.crop((cornice, cornice, im.width - cornice, im.height - cornice))
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    lum = (0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2])
    scuro = lum < SOGLIA_SCURO

    # 1. Riempimento dello sfondo dai tre bordi liberi.
    sfondo = np.zeros((h, w), bool)
    coda = deque()
    for x in range(w):                       # bordo alto
        if not scuro[0, x]: coda.append((0, x)); sfondo[0, x] = True
    for y in range(h):                       # bordi laterali
        if not scuro[y, 0]: coda.append((y, 0)); sfondo[y, 0] = True
        if not scuro[y, w - 1]: coda.append((y, w - 1)); sfondo[y, w - 1] = True

    while coda:
        y, x = coda.popleft()
        c = a[y, x]
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not sfondo[ny, nx] and not scuro[ny, nx]:
                if int(np.abs(a[ny, nx] - c).max()) <= TOLLERANZA:
                    sfondo[ny, nx] = True
                    coda.append((ny, nx))

    # 1bis. Sui due lati resta una striscia scura della cornice originale, che fa
    # da ponte fra il contorno del personaggio e quello del televisore: si toglie
    # riempiendo anche il nero raggiungibile dai bordi laterali.
    # Solo dai lati: in alto la testa tocca il bordo, e partire da lì
    # significherebbe mangiarsi tutto il contorno del disegno.
    coda = deque()
    for y in range(h):
        for x in (0, w - 1):
            if scuro[y, x] and not sfondo[y, x]: coda.append((y, x)); sfondo[y, x] = True
    while coda:
        y, x = coda.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if (0 <= ny < h and 0 <= nx < w and not sfondo[ny, nx] and scuro[ny, nx]
                    and (nx < banda or nx >= w - banda)):
                sfondo[ny, nx] = True
                coda.append((ny, nx))

    # 1ter. Le parti dello sfondo chiuse dentro il loro contorno (il pannello
    # di legno, il muretto, il piede del mobile) non le raggiunge nessun
    # riempimento. Si riconoscono da una cosa sola: arrivano a toccare il
    # bordo alto, sinistro o destro del quadro, dove il personaggio non va
    # mai, perch\u00e9 il busto esce soltanto dal bordo basso.
    orlo = misura(ORLO, fattore)
    for chiazza in chiazze(~sfondo & ~scuro):
        y1, y2, x1, x2 = chiazza[1]
        if not (y1 <= orlo or x1 <= orlo or x2 >= w - 1 - orlo):
            continue
        zona = chiazza[0]
        luce = float(lum[zona].mean())
        rosso = float(a[:, :, 0][zona].mean())
        verde = float(a[:, :, 1][zona].mean())
        blu = float(a[:, :, 2][zona].mean())
        calda = (rosso - blu) > ROSSO_SU_BLU and (rosso - verde) > ROSSO_SU_VERDE
        if (calda and luce > PELLE_CHIARA) or luce < SCURO_GIACCA:
            continue                       # \u00e8 pelle chiara o la giacca scura
        sfondo[zona] = True

    # 2. Taglio a sinistra lungo il bordo vero del soggetto: così televisore e
    # mobile si staccano dal personaggio prima ancora di contare le sagome.
    davanti = ~sfondo
    bordo = bordo_del_soggetto(a, lum, fattore)
    for y in range(h):
        if bordo[y] > 0:
            davanti[y, :bordo[y]] = False
    sfondo = ~davanti

    # 3. Della parte rimasta si tiene solo la sagoma più grande: il personaggio.
    # Prima però si assottiglia la maschera: così i fili di pochi pixel che
    # tengono ancora attaccato il televisore si spezzano, mentre la figura,
    # che è spessa, resta tutta intera. Alla fine si rigonfia di altrettanto.
    m = Image.fromarray((davanti * 255).astype(np.uint8), "L")
    m = m.filter(ImageFilter.MinFilter(2 * erosione + 1))
    davanti = np.asarray(m) > 127
    etichette = np.zeros((h, w), np.int32)
    n, migliore, dim_migliore = 0, 0, 0
    for y0 in range(h):
        for x0 in range(w):
            if davanti[y0, x0] and etichette[y0, x0] == 0:
                n += 1
                q = deque([(y0, x0)]); etichette[y0, x0] = n; dim = 0
                while q:
                    y, x = q.popleft(); dim += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w and davanti[ny, nx] and etichette[ny, nx] == 0:
                            etichette[ny, nx] = n; q.append((ny, nx))
                if dim > dim_migliore:
                    dim_migliore, migliore = dim, n
    soggetto = etichette == migliore
    m = Image.fromarray((soggetto * 255).astype(np.uint8), "L")
    m = m.filter(ImageFilter.MaxFilter(2 * erosione + 1))
    soggetto = (np.asarray(m) > 127) & ~sfondo
    print("sagome trovate: %d | personaggio: %d pixel (%.1f%% del quadro)"
          % (n, dim_migliore, 100.0 * dim_migliore / (h * w)))

    # 4. Trasparenza con bordo ammorbidito, per non lasciare la scaletta.
    alfa = Image.fromarray((soggetto * 255).astype(np.uint8), "L")
    alfa = alfa.filter(ImageFilter.GaussianBlur(0.7))
    fuori = Image.merge("RGBA", (*im.split(), alfa))

    # 5. Ritaglio sul personaggio, con un margine di respiro.
    ys, xs = np.where(soggetto)
    y1, y2 = max(0, ys.min() - margine), min(h, ys.max() + 1 + margine)
    x1, x2 = max(0, xs.min() - margine), min(w, xs.max() + 1 + margine)
    fuori = fuori.crop((x1, y1, x2, y2))
    fuori.save(uscita)
    print("scritto %s  %dx%d" % (uscita, fuori.width, fuori.height))


if __name__ == "__main__":
    scontorna(sys.argv[1], sys.argv[2])
