# -*- coding: utf-8 -*-
"""
regional.py
Agrega o SINASC completo (todos os estabelecimentos) por UF, em três recortes, para a comparação
regional entre as unidades do painel e o conjunto da região:
  ocorr  — todos os nascidos vivos por UF de ocorrência (CODMUNNASC)
  resid  — todos os nascidos vivos por UF de residência da mãe (CODMUNRES)
  painel — nascidos vivos nas unidades do painel (lista de CNES), por UF de ocorrência
Cada recorte guarda numeradores e denominadores de: cesárea (bruta e por grupo de Robson),
prematuridade, baixo peso, Apgar 5º min < 7 (todos os NV e a regra do painel: >= 2.500 g sem anomalia),
anomalia congênita, parto vaginal por enfermeira/obstetriz, mãe adolescente / >= 35 anos,
pré-natal >= 7 consultas, gestação múltipla e local do nascimento (hospital).
Uso: python -X utf8 regional.py --ano 2024 --sinasc <SINASC_<ano>_csv.zip> --lista <planilha .xlsx ou .txt com CNES> --saida <json>
"""
import argparse, collections, csv, io, json, os, sys, time, zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import regras as R

ap = argparse.ArgumentParser()
ap.add_argument("--ano", required=True)
ap.add_argument("--sinasc", required=True)
ap.add_argument("--lista", required=True, help="planilha do painel (.xlsx, coluna CNES) ou .txt com um CNES por linha")
ap.add_argument("--saida", required=True)
a = ap.parse_args()

# --- unidades do painel (+ CNES antigos e complexos que o painel soma)
if a.lista.lower().endswith(".xlsx"):
    import pandas as pd
    cnes_painel = {str(c).strip().zfill(7) for c in pd.read_excel(a.lista, engine="openpyxl")["CNES"].dropna()}
else:
    cnes_painel = {l.strip().zfill(7) for l in open(a.lista, encoding="utf-8") if l.strip()}
# códigos antigos/novos e complexos: se qualquer um dos códigos está na lista, todos entram
# (a planilha 2024 traz os códigos antigos 2679663 e 3511251; a de 2025, os novos)
for principal, antigos in list(R.ALIAS_SINASC.items()) + list(R.COMPLEXO_SINASC.items()):
    grupo = {principal, *antigos}
    if grupo & cnes_painel:
        cnes_painel.update(grupo)
print(f"{len(cnes_painel)} CNES do painel (com apelidos/complexos)", flush=True)

CAMPOS = ["CODESTAB", "CODMUNNASC", "CODMUNRES", "LOCNASC", "PARTO", "TPROBSON", "APGAR5", "PESO",
          "IDANOMAL", "TPNASCASSI", "GESTACAO", "SEMAGESTAC", "IDADEMAE", "CONSPRENAT", "GRAVIDEZ", "DTNASC"]

agg = {n: collections.defaultdict(collections.Counter) for n in ("ocorr", "resid", "painel")}


def uf_de(codmun):
    return codmun[:2] if len(codmun) >= 6 and codmun[:2].isdigit() and "11" <= codmun[:2] <= "53" else "99"


def contar(c, row, g):
    c["nv"] += 1
    if g("LOCNASC") == "1":
        c["hosp"] += 1
    parto = g("PARTO")
    ces, vag = parto == "2", parto == "1"
    if ces or vag:
        c["parto_inf"] += 1
    if ces:
        c["ces"] += 1
    rb = g("TPROBSON")
    grp = int(rb) if rb.isdigit() and 1 <= int(rb) <= 10 else 0
    c[f"nv_g{grp}"] += 1
    if ces:
        c[f"ces_g{grp}"] += 1
    # idade gestacional: semanas (SEMAGESTAC) ou faixa (GESTACAO 1-5)
    sem, fx = g("SEMAGESTAC"), g("GESTACAO")
    if sem.isdigit() and 17 <= int(sem) <= 47:
        c["ig_inf"] += 1
        if int(sem) < 37:
            c["pret"] += 1
    elif fx in ("1", "2", "3", "4", "5", "6"):
        c["ig_inf"] += 1
        if fx in ("1", "2", "3", "4"):
            c["pret"] += 1
    peso = g("PESO")
    peso_ok = peso.isdigit() and 200 <= int(peso) <= 8000
    if peso_ok:
        c["peso_inf"] += 1
        if int(peso) < 2500:
            c["bp"] += 1
        if int(peso) < 1500:
            c["mbp"] += 1
    apg = g("APGAR5")
    apg_ok = apg.isdigit() and int(apg) <= 10
    if apg_ok:
        c["apg_inf"] += 1
        if int(apg) < 7:
            c["apg7"] += 1
    anom = g("IDANOMAL")
    if anom in ("1", "2"):
        c["anom_inf"] += 1
        if anom == "1":
            c["anom"] += 1
    if peso_ok and int(peso) >= 2500 and anom == "2" and apg_ok:   # regra do painel (hub/coordenação 2025)
        c["asf_den"] += 1
        if int(apg) < 7:
            c["asf_num"] += 1
    if vag:
        c["vag"] += 1
        tp = g("TPNASCASSI")
        if tp in ("1", "2", "3", "4"):
            c["enf_den"] += 1
            if tp == "2":
                c["enf_num"] += 1
    idade = g("IDADEMAE")
    if idade.isdigit() and 8 <= int(idade) <= 60:
        c["idade_inf"] += 1
        if int(idade) < 20:
            c["adolesc"] += 1
        if int(idade) >= 35:
            c["idade35"] += 1
    pn = g("CONSPRENAT")
    if pn.isdigit() and int(pn) <= 60:
        c["pn_inf"] += 1
        if int(pn) >= 7:
            c["pn7"] += 1
    grav = g("GRAVIDEZ")
    if grav in ("1", "2", "3"):
        c["grav_inf"] += 1
        if grav != "1":
            c["multipla"] += 1


zf = zipfile.ZipFile(a.sinasc)
membro = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
t0 = time.time(); total = 0
with zf.open(membro) as raw:
    txt = io.TextIOWrapper(raw, encoding="latin-1", newline="")
    rd = csv.reader(txt, delimiter=";")
    header = [c.strip('"').upper() for c in next(rd)]
    idx = {c: i for i, c in enumerate(header)}
    pos = {c: idx[c] for c in CAMPOS}
    for row in rd:
        total += 1
        g = lambda c: row[pos[c]].strip().strip('"')
        uf_o, uf_r = uf_de(g("CODMUNNASC")), uf_de(g("CODMUNRES"))
        contar(agg["ocorr"][uf_o], row, g)
        contar(agg["resid"][uf_r], row, g)
        if g("CODESTAB").zfill(7) in cnes_painel:
            contar(agg["painel"][uf_o], row, g)
        if total % 500_000 == 0:
            print(f"  {total:,} registros ({time.time()-t0:.0f}s)", flush=True)

json.dump({"ano": a.ano, "arquivo": os.path.basename(a.sinasc), "membro": membro, "registros": total,
           "lista": os.path.basename(a.lista), "cnes_painel": sorted(cnes_painel),
           "recortes": {n: {uf: dict(c) for uf, c in d.items()} for n, d in agg.items()}},
          open(a.saida, "w", encoding="utf-8"), ensure_ascii=False)
print(f"{a.ano}: {total:,} NV; painel {sum(c['nv'] for c in agg['painel'].values()):,} NV -> {a.saida} ({time.time()-t0:.0f}s)")
