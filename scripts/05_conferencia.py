# -*- coding: utf-8 -*-
"""
05_conferencia.py — conferência do index.html montado com os dois anos (mesma lógica do workflow montar_painel.yml).
Uso: python 05_conferencia.py [pasta_sia]   (padrão: extracao/saida/sia_pa_2025). Sai com código 1 se houver erro.
"""
import glob, json, os, re, sys

pasta_sia = sys.argv[1] if len(sys.argv) > 1 else "extracao/saida/sia_pa_2025"
h = open("index.html", encoding="utf-8").read()
anos = json.loads(re.search(r"const DADOS_ANOS = (\{.*?\});\nconst ANO_CFG", h, re.S).group(1))
cfg = json.loads(re.search(r"const ANO_CFG = (\{.*?\});\n", h).group(1))
d25, d24 = anos["2025"], anos["2024"]
arqs = glob.glob(os.path.join(pasta_sia, "*.json"))
ufs = {json.load(open(f, encoding="utf-8"))["uf"] for f in arqs}          # SP vem em 4 partes
viol = sum(1 for d in d25 if d["viol"]); selo = sum(1 for d in d25 if d["selo"])
erros = []
if len(ufs) != 27: erros.append(f"SIA: {len(ufs)} UFs tabuladas (esperado 27): faltam {sorted(set('AC AL AM AP BA CE DF ES GO MA MG MS MT PA PB PE PI PR RJ RN RO RR RS SC SE SP TO'.split()) - ufs)}")
if len(d24) != 543: erros.append(f"2024 com {len(d24)} unidades")
if not (540 <= len(d25) <= 570): erros.append(f"2025 com {len(d25)} unidades")
if cfg["2025"].get("semEstagios"): erros.append("2025 ainda sem estágios")
if cfg["2025"].get("indisponiveis"): erros.append(f"indisponíveis em 2025: {cfg['2025']['indisponiveis']}")
if viol < 100: erros.append(f"só {viol} unidades com violência sexual adequada em 2025 (2024: 225)")  # 2024 usou outra fonte (ver METODOLOGIA 4.7); SIA conferido no TabNet dá ~139
resumo = (f"2025: {len(d25)} unidades, {sum(d['tot'] for d in d25):,} partos; violência sexual adequada em {viol}; "
          f"Avançando {selo}; SIA tabulado em {len(ufs)} UFs ({sum(d['violN'] for d in d25):,} atendimentos).")
print(resumo); print("ERROS:", erros) if erros else print("Conferência OK")
sys.exit(1 if erros else 0)
