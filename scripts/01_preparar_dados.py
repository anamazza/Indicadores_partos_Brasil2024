# -*- coding: utf-8 -*-
"""
01_preparar_dados.py
Converte a planilha de indicadores em dados.json para o painel.
Entrada: ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES.xlsx
Saída:   dados.json, flags_nomes.json
Uso:     python 01_preparar_dados.py <planilha.xlsx>
"""
import pandas as pd, json, sys

ARQ = sys.argv[1] if len(sys.argv)>1 else 'ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES_01072026.xlsx'
df = pd.read_excel(ARQ)

def num(c): return pd.to_numeric(df[c], errors='coerce').fillna(0)

ces  = df['OPERAÇÃO CESARIANA'] + df['OPERAÇÃO CESARIANA C/ LAQUEADURA TUBARIA'] + df['OPERAÇÃO CESARIANA EM GAR']
norm = df['PARTO NORMAL'] + df['PARTO NORMAL EM CPN'] + df['PARTO NORMAL EM GESTACAO DE ALTO RISCO']

# 9 flags da base (ordem fixa: define o campo flags); na classificação do
# painel o SMCON conta uma única vez, totalizando 8 indicadores classificatórios
flags_def = [
    ('Asfixia Neonatal',    df['CLASSIFICAÇÃO ASFIXIA']=='ADEQUADO'),
    ('Parto vaginal assistido por enfermeira', df['CLASSIFICAÇÃO PARTO ENF.']=='ADEQUADO'),
    ('Uso de AMIU',         df['CLASSIFICAÇÃO AMIU']=='ADEQUADO'),
    ('Robson \u22652 grupos', df['CLASSIFICAÇÃO ROBSON  (\u22652 GRUPOS)']=='ADEQUADO'),
    ('Oferta de LARC', df['CLASSIFICAÇÃO CONTRACEPÇÃO']=='SIM'),
    ('Atendimento de viol\u00eancia sexual', df['CLASSIFICAÇÃO VIOLÊNCIA SEXUAL']=='SIM'),
    ('SMCON Neonatal', df['SMCON NEO'].astype(str).str.strip()=='ok'),
    ('SMCON Obst\u00e9trico', df['SMCON OBST'].astype(str).str.strip()=='ok'),
    ('Unidade Neonatal completa', df['UNIDADE NEONATAL COMPLETA'].isin(['SIM', 'NÃO SE APLICA'])),
]
mat = pd.DataFrame({n: s.astype(int) for n, s in flags_def})

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
        "hgpar": 1 if r['HGPAR']=='SIM' else 0, "neo": r['UNIDADE NEONATAL COMPLETA'],
        "tot": int(r['TOTAL']), "ces": int(ces.iloc[i]), "norm": int(norm.iloc[i]),
        "cpn": int(r['PARTO NORMAL EM CPN']),
        "asf": round(float(num('% ASFIXIA \u22652500G SEM ANOMALIAS CONGÊNITAS').iloc[i]), 2),
        "asfC": r['CLASSIFICAÇÃO ASFIXIA'] if pd.notna(r['CLASSIFICAÇÃO ASFIXIA']) else "",
        "enf": round(float(num('% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM').iloc[i]), 1),
        "enfC": r['CLASSIFICAÇÃO PARTO ENF.'] if pd.notna(r['CLASSIFICAÇÃO PARTO ENF.']) else "",
        "amiu": round(float(num('% AMIU').iloc[i]), 1),
        "robAd": int(num('TOTAL CLASSIFICAÇÃO').iloc[i]),
        "rob2": 1 if r['CLASSIFICAÇÃO ROBSON  (\u22652 GRUPOS)']=='ADEQUADO' else 0,
        "diu": int(num('DIU').iloc[i]), "imp": int(num('IMPLANTE ').iloc[i]),
        "larc": int(num('TOTAL.1').iloc[i]),
        "violN": int(num('Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL').iloc[i]),
        "viol": 1 if r['CLASSIFICAÇÃO VIOLÊNCIA SEXUAL']=='SIM' else 0,
        "smN": 1 if str(r['SMCON NEO']).strip()=='ok' else 0,
        "smO": 1 if str(r['SMCON OBST']).strip()=='ok' else 0,
        "contrOk": 1 if r['CLASSIFICAÇÃO CONTRACEPÇÃO']=='SIM' else 0,
        # selo = classificação do painel (Avançando): >=5 dos 8 indicadores
        # (SMCON conta uma vez); seloOf preserva o campo oficial da planilha
        "selo": 1 if n8 >= 5 else 0,
        "seloOf": 1 if r['CLASSIFICAÇÃO TOTAL \u22655 ROBSON 2 GRUPOS']=='ADEQUADO' else 0,
        "nAdeq": nA,
        "n8": n8,
        "flags": ''.join(str(mat.iloc[i, j]) for j in range(9)),
    }
    for g in [1, 2, 3, 4]:
        rec[f'g{g}']  = round(float(num(f'% CESAREANA G{g}').iloc[i]), 1)
        rec[f'nv{g}'] = int(num(f'TOTAL NV G{g}').iloc[i])
        rec[f'cs{g}'] = int(num(f'Nº CESAREANA G{g}').iloc[i])
        rec[f'g{g}C'] = 1 if num(f'CLASSIFICAÇÃO G{g}').iloc[i]==1 else 0
    recs.append(rec)

json.dump(recs, open('dados/dados.json','w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
json.dump([n for n,_ in flags_def], open('dados/flags_nomes.json','w',encoding='utf-8'), ensure_ascii=False)
print(f"dados.json: {len(recs)} estabelecimentos")
