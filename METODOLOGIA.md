# Nota Metodológica

**Coordenação de Ações Nacionais e de Cooperação em Saúde da Mulher, da Criança e do Adolescente**
Instituto Nacional de Saúde da Mulher, da Criança e do Adolescente Fernando Figueira (IFF/Fiocruz) · SUS

**Painel de Indicadores Obstétricos e Neonatais — Brasil, 2024**
Estabelecimentos com mais de 1.000 partos · 543 unidades · 1.253.881 partos
Fonte dos dados: SINASC, CNES e SIH-SUS · Extração de 01/07/2026 · Documento revisado em 04/08/2026

---

## 1. Objeto e abrangência

Esta nota descreve a construção dos indicadores do Painel de Indicadores Obstétricos e Neonatais. O painel reúne os **543 estabelecimentos de saúde com mais de 1.000 partos em 2024**, que responderam por **1.253.881 nascimentos**. Todos os agregados referem-se exclusivamente a essas unidades e não à totalidade dos partos do território; cada agregado exibe o número de estabelecimentos considerados.

A **base de dados é única**: a planilha institucional derivada de SINASC, CNES e SIH-SUS (extração de 01/07/2026). O painel apenas **agrega** a classificação de adequação já existente na planilha. O script de auditoria (`scripts/04_auditoria.py`) recalcula os números exibidos diretamente contra a planilha; resultado atual: **36 verificações, 0 falhas**.

Os dados são públicos e agregados por estabelecimento; não há informação individual de pacientes.

## 2. Sistemas de informação de origem

- **SINASC** (Sistema de Informações sobre Nascidos Vivos) — nascidos vivos e variáveis da Declaração de Nascido Vivo: via de nascimento, profissional que assistiu o parto, Apgar, peso e as variáveis da classificação de Robson.
- **CNES** (Cadastro Nacional de Estabelecimentos de Saúde) — identificação dos estabelecimentos e habilitações (unidade neonatal, alto risco).
- **SIH/SUS** (Sistema de Informações Hospitalares) — procedimentos financiados pelo SUS (AMIU, inserção de DIU e implante, entre outros).
- **SMCON** (Sistema de Monitoramento do Cuidado Obstétrico e Neonatal, IFF/Fiocruz) — figura como indicador de adesão, não como fonte dos demais.

## 3. Método de agregação

- **Percentuais de adequação** — (nº de estabelecimentos adequados ÷ nº de estabelecimentos) × 100, apresentados com o número absoluto (adequados/total) e uma casa decimal.
- **Médias** — o percentual de AMIU e as taxas de cesariana por grupo de Robson (gráfico) correspondem à média dos estabelecimentos da seleção; no gráfico de Robson, excluem-se as unidades sem partos no grupo. O painel não utiliza mediana.
- **Mapa coroplético** — todos os indicadores mapeados são percentuais de adequação; as classes são quintis dos territórios visíveis, em escala sequencial de verdes, segura para daltonismo. Territórios sem estabelecimento elegível aparecem em cinza.
- **Matriz semáforo** — cada célula é o percentual de estabelecimentos adequados do território no indicador, em quatro faixas (≥75%, 50–74%, 25–49%, <25%). Territórios com menos de 5 unidades são apresentados em tom atenuado (percentual instável); o `n` acompanha cada linha.

## 4. Indicadores

### 4.1 Estrutura

**Unidade Neonatal completa.** Disponibilidade da linha completa de cuidado ao recém-nascido de risco (UTIN, UCINCo e UCINCa), conforme habilitações do CNES. Adequado quando a resposta é **"sim"** ou **"não se aplica"** — esta última correspondente às maternidades de risco habitual.
*Fonte:* CNES; Portaria GM/MS nº 5.350/2024; Portaria SAES/MS nº 2.902/2025.

### 4.2 Cesárea — grupos de Robson

A Classificação de Robson (OMS, 2017) distribui as gestantes em grupos mutuamente exclusivos segundo características obstétricas, permitindo comparar taxas de cesariana de forma padronizada. O painel acompanha os quatro grupos de menor risco e avalia cada um contra a sua **meta institucional**:

