# -*- coding: utf-8 -*-
"""
03_montar_painel.py
Injeta dados.json, geo_multi.json e flags_nomes.json no template e gera o index.html final.
Uso: python 03_montar_painel.py
"""
html  = open('painel_template.html', encoding='utf-8').read()
dados = open('dados.json', encoding='utf-8').read()
geo   = open('geo_multi.json', encoding='utf-8').read()
flags = open('flags_nomes.json', encoding='utf-8').read()

html = (html.replace('/*__DADOS__*/[]', dados)
            .replace('/*__GEO__*/{}',  geo)
            .replace('/*__FLAGS__*/[]', flags))

open('index.html','w',encoding='utf-8').write(html)
import os
print(f"index.html: {os.path.getsize('index.html')/1024:.0f} KB")
