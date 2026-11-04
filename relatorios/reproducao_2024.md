# Reprodução da planilha 2024 a partir dos microdados

Planilha de referência: `ESTABELECIMENTOS_ACIMA DE 1000 PARTOS_2024_ INDICADORES_01072026.xlsx` — 543 estabelecimentos. Células comparadas: 23,349; iguais: 22,859 (97.90%).

Regras aplicadas (as que reproduzem a planilha; ver `scripts/extracao/regras.py`):

- Partos (6 colunas): PROC_REA da AIH reduzida (RD) por **ano de competência 2025** (ANO_CMPT) — a data de internação/saída 2024 não reproduz a planilha.
- AMIU: `0409060070 ÷ (0409060070 + 0411020013)`, AIH com **data de saída em 2024**.
- Robson: NV e cesáreas por `TPROBSON` 1–4 (cesárea = `PARTO = 2`); grupo adequado quando NV > 0 e **1% ≤ taxa ≤ 30% (G1), 67% (G2), 12% (G3), 47% (G4)** — intervalos empíricos da planilha.
- Asfixia: `APGAR5 < 7`, `PESO ≥ 2500`, `IDANOMAL = 2` ÷ **todos os nascidos vivos** da unidade.
- Enfermagem: `TPNASCASSI = 2` ÷ todos os `PARTO = 1` (inclusive profissional ignorado).
- Unidade neonatal: leitos existentes (CNES-LT, competência 03/2026) de UTIN (81/82), UCINCo (92) e UCINCa (93).
- Gestão: `TPGESTAO` E/M/D; natureza: `NAT_JUR` 1→PÚBLICO, 3→SEM FINS LUCRATIVOS, 2 (inclusive 2011)→PRIVADO; HGPAR: habilitação 1420 vigente.

