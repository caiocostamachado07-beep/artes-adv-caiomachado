#!/usr/bin/env python3
"""Carrossel no estilo editorial claro (fundo bege, títulos em pergunta, texto com **negrito**).
Uso: python3 render/carrossel_claro.py spec.json -> arte/<arquivo>-NN.png
Spec: arquivo, kicker,
  capa{foto, chamada, titulo, texto, cta, crop_x?, crop_y?},
  paginas[{titulo, sub?, paragrafos[] (use **negrito** e "• " para tópicos)}],
  final{foto, l1, l2, texto, crop_x?}"""
import json, os, re, sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVY=(33,41,59); TERRA=(157,87,76); BG=(246,241,234); TXT=(62,66,78); BEIGE=(235,227,217)
W,H=1080,1350; M=96
def sans(w,s): return ImageFont.truetype(f"{R}/fontes/Poppins-{w}.ttf",s)
def serif(s,w="Bold"):
    f=ImageFont.truetype(f"{R}/fontes/Lora-Variable.ttf",s); f.set_variation_by_name(w); return f
def wrap(d,text,font,maxw):
    lines=[];cur=""
    for w in text.split():
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur);cur=w
    if cur: lines.append(cur)
    return lines
def rich(d,x,y,text,size,maxw,color=TXT,bold=NAVY,lh=1.45):
    """Escreve parágrafo com **negrito**; retorna y final."""
    fr,fb=sans("Regular",size),sans("SemiBold",size) if os.path.exists(f"{R}/fontes/Poppins-SemiBold.ttf") else sans("Bold",size)
    toks=[]
    for i,part in enumerate(re.split(r"\*\*",text)):
        for w in part.split(): toks.append((w,i%2==1))
    sp=d.textlength(" ",font=fr); cx=x; step=int(size*lh)
    for w,b in toks:
        f=fb if b else fr; tw=d.textlength(w,font=f)
        if w[0] in ",.;:)" and cx>x: cx-=sp
        if cx>x and cx+tw>x+maxw: cx=x; y+=step
        d.text((cx,y),w,font=f,fill=bold if b else color); cx+=tw+sp
    return y+step
