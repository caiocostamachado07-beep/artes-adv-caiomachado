#!/usr/bin/env python3
"""Stories (1080x1920) do @adv.caiomachado. Só fotos públicas (banco/).
Uso: python3 render/stories.py spec.json -> arte/<arquivo>-NN.jpg (JPEG, exigido para Story)
Spec: {"arquivo": "...", "kicker": "...", "stories": [ {"estilo": ..., ...}, ... ]}
Estilos:
  dica      : foto, titulo, texto (**negrito**)            -> "Dica rápida"
  sabia     : numero, unidade?, texto, fonte                -> "Você sabia?"
  mito      : afirmacao, resposta ("MITO"/"VERDADE"), explicacao, fonte
  post_feed : post (caminho do PNG do post em arte/), titulo  -> chama para um post já publicado
  alerta    : foto?, prazo, titulo, texto                   -> "Fique de olho no prazo"
  termo     : termo, significado                            -> "Juridiquês do dia"
Zona segura: nada importante acima de y=250 nem abaixo de y=1670 (interface do Instagram)."""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVY=(33,41,59); TERRA=(157,87,76); BG=(246,241,234); TXT=(62,66,78); BEIGE=(235,227,217); WHITE=(255,255,255); ROSE=(214,150,138)
W, H, M = 1080, 1920, 96
TOP, BOT = 250, 1670

def sans(w, s): return ImageFont.truetype(f"{R}/fontes/Poppins-{w}.ttf", s)
def serif(s, w="Bold"):
    f = ImageFont.truetype(f"{R}/fontes/Lora-Variable.ttf", s)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
def wrap(d, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out
def lines(d, x, y, text, font, maxw, fill, lh, center=False):
    for l in wrap(d, text, font, maxw):
        xx = (W - d.textlength(l, font=font)) / 2 if center else x
        d.text((xx, y), l, font=font, fill=fill); y += lh
    return y
def rich(d, x, y, text, size, maxw, color=TXT, bold=NAVY, lh=1.45):
    fr, fb = sans("Regular", size), sans("Bold", size)
    toks = []
    for i, part in enumerate(re.split(r"\*\*", text)):
        for w in part.split(): toks.append((w, i % 2 == 1))
    sp = d.textlength(" ", font=fr); cx = x; step = int(size * lh)
    for w, b in toks:
        f = fb if b else fr; tw = d.textlength(w, font=f)
        punct = w[0] in ",.;:)?!" and cx > x
        if punct: cx -= sp
        if cx > x and cx + tw > x + maxw and not punct: cx = x; y += step
        d.text((cx, y), w, font=f, fill=bold if b else color); cx += tw + sp
    return y + step
def foto(path, w, h, crop_y=None):
    im = Image.open(f"{R}/{path}").convert("RGB")
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    oy = int((im.height - h) * (0.4 if crop_y is None else crop_y)); ox = (im.width - w) // 2
    return im.crop((ox, oy, ox + w, oy + h))
def rmask(size, r):
    m = Image.new("L", size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0], size[1]), radius=r, fill=255); return m
def fade(im, y0, y1, color=NAVY, top_dark=True):
    arr = np.array(im, dtype=np.float32); ys = np.arange(H)
    g = np.clip((ys - y0) / max(1, y1 - y0), 0, 1)
    if top_dark: g = np.maximum(g, np.clip(1 - ys / 380, 0, 1) * 0.65)
    g = g[:, None, None]; arr = arr * (1 - g) + np.array(color) * g
    return Image.fromarray(arr.astype("uint8"))
def marca(d, dark, y=TOP + 10):
    c = BEIGE if dark else NAVY
    d.text((M, y), "CAIO MACHADO", font=sans("Medium", 30), fill=c); d.text((M, y + 38), "ADVOCACIA", font=sans("Light", 20), fill=c)
def etiqueta(d, txt, y=TOP + 14, cor=TERRA):
    f = sans("Medium", 24); tw = d.textlength(txt, font=f)
    d.rounded_rectangle((W - M - tw - 44, y, W - M, y + 50), radius=25, fill=cor); d.text((W - M - tw - 22, y + 9), txt, font=f, fill=WHITE)
def rodape(d, dark, txt="Ficou com dúvida? Me chama no direct!"):
    c = BEIGE if dark else NAVY
    d.line((M, BOT - 90, W - M, BOT - 90), fill=TERRA, width=3)
    f = sans("Medium", 32); d.text((M, BOT - 66), txt, font=f, fill=c)
    f2 = sans("Bold", 32); t = "@adv.caiomachado"; d.text((M, BOT - 20), t, font=f2, fill=ROSE if dark else TERRA)
def base(dark): im = Image.new("RGB", (W, H), NAVY if dark else BG); return im, ImageDraw.Draw(im)

def dica(s, k):
    im, d = base(True)
    im.paste(foto(s["foto"], W, 1100, s.get("crop_y")), (0, 0)); im = fade(im, 520, 1080); d = ImageDraw.Draw(im)
    marca(d, True); etiqueta(d, "DICA RÁPIDA")
    y = 980; d.text((M, y), (k or "").upper(), font=sans("Medium", 26), fill=ROSE); y += 56
    y = lines(d, M, y, s["titulo"], serif(76), W - 2 * M, WHITE, 90) + 24
    y = rich(d, M, y, s["texto"], 40, W - 2 * M, color=BEIGE, bold=WHITE)
    assert y < BOT - 110, f"dica estoura {y}"
    rodape(d, True); return im
