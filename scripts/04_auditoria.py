# -*- coding: utf-8 -*-
"""
04_auditoria.py
Recalcula da planilha original de um ano todos os números exibidos no painel e compara
com dados/dados_<ano>.json. Deve terminar com 0 falhas antes de qualquer publicação.
Indicadores marcados como indisponíveis em dados/ano_<ano>.json (colunas vazias na planilha)
não entram nas verificações correspondentes.
Uso: python 04_auditoria.py <planilha.xlsx> <ano>
"""
import json, statistics as st, sys
import pandas as pd

ARQ, ANO = sys.argv[1], sys.argv[2]
df = pd.read_excel(ARQ)
D  = json.load(open(f'dados/dados_{ANO}.json', encoding='utf-8'))
CFG = json.load(open(f'dados/ano_{ANO}.json', encoding='utf-8'))
IND = set(CFG.get('indisponiveis', []))

ok, falhas = 0, []
def chk(nome, esperado, obtido, tol=0.05):
    global ok
    igual = (abs(esperado-obtido) <= tol) if isinstance(esperado,(int,float)) else (esperado==obtido)
    if igual: ok += 1
    else: falhas.append(f"{nome}: planilha={esperado} x painel={obtido}")

ces = (df['OPERAÇÃO CESARIANA'] + df['OPERAÇÃO CESARIANA C/ LAQUEADURA TUBARIA']
       + df['OPERAÇÃO CESARIANA EM GAR']).sum()

# KPIs
chk("Estabelecimentos", len(df), len(D))
chk("Partos totais", int(df['TOTAL'].sum()), sum(d['tot'] for d in D))
chk("Cesarianas", int(ces), sum(d['ces'] for d in D))
chk("Taxa cesariana %", ces/df['TOTAL'].sum()*100,
    sum(d['ces'] for d in D)/sum(d['tot'] for d in D)*100, 0.01)
chk("Enfermagem adequada", int((df['CLASSIFICAÇÃO PARTO ENF.']=='ADEQUADO').sum()),
    sum(1 for d in D if d['enfC']=='ADEQUADO'))
chk("Asfixia inadequada", int((df['CLASSIFICAÇÃO ASFIXIA']=='INADEQUADO').sum()),
    sum(1 for d in D if d['asfC']=='INADEQUADO'))
if 'larc' not in IND:
    chk("LARC", int(pd.to_numeric(df['TOTAL.1'],errors='coerce').fillna(0).sum()), sum(d['larc'] for d in D))
    chk("DIU", int(pd.to_numeric(df['DIU'],errors='coerce').fillna(0).sum()), sum(d['diu'] for d in D))
    chk("Implantes", int(pd.to_numeric(df['IMPLANTE '],errors='coerce').fillna(0).sum()), sum(d['imp'] for d in D))

# Cesariana por região
for reg in ['Norte','Nordeste','Centro-Oeste','Sudeste','Sul']:
    m = df['REGIÃO DO PAÍS']==reg
    if not m.any(): continue
    tx = (df.loc[m,'OPERAÇÃO CESARIANA']+df.loc[m,'OPERAÇÃO CESARIANA C/ LAQUEADURA TUBARIA']
          +df.loc[m,'OPERAÇÃO CESARIANA EM GAR']).sum()/df.loc[m,'TOTAL'].sum()*100
    s=[d for d in D if d['reg']==reg]
    chk(f"Tx cesariana {reg}", tx, sum(d['ces'] for d in s)/sum(d['tot'] for d in s)*100)

# Robson: mediana (gráfico) e ponderada (mapa)
for g in [1,2,3,4]:
    chk(f"Mediana G{g}", pd.to_numeric(df[f'% CESAREANA G{g}'],errors='coerce').fillna(0).median(),
        st.median([d[f'g{g}'] for d in D]))
    chk(f"Ponderada G{g}", df[f'Nº CESAREANA G{g}'].sum()/df[f'TOTAL NV G{g}'].sum()*100,
        sum(d[f'cs{g}'] for d in D)/sum(d[f'nv{g}'] for d in D)*100, 0.01)
chk("Robson ≥2 grupos", int((df['CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)']=='ADEQUADO').sum()), sum(d['rob2'] for d in D))
chk("AMIU adequado", int((df['CLASSIFICAÇÃO AMIU']=='ADEQUADO').sum()), sum(1 for d in D if d['flags'][2]=='1'))

