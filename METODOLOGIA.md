# Nota metodológica · fichas de qualificação dos indicadores

**Coordenação de Ações Nacionais e de Cooperação em Saúde da Mulher, da Criança e do Adolescente**
Instituto Nacional de Saúde da Mulher, da Criança e do Adolescente Fernando Figueira (IFF/Fiocruz) · SUS

**Indicadores da Atenção Obstétrica e Neonatal em Estabelecimentos com mais de 1.000 partos no Brasil — 2024**
543 unidades · 1.253.881 partos
Fonte dos dados: SINASC, CNES, SIH-SUS e SMCON · Extração de 01/07/2026 · Documento revisado em 28/08/2026

---

## 1. Objeto e abrangência

A seleção dos indicadores que compõem o painel considerou, além de sua relevância para o monitoramento da qualidade e da organização da atenção materna e neonatal, a disponibilidade e a confiabilidade das informações nos sistemas de informação em saúde existentes. Foram priorizados indicadores passíveis de obtenção a partir de bases de dados de acesso regular, com variáveis padronizadas e cobertura adequada, bem como aqueles cujo cálculo pudesse ser realizado de forma objetiva, reprodutível e com menor complexidade operacional. Também foram considerados a possibilidade de atualização periódica, a comparabilidade dos resultados entre estabelecimentos e períodos e a viabilidade de interpretação pelos diferentes públicos envolvidos no monitoramento. Dessa forma, a composição do painel buscou conciliar a relevância dos indicadores com sua factibilidade de mensuração, permitindo um acompanhamento sistemático e sustentável dos aspectos selecionados.

O painel reúne os **543 estabelecimentos de saúde com mais de 1.000 partos em 2024**, que responderam por **1.253.881 nascimentos**. Todos os agregados referem-se exclusivamente a essas unidades e não à totalidade dos partos do território; cada agregado exibe o número de estabelecimentos considerados.

A **base de dados é única**: a planilha institucional derivada de SINASC, CNES, SIH-SUS e SMCON (extração de 01/07/2026). O painel apenas **agrega** a classificação de adequação já existente na planilha; a única derivação é a consolidação dos módulos do SMCON em um indicador na classificação por estágios (seção 5). Os parâmetros de adequação são institucionais e não constam em ato oficial publicado. O script de auditoria (`scripts/04_auditoria.py`) recalcula os números exibidos diretamente contra a planilha; resultado atual: **37 verificações, 0 falhas** (execução de 28/08/2026).

Os dados são públicos e agregados por estabelecimento; não há informação individual de pacientes.

## 2. Sistemas de informação de origem

- **SINASC** (Sistema de Informações sobre Nascidos Vivos) — nascidos vivos e variáveis da Declaração de Nascido Vivo: via de nascimento, profissional que assistiu o parto, Apgar, peso e as variáveis da classificação de Robson.
- **CNES** (Cadastro Nacional de Estabelecimentos de Saúde) — identificação dos estabelecimentos e habilitações (unidade neonatal, alto risco).
- **SIH/SUS** (Sistema de Informações Hospitalares) — procedimentos financiados pelo SUS (AMIU, inserção de DIU e implante, entre outros).
- **SMCON** (Sistema de Monitoramento do Cuidado Obstétrico e Neonatal, IFF/Fiocruz) — figura como indicador de adesão, não como fonte dos demais.

## 3. Método de agregação

