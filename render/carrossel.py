#!/usr/bin/env python3
"""Gera carrossel 1080x1350 do @adv.caiomachado a partir de um JSON.
Uso: python3 render/carrossel.py spec.json  ->  arte/<arquivo>-01.png ... -NN.png
Spec: arquivo, kicker, capa{foto,l1,l2,pill}, paginas[{destaque,titulo,itens[],nota?}], final{foto,l1,l2,sub}"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVY=(33,41,59); NAVY2=(44,54,76); TERRA=(157,87,76); BEIGE=(235,227,217); WHITE=(255,255,255); ROSE=(214,150,138)
W,H=1080,1350; M=64
def sans(w,s): return ImageFont.truetype(f"{R}/fontes/Poppins-{w}.ttf",s)
def serif(s):
    f=ImageFont.truetype(f"{R}/fontes/Lora-Variable.ttf",s); f.set_variation_by_name("Bold"); return f
def wrap(d,text,font,maxw):
    lines=[];cur=""
    for w in text.split():
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur);cur=w
    if cur: lines.append(cur)
    return lines
def photo_bg(foto,crop_y=0,strength=1.0):
    im=Image.open(f"{R}/fotos/{foto}").convert("RGB")
    s=W/im.width; im=im.resize((W,int(im.height*s)),Image.LANCZOS); im=im.crop((0,crop_y,W,crop_y+H))
    ys=np.arange(H); t=np.clip((ys-H*0.22)/(H*0.32),0,1); g=t*t*(3-2*t)
    top=np.clip(1-ys/(H*0.16),0,1)*0.8
    a=np.clip(np.maximum(g,top),0,0.985)[:,None]*np.ones((1,W))
    arr=np.array(im,dtype=np.float32)*(1-a[...,None])+np.array(NAVY,dtype=np.float32)*a[...,None]
    return Image.fromarray(arr.astype("uint8")).convert("RGBA")
def header(d,kicker=None,num=None,total=None):
    d.text((M,56),"CAIO MACHADO",font=sans("Medium",26),fill=WHITE)
    d.text((M,90),"ADVOCACIA",font=sans("Light",20),fill=BEIGE)
    if kicker:
        kf=sans("Medium",22); kw=d.textlength(kicker,font=kf)
        d.rounded_rectangle((W-M-kw-44,58,W-M,108),radius=25,fill=TERRA); d.text((W-M-kw-22,69),kicker,font=kf,fill=WHITE)
    if num:
        t=f"{num}/{total}"; f=sans("Medium",26); d.text((W-M-d.textlength(t,font=f),66),t,font=f,fill=BEIGE)
def arrow(d,x,y,c=BEIGE,w=3,L=40):
    d.line((x,y,x+L,y),fill=c,width=w); d.line((x+L-14,y-12,x+L,y),fill=c,width=w); d.line((x+L-14,y+12,x+L,y),fill=c,width=w)
def footer(d,left,right="@adv.caiomachado"):
    d.line((M,1268,W-M,1268),fill=TERRA,width=3); ff=sans("Medium",29)
    ar=left.endswith("→"); left=left.rstrip(" →")
    d.text((M,1288),left,font=ff,fill=BEIGE)
    if ar: arrow(d,M+d.textlength(left,font=ff)+16,1288+22)
    if right: d.text((W-M-d.textlength(right,font=ff),1288),right,font=ff,fill=BEIGE)
def capa(sp,total):
    c=sp["capa"]; im=photo_bg(c["foto"],c.get("crop_y",0)); d=ImageDraw.Draw(im)
    header(d,sp["kicker"])
    y=560; d.text((M,y),c["l1"],font=serif(72),fill=WHITE); d.text((M-6,y+84),c["l2"],font=serif(150),fill=BEIGE)
    pf=sans("Medium",42); tw=d.textlength(c["pill"],font=pf); py=y+84+215
    d.rounded_rectangle((M,py,M+tw+76,py+82),radius=41,fill=TERRA); d.text((M+38,py+13),c["pill"],font=pf,fill=WHITE)
    # chip "arraste"
    footer(d,"Arraste para o lado →")
    return im.convert("RGB")
def pagina(p,num,total,kicker):
    im=Image.new("RGBA",(W,H),NAVY+(255,)); d=ImageDraw.Draw(im)
    # faixa decorativa sutil
    d.rectangle((0,0,W,6),fill=TERRA)
    header(d,None,num,total)
    y=190
    if p.get("destaque"):
        f=serif(210); d.text((M-4,y),p["destaque"],font=f,fill=TERRA); y+=290
    tf=serif(68)
    for ln in wrap(d,p["titulo"],tf,W-2*M):
        d.text((M,y),ln,font=tf,fill=BEIGE); y+=86
    y+=24
    itf=sans("Regular",40); lh=58
    for it in p["itens"]:
        lines=wrap(d,it,itf,W-2*M-150)
        h=len(lines)*lh+64
        card=Image.new("RGBA",(W,H),(0,0,0,0)); cd=ImageDraw.Draw(card)
        cd.rounded_rectangle((M,y,W-M,y+h),radius=28,fill=(255,255,255,22),outline=(235,227,217,90),width=2)
        im=Image.alpha_composite(im,card); d=ImageDraw.Draw(im)
        d.ellipse((M+34,y+h/2-9,M+52,y+h/2+9),fill=TERRA)
        ty=y+30
        for ln in lines: d.text((M+84,ty),ln,font=itf,fill=WHITE); ty+=lh
        y+=h+28
    if p.get("nota"):
        nf=sans("Medium",30)
        nl=wrap(d,p["nota"],nf,W-2*M-70); nh=len(nl)*44+48
        d.rounded_rectangle((M,y+6,W-M,y+6+nh),radius=28,fill=TERRA)
        ty=y+6+24
        for ln in nl: d.text((M+35,ty),ln,font=nf,fill=WHITE); ty+=44
        y+=nh+6
    assert y<1250,f"página {num} estoura a altura: y={y}"
    footer(d,"Arraste para o lado  →" if num<total else "Ficou com dúvida? Fale comigo!")
    return im.convert("RGB")
def final(sp,num,total):
    f=sp["final"]; im=photo_bg(f["foto"],f.get("crop_y",0)); d=ImageDraw.Draw(im); header(d,None,num,total)
    y=560; d.text((M,y),f["l1"],font=serif(72),fill=WHITE); d.text((M-6,y+84),f["l2"],font=serif(150),fill=BEIGE)
    sf=sans("Medium",42); py=y+84+215
    for ln in wrap(d,f["sub"],sf,W-2*M): d.text((M,py),ln,font=sf,fill=WHITE); py+=62
    pf=sans("Medium",36); t="Salve e envie para quem precisa"; tw=d.textlength(t,font=pf)
    d.rounded_rectangle((M,py+24,M+tw+68,py+24+74),radius=37,fill=TERRA); d.text((M+34,py+24+13),t,font=pf,fill=WHITE)
    footer(d,"Ficou com dúvida? Fale comigo!")
    return im.convert("RGB")
def make(sp):
    n=len(sp["paginas"])+2; os.makedirs(f"{R}/arte",exist_ok=True); out=[]
    imgs=[capa(sp,n)]+[pagina(p,i+2,n,sp["kicker"]) for i,p in enumerate(sp["paginas"])]+[final(sp,n,n)]
    for i,im in enumerate(imgs,1):
        fn=f"{R}/arte/{sp['arquivo']}-{i:02d}.png"; im.save(fn); out.append(fn)
    print("\n".join(out))
if __name__=="__main__": make(json.load(open(sys.argv[1])))
