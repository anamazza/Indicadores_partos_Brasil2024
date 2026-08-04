# Metodologia dos Indicadores

**Painel de Indicadores Obstétricos e Neonatais — Brasil 2024**
Estabelecimentos com mais de 1.000 partos · 543 unidades · 1.253.881 partos

Fonte dos dados: SINASC / CNES / SIH-SUS · Extração 01/07/2026
Documento de 15/07/2026, **revisado em 04/08/2026** após a reunião de gestão de 03/08/2026.

> **Base de dados única.** Todo número do painel deriva da planilha institucional `ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES` (543 linhas × 57 colunas). O painel apenas **agrega** a classificação já existente na planilha; o script `scripts/04_auditoria.py` reconfere os números exibidos diretamente contra ela (resultado atual: **36 verificações OK, 0 falhas**).

**Oficial vs. institucional.** Os indicadores são reconhecidos e alinhados à Rede de Atenção Materna e Infantil (Portaria GM/MS 5.350/2024) e ao SMCON (IFF/Fiocruz), mas os **limiares** que definem cada indicador como "adequado" são **institucionais** — não constam nos atos oficiais consultados, que remetem a um ato de indicadores ainda não publicado. Desde a revisão de 04/08/2026, o painel **não exibe meta de taxa geral de cesariana**; a leitura de cesárea é feita pelos grupos de Robson (seção 2.3).

---

## 1. Como os agregados são calculados

Cada estabelecimento traz seus dados brutos e sua classificação de adequação. O painel agrega por território em três níveis — UF, macrorregião de saúde e região de saúde.

- **Indicadores de adequação ("% … adequada")**: (nº de estabelecimentos adequados ÷ nº de estabelecimentos) × 100, sempre exibido com o número absoluto **(adequados/total)** e 1 casa decimal.
- **Médias (o painel não usa mediana)**: % AMIU e as taxas de cesariana nos grupos de Robson (gráfico) são a **média dos percentuais dos estabelecimentos** da seleção; no gráfico de Robson, excluem-se os estabelecimentos sem partos no grupo.
- **Mapa**: todos os indicadores mapeados são percentuais de adequação ("mais é melhor"); cores em quintis calculados sobre os territórios visíveis; escala sequencial de verdes, segura para daltonismo; faixas repetidas são colapsadas na legenda; cinza = território sem estabelecimento elegível.
- **Cobertura parcial**: todo agregado reflete apenas as unidades com mais de 1.000 partos — não a totalidade dos partos do território.

**Sistemas de informação-fonte.** O SINASC (Sistema de Informações sobre Nascidos Vivos) fornece os nascidos vivos e a riqueza clínica da Declaração de Nascido Vivo — via de nascimento, quem assistiu o parto, Apgar, peso e as variáveis da classificação de Robson; o CNES identifica os estabelecimentos e suas habilitações (unidade neonatal, alto risco); e o SIH/SUS fornece os procedimentos financiados pelo SUS (AMIU, inserção de DIU/implante, entre outros). O SMCON (IFF/Fiocruz) é um sistema de monitoramento voluntário, presente em parte das unidades, e figura aqui como indicador de adesão — não como fonte dos demais.

## 2. Os indicadores — o que são, como se calculam e fontes

### 2.1 Visão geral

**% com Selo de conformidade** — Síntese da qualidade global: reconhece os estabelecimentos que alcançam pelo menos 5 dos 9 indicadores classificatórios adequados (seção 3).
*Cálculo:* estab. com selo ÷ estab. × 100 · *Adequação:* campo oficial da planilha (≥5 de 9) · *Fonte:* planilha institucional (SINASC/CNES/SIH).

**Estabelecimentos e Partos** — Números de contexto: contagem de unidades com mais de 1.000 partos e soma dos nascidos vivos de 2024.
*Fonte:* partos: SINASC (via DNV); estabelecimentos: CNES.