# Estágios de desempenho: 8 indicadores (SMCON Neonatal e/ou Obstétrico conta uma vez)
if not CFG.get('semEstagios'):
    chk("Campo oficial ≥5 de 9 (planilha)", int((df['CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS']=='ADEQUADO').sum()),
        sum(d['oficial'] for d in D))
    adeq = ((df['CLASSIFICAÇÃO ASFIXIA']=='ADEQUADO').astype(int)
        + (df['CLASSIFICAÇÃO PARTO ENF.']=='ADEQUADO').astype(int)
        + (df['CLASSIFICAÇÃO AMIU']=='ADEQUADO').astype(int)
        + (df['CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)']=='ADEQUADO').astype(int)
        + (df['CLASSIFICAÇÃO CONTRACEPÇÃO']=='SIM').astype(int)
        + (df['CLASSIFICAÇÃO VIOLÊNCIA SEXUAL']=='SIM').astype(int)
        + (df['SMCON NEO'].astype(str).str.strip()=='ok').astype(int)
        + (df['SMCON OBST'].astype(str).str.strip()=='ok').astype(int)
        + (df['UNIDADE NEONATAL COMPLETA'].isin(['SIM', 'NÃO SE APLICA'])).astype(int))
    both  = ((df['SMCON NEO'].astype(str).str.strip()=='ok')
           & (df['SMCON OBST'].astype(str).str.strip()=='ok')).astype(int)
    adeq8 = adeq - both
    avanc = adeq8 >= 5
    chk("Soma nAdeq (9 flags)", int(adeq.sum()), sum(d['nAdeq'] for d in D))
    chk("Soma n8 (8 indicadores)", int(adeq8.sum()), sum(d['n8'] for d in D))
    chk("Estágio Avançando (≥5 de 8)", int(avanc.sum()), sum(1 for d in D if d['avanc']))
    chk("Estágio Quase lá", int(((~avanc)&(adeq8>=4)).sum()),
        sum(1 for d in D if not d['avanc'] and d['n8']>=4))
    chk("Estágio No caminho", int(((~avanc)&adeq8.isin([2,3])).sum()),
        sum(1 for d in D if not d['avanc'] and d['n8'] in (2,3)))
    chk("Estágio Início", int(((~avanc)&(adeq8<=1)).sum()),
        sum(1 for d in D if not d['avanc'] and d['n8']<=1))
else:
    chk("Sem estágios: avanc nulo", len(df), sum(1 for d in D if d['avanc'] is None and d['n8'] is None))

# Territorial e estrutura
chk("Macros", df['CÓD MRS'].nunique(), len({d['mrs'] for d in D}))
chk("Regiões de saúde", df['CÓD RS'].nunique(), len({d['rs'] for d in D}))
if 'viol' not in IND:
    chk("Violência atendimentos",
        int(pd.to_numeric(df['Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL'],errors='coerce').fillna(0).sum()),
        sum(d['violN'] for d in D))
    chk("Violência adequada", int((df['CLASSIFICAÇÃO VIOLÊNCIA SEXUAL']=='SIM').sum()), sum(d['viol'] for d in D))
chk("CPN partos", int(df['PARTO NORMAL EM CPN'].sum()), sum(d['cpn'] for d in D))
chk("HGPAR", int((df['HGPAR']=='SIM').sum()), sum(d['hgpar'] for d in D))
chk("Neonatal completa", int((df['UNIDADE NEONATAL COMPLETA']=='SIM').sum()),
    sum(1 for d in D if d['neo']=='SIM'))
chk("Neonatal adequada (SIM ou N/A)", int(df['UNIDADE NEONATAL COMPLETA'].isin(['SIM','NÃO SE APLICA']).sum()),
    sum(1 for d in D if d['flags'][8]=='1'))
if 'sm' not in IND:
    chk("SMCON neo", int((df['SMCON NEO'].astype(str).str.strip()=='ok').sum()), sum(d['smN'] for d in D))
    chk("SMCON obst", int((df['SMCON OBST'].astype(str).str.strip()=='ok').sum()), sum(d['smO'] for d in D))

print(f"AUDITORIA {ANO}: {ok} verificações OK | {len(falhas)} falhas" + (f" | indisponíveis: {', '.join(sorted(IND))}" if IND else ""))
for f in falhas: print("  FALHA:", f)
sys.exit(1 if falhas else 0)