- **Percentuais de adequação** — (nº de estabelecimentos adequados ÷ nº de estabelecimentos) × 100, apresentados com o número absoluto (adequados/total) e uma casa decimal.
- **Médias** — o percentual de uso de AMIU e as taxas de cesariana por grupo de Robson (gráfico) correspondem à média dos estabelecimentos da seleção; no gráfico de Robson, excluem-se as unidades sem partos no grupo. O painel não utiliza mediana.
- **Mapa coroplético** — todos os indicadores mapeados são percentuais de adequação; as classes são quintis dos territórios visíveis, em escala sequencial de verdes, segura para daltonismo. Territórios sem estabelecimento elegível aparecem em cinza.
- **Matriz semáforo** — cada célula é o percentual de estabelecimentos adequados do território no indicador, em quatro faixas (≥75%, 50–74%, 25–49%, <25%). Territórios com menos de 5 unidades são apresentados em tom atenuado (percentual instável); o `n` acompanha cada linha.
- **Mapa de unidades** — cada estabelecimento é um ponto na cor do seu estágio de desempenho (Avançando, Quase lá, No caminho, Início da jornada); o seletor "Colorir por" recolore os pontos por qualquer um dos 8 indicadores classificatórios, em verde (adequado) × roxo (não adequado), par seguro para daltonismo. O tamanho do ponto é proporcional à raiz do total de partos; agrupamentos exibem a composição de cores das unidades agrupadas, e a legenda permite ocultar categorias. A ficha de cada unidade traz o estágio de desempenho com o número de indicadores adequados (n/8), total de partos, natureza jurídica e gestão — sem taxa de cesariana, em coerência com a leitura por grupos de Robson. Coordenadas geocodificadas por CNES; duas unidades sem geolocalização exata utilizam o centro do município.

## 4. Fichas dos indicadores

### 4.1 Unidade Neonatal completa

**Conceituação:** disponibilidade das três tipologias de leitos para o cuidado neonatal progressivo — UTIN, UCINCo e UCINCa — conforme habilitações registradas no CNES (Portaria GM/MS nº 930/2012).
**Parâmetro:** "sim" quando a unidade neonatal possui os três tipos de leitos; "não" quando falta pelo menos um deles; "não se aplica" quando a maternidade não possui unidade neonatal. Conta como adequada quando a resposta é **"sim" ou "não se aplica"** — condição das maternidades de risco habitual, que não constituem porta de entrada do recém-nascido grave; nesses casos, a retaguarda depende da regulação e do transporte neonatal.
*Fonte:* CNES (leitos existentes de UTIN, UCINCo e UCINCa). Referências: Portaria GM/MS nº 930/2012; Portaria SAES/MS nº 2.902/2025.

### 4.2 Cesariana — grupos de Robson

A Classificação de Robson (OMS, 2017) distribui as gestantes em grupos mutuamente exclusivos segundo características obstétricas, permitindo comparar taxas de cesariana de forma padronizada. O painel acompanha os quatro grupos de menor risco e avalia cada um contra a sua **meta institucional**:

| Grupo | Perfil | Meta institucional |
|---|---|---|
| G1 | Nulípara, feto único cefálico, ≥37 semanas, trabalho de parto espontâneo | ≤ 10% |
| G2 | Nulípara, com indução ou cesariana anterior ao trabalho de parto | ≤ 35% |
| G3 | Multípara sem cesariana anterior, trabalho de parto espontâneo | ≤ 3% |
| G4 | Multípara, com indução ou cesariana anterior ao trabalho de parto | ≤ 15% |

As metas por grupo são **institucionais**, adotadas pela Coordenação com base nas referências de interpretação do *Robson Classification: Implementation Manual* (OMS, 2017; versão OPAS). Para o **G2**, cuja referência é uma faixa (20–35%), adotou-se nesta primeira versão o limite superior (**≤ 35%**), para simplificar a leitura — parâmetro sujeito a revisão.

**Cesariana — Robson ≥2 grupos.** Indicador-síntese da via de nascimento.
**Conceituação:** ter ao menos dois dos quatro grupos de Robson de menor risco (G1 a G4) com taxa de cesariana dentro da meta do grupo.
**Método de cálculo:** número de grupos de Robson (G1 a G4) com taxa de cesariana dentro da meta estabelecida para cada grupo; grupos sem nascidos vivos são computados como não adequados. Agregado: estab. com ≥2 grupos adequados ÷ estab. × 100.
**Parâmetro:** "sim" (pelo menos 2 grupos dentro da meta) e "não" (menos de 2 grupos dentro da meta). "Robson ≥2 grupos" é **um dos 8 indicadores classificatórios** do desempenho das unidades. O painel não exibe meta de taxa geral de cesariana.
*Fonte:* SINASC. Método: OMS — *Robson Classification Manual* (2017).

