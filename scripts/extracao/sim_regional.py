# -*- coding: utf-8 -*-
"""
sim_regional.py
Agrega o SIM completo (DO de todas as UFs + DOFET nacional) por UF, nos mesmos três recortes de regional.py:
  ocorr  — óbitos por UF de ocorrência (CODMUNOCOR)
  resid  — óbitos por UF de residência (CODMUNRES)
  painel — óbitos ocorridos nas unidades do painel (CODESTAB na lista), por UF de ocorrência
Contadores (regras auditadas em Mortalidade Indicadores/Auditoria_regras_indicadores_mortalidade.md; fichas IDB C.1.4, C.1.1, C.1.2, C.2 e C.3):
  neo       óbitos de 0–27 dias (idade = DTOBITO − DTNASC; sem DTNASC, campo IDADE: unidade 0/1 → 0 dias, 2 → dias)
  neo_prec  0–6 dias;  neo_tard 7–27 dias;  inf  < 1 ano
  fetal     DOFET com ≥ 22 semanas OU ≥ 500 g (exclui os com ambos ignorados; fetal_ign os guarda)
  materno   regra MS/OOBr: mulher; O00–O95, O98, O99 sempre; B20–B24, D39.2, E23.0 só se OBITOGRAV=1 ou OBITOPUERP=1;
            A34, F53, M83.0 se OBITOPUERP = 1 ou ignorado.  materno_tardio = O96/O97 (não entra na RMM)
  mif       óbitos de mulheres de 10–49 anos (denominador alternativo)
Uso: python -X utf8 sim_regional.py --ano 2024 --sim <pasta com DO<UF><ano>.dbc> --dofet <DOFET<aa>.dbc> --lista <planilha .xlsx> --saida <json>
"""
import argparse, collections, datetime, json, os, sys, tempfile, time

import datasus_dbc
from dbfread import DBF

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import regras as R

ap = argparse.ArgumentParser()
ap.add_argument("--ano", required=True)
ap.add_argument("--sim", required=True)
ap.add_argument("--dofet", required=True)
ap.add_argument("--lista", required=True)
ap.add_argument("--saida", required=True)
a = ap.parse_args()
ANO = int(a.ano)

import pandas as pd
cnes_painel = {str(c).strip().zfill(7) for c in pd.read_excel(a.lista, engine="openpyxl")["CNES"].dropna()}
# códigos antigos/novos e complexos: se qualquer um dos códigos está na lista, todos entram
# (a planilha 2024 traz os códigos antigos 2679663 e 3511251; a de 2025, os novos). HC FAMEMA: os óbitos
# maternos ficam no CNES adulto 2025507 e as DNV no 2025523; os dois entram nos dois anos.
for principal, antigos in list(R.ALIAS_SINASC.items()) + list(R.COMPLEXO_SINASC.items()):
    grupo = {principal, *antigos}
    if grupo & cnes_painel:
        cnes_painel.update(grupo)
print(f"{len(cnes_painel)} CNES do painel", flush=True)

UFS = "AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO".split()
agg = {n: collections.defaultdict(collections.Counter) for n in ("ocorr", "resid", "painel")}
diag = collections.Counter()


def uf_de(codmun):
    codmun = (codmun or "").strip()
    return codmun[:2] if len(codmun) >= 6 and codmun[:2].isdigit() and "11" <= codmun[:2] <= "53" else "99"


def data(s):
    s = (s or "").strip().zfill(8)
    try:
        return datetime.date(int(s[4:8]), int(s[2:4]), int(s[0:2]))
    except ValueError:
        return None


def idade_dias(r):
    d_ob, d_na = data(r.get("DTOBITO")), data(r.get("DTNASC"))
    if d_ob and d_na:
        return (d_ob - d_na).days
    u = (r.get("IDADE") or "").strip().zfill(3)
    if u[0] in ("0", "1"):
        return 0
    if u[0] == "2" and u[1:].isdigit():
        return int(u[1:])
    return None


def idade_anos(r):
    u = (r.get("IDADE") or "").strip().zfill(3)
    if u[0] == "4" and u[1:].isdigit():
        return int(u[1:])
    if u[0] == "5" and u[1:].isdigit():
        return 100 + int(u[1:])
    if u[0] in ("0", "1", "2", "3"):
        return 0
    return None


def materno(r):
    sexo = (r.get("SEXO") or "").strip()[:1]
    if sexo not in ("2", "F"):
        return None
    cb = (r.get("CAUSABAS") or "").strip().upper().replace(".", "")
    c3 = cb[:3]
    og = (r.get("OBITOGRAV") or "").strip()[:1] or "9"
    op = (r.get("OBITOPUERP") or "").strip()[:1]
    op = "9" if op in ("", "0", "4", "8") else op
    if ("O00" <= c3 <= "O95") or c3 in ("O98", "O99"):
        return "materno"
    if c3 in ("O96", "O97"):
        return "tardio"
    if (c3 in ("B20", "B21", "B22", "B23", "B24") or cb in ("D392", "E230")) and (og == "1" or op == "1"):
        return "materno"
    if (cb in ("A34", "M830") or c3 == "F53") and op in ("1", "9"):
        return "materno"
    return None


