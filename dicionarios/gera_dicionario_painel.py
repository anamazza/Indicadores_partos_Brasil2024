# -*- coding: utf-8 -*-
"""
gera_dicionario_painel.py
Gera o Dicionário de Dados do painel de partos (Indicadores da Atenção Obstétrica e Neonatal em Estabelecimentos
com mais de 1.000 partos) e da comparação regional, no mesmo formato de blocos do dicionário do SMCON
({"tipo":"p"} e {"tipo":"tabela"}), a partir das regras efetivamente aplicadas pelos scripts
(scripts/extracao/regras.py, montar_planilha.py, regional.py, sim_regional.py, relatorio_regional.py,
scripts/01_preparar_dados.py, .github/workflows/montar_painel.yml) e da METODOLOGIA.md.
Revisado em 09/11/2026 por banca de conferência (regras × código, fontes externas e redação).

    python -X utf8 gera_dicionario_painel.py  -> DICIONARIO_PAINEL_PARTOS_<data>.json e .md (nesta pasta)
    node gera_dicionario_docx.js <node_modules> DICIONARIO_PAINEL_PARTOS_<data>.json DICIONARIO_PAINEL_PARTOS_<data>.docx "cabeçalho"
"""
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
DATA = "2026-11-09"
SAIDA_JSON = os.path.join(AQUI, f"DICIONARIO_PAINEL_PARTOS_{DATA}.json")
SAIDA_MD = os.path.join(AQUI, f"DICIONARIO_PAINEL_PARTOS_{DATA}.md")


def P(texto, estilo=""):
    return {"tipo": "p", "estilo": estilo, "texto": texto}


def tabela(cab, linhas):
    out = [[[c] for c in cab]]
    for l in linhas:
        if l[0] == "SEÇÃO":
            out.append([[l[1]]])
        else:
            out.append([[s for s in str(c).split("\n") if s != ""] or [""] for c in l])
    return {"tipo": "tabela", "linhas": out}


# ----------------------------------------------------------------------------------------------------------------
# TABELA 1: colunas da base por estabelecimento (planilha ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_<ano>)
# (coluna, fonte, regra de cálculo / conteúdo, campo em dados/dados_<ano>.json)
# Em 2024 os valores são os da planilha institucional; a regra descrita é a do recálculo de 2025 e, quando difere,
# a regra que reproduz a planilha de 2024.
# ----------------------------------------------------------------------------------------------------------------
SIH_ANO = ("Ano de referência 2025: AIH com data de internação (DT_INTER) no ano, nas competências de 01/2025 a 08/2026 (regra do dicionário de "
           "indicadores da Coordenação, de 09/09/2026). A planilha institucional de 2024 contou as AIH pela competência de processamento (ANO_CMPT) de 2025.")