def sabia(s, k):
    im, d = base(False); marca(d, False); etiqueta(d, "VOCÊ SABIA?")
    y = 560; d.text((M, y), (k or "").upper(), font=sans("Medium", 26), fill=TERRA); y += 40
    fN = serif(330); d.text((M - 14, y), s["numero"], font=fN, fill=NAVY); nw = d.textlength(s["numero"], font=fN)
    if s.get("unidade"): d.text((M + nw + 16, y + 200), s["unidade"], font=serif(90), fill=TERRA)
    y += 440; d.line((M, y, M + 120, y), fill=TERRA, width=5); y += 50
    y = rich(d, M, y, s["texto"], 46, W - 2 * M) + 20
    d.text((M, y), s["fonte"], font=sans("Medium", 30), fill=TERRA); y += 50
    assert y < BOT - 110, f"sabia estoura {y}"
    rodape(d, False); return im
def mito(s, k):
    im, d = base(True); marca(d, True); etiqueta(d, "MITO OU VERDADE?")
    y = 460; d.text((M, y), (k or "").upper(), font=sans("Medium", 26), fill=ROSE); y += 60
    f = serif(60, "Regular"); ls = wrap(d, "“" + s["afirmacao"] + "”", f, W - 2 * M - 80); h = len(ls) * 76 + 80
    d.rounded_rectangle((M, y, W - M, y + h), radius=36, fill=WHITE); yy = y + 40
    for l in ls: d.text((M + 40, yy), l, font=f, fill=NAVY); yy += 76
    y += h + 70
    cor = (46, 110, 78) if s["resposta"].upper() == "VERDADE" else TERRA
    fr = serif(120); tw = d.textlength(s["resposta"].upper(), font=fr)
    d.rounded_rectangle((M, y, M + tw + 80, y + 170), radius=30, fill=cor); d.text((M + 40, y + 10), s["resposta"].upper(), font=fr, fill=WHITE)
    y += 220; y = rich(d, M, y, s["explicacao"], 42, W - 2 * M, color=BEIGE, bold=WHITE) + 10
    d.text((M, y), s["fonte"], font=sans("Medium", 30), fill=ROSE); y += 50
    assert y < BOT - 110, f"mito estoura {y}"
    rodape(d, True); return im
def post_feed(s, k):
    im, d = base(True); marca(d, True); etiqueta(d, "TEM POST NO FEED")
    y = 380; y = lines(d, M, y, s["titulo"], serif(62), W - 2 * M, WHITE, 76) + 36
    p = Image.open(f"{R}/{s['post']}").convert("RGB"); pw = 640; ph = int(p.height * pw / p.width)
    p = p.resize((pw, ph), Image.LANCZOS); x = (W - pw) // 2
    sh = Image.new("RGB", (pw, ph), (15, 20, 30)); im.paste(sh, (x + 14, y + 18), rmask((pw, ph), 34))
    im.paste(p, (x, y), rmask((pw, ph), 34)); d = ImageDraw.Draw(im); y += ph + 50
    t = "Toque no meu perfil e confira"; f = sans("Medium", 36)
    d.rounded_rectangle(((W - d.textlength(t, font=f)) / 2 - 36, y, (W + d.textlength(t, font=f)) / 2 + 36, y + 80), radius=40, fill=TERRA)
    d.text(((W - d.textlength(t, font=f)) / 2, y + 16), t, font=f, fill=WHITE); y += 80
    assert y < BOT - 110, f"post_feed estoura {y}"
    rodape(d, True); return im
def alerta(s, k):
    im, d = base(True)
    if s.get("foto"): im.paste(foto(s["foto"], W, 900, s.get("crop_y")), (0, 0)); im = fade(im, 380, 880); d = ImageDraw.Draw(im)
    marca(d, True); etiqueta(d, "FIQUE DE OLHO", cor=(190, 120, 40))
    y = 820 if s.get("foto") else 520; d.text((M, y), (k or "").upper(), font=sans("Medium", 26), fill=ROSE); y += 50
    d.rounded_rectangle((M, y, W - M, y + 150), radius=26, fill=BEIGE)
    fp = serif(78); d.text(((W - d.textlength(s["prazo"], font=fp)) / 2, y + 26), s["prazo"], font=fp, fill=NAVY); y += 200
    y = lines(d, M, y, s["titulo"], serif(64), W - 2 * M, WHITE, 78) + 20
    y = rich(d, M, y, s["texto"], 40, W - 2 * M, color=BEIGE, bold=WHITE)
    assert y < BOT - 110, f"alerta estoura {y}"
    rodape(d, True); return im
def termo(s, k):
    im, d = base(False); marca(d, False); etiqueta(d, "JURIDIQUÊS DO DIA")
    y = 600; d.text((M, y), (k or "").upper(), font=sans("Medium", 26), fill=TERRA); y += 60
    y = lines(d, M, y, s["termo"], serif(110), W - 2 * M, NAVY, 124) + 30
    d.line((M, y, M + 120, y), fill=TERRA, width=5); y += 60
    d.text((M, y), "Em bom português:", font=sans("Bold", 36), fill=TERRA); y += 70
    y = lines(d, M, y, s["significado"], serif(58, "Regular"), W - 2 * M, NAVY, 76)
    assert y < BOT - 110, f"termo estoura {y}"
    rodape(d, False); return im

ESTILOS = dict(dica=dica, sabia=sabia, mito=mito, post_feed=post_feed, alerta=alerta, termo=termo)
def make(sp):
    os.makedirs(f"{R}/arte", exist_ok=True); out = []
    for i, s in enumerate(sp["stories"], 1):
        im = ESTILOS[s["estilo"]](s, s.get("kicker", sp.get("kicker")))
        fn = f"{R}/arte/{sp['arquivo']}-{i:02d}.jpg"; im.convert("RGB").save(fn, "JPEG", quality=92); out.append(fn)
    print("\n".join(out))

if __name__ == "__main__": make(json.load(open(sys.argv[1])))
