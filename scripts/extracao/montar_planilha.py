# -*- coding: utf-8 -*-
"""
montar_planilha.py
Monta a planilha de indicadores no formato ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS (57 colunas, uma linha
por estabelecimento) a partir dos agregados de extracao/saida/, com as regras de regras.py.
Uso:
  python montar_planilha.py --ano 2025 --sinasc sinasc_2025.json --partos s2025 --amiu s2025 --cnes 2609 \
         --saida PLANILHA_2025_saida.xlsx [--universo 1000 | --lista cnes.txt] [--smcon smcon.csv] [--sp codigos_sp.json]
  python montar_planilha.py --ano 2024 --sinasc sinasc_2024.json --partos c2025 --amiu s2024 --cnes 2603 \
         --lista extracao/cnes_referencia_2024.txt --referencia <planilha_2024.xlsx> --saida PLANILHA_2024_recalculada.xlsx
--partos/--amiu: atribuição de ano das AIH ('c' competência, 'i' internação, 's' saída + ano).
--cnes: competência (aamm) do CNES-LT para leitos, gestão e natureza (usa cnes_leitos_2401_<aamm>.json).
--referencia: planilha anterior de onde se copiam nomes de território/estabelecimento já padronizados e SMCON.
--smcon: CSV 'cnes;neo;obst' (1/0). Sem ele, as colunas SMCON ficam vazias.
"""
import argparse, io, json, os, re, sys, unicodedata, zipfile
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regras as R

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAIDA = os.path.join(RAIZ, "extracao", "saida")
TERR = os.path.join(RAIZ, "extracao", "territorio")       # base territorial do DATASUS (jun/2026), copiada da Extracao_SINASC

ap = argparse.ArgumentParser()
ap.add_argument("--ano", required=True); ap.add_argument("--sinasc", required=True)
ap.add_argument("--partos", required=True); ap.add_argument("--amiu", required=True); ap.add_argument("--cnes", required=True)
ap.add_argument("--saida", required=True); ap.add_argument("--universo", type=int, default=1000); ap.add_argument("--lista")
ap.add_argument("--referencia"); ap.add_argument("--smcon"); ap.add_argument("--sp"); ap.add_argument("--hgpar-comp", default="999999")
ap.add_argument("--smcon-da-referencia", action="store_true", help="copia SMCON NEO/OBST da planilha de referência (só para recalcular o mesmo ano)")
ap.add_argument("--sia", help="pasta com os JSON por UF de sia_violencia.py (atendimento a vítima de violência sexual)")
ap.add_argument("--sia-atrib", default="c2025", help="atribuição de ano no SIA: c<ano> = competência de realização (PA_CMP), m<ano> = movimento (PA_MVM)")
a = ap.parse_args()

COLUNAS = ["REGIÃO DO PAÍS", "UF", "CÓD MRS", "MACRORREGIÃO DE SAÚDE", "CÓD RS", "REGIÃO DE SAÚDE", "COD MUN", "MUNICÍPIO", "CNES",
           "CNES - ESTABELECIMENTO", "GESTÃO", "NATUREZA JURÍDICA", "STATUS", "HGPAR", "OPERAÇÃO CESARIANA",
           "OPERAÇÃO CESARIANA C/ LAQUEADURA TUBARIA", "OPERAÇÃO CESARIANA EM GAR", "PARTO NORMAL", "PARTO NORMAL EM CPN",
           "PARTO NORMAL EM GESTACAO DE ALTO RISCO", "TOTAL", "TOTAL S/ CPN", "UNIDADE NEONATAL COMPLETA",
           "% ASFIXIA ≥2500G SEM ANOMALIAS CONGÊNITAS", "CLASSIFICAÇÃO ASFIXIA", "% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM",
           "CLASSIFICAÇÃO PARTO ENF.", "% AMIU", "CLASSIFICAÇÃO AMIU"]
for g in (1, 2, 3, 4):
    COLUNAS += [f"TOTAL NV G{g}", f"Nº CESAREANA G{g}", f"% CESAREANA G{g}", f"CLASSIFICAÇÃO G{g}"]
COLUNAS += ["TOTAL CLASSIFICAÇÃO", "CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)", "DIU", "IMPLANTE ", "TOTAL.1", "CLASSIFICAÇÃO CONTRACEPÇÃO",
            "Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL", "CLASSIFICAÇÃO VIOLÊNCIA SEXUAL", "SMCON NEO", "SMCON OBST", "SMCON TOTAL",
            "CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS"]

