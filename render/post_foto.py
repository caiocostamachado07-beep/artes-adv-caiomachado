#!/usr/bin/env python3
"""Gera o post foto 1080x1350 do @adv.caiomachado.
Uso: python3 render/post_foto.py spec.json   (spec com 'arquivo','foto','kicker','l1','l2','pill','bullets', opcional 'crop_y')
Saída: arte/<arquivo>.png"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVY=(33,41,59); TERRA=(157,87,76); BEIGE=(235,227,217); WHITE=(255,255,255)
W,H=1080,1350
def sans(w,s): return ImageFont.truetype(f"{R}/fontes/Poppins-{w}.ttf",s)
def serif(s):
    f=ImageFont.truetype(f"{R}/fontes/Lora-Variable.ttf",s); f.set_variation_by_name("Bold"); return f
def make(sp):
    im=Image.open(f"{R}/{sp['foto']}" if sp['foto'].startswith('banco/') else f"{R}/fotos/{sp['foto']}").convert("RGB")
    s=W/im.width; im=im.resize((W,int(im.height*s)),Image.LANCZOS)
    cy0=sp.get("crop_y",0); im=im.crop((0,cy0,W,cy0+H))
    ys=np.arange(H)
    t=np.clip((ys-H*0.22)/(H*0.32),0,1); g=t*t*(3-2*t)
    top=np.clip(1-ys/(H*0.16),0,1)*0.8
    a=np.clip(np.maximum(g,top),0,0.985)[:,None]*np.ones((1,W))
    arr=np.array(im,dtype=np.float32)*(1-a[...,None])+np.array(NAVY,dtype=np.float32)*a[...,None]
    im=Image.fromarray(arr.astype("uint8")).convert("RGBA"); d=ImageDraw.Draw(im)
    d.text((64,56),"CAIO MACHADO",font=sans("Medium",26),fill=WHITE)
    d.text((64,90),"ADVOCACIA",font=sans("Light",20),fill=BEIGE)
    kf=sans("Medium",22); kw=d.textlength(sp["kicker"],font=kf)
    d.rounded_rectangle((W-64-kw-44,58,W-64,108),radius=25,fill=TERRA)
    d.text((W-64-kw-22,69),sp["kicker"],font=kf,fill=WHITE)
    y=560
    d.text((64,y),sp["l1"],font=serif(72),fill=WHITE)
    d.text((58,y+84),sp["l2"],font=serif(150),fill=BEIGE)
    pf=sans("Medium",42); tw=d.textlength(sp["pill"],font=pf); py=y+84+215
    d.rounded_rectangle((64,py,64+tw+76,py+82),radius=41,fill=TERRA)
    d.text((102,py+13),sp["pill"],font=pf,fill=WHITE)
    cy=py+82+34; ch=1234-cy
    card=Image.new("RGBA",(W,H),(0,0,0,0)); cd=ImageDraw.Draw(card)
    cd.rounded_rectangle((64,cy,W-64,cy+ch),radius=28,fill=(255,255,255,22),outline=(235,227,217,90),width=2)
    im=Image.alpha_composite(im,card); d=ImageDraw.Draw(im)
    d.text((100,cy+26),"FIQUE ATENTO",font=sans("Bold",26),fill=(214,150,138))
    by=cy+74
    for b in sp["bullets"]:
        d.ellipse((102,by+13,114,by+25),fill=TERRA); d.text((136,by),b,font=sans("Regular",30),fill=WHITE); by+=50
    d.line((64,1268,W-64,1268),fill=TERRA,width=3)
    ff=sans("Medium",29)
    d.text((64,1288),"Ficou com dúvida? Fale comigo!",font=ff,fill=BEIGE)
    t="@adv.caiomachado"; d.text((W-64-d.textlength(t,font=ff),1288),t,font=ff,fill=BEIGE)
    os.makedirs(f"{R}/arte",exist_ok=True)
    out=f"{R}/arte/{sp['arquivo']}.png"; im.convert("RGB").save(out); print(out)
if __name__=="__main__":
    make(json.load(open(sys.argv[1])))
