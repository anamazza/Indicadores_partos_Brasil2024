# -*- coding: utf-8 -*-
"""
relatorio_regional.py
Lê os agregados de regional.py (SINASC, extracao/saida/regional_<ano>.json) e de sim_regional.py (SIM,
extracao/saida/sim_regional_<ano>.json) e produz a comparação regional em quatro recortes:
  painel = unidades do painel · demais = demais estabelecimentos da região (região − painel) ·
  região = todos os NV/óbitos ocorridos na região · residência = NV/óbitos de residentes (população)
com IC 95 %, razão painel/demais, cesárea padronizada por Robson e mortalidade (neonatal, fetal, perinatal, materna).
Saídas: relatorios/comparacao_regional.md e planilhas/COMPARACAO_REGIONAL_<anos>.xlsx
Uso: python -X utf8 relatorio_regional.py 2024 2025
"""
import json, math, os, sys
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
ANOS = sys.argv[1:] or ["2024", "2025"]

REGIAO = {"1": "Norte", "2": "Nordeste", "3": "Sudeste", "4": "Sul", "5": "Centro-Oeste"}
ORDEM_REG = ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste", "Brasil"]
UF_NOME = {"11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO", "21": "MA", "22": "PI",
           "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA", "31": "MG", "32": "ES",
           "33": "RJ", "35": "SP", "41": "PR", "42": "SC", "43": "RS", "50": "MS", "51": "MT", "52": "GO", "53": "DF"}
RECORTES = ["painel", "demais", "ocorr", "resid"]
ROTULO = {"painel": "painel", "demais": "demais estab.", "ocorr": "região", "resid": "residência"}

# (chave, nome, numerador, denominador, escala, casas, bloco)
INDICADORES = [
    ("ces", "Cesariana (% dos partos)", "ces", "parto_inf", 100, 1, "sinasc"),
    ("pret", "Prematuridade < 37 semanas (% dos NV)", "pret", "ig_inf", 100, 1, "sinasc"),
    ("bp", "Baixo peso < 2.500 g (% dos NV)", "bp", "peso_inf", 100, 1, "sinasc"),
    ("mbp", "Muito baixo peso < 1.500 g (por 1.000 NV)", "mbp", "peso_inf", 1000, 1, "sinasc"),
    ("apg7", "Apgar no 5º minuto < 7 (por 1.000 NV com Apgar informado)", "apg7", "apg_inf", 1000, 1, "sinasc"),
    ("asf", "Asfixia com denominador restrito (regra da Coordenação, 2025): Apgar < 7 em NV ≥ 2.500 g sem anomalia (%)", "asf_num", "asf_den", 100, 2, "sinasc"),
    ("anom", "Anomalia congênita (por 10.000 NV)", "anom", "anom_inf", 10000, 1, "sinasc"),
    ("enf", "Parto vaginal assistido por enfermeira/obstetriz (%)", "enf_num", "enf_den", 100, 1, "sinasc"),
    ("adolesc", "Mãe adolescente < 20 anos (%)", "adolesc", "idade_inf", 100, 1, "sinasc"),
    ("idade35", "Mãe com 35 anos ou mais (%)", "idade35", "idade_inf", 100, 1, "sinasc"),
    ("pn7", "Pré-natal com 7 ou mais consultas (%)", "pn7", "pn_inf", 100, 1, "sinasc"),
    ("multipla", "Gestação múltipla (%)", "multipla", "grav_inf", 100, 2, "sinasc"),
    ("hosp", "Nascimento em hospital (% dos NV)", "hosp", "nv", 100, 1, "sinasc"),
    ("tmn", "Mortalidade neonatal 0–27 dias (por 1.000 NV)", "neo", "nv", 1000, 2, "sim"),
    ("tmnp", "Mortalidade neonatal precoce 0–6 dias (por 1.000 NV)", "neo_prec", "nv", 1000, 2, "sim"),
    ("tmnt", "Mortalidade neonatal tardia 7–27 dias (por 1.000 NV)", "neo_tard", "nv", 1000, 2, "sim"),
    ("tmi", "Mortalidade infantil < 1 ano (por 1.000 NV)", "inf", "nv", 1000, 2, "sim"),
    ("tmf", "Mortalidade fetal ≥ 22 semanas ou ≥ 500 g (por 1.000 nascimentos)", "fetal", "nasc_tot", 1000, 2, "sim"),
    ("tmp", "Mortalidade perinatal: fetais + 0–6 dias (por 1.000 nascimentos)", "perinatal", "nasc_tot", 1000, 2, "sim"),
    ("rmm", "Razão de mortalidade materna (por 100.000 NV)", "materno", "nv", 100000, 1, "sim"),
]
GRUPOS = list(range(1, 11)) + [0]