def rule(d,x,y,L=120): d.line((x,y,x+L,y),fill=TERRA,width=4)
def marca(d,y,cx=W//2):
    f=serif(40); t="CAIO MACHADO"; d.text((cx-d.textlength(t,font=f)/2,y),t,font=f,fill=NAVY)
    d.line((cx-150,y+58,cx+150,y+58),fill=TERRA,width=2)
    f2=sans("Regular",20); t2="A D V O C A C I A"; d.text((cx-d.textlength(t2,font=f2)/2,y+70),t2,font=f2,fill=TXT)
def contador(d,num,total):
    t=f"{num}/{total}"; f=sans("Medium",28); tw=d.textlength(t,font=f)
    d.rounded_rectangle((W-60-tw-44,54,W-60,108),radius=27,fill=NAVY); d.text((W-60-tw-22,62),t,font=f,fill=BEIGE)
def kick(d,k): d.text((M,68),k,font=sans("Medium",24),fill=TERRA)
def rodape(d):
    rule(d,W-M-120,1110); marca(d,1170)
def foto_fade(foto,box,crop_x=0.5,crop_y=0.5,fade="left",fade_w=0.45,zoom=1.0):
    x0,y0,x1,y1=box; bw,bh=x1-x0,y1-y0
    im=Image.open(f"{R}/{foto}" if foto.startswith("banco/") else f"{R}/fotos/{foto}").convert("RGB")
    s=max(bw/im.width,bh/im.height)*zoom; im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    ox=int((im.width-bw)*crop_x); oy=int((im.height-bh)*crop_y); im=im.crop((ox,oy,ox+bw,oy+bh))
    xs=np.arange(bw)/bw; ys=np.arange(bh)/bh
    def sm(t): t=np.clip(t,0,1); return t*t*(3-2*t)
    ax=sm(xs/fade_w) if "left" in fade else np.ones(bw)
    ay=sm(ys/0.35) if "top" in fade else np.ones(bh)
    a=(ay[:,None]*ax[None,:])
    if "bottom" in fade: a=a*sm((1-ys)/0.12)[:,None]
    return im,Image.fromarray((a*255).astype("uint8"),"L")
def base(): im=Image.new("RGB",(W,H),BG); return im,ImageDraw.Draw(im)
def capa(sp,total):
    c=sp["capa"]; im,d=base()
    ph,mk=foto_fade(c["foto"],(400,720,W,H),c.get("crop_x",0.5),c.get("crop_y",0.5),fade="left top",fade_w=0.35)
    im.paste(ph,(400,720),mk); d=ImageDraw.Draw(im)
    marca(d,60); contador(d,1,total)
    y=200; d.text((M,y),c["chamada"],font=serif(62),fill=TERRA); y+=92; rule(d,M,y); y+=34
    for l in c["titulo"].split("|"): d.text((M,y),l,font=serif(76),fill=NAVY); y+=92
    y+=20; y=rich(d,M,y,c["texto"],38,W-2*M)
    assert y<730,y
    y=790; rule(d,M,y); y+=34
    for l in wrap(d,c["cta"],serif(42),300): d.text((M,y),l,font=serif(42),fill=TERRA); y+=54
    y+=26; d.rounded_rectangle((M,y,M+100,y+22),radius=11,outline=NAVY,width=3)
    d.line((M+15,y+11,M+82,y+11),fill=NAVY,width=3); d.line((M+72,y+3,M+84,y+11),fill=NAVY,width=3); d.line((M+72,y+19,M+84,y+11),fill=NAVY,width=3)
    return im
def pagina(p,num,total,k):
    im,d=base(); kick(d,k); contador(d,num,total)
    y=200
    for l in wrap(d,p["titulo"],serif(66),W-2*M): d.text((M,y),l,font=serif(66),fill=NAVY); y+=82
    y+=40; rule(d,M,y); y+=70
    if p.get("sub"): d.text((M,y),p["sub"],font=serif(46),fill=NAVY); y+=86
    for par in p["paragrafos"]:
        if par.startswith("• "):
            d.ellipse((M+38,y+22,M+50,y+34),fill=TERRA); y=rich(d,M+76,y,par[2:],41,W-2*M-90)+14
        else: y=rich(d,M+30,y,par,42,W-2*M-50)+40
    assert y<1100,f"página {num} estoura: y={y}"
    rodape(d); return im
def final(sp,num,total):
    f=sp["final"]; im,d=base()
    ph,mk=foto_fade(f["foto"],(500,0,W,H),f.get("crop_x",0.5),f.get("crop_y",0.2),fade="left",fade_w=0.4,zoom=1.12)
    im.paste(ph,(500,0),mk); d=ImageDraw.Draw(im); contador(d,num,total)
    y=520; d.text((M,y),f["l1"],font=serif(50),fill=TERRA); y+=76
    d.text((M,y),f["l2"],font=serif(76),fill=NAVY); y+=116; rule(d,M,y); y+=50
    for l in wrap(d,f["texto"],sans("Regular",36),400): d.text((M,y),l,font=sans("Regular",36),fill=TXT); y+=52
    y+=40; t="@adv.caiomachado"; ff=sans("Medium",34); tw=d.textlength(t,font=ff)
    d.rounded_rectangle((M,y,M+tw+60,y+70),radius=35,fill=NAVY); d.text((M+30,y+14),t,font=ff,fill=BEIGE)
    marca(d,1170,cx=M+170)
    return im
def make(sp):
    total=len(sp["paginas"])+2; out=[]
    out.append(capa(sp,total))
    for i,p in enumerate(sp["paginas"]): out.append(pagina(p,i+2,total,sp["kicker"]))
    out.append(final(sp,total,total))
    os.makedirs(f"{R}/arte",exist_ok=True)
    for i,im in enumerate(out,1):
        fn=f"{R}/arte/{sp['arquivo']}-{i:02d}.png"; im.save(fn); print(fn)
if __name__=="__main__": make(json.load(open(sys.argv[1])))
