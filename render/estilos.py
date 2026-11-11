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
        im = ESTILOS[t["estilo"]](t, t.get("kicker", sp.get("kicker")))
        fn = f"{R}/arte/{sp['arquivo']}-{i:02d}.png"; im.save(fn); out.append(fn)
    print("\n".join(out))

# ---------- estilos extras (amostras 11/11/2026) ----------
def timeline(t, k):
    im, d = base(False); header(d, False, k)
    y = lines(d, M, 160, t["titulo"], serif(58), W - 2 * M, NAVY, 72) + 40
    x0 = M + 30; dots = []
    for i, (marco, txt) in enumerate(t["marcos"]):
        dots.append(y)
        d.text((x0 + 50, y - 2), marco, font=serif(44), fill=TERRA)
        y = rich(d, x0 + 50, y + 60, txt, 34, W - 2 * M - 110) + 40
    d.line((x0, dots[0] + 22, x0, dots[-1] + 22), fill=(214, 200, 186), width=4)
    for i, dy in enumerate(dots):
        d.ellipse((x0 - 20, dy + 2, x0 + 20, dy + 42), fill=TERRA if i < len(dots) - 1 else NAVY, outline=BG, width=4)
    assert y < 1240, f"timeline estoura {y}"
    footer(d, False); return im
def certo_errado(t, k):
    im, d = base(False); header(d, False, k)
    y = lines(d, M, 160, t["titulo"], serif(56), W - 2 * M, NAVY, 70) + 30
    cw = (W - 2 * M - 30) // 2
    for col, (lab, cor, itens, sim) in enumerate((("FAÇA ASSIM", (46, 110, 78), t["certo"], "✓"), ("EVITE", TERRA, t["errado"], "✕"))):
        x = M + col * (cw + 30)
        fi = sans("Regular", 32); hh = 120 + sum(len(wrap(d, it, fi, cw - 100)) * 46 + 34 for it in itens) + 10
        hh = max(hh, 120 + max(sum(len(wrap(d, it, fi, cw - 100)) * 46 + 34 for it in L) for L in (t["certo"], t["errado"])) + 10)
        d.rounded_rectangle((x, y, x + cw, y + hh), radius=28, fill=WHITE, outline=(225, 215, 203), width=2)
        d.rounded_rectangle((x + 24, y + 24, x + cw - 24, y + 84), radius=30, fill=cor)
        f = sans("Bold", 26); d.text((x + cw / 2 - d.textlength(lab, font=f) / 2, y + 38), lab, font=f, fill=WHITE)
        iy = y + 120
        for it in itens:
            if sim == "✓":
                d.line((x + 28, iy + 22, x + 38, iy + 34), fill=cor, width=6); d.line((x + 38, iy + 34, x + 58, iy + 8), fill=cor, width=6)
            else:
                d.line((x + 30, iy + 8, x + 56, iy + 34), fill=cor, width=6); d.line((x + 56, iy + 8, x + 30, iy + 34), fill=cor, width=6)
            iy = lines(d, x + 76, iy, it, sans("Regular", 32), cw - 100, TXT, 46) + 34
        assert iy < 1215, f"certo_errado estoura {iy}"
    footer(d, False); return im
def pergunta(t, k):
    im, d = base(True); header(d, True, k)
    d.text((M, 150), "ME PERGUNTARAM", font=sans("Bold", 28), fill=ROSE)
    f = sans("Medium", 40); ls = wrap(d, t["pergunta"], f, W - 2 * M - 80); h = len(ls) * 56 + 70
    d.rounded_rectangle((M, 210, W - M, 210 + h), radius=36, fill=WHITE)
    d.polygon([(M + 60, 210 + h - 2), (M + 120, 210 + h - 2), (M + 50, 210 + h + 50)], fill=WHITE)
    yy = 245
    for l in ls: d.text((M + 40, yy), l, font=f, fill=NAVY); yy += 56
    y = 210 + h + 100
    d.text((M, y), "MINHA RESPOSTA", font=sans("Bold", 28), fill=ROSE); y += 60
    y = lines(d, M, y, t["resposta_curta"], serif(64), W - 2 * M, BEIGE, 78) + 20
    y = rich(d, M, y, t["resposta"], 38, W - 2 * M, color=BEIGE, bold=WHITE)
    assert y < 1240, f"pergunta estoura {y}"
    footer(d, True, "Mande a sua pergunta no direct!"); return im
def juridiques(t, k):
    im, d = base(False); header(d, False, k)
    d.text((M, 200), "JURIDIQUÊS TRADUZIDO", font=sans("Bold", 28), fill=TERRA)
    y = lines(d, M, 260, t["termo"], serif(96), W - 2 * M, NAVY, 108) + 10
    d.text((M, y), t.get("classe", "expressão jurídica"), font=serif(34, "Regular"), fill=TXT); y += 70
    d.line((M, y, M + 110, y), fill=TERRA, width=4); y += 50
    d.text((M, y), "Em bom português:", font=sans("Bold", 30), fill=TERRA); y += 56
    y = lines(d, M, y, t["significado"], serif(48, "Regular"), W - 2 * M, NAVY, 64) + 30
    if t.get("exemplo"):
        d.rounded_rectangle((M, y, W - M, y + 10), radius=5, fill=BG)
        y = rich(d, M, y, "**Exemplo:** " + t["exemplo"], 32, W - 2 * M)
    assert y < 1240, f"juridiques estoura {y}"
    footer(d, False); return im