def wilson(k, n, z=1.96):
    if not n:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def razao(k1, n1, k2, n2, z=1.96):
    if not (k1 and n1 and k2 and n2):
        return (float("nan"),) * 3
    rr = (k1 / n1) / (k2 / n2)
    se = math.sqrt(1 / k1 - 1 / n1 + 1 / k2 - 1 / n2)
    return (rr, rr * math.exp(-z * se), rr * math.exp(z * se))


def fmt(x, casas=1):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def somar(cs):
    tot = {}
    for c in cs:
        for k, v in c.items():
            tot[k] = tot.get(k, 0) + v
    return tot


def subtrair(a, b):
    return {k: a.get(k, 0) - b.get(k, 0) for k in set(a) | set(b)}


def derivar(c):
    c["nasc_tot"] = c.get("nv", 0) + c.get("fetal", 0)
    c["perinatal"] = c.get("fetal", 0) + c.get("neo_prec", 0)
    return c


def por_regiao(recorte):
    out = {r: [] for r in REGIAO.values()}
    for uf, c in recorte.items():
        if uf[0] in REGIAO:
            out[REGIAO[uf[0]]].append(c)
    res = {r: somar(cs) for r, cs in out.items()}
    res["Brasil"] = somar(recorte.values())
    return res


dados = {}
for ano in ANOS:
    j = json.load(open(os.path.join(RAIZ, "extracao", "saida", f"regional_{ano}.json"), encoding="utf-8"))
    uf = {n: {u: dict(c) for u, c in r.items()} for n, r in j["recortes"].items()}
    meta = {"registros": j["registros"], "arquivo": j["arquivo"], "lista": j["lista"], "n_cnes": len(j["cnes_painel"])}
    psim = os.path.join(RAIZ, "extracao", "saida", f"sim_regional_{ano}.json")
    if os.path.exists(psim):
        s = json.load(open(psim, encoding="utf-8"))
        meta.update({"sim_do": s["registros_do"], "sim_dofet": s["registros_dofet"], "sim_diag": s["diagnostico"]})
        for n in ("ocorr", "resid", "painel"):
            for u, c in s["recortes"][n].items():
                uf[n].setdefault(u, {})
                for k, v in c.items():
                    uf[n][u][k] = uf[n][u].get(k, 0) + v
    uf["demais"] = {u: subtrair(uf["ocorr"][u], uf["painel"].get(u, {})) for u in uf["ocorr"]}
    for n in uf:
        for u in uf[n]:
            derivar(uf[n][u])
    reg = {n: {r: derivar(c) for r, c in por_regiao(uf[n]).items()} for n in uf}
    dados[ano] = {"meta": meta, "uf": uf, "reg": reg}
TEM_SIM = all("sim_do" in dados[a]["meta"] for a in ANOS)

base = dados[ANOS[0]]["reg"]["ocorr"]["Brasil"]
PESOS = {g: base.get(f"nv_g{g}", 0) / base["nv"] for g in GRUPOS}


def ces_padronizada(c):
    tx = 0.0
    for g in GRUPOS:
        nv = c.get(f"nv_g{g}", 0)
        if not nv:
            return float("nan")
        tx += PESOS[g] * c.get(f"ces_g{g}", 0) / nv
    return 100 * tx


