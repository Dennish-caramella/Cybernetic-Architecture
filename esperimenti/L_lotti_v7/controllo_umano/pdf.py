"""PDF del controllo umano (stesse 60 immagini di prepara.py, stesso ordine H01-H60): una pagina per immagine, con la legenda. Fuori da git (AGEA, sola visione)."""
import os, pandas as pd
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, "..", "..", "_cache", "L_lotti_v7", "controllo_umano")
LEG = ["L  libera: suolo nudo, sterrato, prato o incolto non curato, piazzale vuoto", "C  cantiere", "D  edificato dismesso o degradato (tetti rotti, vegetazione su edifici, nessun segno d'uso)",
       "U  edificato o area in uso (cortili, parcheggi pieni, pertinenze)", "V  verde curato (parco, giardino) o agricolo coltivato", "I  infrastruttura in uso (binari attivi, strade, piazzali di servizio)", "X  non giudicabile"]
F = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", s)
W, H = 1240, 1754; pages = []
def page(): im = Image.new("RGB", (W, H), "white"); return im, ImageDraw.Draw(im)
im, d = page(); d.text((60, 60), "Controllo umano C5 - Base L v7", fill="black", font=F(40))
intro = ["60 immagini aeree AGEA 2018-2019 (licenza di sola visione: non diffondere).", "Per ognuna guarda la parte DENTRO il contorno rosso e scegli la categoria", "che occupa la parte piu' grande dell'area (non la piu' interessante).",
         "Se nessuna supera la meta' scegli comunque la maggiore.", "", "Rispondi in chat con una lettera per codice, per esempio:  H01 L, H02 U, H03 D ...", "Note facoltative dopo la lettera. Puoi rispondere a blocchi.", ""] + LEG
for i, t in enumerate(intro): d.text((60, 160 + i * 42), t, fill="black", font=F(26))
pages.append(im)
for c in sorted(f[:-4] for f in os.listdir(IMG) if f.endswith(".jpg")):
    im, d = page(); d.text((60, 40), c, fill="black", font=F(56)); im.paste(Image.open(os.path.join(IMG, c + ".jpg")).convert("RGB").resize((1100, 1100)), (70, 130))
    for i, t in enumerate(LEG): d.text((70, 1270 + i * 46), t, fill=(60, 60, 60), font=F(24))
    pages.append(im)
out = os.path.join(IMG, "controllo_umano.pdf"); pages[0].save(out, save_all=True, append_images=pages[1:], resolution=150, quality=82); print(len(pages), os.path.getsize(out) // 1024, "KB")