**% Cesariana Adeq. Robson G1 a G4.** Percentual de estabelecimentos adequados em cada grupo, individualmente.

**Gráfico "Cesariana nos grupos de Robson".** Média do percentual de cesariana dos estabelecimentos da seleção em cada grupo (excluídos os sem partos no grupo). A meta de cada grupo consta do subtítulo do gráfico e do tooltip de cada barra.

### 4.3 Parto vaginal assistido por enfermeira

**Conceituação:** proporção de partos vaginais assistidos por enfermeira obstétrica ou obstetriz, conforme o campo "profissional que assistiu o parto" da Declaração de Nascido Vivo. Expressa a adoção do modelo assistencial recomendado para a gestação de risco habitual (OMS, 2018; Diretrizes Nacionais de Assistência ao Parto Normal, Ministério da Saúde).
**Método de cálculo:** partos vaginais assistidos por enfermeira obstétrica ou obstetriz ÷ total de partos vaginais × 100.
**Parâmetro:** adequado quando igual ou superior a 50%, conforme meta estabelecida pela equipe responsável pela elaboração do painel.
**Limitações:** o campo apresenta subregistro conhecido, com possibilidade de preenchimento inadequado na DNV — o valor observado pode ser inferior à prática efetivamente realizada. Valores nulos em unidades que dispõem de Centro de Parto Normal indicam falha de preenchimento, e não ausência da prática.
*Fonte:* SINASC (DNV: campo "profissional que assistiu o parto"). Referências: OMS (2018); Diretrizes Nacionais de Assistência ao Parto Normal (Ministério da Saúde).

### 4.4 Uso de AMIU — aspiração manual intrauterina

**Conceituação:** proporção dos esvaziamentos uterinos realizados pela técnica de aspiração manual intrauterina, recomendada pela norma técnica de Atenção Humanizada ao Abortamento (Ministério da Saúde) em substituição à curetagem.
**Método de cálculo:** procedimentos de AMIU ÷ total de esvaziamentos uterinos (AMIU + curetagem) × 100. No painel, o agregado é a média do percentual entre os estabelecimentos da seleção.
**Parâmetro:** adequado quando igual ou superior a 50%, conforme meta estabelecida pela equipe responsável pela elaboração do painel.
**Limitações:** por se tratar de dado de produção faturada, o valor nulo não distingue a unidade que não realiza o procedimento daquela que o registra sob outro código ou que referencia os casos a outro serviço.
*Fonte:* SIH-SUS (procedimentos de AMIU e curetagem). Referência: norma técnica de Atenção Humanizada ao Abortamento (Ministério da Saúde).

### 4.5 Asfixia Neonatal

**Conceituação:** a taxa de asfixia da unidade é a proporção de nascidos vivos com peso igual ou superior a 2.500g, sem anomalias congênitas, com índice de Apgar inferior a 7 no 5º minuto de vida. O Apgar baixo é utilizado como marcador de possível asfixia ao nascer, desfecho sensível à qualidade da vigilância do trabalho de parto e da reanimação neonatal.
**Método de cálculo do indicador:** % de estabelecimentos com asfixia adequada = estabelecimentos com taxa ≤0,6% ÷ estabelecimentos da seleção × 100, exibido com o número absoluto (adequados/total). A taxa de cada unidade permanece disponível na lista de estabelecimentos (ao passar o mouse) e nas exportações.
**Parâmetro:** unidade adequada quando a taxa é igual ou inferior a 0,6% — média do Brasil em 2024, adotada como referência.
**Limitações:** em unidades com pequeno número de casos, a taxa apresenta oscilação aleatória importante. Taxa de 0,0% em unidade de grande volume sugere falha de registro do Apgar na DNV e deve ser objeto de verificação, não de comparação.
*Fonte:* SINASC (DNV: Apgar no 5º minuto, peso ao nascer e anomalias congênitas).

### 4.6 Oferta de LARC — DIU e implante

