#!/usr/bin/env python3
"""Estilos alternativos do @adv.caiomachado (para mesclar com o estilo principal).
Uso: python3 render/estilos.py spec.json -> arte/<arquivo>-NN.png
Spec: {"arquivo": "...", "kicker": "DIREITO DO CONSUMIDOR", "telas": [ {...}, ... ]}
Cada tela tem "estilo" e os campos do estilo:
  moldura : foto, crop_y?, titulo, texto (**negrito**), chamada?
  mito    : mito, verdade (**negrito**), base? (fonte legal)
  mito_capa: foto, titulo, sub
  lei     : citacao, fonte, significado (**negrito**)
  checklist: titulo, itens[], nota?
  numero  : foto?, numero, unidade, titulo, texto
  final   : foto, l1, l2, sub   (página final com foto pública e convite)
Fotos: sempre do banco público (banco/...)."""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVY=(33,41,59); TERRA=(157,87,76); BG=(246,241,234); TXT=(62,66,78); BEIGE=(235,227,217); WHITE=(255,255,255); ROSE=(214,150,138)
W, H, M = 1080, 1350, 90

def sans(w, s): return ImageFont.truetype(f"{R}/fontes/Poppins-{w}.ttf", s)
def serif(s, w="Bold", italic=False):
    f = ImageFont.truetype(f"{R}/fontes/Lora-Variable.ttf", s)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def rich(d, x, y, text, size, maxw, color=TXT, bold=NAVY, lh=1.45):
    fr, fb = sans("Regular", size), sans("Bold", size)
    toks = []
    for i, part in enumerate(re.split(r"\*\*", text)):
        for w in part.split(): toks.append((w, i % 2 == 1))
    sp = d.textlength(" ", font=fr); cx = x; step = int(size * lh)
    for w, b in toks:
        f = fb if b else fr; tw = d.textlength(w, font=f)
        if w[0] in ",.;:)?!" and cx > x: cx -= sp
        if cx > x and cx + tw > x + maxw: cx = x; y += step
        d.text((cx, y), w, font=f, fill=bold if b else color); cx += tw + sp
    return y + step
def lines(d, x, y, text, font, maxw, fill, lh):
    for l in wrap(d, text, font, maxw): d.text((x, y), l, font=font, fill=fill); y += lh
    return y
def foto(path, w, h, crop_y=None):
    im = Image.open(f"{R}/{path}").convert("RGB")
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    oy = int((im.height - h) * (0.35 if crop_y is None else crop_y)); ox = (im.width - w) // 2
    return im.crop((ox, oy, ox + w, oy + h))
def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width, im.height), radius=r, fill=255); return m
def header(d, dark, kicker=None):
    c = BEIGE if dark else NAVY
    d.text((M, 58), "CAIO MACHADO", font=sans("Medium", 26), fill=c)
    d.text((M, 90), "ADVOCACIA", font=sans("Light", 18), fill=c)
    if kicker:
        f = sans("Medium", 20); tw = d.textlength(kicker, font=f)
        d.rounded_rectangle((W - M - tw - 40, 58, W - M, 100), radius=21, fill=TERRA); d.text((W - M - tw - 20, 66), kicker, font=f, fill=WHITE)
def footer(d, dark, txt="Ficou com dúvida? Fale comigo!"):
    c = BEIGE if dark else NAVY
    d.line((M, 1250, W - M, 1250), fill=TERRA, width=3)
    f = sans("Medium", 26); d.text((M, 1270), txt, font=f, fill=c)
    t = "@adv.caiomachado"; d.text((W - M - d.textlength(t, font=f), 1270), t, font=f, fill=c)
def base(dark):
    im = Image.new("RGB", (W, H), NAVY if dark else BG); return im, ImageDraw.Draw(im)

