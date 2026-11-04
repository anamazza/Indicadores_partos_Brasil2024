# -*- coding: utf-8 -*-
"""
reproducao_2024.py
Recalcula, a partir dos microdados (SINASC, SIH-RD, SIH-SP, CNES), todas as colunas da planilha
ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024 e compara CNES a CNES, gerando o relatório
relatorios/reproducao_2024.md e a tabela de diferenças extracao/saida/reproducao_2024_diferencas.csv.
Uso: python reproducao_2024.py <planilha_2024.xlsx>
Pré-requisitos (saídas em extracao/saida/): sinasc_2024.json, sih_rd/*.json, cnes_leitos_2401_2603.json,
cnes_fichas.json e, se existirem, sih_sp/*.json com os códigos de DIU/implante/violência em codigos_sp.json.
"""
import collections, json, os, sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import regras as R

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAIDA = os.path.join(RAIZ, "extracao", "saida")
ARQ = sys.argv[1]
ATRIB_PARTO, ATRIB_AMIU, COMP_CNES = "c2025", "s2024", "2603"

df = pd.read_excel(ARQ)
# chave = CNES do rótulo "CNES - ESTABELECIMENTO": em 2 linhas a coluna CNES traz o código antigo
# (2679663→9131922, 3511251→5878640) e os dados dos sistemas estão no código novo
df["_cnes"] = df["CNES - ESTABELECIMENTO"].str.extract(r"^(\d+)")[0].str.zfill(7)
S = json.load(open(os.path.join(SAIDA, "sinasc_2024.json"), encoding="utf-8"))["estabelecimentos"]
P = R.carregar_uf_json(os.path.join(SAIDA, "sih_rd"), "procedimentos")
LJ = json.load(open(os.path.join(SAIDA, f"cnes_leitos_2401_{COMP_CNES}.json"), encoding="utf-8"))
L, CAD = LJ["leitos"], LJ["cadastro"]
F = json.load(open(os.path.join(SAIDA, "cnes_fichas.json"), encoding="utf-8"))
codigos_sp = os.path.join(SAIDA, "codigos_sp.json")
SP = R.carregar_uf_json(os.path.join(SAIDA, "sih_sp"), "linhas") if os.path.exists(codigos_sp) else None
CSP = json.load(open(codigos_sp, encoding="utf-8")) if SP else None

recs = []
for _, r in df.iterrows():
    c = r["_cnes"]
    rec = {"CNES": c}
    rec.update(R.partos(P, c, ATRIB_PARTO))
    rec["% AMIU"], rec["_amiu"], rec["_curet"] = R.amiu(P, c, ATRIB_AMIU)
    rec.update(R.sinasc(S, c))
    rec["UNIDADE NEONATAL COMPLETA"] = R.neonatal(L, c, COMP_CNES)
    rec["GESTÃO"], rec["NATUREZA JURÍDICA"] = R.gestao_natureza(CAD, c)
    rec["HGPAR"] = R.hgpar(F, c)
    # colunas do SIH-SP: recalculadas quando o código foi identificado; senão, copiadas da planilha (não reproduzidas)
    for col in ("DIU", "IMPLANTE ", "Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL"):
        spec = (CSP or {}).get(col)
        rec[col] = sum(SP.get(c, {}).get(f"{code}|{spec['atrib']}", 0) for code in spec["codigos"]) if spec else r[col]
    R.classificar(rec, str(r["SMCON NEO"]).strip() == "ok", str(r["SMCON OBST"]).strip() == "ok")
    recs.append(rec)
calc = pd.DataFrame(recs).set_index("CNES")
calc.to_csv(os.path.join(SAIDA, "reproducao_2024_recalculo.csv"), encoding="utf-8-sig")

# ------------------------------------------------------------------ comparação
GRUPOS = [
    ("SIH — partos (AIH por competência 2025)", list(R.PARTO_COLS.values()) + ["TOTAL", "TOTAL S/ CPN"]),
    ("SIH — AMIU (ano pela data de saída 2024)", ["% AMIU", "CLASSIFICAÇÃO AMIU"]),
    ("SINASC 2024 — Robson", [f"{p} G{g}" for g in (1, 2, 3, 4) for p in ("TOTAL NV", "Nº CESAREANA", "% CESAREANA", "CLASSIFICAÇÃO")] + ["TOTAL CLASSIFICAÇÃO", "CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)"]),
    ("SINASC 2024 — asfixia e enfermagem", ["% ASFIXIA ≥2500G SEM ANOMALIAS CONGÊNITAS", "CLASSIFICAÇÃO ASFIXIA", "% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM", "CLASSIFICAÇÃO PARTO ENF."]),
    ("CNES (competência 03/2026)", ["UNIDADE NEONATAL COMPLETA", "GESTÃO", "NATUREZA JURÍDICA", "HGPAR"]),
    ("SIH-SP — LARC (atos 0301040141 DIU e 0301040176 implante, competência 2025)", ["DIU", "IMPLANTE ", "TOTAL.1", "CLASSIFICAÇÃO CONTRACEPÇÃO"]),
    ("Violência sexual (não reproduzida: nenhum ato do SIH-SP corresponde; valores copiados da planilha)", ["Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL", "CLASSIFICAÇÃO VIOLÊNCIA SEXUAL"]),
    ("Campo oficial (≥5 de 9)", ["CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS"]),
]


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


