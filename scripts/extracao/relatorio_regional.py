# -*- coding: utf-8 -*-
"""
relatorio_regional.py
Lê os agregados de regional.py (extracao/saida/regional_<ano>.json) e produz a comparação regional:
unidades do painel x conjunto da região (ocorrência) x residência, com IC 95 % e razão painel/região,
mais a taxa de cesárea padronizada pela distribuição de Robson do Brasil (ocorrência, 2024).
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

# (chave, nome, numerador, denominador, escala, casas)
INDICADORES = [
    ("ces", "Cesárea (% dos partos)", "ces", "parto_inf", 100, 1),
    ("pret", "Prematuridade < 37 semanas (% dos NV)", "pret", "ig_inf", 100, 1),
    ("bp", "Baixo peso < 2.500 g (% dos NV)", "bp", "peso_inf", 100, 1),
    ("mbp", "Muito baixo peso < 1.500 g (por 1.000 NV)", "mbp", "peso_inf", 1000, 1),
    ("apg7", "Apgar 5º min < 7 (por 1.000 NV com Apgar informado)", "apg7", "apg_inf", 1000, 1),
    ("asf", "Asfixia, regra do painel: Apgar < 7 em NV ≥ 2.500 g sem anomalia (%)", "asf_num", "asf_den", 100, 2),
    ("anom", "Anomalia congênita (por 10.000 NV)", "anom", "anom_inf", 10000, 1),
    ("enf", "Parto vaginal assistido por enfermeira/obstetriz (%)", "enf_num", "enf_den", 100, 1),
    ("adolesc", "Mãe adolescente < 20 anos (%)", "adolesc", "idade_inf", 100, 1),
    ("idade35", "Mãe com 35 anos ou mais (%)", "idade35", "idade_inf", 100, 1),
    ("pn7", "Pré-natal com 7 ou mais consultas (%)", "pn7", "pn_inf", 100, 1),
    ("multipla", "Gestação múltipla (%)", "multipla", "grav_inf", 100, 2),
    ("hosp", "Nascimento em hospital (% dos NV)", "hosp", "nv", 100, 1),
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


def por_regiao(recorte):
    """{região: contadores} a partir de {uf: contadores}; 'Brasil' inclui UF ignorada."""
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
    dados[ano] = {"meta": {k: j[k] for k in ("registros", "arquivo", "lista")}, "n_cnes": len(j["cnes_painel"]),
                  "uf": j["recortes"], "reg": {n: por_regiao(r) for n, r in j["recortes"].items()}}

# pesos de padronização: distribuição de Robson do Brasil (ocorrência) no primeiro ano
base = dados[ANOS[0]]["reg"]["ocorr"]["Brasil"]
PESOS = {g: base.get(f"nv_g{g}", 0) / base["nv"] for g in GRUPOS}


def ces_padronizada(c):
    tx = 0.0
    for g in GRUPOS:
        nv = c.get(f"nv_g{g}", 0)
        if nv:
            tx += PESOS[g] * c.get(f"ces_g{g}", 0) / nv
        else:
            return float("nan")
    return 100 * tx


# ------------------------------------------------------------------ tabelas longas
linhas, linhas_uf, rob, cob = [], [], [], []
for ano in ANOS:
    D = dados[ano]
    for nivel, chaves in (("região", ORDEM_REG), ("UF", sorted(UF_NOME))):
        for ch in chaves:
            if nivel == "região":
                P, O, Rr = (D["reg"][n].get(ch, {}) for n in ("painel", "ocorr", "resid"))
                nome = ch
            else:
                P, O, Rr = (D["uf"][n].get(ch, {}) for n in ("painel", "ocorr", "resid"))
                nome = UF_NOME[ch]
            if nivel == "região":
                cob.append({"ano": ano, "região": ch, "NV nas unidades do painel": P.get("nv", 0),
                            "NV na região (ocorrência)": O.get("nv", 0), "NV de residentes": Rr.get("nv", 0),
                            "cobertura ocorrência (%)": 100 * P.get("nv", 0) / O["nv"] if O.get("nv") else float("nan"),
                            "cobertura residência (%)": 100 * P.get("nv", 0) / Rr["nv"] if Rr.get("nv") else float("nan")})
            for ch_i, nome_i, num, den, esc, casas in INDICADORES:
                k1, n1, k2, n2, k3, n3 = P.get(num, 0), P.get(den, 0), O.get(num, 0), O.get(den, 0), Rr.get(num, 0), Rr.get(den, 0)
                lo1, hi1 = wilson(k1, n1); lo2, hi2 = wilson(k2, n2); lo3, hi3 = wilson(k3, n3)
                rr, rlo, rhi = razao(k1, n1, k2, n2)
                reg = {"ano": ano, "nível": nivel, "território": nome, "indicador": nome_i, "chave": ch_i, "escala": esc,
                       "painel_num": k1, "painel_den": n1, "painel": esc * k1 / n1 if n1 else float("nan"),
                       "painel_ic_inf": esc * lo1, "painel_ic_sup": esc * hi1,
                       "região_num": k2, "região_den": n2, "região": esc * k2 / n2 if n2 else float("nan"),
                       "região_ic_inf": esc * lo2, "região_ic_sup": esc * hi2,
                       "residência_num": k3, "residência_den": n3, "residência": esc * k3 / n3 if n3 else float("nan"),
                       "residência_ic_inf": esc * lo3, "residência_ic_sup": esc * hi3,
                       "razão painel/região": rr, "razão_ic_inf": rlo, "razão_ic_sup": rhi}
                (linhas if nivel == "região" else linhas_uf).append(reg)
            if nivel == "região":
                for rec_nome, C in (("painel", P), ("região (ocorrência)", O), ("residência", Rr)):
                    for g in GRUPOS:
                        nv, ces = C.get(f"nv_g{g}", 0), C.get(f"ces_g{g}", 0)
                        rob.append({"ano": ano, "região": ch, "recorte": rec_nome, "grupo de Robson": g if g else "não classificado",
                                    "NV": nv, "cesáreas": ces, "% dos NV": 100 * nv / C["nv"] if C.get("nv") else float("nan"),
                                    "% cesárea no grupo": 100 * ces / nv if nv else float("nan"),
                                    "contribuição à taxa de cesárea (p.p.)": 100 * ces / C["parto_inf"] if C.get("parto_inf") else float("nan")})
                    rob.append({"ano": ano, "região": ch, "recorte": rec_nome, "grupo de Robson": "TOTAL",
                                "NV": C.get("nv", 0), "cesáreas": C.get("ces", 0), "% dos NV": 100.0,
                                "% cesárea no grupo": 100 * C.get("ces", 0) / C["parto_inf"] if C.get("parto_inf") else float("nan"),
                                "contribuição à taxa de cesárea (p.p.)": float("nan"),
                                "cesárea padronizada por Robson (%)": ces_padronizada(C)})

df, df_uf, df_rob, df_cob = pd.DataFrame(linhas), pd.DataFrame(linhas_uf), pd.DataFrame(rob), pd.DataFrame(cob)

# ------------------------------------------------------------------ planilha
xlsx = os.path.join(RAIZ, "planilhas", f"COMPARACAO_REGIONAL_{'_'.join(ANOS)}.xlsx")
with pd.ExcelWriter(xlsx, engine="openpyxl") as w:
    df_cob.to_excel(w, sheet_name="Cobertura", index=False)
    df.to_excel(w, sheet_name="Por região", index=False)
    df_uf.to_excel(w, sheet_name="Por UF", index=False)
    df_rob.to_excel(w, sheet_name="Robson", index=False)
    pd.DataFrame([{"grupo de Robson": g if g else "não classificado", "peso (Brasil ocorrência %s)" % ANOS[0]: PESOS[g]} for g in GRUPOS]).to_excel(w, sheet_name="Pesos Robson", index=False)
    for ws in w.book.worksheets:
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = min(60, max(10, max(len(str(c.value or "")) for c in col[:50]) + 2))
        ws.freeze_panes = "A2"

# ------------------------------------------------------------------ markdown
L = []
L.append(f"# Comparação regional — unidades do painel × conjunto da região ({' e '.join(ANOS)})\n")
L.append("Protótipo gerado por `scripts/extracao/regional.py` e `scripts/extracao/relatorio_regional.py` a partir do SINASC completo "
         "(todos os estabelecimentos). **Unidades do painel** = CNES da planilha do ano (mais os CNES antigos/complexos que o painel soma), "
         "por UF de ocorrência. **Região** = todos os nascidos vivos ocorridos na região, em qualquer estabelecimento ou domicílio. "
         "**Residência** = nascidos vivos de mães residentes na região, onde quer que tenham nascido (prevalência populacional). "
         "IC 95 % de Wilson para as proporções; a razão painel/região usa o IC pelo logaritmo.\n")
for ano in ANOS:
    m = dados[ano]["meta"]
    L.append(f"- **{ano}:** {m['registros']:,} NV no `{m['arquivo']}`; lista do painel `{m['lista']}` ({dados[ano]['n_cnes']} CNES com apelidos).".replace(",", "."))
L.append("")
L.append("## 1. Cobertura: quanto dos nascimentos da região acontece nas unidades do painel\n")
L.append("| Região | " + " | ".join(f"{a} NV painel | {a} NV região | {a} cobertura" for a in ANOS) + " |")
L.append("|---|" + "---|" * (3 * len(ANOS)))
for r in ORDEM_REG:
    cel = []
    for a in ANOS:
        x = df_cob[(df_cob.ano == a) & (df_cob["região"] == r)].iloc[0]
        cel += [fmt(x["NV nas unidades do painel"], 0), fmt(x["NV na região (ocorrência)"], 0), fmt(x["cobertura ocorrência (%)"]) + " %"]
    L.append(f"| {r} | " + " | ".join(cel) + " |")
L.append("")
L.append("## 2. Indicadores por região: painel × região (ocorrência) e razão\n")
L.append("Valor do painel, valor da região e razão painel/região [IC 95 %]. Razão > 1: o indicador é mais frequente nas unidades do painel do que no conjunto da região.\n")
for ch_i, nome_i, num, den, esc, casas in INDICADORES:
    L.append(f"### {nome_i}\n")
    L.append("| Região | " + " | ".join(f"{a} painel | {a} região | {a} razão [IC]" for a in ANOS) + " |")
    L.append("|---|" + "---|" * (3 * len(ANOS)))
    for r in ORDEM_REG:
        cel = []
        for a in ANOS:
            x = df[(df.ano == a) & (df["território"] == r) & (df.chave == ch_i)].iloc[0]
            cel += [fmt(x["painel"], casas), fmt(x["região"], casas),
                    f"{fmt(x['razão painel/região'], 2)} [{fmt(x['razão_ic_inf'], 2)}–{fmt(x['razão_ic_sup'], 2)}]"]
        L.append(f"| {r} | " + " | ".join(cel) + " |")
    L.append("")
L.append("## 3. Prevalência por residência (toda a população da região)\n")
L.append("Mesmos indicadores pelo local de residência da mãe — é o denominador correto para falar de prevalência/incidência na população da região.\n")
sel = ["ces", "pret", "bp", "apg7", "anom", "adolesc", "pn7"]
for a in ANOS:
    L.append(f"**{a}**\n")
    L.append("| Região | " + " | ".join(next(i[1] for i in INDICADORES if i[0] == s).split(" (")[0] for s in sel) + " |")
    L.append("|---|" + "---|" * len(sel))
    for r in ORDEM_REG:
        cel = []
        for s in sel:
            x = df[(df.ano == a) & (df["território"] == r) & (df.chave == s)].iloc[0]
            casas = next(i[5] for i in INDICADORES if i[0] == s)
            cel.append(f"{fmt(x['residência'], casas)} [{fmt(x['residência_ic_inf'], casas)}–{fmt(x['residência_ic_sup'], casas)}]")
        L.append(f"| {r} | " + " | ".join(cel) + " |")
    L.append("")
L.append("## 4. Cesárea: bruta × padronizada pela distribuição de Robson\n")
L.append(f"Padronização direta: taxa de cesárea de cada grupo de Robson do território, ponderada pela distribuição dos grupos no Brasil "
         f"(ocorrência, {ANOS[0]}). Remove o efeito do perfil obstétrico (mais cesárea anterior, mais indução etc.) na comparação.\n")
L.append("| Região | " + " | ".join(f"{a} painel bruta | {a} painel padron. | {a} região bruta | {a} região padron." for a in ANOS) + " |")
L.append("|---|" + "---|" * (4 * len(ANOS)))
for r in ORDEM_REG:
    cel = []
    for a in ANOS:
        for rec in ("painel", "região (ocorrência)"):
            x = df_rob[(df_rob.ano == a) & (df_rob["região"] == r) & (df_rob.recorte == rec) & (df_rob["grupo de Robson"] == "TOTAL")].iloc[0]
            cel += [fmt(x["% cesárea no grupo"]), fmt(x["cesárea padronizada por Robson (%)"])]
    L.append(f"| {r} | " + " | ".join(cel) + " |")
L.append("")
ult = ANOS[-1]
L.append(f"### Cesárea por grupo de Robson, Brasil {ult}: painel × região\n")
L.append("| Grupo | % dos NV (painel) | % dos NV (região) | % cesárea (painel) | % cesárea (região) | contribuição p.p. (painel) | contribuição p.p. (região) |")
L.append("|---|---|---|---|---|---|---|")
for g in GRUPOS:
    gl = g if g else "não classificado"
    p = df_rob[(df_rob.ano == ult) & (df_rob["região"] == "Brasil") & (df_rob.recorte == "painel") & (df_rob["grupo de Robson"] == gl)].iloc[0]
    o = df_rob[(df_rob.ano == ult) & (df_rob["região"] == "Brasil") & (df_rob.recorte == "região (ocorrência)") & (df_rob["grupo de Robson"] == gl)].iloc[0]
    L.append(f"| {gl} | {fmt(p['% dos NV'])} | {fmt(o['% dos NV'])} | {fmt(p['% cesárea no grupo'])} | {fmt(o['% cesárea no grupo'])} | "
             f"{fmt(p['contribuição à taxa de cesárea (p.p.)'])} | {fmt(o['contribuição à taxa de cesárea (p.p.)'])} |")
L.append("")
L.append("## 5. Leitura e limites\n")
L.append("- As unidades do painel são maternidades de maior porte (> 1.000 partos SUS) e, em grande parte, referência para alto risco; "
         "espera-se que concentrem prematuridade, baixo peso, Apgar baixo e anomalias da região (razão > 1). Isso é efeito de seleção, não de qualidade.")
L.append("- A região (ocorrência) inclui a própria rede do painel; a comparação mais limpa seria painel × *demais* estabelecimentos, "
         "que se obtém por subtração (os numeradores e denominadores estão na planilha).")
L.append("- Residência × ocorrência divergem onde há migração para parir (Norte, interior do Nordeste, entorno do DF). Para prevalência populacional use a seção 3.")
L.append(f"- {ANOS[-1]} é SINASC preliminar; os valores mudam a cada versão. Apgar, peso e idade gestacional ignorados foram excluídos dos denominadores.")
L.append("- Mortalidade (neonatal, materna) e taxas por população (por 100 mil mulheres) não estão aqui: exigem SIM e estimativas populacionais do IBGE.")
L.append(f"\nPlanilha completa (por região, por UF, Robson, cobertura): `planilhas/{os.path.basename(xlsx)}`.")
open(os.path.join(RAIZ, "relatorios", "comparacao_regional.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("ok:", xlsx, "e relatorios/comparacao_regional.md")
