#!/usr/bin/env python3
"""Gera Reels 1080x1920 (MP4, mudo, texto animado) do @adv.caiomachado a partir de um JSON.
Uso: python3 render/reels.py spec.json -> reels/<arquivo>.mp4 (+ quadros em /tmp)
Spec igual ao do carrossel: arquivo, kicker, capa{foto,l1,l2,pill}, paginas[{destaque,titulo,itens[],nota?}], final{foto,l1,l2,sub}
Opcional: seg_capa, seg_pagina, seg_final (segundos por tela)."""
import json, os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import carrossel as c
from PIL import Image
import numpy as np
W,HH=1080,1920; M=64
from PIL import ImageDraw
def photo_bg(foto):
    im=Image.open(f"{c.R}/fotos/{foto}").convert("RGB")
    s=max(W/im.width,HH/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    x=(im.width-W)//2; im=im.crop((x,0,x+W,HH))
    ys=np.arange(HH); t=np.clip((ys-HH*0.30)/(HH*0.26),0,1); g=t*t*(3-2*t)
    top=np.clip(1-ys/(HH*0.12),0,1)*0.7
    a=np.clip(np.maximum(g,top),0,0.985)[:,None]*np.ones((1,W))
    arr=np.array(im,dtype=np.float32)*(1-a[...,None])+np.array(c.NAVY,dtype=np.float32)*a[...,None]
    return Image.fromarray(arr.astype("uint8")).convert("RGBA")
def head(d,kicker=None):
    d.text((M,170),"CAIO MACHADO",font=c.sans("Medium",28),fill=c.WHITE); d.text((M,206),"ADVOCACIA",font=c.sans("Light",21),fill=c.BEIGE)
    if kicker:
        kf=c.sans("Medium",23); kw=d.textlength(kicker,font=kf)
        d.rounded_rectangle((W-M-kw-44,172,W-M,224),radius=26,fill=c.TERRA); d.text((W-M-kw-22,184),kicker,font=kf,fill=c.WHITE)
def foot(d,left):
    d.line((M,1590,W-M,1590),fill=c.TERRA,width=3); ff=c.sans("Medium",30)
    d.text((M,1612),left,font=ff,fill=c.BEIGE); r="@adv.caiomachado"; d.text((W-M-d.textlength(r,font=ff),1612),r,font=ff,fill=c.BEIGE)
def f_capa(sp):
    k=sp["capa"]; im=photo_bg(k["foto"]); d=ImageDraw.Draw(im); head(d)
    kf=c.sans("Medium",26); kw=d.textlength(sp["kicker"],font=kf)
    d.rounded_rectangle((M,900,M+kw+44,954),radius=27,fill=c.TERRA); d.text((M+22,912),sp["kicker"],font=kf,fill=c.WHITE)
    y=1000; d.text((M,y),k["l1"],font=c.serif(76),fill=c.WHITE); d.text((M-6,y+90),k["l2"],font=c.serif(160),fill=c.BEIGE)
    pf=c.sans("Medium",44); tw=d.textlength(k["pill"],font=pf); py=y+90+230
    d.rounded_rectangle((M,py,M+tw+76,py+86),radius=43,fill=c.TERRA); d.text((M+38,py+14),k["pill"],font=pf,fill=c.WHITE)
    foot(d,"Fique até o final"); return im.convert("RGB")
def f_pag(p):
    im=Image.new("RGBA",(W,HH),c.NAVY+(255,)); d=ImageDraw.Draw(im); head(d)
    y=380
    if p.get("destaque"): d.text((M-4,y),p["destaque"],font=c.serif(230),fill=c.TERRA); y+=320
    tf=c.serif(76)
    for ln in c.wrap(d,p["titulo"],tf,W-2*M): d.text((M,y),ln,font=tf,fill=c.BEIGE); y+=96
    y+=34; itf=c.sans("Regular",46); lh=66
    for it in p["itens"]:
        lines=c.wrap(d,it,itf,W-2*M-150); h=len(lines)*lh+72
        card=Image.new("RGBA",(W,HH),(0,0,0,0)); cd=ImageDraw.Draw(card)
        cd.rounded_rectangle((M,y,W-M,y+h),radius=30,fill=(255,255,255,22),outline=(235,227,217,90),width=2)
        im=Image.alpha_composite(im,card); d=ImageDraw.Draw(im)
        d.ellipse((M+34,y+h/2-10,M+54,y+h/2+10),fill=c.TERRA); ty=y+34
        for ln in lines: d.text((M+88,ty),ln,font=itf,fill=c.WHITE); ty+=lh
        y+=h+32
    if p.get("nota"):
        nf=c.sans("Medium",34); nl=c.wrap(d,p["nota"],nf,W-2*M-70); nh=len(nl)*50+52
        d.rounded_rectangle((M,y+6,W-M,y+6+nh),radius=30,fill=c.TERRA); ty=y+6+26
        for ln in nl: d.text((M+35,ty),ln,font=nf,fill=c.WHITE); ty+=50
        y+=nh+6
    assert y<1560,f"tela estoura: y={y}"
    foot(d,"Salve para consultar depois"); return im.convert("RGB")
def f_final(sp):
    k=sp["final"]; im=photo_bg(k["foto"]); d=ImageDraw.Draw(im); head(d)
    y=1000; d.text((M,y),k["l1"],font=c.serif(76),fill=c.WHITE); d.text((M-6,y+90),k["l2"],font=c.serif(160),fill=c.BEIGE)
    sf=c.sans("Medium",44); py=y+90+230
    for ln in c.wrap(d,k["sub"],sf,W-2*M): d.text((M,py),ln,font=sf,fill=c.WHITE); py+=64
    pf=c.sans("Medium",38); t="Me chama no direct"; tw=d.textlength(t,font=pf)
    d.rounded_rectangle((M,py+26,M+tw+68,py+26+78),radius=39,fill=c.TERRA); d.text((M+34,py+26+14),t,font=pf,fill=c.WHITE)
    foot(d,"Ficou com dúvida? Fale comigo!"); return im.convert("RGB")
def to_reels(im): return im
def make(sp):
    R=c.R; n=len(sp["paginas"])+2
    frames=[(f_capa(sp),sp.get("seg_capa",3.5))]
    frames+=[(f_pag(p),sp.get("seg_pagina",5.5)) for p in sp["paginas"]]
    frames+=[(f_final(sp),sp.get("seg_final",4.5))]
    tmp=tempfile.mkdtemp(); clips=[]
    for i,(im,dur) in enumerate(frames):
        png=f"{tmp}/f{i}.png"; to_reels(im).save(png); mp=f"{tmp}/c{i}.mp4"
        vf=(f"scale=1134:2016,crop=1080:1920:x='54*t/{dur}':y='96*t/{dur}',"
            f"fade=t=in:st=0:d=0.35,fade=t=out:st={dur-0.35}:d=0.35,format=yuv420p")
        subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-t",str(dur),"-i",png,"-vf",vf,"-r","30","-c:v","libx264","-crf","20","-preset","veryfast",mp],check=True)
        clips.append(mp)
        if i==0: im.save(f"{tmp}/capa.png")
    lst=f"{tmp}/l.txt"; open(lst,"w").write("".join(f"file '{x}'\n" for x in clips))
    os.makedirs(f"{R}/reels",exist_ok=True); out=f"{R}/reels/{sp['arquivo']}.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-f","lavfi","-i","anullsrc=r=44100:cl=stereo",
        "-shortest","-c:v","libx264","-crf","22","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","96k","-movflags","+faststart",out],check=True)
    cap=f"{R}/reels/{sp['arquivo']}-capa.jpg"; to_reels(frames[0][0]).save(cap,quality=90)
    print(out); print(cap); print("frames:",tmp)
if __name__=="__main__": make(json.load(open(sys.argv[1])))
