# Indicadores da Atenção Obstétrica e Neonatal em Estabelecimentos com mais de 1.000 partos no Brasil — 2024

Painel interativo dos estabelecimentos de saúde com **mais de 1.000 partos no ano** no Brasil e os indicadores da atenção obstétrica e neonatal, com **seletor de ano de referência**:

| Ano | Universo | Situação |
|---|---|---|
| **2024** | 543 estabelecimentos · 1.253.881 partos | planilha institucional de 01/07/2026 (dados finais) |
| **2025** | 555 estabelecimentos · 1.272.466 partos | **preliminar** — recalculado dos microdados em 04/11/2026 (SINASC preliminar de 31/08/2026; SIH sujeito a acréscimos); ainda sem SMCON e sem atendimento de violência sexual (fonte fora do SIH), por isso **sem estágios de desempenho** |

A ficha de cada unidade (mapa de unidades e lista) mostra a variação de partos e de indicadores adequados entre os anos.

**Painel publicado:** https://anamazza.github.io/Indicadores_partos_Brasil2024/

**Metodologia completa:** [METODOLOGIA.md](METODOLOGIA.md)

> **Base de dados por ano:** uma planilha no formato `ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_<ano>__INDICADORES` (derivada de SINASC, CNES, SIH-SUS e SMCON). 2024 é a planilha institucional de 01/07/2026; 2025 foi montada pelos scripts de `scripts/extracao/` com as regras que reproduzem a planilha de 2024 CNES a CNES (97,9% das 23.349 células; violência sexual não reproduzida — ver [relatorios/reproducao_2024.md](relatorios/reproducao_2024.md)). Todo número exibido deriva da planilha do ano e é conferido contra ela pelo script de auditoria (2024: 41 verificações, 0 falhas; 2025: 31, 0 falhas).

## Funcionalidades

- **Capa institucional** — Coordenação de Ações Nacionais e de Cooperação em Saúde da Mulher, da Criança e do Adolescente (IFF · Fiocruz · SUS) — com navegação direta pelos indicadores, na ordem padrão.
- **Mapa coroplético em três níveis territoriais** (UF, macrorregião de saúde e região de saúde), com navegação em cascata Brasil → Região → Estado, zoom animado e toque para filtrar todo o painel.
- **Indicadores mapeáveis na ordem padrão** — Unidade Neonatal completa, cesariana pelos grupos de Robson, parto vaginal assistido por enfermeira, uso de AMIU, asfixia neonatal, oferta de LARC, atendimento de violência sexual, SMCON Neonatal e/ou Obstétrico e o estágio Avançando — todos com 1 casa decimal e número absoluto (adequados/total).
- **Cesariana pelos grupos de Robson (G1 a G4)**: estabelecimento adequado quando pelo menos **2 grupos** estão dentro da referência do grupo. O painel não exibe meta de taxa geral de cesariana.
- **Estágios de desempenho (Avançando: ≥5 de 8 indicadores)** em quatro estágios clicáveis — Avançando, Quase lá, No caminho e Início da jornada — com destaque para o que mais falta às unidades a um passo do estágio Avançando.
- **Mapa de unidades (Leaflet)**: cada estabelecimento é um ponto na cor do seu estágio de desempenho, com clusters, filtros por estado/macrorregião e popup-resumo da unidade.
- **Matriz semáforo** território × indicador na ordem padrão, ordenável, com % de estabelecimentos adequados em quatro faixas de cor, guarda para n<5 e exportação em Excel.
- **Lista de estabelecimentos** com CNES pesquisável (oculto na exibição), Município (UF) condensado, badges dos indicadores na ordem padrão, filtros rápidos, paginação e exportação em Excel.
- **Exportações**: Excel e PDF da seleção, PNG do mapa e de cada gráfico (com título e contexto embutidos).
- **Mobile-first**: filtros em gaveta inferior (bottom sheet), barra fixa de filtros ativos e alvos de toque ampliados.

## Fontes de dados

| Dado | Fonte |
|---|---|
| Indicadores por estabelecimento | Planilha institucional derivada de SINASC, CNES, SIH/SUS e SMCON (extração 01/07/2026) |
| Malha das regiões de saúde (439) | Shapefile `view_tb_regiao_saudePolygon` (SIRGAS 2000 / EPSG 4674) |
| Malha das macrorregiões de saúde (121) | GeoJSON atualizado (inclui a revisão da regionalização de Minas Gerais); códigos casados por etiqueta com `view_tb_macro_regiao` |
| Limites estaduais | Dissolve das regiões de saúde por código de UF |
| Coordenadas dos estabelecimentos | Geocodificação por CNES (duas unidades sem geo exata usam o centro do município) |

