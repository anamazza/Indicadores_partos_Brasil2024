# -*- coding: utf-8 -*-
"""
comparar_2024.py
Compara, unidade a unidade, a planilha institucional de 2024 com a extração de 2024 feita dos microdados com as
mesmas regras de 2025 (planilhas/EXTRACAO_2024_regras_2025.xlsx, gerada por montar_planilha.py):
partos e AMIU pela data de internação 2024, DNV do complexo HC FAMEMA somadas, LARC pela data de saída 2024,
violência sexual pelo SIA/SUS (competência de realização 2024), CNES 03/2026 e SMCON 2024.
Gera relatorios/extracao_2024_x_planilha.md, extracao/saida/extracao_2024_diferencas.csv e
planilhas/COMPARACAO_2024_extracao_x_planilha.xlsx.
Uso: python comparar_2024.py <planilha_institucional.xlsx> <extracao.xlsx>
"""
import collections, json, os, re, sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regras as R

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAIDA = os.path.join(RAIZ, "extracao", "saida")
ARQ_PL, ARQ_EX = sys.argv[1], sys.argv[2]

cnes_rotulo = lambda s: re.match(r"^(\d+)", str(s)).group(1).zfill(7)
pl = pd.read_excel(ARQ_PL); pl["_cnes"] = pl["CNES - ESTABELECIMENTO"].map(cnes_rotulo); pl = pl.set_index("_cnes")
ex = pd.read_excel(ARQ_EX); ex["_cnes"] = ex["CNES - ESTABELECIMENTO"].map(cnes_rotulo); ex = ex.set_index("_cnes")
P = R.carregar_uf_json(os.path.join(SAIDA, "sih_rd"), "procedimentos")
TEM_VIOL = ex["Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL"].notna().any()

VIOL = "Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL"
GRUPOS = [
    ("Partos (SIH)", "planilha: competência 2025 · extração: internação 2024", list(R.PARTO_COLS.values()) + ["TOTAL", "TOTAL S/ CPN"]),
    ("AMIU (SIH)", "planilha: saída 2024 · extração: internação 2024", ["% AMIU", "CLASSIFICAÇÃO AMIU"]),
    ("Robson (SINASC 2024)", "mesma regra; extração soma as DNV do complexo HC FAMEMA",
     [f"{p} G{g}" for g in (1, 2, 3, 4) for p in ("TOTAL NV", "Nº CESAREANA", "% CESAREANA", "CLASSIFICAÇÃO")] + ["TOTAL CLASSIFICAÇÃO", "CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)"]),
    ("Asfixia e enfermagem (SINASC 2024)", "mesma regra; extração soma as DNV do complexo HC FAMEMA",
     ["% ASFIXIA ≥2500G SEM ANOMALIAS CONGÊNITAS", "CLASSIFICAÇÃO ASFIXIA", "% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM", "CLASSIFICAÇÃO PARTO ENF."]),
    ("CNES (03/2026)", "mesma regra e competência", ["UNIDADE NEONATAL COMPLETA", "GESTÃO", "NATUREZA JURÍDICA", "HGPAR"]),
    ("LARC (atos da AIH)", "planilha: competência 2025 · extração: saída 2024", ["DIU", "IMPLANTE ", "TOTAL.1", "CLASSIFICAÇÃO CONTRACEPÇÃO"]),
    ("Violência sexual", "planilha: fonte não identificada · extração: SIA/SUS 0301040052 + 0301040060, realização 2024", [VIOL, "CLASSIFICAÇÃO VIOLÊNCIA SEXUAL"]),
    ("SMCON", "mesma lista", ["SMCON NEO", "SMCON OBST", "SMCON TOTAL"]),
    ("Campo oficial (≥5 de 9)", "consequência das colunas acima", ["CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS"]),
]
POSITIVO = {"ADEQUADO", "SIM", "ok", "1", "1.0"}


def norm(v):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    if isinstance(v, str):
        return v.strip()
    return float(v)


def igual(a, b):
    a, b = norm(a), norm(b)
    if a is None or b is None:
        return a == b
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) < 0.051
    return str(a) == str(b)


def positivo(v):
    v = norm(v)
    return v is not None and (str(v) in POSITIVO or (isinstance(v, float) and v >= 1))


