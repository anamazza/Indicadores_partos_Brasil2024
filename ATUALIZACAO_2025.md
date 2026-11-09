# Atualização do painel para 2025 — briefing para a sessão local

> Para abrir no Claude Code **no computador da Ana** (app Desktop ou `claude` no terminal), dentro da
> pasta que contém os projetos de extração. Este arquivo substitui o contexto da conversa na nuvem:
> leia-o inteiro antes de começar. Linguagem: português.

**Painel a atualizar:** https://anamazza.github.io/Indicadores_partos_Brasil2024/ (repositório
`anamazza/Indicadores_partos_Brasil2024`, GitHub Pages pela raiz da `main`).
**Objetivo:** acrescentar o ano de **2025** com as **mesmas regras já definidas** para 2024, de preferência
mantendo os dois anos no painel (seletor de ano + evolução de cada unidade), com 2025 marcado como
**preliminar**. Nada do método muda; o que muda é o ano dos dados.

---

## 0. Antes de tudo: localizar os dados na máquina

A Ana não lembra se os dados de extração ficaram no OneDrive, no Google Drive ou só no disco. Procure
antes de baixar qualquer coisa — os microdados do SIH são pesados (≈31 GB acumulados) e já foram baixados.

O que procurar (nomes conhecidos, vindos dos READMEs do repositório `anamazza/Indicadores_Brasil`):

| O quê | Nome/pasta conhecida | Observação |
|---|---|---|
| Esteira do SIH (AIH) | pasta `Extracao_SIH` (scripts numerados `1_baixar_sih.py`, `55`/`56`/`61`, `63_baixar_2026.py`, `tabula_periodo.py`, `gera_tabula_periodo.py`, `extrai_leitos_periodo.py`; saída em `saida/planilhas_corrigidas_v3.json`, `saida/tabulacao_2026S1/`) | microdados `RD<UF><aamm>.dbc` (AIH reduzida) e `SP<UF><aamm>.dbc`; pode haver versões convertidas (`.parquet`/`.csv`) |
| Esteira do SINASC | pasta `Extracao_SINASC` (`baixar_sinasc.py`, `1_coleta_unidades.py`, `2_tabelas_unidades.py`, `10_perfil_sociodemografico.py`, `11_perfil_obstetrico_novos.py`) | CSV anuais `SINASC_<ano>_csv.zip` do OpenDataSUS |
| Pipeline comum | pasta `Pipeline_Python` | |
| Pastas de trabalho dos painéis | `Pojeto Apresentações NV_2026/Painel_2026_Novo`, `Projeto Apresentações Internação/Painel_Internacao`, `Mortalidade Indicadores/Painel_Mortalidade` (OneDrive/Documentos) | as esteiras ficam nas pastas vizinhas (`../Extracao_SIH`, `../Extracao_SINASC`) |
| Clone do hub | `Documentos/Página principal` (repositório `Indicadores_Brasil`) | |
| Planilha-base de 2024 | `ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES_01072026.xlsx` | **não está em nenhum repositório**; é a referência de validação |

Busca sugerida no Windows (PowerShell), cobrindo disco, OneDrive e Google Drive para computador:

```powershell
$raizes = @("$env:USERPROFILE", "$env:OneDrive", "G:\Meu Drive", "$env:USERPROFILE\Google Drive", "D:\") | Where-Object { $_ -and (Test-Path $_) }
foreach ($r in $raizes) {
  Get-ChildItem $r -Recurse -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match 'Extracao_SIH|Extracao_SINASC|Pipeline_Python|Painel_Internacao|Painel_2026_Novo|gina principal' } |
    Select-Object FullName
  Get-ChildItem $r -Recurse -File -ErrorAction SilentlyContinue -Include 'RD*.dbc','SINASC_20*','planilhas_corrigidas_v3.json','ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS*.xlsx' |
    Select-Object FullName, Length | Select-Object -First 40
}
```