**Conceituação:** oferta de contraceptivos reversíveis de longa duração (DIU e implante subdérmico) no pós-parto e pós-abortamento, registrada no SIH-SUS, como marcador de planejamento reprodutivo na unidade.
**Método de cálculo:** número de registros de procedimentos de inserção de DIU ou implante nas AIH no ano.
**Parâmetro:** pelo menos 3 registros desses procedimentos no ano, conforme meta estabelecida pela equipe responsável pela elaboração do painel.
**Limitações:** o parâmetro identifica a existência de serviço ativo (insumo, profissional habilitado e fluxo), não a suficiência da oferta frente ao volume de partos. A inserção pós-placentária nem sempre é faturada, o que pode subestimar o dado.
*Fonte:* SIH-SUS (procedimentos de inserção de DIU e implante subdérmico). Referência: Nota Técnica de ampliação do acesso ao DIU (Ministério da Saúde / IFF-Fiocruz).

### 4.7 Atendimento de violência sexual

**Conceituação:** número de atendimentos a vítimas de violência sexual registrados pelo estabelecimento no ano.
**Método de cálculo:** contagem anual de atendimentos registrados.
**Parâmetro:** pelo menos dois atendimentos registrados no ano.
**Limitações:** o atendimento é obrigatório em todos os hospitais do SUS (Lei nº 12.845/2013); o que o indicador capta é o registro do atendimento e o papel de referência da unidade na rede. A ausência de registro não caracteriza recusa: a unidade pode encaminhar os casos ao serviço de referência do território.
*Fonte:* SIH-SUS (registros de atendimento a vítimas de violência sexual). Referência: Lei nº 12.845/2013.

### 4.8 SMCON Neonatal e/ou Obstétrico

**Conceituação:** adesão do estabelecimento aos módulos Neonatal e Obstétrico do Sistema de Monitoramento do Cuidado Obstétrico e Neonatal (SMCON/IFF-Fiocruz, estratégia Qualineo), de alimentação voluntária.
**Parâmetro:** adesão a pelo menos um dos módulos do SMCON.
**Limitações:** o indicador expressa a incorporação do monitoramento à rotina da unidade, não o resultado assistencial.
*Fonte:* IFF/Fiocruz — Instrutivo do SMCON.

## 5. Estágios de desempenho

A classificação por estágios acompanha o número de **indicadores classificatórios adequados** entre os **8** do painel: Unidade Neonatal completa · Cesariana (Robson ≥2 grupos) · Parto vaginal assistido por enfermeira · Uso de AMIU · Asfixia Neonatal · Oferta de LARC · Atendimento de violência sexual · SMCON Neonatal e/ou Obstétrico.

- "Robson ≥2 grupos" é **um dos 8 indicadores contados**, não uma exigência à parte.
- "Unidade Neonatal completa" conta como adequada quando é **"sim" ou "não se aplica"**.
- O **SMCON conta uma única vez**, por adesão a qualquer um dos módulos.
- A classificação deriva do campo classificatório oficial da planilha (ali denominado "selo de conformidade": ≥5 de 9 itens), **com os módulos do SMCON consolidados em um único indicador**.

| Estágio | Critério | Brasil 2024 |
|---|---|---|
| Avançando | 5 ou mais indicadores adequados | 108 (19,9%) |
| Quase lá | 4 indicadores adequados | 140 (25,8%) |
| No caminho | 2 a 3 indicadores adequados | 232 (42,7%) |
| Início da jornada | 0 a 1 indicador adequado | 63 (11,6%) |

A classificação afere conformidade com itens de qualificação — estrutura, processo e registro — e não constitui, por si, medida de qualidade assistencial. A taxa de cesariana não integra a classificação. Unidades de maior porte e complexidade tendem a reunir mais itens por capacidade instalada e de registro; recomenda-se acompanhar a evolução de cada unidade no tempo, em vez de ordenar unidades de perfis distintos.

## 6. Resultados nacionais de referência (2024)

Valores agregados dos 543 estabelecimentos, para conferência.