def n8(r):
    """Indicadores adequados entre os 8 do painel (SMCON conta uma vez; neonatal 'sim' ou 'não se aplica')."""
    f = [norm(r["CLASSIFICAÇÃO ASFIXIA"]) == "ADEQUADO", norm(r["CLASSIFICAÇÃO PARTO ENF."]) == "ADEQUADO", norm(r["CLASSIFICAÇÃO AMIU"]) == "ADEQUADO",
         norm(r["CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)"]) == "ADEQUADO", norm(r["CLASSIFICAÇÃO CONTRACEPÇÃO"]) == "SIM", norm(r["CLASSIFICAÇÃO VIOLÊNCIA SEXUAL"]) == "SIM",
         positivo(r["SMCON NEO"]) or positivo(r["SMCON OBST"]), norm(r["UNIDADE NEONATAL COMPLETA"]) in ("SIM", "NÃO SE APLICA")]
    return sum(f)


def estagio(n):
    return "Avançando" if n >= 5 else "Quase lá" if n == 4 else "No caminho" if n >= 2 else "Início da jornada"


comuns = [c for c in pl.index if c in ex.index]
assert len(comuns) == len(pl), "a extração precisa conter todas as unidades da planilha"
CLASSIF = lambda col: col.startswith("CLASSIFICAÇÃO") or col in ("UNIDADE NEONATAL COMPLETA", "HGPAR", "SMCON NEO", "SMCON OBST")

linhas, difs = [], []
for grupo, regra, cols in GRUPOS:
    for col in cols:
        if grupo == "Violência sexual" and not TEM_VIOL:
            linhas.append((grupo, regra, col, None, None, "", "", "extração sem SIA 2024 (pendente)")); continue
        if col == "CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS" and not TEM_VIOL:
            linhas.append((grupo, regra, col, None, None, "", "", "depende da violência sexual (pendente)")); continue
        ok = 0; exs = []; ganhou = perdeu = 0
        for c in comuns:
            a, b = pl.at[c, col], ex.at[c, col]
            if igual(a, b):
                ok += 1
            else:
                difs.append({"grupo": grupo, "coluna": col, "cnes": c, "estabelecimento": pl.at[c, "CNES - ESTABELECIMENTO"], "uf": pl.at[c, "UF"],
                             "planilha": a, "extracao": b})
                if len(exs) < 3:
                    exs.append(f"{c}: {norm(a)} × {norm(b)}")
                if CLASSIF(col) and col not in ("GESTÃO", "NATUREZA JURÍDICA"):
                    ganhou += (not positivo(a)) and positivo(b); perdeu += positivo(a) and (not positivo(b))
        num = pd.api.types.is_numeric_dtype(pl[col]) and not col.startswith("%") and not CLASSIF(col)
        soma = f"{pl.loc[comuns, col].sum():,.0f} × {ex.loc[comuns, col].sum():,.0f}".replace(",", ".") if num else ""
        mov = f"+{ganhou} / −{perdeu}" if (ganhou or perdeu) else ""
        linhas.append((grupo, regra, col, ok, len(comuns) - ok, soma, mov, "; ".join(exs)))
difs = pd.DataFrame(difs)
difs.to_csv(os.path.join(SAIDA, "extracao_2024_diferencas.csv"), index=False, encoding="utf-8-sig")

# ------------------------------------------------------------------ universo e partos nos dois recortes
tot_c25 = {c: R.partos(P, c, "c2025")["TOTAL"] for c in ex.index}
tot_i24 = {c: int(ex.at[c, "TOTAL"]) for c in ex.index}
so_ex = [c for c in ex.index if c not in pl.index]                      # > 1.000 por internação 2024, fora da planilha
abaixo = [c for c in comuns if tot_i24[c] <= 1000]                       # na planilha, ≤ 1.000 por internação 2024
iguais_c25 = sum(1 for c in comuns if tot_c25[c] == int(pl.at[c, "TOTAL"]))