BASE = [
    ("SEÇÃO", "IDENTIFICAÇÃO E TERRITÓRIO"),
    ("REGIÃO DO PAÍS", "IBGE (código da UF)", "Norte, Nordeste, Sudeste, Sul e Centro-Oeste.", "reg"),
    ("UF", "CNES", "Nome da unidade da federação do estabelecimento.", "uf"),
    ("CÓD MRS / MACRORREGIÃO DE SAÚDE; CÓD RS / REGIÃO DE SAÚDE", "2024: planilha institucional. 2025: CNES + base territorial do DATASUS",
     "Códigos e nomes da macrorregião e da região de saúde (CIR) do município do estabelecimento. Em 2025: município da ficha do CNES (ou CODUFMUN do arquivo LT); "
     "códigos de região e macrorregião em extracao/territorio/municipio_territorios.csv (CO_REGSAUD, CO_MACSAUD, base territorial do DATASUS de junho/2026); nomes copiados "
     "da planilha de 2024 quando o código coincide e, caso contrário, de tb_regsaud e tb_macsaud da mesma base.", "mrs, mrsN, rs, rsN"),
    ("COD MUN / MUNICÍPIO", "CNES", "Código IBGE (6 dígitos) e nome do município do estabelecimento.", "mun"),
    ("CNES / CNES - ESTABELECIMENTO", "CNES",
     "Código CNES (gravado como número inteiro, sem zeros à esquerda) e 'código - nome fantasia'. Complexo HC FAMEMA (Marília/SP): as AIH estão no CNES 2025507 e as DNV no 2025523 "
     "(Unidade Materno Infantil); a partir de 2025 os dois códigos são somados no 2025507. Na planilha de 2024 não foram somados: a unidade ficou com 0 NV, Robson sem nascidos vivos, "
     "parto por enfermeira 0 % e asfixia 0 % (classificada como adequada). Mudanças de código: 3511251 → 5878640 e 2679663 → 9131922 (as DNV seguem no código antigo; a planilha de 2024 "
     "usa os códigos antigos e a de 2025, os novos).", "est"),
    ("GESTÃO", "CNES (TPGESTAO)", "ESTADUAL (E), MUNICIPAL (M) ou DUPLA (D). Em 2025: cadastro da última competência do arquivo LT em que o CNES aparece; ficha da API do CNES como reserva.", "gestao"),
    ("NATUREZA JURÍDICA", "CNES (NAT_JUR)", "PÚBLICO (natureza jurídica 1xxx, administração pública), SEM FINS LUCRATIVOS (3xxx) e PRIVADO (demais, inclusive 2xxx, entidades empresariais, o que classifica como PRIVADO "
     "empresas públicas e sociedades de economia mista, como os hospitais da EBSERH, natureza 2011). "
     "Mesma competência da GESTÃO.", "nat"),
    ("STATUS", "API do CNES", "ATIVO, ou DESATIVADO quando a ficha traz motivo de desabilitação (uma unidade em cada ano).", "—"),
    ("HGPAR", "CNES, habilitações (serviço de fichas do CNES)",
     "2025: SIM quando a ficha do CNES (consulta de 03/11/2026) tem a habilitação 14.20, Hospital de Referência à Gestação e ao Puerpério de Alto Risco (HGPAR), criada pela Rede Alyne "
     "(Portaria GM/MS 5.350/2024), sem data de fim; "
     "caso contrário, ou com erro na consulta, 0. 2024: valor da planilha institucional (160 SIM), cuja fonte não foi reproduzida (495 de 543 unidades coincidem; a habilitação 1420 "
     "existe desde 08/2025; as habilitações anteriores de gestação de alto risco são 14.13 e 14.14).", "hgpar (1/0)"),
    ("SEÇÃO", "PARTOS (SIH/SUS, arquivos RD, procedimento realizado PROC_REA)"),
    ("OPERAÇÃO CESARIANA", "SIH/SUS, RD", "AIH com PROC_REA 0411010034. " + SIH_ANO, "ces (soma das três colunas de cesariana)"),
    ("OPERAÇÃO CESARIANA C/ LAQUEADURA TUBARIA", "SIH/SUS, RD", "PROC_REA 0411010042.", "ces"),
    ("OPERAÇÃO CESARIANA EM GAR", "SIH/SUS, RD", "PROC_REA 0411010026 (gestação de alto risco).", "ces"),
    ("PARTO NORMAL", "SIH/SUS, RD", "PROC_REA 0310010039.", "norm (soma das três colunas de parto normal)"),
    ("PARTO NORMAL EM CPN", "SIH/SUS, RD", "PROC_REA 0310010055 (centro de parto normal).", "cpn; norm"),
    ("PARTO NORMAL EM GESTACAO DE ALTO RISCO", "SIH/SUS, RD", "PROC_REA 0310010047.", "norm"),
    ("TOTAL", "derivada",
     "Soma das seis colunas de parto. Define o universo do painel: estabelecimentos com mais de 1.000 partos no ano (2025). O critério da planilha de 2024 não foi reproduzido: "
     "pela competência 2025 o universo teria 553 unidades, não 543. A laqueadura tubária na internação do parto vaginal (0409060313) não é contada; o dicionário da Coordenação "
     "a conta como parto vaginal (28.638 AIH com internação em 2025 nas 555 unidades; 30.970 no país).", "tot"),
    ("TOTAL S/ CPN", "derivada", "TOTAL menos PARTO NORMAL EM CPN.", "—"),
    ("SEÇÃO", "UNIDADE NEONATAL (CNES, arquivos LT: leitos existentes, QT_EXIST)"),
    ("UNIDADE NEONATAL COMPLETA", "CNES, LT",
     "SIM: há leitos existentes de UTIN tipo II ou III (códigos 81 ou 82), UCINCo (92) e UCINCa (93) na competência de referência. NÃO: há leitos de um ou dois desses tipos, mas não dos três. "
     "NÃO SE APLICA: não há leitos de nenhum dos três (maternidade sem unidade neonatal). UTIN tipo I (código 80) não é considerada. Em branco quando o CNES não consta no LT "
     "(duas unidades em 2025), o que conta como não adequado. Competência: 09/2026 para 2025; a planilha de 2024 é reproduzida com a competência 03/2026. São adequados SIM e NÃO SE APLICA.", "neo"),
    ("SEÇÃO", "ASFIXIA NEONATAL (SINASC)"),
    ("% ASFIXIA ≥2500G SEM ANOMALIAS CONGÊNITAS", "SINASC (APGAR5, PESO, IDANOMAL)",
     "Numerador: NV com APGAR5 < 7, PESO ≥ 2.500 g e IDANOMAL = 2 (sem anomalia). Denominador (planilha de 2024 e painel): todos os NV do estabelecimento (CODESTAB) no ano. "
     "O dicionário da Coordenação (2025) restringe o denominador aos NV com peso ≥ 2.500 g e sem anomalia; o painel mantém a regra de 2024 para preservar a comparabilidade. "
     "Valor com uma casa decimal.", "asf"),
    ("CLASSIFICAÇÃO ASFIXIA", "derivada", "ADEQUADO se % ≤ 0,6 (média do Brasil em 2024, segundo a METODOLOGIA); caso contrário, INADEQUADO.", "asfC"),
    ("SEÇÃO", "PARTO VAGINAL ASSISTIDO POR ENFERMEIRA (SINASC)"),
    ("% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM", "SINASC (PARTO, TPNASCASSI)",
     "Numerador: NV de parto vaginal (PARTO = 1) com TPNASCASSI = 2 (enfermeira ou obstetriz). Denominador: todos os NV de parto vaginal, inclusive os registros com profissional ignorado "
     "(regra da planilha de 2024; o dicionário da Coordenação exclui os ignorados).", "enf"),
    ("CLASSIFICAÇÃO PARTO ENF.", "derivada", "ADEQUADO se % ≥ 50; caso contrário, INADEQUADO.", "enfC"),
    ("SEÇÃO", "USO DE AMIU (SIH/SUS)"),
    ("% AMIU", "SIH/SUS, RD", "AMIU (0409060070, esvaziamento de útero pós-aborto por aspiração manual intrauterina) ÷ [AMIU + curetagem pós-abortamento/puerperal (0411020013)] × 100; "
     "o denominador inclui, portanto, a curetagem puerperal. Em 2025, AIH por data de internação; na planilha de 2024, por data de saída em 2024.", "amiu"),
    ("CLASSIFICAÇÃO AMIU", "derivada", "ADEQUADO se % ≥ 50; caso contrário, vazio.", "— (posição 3 do campo 'flags')"),
    ("SEÇÃO", "CESARIANA POR GRUPO DE ROBSON, G1 A G4 (SINASC, TPROBSON E PARTO)"),
    ("TOTAL NV G1 … G4", "SINASC (TPROBSON)", "NV do estabelecimento com TPROBSON igual a 1, 2, 3 e 4, respectivamente (grupo de Robson atribuído pelo SINASC).", "nv1 … nv4"),
    ("Nº CESAREANA G1 … G4", "SINASC (PARTO = 2)", "Cesarianas em cada grupo.", "cs1 … cs4"),
    ("% CESAREANA G1 … G4", "derivada", "Nº de cesarianas ÷ NV do grupo × 100, com uma casa decimal.", "g1 … g4"),
    ("CLASSIFICAÇÃO G1 … G4", "derivada",
     "1 quando o grupo tem NV > 0 e o percentual está no intervalo usado na planilha de 2024: G1, 1 % a 30 %; G2, 1 % a 67 %; G3, 1 % a 12 %; G4, 1 % a 47 % (0 % nunca é classificado "
     "como adequado). As metas institucionais publicadas na METODOLOGIA.md (≤ 10 %, ≤ 35 %, ≤ 3 % e ≤ 15 %) diferem desses intervalos, que estão em confirmação com a Coordenação.", "g1C … g4C"),
    ("TOTAL CLASSIFICAÇÃO", "derivada", "Número de grupos (0 a 4) classificados como adequados.", "robAd"),
    ("CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS)", "derivada", "ADEQUADO se TOTAL CLASSIFICAÇÃO ≥ 2; caso contrário, vazio.", "rob2"),
    ("SEÇÃO", "OFERTA DE LARC (SIH/SUS, atos profissionais SP_ATOPROF dos arquivos SP; estabelecimento = SP_CNES)"),
    ("DIU", "SIH/SUS, SP", "Registros de inserção de DIU (0301040141) nas AIH do estabelecimento. Em 2025, AIH com data de saída em 2025; a planilha de 2024 corresponde à competência de processamento 2025.", "diu"),
    ("IMPLANTE (o nome da coluna tem um espaço final)", "SIH/SUS, SP", "Registros de inserção de implante subdérmico (0301040176). Mesma atribuição de ano do DIU.", "imp"),
    ("TOTAL.1", "derivada", "DIU + IMPLANTE.", "larc"),
    ("CLASSIFICAÇÃO CONTRACEPÇÃO", "derivada", "SIM se TOTAL.1 ≥ 3; caso contrário, vazio.", "contrOk"),
    ("SEÇÃO", "ATENDIMENTO DE VIOLÊNCIA SEXUAL (SIA/SUS)"),
    ("Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL", "SIA/SUS, PA (2025)",
     "Soma da quantidade aprovada (PA_QTDAPR) dos procedimentos 0301040052 e 0301040060, por estabelecimento executante (PA_CODUNI), na competência de realização (PA_CMP) do ano, "
     "lida nos arquivos PA de movimento 01 a 12/2025 (produção de 2025 apresentada em 2026 não entra). A coluna de 2024 da planilha institucional não é reproduzida por essa regra "
     "(fonte não confirmada).", "violN"),
    ("CLASSIFICAÇÃO VIOLÊNCIA SEXUAL", "derivada", "SIM se nº ≥ 2; caso contrário, vazio.", "viol"),
    ("SEÇÃO", "SMCON (IFF/Fiocruz)"),
    ("SMCON NEO", "lista de adesão do IFF (2024)", "'ok' quando o estabelecimento aderiu ao módulo Cuidado Neonatal. Em 2025 repete-se a lista de 2024; 18 das 555 unidades de 2025 não constam da lista e ficam em branco (não aderidas).", "smN"),
    ("SMCON OBST", "lista de adesão do IFF (2024)", "'ok' quando o estabelecimento aderiu ao módulo obstétrico (Parto e Nascimento; a inclusão do módulo Abortamento está em confirmação).", "smO"),
    ("SMCON TOTAL", "derivada", "0, 1 ou 2 módulos.", "—"),
    ("SEÇÃO", "CLASSIFICAÇÃO GERAL"),
    ("CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS", "derivada (campo classificatório oficial da planilha)",
     "ADEQUADO quando pelo menos 5 dos 9 marcadores da base são positivos: asfixia, enfermeira, AMIU, Robson ≥ 2, LARC, violência, SMCON NEO, SMCON OBST e unidade neonatal (SIM ou NÃO SE APLICA). "
     "No recálculo de 2025 fica em branco quando a unidade não está na lista do SMCON ou quando falta LARC ou violência. O painel não usa esse campo diretamente: recalcula o número de "
     "indicadores adequados com o SMCON consolidado em um único indicador (n8, de 0 a 8) e classifica o estabelecimento em estágios de desempenho (Tabela 2). O campo oficial é guardado "
     "só para auditoria (campo 'oficial').",
     "oficial (campo oficial da planilha, 1/0); avanc (1 se n8 ≥ 5, isto é, estágio Avançando); nAdeq (0 a 9); n8 (0 a 8); flags (9 caracteres, na ordem acima)"),
]