Se os microdados do SIH **não** estiverem na máquina, o download refaz-se com a própria esteira
(`1_baixar_sih.py`, FTP do DATASUS `SIHSUS/200801_/Dados`, arquivos `RD<UF><aamm>.dbc`) — do Brasil o FTP
responde. Só é preciso 2024 (validação) e 2025 (atualização), todas as UFs. O SINASC baixa-se de
`https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SINASC/csv/SINASC_<ano>_csv.zip` (2024 ≈ 92 MB;
2025 ≈ 102 MB, versão preliminar de 31/08/2026).

---

## 1. Os dois repositórios e o que cada um dá

### `anamazza/Indicadores_partos_Brasil2024` (o painel)

- `painel_template.html` → `scripts/03_montar_painel.py` → `index.html`. **Nunca editar o `index.html`
  diretamente**; o template é a fonte.
- `scripts/01_preparar_dados.py <planilha.xlsx>` → `dados/dados.json` + `dados/flags_nomes.json`.
- `scripts/04_auditoria.py <planilha.xlsx>` → recalcula tudo da planilha e compara com `dados.json`
  (**37 verificações; tem de terminar com 0 falhas** antes de publicar).
- `METODOLOGIA.md` e `README.md`: regras, fichas dos indicadores, números nacionais de 2024.
- `dados/dados.json`: os 543 estabelecimentos de 2024 já processados (por CNES) — serve de gabarito para
  comparar qualquer reprodução.

### `anamazza/Indicadores_Brasil` (hub dos painéis das maternidades)

- `docs/apostila_src/fontes/DICIONARIO_INDICADORES_AIH_versao_final_2026-09-10.json`: regras e códigos SIGTAP
  do SIH aprovados pela coordenação em 09/09/2026 (lista na seção 4).
- `docs/apostila_src/fontes/painel_nv_metodologia.json`: numerador/denominador dos indicadores do SINASC.
- `monitor/estado.json`: quais arquivos do SINASC/SIM/SIH existiam no DATASUS na última consulta (datas e
  competências por UF) — útil para saber até que competência 2025 está disponível.
- `.github/workflows/cnes.yml` + `<painel>/atualizar_cnes.py`: consulta da ficha CNES pela API de Dados
  Abertos (`https://apidadosabertos.saude.gov.br/cnes/estabelecimentos/{cnes}`) e das habilitações pelo
  serviço do site do CNES (`https://cnes.datasus.gov.br/services/estabelecimentos-habilitacoes/{cnes}`).
- `ESTRATEGIA_ATUALIZACAO.md`: onde cada fonte roda (SIH só local; CNES na nuvem; SINASC local/nuvem).

---

## 2. Formato-alvo: a planilha de 2024

A entrada do pipeline é uma planilha com **uma linha por estabelecimento** e estas colunas (nomes exatos,
como o `01_preparar_dados.py` lê). A planilha de 2025 deve nascer **neste mesmo formato**:

```
REGIÃO DO PAÍS · UF · MUNICÍPIO · CÓD MRS · MACRORREGIÃO DE SAÚDE · CÓD RS · REGIÃO DE SAÚDE
CNES - ESTABELECIMENTO ("<CNES> - <NOME>") · GESTÃO · NATUREZA JURÍDICA · HGPAR (SIM/NÃO)
UNIDADE NEONATAL COMPLETA (SIM / NÃO / NÃO SE APLICA)
TOTAL (partos) · OPERAÇÃO CESARIANA · OPERAÇÃO CESARIANA C/ LAQUEADURA TUBARIA · OPERAÇÃO CESARIANA EM GAR
PARTO NORMAL · PARTO NORMAL EM CPN · PARTO NORMAL EM GESTACAO DE ALTO RISCO
% ASFIXIA ≥2500G SEM ANOMALIAS CONGÊNITAS · CLASSIFICAÇÃO ASFIXIA (ADEQUADO/INADEQUADO)
% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM · CLASSIFICAÇÃO PARTO ENF.
% AMIU · CLASSIFICAÇÃO AMIU
% CESAREANA G1..G4 · TOTAL NV G1..G4 · Nº CESAREANA G1..G4 · CLASSIFICAÇÃO G1..G4 (1/0)
TOTAL CLASSIFICAÇÃO (nº de grupos adequados) · CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS) (ADEQUADO/INADEQUADO)
DIU · IMPLANTE · TOTAL.1 (DIU+implante) · CLASSIFICAÇÃO CONTRACEPÇÃO (SIM/NÃO)
Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL · CLASSIFICAÇÃO VIOLÊNCIA SEXUAL (SIM/NÃO)
SMCON NEO · SMCON OBST ("ok" quando adere)
CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS (campo oficial: ADEQUADO quando ≥5 das 9 flags)
```