| Indicador | Nacional | Indicador | Nacional |
|---|---|---|---|
| % Cesariana adequada (≥2 grupos) | 56,7% (308/543) | % Oferta de LARC | 35,7% (194/543) |
| % Adeq. Robson G1 | 41,8% (227/543) | % Atendimento de violência sexual | 41,4% (225/543) |
| % Adeq. Robson G2 | 51,0% (277/543) | % SMCON Neonatal e/ou Obstétrico | 22,1% (120/543) |
| % Adeq. Robson G3 | 38,9% (211/543) | % Unidade Neonatal completa | 43,6% (237/543) |
| % Adeq. Robson G4 | 50,1% (272/543) | % Uso de AMIU (média das unidades) | 12,6% |
| % Parto vaginal assistido por enfermeira | 28,5% (155/543) | % Avançando (≥5 de 8) | 19,9% (108/543) |
| % Asfixia Neonatal | 71,5% (388/543) | | |

Média do percentual de cesariana nos grupos (estabelecimentos com partos no grupo): G1 36,1% · G2 66,3% · G3 18,5% · G4 49,1%.

## 7. Natureza dos parâmetros

| Item | Natureza |
|---|---|
| Dados-fonte (nascidos vivos, procedimentos, cadastro) | Oficial — SINASC, SIH/SUS, CNES |
| Definição de "unidade neonatal completa" | Oficial — leitos/habilitações CNES (Portarias GM/MS 930/2012 e SAES/MS 2.902/2025) |
| Variáveis clínicas (via de nascimento, Apgar etc.) | DNV/SINASC, alinhadas ao Instrutivo do SMCON |
| Método da classificação de Robson | Oficial — OMS, 2017 |
| Metas por grupo de Robson e demais limiares de adequação | Institucionais — adotados pela equipe responsável pelo painel |
| Consolidação dos módulos do SMCON em um único indicador (8 no total) | Institucional — Coordenação (ago/2026) |
| Taxa geral de cesariana | Não exibida no painel; leitura por grupos de Robson |

## 8. Referências

- BRASIL. Ministério da Saúde. **Portaria GM/MS nº 5.350, de 12 de setembro de 2024** — institui a Rede de Atenção Materna e Infantil no SUS.
- BRASIL. Ministério da Saúde. **Portaria GM/MS nº 5.349, de 12 de setembro de 2024** — financiamento da Rede.
- BRASIL. Ministério da Saúde. **Portaria GM/MS nº 930, de 10 de maio de 2012** — define a organização da atenção ao recém-nascido grave ou potencialmente grave (UTIN, UCINCo e UCINCa).
- BRASIL. Ministério da Saúde/SAES. **Portaria SAES/MS nº 2.902, de 26 de junho de 2025** — leitos e habilitações neonatais no CNES.
- BRASIL. Ministério da Saúde. **Diretrizes Nacionais de Assistência ao Parto Normal.**
- BRASIL. Ministério da Saúde. **Atenção Humanizada ao Abortamento — norma técnica.**
- ORGANIZAÇÃO MUNDIAL DA SAÚDE. **WHO recommendations: intrapartum care for a positive childbirth experience.** Genebra: OMS, 2018.
- BRASIL. Ministério da Saúde. **Nota Técnica Conjunta nº 220**.
- IFF/FIOCRUZ. **Instrutivo do SMCON** — Estratégia Qualineo.
- MINISTÉRIO DA SAÚDE / IFF-FIOCRUZ. **Nota Técnica de ampliação do acesso ao DIU**.
- ORGANIZAÇÃO MUNDIAL DA SAÚDE. **Robson Classification: Implementation Manual.** Genebra: OMS, 2017 (versão OPAS: *La clasificación de Robson: Manual de aplicación*).
- BRASIL. **Lei nº 12.845, de 1º de agosto de 2013** — atendimento obrigatório a vítimas de violência sexual.
- Dados-fonte do painel: **SINASC, CNES, SIH/SUS e SMCON** (extração de 01/07/2026).

## 9. Auditoria

O script `scripts/04_auditoria.py` recalcula os números do painel diretamente da planilha institucional (incluindo a conferência do campo classificatório oficial e da consolidação do SMCON) e deve terminar com 0 falhas antes de qualquer publicação. **Resultado atual: 37 verificações, 0 falhas** (execução de 28/08/2026).
