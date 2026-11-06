# -*- coding: utf-8 -*-
"""
regras.py
Regras de cálculo das colunas da planilha de indicadores (formato ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS),
derivadas da reprodução CNES a CNES da planilha de 2024 (ver relatorios/reproducao_2024.md).
Cada função recebe os agregados gerados pelos scripts desta pasta (sinasc_indicadores.py, sih_partos.py,
sih_sp_atos.py, cnes_leitos_neo.py, cnes_habilitacoes.py) e devolve as colunas por CNES.
"""
import json, os

# --- SIH: procedimentos de parto (PROC_REA) e colunas da planilha
PARTO_COLS = {
    "0411010034": "OPERAÇÃO CESARIANA",
    "0411010042": "OPERAÇÃO CESARIANA C/ LAQUEADURA TUBARIA",
    "0411010026": "OPERAÇÃO CESARIANA EM GAR",
    "0310010039": "PARTO NORMAL",
    "0310010055": "PARTO NORMAL EM CPN",
    "0310010047": "PARTO NORMAL EM GESTACAO DE ALTO RISCO",
}
LAQ_PV = "0409060313"                 # laqueadura na internação do parto normal (não entra na planilha 2024)
AMIU, CURET = "0409060070", "0411020013"

# --- limiares de classificação (reproduzem a planilha 2024)
ROBSON_INTERVALO = {1: (1.0, 30.0), 2: (1.0, 67.0), 3: (1.0, 12.0), 4: (1.0, 47.0)}   # adequado: lo <= % <= hi e NV > 0
ASFIXIA_MAX, ENF_MIN, AMIU_MIN, LARC_MIN, VIOL_MIN, SELO_MIN = 0.6, 50.0, 50.0, 3, 2, 5


def pct(n, d, casas=1):
    return round(100.0 * n / d, casas) if d else 0.0


def carregar_uf_json(pasta, chave, somar=False):
    """Junta os checkpoints por UF ({chave: {cnes: {...}}}) num único dicionário por CNES.
    somar=True soma os contadores quando o mesmo CNES aparece em mais de um arquivo (UF dividida em períodos)."""
    out = {}
    for f in sorted(os.listdir(pasta)):
        if not f.endswith(".json"):
            continue
        for cnes, cont in json.load(open(os.path.join(pasta, f), encoding="utf-8"))[chave].items():
            if somar and cnes in out:
                for k, v in cont.items():
                    out[cnes][k] = out[cnes].get(k, 0) + v
            else:
                out[cnes] = dict(cont)
    return out


# ------------------------------------------------------------------ SIH
def partos(proc, cnes, atrib):
    """Contagens das 6 colunas de parto para a atribuição de ano `atrib` (ex.: 'c2025' = competência 2025)."""
    p = proc.get(cnes, {})
    cols = {col: p.get(f"{code}|{atrib}", 0) for code, col in PARTO_COLS.items()}
    cols["TOTAL"] = sum(cols.values())
    cols["TOTAL S/ CPN"] = cols["TOTAL"] - cols["PARTO NORMAL EM CPN"]
    cols["_laqueadura_pv"] = p.get(f"{LAQ_PV}|{atrib}", 0)
    return cols


def amiu(proc, cnes, atrib):
    """% AMIU = AMIU ÷ (AMIU + curetagem pós-abortamento) × 100; atribuição de ano `atrib` (planilha 2024: 's2024')."""
    p = proc.get(cnes, {})
    a, c = p.get(f"{AMIU}|{atrib}", 0), p.get(f"{CURET}|{atrib}", 0)
    return pct(a, a + c), a, c


# ------------------------------------------------------------------ SINASC
# estabelecimentos que trocaram de CNES: o SIH já usa o código novo, mas as DNV seguem no antigo
ALIAS_SINASC = {"5878640": ["3511251"], "9131922": ["2679663"]}
# complexos hospitalares: as AIH de parto saem por um CNES e as DNV por outro do mesmo complexo. Somados só a partir
# de 2025 (complexos=True); a planilha institucional de 2024 não somou e ficou com os indicadores do SINASC zerados.
# HC FAMEMA (Marília/SP): 2025507 = hospital (AIH); 2025523 = Unidade Materno Infantil (DNV), conforme o CNES.
COMPLEXO_SINASC = {"2025507": ["2025523"]}


def sinasc(est, cnes, complexos=False):
    """Robson (NV e cesáreas G1–G4), asfixia e parto vaginal por enfermeira a partir de sinasc_indicadores.py."""
    s = dict(est.get(cnes, {}))
    for antigo in ALIAS_SINASC.get(cnes, []) + (COMPLEXO_SINASC.get(cnes, []) if complexos else []):
        for k, v in est.get(antigo, {}).items():
            s[k] = s.get(k, 0) + v
    out = {}
    nv = s.get("nv", 0)
    for g in (1, 2, 3, 4):
        n, c = s.get(f"nv_g{g}", 0), s.get(f"ces_g{g}", 0)
        out[f"TOTAL NV G{g}"], out[f"Nº CESAREANA G{g}"], out[f"% CESAREANA G{g}"] = n, c, pct(c, n)
    # asfixia: Apgar 5' < 7, peso >= 2500 g e anomalia congênita = "não" (IDANOMAL = 2), sobre TODOS os NV
    out["% ASFIXIA ≥2500G SEM ANOMALIAS CONGÊNITAS"] = pct(s.get("asf_num_b", 0), nv)
    # enfermagem: TPNASCASSI = 2 sobre todos os partos vaginais (PARTO = 1), inclusive profissional ignorado
    out["% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM"] = pct(s.get("enf_num", 0), s.get("enf_den_todos", 0))
    out["_nv"] = nv
    return out