# ------------------------------------------------------------------ unidade a unidade (lado a lado) e estágios
unid = []
for c in comuns:
    rp, re_ = pl.loc[c], ex.loc[c]
    d = {"CNES": c, "UF": rp["UF"], "Estabelecimento": rp["CNES - ESTABELECIMENTO"],
         "Partos planilha (comp. 2025)": int(rp["TOTAL"]), "Partos extração (intern. 2024)": tot_i24[c], "Dif. partos": tot_i24[c] - int(rp["TOTAL"]),
         "NV G1–G4 planilha": int(sum(rp[f"TOTAL NV G{g}"] for g in (1, 2, 3, 4))), "NV G1–G4 extração": int(sum(re_[f"TOTAL NV G{g}"] for g in (1, 2, 3, 4)))}
    for rot, col in (("Asfixia", "CLASSIFICAÇÃO ASFIXIA"), ("Enfermagem", "CLASSIFICAÇÃO PARTO ENF."), ("AMIU", "CLASSIFICAÇÃO AMIU"), ("Robson ≥2", "CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)"),
                     ("LARC", "CLASSIFICAÇÃO CONTRACEPÇÃO"), ("Violência", "CLASSIFICAÇÃO VIOLÊNCIA SEXUAL"), ("Neonatal", "UNIDADE NEONATAL COMPLETA")):
        d[f"{rot} planilha"] = norm(rp[col]); d[f"{rot} extração"] = norm(re_[col]) if (TEM_VIOL or rot != "Violência") else "pendente"
    d["Violência nº planilha"] = norm(rp[VIOL]); d["Violência nº extração (SIA)"] = norm(re_[VIOL]) if TEM_VIOL else "pendente"
    d["Adequados (de 8) planilha"] = n8(rp); d["Estágio planilha"] = estagio(d["Adequados (de 8) planilha"])
    if TEM_VIOL:
        d["Adequados (de 8) extração"] = n8(re_); d["Estágio extração"] = estagio(d["Adequados (de 8) extração"])
    d["Colunas diferentes"] = int((difs["cnes"] == c).sum()) if len(difs) else 0
    unid.append(d)
unid = pd.DataFrame(unid)
ORDEM = ["Avançando", "Quase lá", "No caminho", "Início da jornada"]
est_pl = collections.Counter(unid["Estágio planilha"]); est_ex = collections.Counter(unid["Estágio extração"]) if TEM_VIOL else None

# ------------------------------------------------------------------ relatório
f = lambda n: f"{n:,}".replace(",", ".")
md = ["# Extração de 2024 pelos microdados × planilha institucional de 2024\n",
      f"Planilha: `{os.path.basename(ARQ_PL)}` ({len(pl)} unidades). Extração: `{os.path.basename(ARQ_EX)}` ({len(ex)} unidades: as {len(pl)} da planilha "
      f"mais {len(so_ex)} que passam de 1.000 partos pela data de internação e não estão nela). Comparação unidade a unidade nas {len(comuns)} da planilha; "
      "a planilha **não é tratada como gabarito**.\n",
      "Regras da extração (as mesmas do painel de 2025): partos e AMIU pela **data de internação em 2024**; Robson, asfixia e enfermagem pelo SINASC 2024, "
      "com as DNV do complexo HC FAMEMA (2025523) somadas à unidade 2025507; unidade neonatal, gestão, natureza e HGPAR pelo CNES 03/2026; DIU e implante "
      "pelos atos da AIH com **data de saída em 2024**; violência sexual pelo **SIA/SUS** (0301040052 + 0301040060, quantidade aprovada, realização 2024); SMCON pela lista de 2024.\n",
      "## Resultado por coluna\n",
      "| Grupo | Coluna | Iguais | Diferentes | Soma planilha × extração | Classificação: ganha / perde | Exemplos (planilha × extração) |", "|---|---|---:|---:|---|---|---|"]
for g, regra, col, ok, dif, soma, mov, exs in linhas:
    md.append(f"| {g} | {col} | {'—' if ok is None else ok} | {'—' if dif is None else dif} | {soma} | {mov} | {exs} |")
