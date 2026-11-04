# -*- coding: utf-8 -*-
"""
01_preparar_dados.py
Converte a planilha de indicadores de um ano em dados/dados_<ano>.json (+ dados/ano_<ano>.json com a
configuração do ano: universo, extração, caráter preliminar e indicadores indisponíveis).
Entrada: planilha no formato ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_<ano>__INDICADORES.xlsx
Uso:     python 01_preparar_dados.py <planilha.xlsx> <ano> [--preliminar] [--extracao dd/mm/aaaa] [--nota "texto"]
Indicadores cujas colunas estão inteiramente vazias na planilha (ex.: SMCON e LARC/violência de 2025 enquanto
as fontes não chegam) são marcados como indisponíveis: a flag correspondente fica '-', e a contagem de
indicadores adequados (n8) e o estágio de desempenho ficam nulos — o painel não os exibe para esse ano.
"""
import argparse, json, os
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("planilha"); ap.add_argument("ano")
ap.add_argument("--preliminar", action="store_true"); ap.add_argument("--extracao", default="")
ap.add_argument("--nota", default="")
a = ap.parse_args()
df = pd.read_excel(a.planilha)
os.makedirs("dados", exist_ok=True)

def num(c): return pd.to_numeric(df[c], errors="coerce").fillna(0)
def vazia(*cols): return all(df[c].isna().all() for c in cols)

ces  = df['OPERAÇÃO CESARIANA'] + df['OPERAÇÃO CESARIANA C/ LAQUEADURA TUBARIA'] + df['OPERAÇÃO CESARIANA EM GAR']
norm = df['PARTO NORMAL'] + df['PARTO NORMAL EM CPN'] + df['PARTO NORMAL EM GESTACAO DE ALTO RISCO']

# indicadores sem fonte neste ano (colunas inteiramente vazias)
indisp = []
if vazia('DIU', 'IMPLANTE '): indisp.append('larc')
if vazia('Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL'): indisp.append('viol')
if vazia('SMCON NEO', 'SMCON OBST'): indisp.append('sm')
sem_estagios = bool(indisp)          # sem todos os 8 indicadores não há contagem de adequados nem estágio

# 9 flags da base (ordem fixa: define o campo flags); na classificação do
# painel o SMCON conta uma única vez, totalizando 8 indicadores classificatórios
flags_def = [
    ('Asfixia Neonatal',    df['CLASSIFICAÇÃO ASFIXIA']=='ADEQUADO'),
    ('Parto vaginal assistido por enfermeira', df['CLASSIFICAÇÃO PARTO ENF.']=='ADEQUADO'),
    ('Uso de AMIU',         df['CLASSIFICAÇÃO AMIU']=='ADEQUADO'),
    ('Robson ≥2 grupos', df['CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)']=='ADEQUADO'),
    ('Oferta de LARC', df['CLASSIFICAÇÃO CONTRACEPÇÃO']=='SIM'),
    ('Atendimento de violência sexual', df['CLASSIFICAÇÃO VIOLÊNCIA SEXUAL']=='SIM'),
    ('SMCON Neonatal', df['SMCON NEO'].astype(str).str.strip()=='ok'),
    ('SMCON Obstétrico', df['SMCON OBST'].astype(str).str.strip()=='ok'),
    ('Unidade Neonatal completa', df['UNIDADE NEONATAL COMPLETA'].isin(['SIM', 'NÃO SE APLICA'])),
]
mat = pd.DataFrame({n: s.astype(int) for n, s in flags_def})
flag_indisp = {4: 'larc' in indisp, 5: 'viol' in indisp, 6: 'sm' in indisp, 7: 'sm' in indisp}

