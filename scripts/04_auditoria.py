# -*- coding: utf-8 -*-
"""
04_auditoria.py
Recalcula da planilha original todos os números exibidos no painel e compara
com dados.json. Deve terminar com 0 falhas antes de qualquer publicação.
Uso: python 04_auditoria.py <planilha.xlsx>
"""
import pandas as pd, json, statistics as st, sys

ARQ = sys.argv[1] if len(sys.argv)>1 else 'ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES_01072026.xlsx'
df = pd.read_excel(ARQ)
D  = json.load(open('dados/dados.json', encoding='utf-8'))

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
chk("Selo", int((df['CLASSIFICAÇÃO TOTAL \u22655 ROBSON 2 GRUPOS']=='ADEQUADO').sum()),
    sum(d['selo'] for d in D))
chk("Enfermagem adequada", int((df['CLASSIFICAÇÃO PARTO ENF.']=='ADEQUADO').sum()),
    sum(1 for d in D if d['enfC']=='ADEQUADO'))
chk("Asfixia inadequada", int((df['CLASSIFICAÇÃO ASFIXIA']=='INADEQUADO').sum()),
    sum(1 for d in D if d['asfC']=='INADEQUADO'))
chk("LARC", int(pd.to_numeric(df['TOTAL.1'],errors='coerce').fillna(0).sum()), sum(d['larc'] for d in D))
chk("DIU", int(df['DIU'].sum()), sum(d['diu'] for d in D))
chk("Implantes", int(pd.to_numeric(df['IMPLANTE '],errors='coerce').fillna(0).sum()), sum(d['imp'] for d in D))

# Cesariana por região
for reg in ['Norte','Nordeste','Centro-Oeste','Sudeste','Sul']:
    m = df['REGIÃO DO PAÍS']==reg
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

# Estágios do selo
adeq = ((df['CLASSIFICAÇÃO ASFIXIA']=='ADEQUADO').astype(int)
    + (df['CLASSIFICAÇÃO PARTO ENF.']=='ADEQUADO').astype(int)
    + (df['CLASSIFICAÇÃO AMIU']=='ADEQUADO').astype(int)
    + (df['CLASSIFICAÇÃO ROBSON  (\u22652 GRUPOS)']=='ADEQUADO').astype(int)
    + (df['CLASSIFICAÇÃO CONTRACEPÇÃO']=='SIM').astype(int)
    + (df['CLASSIFICAÇÃO VIOLÊNCIA SEXUAL']=='SIM').astype(int)
    + (df['SMCON NEO'].astype(str).str.strip()=='ok').astype(int)
    + (df['SMCON OBST'].astype(str).str.strip()=='ok').astype(int)
    + (df['UNIDADE NEONATAL COMPLETA'].isin(['SIM', 'NÃO SE APLICA'])).astype(int))
selo = (df['CLASSIFICAÇÃO TOTAL \u22655 ROBSON 2 GRUPOS']=='ADEQUADO')
chk("Soma nAdeq", int(adeq.sum()), sum(d['nAdeq'] for d in D))
chk("Estágio Com selo", int(selo.sum()), sum(1 for d in D if d['selo']))
chk("Estágio Quase lá", int(((~selo)&(adeq>=4)).sum()),
    sum(1 for d in D if not d['selo'] and d['nAdeq']>=4))
chk("Estágio No caminho", int(((~selo)&adeq.isin([2,3])).sum()),
    sum(1 for d in D if not d['selo'] and d['nAdeq'] in (2,3)))
chk("Estágio Início", int(((~selo)&(adeq<=1)).sum()),
    sum(1 for d in D if not d['selo'] and d['nAdeq']<=1))

# Territorial e estrutura
chk("Macros", df['CÓD MRS'].nunique(), len({d['mrs'] for d in D}))
chk("Regiões de saúde", df['CÓD RS'].nunique(), len({d['rs'] for d in D}))
chk("Violência atendimentos",
    int(pd.to_numeric(df['Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL'],errors='coerce').fillna(0).sum()),
    sum(d['violN'] for d in D))
chk("CPN partos", int(df['PARTO NORMAL EM CPN'].sum()), sum(d['cpn'] for d in D))
chk("HGPAR", int((df['HGPAR']=='SIM').sum()), sum(d['hgpar'] for d in D))
chk("Neonatal completa", int((df['UNIDADE NEONATAL COMPLETA']=='SIM').sum()),
    sum(1 for d in D if d['neo']=='SIM'))
chk("SMCON neo", int((df['SMCON NEO'].astype(str).str.strip()=='ok').sum()), sum(d['smN'] for d in D))
chk("SMCON obst", int((df['SMCON OBST'].astype(str).str.strip()=='ok').sum()), sum(d['smO'] for d in D))

print(f"AUDITORIA: {ok} verificações OK | {len(falhas)} falhas")
for f in falhas: print("  FALHA:", f)
sys.exit(1 if falhas else 0)