Universo: **estabelecimentos com mais de 1.000 partos no ano** (TOTAL > 1.000, partos SUS pelo SIH).
Em 2024: 543 estabelecimentos, 1.253.881 partos. O universo de 2025 será recalculado com o mesmo corte.

Valores nacionais de 2024 para conferência (de `METODOLOGIA.md`, seção 6): cesariana adequada (≥2 grupos)
56,7% (308/543) · parto vaginal por enfermeira 28,5% (155/543) · asfixia neonatal 71,5% (388/543) · oferta de
LARC 35,7% (194/543) · violência sexual 41,4% (225/543) · SMCON e/ou 22,1% (120/543) · unidade neonatal
completa 43,6% (237/543) · uso de AMIU (média) 12,6% · Avançando 108 · Quase lá 140 · No caminho 232 ·
Início da jornada 63. Médias de cesariana por grupo: G1 36,1% · G2 66,3% · G3 18,5% · G4 49,1%.

---

## 3. Ordem de trabalho

### Passo 1 — Reproduzir 2024 (prova de que a regra foi reproduzida)

Antes de tocar em 2025, recalcular as colunas da planilha de 2024 **a partir dos microdados** e comparar,
CNES a CNES, com a planilha oficial. É este relatório que a coordenação precisa ver.

**SINASC 2024** (variáveis da DNV — conferir no dicionário oficial do SINASC):

| Indicador | Cálculo (por `CODESTAB`) |
|---|---|
| Nascidos vivos por grupo de Robson (`TOTAL NV G1..G4`) | contagem por `TPROBSON` (01–10; demais = não classificado) |
| Cesáreas por grupo (`Nº CESAREANA G1..G4`) | `PARTO = 2` dentro de cada grupo; `% CESAREANA Gn` = cesáreas ÷ NV do grupo × 100 |
| `% ASFIXIA ≥2500G SEM ANOMALIAS` | numerador: `APGAR5` 0–6; denominador: NV com Apgar informado, `PESO ≥ 2500` e `IDANOMAL ≠ 1` (sem anomalia); os demais não entram em nenhum dos dois |
| `% PARTO VAGINAL ASSISTIDO POR ENFERMAGEM` | numerador: `TPNASCASSI = 2` (enfermeira/obstetriz); denominador: `PARTO = 1`, excluídos os registros com profissional ignorado |

**SIH/SUS 2024** (AIH reduzida `RD`, variável `PROC_REA`, por `CNES`; universo obstétrico = mulheres de 10 a
59 anos; seguir as **regras v3 de 09/09/2026** da esteira local para competência × data de internação e
para AIH aprovadas — não reinventar: ler `tabula_periodo.py`/`gera_tabula_periodo.py` em `Extracao_SIH`):

| Coluna | Códigos SIGTAP |
|---|---|
| PARTO NORMAL / EM CPN / EM GESTAÇÃO DE ALTO RISCO | `0310010039` / `0310010047` / `0310010055` |
| (parto vaginal com laqueadura na mesma internação) | `0409060313` — regra vigente desde a competência 04/2024; a coordenação decidiu (09/09/2026) que é parto vaginal em todas as listas. A planilha de 2024 **não** tem esta coluna: verificar se foi somada ao parto normal ou ignorada |
| OPERAÇÃO CESARIANA EM GAR / CESARIANA / C/ LAQUEADURA | `0411010026` / `0411010034` / `0411010042` |
| AMIU | `0409060070` (`% AMIU` = AMIU ÷ (AMIU + curetagem) × 100) |
| Curetagem pós-abortamento/puerperal | `0411020013` (a curetagem semiótica `0409060046` **não** entra no AMIU) |
| DIU · IMPLANTE · violência sexual | **códigos não constam do dicionário** — procurar nos scripts da esteira local; se não houver, confirmar com a Tatiana antes de calcular |

