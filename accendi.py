# -*- coding: utf-8 -*-
"""Accende lo schermo del televisore e ci mette dentro la scatola di GinoPizza.

Il vetro dello schermo viene riconosciuto con un riempimento che parte da
dentro e si ferma sul tratto nero: così testa e occhiali, che stanno davanti,
restano fuori dalla maschera e la luce non ci finisce sopra.
"""
import numpy as np
from collections import deque
from PIL import Image, ImageFilter

SEME = (320, 250)        # un punto qualsiasi dentro al vetro (riga, colonna)
SOGLIA_TRATTO = 45       # sotto questa luce si è sul contorno nero
LUCE = 0.93              # quanto la luce copre il grigio dello schermo spento
ALONE = 0.50             # quanto lo schermo illumina quello che ha intorno
SFOCATURA = 55           # quanto è morbido l'alone


def vetro(a):
    lum = 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]
    h, w = lum.shape
    scuro = lum < SOGLIA_TRATTO
    dentro = np.zeros((h, w), bool)
    coda = deque([SEME]); dentro[SEME] = True
    while coda:
        y, x = coda.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not dentro[ny, nx] and not scuro[ny, nx]:
                dentro[ny, nx] = True
                coda.append((ny, nx))
    return dentro


def accendi(entrata, scatola_png, uscita):
    base = Image.open(entrata).convert("RGB")
    a = np.asarray(base).astype(np.float64)
    h, w, _ = a.shape
    m = vetro(a)
    ys, xs = np.where(m)
    cx, cy = xs.mean(), ys.mean()

    # 1. La luce dello schermo: più chiara al centro, più calda ai bordi.
    yy, xx = np.mgrid[0:h, 0:w]
    raggio = max(xs.max() - xs.min(), ys.max() - ys.min()) / 1.35
    d = np.clip(np.sqrt(((xx - cx) ** 2 + (yy - cy) ** 2)) / raggio, 0, 1)[:, :, None]
    centro = np.array([255, 253, 244], float)
    orlo = np.array([214, 188, 132], float)
    luce = centro * (1 - d) + orlo * d

    # 2. Le righe orizzontali del tubo catodico, appena accennate.
    righe = (np.arange(h) % 4 < 1).astype(float)[:, None, None] * 14
    luce = np.clip(luce - righe, 0, 255)

    fuori = a.copy()
    mm = m[:, :, None]
    fuori = np.where(mm, a * (1 - LUCE) + luce * LUCE, fuori)

    # 3. Il riflesso obliquo sul vetro.
    diag = np.clip((xx * 0.55 + yy * 0.8) / (w * 0.42), 0, 1)
    vel = np.clip(0.40 * (1 - diag), 0, 1)[:, :, None]
    fuori = np.where(mm, fuori + (255 - fuori) * vel, fuori)

    # 4. L'alone che lo schermo acceso butta fuori dal vetro.
    sfocata = np.asarray(Image.fromarray((m * 255).astype(np.uint8), "L")
                         .filter(ImageFilter.GaussianBlur(SFOCATURA))).astype(float) / 255.0
    sfocata = (sfocata * ALONE)[:, :, None]
    calda = np.array([255, 244, 210], float)
    fuori = fuori + (calda - fuori) * np.clip(sfocata - (mm * ALONE), 0, 1)

    im = Image.fromarray(np.clip(fuori, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

    # 5. La scatola, centrata sul vetro e ritagliata come il vetro: dove passa
    # la testa sparisce dietro, invece di stamparcisi sopra.
    sc = Image.open(scatola_png).convert("RGBA")
    # Grande quanto lo consente il vetro: la testa taglia la parte destra
    # dello schermo, quindi la scatola si appoggia al bordo sinistro e la
    # scritta resta tutta nella parte che si vede.
    lato = int((xs.max() - xs.min()) * 0.74)
    sc = sc.resize((lato, lato), Image.LANCZOS)
    px = int(xs.min()) + 2
    py = int(cy - lato / 2)
    strato = Image.new("RGBA", im.size, (0, 0, 0, 0))
    strato.paste(sc, (px, py), sc)
    alfa = np.asarray(strato)[:, :, 3].astype(float) / 255.0
    alfa = alfa * m
    strato = Image.merge("RGBA", (*strato.split()[:3],
                                  Image.fromarray((alfa * 255).astype(np.uint8), "L")))
    im.alpha_composite(strato)

    im.convert("RGB").save(uscita, quality=95)
    print("vetro %d px, centro (%d,%d), scatola %d px -> %s"
          % (m.sum(), cx, cy, lato, uscita))


if __name__ == "__main__":
    import sys
    accendi(sys.argv[1], sys.argv[2], sys.argv[3])