md.append("\nRegra de cada grupo: " + " · ".join(f"**{g}**: {r}" for g, r, _ in GRUPOS) + ".\n")
md += ["## Universo e recorte de ano dos partos\n",
       f"- Pela **competência 2025** (regra que reproduz a planilha), o total de partos da extração é igual ao da planilha em **{iguais_c25} de {len(comuns)}** unidades.",
       f"- Pela **data de internação em 2024**, {f(sum(tot_i24[c] for c in comuns))} partos nas {len(comuns)} unidades da planilha, contra {f(int(pl['TOTAL'].sum()))} na planilha.",
       f"- **{len(abaixo)} unidades da planilha ficam com 1.000 partos ou menos** pela data de internação em 2024 e sairiam do universo; "
       f"**{len(so_ex)} unidades entrariam** (mais de 1.000 partos por internação e fora da planilha). Universo por internação 2024: {len(comuns) - len(abaixo) + len(so_ex)} unidades.\n"]
if TEM_VIOL:
    md += ["## Estágios de desempenho (nas unidades da planilha)\n", "| Estágio | Planilha | Extração |", "|---|---:|---:|"]
    md += [f"| {e} | {est_pl[e]} | {est_ex[e]} |" for e in ORDEM]
    mud = int((unid["Estágio planilha"] != unid["Estágio extração"]).sum())
    md.append(f"\n{mud} unidades mudam de estágio entre a planilha e a extração.\n")
else:
    md.append("## Estágios de desempenho\n\nPendente: dependem da violência sexual do SIA 2024, em tabulação.\n")
md.append("Arquivos: diferenças célula a célula em `extracao/saida/extracao_2024_diferencas.csv`; comparação lado a lado em `planilhas/COMPARACAO_2024_extracao_x_planilha.xlsx`.\n")
os.makedirs(os.path.join(RAIZ, "relatorios"), exist_ok=True)
open(os.path.join(RAIZ, "relatorios", "extracao_2024_x_planilha.md"), "w", encoding="utf-8", newline="\n").write("\n".join(md))

# ------------------------------------------------------------------ planilha de comparação
resumo = pd.DataFrame([{"Grupo": g, "Regra": r, "Coluna": c, "Iguais": ok, "Diferentes": d, "Soma planilha × extração": s, "Classificação: ganha / perde": m, "Exemplos": e}
                       for g, r, c, ok, d, s, m, e in linhas])
uni = pd.DataFrame([{"CNES": c, "Estabelecimento": ex.at[c, "CNES - ESTABELECIMENTO"], "UF": ex.at[c, "UF"], "Situação": "entraria (fora da planilha)",
                     "Partos por internação 2024": tot_i24[c], "Partos por competência 2025": tot_c25[c]} for c in so_ex] +
                   [{"CNES": c, "Estabelecimento": pl.at[c, "CNES - ESTABELECIMENTO"], "UF": pl.at[c, "UF"], "Situação": "sairia (≤ 1.000 por internação)",
                     "Partos por internação 2024": tot_i24[c], "Partos por competência 2025": tot_c25[c]} for c in abaixo])
with pd.ExcelWriter(os.path.join(RAIZ, "planilhas", "COMPARACAO_2024_extracao_x_planilha.xlsx"), engine="openpyxl") as w:
    resumo.to_excel(w, sheet_name="Resumo por coluna", index=False)
    unid.sort_values("Colunas diferentes", ascending=False).to_excel(w, sheet_name="Unidade a unidade", index=False)
    difs.to_excel(w, sheet_name="Diferenças (célula)", index=False)
    uni.sort_values(["Situação", "Partos por internação 2024"], ascending=[True, False]).to_excel(w, sheet_name="Universo", index=False)
    for ws in w.book.worksheets:
        ws.freeze_panes = "A2"
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = min(55, max(10, max(len(str(c.value or "")) for c in col[:50]) + 2))

print(f"unidades {len(comuns)} | diferenças (células) {len(difs)} | violência: {'SIA' if TEM_VIOL else 'pendente'}")
for g, regra, col, ok, dif, soma, mov, exs in linhas:
    print(f"  {g[:22]:22} | {col[:44]:44} | {'—' if ok is None else ok:>4} iguais | {'—' if dif is None else dif:>4} dif | {soma:>22} | {mov}")
print(f"partos por competência 2025 iguais à planilha: {iguais_c25}/{len(comuns)} | sairiam {len(abaixo)} | entrariam {len(so_ex)}")