| Grupo | Perfil | Meta institucional |
|---|---|---|
| G1 | Nulípara, feto único cefálico, ≥37 semanas, trabalho de parto espontâneo | ≤ 10% |
| G2 | Nulípara, com indução ou cesárea anterior ao trabalho de parto | ≤ 35% |
| G3 | Multípara sem cesárea anterior, trabalho de parto espontâneo | ≤ 3% |
| G4 | Multípara, com indução ou cesárea anterior ao trabalho de parto | ≤ 15% |

As metas por grupo são **institucionais**, adotadas pela Coordenação com base nas referências de interpretação do *Robson Classification: Implementation Manual* (OMS, 2017; versão OPAS). Para o **G2**, cuja referência é uma faixa (20–35%), adotou-se nesta primeira versão o limite superior (**≤ 35%**), para simplificar a leitura — parâmetro sujeito a revisão.

**% Cesariana adequada (≥2 grupos).** Indicador-síntese da via de nascimento: o estabelecimento é adequado quando pelo menos **2 dos 4 grupos** estão dentro da meta.
*Cálculo:* estab. com ≥2 grupos adequados ÷ estab. × 100. *Fonte:* SINASC.

**% Cesariana Adeq. Robson G1 a G4.** Percentual de estabelecimentos adequados em cada grupo, individualmente.

**Gráfico "Cesariana nos grupos de Robson".** Média do percentual de cesariana dos estabelecimentos da seleção em cada grupo (excluídos os sem partos no grupo). A meta de cada grupo consta do subtítulo do gráfico e do tooltip de cada barra. O painel não exibe taxa geral de cesariana.

### 4.3 Boas práticas

**Parto vaginal assistido por enfermeira.** Proporção de partos vaginais assistidos por enfermeira obstétrica ou obstetriz. Adequado ≥ 50%.
*Fonte:* SINASC.

**AMIU.** Aspiração Manual Intrauterina, técnica recomendada para o esvaziamento uterino no abortamento. Exibida como média do percentual entre os estabelecimentos.
*Fonte:* SIH/SUS.

**Asfixia.** Percentual de estabelecimentos adequados quanto à asfixia neonatal — taxa de recém-nascidos ≥ 2.500 g, sem anomalias, com Apgar < 7 no 5º minuto **≤ 0,6%**. A taxa de cada unidade permanece disponível na lista de estabelecimentos (ao passar o mouse) e nas exportações.
*Fonte:* SINASC.

### 4.4 Oferta de LARC

**Oferta de LARC.** Oferta de contracepção reversível de longa ação (DIU e implante subdérmico) no pós-parto e pós-abortamento. Percentual de estabelecimentos com oferta adequada, conforme a classificação da planilha.
*Fonte:* SIH/SUS.

### 4.5 Atendimento de violência sexual

**Atendimento de violência sexual.** Percentual de estabelecimentos que atendem vítimas de violência sexual (adequado ≥ 2 atendimentos registrados no ano). O painel também exibe o número de atendimentos.
*Fonte:* SIH/SUS; Lei nº 12.845/2013.

### 4.6 Monitoramento pelo SMCON

**SMCON Neonatal · SMCON Obstétrico · SMCON Neonatal e/ou Obstétrico.** Adesão do estabelecimento aos módulos Neonatal e Obstétrico do SMCON (IFF/Fiocruz, Estratégia Qualineo), de alimentação voluntária. Adequado quando a unidade alimenta o(s) módulo(s).
*Fonte:* IFF/Fiocruz — Instrutivo do SMCON.

## 5. Selo de conformidade

O selo reconhece os estabelecimentos com **5 ou mais dos 9 indicadores classificatórios** adequados. Corresponde ao campo classificatório da planilha (número de indicadores adequados ≥ 5).

Os 9 indicadores: Asfixia · Parto vaginal assistido por enfermeira · AMIU · Robson ≥2 grupos · Oferta de LARC · Atendimento de violência sexual · SMCON Neonatal · SMCON Obstétrico · Unidade Neonatal completa.

- "Unidade Neonatal completa" conta como adequada quando é **"sim" ou "não se aplica"**.
- "Robson ≥2 grupos" é **um dos 9 indicadores contados**, não uma exigência à parte.