# ---------- estilos ----------
def moldura(t, k):
    im, d = base(False); header(d, False, k)
    ph = foto(t["foto"], W - 2 * M, 560, t.get("crop_y")); im.paste(ph, (M, 140), rounded(ph, 36)); d = ImageDraw.Draw(im)
    y = 740
    if t.get("chamada"): d.text((M, y), t["chamada"].upper(), font=sans("Medium", 24), fill=TERRA); y += 48
    y = lines(d, M, y, t["titulo"], serif(60), W - 2 * M, NAVY, 74) + 18
    d.line((M, y, M + 110, y), fill=TERRA, width=4); y += 30
    y = rich(d, M, y, t["texto"], 34, W - 2 * M)
    assert y < 1240, f"moldura estoura: {y}"
    footer(d, False); return im
def mito_capa(t, k):
    im, d = base(True)
    ph = foto(t["foto"], W, 640, t.get("crop_y")); im.paste(ph, (0, 0))
    g = np.clip((np.arange(640) - 300) / 340, 0, 1)[:, None, None]
    arr = np.array(im, dtype=np.float32); arr[:640] = arr[:640] * (1 - g) + np.array(NAVY) * g; im = Image.fromarray(arr.astype("uint8")); d = ImageDraw.Draw(im)
    header(d, True, k)
    y = 640
    for word, col in (("MITO", ROSE), ("ou", BEIGE), ("VERDADE?", BEIGE)):
        f = serif(120 if word != "ou" else 60); d.text((M, y), word, font=f, fill=col); y += 130 if word != "ou" else 70
    y += 10; y = lines(d, M, y, t["titulo"], sans("Medium", 38), W - 2 * M, WHITE, 54)
    footer(d, True, "Arraste e teste o que você sabe"); return im
def mito(t, k):
    im, d = base(False); header(d, False, k)
    d.rounded_rectangle((M, 150, W - M, 610), radius=32, fill=WHITE, outline=(225, 215, 203), width=2)
    d.rounded_rectangle((M + 40, 190, M + 200, 240), radius=25, fill=TERRA); d.text((M + 72, 198), "MITO", font=sans("Bold", 26), fill=WHITE)
    y = lines(d, M + 40, 280, "“" + t["mito"] + "”", serif(52, "Regular"), W - 2 * M - 80, NAVY, 66)
    assert y < 600
    d.rounded_rectangle((M, 650, W - M, 1200), radius=32, fill=NAVY)
    d.rounded_rectangle((M + 40, 690, M + 260, 740), radius=25, fill=BEIGE); d.text((M + 68, 698), "VERDADE", font=sans("Bold", 26), fill=NAVY)
    y = rich(d, M + 40, 780, t["verdade"], 36, W - 2 * M - 80, color=BEIGE, bold=WHITE)
    if t.get("base"): d.text((M + 40, y + 10), t["base"], font=sans("Medium", 26), fill=ROSE); y += 50
    assert y < 1190, f"mito estoura {y}"
    footer(d, False); return im
def lei(t, k):
    im, d = base(True); header(d, True, k)
    d.text((M - 10, 120), "“", font=serif(260), fill=TERRA)
    y = lines(d, M, 360, t["citacao"], serif(44, "Regular"), W - 2 * M, BEIGE, 62) + 20
    d.text((M, y), t["fonte"], font=sans("Medium", 30), fill=ROSE); y += 70
    d.rectangle((0, y, W, H), fill=BG); d = ImageDraw.Draw(im)
    y += 50; d.text((M, y), "O QUE ISSO SIGNIFICA PARA VOCÊ", font=sans("Bold", 26), fill=TERRA); y += 56
    y = rich(d, M, y, t["significado"], 36, W - 2 * M)
    assert y < 1240, f"lei estoura {y}"
    footer(d, False); return im