# ----------------------------------------------------------------------------------------------------------------
# TABELA 2: indicadores classificatórios e estágios
# ----------------------------------------------------------------------------------------------------------------
IND = [
    ("Unidade neonatal completa", "UNIDADE NEONATAL COMPLETA = SIM ou NÃO SE APLICA", "CNES, LT (leitos 81/82, 92 e 93)", "% de estabelecimentos adequados (n/total)", "neo; posição 9"),
    ("Cesariana por grupos de Robson (≥ 2 grupos adequados)", "TOTAL CLASSIFICAÇÃO ≥ 2 (grupos G1 a G4 dentro do intervalo)", "SINASC (TPROBSON, PARTO)",
     "% de estabelecimentos adequados; % de adequados por grupo (G1 a G4); gráfico: média do percentual de cesariana dos estabelecimentos com NV no grupo", "rob2, robAd, g1C … g4C; posição 4"),
    ("Parto vaginal assistido por enfermeira", "% ≥ 50", "SINASC (TPNASCASSI = 2 ÷ PARTO = 1)", "% de estabelecimentos adequados", "enf, enfC; posição 2"),
    ("Uso de AMIU", "% ≥ 50", "SIH/SUS, RD (0409060070 ÷ 0409060070 + 0411020013)", "média do percentual entre os estabelecimentos; % de adequados", "amiu; posição 3"),
    ("Asfixia neonatal", "% ≤ 0,6", "SINASC (APGAR5 < 7, PESO ≥ 2.500 g, IDANOMAL = 2 ÷ todos os NV)", "% de estabelecimentos adequados", "asf, asfC; posição 1"),
    ("Oferta de LARC", "DIU + implante ≥ 3 registros no ano", "SIH/SUS, SP (0301040141, 0301040176)", "% de estabelecimentos adequados", "larc, diu, imp, contrOk; posição 5"),
    ("Atendimento de violência sexual", "≥ 2 atendimentos no ano", "SIA/SUS, PA (0301040052, 0301040060), 2025; fonte de 2024 não confirmada", "% de estabelecimentos adequados", "violN, viol; posição 6"),
    ("SMCON Neonatal e/ou Obstétrico", "adesão a pelo menos um módulo", "lista de adesão do IFF (2024)", "% de estabelecimentos adequados (o SMCON conta uma única vez)", "smN, smO; posições 7 e 8"),
    ("SEÇÃO", "ESTÁGIOS DE DESEMPENHO (n8 = número de indicadores adequados entre os 8; o SMCON conta uma única vez)"),
    ("Avançando", "n8 ≥ 5", "derivado", "número e % de estabelecimentos", "avanc = 1; n8"),
    ("Quase lá", "n8 = 4", "derivado", "número e % de estabelecimentos", "n8"),
    ("No caminho", "n8 = 2 ou 3", "derivado", "número e % de estabelecimentos", "n8"),
    ("Início da jornada", "n8 = 0 ou 1", "derivado", "número e % de estabelecimentos", "n8"),
    ("Indicador indisponível no ano", "coluna inteiramente vazia na planilha (por exemplo, LARC, violência ou SMCON sem fonte)", "—",
     "a posição em 'flags' recebe '-', n8 e o estágio são nulos e o painel não exibe os estágios do ano (ano_<ano>.json: campos indisponiveis e semEstagios)", "flags; n8 = null"),
]

