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

CORNICE = 45           # cornice scura da togliere prima di cominciare
BANDA = 35             # entro quanti pixel dai lati il nero è cornice e non disegno
EROSIONE = 5           # di quanto assottigliare per spezzare i fili sottili
SOGLIA_SCURO = 25       # solo il nero pieno è contorno: lo sfondo qui è scuro quanto un'ombra
TOLLERANZA = 999        # il colore non vincola: a fermare il riempimento basta il contorno


# Il taglio a sinistra vale per questo ritratto: lo sfondo freddo sta a
# sinistra, il soggetto è caldo di pelle. I due numeri qui sotto dicono da
# dove partire a cercare e fin dove guardare.
PARTENZA = 350          # prima colonna utile: più a sinistra c'è solo sfondo
ARRIVO = 900            # oltre questa colonna il soggetto c'è di sicuro
FINE_OCCHIALI = 940     # ultima riga in cui il bordo è la montatura
FINE_TAGLIO = 1010      # sotto questa riga non resta nulla da togliere
BORDO_BARBA = 620       # bordo del soggetto sotto gli occhiali


def taglia_a_sinistra(a, lum, soggetto):
    """Toglie dalla sagoma tutto ciò che sta a sinistra del bordo vero."""
    h, w = soggetto.shape
    caldo = (a[:, :, 0] - a[:, :, 2]) > 25
    bordo = np.full(h, -1)
    for y in range(h):
        x0, fila = None, 0
        for x in range(PARTENZA, min(ARRIVO, w)):
            if caldo[y, x]:
                fila += 1
                if fila >= 8:
                    x0 = x - 7
                    break
            else:
                fila = 0
        if x0 is None:
            continue
        while x0 > PARTENZA and lum[y, x0 - 1] < 70:
            x0 -= 1
        bordo[y] = x0
    # una mediana mobile toglie i salti dove passa la linea del mobile
    liscio = bordo.copy()
    for y in range(h):
        finestra = [v for v in bordo[max(0, y - 15):y + 16] if v > 0]
        if finestra:
            liscio[y] = int(np.median(finestra))
    for y in range(PARTENZA, min(FINE_TAGLIO, h)):
        if y <= FINE_OCCHIALI:
            taglio = liscio[y]
        elif y < FINE_OCCHIALI + 10:
            passo = (y - FINE_OCCHIALI) / 10.0
            taglio = int(liscio[FINE_OCCHIALI] + (BORDO_BARBA - liscio[FINE_OCCHIALI]) * passo)
        else:
            taglio = BORDO_BARBA
        if taglio > 0:
            soggetto[y, :taglio] = False
    return soggetto


def scontorna(entrata, uscita, margine=14):
    im = Image.open(entrata).convert("RGB")
    # L'immagine ha una cornice scura tutt'intorno: se non la si toglie,
    # il riempimento non ha da dove partire perché ogni bordo risulta contorno.
    if CORNICE:
        im = im.crop((CORNICE, CORNICE, im.width - CORNICE, im.height - CORNICE))
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
                    and (nx < BANDA or nx >= w - BANDA)):
                sfondo[ny, nx] = True
                coda.append((ny, nx))

    # 2. Della parte rimasta si tiene solo la sagoma più grande: il personaggio.
    # Prima però si assottiglia la maschera: così i fili di pochi pixel che
    # tengono ancora attaccato il televisore si spezzano, mentre la figura,
    # che è spessa, resta tutta intera. Alla fine si rigonfia di altrettanto.
    davanti = ~sfondo
    m = Image.fromarray((davanti * 255).astype(np.uint8), "L")
    m = m.filter(ImageFilter.MinFilter(2 * EROSIONE + 1))
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
    m = m.filter(ImageFilter.MaxFilter(2 * EROSIONE + 1))
    soggetto = (np.asarray(m) > 127) & ~sfondo
    print("sagome trovate: %d | personaggio: %d pixel (%.1f%% del quadro)"
          % (n, dim_migliore, 100.0 * dim_migliore / (h * w)))

    # 2bis. Del televisore e del mobile resta la parte che tocca il disegno:
    # il loro contorno, dove sono nascosti dalla testa, è lo stesso contorno
    # della testa, quindi nessun assottigliamento li stacca. Si tagliano
    # seguendo il bordo vero del soggetto, misurato riga per riga: dal grigio
    # dello sfondo si cammina verso destra fino alla prima pelle e si torna
    # indietro fino a dove comincia il nero del contorno.
    soggetto = taglia_a_sinistra(a, lum, soggetto)

    # 3. Trasparenza con bordo ammorbidito, per non lasciare la scaletta.
    alfa = Image.fromarray((soggetto * 255).astype(np.uint8), "L")
    alfa = alfa.filter(ImageFilter.GaussianBlur(0.7))
    fuori = Image.merge("RGBA", (*im.split(), alfa))

    # 4. Ritaglio sul personaggio, con un margine di respiro.
    ys, xs = np.where(soggetto)
    y1, y2 = max(0, ys.min() - margine), min(h, ys.max() + 1 + margine)
    x1, x2 = max(0, xs.min() - margine), min(w, xs.max() + 1 + margine)
    fuori = fuori.crop((x1, y1, x2, y2))
    fuori.save(uscita)
    print("scritto %s  %dx%d" % (uscita, fuori.width, fuori.height))


if __name__ == "__main__":
    scontorna(sys.argv[1], sys.argv[2])
