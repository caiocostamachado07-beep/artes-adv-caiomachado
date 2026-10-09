#!/usr/bin/env python3
"""Conta quantas vezes cada foto de fotos/ foi usada nos JSON de render/ e diz se é hora de pedir mais fotos ao Caio.
Uso: python3 render/uso_fotos.py  -> lista (menos usadas primeiro) e linha final 'PEDIR_FOTOS: SIM|NAO'.
Regra: pedir mais fotos quando restarem menos de 5 fotos com 0 usos OU quando a foto menos usada já tiver 2+ usos."""
import glob, json, os, re, collections
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fotos=sorted(os.path.basename(f) for f in glob.glob(f"{R}/fotos/*") if f.lower().endswith((".jpg",".jpeg",".png")))
uso=collections.Counter()
for j in glob.glob(f"{R}/render/*.json"):
    for m in re.findall(r'"foto"\s*:\s*"([^"]+)"',open(j).read()): uso[m]+=1
rows=sorted(((uso[f],f) for f in fotos))
for n,f in rows: print(n,f)
zero=sum(1 for n,_ in rows if n==0); minimo=rows[0][0]
pedir= zero<5 or minimo>=2
print(f"\nTotal {len(fotos)} fotos; nunca usadas: {zero}; uso mínimo: {minimo}")
print("PEDIR_FOTOS:", "SIM" if pedir else "NAO")
