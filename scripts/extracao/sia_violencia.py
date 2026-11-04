# -*- coding: utf-8 -*-
"""
sia_violencia.py
Baixa do FTP do DATASUS os arquivos PA (produção ambulatorial, SIA/SUS) de cada UF e competência e conta,
por estabelecimento executante (PA_CODUNI), os procedimentos de atendimento a vítima de violência sexual —
0301040052 e 0301040060 (códigos informados pela coordenação em 04/11/2026) — em duas atribuições de ano:
competência de movimento (PA_MVM) e competência de realização (PA_CMP), somando quantidade aprovada e
produzida. Checkpoint por UF, retomável; os .dbc ficam em <pasta_pa> (fora do OneDrive).
Uso: python sia_violencia.py <pasta_pa> <aamm_ini> <aamm_fim> <pasta_saida> [UF ...]
"""
import collections, ftplib, json, os, sys, time

ESTEIRA = r"C:\Users\anapa\OneDrive\Documentos\Projeto Apresentações Internação\Extracao_SIH"
sys.path.insert(0, ESTEIRA)
import datasus_dbc                       # noqa: E402
from dbf_rapido import registros_bytes   # noqa: E402

pasta, aamm_ini, aamm_fim, out = sys.argv[1:5]
UFS = [u.upper() for u in sys.argv[5:]] or ["AC", "RR", "AP", "TO", "SE", "AL", "RN", "PI", "DF", "MS", "MT", "PB", "ES",
                                             "MA", "GO", "RO", "AM", "CE", "SC", "PA", "RS", "BA", "PR", "RJ", "MG", "PE", "SP"]
os.makedirs(pasta, exist_ok=True); os.makedirs(out, exist_ok=True)
PROCS = {"0301040052", "0301040060"}
CAMPOS = ("PA_CODUNI", "PA_PROC_ID", "PA_MVM", "PA_CMP", "PA_QTDAPR", "PA_QTDPRO")
FTP_DIR = "/dissemin/publicos/SIASUS/200801_/Dados"


def competencias(ini, fim):
    a, m = int(ini[:2]), int(ini[2:]); af, mf = int(fim[:2]), int(fim[2:]); s = []
    while (a, m) <= (af, mf):
        s.append(f"{a:02d}{m:02d}"); m += 1
        if m == 13: a, m = a + 1, 1
    return s


def conectar():
    f = ftplib.FTP("ftp.datasus.gov.br", timeout=300); f.login("anonymous", "painel_partos@iff"); f.cwd(FTP_DIR); return f


ftp = conectar()
nomes = []; ftp.retrlines("NLST", nomes.append)
NOMES = set(nomes)


def baixa(arq):
    global ftp
    destino = os.path.join(pasta, arq)
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        return destino
    for tent in (1, 2, 3):
        try:
            tmp = destino + ".part"
            with open(tmp, "wb") as fh:
                ftp.retrbinary("RETR " + arq, fh.write)
            os.replace(tmp, destino); return destino
        except Exception as e:
            print(f"    {arq}: falha {tent} ({e}); reconectando", flush=True); time.sleep(10 * tent)
            try: ftp.quit()
            except Exception: pass
            ftp = conectar()
    raise SystemExit(f"não baixou {arq}")


for uf in UFS:
    destino = os.path.join(out, f"{uf}.json")
    if os.path.exists(destino):
        print(f"{uf}: checkpoint existente, pulando", flush=True); continue
    cont = collections.defaultdict(collections.Counter); t0 = time.time(); n = 0; arquivos = []
    for aamm in competencias(aamm_ini, aamm_fim):
        partes = sorted(a for a in NOMES if a.startswith(f"PA{uf}{aamm}") and a.endswith(".dbc"))
        if not partes:
            print(f"  {uf}{aamm}: não publicado", flush=True); continue
        for arq in partes:
            caminho = baixa(arq); arquivos.append(arq)
            dados = datasus_dbc.decompress_bytes(open(caminho, "rb").read())
            for r in registros_bytes(dados, CAMPOS):
                n += 1
                if r["PA_PROC_ID"] not in PROCS:
                    continue
                c = cont[r["PA_CODUNI"].zfill(7)]; p = r["PA_PROC_ID"]
                apr = int(r["PA_QTDAPR"]) if r["PA_QTDAPR"].isdigit() else 0
                pro = int(r["PA_QTDPRO"]) if r["PA_QTDPRO"].isdigit() else 0
                for k in (f"{p}|m{r['PA_MVM'][:4]}", f"{p}|c{r['PA_CMP'][:4]}"):
                    c[k + "|apr"] += apr; c[k + "|pro"] += pro; c[k + "|lin"] += 1
            print(f"  {arq}: {os.path.getsize(caminho)/1e6:.0f} MB, {n:,} registros acumulados ({time.time()-t0:.0f}s)", flush=True)
    json.dump({"uf": uf, "arquivos": arquivos, "registros": n, "estabelecimentos": {c: dict(v) for c, v in cont.items()}},
              open(destino, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"=== {uf}: {len(cont)} CNES com os procedimentos -> {destino} ({time.time()-t0:.0f}s)", flush=True)
print("FIM_SIA_VIOLENCIA")