linhas, difs = [], []
for grupo, cols in GRUPOS:
    for col in cols:
        ok = 0; ex = []
        for _, r in df.iterrows():
            a, b = calc.loc[r["_cnes"], col], r[col]
            if igual(a, b):
                ok += 1
            else:
                difs.append({"grupo": grupo, "coluna": col, "cnes": r["_cnes"], "estabelecimento": r["CNES - ESTABELECIMENTO"], "uf": r["UF"], "planilha": b, "recalculado": a})
                if len(ex) < 3:
                    ex.append(f"{r['_cnes']}: {norm(b)} × {norm(a)}")
        linhas.append((grupo, col, ok, len(df) - ok, "; ".join(ex)))
pd.DataFrame(difs).to_csv(os.path.join(SAIDA, "reproducao_2024_diferencas.csv"), index=False, encoding="utf-8-sig")

tot_ok = sum(l[2] for l in linhas); tot_n = sum(l[2] + l[3] for l in linhas)
md = [f"# Reprodução da planilha 2024 a partir dos microdados\n",
      f"Planilha de referência: `{os.path.basename(ARQ)}` — {len(df)} estabelecimentos. "
      f"Células comparadas: {tot_n:,}; iguais: {tot_ok:,} ({100*tot_ok/tot_n:.2f}%).\n",
      "Regras aplicadas (as que reproduzem a planilha; ver `scripts/extracao/regras.py`):\n",
      "- Partos (6 colunas): PROC_REA da AIH reduzida (RD) por **ano de competência 2025** (ANO_CMPT) — a data de internação/saída 2024 não reproduz a planilha.",
      "- AMIU: `0409060070 ÷ (0409060070 + 0411020013)`, AIH com **data de saída em 2024**.",
      "- Robson: NV e cesáreas por `TPROBSON` 1–4 (cesárea = `PARTO = 2`); grupo adequado quando NV > 0 e **1% ≤ taxa ≤ 30% (G1), 67% (G2), 12% (G3), 47% (G4)** — intervalos empíricos da planilha.",
      "- Asfixia: `APGAR5 < 7`, `PESO ≥ 2500`, `IDANOMAL = 2` ÷ **todos os nascidos vivos** da unidade.",
      "- Enfermagem: `TPNASCASSI = 2` ÷ todos os `PARTO = 1` (inclusive profissional ignorado).",
      "- Unidade neonatal: leitos existentes (CNES-LT, competência 03/2026) de UTIN (81/82), UCINCo (92) e UCINCa (93).",
      "- Gestão: `TPGESTAO` E/M/D; natureza: `NAT_JUR` 1→PÚBLICO, 3→SEM FINS LUCRATIVOS, 2 (inclusive 2011)→PRIVADO; HGPAR: habilitação 1420 vigente.\n",
      "| Grupo | Coluna | Iguais | Diferentes | Exemplos (planilha × recalculado) |", "|---|---|---:|---:|---|"]
for g, col, ok, dif, ex in linhas:
    md.append(f"| {g} | {col} | {ok} | {dif} | {ex} |")