**CNES 2024**: `UNIDADE NEONATAL COMPLETA` = leitos existentes de UTIN, UCINCo e UCINCa (nota metodológica:
"sim" com os três tipos; "não" faltando algum; "não se aplica" sem unidade neonatal); `HGPAR`, `GESTÃO`,
`NATUREZA JURÍDICA`. Confirmar com a Tatiana a **competência do CNES** usada em 2024 e se foram leitos
existentes ou habilitações. A API de Dados Abertos e o serviço de habilitações (seção 1) funcionam da
máquina local; os arquivos mensais do CNES (`BASE_DE_DADOS_CNES_aaaamm`, tabela `tbLeito`/`rlEstabComplementar`)
ficam no FTP do DATASUS.

**Critério de aceite do passo 1:** para os 543 CNES, cada coluna recalculada igual à planilha (contagens
exatas; percentuais com 1 casa decimal; classificações idênticas). Diferenças devem ser explicadas (regra
nova do `0409060313`, competências acrescidas, AIH rejeitadas…) e listadas num relatório
`relatorios/reproducao_2024.md` (tabela coluna × nº de CNES iguais × diferenças com exemplos).

### Passo 2 — Calcular 2025

Mesmas rotinas com SINASC 2025 (preliminar) e SIH 2025 (competências disponíveis — ver `monitor/estado.json`
e o FTP; a esteira local tinha até 06/2026 em outubro). Recortar o universo (TOTAL > 1.000 partos em 2025),
montar a planilha 2025 no formato da seção 2, com as classificações pelas regras da seção 5. SMCON 2025 vem
da equipe do IFF (lista CNES × módulo); até chegar, deixar as duas colunas vazias e **não** publicar
estágios de desempenho de 2025.

### Passo 3 — Pipeline, auditoria e painel

1. `python scripts/01_preparar_dados.py PLANILHA_2025.xlsx` (gera `dados/dados.json`).
2. `python scripts/04_auditoria.py PLANILHA_2025.xlsx` → **0 falhas**.
3. Decisão de desenho recomendada: **2024 × 2025 no mesmo painel** — um arquivo de dados por ano
   (`dados/dados_2024.json`, `dados/dados_2025.json`), seletor de ano no cabeçalho, rótulo "2025
   (preliminar)" e, na ficha da unidade, a variação entre os anos. Hoje o template fixa "2024" em títulos,
   KPI "Partos em 2024", rodapé e PDF — parametrizar por ano.
4. `python scripts/03_montar_painel.py` → `index.html`; verificar no navegador; atualizar `METODOLOGIA.md`
   (seção 6 com os números de 2025, universo, datas de extração, caráter preliminar) e `README.md`.
5. Commit na `main` e push (Pages publica em 1–2 min). Nunca publicar com auditoria em falha.

---

## 4. Referência rápida de códigos e variáveis

- **SIH-RD**: `PROC_REA` (procedimento realizado), `CNES`, `ANO_CMPT`/`MES_CMPT` (competência), `DT_INTER`,
  `DT_SAIDA`, `SEXO` (3 = feminino), `IDADE` + `COD_IDADE` (4 = anos), `N_AIH`, `COBRANCA` (motivo de saída),
  `MUNIC_MOV`. Universo obstétrico: mulheres de 10 a 59 anos.
