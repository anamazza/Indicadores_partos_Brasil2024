# -*- coding: utf-8 -*-
"""
03_montar_painel.py
Injeta no template os dados de todos os anos (dados/dados_<ano>.json + dados/ano_<ano>.json),
geo_multi.json e flags_nomes.json, e gera o index.html final.
Uso: python 03_montar_painel.py
"""
import glob, json, os, re

html  = open('painel_template.html', encoding='utf-8').read()
anos, cfgs = {}, {}
for arq in sorted(glob.glob('dados/dados_*.json')):
    ano = re.search(r'dados_(\d{4})\.json$', arq).group(1)
    anos[ano] = json.load(open(arq, encoding='utf-8'))
    c = f'dados/ano_{ano}.json'
    cfgs[ano] = json.load(open(c, encoding='utf-8')) if os.path.exists(c) else {"ano": ano}
if not anos:
    raise SystemExit("nenhum dados/dados_<ano>.json — rode 01_preparar_dados.py <planilha> <ano>")
geo   = open('dados/geo_multi.json', encoding='utf-8').read()
flags = open('dados/flags_nomes.json', encoding='utf-8').read()

html = (html.replace('/*__DADOS_ANOS__*/{}', json.dumps(anos, ensure_ascii=False, separators=(',', ':')))
            .replace('/*__ANO_CFG__*/{}', json.dumps(cfgs, ensure_ascii=False, separators=(',', ':')))
            .replace('/*__GEO__*/{}',  geo)
            .replace('/*__FLAGS__*/[]', flags))

open('index.html','w',encoding='utf-8').write(html)
print(f"index.html: {os.path.getsize('index.html')/1024:.0f} KB | anos: " +
      ", ".join(f"{a} ({len(d)} estab.{' · preliminar' if cfgs[a].get('preliminar') else ''})" for a, d in anos.items()))