| Grupo | Coluna | Iguais | Diferentes | Exemplos (planilha × recalculado) |
|---|---|---:|---:|---|
| SIH — partos (AIH por competência 2025) | OPERAÇÃO CESARIANA | 530 | 13 | 2615746: 1041.0 × 1042.0; 2000733: 26.0 × 27.0; 2000296: 1276.0 × 1352.0 |
| SIH — partos (AIH por competência 2025) | OPERAÇÃO CESARIANA C/ LAQUEADURA TUBARIA | 533 | 10 | 2615746: 474.0 × 473.0; 2000296: 192.0 × 203.0; 2365146: 47.0 × 65.0 |
| SIH — partos (AIH por competência 2025) | OPERAÇÃO CESARIANA EM GAR | 540 | 3 | 2000733: 2159.0 × 2321.0; 2002078: 74.0 × 78.0; 2153882: 624.0 × 626.0 |
| SIH — partos (AIH por competência 2025) | PARTO NORMAL | 531 | 12 | 2000733: 476.0 × 497.0; 2000296: 1194.0 × 1293.0; 2365146: 955.0 × 1004.0 |
| SIH — partos (AIH por competência 2025) | PARTO NORMAL EM CPN | 540 | 3 | 2000733: 1248.0 × 1378.0; 2806215: 1041.0 × 1040.0; 2002078: 968.0 × 1059.0 |
| SIH — partos (AIH por competência 2025) | PARTO NORMAL EM GESTACAO DE ALTO RISCO | 542 | 1 | 2002078: 30.0 × 31.0 |
| SIH — partos (AIH por competência 2025) | TOTAL | 528 | 15 | 2000733: 3910.0 × 4224.0; 2000296: 2662.0 × 2848.0; 2365146: 2427.0 × 2587.0 |
| SIH — partos (AIH por competência 2025) | TOTAL S/ CPN | 528 | 15 | 2000733: 2662.0 × 2846.0; 2000296: 2662.0 × 2848.0; 2365146: 2427.0 × 2587.0 |
| SIH — AMIU (ano pela data de saída 2024) | % AMIU | 541 | 2 | 2710935: 6.8 × 6.7; 5878640: 0.0 × 36.1 |
| SIH — AMIU (ano pela data de saída 2024) | CLASSIFICAÇÃO AMIU | 543 | 0 |  |
| SINASC 2024 — Robson | TOTAL NV G1 | 543 | 0 |  |
| SINASC 2024 — Robson | Nº CESAREANA G1 | 543 | 0 |  |
| SINASC 2024 — Robson | % CESAREANA G1 | 543 | 0 |  |
| SINASC 2024 — Robson | CLASSIFICAÇÃO G1 | 543 | 0 |  |
| SINASC 2024 — Robson | TOTAL NV G2 | 543 | 0 |  |
| SINASC 2024 — Robson | Nº CESAREANA G2 | 543 | 0 |  |
| SINASC 2024 — Robson | % CESAREANA G2 | 543 | 0 |  |
| SINASC 2024 — Robson | CLASSIFICAÇÃO G2 | 543 | 0 |  |
| SINASC 2024 — Robson | TOTAL NV G3 | 543 | 0 |  |
| SINASC 2024 — Robson | Nº CESAREANA G3 | 543 | 0 |  |
| SINASC 2024 — Robson | % CESAREANA G3 | 543 | 0 |  |
| SINASC 2024 — Robson | CLASSIFICAÇÃO G3 | 543 | 0 |  |
| SINASC 2024 — Robson | TOTAL NV G4 | 543 | 0 |  |
| SINASC 2024 — Robson | Nº CESAREANA G4 | 543 | 0 |  |
| SINASC 2024 — Robson | % CESAREANA G4 | 543 | 0 |  |
| SINASC 2024 — Robson | CLASSIFICAÇÃO G4 | 543 | 0 |  |
| SINASC 2024 — Robson | TOTAL CLASSIFICAÇÃO | 543 | 0 |  |
| SINASC 2024 — Robson | CLASSIFICAÇÃO ROBSON  (≥2 GRUPOS) | 543 | 0 |  |
| SINASC 2024 — asfixia e enfermagem | % ASFIXIA ≥2500G SEM ANOMALIAS CONGÊNITAS | 543 | 0 |  |
| SINASC 2024 — asfixia e enfermagem | CLASSIFICAÇÃO ASFIXIA | 543 | 0 |  |
| SINASC 2024 — asfixia e enfermagem | % PARTO VAGINAL ASSISTIDO POR ENFERMAGEM | 543 | 0 |  |
| SINASC 2024 — asfixia e enfermagem | CLASSIFICAÇÃO PARTO ENF. | 543 | 0 |  |
| CNES (competência 03/2026) | UNIDADE NEONATAL COMPLETA | 541 | 2 | 0013846: SIM × NÃO; 2351994: NÃO SE APLICA × None |
| CNES (competência 03/2026) | GESTÃO | 541 | 2 | 8015899: MUNICIPAL × ESTADUAL; 0018333: ESTADUAL × DUPLA |
| CNES (competência 03/2026) | NATUREZA JURÍDICA | 543 | 0 |  |
| CNES (competência 03/2026) | HGPAR | 495 | 48 | 2798662: 0 × SIM; 2436477: 0 × SIM; 2499363: SIM × 0 |
| SIH-SP — LARC (atos 0301040141 DIU e 0301040176 implante, competência 2025) | DIU | 383 | 160 | 0026794: 323.0 × 336.0; 2410281: 159.0 × 207.0; 2323397: 15.0 × 22.0 |
| SIH-SP — LARC (atos 0301040141 DIU e 0301040176 implante, competência 2025) | IMPLANTE  | 514 | 29 | 2079186: 433.0 × 452.0; 0009628: 49.0 × 50.0; 2077388: 93.0 × 92.0 |
| SIH-SP — LARC (atos 0301040141 DIU e 0301040176 implante, competência 2025) | TOTAL.1 | 375 | 168 | 0026794: 323.0 × 336.0; 2410281: 159.0 × 207.0; 2323397: 15.0 × 22.0 |
| SIH-SP — LARC (atos 0301040141 DIU e 0301040176 implante, competência 2025) | CLASSIFICAÇÃO CONTRACEPÇÃO | 537 | 6 | 2269945: None × SIM; 0010499: None × SIM; 0010529: None × SIM |
| Violência sexual (não reproduzida: nenhum ato do SIH-SP corresponde; valores copiados da planilha) | Nº DE ATENDIMENTOS A VÍTIMA DE VIOLÊNCIA SEXUAL | 543 | 0 |  |
| Violência sexual (não reproduzida: nenhum ato do SIH-SP corresponde; valores copiados da planilha) | CLASSIFICAÇÃO VIOLÊNCIA SEXUAL | 543 | 0 |  |
| Campo oficial (≥5 de 9) | CLASSIFICAÇÃO TOTAL ≥5 ROBSON 2 GRUPOS | 542 | 1 | 2269945: None × ADEQUADO |

Tabela completa das diferenças: `extracao/saida/reproducao_2024_diferencas.csv`; recálculo por CNES: `extracao/saida/reproducao_2024_recalculo.csv`; planilha recalculada no formato original: `planilhas/PLANILHA_2024_recalculada.xlsx`.

## Achados da reprodução (para decisão da coordenação)