# ----------------------------------------------------------------------------------------------------------------
# TABELA 3: comparação regional, indicadores do SINASC (regional.py)
# ----------------------------------------------------------------------------------------------------------------
REG_SINASC = [
    ("Cesariana", "NV com PARTO = 2", "NV com PARTO = 1 ou 2", "PARTO (1 = vaginal; 2 = cesáreo); valores ignorados excluídos do denominador", "% dos partos", "ces / parto_inf"),
    ("Cesariana por grupo de Robson", "cesarianas no grupo", "NV no grupo", "TPROBSON 1 a 10; 11 = não classificado no SINASC. O script recodifica 11, ignorado e inválido como grupo 0 ('não classificado'), mantido como grupo próprio",
     "% no grupo; distribuição dos grupos (% dos NV); contribuição = cesarianas do grupo ÷ partos informados, em p.p.", "ces_g{k} / nv_g{k}"),
    ("Cesariana padronizada por Robson", "Σ peso_k × (ces_gk ÷ nv_gk)", "—",
     "Padronização direta; pesos: distribuição dos 11 grupos (1 a 10 e não classificado) no Brasil, por local de ocorrência, em 2024. Não é calculada quando algum grupo tem 0 NV no território. Sem IC",
     "%", "aba Robson, linha TOTAL"),
    ("Prematuridade", "NV com idade gestacional < 37 semanas", "NV com IG informada", "SEMAGESTAC (17 a 47 semanas); se ausente ou fora dessa faixa, GESTACAO 1 a 4 (< 37) ou 5 e 6 (≥ 37)", "% dos NV", "pret / ig_inf"),
    ("Baixo peso", "NV com PESO < 2.500 g", "NV com peso informado (200 a 8.000 g)", "PESO", "% dos NV", "bp / peso_inf"),
    ("Muito baixo peso", "NV com PESO < 1.500 g", "idem", "PESO", "por 1.000 NV", "mbp / peso_inf"),
    ("Apgar no 5º minuto < 7", "NV com APGAR5 < 7", "NV com APGAR5 informado (0 a 10)", "APGAR5", "por 1.000 NV", "apg7 / apg_inf"),
    ("Asfixia com denominador restrito (regra da Coordenação, 2025)", "APGAR5 < 7 em NV com PESO ≥ 2.500 g e IDANOMAL = 2", "NV com PESO ≥ 2.500 g, IDANOMAL = 2 e Apgar informado",
     "APGAR5, PESO, IDANOMAL; denominador restrito, diferente do usado no painel por estabelecimento (todos os NV)", "%", "asf_num / asf_den"),
    ("Anomalia congênita", "NV com IDANOMAL = 1", "NV com IDANOMAL = 1 ou 2", "IDANOMAL (9 ou vazio: excluído do denominador). O aumento em 2025 provavelmente reflete mudança no registro", "por 10.000 NV", "anom / anom_inf"),
    ("Parto vaginal por enfermeira ou obstetriz", "PARTO = 1 e TPNASCASSI = 2", "PARTO = 1 e TPNASCASSI 1 a 4",
     "TPNASCASSI (1 = médico; 2 = enfermeira/obstetriz; 3 = parteira; 4 = outros); ignorado excluído do denominador (diferente do painel por estabelecimento)", "%", "enf_num / enf_den"),
    ("Mãe adolescente", "IDADEMAE < 20", "NV com IDADEMAE de 8 a 60", "IDADEMAE", "%", "adolesc / idade_inf"),
    ("Mãe com 35 anos ou mais", "IDADEMAE ≥ 35", "idem", "IDADEMAE", "%", "idade35 / idade_inf"),
    ("Pré-natal com 7 ou mais consultas", "CONSPRENAT ≥ 7", "NV com CONSPRENAT de 0 a 60", "CONSPRENAT (número de consultas)", "%", "pn7 / pn_inf"),
    ("Gestação múltipla", "GRAVIDEZ = 2 ou 3", "NV com GRAVIDEZ 1 a 3", "GRAVIDEZ (1 = única; 2 = dupla; 3 = tripla ou mais)", "%", "multipla / grav_inf"),
    ("Nascimento em hospital", "LOCNASC = 1", "todos os NV", "LOCNASC", "% dos NV", "hosp / nv"),
    ("Cobertura do painel", "NV nas unidades do painel", "NV ocorridos na região (ou de residentes)", "CODESTAB na lista do ano; CODMUNNASC; CODMUNRES. Sem IC", "%", "nv (painel) / nv (ocorr ou resid)"),
]