### 2.2 Estrutura

**% Unidade Neonatal completa** — Capacidade instalada para o cuidado ao recém-nascido de risco: presença de UTIN, UCINCo e UCINCa. Maternidades de risco habitual, que não precisam do conjunto completo, recebem "não se aplica".
*Cálculo:* % de estabelecimentos com unidade neonatal completa = SIM · *Adequação (selo):* SIM **ou** "não se aplica" · *Fonte:* CNES (habilitações); Portaria SAES/MS 2.902/2025; Portaria GM/MS 5.350/2024, Art. 47.

**Nota — HGPAR não é indicador de qualidade.** A sigla designa a habilitação "Hospital de Gestação e Puerpério de Alto Risco" (CNES/SAIPS). É classificação estrutural — não figura entre os indicadores mapeáveis; o dado permanece como característica do estabelecimento na exportação. *Fonte:* Portaria GM/MS 5.350/2024; Nota Técnica Conjunta 220.

### 2.3 Cesárea — grupos de Robson

A Classificação de Robson (OMS, 2017) divide as gestantes em 10 grupos mutuamente exclusivos a partir de características obstétricas, permitindo comparar taxas de cesárea de forma padronizada. O painel acompanha os quatro grupos de menor risco:

| Grupo | Perfil | Meta por grupo (OMS) |
|---|---|---|
| G1 | Nulípara, feto único cefálico, ≥37 sem, trabalho espontâneo | ≤10% |
| G2 | Nulípara, induzida ou cesárea antes do trabalho | ≤35% |
| G3 | Multípara sem cesárea anterior, espontâneo | ≤3% |
| G4 | Multípara, induzida ou cesárea antes do trabalho | ≤15% |

**Cada grupo de Robson tem a sua própria meta**, e a adequação do estabelecimento é avaliada grupo a grupo contra essas metas na base institucional.

**% Cesariana adequada (≥2 grupos)** — indicador-síntese da via de nascimento: estabelecimento adequado quando **pelo menos 2 dos 4 grupos** estão dentro da meta do grupo.
*Cálculo:* estab. com ≥2 grupos adequados ÷ estab. × 100 · *Adequação por grupo:* metas por grupo aplicadas na planilha institucional (tabela acima) · *Fonte:* SINASC (DNV: paridade, idade gestacional, apresentação, via de nascimento); WHO — Robson Classification Manual (2017).

**% Cesariana Adeq. Robson G1 a G4** — % de estabelecimentos adequados em cada grupo, individualmente.

**Gráfico "Cesariana nos grupos de Robson"** — **média** do % de cesariana dos estabelecimentos da seleção em cada grupo, excluídos os sem partos no grupo, comparada à meta do grupo (barra verde = média dentro da meta; vermelha = acima).

O painel **não exibe** taxa geral de cesariana nem meta de 35%; a taxa por estabelecimento permanece disponível nas exportações. *Referência de contexto:* OMS (2015) considera 10–15% a faixa populacional ideal.

### 2.4 Boas práticas

**% Parto vaginal assistido por enfermeira** — Proporção adequada de partos vaginais assistidos por enfermeiras obstétricas/obstetrizes; o cuidado de baixa intervenção associa-se a menos cesáreas e melhores desfechos.
*Cálculo:* % de estabelecimentos adequados (adequados/total) · *Adequação:* institucional (planilha) · *Fonte:* SINASC (DNV).

**% AMIU** — A Aspiração Manual Intrauterina é a técnica recomendada pela OMS para o esvaziamento uterino no abortamento, por ser mais segura e menos traumática que a curetagem.
*Cálculo:* **média** do % de AMIU entre os estabelecimentos · *Adequação (selo):* institucional · *Fonte:* SIH/SUS (procedimentos); OMS/FEBRASGO.

