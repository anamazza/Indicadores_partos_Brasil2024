# -*- coding: utf-8 -*-
"""
sinasc_indicadores.py
Agrega, por estabelecimento (CODESTAB), as variáveis do SINASC usadas no painel:
nascidos vivos e cesáreas por grupo de Robson, asfixia (Apgar 5º min < 7 em NV ≥ 2.500 g
sem anomalia congênita) e parto vaginal assistido por enfermeira/obstetriz.
Guarda numerador e denominador de cada variante de regra para a calibração contra a planilha.
Entrada: SINASC_<ano>_csv.zip do OpenDataSUS (CSV ';' em latin-1).
Uso:     python sinasc_indicadores.py <ano|AAAAS1|AAAAS2> <SINASC_<ano>_csv.zip> <saida.json>
"""
import collections, csv, io, json, re, sys, time, zipfile

periodo, zip_path, out = sys.argv[1:4]
m = re.fullmatch(r"(\d{4})(S[12])?", periodo)
if not m:
    raise SystemExit(f"período inválido: {periodo}")
MESES = {None: None, "S1": set(range(1, 7)), "S2": set(range(7, 13))}[m.group(2)]
CAMPOS = ["CODESTAB", "PARTO", "TPROBSON", "APGAR5", "PESO", "IDANOMAL", "TPNASCASSI", "DTNASC", "CODMUNNASC"]

agg = collections.defaultdict(collections.Counter)
zf = zipfile.ZipFile(zip_path)
membro = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
t0 = time.time(); total = fora = 0
with zf.open(membro) as raw:
    txt = io.TextIOWrapper(raw, encoding="latin-1", newline="")
    rd = csv.reader(txt, delimiter=";")
    header = [c.strip('"').upper() for c in next(rd)]
    idx = {c: i for i, c in enumerate(header)}
    pos = {c: idx[c] for c in CAMPOS}

    def g(row, c):
        return row[pos[c]].strip().strip('"')

    for row in rd:
        if MESES is not None:                       # recorte por mês de nascimento (ddmmaaaa)
            dt = g(row, "DTNASC")
            if len(dt) != 8 or not dt.isdigit() or int(dt[2:4]) not in MESES:
                fora += 1; continue
        total += 1
        est = g(row, "CODESTAB") or "SEM_CODESTAB"
        c = agg[est.zfill(7)]
        c["nv"] += 1
        parto = g(row, "PARTO")
        ces, vag = parto == "2", parto == "1"
        if ces: c["ces"] += 1
        if vag: c["vag"] += 1
        if not (ces or vag): c["parto_ign"] += 1
        rb = g(row, "TPROBSON")
        grp = int(rb) if rb.isdigit() and 1 <= int(rb) <= 10 else 0     # 0 = não classificado
        c[f"nv_g{grp}"] += 1
        if ces: c[f"ces_g{grp}"] += 1
        # --- asfixia: NV >= 2500 g; variante a = IDANOMAL != 1 (inclui ignorado), b = IDANOMAL == 2
        peso, apg, anom = g(row, "PESO"), g(row, "APGAR5"), g(row, "IDANOMAL")
        if peso.isdigit() and int(peso) >= 2500:
            apg_inf = apg.isdigit() and int(apg) <= 10
            baixo = apg_inf and int(apg) < 7
            if anom != "1":
                c["asf_den_a_todos"] += 1
                if apg_inf: c["asf_den_a"] += 1
                if baixo: c["asf_num_a"] += 1
            if anom == "2":
                c["asf_den_b_todos"] += 1
                if apg_inf: c["asf_den_b"] += 1
                if baixo: c["asf_num_b"] += 1
        # --- parto vaginal por enfermeira/obstetriz (TPNASCASSI = 2)
        if vag:
            tp = g(row, "TPNASCASSI")
            c["enf_den_todos"] += 1
            if tp in ("1", "2", "3", "4"): c["enf_den_inf"] += 1
            if tp == "2": c["enf_num"] += 1
        if total % 500_000 == 0:
            print(f"  {total:,} registros ({time.time()-t0:.0f}s)", flush=True)

json.dump({"periodo": periodo, "arquivo": membro, "registros": total, "fora_periodo": fora,
           "estabelecimentos": {k: dict(v) for k, v in agg.items()}},
          open(out, "w", encoding="utf-8"), ensure_ascii=False)
print(f"{periodo}: {total:,} NV, {len(agg):,} estabelecimentos -> {out} ({time.time()-t0:.0f}s)")