# ----------------------------------------------------------------------------------------------------------------
# TABELA 4: comparação regional, mortalidade (sim_regional.py)
# ----------------------------------------------------------------------------------------------------------------
REG_SIM = [
    ("Mortalidade neonatal", "óbitos de 0 a 27 dias de vida", "NV (SINASC) do mesmo recorte",
     "Idade em dias na DO = DTOBITO − DTNASC; na falta de DTNASC, usa-se o campo IDADE, cujo primeiro dígito é a unidade (0 = minutos, 1 = horas, 2 = dias, 3 = meses, 4 = anos, "
     "5 = mais de 100 anos; dicionário do SIM da SES-ES e IDADE.CNV do TabNet): unidades 0 e 1 valem 0 dias e a unidade 2 dá os dias. Referência: ficha IDB C.1.4", "por 1.000 NV", "neo / nv"),
    ("Mortalidade neonatal precoce", "óbitos de 0 a 6 dias", "NV", "idem. Referência: IDB C.1.1", "por 1.000 NV", "neo_prec / nv"),
    ("Mortalidade neonatal tardia", "óbitos de 7 a 27 dias", "NV", "idem. Referência: IDB C.1.2", "por 1.000 NV", "neo_tard / nv"),
    ("Mortalidade infantil", "óbitos com menos de 1 ano (0 a 364 dias)", "NV",
     "idem; sem DTNASC, óbitos com IDADE em meses (unidade 3) não são recuperados. Apresentada apenas por residência, porque o estabelecimento do óbito nem sempre é o do nascimento. "
     "Referência: IDB C.1", "por 1.000 NV", "inf / nv"),
    ("Mortalidade fetal", "óbitos fetais com SEMAGESTAC ≥ 22 ou PESO ≥ 500 g", "NV + óbitos fetais elegíveis",
     "DOFET (arquivo nacional de óbitos fetais; não há filtro adicional por TIPOBITO). Validade: SEMAGESTAC de 1 a 44 semanas; PESO de 100 a 8.000 g. Óbitos fetais sem IG e sem peso válidos "
     "ficam fora do numerador e do denominador (contados em fetal_ign); os demais não elegíveis, em fetal_menor22. Referência: componente fetal da ficha IDB C.2, que usa só o critério "
     "de 22 semanas; a inclusão alternativa por peso ≥ 500 g é adaptação", "por 1.000 nascimentos", "fetal / nasc_tot"),
    ("Mortalidade perinatal", "óbitos fetais elegíveis + óbitos de 0 a 6 dias", "NV + óbitos fetais elegíveis", "Referência: IDB C.2", "por 1.000 nascimentos", "perinatal / nasc_tot"),
    ("Razão de mortalidade materna (RMM)", "óbitos maternos (regra MS/OOBr)", "NV",
     "Mulher (SEXO = 2); CAUSABAS O00 a O95, O98 e O99 sempre; B20 a B24, D39.2 e E23.0 só com OBITOGRAV = 1 ou OBITOPUERP = 1; A34, F53 e M83.0 com OBITOPUERP = 1 ou ignorado. "
     "OBITOGRAV vazio é tratado como 9; OBITOPUERP vazio, 0, 4 e 8 são tratados como 9. Óbitos maternos tardios (O96 e O97) são contados à parte, fora da RMM, sem restrição de idade "
     "(o TabNet os restringe a 10 a 49 anos). Conferência: óbitos maternos por UF de residência idênticos ao TabNet/DATASUS (mat10uf) em 2024 e 2025. Referências: IDB C.3; "
     "Auditoria_regras_indicadores_mortalidade.md (10/09/2026)", "por 100.000 NV", "materno / nv; materno_tardio"),
    ("Óbitos de mulheres em idade fértil (MIF)", "óbitos de mulheres de 10 a 49 anos", "—", "SEXO = 2 e IDADE 4xx de 10 a 49. Só no JSON; não entra no relatório nem na planilha", "número", "mif"),
]