def tabela(t, k):
    im, d = base(False); header(d, False, k)
    y = lines(d, M, 160, t["titulo"], serif(54), W - 2 * M, NAVY, 68) + 10
    if t.get("sub"): y = lines(d, M, y, t["sub"], sans("Regular", 30), W - 2 * M, TXT, 42) + 20
    c1 = M + 40; c2 = W // 2 + 60; rh = 74
    d.rounded_rectangle((M, y, W - M, y + rh), radius=18, fill=NAVY)
    hf = sans("Bold", 28); d.text((c1, y + 22), t["colunas"][0].upper(), font=hf, fill=BEIGE); d.text((c2, y + 22), t["colunas"][1].upper(), font=hf, fill=BEIGE)
    y += rh + 6
    for i, (a, b) in enumerate(t["linhas"]):
        if i % 2 == 0: d.rounded_rectangle((M, y, W - M, y + rh), radius=14, fill=WHITE)
        d.text((c1, y + 20), a, font=sans("Regular", 32), fill=TXT); d.text((c2, y + 18), b, font=sans("Bold", 34), fill=TERRA)
        y += rh
    y += 20
    if t.get("nota"): y = lines(d, M, y, t["nota"], sans("Medium", 26), W - 2 * M, TXT, 38)
    assert y < 1240, f"tabela estoura {y}"
    footer(d, False); return im
def mudou_lei(t, k):
    im, d = base(True)
    if t.get("foto"):
        ph = foto(t["foto"], W, 600, t.get("crop_y")); im.paste(ph, (0, 0))
        ys = np.arange(600); g = np.maximum(np.clip((ys - 150) / 450, 0, 1), np.clip(1 - ys / 190, 0, 1) * 0.7)[:, None, None]
        arr = np.array(im, dtype=np.float32); arr[:600] = arr[:600] * (1 - g) + np.array(NAVY) * g; im = Image.fromarray(arr.astype("uint8")); d = ImageDraw.Draw(im)
    header(d, True, k)
    d.rectangle((0, 470, W, 560), fill=TERRA); f = sans("Bold", 46); tx = t.get("selo", "MUDOU A LEI")
    d.text((M, 486), tx, font=f, fill=WHITE); d.text((W - M - d.textlength(t["data"], font=sans("Medium", 30)), 500), t["data"], font=sans("Medium", 30), fill=WHITE)
    y = 610; y = lines(d, M, y, t["manchete"], serif(64), W - 2 * M, WHITE, 78) + 20
    y = rich(d, M, y, t["texto"], 34, W - 2 * M, color=BEIGE, bold=WHITE)
    assert y < 1240, f"mudou_lei estoura {y}"
    footer(d, True); return im
def fluxo(t, k):
    im, d = base(False); header(d, False, k)
    y = lines(d, M, 160, t["titulo"], serif(60), W - 2 * M, NAVY, 74) + 40
    bx0, bx1 = M, W - M - 250; cx = (bx0 + bx1) // 2
    for perg, nao in t["passos"]:
        f = sans("Medium", 36); ls = wrap(d, perg, f, bx1 - bx0 - 60); h = len(ls) * 50 + 50
        d.rounded_rectangle((bx0, y, bx1, y + h), radius=26, fill=WHITE, outline=NAVY, width=3)
        yy = y + 25
        for l in ls: d.text((cx - d.textlength(l, font=f) / 2, yy), l, font=f, fill=NAVY); yy += 50
        # saída "Não" à direita
        d.line((bx1, y + h // 2, bx1 + 40, y + h // 2), fill=TERRA, width=4)
        d.rounded_rectangle((bx1 + 40, y + h // 2 - 70, W - M, y + h // 2 + 80), radius=20, fill=(240, 226, 220))
        d.text((bx1 + 60, y + h // 2 - 58), "Não", font=sans("Bold", 28), fill=TERRA)
        ny = y + h // 2 - 18
        for l in wrap(d, nao, sans("Regular", 24), 170): d.text((bx1 + 60, ny), l, font=sans("Regular", 24), fill=TXT); ny += 30
        y += h
        d.line((cx, y, cx, y + 70), fill=(46, 110, 78), width=5); d.polygon([(cx - 14, y + 58), (cx + 14, y + 58), (cx, y + 78)], fill=(46, 110, 78))
        d.text((cx + 24, y + 18), "Sim", font=sans("Bold", 30), fill=(46, 110, 78)); y += 86
    f = sans("Bold", 38); ls = wrap(d, t["resultado"], f, W - 2 * M - 80); h = len(ls) * 52 + 56
    d.rounded_rectangle((M, y, W - M, y + h), radius=26, fill=NAVY)
    yy = y + 28
    for l in ls: d.text((W // 2 - d.textlength(l, font=f) / 2, yy), l, font=f, fill=BEIGE); yy += 52
    y += h
    assert y < 1240, f"fluxo estoura {y}"
    footer(d, False); return im
ESTILOS.update(timeline=timeline, certo_errado=certo_errado, pergunta=pergunta, juridiques=juridiques, tabela=tabela, mudou_lei=mudou_lei, fluxo=fluxo)

if __name__ == "__main__": make(json.load(open(sys.argv[1])))