def checklist(t, k):
    im, d = base(False); header(d, False, k)
    y = lines(d, M, 170, t["titulo"], serif(62), W - 2 * M, NAVY, 76) + 20
    d.line((M, y, M + 110, y), fill=TERRA, width=4); y += 50
    f = sans("Regular", 36)
    for it in t["itens"]:
        d.rounded_rectangle((M, y + 4, M + 52, y + 56), radius=10, outline=TERRA, width=4)
        d.line((M + 12, y + 30, M + 23, y + 43), fill=TERRA, width=6); d.line((M + 23, y + 43, M + 42, y + 16), fill=TERRA, width=6)
        ly = y
        for l in wrap(d, it, f, W - 2 * M - 90): d.text((M + 84, ly), l, font=f, fill=TXT); ly += 50
        y = max(ly, y + 60) + 30
    if t.get("nota"):
        nf = sans("Medium", 28); nl = wrap(d, t["nota"], nf, W - 2 * M - 60); nh = len(nl) * 42 + 44
        d.rounded_rectangle((M, y, W - M, y + nh), radius=24, fill=NAVY); ty = y + 22
        for l in nl: d.text((M + 30, ty), l, font=nf, fill=BEIGE); ty += 42
        y += nh
    assert y < 1240, f"checklist estoura {y}"
    footer(d, False); return im
def numero(t, k):
    im, d = base(True)
    if t.get("foto"):
        ph = foto(t["foto"], W, 520, t.get("crop_y")); im.paste(ph, (0, 0))
        g = np.clip((np.arange(520) - 160) / 360, 0, 1)[:, None, None]
        arr = np.array(im, dtype=np.float32); arr[:520] = arr[:520] * (1 - g) + np.array(NAVY) * g; im = Image.fromarray(arr.astype("uint8")); d = ImageDraw.Draw(im)
    header(d, True, k)
    fN = serif(400); d.text((M - 20, 330), t["numero"], font=fN, fill=BEIGE)
    nw = d.textlength(t["numero"], font=fN)
    d.text((M + nw + 10, 600), t["unidade"], font=serif(110), fill=ROSE)
    y = 820; y = lines(d, M, y, t["titulo"], serif(52), W - 2 * M, WHITE, 66) + 16
    y = rich(d, M, y, t["texto"], 34, W - 2 * M, color=BEIGE, bold=WHITE)
    assert y < 1240, f"numero estoura {y}"
    footer(d, True); return im
def final(t, k):
    im, d = base(True)
    ph = foto(t["foto"], W, 760, t.get("crop_y")); im.paste(ph, (0, 0))
    ys = np.arange(760); g = np.maximum(np.clip((ys - 300) / 460, 0, 1), np.clip(1 - ys / 200, 0, 1) * 0.75)[:, None, None]
    arr = np.array(im, dtype=np.float32); arr[:760] = arr[:760] * (1 - g) + np.array(NAVY) * g; im = Image.fromarray(arr.astype("uint8")); d = ImageDraw.Draw(im)
    header(d, True)
    y = 720; d.text((M, y), t["l1"], font=serif(64), fill=WHITE); y += 84
    d.text((M - 4, y), t["l2"], font=serif(130), fill=BEIGE); y += 170
    y = lines(d, M, y, t["sub"], sans("Medium", 38), W - 2 * M, WHITE, 54) + 20
    pf = sans("Medium", 32); tx = "Salve e envie para quem precisa"; tw = d.textlength(tx, font=pf)
    d.rounded_rectangle((M, y, M + tw + 60, y + 68), radius=34, fill=TERRA); d.text((M + 30, y + 13), tx, font=pf, fill=WHITE)
    footer(d, True); return im

ESTILOS = dict(moldura=moldura, mito_capa=mito_capa, mito=mito, lei=lei, checklist=checklist, numero=numero, final=final)
def make(sp):
    os.makedirs(f"{R}/arte", exist_ok=True); out = []
    for i, t in enumerate(sp["telas"], 1):
        im = ESTILOS[t["estilo"]](t, sp.get("kicker"))
        fn = f"{R}/arte/{sp['arquivo']}-{i:02d}.png"; im.save(fn); out.append(fn)
    print("\n".join(out))
if __name__ == "__main__": make(json.load(open(sys.argv[1])))