recs = []
for i, r in df.iterrows():
    # contagem de adequados: 9 flags da base e 8 indicadores (SMCON e/ou = 1)
    nA   = int(mat.iloc[i].sum())
    both = 1 if (mat.iloc[i, 6] == 1 and mat.iloc[i, 7] == 1) else 0
    n8   = nA - both
    rec = {
        "reg": r['REGIÃO DO PAÍS'], "uf": r['UF'], "mun": r['MUNICÍPIO'],
        "mrs": int(r['CÓD MRS']), "mrsN": r['MACRORREGIÃO DE SAÚDE'],
        "rs": int(r['CÓD RS']),  "rsN": r['REGIÃO DE SAÚDE'],
        "est": r['CNES - ESTABELECIMENTO'], "gestao": r['GESTÃO'], "nat": r['NATUREZA JURÍDICA'],
        "hgpar": 1 if r['HGPAR']=='SIM' else 0, "neo": r['UNIDADE NEONATAL COMPLETA'] if pd.notna(r['UNIDADE NEONATAL COMPLETA']) else "",
        "tot": int(r['TOTAL']), "ces": int(ces.iloc[i]), "norm": int(norm.iloc[i]),
        "cpn": int(r['PARTO NORMAL EM CPN']),
        "asf": round(float(num('% ASFIXIA ≥2500G SEM ANOMALIAS CONGÊNITAS').iloc[i]), 2),
        "asfC": r['CLASSIFICAÇÃO ASFIXIA'] if pd.notna(r['CLASSIFICAÇÃO ASFIXIA']) else "",
        "enf": round(float(num('% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM').iloc[i]), 1),
        "enfC": r['CLASSIFICAÇÃO PARTO ENF.'] if pd.notna(r['CLASSIFICAÇÃO PARTO ENF.']) else "",
        "amiu": round(float(num('% AMIU').iloc[i]), 1),
        "robAd": int(num('TOTAL CLASSIFICAÇÃO').iloc[i]),
        "rob2": 1 if r['CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)']=='ADEQUADO' else 0,
        "diu": None if 'larc' in indisp else int(num('DIU').iloc[i]),
        "imp": None if 'larc' in indisp else int(num('IMPLANTE ').iloc[i]),
        "larc": None if 'larc' in indisp else int(num('TOTAL.1').iloc[i]),
        "violN": None if 'viol' in indisp else int(num('Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL').iloc[i]),
        "viol": None if 'viol' in indisp else (1 if r['CLASSIFICAÇÃO VIOLÊNCIA SEXUAL']=='SIM' else 0),
        "smN": None if 'sm' in indisp else (1 if str(r['SMCON NEO']).strip()=='ok' else 0),
        "smO": None if 'sm' in indisp else (1 if str(r['SMCON OBST']).strip()=='ok' else 0),
        "contrOk": None if 'larc' in indisp else (1 if r['CLASSIFICAÇÃO CONTRACEPÇÃO']=='SIM' else 0),
        # selo = classificação do painel (Avançando): >=5 dos 8 indicadores
        # (SMCON conta uma vez); seloOf preserva o campo oficial da planilha
        "selo": None if sem_estagios else (1 if n8 >= 5 else 0),
        "seloOf": None if sem_estagios else (1 if r['CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS']=='ADEQUADO' else 0),
        "nAdeq": None if sem_estagios else nA,
        "n8": None if sem_estagios else n8,
        "flags": ''.join('-' if flag_indisp.get(j) else str(mat.iloc[i, j]) for j in range(9)),
    }
    for g in [1, 2, 3, 4]:
        rec[f'g{g}']  = round(float(num(f'% CESAREANA G{g}').iloc[i]), 1)
        rec[f'nv{g}'] = int(num(f'TOTAL NV G{g}').iloc[i])
        rec[f'cs{g}'] = int(num(f'Nº CESAREANA G{g}').iloc[i])
        rec[f'g{g}C'] = 1 if num(f'CLASSIFICAÇÃO G{g}').iloc[i]==1 else 0
    recs.append(rec)

json.dump(recs, open(f'dados/dados_{a.ano}.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
json.dump([n for n,_ in flags_def], open('dados/flags_nomes.json','w',encoding='utf-8'), ensure_ascii=False)
cfg = {"ano": a.ano, "n": len(recs), "partos": int(df['TOTAL'].sum()), "extracao": a.extracao,
       "preliminar": a.preliminar, "indisponiveis": indisp, "semEstagios": sem_estagios, "nota": a.nota,
       "planilha": os.path.basename(a.planilha)}
json.dump(cfg, open(f'dados/ano_{a.ano}.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"dados_{a.ano}.json: {len(recs)} estabelecimentos, {cfg['partos']:,} partos"
      + (f" | indisponíveis: {', '.join(indisp)} (sem estágios)" if indisp else "") + (" | PRELIMINAR" if a.preliminar else ""))