# ----------------------------------------------------------------------------------------------------------------
# TABELA 5: recortes, territórios e estatística
# ----------------------------------------------------------------------------------------------------------------
RECORTES = [
    ("painel", "Estabelecimentos incluídos no painel do ano (coluna CNES da planilha), por UF de ocorrência. Quando um estabelecimento tem mais de um código (mudança de código ou complexo), "
     "todos os códigos entram, nos dois anos: 2679663/9131922, 3511251/5878640 e 2025507/2025523 (HC FAMEMA, embora a planilha de 2024 não some o complexo).",
     "SINASC: CODESTAB na lista; UF = dois primeiros dígitos de CODMUNNASC. SIM: CODESTAB na lista; UF = dois primeiros dígitos de CODMUNOCOR. O óbito é atribuído ao estabelecimento onde ocorreu, não àquele onde o RN nasceu."),
    ("demais estab.", "NV e óbitos ocorridos na região fora das unidades do painel (região − painel): hospitais privados sem atendimento pelo SUS, hospitais do SUS com até 1.000 partos e nascimentos fora de hospital.",
     "Calculado por subtração dos contadores (ocorr − painel), em cada UF."),
    ("região (ocorrência)", "Todos os NV e óbitos ocorridos na região.", "SINASC: CODMUNNASC; SIM: CODMUNOCOR. Inclui as próprias unidades do painel."),
    ("residência", "NV e óbitos de residentes da região, independentemente do local de ocorrência; recorte adequado para prevalência e incidência populacionais.", "SINASC: CODMUNRES; SIM: CODMUNRES."),
    ("SEÇÃO", "TERRITÓRIOS"),
    ("UF", "27 unidades da federação; código IBGE de 2 dígitos (11 a 53); '99' = município ignorado ou inválido (incluído apenas no total Brasil).", "Código do município com 6 dígitos ou mais; UF = dois primeiros dígitos."),
    ("Região", "Primeiro dígito do código da UF: 1 Norte, 2 Nordeste, 3 Sudeste, 4 Sul, 5 Centro-Oeste.", "Brasil = soma de todas as UFs, inclusive '99'."),
    ("SEÇÃO", "ESTATÍSTICA"),
    ("Proporção e intervalo de confiança de 95 % (IC 95 %)", "numerador ÷ denominador × escala; intervalo de Wilson (z = 1,96).",
     "Indicadores das tabelas 3 e 4 com numerador e denominador (não se aplica à cobertura, à cesariana padronizada nem às linhas por grupo de Robson); colunas <recorte>, <recorte>_ic_inf e <recorte>_ic_sup."),
    ("Razão painel/demais", "(k1/n1) ÷ (k2/n2); IC na escala logarítmica: exp[ln(razão) ± 1,96 × √(1/k1 − 1/n1 + 1/k2 − 1/n2)].", "Razão > 1 indica frequência maior nas unidades do painel. Não é calculada quando algum numerador é zero."),
    ("Cesariana padronizada", "Padronização direta pela distribuição dos grupos de Robson (Brasil, ocorrência, primeiro ano da série).", "Remove o efeito das diferenças de perfil obstétrico; pesos na aba Pesos Robson."),
    ("Cobertura", "NV nas unidades do painel ÷ NV da região (ocorrência ou residência) × 100.", "Aba Cobertura."),
]

# ----------------------------------------------------------------------------------------------------------------
# TABELA 6: arquivos e scripts
# ----------------------------------------------------------------------------------------------------------------
ARQS = [
    ("planilhas/ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES_01072026.xlsx", "Base institucional de 2024 (543 unidades, 57 colunas da Tabela 1).", "Coordenação / IFF"),
    ("planilhas/PLANILHA_2025_prelim_internacao.xlsx", "Base de 2025 (555 unidades), recalculada dos microdados com as regras da Tabela 1; preliminar.", "scripts/extracao/montar_planilha.py (parâmetros em .github/workflows/montar_painel.yml)"),
    ("dados/dados_<ano>.json; dados/ano_<ano>.json; dados/flags_nomes.json", "Estabelecimentos do ano com os campos da coluna 'campo no painel'; configuração do ano (n, partos, extração, preliminar, indisponíveis); nomes dos 9 marcadores.", "scripts/01_preparar_dados.py"),
    ("index.html", "Painel publicado (GitHub Pages), montado a partir de painel_template.html e dos arquivos JSON.", "scripts/03_montar_painel.py; 04_auditoria.py (0 falhas antes de publicar); conferência final no workflow"),
    ("extracao/saida/sinasc_<ano>.json", "Agregados do SINASC por CODESTAB: NV e cesarianas por grupo de Robson, asfixia (variante a: anomalia ≠ sim; variante b: anomalia = não, a usada) e parto por enfermeira.", "scripts/extracao/sinasc_indicadores.py"),
    ("extracao/saida/sih_rd/, sih_sp/, sia_pa_<ano>/", "Agregados por UF do SIH (partos, AMIU, laqueadura), dos atos profissionais (DIU, implante) e do SIA (violência).", "sih_partos.py; sih_sp_atos.py; sia_violencia.py (GitHub Actions)"),
    ("extracao/saida/cnes_leitos_2401_<aamm>.json; cnes_fichas.json", "Leitos existentes por CNES e competência e cadastro (gestão, natureza); fichas do CNES com habilitações, município e situação.", "cnes_leitos_neo.py; cnes_habilitacoes.py"),
    ("extracao/saida/codigos_sp.json; codigos_sp_2025.json; extracao/smcon_2024.csv; extracao/territorio/; extracao/cnes_referencia_2024.txt", "Contagens de DIU e implante por CNES (competência 2025; saída 2025); lista de adesão ao SMCON; base territorial; lista de CNES de referência de 2024.", "sih_sp_atos.py; IFF; DATASUS; planilha de 2024"),
    ("extracao/saida/regional_<ano>.json", "Contadores da Tabela 3 por UF, nos recortes ocorr, resid e painel (SINASC completo).", "scripts/extracao/regional.py"),
    ("extracao/saida/sim_regional_<ano>.json", "Contadores da Tabela 4 por UF, nos mesmos recortes (DO de todas as UFs e DOFET), com diagnóstico (registros fora do ano; idade recuperada pelo campo IDADE).", "scripts/extracao/sim_regional.py"),
    ("extracao/saida/tabnet_mat_2024_2025.json", "Tabulação do TabNet/DATASUS (mat10uf: óbitos maternos, tardios e de mulheres em idade fértil por UF e por faixa etária, 2024 e 2025) usada na conferência da mortalidade materna.", "consulta ao TabNet em 09/11/2026"),
    ("relatorios/comparacao_regional.md; planilhas/COMPARACAO_REGIONAL_2024_2025.xlsx", "Relatório e tabelas (abas Cobertura, Por região, Por UF, Robson, Pesos Robson e Diagnóstico SIM), com a conferência da mortalidade materna contra o TabNet.", "scripts/extracao/relatorio_regional.py"),
    ("relatorios/reproducao_2024.md; relatorios/extracao_2024_x_planilha.md", "Reprodução da planilha de 2024 e extração de 2024 com as regras de 2025.", "reproducao_2024.py; comparar_2024.py"),
    ("relatorios/comparacao_2025_tatiana.md", "Comparação com a planilha de 2025 da Coordenação.", "redigido manualmente, sem script"),
    ("dicionarios/DICIONARIO_SMCON_2026-11-09.*", "Dicionário de dados do SMCON (módulos Parto e Nascimento, Abortamento e Cuidado Neonatal).", "gera_dicionario_smcon.py; gera_dicionario_docx.js"),
]