1. **Ano das AIH de parto.** As seis colunas de parto da planilha "2024" são as AIH **processadas na competência 2025** (ANO_CMPT = 2025): 528/543 exatas. Nenhuma atribuição de 2024 (competência, data de internação ou data de saída) reproduz a planilha. As 15 diferenças restantes são todas de unidades em que o recálculo tem **mais** AIH (AC, PI, PA, RJ, BA, SE, MA, AL, RO; de +73 a +536) — reapresentações incorporadas ao SIH depois da extração de 01/07/2026 — ou diferenças de 1 a 3 AIH. Consequência: para 2025 é preciso decidir qual ano das AIH usar (competência 2026 só existe até 08/2026; a data de saída 2025 é a opção consistente com a regra do AMIU).
2. **AMIU** usa outro recorte de ano: AIH com **data de saída em 2024** (541/543). A planilha mistura, portanto, dois recortes de ano do SIH.
3. **Asfixia**: o denominador é o **total de nascidos vivos** da unidade, não os nascidos ≥2.500 g sem anomalia como diz o nome da coluna (543/543 só com esse denominador). O numerador exige anomalia congênita = "Não" (IDANOMAL = 2; ignorados ficam fora).
4. **Classificação por grupo de Robson** não usa as metas 10/35/3/15 da nota metodológica: o grupo é adequado quando a taxa de cesariana está num **intervalo** — G1 de 1% a 30%, G2 até 67%, G3 de 1% a 12%, G4 até 47% (limites empíricos; 0% nunca é adequado; não há valores observados entre 0,8% e 1,1% nem exatamente nos limites superiores de G2/G4, que podem estar entre 67,0–67,4 e 46,8–47,1). As demais regras de classificação (≥2 grupos, asfixia ≤0,6, enfermagem ≥50, AMIU ≥50, LARC ≥3, violência ≥2, ≥5 de 9) reproduzem 543/543.
5. **Parto por enfermeira**: denominador = todos os partos vaginais, **inclusive** os com profissional ignorado (542/542).
6. **Unidade neonatal completa**: leitos existentes do CNES-LT na competência **03/2026** (UTIN 81/82 + UCINCo 92 + UCINCa 93) — 541/543; divergem o Hospital do Rocio (0013846, tem 81/82 e 92 mas não 93 no LT; planilha "SIM") e o Hospital de Caruaru (2351994, desativado, sem leitos no LT; planilha "NÃO SE APLICA").
7. **HGPAR**: a habilitação CNES 1420 só existe desde 08/2025; a planilha marca 160 unidades, das quais 158 têm a 1420, e deixa de marcar 46 que também a têm — a lista da planilha veio de outra fonte/momento. Duas unidades marcadas não têm a habilitação (HGCC 2499363 e 2798662).
8. **Gestão e natureza**: TPGESTAO (E/M/D) e NAT_JUR (1 → público; 3 → sem fins lucrativos; 2, inclusive 2011 EBSERH → privado) na competência 03/2026: 541 e 543 iguais.
9. **CNES trocado**: em duas linhas a coluna CNES traz o código antigo (2679663, 3511251) e o rótulo o novo (9131922, 5878640); o SIH está no código novo e o SINASC continua no antigo (por isso Robson/asfixia dessas linhas são 0 na planilha). O recálculo 2025 funde os dois códigos no SINASC.
10. **Universo**: "mais de 1.000 partos" pelas AIH de competência 2025 dá 553 unidades: 541 das 543 (as 2 restantes são os códigos antigos acima) e 12 unidades com 1.003–1.232 partos que não estão na planilha. O critério exato de inclusão da planilha não foi reproduzido.
11. **DIU e implante** são atos profissionais da AIH (arquivo SP, `SP_ATOPROF`): **0301040141** (inserção de DIU) e **0301040176** (implante subdérmico de etonogestrel), contados por linha na competência 2025 — o mesmo recorte dos partos. Identificados por casamento do vetor por CNES (383/543 e 514/543 exatos; as diferenças seguem o padrão das reapresentações). **Violência sexual não corresponde a nenhum ato do SIH-SP** (melhor casamento: 22 de 271 unidades) — a fonte deve ser o SIA/BPA (produção ambulatorial), que não está na esteira local; em 2025 a coluna fica em branco até a coordenação informar a fonte e os códigos.

## Perguntas para a coordenação antes de fechar 2025

- Confirmar o recorte de ano do SIH para 2025 (competência × data de saída × data de internação) e, se for o caso, reprocessar 2024 com o mesmo recorte.
- Confirmar os limites por grupo de Robson usados (intervalos acima) e atualizar a nota metodológica.
- Confirmar fonte e códigos de DIU, implante e atendimento a vítima de violência sexual (SIH-SP? SIA/BPA?).
- Confirmar a regra de HGPAR (habilitação 1420 vigente ou lista própria) e a competência do CNES para leitos/gestão/natureza.
- SMCON 2025: lista CNES × módulo e data de corte.