md.append("\nTabela completa das diferenças: `extracao/saida/reproducao_2024_diferencas.csv`; recálculo por CNES: `extracao/saida/reproducao_2024_recalculo.csv`; planilha recalculada no formato original: `planilhas/PLANILHA_2024_recalculada.xlsx`.\n")
md += ["""## Achados da reprodução (para decisão da coordenação)

1. **Ano das AIH de parto.** As seis colunas de parto da planilha "2024" são as AIH **processadas na competência 2025** (ANO_CMPT = 2025): 528/543 exatas. Nenhuma atribuição de 2024 (competência, data de internação ou data de saída) reproduz a planilha. As 15 diferenças restantes são todas de unidades em que o recálculo tem **mais** AIH (AC, PI, PA, RJ, BA, SE, MA, AL, RO; de +73 a +536) — reapresentações incorporadas ao SIH depois da extração de 01/07/2026 — ou diferenças de 1 a 3 AIH. Consequência: para 2025 é preciso decidir qual ano das AIH usar (competência 2026 só existe até 08/2026; a data de saída 2025 é a opção consistente com a regra do AMIU).
2. **AMIU** usa outro recorte de ano: AIH com **data de saída em 2024** (541/543). A planilha mistura, portanto, dois recortes de ano do SIH.
3. **Asfixia**: o denominador é o **total de nascidos vivos** da unidade, não os nascidos ≥2.500 g sem anomalia como diz o nome da coluna (543/543 só com esse denominador). O numerador exige anomalia congênita = "Não" (IDANOMAL = 2; ignorados ficam fora).
4. **Classificação por grupo de Robson** não usa as metas 10/35/3/15 da nota metodológica: o grupo é adequado quando a taxa de cesariana está num **intervalo** — G1 de 1% a 30%, G2 até 67%, G3 de 1% a 12%, G4 até 47% (limites empíricos; 0% nunca é adequado; não há valores observados entre 0,8% e 1,1% nem exatamente nos limites superiores de G2/G4, que podem estar entre 67,0–67,4 e 46,8–47,1). As demais regras de classificação (≥2 grupos, asfixia ≤0,6, enfermagem ≥50, AMIU ≥50, LARC ≥3, violência ≥2, ≥5 de 9) reproduzem 543/543.
5. **Parto por enfermeira**: denominador = todos os partos vaginais, **inclusive** os com profissional ignorado (542/542).
6. **Unidade neonatal completa**: leitos existentes do CNES-LT na competência **03/2026** (UTIN 81/82 + UCINCo 92 + UCINCa 93) — 541/543; divergem o Hospital do Rocio (0013846, tem 81/82 e 92 mas não 93 no LT; planilha "SIM") e o Hospital de Caruaru (2351994, desativado, sem leitos no LT; planilha "NÃO SE APLICA").
7. **HGPAR**: a habilitação CNES 1420 só existe desde 08/2025; a planilha marca 160 unidades, das quais 158 têm a 1420, e deixa de marcar 46 que também a têm — a lista da planilha veio de outra fonte/momento. Duas unidades marcadas não têm a habilitação (HGCC 2499363 e 2798662).
8. **Gestão e natureza**: TPGESTAO (E/M/D) e NAT_JUR (1 → público; 3 → sem fins lucrativos; 2, inclusive 2011 EBSERH → privado) na competência 03/2026: 541 e 543 iguais.
9. **CNES trocado**: em duas linhas a coluna CNES traz o código antigo (2679663, 3511251) e o rótulo o novo (9131922, 5878640); o SIH está no código novo e o SINASC continua no antigo (por isso Robson/asfixia dessas linhas são 0 na planilha). O recálculo 2025 funde os dois códigos no SINASC.
10. **Universo**: "mais de 1.000 partos" pelas AIH de competência 2025 dá 553 unidades: 541 das 543 (as 2 restantes são os códigos antigos acima) e 12 unidades com 1.003–1.232 partos que não estão na planilha. O critério exato de inclusão da planilha não foi reproduzido.
11. **DIU e implante** são atos profissionais da AIH (arquivo SP, `SP_ATOPROF`): **0301040141** (inserção de DIU) e **0301040176** (implante subdérmico de etonogestrel), contados por linha na competência 2025 — o mesmo recorte dos partos. Identificados por casamento do vetor por CNES (383/543 e 514/543 exatos; as diferenças seguem o padrão das reapresentações). **Violência sexual não corresponde a nenhum ato do SIH-SP** (melhor casamento: 22 de 271 unidades) — a fonte deve ser o SIA/BPA (produção ambulatorial), que não está na esteira local; em 2025 a coluna fica em branco até a coordenação informar a fonte e os códigos.

## Perguntas para a coordenação antes de fechar 2025

- Confirmar o recorte de ano do SIH para 2025 (competência × data de saída × data de internação) e, se for o caso, reprocessar 2024 com o mesmo recorte.
- Confirmar os limites por grupo de Robson usados (intervalos acima) e atualizar a nota metodológica.
- Confirmar fonte e códigos de DIU, implante e atendimento a vítima de violência sexual (SIH-SP? SIA/BPA?).
- Confirmar a regra de HGPAR (habilitação 1420 vigente ou lista própria) e a competência do CNES para leitos/gestão/natureza.
- SMCON 2025: lista CNES × módulo e data de corte.
"""]
os.makedirs(os.path.join(RAIZ, "relatorios"), exist_ok=True)
open(os.path.join(RAIZ, "relatorios", "reproducao_2024.md"), "w", encoding="utf-8").write("\n".join(md))
print(f"células {tot_n:,} | iguais {tot_ok:,} ({100*tot_ok/tot_n:.2f}%) | diferenças {len(difs)}")
for g, col, ok, dif, ex in linhas:
    if dif:
        print(f"  {col[:45]:45s} ok={ok:3d} dif={dif:3d}  {ex[:120]}")