FONTES = [
    "SINASC (Sistema de Informações sobre Nascidos Vivos): arquivos CSV anuais do OpenDataSUS (SINASC_<ano>_csv.zip); 2025 na versão preliminar de 31/08/2026",
    "SIH/SUS (Sistema de Informações Hospitalares): arquivos RD e SP por UF e competência (FTP do DATASUS), competências até 08/2026",
    "SIA/SUS (Sistema de Informações Ambulatoriais): arquivos PA por UF e competência (FTP do DATASUS), 2024 e 2025",
    "CNES (Cadastro Nacional de Estabelecimentos de Saúde): arquivos LT (leitos) por UF e competência; fichas de estabelecimento da API de dados abertos (apidadosabertos.saude.gov.br) e habilitações do serviço cnes.datasus.gov.br",
    "SIM (Sistema de Informações sobre Mortalidade): DO por UF (DO<UF><ano>.dbc ou DO<UF>OPEN<aa>.dbc para preliminares) e DOFET nacional (FTP do DATASUS); 2025 preliminar (versão do FTP de 28/08/2026, baixada em 23/09/2026)",
    "SMCON (Sistema de Monitoramento do Cuidado Obstétrico e Neonatal, IFF/Fiocruz): lista de unidades aderidas fornecida pelo IFF (2024)",
    "Territórios: base territorial do DATASUS (regiões e macrorregiões de saúde, junho/2026) e códigos IBGE",
]

SIGLAS = ("AIH: autorização de internação hospitalar. AMIU: aspiração manual intrauterina. CID-10: Classificação Internacional de Doenças, 10ª revisão. CIR: comissão intergestores regional "
          "(região de saúde). CPN: centro de parto normal. DIU: dispositivo intrauterino. DNV: declaração de nascido vivo. DO: declaração de óbito. DOFET: arquivo de óbitos fetais do SIM. "
          "GAR: gestação de alto risco. HGPAR: hospital geral de referência para atenção à gestante de alto risco. IC: intervalo de confiança. IDB: Indicadores e Dados Básicos (RIPSA/DATASUS). "
          "IG: idade gestacional. LARC: contraceptivos reversíveis de longa duração. LT: arquivo de leitos do CNES. MIF: mulheres em idade fértil. MS: Ministério da Saúde. NV: nascidos vivos. "
          "OOBr: Observatório Obstétrico Brasileiro. PA: arquivo de produção ambulatorial do SIA. p.p.: pontos percentuais. RD: arquivo reduzido da AIH. RMM: razão de mortalidade materna. "
          "RN: recém-nascido. SP: arquivo de serviços profissionais da AIH. UCINCa: unidade de cuidado intermediário neonatal canguru. UCINCo: unidade de cuidado intermediário neonatal "
          "convencional. UF: unidade da federação. UTIN: unidade de terapia intensiva neonatal.")