- **SINASC (DNV)**: `CODESTAB` (CNES), `PARTO` (1 vaginal, 2 cesáreo, 9 ignorado), `TPROBSON` (grupo de
  Robson), `APGAR5`, `PESO` (g), `IDANOMAL` (1 sim, 2 não, 9 ignorado), `TPNASCASSI` (1 médico,
  2 enfermeira/obstetriz, 3 parteira, 4 outros, 9 ignorado), `SEMAGESTAC`, `CODMUNNASC`.
- **Leitura de `.dbc`** em Python: `pyreaddbc` (`read_dbc`) ou conversão com `dbc2dbf`; a esteira local
  já tem a forma de ler — reutilizar.

---

## 5. Regras de negócio que NÃO mudam (checklist)

- **8 indicadores classificatórios**: Unidade Neonatal completa · Cesariana (Robson ≥2 grupos) · Parto
  vaginal assistido por enfermeira · Uso de AMIU · Asfixia Neonatal · Oferta de LARC · Atendimento de
  violência sexual · SMCON Neonatal e/ou Obstétrico (os dois módulos contam **uma vez**).
- **Estágios de desempenho** pelo nº de indicadores adequados: **Avançando ≥5 de 8** · Quase lá = 4 ·
  No caminho = 2–3 · Início da jornada = 0–1. O campo oficial da planilha (≥5 dos 9 marcadores,
  "CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS") é preservado no campo `oficial` só para auditoria; o estágio
  Avançando fica no campo `avanc`.
- Limiares (institucionais): asfixia ≤ 0,6% · parto por enfermeira ≥ 50% · AMIU ≥ 50% · LARC ≥ 3
  inserções de DIU/implante no ano · violência sexual ≥ 2 atendimentos · Robson por grupo G1 ≤10% ·
  G2 ≤35% · G3 ≤3% · G4 ≤15% (ref. Manual de Robson, OMS/OPAS 2017; G2 pelo limite superior da faixa
  20–35%). Estabelecimento adequado em Robson = ≥2 grupos dentro da meta; grupo sem NV = não adequado.
- Unidade neonatal completa: adequada quando "SIM" **ou** "NÃO SE APLICA".
- Agregados: % de estabelecimentos adequados sempre com (x/n); **médias, nunca medianas** (AMIU e taxas de
  Robson no gráfico, excluídas unidades sem partos no grupo); **sem meta de taxa geral de cesariana**.
- Nomes padronizados em todas as telas: "Uso de AMIU", "Asfixia Neonatal", "Atendimento de violência
  sexual", "SMCON Neonatal e/ou Obstétrico", "cesariana" (não "cesárea"), "Avançando", "Estágios de desempenho".
- Tudo de 2025 rotulado **preliminar** (SINASC preliminar; SIH sujeito a acréscimos).

---

## 6. Perguntas em aberto (confirmar antes de fechar 2025)

1. Códigos SIGTAP de **DIU**, **implante subdérmico** e **atendimento a vítima de violência sexual** usados
   na planilha de 2024, e a fonte (SIH-RD ou SIH-SP? BPA?).
2. Regra exata de **UNIDADE NEONATAL COMPLETA** (leitos existentes × habilitações; competência do CNES) e de
   **HGPAR**.
3. O `0409060313` entrou ou não no total de partos de 2024.
4. Filtros das AIH na contagem de partos (aprovadas/rejeitadas; `IDENT`; competência × data de internação).
5. **SMCON 2025**: quem envia a lista e em que data de corte.
6. Painel: substituir 2024 por 2025 ou mostrar os dois (recomendação: os dois).

---

## 7. Entregáveis

- `relatorios/reproducao_2024.md` — tabela de reprodução coluna a coluna (critério: 543/543).
- `PLANILHA_2025.xlsx` no formato da seção 2 (+ a mesma coisa para 2024 recalculada, para rastreabilidade).
- `dados/dados_2025.json`, auditoria **0 falhas**, painel com os dois anos, METODOLOGIA.md e README atualizados.
- Commit e push na `main` do `Indicadores_partos_Brasil2024`.

*Gerado em 04/11/2026 a partir da sessão na nuvem (https://claude.ai/code/session_01PdPgzdegrLD98pzmcCLmQY).*