# ------------------------------------------------------------------ tabelas longas
linhas, rob, cob = [], [], []
for ano in ANOS:
    D = dados[ano]
    for nivel, chaves in (("região", ORDEM_REG), ("UF", sorted(UF_NOME))):
        for ch in chaves:
            C = {n: (D["reg"][n].get(ch, {}) if nivel == "região" else D["uf"][n].get(ch, {})) for n in RECORTES}
            nome = ch if nivel == "região" else UF_NOME[ch]
            if nivel == "região":
                cob.append({"ano": ano, "região": ch, "NV nas unidades do painel": C["painel"].get("nv", 0),
                            "NV nos demais estabelecimentos": C["demais"].get("nv", 0),
                            "NV na região (ocorrência)": C["ocorr"].get("nv", 0), "NV de residentes": C["resid"].get("nv", 0),
                            "cobertura ocorrência (%)": 100 * C["painel"].get("nv", 0) / C["ocorr"]["nv"] if C["ocorr"].get("nv") else float("nan"),
                            "cobertura residência (%)": 100 * C["painel"].get("nv", 0) / C["resid"]["nv"] if C["resid"].get("nv") else float("nan")})
            for ch_i, nome_i, num, den, esc, casas, bloco in INDICADORES:
                if bloco == "sim" and not TEM_SIM:
                    continue
                reg = {"ano": ano, "nível": nivel, "território": nome, "indicador": nome_i, "chave": ch_i, "bloco": bloco, "escala": esc}
                for n in RECORTES:
                    k, d = C[n].get(num, 0), C[n].get(den, 0)
                    lo, hi = wilson(k, d)
                    reg[f"{n}_num"], reg[f"{n}_den"] = k, d
                    reg[n] = esc * k / d if d else float("nan")
                    reg[f"{n}_ic_inf"], reg[f"{n}_ic_sup"] = esc * lo, esc * hi
                rr, rlo, rhi = razao(C["painel"].get(num, 0), C["painel"].get(den, 0), C["demais"].get(num, 0), C["demais"].get(den, 0))
                reg["razão painel/demais"], reg["razão_ic_inf"], reg["razão_ic_sup"] = rr, rlo, rhi
                linhas.append(reg)
            if nivel == "região":
                for n in RECORTES:
                    Cn = C[n]
                    for g in GRUPOS:
                        nv, ces = Cn.get(f"nv_g{g}", 0), Cn.get(f"ces_g{g}", 0)
                        rob.append({"ano": ano, "região": ch, "recorte": ROTULO[n], "grupo de Robson": g if g else "não classificado",
                                    "NV": nv, "cesáreas": ces, "% dos NV": 100 * nv / Cn["nv"] if Cn.get("nv") else float("nan"),
                                    "% cesárea no grupo": 100 * ces / nv if nv else float("nan"),
                                    "contribuição à taxa de cesárea (p.p.)": 100 * ces / Cn["parto_inf"] if Cn.get("parto_inf") else float("nan")})
                    rob.append({"ano": ano, "região": ch, "recorte": ROTULO[n], "grupo de Robson": "TOTAL",
                                "NV": Cn.get("nv", 0), "cesáreas": Cn.get("ces", 0), "% dos NV": 100.0,
                                "% cesárea no grupo": 100 * Cn.get("ces", 0) / Cn["parto_inf"] if Cn.get("parto_inf") else float("nan"),
                                "contribuição à taxa de cesárea (p.p.)": float("nan"),
                                "cesárea padronizada por Robson (%)": ces_padronizada(Cn)})

df_all, df_rob, df_cob = pd.DataFrame(linhas), pd.DataFrame(rob), pd.DataFrame(cob)
df, df_uf = df_all[df_all["nível"] == "região"], df_all[df_all["nível"] == "UF"]

