# Comparação: planilha 2025 da coordenação × recálculo pelos microdados

Planilha recebida em 04/11/2026: `ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2025_INDICADORES_04112026.xlsx` (aba INDICADORES, 554 unidades, 48 colunas — sem as colunas de classificação, sem SMCON, sem STATUS; percentuais em fração).
Recálculo: `planilhas/PLANILHA_2025_prelim_internacao.xlsx` (555 unidades), gerado por `scripts/extracao/montar_planilha.py` com as regras de `regras.py`.
Comparação CNES a CNES; **a planilha da coordenação não é tratada como gabarito** — cada divergência vem com a evidência de qual lado a sustenta.

## Resumo

| Coluna | Resultado | Leitura |
|---|---|---|
| Partos (6 colunas, TOTAL) | **AIH pela data de internação 2025**: 501/554 TOTAL exatos; nas 53 restantes o recálculo tem **mais** AIH (de +1 a +25) | Recorte coincide com a regra aprovada no dicionário da coordenação (09/09/2026); as diferenças são reapresentações posteriores à extração dela. Adotado no painel. |
| Universo (> 1.000 partos) | 554 × 555: todas as 554 estão no recálculo; a extra (2527413, 1.022 partos) ficou acima de 1.000 com as reapresentações | Consequência do item anterior. |
| % AMIU | data de internação 2025: 547/554 (±0,05 p.p.) | Mesma regra; diferenças de reapresentação. |
| % Parto vaginal por enfermeira | 551/554 | Mesma regra (TPNASCASSI = 2 ÷ todos os partos vaginais). |
| HGPAR | 553/554 (habilitação 1420 vigente) | Mesma regra. |
| Gestão / natureza jurídica | 548/554 (rótulos diferentes: "Municipal" ≡ MUNICIPAL; "Administração Pública" ≡ PÚBLICO; "Entidades Empresariais" ≡ PRIVADO) | Mesma regra; diferenças pela competência do CNES. |
| Unidade neonatal completa | "SIM" coincide em 554/554 (CNES 03/2026), mas a planilha dela **não tem "NÃO SE APLICA"** (só SIM/NÃO) | Divergência de regra: no painel, "não se aplica" (unidade sem leitos neonatais) conta como adequado; na planilha dela essas 96 unidades viram "NÃO". O recálculo mantém a regra de 2024. |
| % Asfixia | 236/554 com a regra de 2024; **551/554** com outro denominador | Ela mudou a regra em relação a 2024: numerador igual (Apgar 5' < 7, peso ≥ 2.500 g, anomalia = "não") mas denominador = **NV ≥ 2.500 g sem anomalia** (coerente com o nome da coluna), enquanto a planilha 2024 dividia por **todos os NV** (543/543 só assim). Aplicar a regra nova a 2024 reproduz só 215/543. Decisão pendente: qual regra vale — e, se for a nova, 2024 precisa ser recalculado para manter a comparabilidade. O painel segue com a regra de 2024 nos dois anos. |
| Robson (NV e cesáreas G1–G4) | **não reproduzido** (1–6 de 554 iguais) | **Os valores dela não são grupos de Robson**: os 4 "grupos" somam o total de nascidos vivos da unidade em 483/549 (G1–G4 de Robson cobrem só parte dos NV) e as cesáreas dos 4 somam todas as cesáreas em 499/549; a taxa de cesárea sai ~54–57% nos quatro grupos (pelo TPROBSON: G1 38,6%, G2 67,2%, G3 18,2%, G4 47,6%; G3 com 69,5% de cesárea é impossível para multíparas sem cesárea prévia em trabalho de parto espontâneo). Nenhuma combinação dos grupos 1–10 do TPROBSON reproduz as colunas. Provável erro de tabulação na planilha dela. O painel usa o TPROBSON, como a planilha 2024 (542/542). |
| DIU / implante | 366/554 e 515/554 iguais, mas **soma dela = 14.249 DIU e 531 implantes** contra 26.585 e 2.899 no recálculo | **São Paulo está zerado na planilha dela** (0 × 11.833 DIU; 61 unidades com registro), e as demais UFs ficam próximas (pequenas diferenças de reapresentação). Fonte igual (atos profissionais da AIH, SP_ATOPROF 0301040141 e 0301040176); faltou o estado de SP na extração dela. O painel usa o recálculo (atribuição por data de saída até a varredura por data de internação terminar). |
| Violência sexual | zerada nas duas | Fonte ainda não identificada (não está no SIH). |
| SMCON | ausente nas duas | Pendente. |

## Decisões adotadas no painel (2025, preliminar)

- Partos e AMIU pela **data de internação 2025** (regra do dicionário da coordenação; coincide com a planilha dela). Universo: 555 unidades, 1.272.466 partos.
- Robson pelo **TPROBSON** (regra da planilha 2024); asfixia com a **regra de 2024** (÷ todos os NV); unidade neonatal com "não se aplica".
- DIU/implante pelos atos profissionais da AIH, todas as UFs.
- Sem estágios de desempenho até haver SMCON e violência sexual.

## Para levar à coordenação

1. Robson 2025: a tabulação da planilha precisa ser refeita (os grupos não são os de Robson).
2. DIU/implante 2025: incluir São Paulo.
3. Asfixia: definir o denominador (todos os NV, como em 2024, ou NV ≥ 2.500 g sem anomalia, como em 2025) e aplicar o mesmo aos dois anos.
4. Unidade neonatal: manter "não se aplica" (regra do painel) ou passar a SIM/NÃO.
5. Fonte e códigos da violência sexual; lista SMCON 2025.
6. HC FAMEMA (Marília/SP): as AIH de parto estão no CNES 2025507 e as DNV no 2025523 (Unidade Materno Infantil). Na planilha de 2024 a unidade (2025507) está com Robson, asfixia e parto por enfermeira zerados (asfixia 0% = "adequado"); no painel 2025 os nascimentos do 2025523 passaram a ser somados (1.359 NV). Corrigir 2024 na planilha institucional.
