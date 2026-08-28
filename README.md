# Indicadores da Atenção Obstétrica e Neonatal em Estabelecimentos com mais de 1.000 partos no Brasil — 2024

Painel interativo dos **543 estabelecimentos de saúde com mais de 1.000 partos em 2024** no Brasil, cobrindo **1.253.881 nascimentos** e os indicadores da atenção obstétrica e neonatal.

**Painel publicado:** https://anamazza.github.io/Indicadores_partos_Brasil2024/

**Metodologia completa:** [METODOLOGIA.md](METODOLOGIA.md)

> **Base de dados única:** a planilha institucional `ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES` (derivada de SINASC, CNES, SIH-SUS e SMCON; extração de 01/07/2026). Todo número exibido no painel deriva dela e é conferido contra ela pelo script de auditoria (37 verificações; 0 falhas exigidas antes de publicar).

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

**Cobertura parcial (importante).** O painel inclui apenas estabelecimentos com mais de 1.000 partos em 2024. Agregados territoriais refletem somente essas unidades, não a totalidade dos partos do território. Todo agregado exibe o número de estabelecimentos considerados.

**Estatística de agregação.** Percentuais de adequação = proporção de estabelecimentos adequados, sempre com o número absoluto (adequados/total) — inclusive a asfixia neonatal (% de estabelecimentos com taxa ≤0,6%). % Uso de AMIU e a cesariana nos grupos de Robson usam a **média** das unidades da seleção (excluídas, no caso de Robson, as sem partos no grupo). O painel **não usa mediana**.

**Cesariana.** A leitura é pelos **grupos de Robson (G1 a G4)** — cada grupo tem a sua própria meta institucional (ref. Manual de Robson, OMS/OPAS 2017: G1 ≤10% · G2 ≤35% · G3 ≤3% · G4 ≤15%); estabelecimento adequado = **≥2 grupos** dentro da meta. Não há meta de taxa geral de cesariana no painel.

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
img/
  logos_institucionais_branco_semgov.png   Faixa IFF · Fiocruz · SUS
dados/
  dados.json             543 estabelecimentos com todos os campos usados
  geo_multi.json         Geometria dos 3 níveis territoriais (paths SVG)
  flags_nomes.json       Nomes das 9 flags da base (o painel consolida o SMCON em 1 — 8 indicadores)
scripts/
  01_preparar_dados.py   Planilha .xlsx → dados/dados.json
  02_gerar_geometria.py  Shapefiles/GeoJSON → dados/geo_multi.json
  03_montar_painel.py    Template + JSONs → index.html
  04_auditoria.py        Confere os números do painel contra a planilha
publicar_no_github.sh    Publica as alterações locais neste repositório
```

## Como atualizar com uma nova planilha

```bash
pip install pandas openpyxl pyshp shapely

python scripts/01_preparar_dados.py NOVA_PLANILHA.xlsx
python scripts/04_auditoria.py     NOVA_PLANILHA.xlsx   # precisa terminar com 0 falhas
python scripts/03_montar_painel.py                       # gera o index.html
```

O `painel_template.html` regenera o painel publicado byte a byte (roundtrip verificado). O `02_gerar_geometria.py` só precisa ser reexecutado se a malha territorial mudar.

## Tecnologias

HTML/CSS/JS em arquivo único, sem build. Bibliotecas via CDN: Chart.js 4 + ChartDataLabels, Leaflet + MarkerCluster (mapa de unidades), SheetJS (Excel), jsPDF + AutoTable (PDF). Mapa coroplético em SVG inline gerado pelo pipeline Python (pyshp + shapely). Identidade visual inspirada na publicação *Indicadores Básicos para a Saúde no Brasil* (RIPSA/Fiocruz).