# ------------------------------------------------------------------ planilha
xlsx = os.path.join(RAIZ, "planilhas", f"COMPARACAO_REGIONAL_{'_'.join(ANOS)}.xlsx")
with pd.ExcelWriter(xlsx, engine="openpyxl") as w:
    df_cob.to_excel(w, sheet_name="Cobertura", index=False)
    df.to_excel(w, sheet_name="Por região", index=False)
    df_uf.to_excel(w, sheet_name="Por UF", index=False)
    df_rob.to_excel(w, sheet_name="Robson", index=False)
    pd.DataFrame([{"grupo de Robson": g if g else "não classificado", f"peso (Brasil ocorrência {ANOS[0]})": PESOS[g]} for g in GRUPOS]).to_excel(w, sheet_name="Pesos Robson", index=False)
    if TEM_SIM:
        pd.DataFrame([{"ano": a, **{k: v for k, v in dados[a]["meta"]["sim_diag"].items()}} for a in ANOS]).to_excel(w, sheet_name="Diagnóstico SIM", index=False)
    for ws in w.book.worksheets:
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = min(60, max(10, max(len(str(c.value or "")) for c in col[:50]) + 2))
        ws.freeze_panes = "A2"


# ------------------------------------------------------------------ markdown
def linha_ind(ch_i, r, cols):
    cel = []
    for a in ANOS:
        x = df[(df.ano == a) & (df["território"] == r) & (df.chave == ch_i)].iloc[0]
        casas = next(i[5] for i in INDICADORES if i[0] == ch_i)
        for c in cols:
            if c == "razao":
                cel.append(f"{fmt(x['razão painel/demais'], 2)} [{fmt(x['razão_ic_inf'], 2)}–{fmt(x['razão_ic_sup'], 2)}]")
            elif c.endswith("_ic"):
                n = c[:-3]
                cel.append(f"{fmt(x[n], casas)} [{fmt(x[f'{n}_ic_inf'], casas)}–{fmt(x[f'{n}_ic_sup'], casas)}]")
            else:
                cel.append(fmt(x[c], casas))
    return f"| {r} | " + " | ".join(cel) + " |"


def cab(cols):
    def rot(c):
        if c == "razao":
            return "razão painel/demais [IC]"
        if c.endswith("_ic"):
            return ROTULO[c[:-3]] + " [IC]"
        return ROTULO[c]
    return "| Região | " + " | ".join(f"{a} {rot(c)}" for a in ANOS for c in cols) + " |\n|---|" + "---|" * (len(cols) * len(ANOS))


L = []
L.append(f"# Comparação regional: unidades do painel, demais estabelecimentos e região ({' e '.join(ANOS)})\n")
L.append("Protótipo gerado pelos scripts `scripts/extracao/regional.py` (SINASC completo), `scripts/extracao/sim_regional.py` (SIM: DO de todas as UFs e DOFET) "
         "e `scripts/extracao/relatorio_regional.py`. Cada região é analisada em quatro recortes: **painel**, estabelecimentos (CNES) da planilha do ano, incluídos os códigos "
         "antigos e os complexos somados pelo painel, por UF de ocorrência; **demais estab.**, nascidos vivos (NV) e óbitos ocorridos na região fora dessas unidades (região − painel); "
         "**região**, todos os NV e óbitos ocorridos na região; **residência**, NV e óbitos de residentes da região, independentemente do local de ocorrência (base para prevalência "
         "e incidência populacionais). Os intervalos de confiança de 95 % (IC 95 %) são de Wilson; o IC da razão painel/demais é calculado na escala logarítmica. "
         "p.p. = pontos percentuais.\n")
for ano in ANOS:
    m = dados[ano]["meta"]
    s = f"- **{ano}:** {fmt(m['registros'], 0)} NV no `{m['arquivo']}`; lista do painel `{m['lista']}` ({m['n_cnes']} códigos CNES, incluídos códigos antigos e complexos)"
    if "sim_do" in m:
        s += f"; SIM: {fmt(m['sim_do'], 0)} DO (27 UFs) e {fmt(m['sim_dofet'], 0)} DOFET"
    L.append(s + ".")