**% Asfixia adequada** — A taxa de asfixia da unidade é a proporção de recém-nascidos com Apgar <7 no 5º minuto entre os nascidos com ≥2.500g e sem malformação — marcador sensível da qualidade da assistência ao parto. O indicador do painel é o **percentual de estabelecimentos adequados** (taxa ≤0,6%).
*Cálculo:* estab. com asfixia adequada ÷ estab. × 100 (adequados/total) · *Adequação:* institucional (taxa ≤0,6%) · *Fonte:* SINASC (DNV: Apgar e peso). A taxa de cada unidade permanece visível na lista de estabelecimentos (tooltip) e nas exportações.

### 2.5 Contracepção

**% Contracepção adequada** — Oferta de contracepção reversível de longa ação (DIU e implante subdérmico) no pós-parto e pós-abortamento imediato.
*Cálculo:* % de estabelecimentos com classificação de contracepção adequada (adequados/total) · *Adequação:* institucional (DIU + implante inseridos no ano, conforme planilha) · *Fonte:* SIH/SUS (procedimentos de inserção); Nota Técnica de Ampliação do DIU (MS/IFF-Fiocruz).

*(Revisão de 04/08/2026: o indicador de volume de LARC — inserções por 1.000 partos — foi retirado do painel para evitar confusão de interpretação; a leitura é pela classificação de adequação.)*

### 2.6 Violência sexual

**% Atendimento de violência sexual** — Proporção de estabelecimentos que atendem vítimas de violência sexual; a maternidade é porta de entrada para acolhimento, profilaxias, contracepção de emergência e notificação compulsória. O painel também exibe o número de **atendimentos**.
*Cálculo:* % de estabelecimentos com classificação = SIM (adequados/total) · *Adequação:* institucional (≥2 atendimentos registrados no ano) · *Fonte:* registro SUS; Convenção de Belém do Pará (1994).

### 2.7 SMCON

**% SMCON Neo · % SMCON Obstétrico · % SMCON Neo e/ou Obst** — O Sistema de Monitoramento do Cuidado Obstétrico e Neonatal (IFF/Fiocruz, Estratégia Qualineo) é uma plataforma de coleta e análise de dados clínicos. Os indicadores mostram a adesão ao módulo neonatal, ao obstétrico, ou a pelo menos um deles.
*Cálculo:* % de estabelecimentos com o(s) módulo(s) alimentado(s) (adequados/total) · *Fonte:* IFF/Fiocruz — Instrutivo do SMCON.

## 3. O selo de conformidade

O selo reconhece estabelecimentos com **5 ou mais dos 9 indicadores classificatórios** adequados. É o campo oficial da planilha e corresponde exatamente a "número de indicadores adequados ≥ 5".

Os 9 indicadores classificatórios: 1. Asfixia · 2. Enfermagem obstétrica · 3. AMIU · 4. Robson ≥2 grupos · 5. Contracepção · 6. Violência sexual · 7. SMCON neonatal · 8. SMCON obstétrico · 9. Unidade neonatal completa.

Duas regras importantes:
- "Unidade neonatal completa" conta como adequada quando é **SIM ou "não se aplica"** (não penaliza maternidades de risco habitual).
- Robson ≥2 grupos é **um dos 9 indicadores contados** — não é uma exigência à parte. Há estabelecimentos com selo sem Robson ≥2 grupos.

| Estágio | Critério | Brasil 2024 |
|---|---|---|
| **Com selo** | 5 ou mais indicadores adequados | 122 (22,5%) |
| **Quase lá** | 4 indicadores adequados | 129 (23,8%) |
| **No caminho** | 2 a 3 indicadores adequados | 229 (42,2%) |
| **Início da jornada** | 0 a 1 indicador adequado | 63 (11,6%) |

## 4. Resultados nacionais (2024) — referência

Valores agregados dos 543 estabelecimentos (1.253.881 partos), para conferência.