# ------------------------------------------------------------------ fontes
S = json.load(open(os.path.join(SAIDA, a.sinasc) if not os.path.isabs(a.sinasc) else a.sinasc, encoding="utf-8"))["estabelecimentos"]
P = R.carregar_uf_json(os.path.join(SAIDA, "sih_rd"), "procedimentos")
LJ = json.load(open(os.path.join(SAIDA, f"cnes_leitos_2401_{a.cnes}.json"), encoding="utf-8")); L, CAD = LJ["leitos"], LJ["cadastro"]
F = json.load(open(os.path.join(SAIDA, "cnes_fichas.json"), encoding="utf-8"))
SP = CSP = None
if a.sp:
    CSP = json.load(open(a.sp, encoding="utf-8")); SP = R.carregar_uf_json(os.path.join(SAIDA, "sih_sp"), "linhas")
SIA = R.carregar_uf_json(a.sia, "estabelecimentos", somar=True) if a.sia else None
VIOL_PROCS = ("0301040052", "0301040060")       # SIA/PA, quantidade aprovada (coordenação, 04/11/2026)
SM = {}
if a.smcon:
    for _, r in pd.read_csv(a.smcon, sep=";", dtype=str).iterrows():
        SM[r["cnes"].zfill(7)] = (str(r["neo"]).strip() in ("1", "ok"), str(r["obst"]).strip() in ("1", "ok"))
REF = pd.read_excel(a.referencia) if a.referencia else None

# território: base territorial (jun/2026) + nomes padronizados
z = zipfile.ZipFile(os.path.join(TERR, "base_territorial.zip"))
rd = lambda n, sep: pd.read_csv(io.BytesIO(z.read(n)), sep=sep, encoding="latin-1", dtype=str)
rs_nome = dict(zip(*(rd("tb_regsaud.csv", ",")[c] for c in ("CO_REGSAUD", "DS_NOMEPAD"))))
mac_nome = dict(zip(*(rd("tb_macsaud.csv", ";")[c] for c in ("CO_MACSAUD", "DS_NOMEPAD"))))
tm = rd("tb_municip.csv", ";"); mun_nome = dict(zip(tm.CO_MUNICIP, tm.DS_NOME)); mun_uf = dict(zip(tm.CO_MUNICIP, tm.UF))
tu = rd("tb_uf.csv", ";"); uf_nome = {s.strip(): n.strip() for s, n in zip(tu.ds_sigla, tu.ds_nome)}
REGIAO = {"1": "Norte", "2": "Nordeste", "3": "Sudeste", "4": "Sul", "5": "Centro-Oeste"}   # 1º dígito do código IBGE
mt = pd.read_csv(os.path.join(TERR, "municipio_territorios.csv"), dtype=str)
mun_rs = dict(zip(mt.CO_MUNICIP, mt.CO_REGSAUD)); mun_mac = dict(zip(mt.CO_MUNICIP, mt.CO_MACSAUD))


def sem_acento(s):
    s = unicodedata.normalize("NFD", str(s)).replace("ª", "a").replace("º", "o")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def nome_territorio(s, uf=None):
    s = sem_acento(s).replace("/", " ").strip()
    if uf and s.upper().endswith(" - " + uf.upper()):
        s = s[:-5].strip()
    return re.sub(r"\s+", " ", s).upper()


def nome_municipio(s):
    palavras = sem_acento(s).title().split()
    return " ".join(w.lower() if w.lower() in ("de", "da", "do", "das", "dos", "e") else w for w in palavras)


ref_nomes = {}
if REF is not None:
    for _, r in REF.iterrows():
        ref_nomes[("rs", str(r["CÓD RS"]))] = r["REGIÃO DE SAÚDE"]; ref_nomes[("mac", str(r["CÓD MRS"]))] = r["MACRORREGIÃO DE SAÚDE"]
        ref_nomes[("mun", str(r["COD MUN"]))] = r["MUNICÍPIO"]
        ref_nomes[("est", re.match(r"^(\d+)", r["CNES - ESTABELECIMENTO"]).group(1).zfill(7))] = r["CNES - ESTABELECIMENTO"]
        if a.smcon is None and a.smcon_da_referencia:
            SM.setdefault(re.match(r"^(\d+)", r["CNES - ESTABELECIMENTO"]).group(1).zfill(7),
                          (str(r["SMCON NEO"]).strip() == "ok", str(r["SMCON OBST"]).strip() == "ok"))

# ------------------------------------------------------------------ universo
if a.lista:
    universo = [l.strip().zfill(7) for l in open(a.lista, encoding="utf-8") if l.strip()]
    if REF is not None:   # usa o CNES do rótulo (código novo) quando a coluna CNES traz o antigo
        universo = [re.match(r"^(\d+)", r["CNES - ESTABELECIMENTO"]).group(1).zfill(7) for _, r in REF.iterrows()]
else:
    universo = sorted(c for c in P if R.partos(P, c, a.partos)["TOTAL"] > a.universo)
print(f"ano {a.ano}: {len(universo)} estabelecimentos (partos {a.partos}, AMIU {a.amiu}, CNES {a.cnes}, SINASC {a.sinasc})")