L.append("")
L.append("## 1. Cobertura: proporção dos nascimentos da região ocorridos nas unidades do painel\n")
L.append("| Região | " + " | ".join(f"{a} NV painel | {a} NV demais | {a} NV região | {a} cobertura" for a in ANOS) + " |")
L.append("|---|" + "---|" * (4 * len(ANOS)))
for r in ORDEM_REG:
    cel = []
    for a in ANOS:
        x = df_cob[(df_cob.ano == a) & (df_cob["região"] == r)].iloc[0]
        cel += [fmt(x["NV nas unidades do painel"], 0), fmt(x["NV nos demais estabelecimentos"], 0), fmt(x["NV na região (ocorrência)"], 0), fmt(x["cobertura ocorrência (%)"]) + " %"]
    L.append(f"| {r} | " + " | ".join(cel) + " |")
L.append("")
L.append("## 2. Indicadores do SINASC por região: unidades do painel e demais estabelecimentos\n")
L.append("Cada tabela apresenta o valor nas unidades do painel, o valor nos demais estabelecimentos da região e a razão painel/demais, com o IC 95 % entre colchetes. "
         "Razão > 1 indica frequência maior nas unidades do painel. Os valores da região como um todo e por residência estão na planilha (abas \"Por região\" e \"Por UF\").\n")
COLS2 = ["painel", "demais", "razao"]
for ch_i, nome_i, *_ , bloco in INDICADORES:
    if bloco != "sinasc":
        continue
    L.append(f"### {nome_i}\n")
    L.append(cab(COLS2))
    for r in ORDEM_REG:
        L.append(linha_ind(ch_i, r, COLS2))
    L.append("")
L.append("## 3. Indicadores por local de residência\n")
L.append("Indicadores selecionados, calculados pelo município de residência da mãe; recorte adequado para estimar prevalência e incidência na população da região.\n")
sel = ["ces", "pret", "bp", "apg7", "anom", "adolesc", "pn7"]
for a in ANOS:
    L.append(f"### {a}\n")
    L.append("| Região | " + " | ".join(next(i[1] for i in INDICADORES if i[0] == s).split(" (")[0] for s in sel) + " |")
    L.append("|---|" + "---|" * len(sel))
    for r in ORDEM_REG:
        cel = []
        for s in sel:
            x = df[(df.ano == a) & (df["território"] == r) & (df.chave == s)].iloc[0]
            casas = next(i[5] for i in INDICADORES if i[0] == s)
            cel.append(f"{fmt(x['resid'], casas)} [{fmt(x['resid_ic_inf'], casas)}–{fmt(x['resid_ic_sup'], casas)}]")
        L.append(f"| {r} | " + " | ".join(cel) + " |")
    L.append("")
L.append("## 4. Taxa de cesariana bruta e padronizada pelos grupos de Robson\n")
L.append(f"Padronização direta, com pesos dados pela distribuição dos grupos de Robson no Brasil (local de ocorrência, {ANOS[0]}). "
         "A padronização remove da comparação o efeito das diferenças de perfil obstétrico.\n")
L.append("| Região | " + " | ".join(f"{a} painel bruta | {a} painel padronizada | {a} demais bruta | {a} demais padronizada" for a in ANOS) + " |")
L.append("|---|" + "---|" * (4 * len(ANOS)))
for r in ORDEM_REG:
    cel = []
    for a in ANOS:
        for rec in ("painel", "demais estab."):
            x = df_rob[(df_rob.ano == a) & (df_rob["região"] == r) & (df_rob.recorte == rec) & (df_rob["grupo de Robson"] == "TOTAL")].iloc[0]
            cel += [fmt(x["% cesárea no grupo"]), fmt(x["cesárea padronizada por Robson (%)"])]
    L.append(f"| {r} | " + " | ".join(cel) + " |")