# ------------------------------------------------------------------ CNES
def neonatal(leitos, cnes, comp, utin=("81", "82")):
    """UNIDADE NEONATAL COMPLETA pelos leitos existentes (QT_EXIST) do CNES-LT na competência `comp` (aamm)."""
    d = leitos.get(cnes, {}).get(comp)
    if d is None:
        return None
    u = sum(d.get(x, [0, 0])[0] for x in utin) > 0
    co, ca = d.get("92", [0, 0])[0] > 0, d.get("93", [0, 0])[0] > 0
    if u and co and ca:
        return "SIM"
    return "NÃO SE APLICA" if not (u or co or ca) else "NÃO"


GESTAO = {"E": "ESTADUAL", "M": "MUNICIPAL", "D": "DUPLA"}


def gestao_natureza(cadastro, cnes):
    c = cadastro.get(cnes)
    if not c:
        return None, None
    nj = c["nat_jur"]
    nat = "PÚBLICO" if nj.startswith("1") else ("SEM FINS LUCRATIVOS" if nj.startswith("3") else "PRIVADO")
    return GESTAO.get(c["tpgestao"]), nat


def _comp(s):
    return s[3:] + s[:2] if s and len(s) == 7 else "999999"


def hgpar(fichas, cnes, comp="999999"):
    """HGPAR = habilitação CNES 1420 vigente na competência (aaaamm); None se a ficha falhou."""
    f = fichas.get(cnes)
    if not f or "erro" in f:
        return None
    return "SIM" if any(h["coGrupo"] == "1420" and _comp(h["dtCompInicio"]) <= comp <= _comp(h["dtCompFim"])
                        for h in f.get("habilitacoes") or []) else "0"


# ------------------------------------------------------------------ classificações
def classificar(rec, smcon_neo=False, smcon_obst=False):
    """Preenche as colunas de classificação a partir dos valores numéricos (regras da planilha 2024)."""
    tot = 0
    for g in (1, 2, 3, 4):
        lo, hi = ROBSON_INTERVALO[g]
        ok = rec[f"TOTAL NV G{g}"] > 0 and lo <= rec[f"% CESAREANA G{g}"] <= hi
        rec[f"CLASSIFICAÇÃO G{g}"] = 1 if ok else None
        tot += int(ok)
    rec["TOTAL CLASSIFICAÇÃO"] = tot
    rec["CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)"] = "ADEQUADO" if tot >= 2 else None
    rec["CLASSIFICAÇÃO ASFIXIA"] = "ADEQUADO" if rec["% ASFIXIA ≥2500G SEM ANOMALIAS CONGÊNITAS"] <= ASFIXIA_MAX else "INADEQUADO"
    rec["CLASSIFICAÇÃO PARTO ENF."] = "ADEQUADO" if rec["% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM"] >= ENF_MIN else "INADEQUADO"
    rec["CLASSIFICAÇÃO AMIU"] = "ADEQUADO" if rec["% AMIU"] >= AMIU_MIN else None
    rec["TOTAL.1"] = (rec.get("DIU") or 0) + (rec.get("IMPLANTE ") or 0)
    rec["CLASSIFICAÇÃO CONTRACEPÇÃO"] = "SIM" if rec["TOTAL.1"] >= LARC_MIN else None
    rec["CLASSIFICAÇÃO VIOLÊNCIA SEXUAL"] = "SIM" if (rec.get("Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL") or 0) >= VIOL_MIN else None
    rec["SMCON NEO"] = "ok" if smcon_neo else None
    rec["SMCON OBST"] = "ok" if smcon_obst else None
    rec["SMCON TOTAL"] = int(smcon_neo) + int(smcon_obst)
    flags = [rec["CLASSIFICAÇÃO ASFIXIA"] == "ADEQUADO", rec["CLASSIFICAÇÃO PARTO ENF."] == "ADEQUADO",
             rec["CLASSIFICAÇÃO AMIU"] == "ADEQUADO", rec["CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)"] == "ADEQUADO",
             rec["CLASSIFICAÇÃO CONTRACEPÇÃO"] == "SIM", rec["CLASSIFICAÇÃO VIOLÊNCIA SEXUAL"] == "SIM",
             smcon_neo, smcon_obst, rec.get("UNIDADE NEONATAL COMPLETA") in ("SIM", "NÃO SE APLICA")]
    rec["CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS"] = "ADEQUADO" if sum(flags) >= SELO_MIN else None
    return rec