def contar(c, r):
    c["obitos"] += 1
    d = idade_dias(r)
    if d is not None and 0 <= d <= 27:
        c["neo"] += 1
        c["neo_prec" if d <= 6 else "neo_tard"] += 1
    if d is not None and 0 <= d < 365:
        c["inf"] += 1
    m = materno(r)
    if m == "materno":
        c["materno"] += 1
    elif m == "tardio":
        c["materno_tardio"] += 1
    an = idade_anos(r)
    if (r.get("SEXO") or "").strip()[:1] in ("2", "F") and an is not None and 10 <= an <= 49:
        c["mif"] += 1


def registrar(r):
    if (r.get("TIPOBITO") or "").strip() == "1":          # fetal dentro do DO (não deveria haver; vai para diagnóstico)
        diag["tipobito1_no_DO"] += 1
        return
    if data(r.get("DTOBITO")) is None or data(r.get("DTOBITO")).year != ANO:
        diag["fora_do_ano"] += 1
        return
    uf_o, uf_r = uf_de(r.get("CODMUNOCOR")), uf_de(r.get("CODMUNRES"))
    contar(agg["ocorr"][uf_o], r)
    contar(agg["resid"][uf_r], r)
    if (r.get("CODESTAB") or "").strip().zfill(7) in cnes_painel:
        contar(agg["painel"][uf_o], r)
    # diagnóstico do campo IDADE x datas (neonatais)
    d_ob, d_na = data(r.get("DTOBITO")), data(r.get("DTNASC"))
    u = (r.get("IDADE") or "").strip().zfill(3)
    if d_ob and d_na and 0 <= (d_ob - d_na).days <= 27:
        diag[f"neo_por_datas_unidade_{u[0]}"] += 1
    if not d_na and u[0] in ("0", "1", "2"):
        diag["neo_recuperado_pelo_IDADE"] += 1


def ler_dbc(caminho, func):
    dbf = os.path.join(tempfile.gettempdir(), os.path.basename(caminho)[:-4] + f"_{os.getpid()}.dbf")
    datasus_dbc.decompress(caminho, dbf)
    n = 0
    for r in DBF(dbf, encoding="latin-1", char_decode_errors="ignore"):
        func(r); n += 1
    os.remove(dbf)
    return n


t0 = time.time(); total = 0
for uf in UFS:
    cand = [os.path.join(a.sim, f"DO{uf}{ANO}.dbc"), os.path.join(a.sim, f"DO{uf}OPEN{str(ANO)[-2:]}.dbc")]
    arq = next((p for p in cand if os.path.exists(p)), None)
    if not arq:
        print("FALTA", uf, flush=True); diag[f"falta_{uf}"] += 1; continue
    n = ler_dbc(arq, registrar); total += n
    print(f"  {uf} {n:,} ({time.time()-t0:.0f}s)", flush=True)

# ---- DOFET (arquivo nacional)
fet_tot = 0


def registrar_fetal(r):
    global fet_tot
    fet_tot += 1
    if data(r.get("DTOBITO")) is None or data(r.get("DTOBITO")).year != ANO:
        diag["fetal_fora_do_ano"] += 1
        return
    sem, peso = (r.get("SEMAGESTAC") or "").strip(), (r.get("PESO") or "").strip()
    sem_ok = sem.isdigit() and 1 <= int(sem) <= 44
    peso_ok = peso.isdigit() and 100 <= int(peso) <= 8000
    elegivel = (sem_ok and int(sem) >= 22) or (peso_ok and int(peso) >= 500)
    chave = "fetal" if elegivel else ("fetal_ign" if not (sem_ok or peso_ok) else "fetal_menor22")
    uf_o, uf_r = uf_de(r.get("CODMUNOCOR")), uf_de(r.get("CODMUNRES"))
    agg["ocorr"][uf_o][chave] += 1
    agg["resid"][uf_r][chave] += 1
    if (r.get("CODESTAB") or "").strip().zfill(7) in cnes_painel:
        agg["painel"][uf_o][chave] += 1


ler_dbc(a.dofet, registrar_fetal)
print(f"  DOFET {fet_tot:,}", flush=True)

json.dump({"ano": a.ano, "pasta_sim": a.sim, "dofet": os.path.basename(a.dofet), "registros_do": total, "registros_dofet": fet_tot,
           "lista": os.path.basename(a.lista), "diagnostico": dict(diag),
           "recortes": {n: {uf: dict(c) for uf, c in d.items()} for n, d in agg.items()}},
          open(a.saida, "w", encoding="utf-8"), ensure_ascii=False)
B = {k: sum(c.get(k, 0) for c in agg["ocorr"].values()) for k in ("obitos", "neo", "neo_prec", "inf", "fetal", "materno", "materno_tardio")}
print(f"{a.ano}: {total:,} DO; Brasil {B} -> {a.saida} ({time.time()-t0:.0f}s)")