L.append("")
ult = ANOS[-1]
L.append(f"### Cesariana por grupo de Robson, Brasil, {ult}: unidades do painel e demais estabelecimentos\n")
L.append("| Grupo | % dos NV (painel) | % dos NV (demais) | % cesariana (painel) | % cesariana (demais) | contribuição em p.p. (painel) | contribuição em p.p. (demais) |")
L.append("|---|---|---|---|---|---|---|")
for g in GRUPOS:
    gl = g if g else "não classificado"
    p = df_rob[(df_rob.ano == ult) & (df_rob["região"] == "Brasil") & (df_rob.recorte == "painel") & (df_rob["grupo de Robson"] == gl)].iloc[0]
    o = df_rob[(df_rob.ano == ult) & (df_rob["região"] == "Brasil") & (df_rob.recorte == "demais estab.") & (df_rob["grupo de Robson"] == gl)].iloc[0]
    L.append(f"| {gl} | {fmt(p['% dos NV'])} | {fmt(o['% dos NV'])} | {fmt(p['% cesárea no grupo'])} | {fmt(o['% cesárea no grupo'])} | "
             f"{fmt(p['contribuição à taxa de cesárea (p.p.)'])} | {fmt(o['contribuição à taxa de cesárea (p.p.)'])} |")
L.append("")
if TEM_SIM:
    L.append("## 5. Mortalidade (SIM): unidades do painel, demais estabelecimentos e residência\n")
    L.append("Óbitos registrados no SIM (DO de todas as UFs e DOFET), segundo as regras auditadas no processamento da mortalidade (fichas IDB C.1.4, C.1.1, C.1.2, C.2 e C.3; óbito materno pela "
             "regra do MS/OOBr). Nos recortes painel e demais estab., o numerador é o óbito ocorrido no estabelecimento (CODESTAB) e o denominador são os NV nascidos no mesmo "
             "estabelecimento. Maternidades com UTI neonatal de referência recebem recém-nascidos (RN) de outros serviços, e a DO não informa o local de nascimento; por isso, "
             "a razão painel/demais superestima a mortalidade nas unidades do painel. A coluna residência (óbitos de residentes ÷ NV de residentes) corresponde à taxa "
             "populacional da região e não está sujeita a esse viés.\n")
    COLS5 = ["painel", "demais", "razao", "resid_ic"]
    for ch_i, nome_i, *_ , bloco in INDICADORES:
        if bloco != "sim":
            continue
        cols = ["resid_ic"] if ch_i == "tmi" else COLS5     # infantil: só faz sentido por residência
        L.append(f"### {nome_i}\n")
        if ch_i == "tmi":
            L.append("Só por residência: o óbito infantil raramente ocorre no estabelecimento do nascimento.\n")
        L.append(cab(cols))
        for r in ORDEM_REG:
            L.append(linha_ind(ch_i, r, cols))
        L.append("")
    L.append("Número de óbitos (Brasil, por local de ocorrência):\n")
    L.append("| Ano | Neonatais (0–27 dias) | Neonatais precoces (0–6 dias) | Neonatais tardios (7–27 dias) | Infantis (< 1 ano) | Fetais (≥ 22 semanas ou ≥ 500 g) | "
             "Fetais sem IG e sem peso | Maternos (regra MS/OOBr) | Maternos tardios (O96–O97) |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for a in ANOS:
        b = dados[a]["reg"]["ocorr"]["Brasil"]
        L.append(f"| {a} | " + " | ".join(fmt(b.get(k, 0), 0) for k in ("neo", "neo_prec", "neo_tard", "inf", "fetal", "fetal_ign", "materno", "materno_tardio")) + " |")
    L.append("")
    # conferência externa: TabNet/DATASUS (Mortalidade: óbitos de mulheres em idade fértil e óbitos maternos, mat10uf), por UF de residência
    ptab = os.path.join(RAIZ, "extracao", "saida", "tabnet_mat_2024_2025.json")
    if os.path.exists(ptab):
        T = json.load(open(ptab, encoding="utf-8"))
        L.append("Conferência com o TabNet/DATASUS (óbitos maternos e óbitos de mulheres em idade fértil, por UF de residência; arquivos matuf<aa>; consulta de 09/11/2026):\n")
        L.append("| Ano | Indicador | Protótipo | TabNet | UFs iguais / comparadas |")
        L.append("|---|---|---|---|---|")
        for a in ANOS:
            R_ = dados[a]["uf"]["resid"]
            for chave, inc, rot in (("materno", "Óbitos_maternos", "Óbitos maternos (regra MS)"), ("mif", "Óbitos_mulheres_idade_fértil", "Óbitos de mulheres de 10 a 49 anos"),
                                    ("materno_tardio", "Óbitos_maternos_tardios", "Óbitos maternos tardios (O96 e O97)")):
                tb = T.get(f"{a}|{inc}|UF")
                if not tb:
                    continue
                tuf = {k[:2]: int(v) for k, v in tb.items() if k[:2].isdigit()}
                iguais = sum(1 for uf, v in tuf.items() if R_.get(uf, {}).get(chave, 0) == v)
                meu = sum(c.get(chave, 0) for c in R_.values())
                L.append(f"| {a} | {rot} | {fmt(meu, 0)} | {fmt(int(tb['Total']), 0)} | {iguais} / {len(tuf)} |")
        L.append("")
        L.append("Os óbitos maternos tardios diferem porque o TabNet os restringe a mulheres de 10 a 49 anos (só essas faixas aparecem na tabulação) e o protótipo conta todas as idades; "
                 "eles não entram na razão de mortalidade materna. Nas UFs em que o TabNet não lista óbitos tardios, a comparação não é feita.\n")
sec = 6 if TEM_SIM else 5
L.append(f"## {sec}. Interpretação e limitações\n")
L.append("- As unidades do painel são maternidades de maior porte (mais de 1.000 partos pelo SUS no ano) e, em grande parte, referência para alto risco; "
         "concentram prematuridade, baixo peso, Apgar baixo, anomalias e, por consequência, óbitos neonatais da região. Nesses indicadores, razão > 1 reflete principalmente "
         "a seleção de casos e as transferências e não deve ser lida como medida de qualidade assistencial.")
L.append("- O recorte \"demais estabelecimentos\" reúne hospitais privados sem atendimento pelo SUS, hospitais do SUS com até 1.000 partos no ano e partos fora de hospital; "
         "é, portanto, um grupo heterogêneo.")
L.append("- Os recortes por residência e por ocorrência divergem onde há deslocamento de gestantes para o parto (Norte, interior do Nordeste e entorno do DF). "
         "Para prevalência e incidência populacionais, devem ser usadas as colunas de residência.")
L.append(f"- Os dados de {ANOS[-1]} são preliminares (SINASC de 31/08/2026; SIM preliminar). O número de óbitos, em especial os maternos, ainda aumenta com a investigação e "
         "com a inclusão tardia de registros. Registros com Apgar, peso ou idade gestacional ignorados foram excluídos dos denominadores; óbitos fetais sem IG e sem peso foram "
         "excluídos do numerador e do denominador (quantidade na tabela de número de óbitos, acima).")
L.append("- Taxas com denominador populacional (por 100.000 mulheres ou por 1.000 mulheres em idade fértil) dependem de estimativas populacionais do IBGE e não foram calculadas.")
L.append(f"\nPlanilha completa (abas Cobertura, Por região, Por UF, Robson, Pesos Robson{', Diagnóstico SIM' if TEM_SIM else ''}): `planilhas/{os.path.basename(xlsx)}`.")
open(os.path.join(RAIZ, "relatorios", "comparacao_regional.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("ok:", xlsx, "e relatorios/comparacao_regional.md", "| SIM incluído" if TEM_SIM else "| sem SIM")