| Estágio | Critério | Brasil 2024 |
|---|---|---|
| Com selo | 5 ou mais indicadores adequados | 122 (22,5%) |
| Quase lá | 4 indicadores adequados | 129 (23,8%) |
| No caminho | 2 a 3 indicadores adequados | 229 (42,2%) |
| Início da jornada | 0 a 1 indicador adequado | 63 (11,6%) |

O selo afere conformidade com itens de qualificação — estrutura, processo e registro — e não constitui, por si, medida de qualidade assistencial. A taxa de cesariana não integra o selo.

## 6. Resultados nacionais de referência (2024)

Valores agregados dos 543 estabelecimentos, para conferência.

| Indicador | Nacional | Indicador | Nacional |
|---|---|---|---|
| % Cesariana adequada (≥2 grupos) | 56,7% (308/543) | % Oferta de LARC | 35,7% (194/543) |
| % Adeq. Robson G1 | 41,8% (227/543) | % Atendimento de violência sexual | 41,4% (225/543) |
| % Adeq. Robson G2 | 51,0% (277/543) | % SMCON Neonatal | 19,7% (107/543) |
| % Adeq. Robson G3 | 38,9% (211/543) | % SMCON Obstétrico | 9,4% (51/543) |
| % Adeq. Robson G4 | 50,1% (272/543) | % SMCON Neonatal e/ou Obstétrico | 22,1% (120/543) |
| % Parto vaginal assistido por enfermeira | 28,5% (155/543) | % Unidade Neonatal completa | 43,6% (237/543) |
| % Asfixia | 71,5% (388/543) | % com Selo | 22,5% (122/543) |

Média do percentual de cesariana nos grupos (estabelecimentos com partos no grupo): G1 36,1% · G2 66,3% · G3 18,5% · G4 49,1%.

## 7. Natureza dos parâmetros

| Item | Natureza |
|---|---|
| Dados-fonte (nascidos vivos, procedimentos, cadastro) | Oficial — SINASC, SIH/SUS, CNES |
| Definição de "unidade neonatal completa" | Oficial — habilitações CNES (Portaria SAES/MS 2.902/2025) |
| Variáveis clínicas (via de nascimento, Apgar etc.) | DNV/SINASC, alinhadas ao Instrutivo do SMCON |
| Método da classificação de Robson | Oficial — OMS, 2017 |
| Metas por grupo de Robson e demais limiares de adequação | Institucionais — adotados pela Coordenação |
| Taxa geral de cesariana | Não exibida no painel; leitura por grupos de Robson |

## 8. Referências

- BRASIL. Ministério da Saúde. **Portaria GM/MS nº 5.350, de 12 de setembro de 2024** — institui a Rede de Atenção Materna e Infantil no SUS.
- BRASIL. Ministério da Saúde. **Portaria GM/MS nº 5.349, de 12 de setembro de 2024** — financiamento da Rede.
- BRASIL. Ministério da Saúde/SAES. **Portaria SAES/MS nº 2.902, de 26 de junho de 2025** — leitos e habilitações neonatais no CNES.
- BRASIL. Ministério da Saúde. **Nota Técnica Conjunta nº 220**.
- IFF/FIOCRUZ. **Instrutivo do SMCON** — Estratégia Qualineo.
- MINISTÉRIO DA SAÚDE / IFF-FIOCRUZ. **Nota Técnica de ampliação do acesso ao DIU**.
- ORGANIZAÇÃO MUNDIAL DA SAÚDE. **Robson Classification: Implementation Manual.** Genebra: OMS, 2017 (versão OPAS: *La clasificación de Robson: Manual de aplicación*).
- BRASIL. **Lei nº 12.845, de 1º de agosto de 2013** — atendimento obrigatório a vítimas de violência sexual.
- Dados-fonte do painel: **SINASC, CNES e SIH/SUS** (extração de 01/07/2026).

## 9. Auditoria

O script `scripts/04_auditoria.py` recalcula os números do painel diretamente da planilha institucional. **Resultado atual: 36 verificações, 0 falhas.**