Todos os dados são públicos e agregados por estabelecimento; não há informação individual de pacientes.

## Notas metodológicas

**Cobertura parcial (importante).** O painel inclui apenas estabelecimentos com mais de 1.000 partos no ano selecionado. Agregados territoriais refletem somente essas unidades, não a totalidade dos partos do território. Todo agregado exibe o número de estabelecimentos considerados.

**2025 é preliminar.** O SINASC 2025 é a versão preliminar de 31/08/2026 e o SIH recebe reapresentações; os números mudam a cada extração. Os indicadores sem fonte recebida (SMCON; atendimento de violência sexual, que não consta do SIH) aparecem como "—" e os estágios de desempenho não são calculados até que todos os 8 indicadores existam. Os partos e o AMIU de 2025 são as AIH com **data de internação em 2025** (regra do dicionário da coordenação; a planilha de 2024 usou a competência 2025 — ver o relatório de reprodução). A comparação com a planilha 2025 enviada pela coordenação está em [relatorios/comparacao_2025_tatiana.md](relatorios/comparacao_2025_tatiana.md).

**Estatística de agregação.** Percentuais de adequação = proporção de estabelecimentos adequados, sempre com o número absoluto (adequados/total) — inclusive a asfixia neonatal (% de estabelecimentos com taxa ≤0,6%). % Uso de AMIU e a cesariana nos grupos de Robson usam a **média** das unidades da seleção (excluídas, no caso de Robson, as sem partos no grupo). O painel **não usa mediana**.

**Cesariana.** A leitura é pelos **grupos de Robson (G1 a G4)** — cada grupo tem a sua própria faixa de adequação; estabelecimento adequado = **≥2 grupos** dentro da faixa. A reprodução da planilha de 2024 mostrou que a classificação por grupo usa **intervalos** (G1 1–30% · G2 até 67% · G3 1–12% · G4 até 47%; 0% nunca é adequado), e não as metas 10/35/3/15 citadas anteriormente — os limites estão em confirmação com a coordenação. Não há meta de taxa geral de cesariana no painel.

**Classes do mapa.** Todos os indicadores mapeados são percentuais de adequação ("mais é melhor"). Quintis sobre os territórios visíveis no nível selecionado; escala sequencial de verdes, segura para daltonismo; faixas repetidas são colapsadas na legenda. Territórios sem estabelecimento elegível aparecem em cinza.

**Matriz semáforo.** Cada célula é o % de estabelecimentos do território adequados no indicador, em quatro faixas: ≥75%, 50–74%, 25–49% e <25%. Territórios com menos de 5 unidades aparecem em tom atenuado (percentual instável); o `n` acompanha cada linha.

**Estágios de desempenho.** O estágio **Avançando** reconhece estabelecimentos com **5 ou mais dos 8 indicadores classificatórios** adequados (Unidade Neonatal completa, Cesariana/Robson ≥2 grupos, Parto vaginal assistido por enfermeira, Uso de AMIU, Asfixia Neonatal, Oferta de LARC, Atendimento de violência sexual e SMCON Neonatal e/ou Obstétrico). Robson ≥2 grupos é **um dos 8 indicadores, não uma exigência à parte**; o **SMCON conta uma única vez**, por qualquer um dos módulos. A "unidade neonatal completa" conta como adequada quando é "sim" **ou** "não se aplica". A classificação deriva do campo classificatório oficial da planilha (ali denominado "selo de conformidade": ≥5 de 9 itens), com o SMCON consolidado em um indicador. Brasil 2024: Avançando 108 · Quase lá 140 · No caminho 232 · Início da jornada 63.

**Critérios de adequação.** Os limiares que classificam cada indicador como "adequado" (ex.: asfixia neonatal ≤ 0,6%; parto por enfermeira e uso de AMIU ≥ 50%; oferta de LARC ≥ 3 inserções/ano; violência sexual ≥ 2 atendimentos; faixas por grupo de Robson) são **institucionais**, definidos na planilha-base, e não constam em ato oficial publicado.

**Enquadramento do zoom.** As caixas de zoom por UF excluem ilhas oceânicas remotas (Trindade/Martim Vaz no ES e Fernando de Noronha em PE) e aplicam um piso de enquadramento para estados pequenos.

## Estrutura do repositório