def main():
    blocos = [
        P("DICIONÁRIO DE DADOS DO PAINEL DE PARTOS: INDICADORES DA ATENÇÃO OBSTÉTRICA E NEONATAL EM ESTABELECIMENTOS COM MAIS DE 1.000 PARTOS E COMPARAÇÃO REGIONAL"),
        P(f"Versão de {DATA[8:]}/{DATA[5:7]}/{DATA[:4]}. Este dicionário descreve as colunas da base por estabelecimento; os 8 indicadores classificatórios e os estágios de desempenho "
          "do painel (2024 e 2025); e os indicadores da comparação regional (SINASC e SIM completos), incluídos em 09/11/2026 em caráter de protótipo. As regras descritas são as "
          "aplicadas pelos scripts do repositório. Quando a regra do painel difere da do dicionário de indicadores da Coordenação de Ações Nacionais e de Cooperação em Saúde da Mulher, "
          "da Criança e do Adolescente do IFF/Fiocruz (aqui, Coordenação), de 09/09/2026, ambas são apresentadas."),
        P("Universo. Estabelecimentos com mais de 1.000 partos pelo SUS no ano, contados nas AIH de parto do SIH/SUS: 543 em 2024 (1.253.881 partos; planilha institucional de 01/07/2026) "
          "e 555 em 2025 (1.272.466 partos; recálculo preliminar de 04/11/2026). Os agregados do painel referem-se apenas a esses estabelecimentos, chamados aqui de unidades do painel. "
          "A comparação regional usa, além deles, todos os nascidos vivos (NV) e óbitos do país, em quatro recortes (Tabela 5). Em 2024 os valores da base são os da planilha "
          "institucional; a regra descrita na Tabela 1 é a do recálculo de 2025 e, quando difere, a regra que reproduz a planilha de 2024."),
        P("Fontes: " + "; ".join(FONTES) + "."),
        P("Siglas. " + SIGLAS),
        P("Tabela 1. Base por estabelecimento: colunas da planilha ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_<ano> e campos do painel"),
        tabela(["COLUNA DA PLANILHA", "FONTE", "REGRA DE CÁLCULO / CONTEÚDO", "CAMPO NO PAINEL (dados_<ano>.json)"], BASE),
        P("Tabela 2. Indicadores classificatórios e estágios de desempenho"),
        tabela(["INDICADOR", "PARÂMETRO DE ADEQUAÇÃO (por estabelecimento)", "FONTE E VARIÁVEIS", "AGREGADO EXIBIDO", "CAMPOS / POSIÇÃO EM 'flags'"], IND),
        P("Tabela 3. Comparação regional: indicadores do SINASC (todos os estabelecimentos)"),
        tabela(["INDICADOR", "NUMERADOR", "DENOMINADOR", "CAMPOS DO SINASC E VALIDADE", "ESCALA", "CHAVES (regional_<ano>.json)"], REG_SINASC),
        P("Tabela 4. Comparação regional: mortalidade (SIM, DO e DOFET)"),
        tabela(["INDICADOR", "NUMERADOR", "DENOMINADOR", "CAMPOS DO SIM E REGRA", "ESCALA", "CHAVES (sim_regional_<ano>.json)"], REG_SIM),
        P("Tabela 5. Recortes, territórios e estatística da comparação regional"),
        tabela(["TERMO", "DEFINIÇÃO", "OPERACIONALIZAÇÃO"], RECORTES),
        P("Tabela 6. Arquivos e scripts"),
        tabela(["ARQUIVO", "CONTEÚDO", "GERADO POR / ORIGEM"], ARQS),
        P("Notas"),
        P("1. Regras de 2024 e de 2025. A planilha institucional de 2024 contou os partos pela competência de processamento 2025, o AMIU pela data de saída em 2024 e os atos de DIU e implante "
          "pela competência 2025, e não somou o complexo HC FAMEMA; o recálculo de 2025 usa a data de internação para partos e AMIU, a data de saída para DIU e implante, e soma o complexo. "
          "Pela data de internação em 2024, as 543 unidades da planilha somariam 1.219.014 partos (contra 1.253.881) e o universo de mais de 1.000 partos teria 526 unidades "
          "(relatorios/extracao_2024_x_planilha.md). A coluna de violência sexual de 2024 não é reproduzida pelo SIA/SUS; a de 2025 vem do SIA/SUS. O SMCON de 2025 repete a lista de 2024."),
        P("2. Regras do painel que diferem do dicionário da Coordenação. Laqueadura 0409060313 não contada como parto; universo sem o filtro obstétrico (sexo feminino, 10 a 59 anos, "
          "CID-10 capítulo O); denominador da asfixia com todos os NV, e não apenas os NV com peso ≥ 2.500 g e sem anomalia; parto por enfermeira com os profissionais ignorados no denominador; "
          "Robson pelos intervalos observados na planilha de 2024, não pelas metas ≤ 10 %, ≤ 35 %, ≤ 3 % e ≤ 15 %. A comparação regional (Tabela 3) usa os denominadores restritos (asfixia e "
          "enfermeira); por isso, seus valores não coincidem com os do painel por estabelecimento."),
        P("3. Limitações da mortalidade por estabelecimento. A DO informa o estabelecimento do óbito (CODESTAB), não o do nascimento. Maternidades com UTI neonatal de referência recebem óbitos "
          "de RN nascidos em outros serviços, e o denominador (NV nascidos na unidade) não os inclui. Por isso, a razão painel/demais superestima a mortalidade nas unidades do painel; a taxa por "
          "residência é a medida populacional. Os óbitos maternos de 2025 são preliminares e ainda aumentam à medida que os casos são investigados."),
        P("4. Valores ignorados. Nos indicadores da comparação regional com variável de validade definida (peso, Apgar, idade gestacional, anomalia, idade da mãe, consultas, tipo de gravidez, "
          "profissional), os registros com valor ignorado ou inválido são excluídos do denominador. Exceções: nascimento em hospital e mortalidade usam todos os NV; o grupo de Robson não "
          "classificado é mantido como grupo próprio; idade gestacional em semanas fora de 17 a 47 recorre à faixa GESTACAO. No painel por estabelecimento, a asfixia usa como denominador "
          "todos os NV, e o parto por enfermeira, todos os partos vaginais."),
        P("5. Atualização. Executar regional.py e sim_regional.py para o ano e, em seguida, relatorio_regional.py. Para o painel, executar, nesta ordem: montar_planilha.py → 01_preparar_dados.py "
          "→ 04_auditoria.py (0 falhas) → 03_montar_painel.py → conferência final (05_conferencia.py localmente; no workflow, etapa equivalente). Para outro ano, informar --sia-atrib "
          "(padrão c2025) e --cnes. Este dicionário é gerado por gera_dicionario_painel.py; a versão Word, por gera_dicionario_docx.js."),
    ]
    json.dump(blocos, open(SAIDA_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    md = []
    for b in blocos:
        if b["tipo"] == "p":
            t = b["texto"]
            if t.isupper() or t.startswith("Tabela ") or t == "Notas":
                md.append(("# " if t.isupper() else "## ") + t)
            else:
                md.append(t)
            md.append("")
        else:
            cab = [c[0] for c in b["linhas"][0]]
            md.append("| " + " | ".join(cab) + " |"); md.append("|" + "---|" * len(cab))
            for l in b["linhas"][1:]:
                if len(l) == 1:
                    md.append("| **" + l[0][0] + "** |" + " |" * (len(cab) - 1))
                else:
                    md.append("| " + " | ".join(" ".join(c).replace("|", "/") for c in l) + " |")
            md.append("")
    open(SAIDA_MD, "w", encoding="utf-8").write("\n".join(md))
    n = {i: len(b["linhas"]) - 1 for i, b in enumerate(blocos) if b["tipo"] == "tabela"}
    print("ok:", SAIDA_JSON, "| linhas por tabela:", n)


if __name__ == "__main__":
    main()
