# Indicadores Obstétricos e Neonatais — Brasil 2024

Painel interativo dos **543 estabelecimentos de saúde com mais de 1.000 partos em 2024** no Brasil, cobrindo 1.253.881 nascimentos e 20 indicadores de qualidade da atenção obstétrica e neonatal.

**Painel publicado:** https://anamazza.github.io/Indicadores_partos_Brasil2024/

## Funcionalidades

- **Mapa coroplético em três níveis territoriais** (UF, macrorregião de saúde e região de saúde), com geometria oficial em SIRGAS 2000, navegação em cascata Brasil → Região → Estado, zoom animado, rótulos dos territórios no recorte estadual e toque para filtrar todo o painel.
- **20 indicadores mapeáveis organizados em 5 eixos temáticos**: via de parto e Robson, segurança e estrutura, boas práticas, direitos reprodutivos e visão geral.
- **Selo de qualidade (≥5 indicadores adequados)**: card com percentual geral e quatro estágios nomeados e clicáveis (Com selo, Quase lá, No caminho, Início da jornada), com destaque para o indicador que mais falta entre as unidades a um passo do selo.
- **Matriz semáforo** território × indicador, ordenável, com % de estabelecimentos adequados em quatro faixas de cor e exportação em Excel.
- **Lista de estabelecimentos** com filtros rápidos (busca, selo, situações de atenção), paginação e exportação em Excel.
- **Exportações**: Excel e PDF da seleção, PNG do mapa e de cada gráfico (com título e contexto da seleção embutidos na imagem).
- **Mobile-first**: filtros em gaveta inferior (bottom sheet) com botão flutuante, barra fixa de filtros ativos e alvos de toque ampliados no mapa.

## Fontes de dados

| Dado | Fonte |
|---|---|
| Indicadores por estabelecimento | Planilha institucional derivada de SINASC, CNES e SIH/SUS (extração 01/07/2026) |
| Malha das regiões de saúde (439) | Shapefile `view_tb_regiao_saudePolygon` (SIRGAS 2000 / EPSG 4674) |
| Malha das macrorregiões de saúde (121) | GeoJSON atualizado (inclui a revisão da regionalização de Minas Gerais); códigos casados por etiqueta com `view_tb_macro_regiao` |
| Limites estaduais | Dissolve das regiões de saúde por código de UF |

Todos os dados são públicos e agregados por estabelecimento; não há informação individual de pacientes.

## Notas metodológicas

**Cobertura parcial (importante).** O painel inclui apenas estabelecimentos com mais de 1.000 partos em 2024. Agregados territoriais (taxa de cesariana de uma região, por exemplo) refletem somente essas unidades, não a totalidade dos partos do território. Todo agregado exibe o número de estabelecimentos considerados.

**Classes do mapa.** Quintis calculados sobre os territórios visíveis no nível selecionado (nacionais no Brasil inteiro; regionais quando há zoom em uma região do país). Escala sequencial de verdes, segura para daltonismo. Territórios sem estabelecimento elegível aparecem em cinza. Verde mais escuro significa **valor maior**, inclusive em indicadores nos quais valor alto é desfavorável (ex.: % cesariana).

**Robson.** O gráfico de barras usa a **mediana** dos percentuais por estabelecimento; o mapa e a matriz usam a taxa **ponderada** (soma de cesarianas ÷ soma de nascidos vivos do grupo), por isso os valores podem diferir entre as visualizações.

**Matriz semáforo.** Cada célula é o % de estabelecimentos do território adequados no indicador, em quatro faixas: ≥75%, 50–74%, 25–49% e <25%. Territórios com poucas unidades têm percentuais instáveis; o `n` acompanha cada linha.

**Estágios do selo.** O selo reconhece estabelecimentos com **5 ou mais dos 9 indicadores classificatórios** adequados (asfixia, enfermagem obstétrica, AMIU, Robson ≥2 grupos, contracepção, violência sexual, SMCON neonatal, SMCON obstétrico e unidade neonatal completa). Robson ≥2 grupos é **um dos 9 indicadores contados, não uma exigência à parte** — há estabelecimentos com selo sem Robson ≥2 grupos. A "unidade neonatal completa" conta como adequada quando é "sim" **ou** "não se aplica". O selo exibido é o campo oficial da planilha e corresponde exatamente a `nAdeq ≥ 5`.

**Critérios de adequação (importante).** Os limiares que classificam cada indicador como "adequado" (ex.: asfixia ≤ 0,6%; enfermagem e AMIU ≥ 50%; contracepção com DIU+implante ≥ 3; violência sexual ≥ 2 atendimentos; grupos de Robson) são **institucionais**, derivados dos sistemas nacionais (SINASC, CNES, SIH-SUS) e alinhados às variáveis coletadas pelo SMCON (IFF/Fiocruz). A Rede Alyne (Portaria GM/MS 5.350/2024) ainda **não publicou o ato oficial de indicadores** ao qual remete; a única meta oficial referenciada no painel é a **taxa de cesárea ≤ 35%** (valor de referência da Rede Alyne).

**Enquadramento do zoom.** As caixas de zoom por UF excluem ilhas oceânicas remotas (Trindade/Martim Vaz no ES e Fernando de Noronha em PE, que continuam desenhadas no mapa nacional) e aplicam um piso de enquadramento para que estados pequenos não sejam ampliados desproporcionalmente.

## Estrutura do repositório

```
index.html               Painel final autossuficiente (publicado no GitHub Pages)
painel_template.html     Código-fonte do painel, sem dados embutidos
dados/
  dados.json             543 estabelecimentos com todos os campos usados
  geo_multi.json         Geometria dos 3 níveis territoriais (paths SVG)
  flags_nomes.json       Nomes dos 9 indicadores classificatórios (ordem das flags)
scripts/
  01_preparar_dados.py   Planilha .xlsx → dados.json
  02_gerar_geometria.py  Shapefiles/GeoJSON → geo_multi.json
  03_montar_painel.py    Template + JSONs → index.html
  04_auditoria.py        Confere todos os números do painel contra a planilha
```

## Como atualizar com uma nova planilha

```bash
pip install pandas openpyxl pyshp shapely

python scripts/01_preparar_dados.py NOVA_PLANILHA.xlsx
python scripts/04_auditoria.py     NOVA_PLANILHA.xlsx   # precisa terminar com 0 falhas
python scripts/03_montar_painel.py                       # gera o index.html
```

O script `02_gerar_geometria.py` só precisa ser reexecutado se a malha territorial mudar (novos shapefiles).

## Tecnologias

HTML/CSS/JS em arquivo único, sem build. Bibliotecas via CDN: Chart.js 4 + ChartDataLabels, SheetJS (Excel), jsPDF + AutoTable (PDF). Mapa em SVG inline gerado pelo pipeline Python (pyshp + shapely). Identidade visual inspirada na publicação *Indicadores Básicos para a Saúde no Brasil* (RIPSA/Fiocruz).