```
index.html               Painel final autossuficiente (publicado no GitHub Pages)
painel_template.html     Código-fonte do painel, sem dados embutidos
METODOLOGIA.md           Metodologia dos indicadores
ATUALIZACAO_2025.md      Briefing da atualização 2025
relatorios/
  reproducao_2024.md     Reprodução da planilha 2024 a partir dos microdados (regras efetivas, diferenças, questões)
planilhas/
  ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES_01072026.xlsx   planilha institucional de 2024
  PLANILHA_2024_recalculada.xlsx    2024 recalculada dos microdados (rastreabilidade)
  PLANILHA_2025_prelim_internacao.xlsx   2025 preliminar (partos e AMIU pela data de internação 2025) — base do painel
  PLANILHA_2025_prelim_saida.xlsx        variante pela data de saída 2025
  reproducao_2024.md / comparacao_2025_tatiana.md (em relatorios/)
img/
  logos_institucionais_branco_semgov.png   Faixa IFF · Fiocruz · SUS
dados/
  dados_<ano>.json       Estabelecimentos do ano com todos os campos usados
  ano_<ano>.json         Configuração do ano: universo, extração, preliminar, indicadores sem fonte
  geo_multi.json         Geometria dos 3 níveis territoriais (paths SVG)
  flags_nomes.json       Nomes das 9 flags da base (o painel consolida o SMCON em 1 — 8 indicadores)
scripts/
  01_preparar_dados.py   Planilha .xlsx + ano → dados/dados_<ano>.json e dados/ano_<ano>.json
  02_gerar_geometria.py  Shapefiles/GeoJSON → dados/geo_multi.json
  03_montar_painel.py    Template + todos os anos → index.html
  04_auditoria.py        Confere os números do painel contra a planilha do ano
  extracao/              Recalcula a planilha a partir dos microdados (SINASC, SIH-RD/SP, CNES):
    sinasc_indicadores.py, sih_partos.py, sih_sp_atos.py, cnes_leitos_neo.py, cnes_habilitacoes.py,
    regras.py (regras que reproduzem a planilha), montar_planilha.py (gera a planilha do ano),
    reproducao_2024.py (relatório de reprodução)
extracao/                Listas de CNES e agregados intermediários (saida/); cache/ e varreduras grandes ficam fora do git
publicar_no_github.sh    Publica as alterações locais neste repositório
```

## Como atualizar

**Com uma planilha recebida da coordenação** (mesmo formato de 57 colunas):

```bash
pip install pandas openpyxl pyshp shapely

python scripts/01_preparar_dados.py planilhas/PLANILHA_2025.xlsx 2025 --extracao dd/mm/aaaa [--preliminar]
python scripts/04_auditoria.py     planilhas/PLANILHA_2025.xlsx 2025   # precisa terminar com 0 falhas
python scripts/03_montar_painel.py                                      # gera o index.html com todos os anos
```

Colunas inteiramente vazias (ex.: SMCON ainda não recebido) são tratadas como indicador sem fonte no ano: o painel mostra "—" e não calcula estágios.

**Recalculando a planilha dos microdados** (máquina com a esteira `Extracao_SIH`/`Extracao_SINASC`; caminhos em `scripts/extracao/*.py`):

```bash
python scripts/extracao/sinasc_indicadores.py 2025 SINASC_2025_csv.zip extracao/saida/sinasc_2025.json
python scripts/extracao/sih_partos.py <pasta_RD> 2401 2608 extracao/cnes_referencia_2024.txt extracao/saida/sih_rd
python scripts/extracao/cnes_leitos_neo.py <pasta_LT> 2401 2609 extracao/saida/cnes_leitos_2401_2609.json
python scripts/extracao/cnes_habilitacoes.py extracao/cnes_candidatos_2025.txt extracao/saida/cnes_fichas.json
python scripts/extracao/montar_planilha.py --ano 2025 --sinasc sinasc_2025.json --partos i2025 --amiu i2025 --cnes 2609 \
       --referencia planilhas/ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES_01072026.xlsx \
       --sp extracao/saida/codigos_sp_2025.json --saida planilhas/PLANILHA_2025_prelim_internacao.xlsx [--smcon smcon_2025.csv]
```

O `painel_template.html` regenera o painel publicado (roundtrip verificado). O `02_gerar_geometria.py` só precisa ser reexecutado se a malha territorial mudar.

## Tecnologias

HTML/CSS/JS em arquivo único, sem build. Bibliotecas via CDN: Chart.js 4 + ChartDataLabels, Leaflet + MarkerCluster (mapa de unidades), SheetJS (Excel), jsPDF + AutoTable (PDF). Mapa coroplético em SVG inline gerado pelo pipeline Python (pyshp + shapely). Identidade visual inspirada na publicação *Indicadores Básicos para a Saúde no Brasil* (RIPSA/Fiocruz).