linhas, avisos = [], []
for c in universo:
    f = F.get(c, {}); cad = CAD.get(c, {})
    mun = str(f.get("codigo_municipio") or cad.get("codufmun") or "")[:6]
    if not mun:
        avisos.append(f"{c}: sem município (ficha e LT)"); continue
    uf = mun_uf.get(mun, "")
    rs, mac = mun_rs.get(mun), mun_mac.get(mun)
    rec = {"REGIÃO DO PAÍS": REGIAO.get(mun[:1], ""), "UF": nome_municipio(uf_nome.get(uf, uf)), "CÓD MRS": int(mac) if mac else None,
           "MACRORREGIÃO DE SAÚDE": ref_nomes.get(("mac", str(mac))) or nome_territorio(mac_nome.get(mac, "")),
           "CÓD RS": int(rs) if rs else None, "REGIÃO DE SAÚDE": ref_nomes.get(("rs", str(rs))) or nome_territorio(rs_nome.get(rs, ""), uf),
           "COD MUN": int(mun), "MUNICÍPIO": ref_nomes.get(("mun", mun)) or nome_municipio(mun_nome.get(mun, "")),
           "CNES": int(c), "CNES - ESTABELECIMENTO": ref_nomes.get(("est", c)) or f"{c} - {sem_acento(f.get('nome_fantasia') or f.get('nome_razao_social') or '').upper()}",
           "STATUS": "DESATIVADO" if f.get("codigo_motivo_desabilitacao_estabelecimento") else "ATIVO"}
    rec["GESTÃO"], rec["NATUREZA JURÍDICA"] = R.gestao_natureza(CAD, c)
    if rec["GESTÃO"] is None and f:   # sem cadastro LT na competência: usa a ficha da API
        rec["GESTÃO"] = R.GESTAO.get(f.get("tipo_gestao")); nj = str(f.get("descricao_natureza_juridica_estabelecimento") or "")
        rec["NATUREZA JURÍDICA"] = "PÚBLICO" if nj.startswith("1") else ("SEM FINS LUCRATIVOS" if nj.startswith("3") else ("PRIVADO" if nj else None))
        avisos.append(f"{c}: gestão/natureza pela ficha da API (sem LT {a.cnes})")
    rec["HGPAR"] = R.hgpar(F, c, a.hgpar_comp) or "0"
    rec.update(R.partos(P, c, a.partos))
    rec["% AMIU"], _, _ = R.amiu(P, c, a.amiu)
    rec.update(R.sinasc(S, c, complexos=int(a.ano) >= 2025))   # 2025 em diante: soma as DNV dos complexos (HC FAMEMA)
    if rec["_nv"] == 0:
        avisos.append(f"{c}: sem nascidos vivos no SINASC ({a.sinasc})")
    rec["UNIDADE NEONATAL COMPLETA"] = R.neonatal(L, c, a.cnes)
    if rec["UNIDADE NEONATAL COMPLETA"] is None:
        avisos.append(f"{c}: sem leitos no LT {a.cnes} (unidade neonatal em branco)")
    COLS_SP = ("DIU", "IMPLANTE ", "Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL")
    for col in COLS_SP:
        spec = (CSP or {}).get(col)
        rec[col] = sum(SP.get(c, {}).get(f"{code}|{spec['atrib']}", 0) for code in spec["codigos"]) if spec else None
    if SIA is not None:
        rec["Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL"] = sum(SIA.get(c, {}).get(f"{p}|{a.sia_atrib}|apr", 0) for p in VIOL_PROCS)
    neo, obst = SM.get(c, (False, False))
    R.classificar(rec, neo, obst)
    # colunas sem fonte: valor e classificação em branco; sem todas as fontes não há campo oficial (≥5 de 9)
    sem_larc = rec["DIU"] is None or rec["IMPLANTE "] is None
    sem_viol = rec["Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL"] is None
    if sem_larc:
        rec["TOTAL.1"] = rec["CLASSIFICAÇÃO CONTRACEPÇÃO"] = None
    if sem_viol:
        rec["CLASSIFICAÇÃO VIOLÊNCIA SEXUAL"] = None
    if c not in SM:
        rec["SMCON NEO"] = rec["SMCON OBST"] = None; rec["SMCON TOTAL"] = None
    if sem_larc or sem_viol or c not in SM:
        rec["CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS"] = None
    linhas.append(rec)

df = pd.DataFrame(linhas)
df = df.sort_values(["REGIÃO DO PAÍS", "UF", "MUNICÍPIO", "TOTAL"], ascending=[True, True, True, False])[COLUNAS]
df.to_excel(a.saida, index=False)
print(f"gravado {a.saida}: {len(df)} linhas, {df['TOTAL'].sum():,} partos")
for w in avisos:
    print("  aviso:", w)
