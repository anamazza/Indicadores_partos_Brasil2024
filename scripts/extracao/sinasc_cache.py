# -*- coding: utf-8 -*-
"""
sinasc_cache.py
Extrai do CSV do SINASC só os campos usados pelo painel, para todos os registros, num CSV
compacto (cache) que permite testar variantes de regra sem reler o zip de ~900 MB.
Uso: python sinasc_cache.py <SINASC_<ano>_csv.zip> <cache.csv>
"""
import csv, io, sys, time, zipfile

zip_path, out = sys.argv[1:3]
CAMPOS = ["CODESTAB", "DTNASC", "PARTO", "TPROBSON", "APGAR5", "PESO", "IDANOMAL", "TPNASCASSI",
          "GESTACAO", "SEMAGESTAC", "GRAVIDEZ", "CODMUNNASC", "LOCNASC"]
zf = zipfile.ZipFile(zip_path)
membro = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
t0 = time.time(); n = 0
with zf.open(membro) as raw, open(out, "w", encoding="utf-8", newline="") as fo:
    txt = io.TextIOWrapper(raw, encoding="latin-1", newline="")
    rd = csv.reader(txt, delimiter=";")
    header = [c.strip('"').upper() for c in next(rd)]
    idx = {c: i for i, c in enumerate(header)}
    pos = [idx[c] for c in CAMPOS]
    w = csv.writer(fo); w.writerow(CAMPOS)
    for row in rd:
        n += 1
        w.writerow([row[p].strip().strip('"') for p in pos])
print(f"{membro}: {n:,} registros -> {out} ({time.time()-t0:.0f}s)")