| Indicador | Nacional | Indicador | Nacional |
|---|---|---|---|
| % Cesariana adequada (≥2 grupos) | 56,7% (308/543) | % Contracepção adequada | 35,7% (194/543) |
| % Adeq. Robson G1 | 41,8% (227/543) | % Atendimento de violência sexual | 41,4% (225/543) |
| % Adeq. Robson G2 | 51,0% (277/543) | % SMCON Neo | 19,7% (107/543) |
| % Adeq. Robson G3 | 38,9% (211/543) | % SMCON Obstétrico | 9,4% (51/543) |
| % Adeq. Robson G4 | 50,1% (272/543) | % SMCON Neo e/ou Obst | 22,1% (120/543) |
| % Parto vaginal assistido por enfermeira | 28,5% (155/543) | % Unidade Neonatal completa | 43,6% (237/543) |
| % Asfixia adequada | 71,5% (388/543) | Neonatal adequada no selo (SIM ou N/A) | 60,8% (330/543) |
| % AMIU (média) | 12,6% | % com Selo | 22,5% (122/543) |

Médias do % de cesariana nos grupos (estab. com partos no grupo): G1 36,1% · G2 66,3% · G3 18,5% · G4 49,1%.

## 5. Fontes e referências

- BRASIL. Ministério da Saúde. **Portaria GM/MS nº 5.350, de 12/09/2024** — institui a Rede de Atenção Materna e Infantil no SUS e os requisitos de unidade neonatal.
- BRASIL. Ministério da Saúde. **Portaria GM/MS nº 5.349, de 12/09/2024** — financiamento da Rede.
- BRASIL. Ministério da Saúde. **Nota Técnica Conjunta nº 220** (SEI 0044549197).
- BRASIL. Ministério da Saúde/SAES. **Portaria SAES/MS nº 2.902, de 26/06/2025** — códigos de leitos e habilitações neonatais no CNES (UTIN II/III, UCINCo, UCINCa).
- IFF/FIOCRUZ. **Instrutivo do SMCON** — módulos Parto/Nascimento/Abortamento e Cuidado Neonatal (Estratégia Qualineo).
- MINISTÉRIO DA SAÚDE/IFF-FIOCRUZ. **Nota Técnica de Ampliação do acesso ao DIU**.
- WORLD HEALTH ORGANIZATION. **Robson Classification: Implementation Manual.** Genebra: OMS, 2017.
- WORLD HEALTH ORGANIZATION. **WHO Statement on Caesarean Section Rates.** Genebra: OMS, 2015.
- ANS. **Fichas Técnicas dos Indicadores — QualiSS.**
- Dados-fonte do painel: **SINASC, CNES e SIH/SUS** (extração de 01/07/2026).

## 6. Oficial × institucional e auditoria

| Item | Situação |
|---|---|
| Dados-fonte do painel | OFICIAL — SINASC (nascidos vivos/DNV), SIH/SUS (procedimentos), CNES (cadastro) |
| Definição de "unidade neonatal completa" | OFICIAL — habilitações CNES (Portaria 2.902/2025) |
| Definições das variáveis clínicas (via de nascimento, Apgar etc.) | DNV/SINASC; alinhadas ao Instrutivo SMCON (IFF/Fiocruz) |
| Classificação de Robson e referências por grupo | Método OMS (2017); faixas de adequação por grupo: INSTITUCIONAL (planilha) |
| Limiares de adequação (asfixia, enfermagem, AMIU, contracepção, violência) | INSTITUCIONAL — não constam em ato oficial publicado |
| Selo (≥5 de 9 indicadores) e estágios | INSTITUCIONAL / operacional |
| Meta de taxa geral de cesariana | NÃO EXIBIDA no painel (revisão de 04/08/2026); leitura por grupos de Robson |

**Auditoria:** o script `scripts/04_auditoria.py` recalcula os números do painel diretamente da planilha; resultado atual: **36 verificações OK, 0 falhas**.
