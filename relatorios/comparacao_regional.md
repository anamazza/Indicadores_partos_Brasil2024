# Comparação regional: unidades do painel, demais estabelecimentos e região (2024 e 2025)

Protótipo gerado pelos scripts `scripts/extracao/regional.py` (SINASC completo), `scripts/extracao/sim_regional.py` (SIM: DO de todas as UFs e DOFET) e `scripts/extracao/relatorio_regional.py`. Cada região é analisada em quatro recortes: **painel**, estabelecimentos (CNES) da planilha do ano, incluídos os códigos antigos e os complexos somados pelo painel, por UF de ocorrência; **demais estab.**, nascidos vivos (NV) e óbitos ocorridos na região fora dessas unidades (região − painel); **região**, todos os NV e óbitos ocorridos na região; **residência**, NV e óbitos de residentes da região, independentemente do local de ocorrência (base para prevalência e incidência populacionais). Os intervalos de confiança de 95 % (IC 95 %) são de Wilson; o IC da razão painel/demais é calculado na escala logarítmica. p.p. = pontos percentuais.

- **2024:** 2.389.325 NV no `SINASC_2024_csv.zip`; lista do painel `ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES_01072026.xlsx` (546 códigos CNES, incluídos códigos antigos e complexos); SIM: 1.532.015 DO (27 UFs) e 24.364 DOFET.
- **2025:** 2.456.688 NV no `SINASC_2025_csv.zip`; lista do painel `PLANILHA_2025_prelim_internacao.xlsx` (558 códigos CNES, incluídos códigos antigos e complexos); SIM: 1.534.588 DO (27 UFs) e 25.073 DOFET.

## 1. Cobertura: proporção dos nascimentos da região ocorridos nas unidades do painel

| Região | 2024 NV painel | 2024 NV demais | 2024 NV região | 2024 cobertura | 2025 NV painel | 2025 NV demais | 2025 NV região | 2025 cobertura |
|---|---|---|---|---|---|---|---|---|
| Norte | 157.861 | 107.385 | 265.246 | 59,5 % | 166.532 | 108.749 | 275.281 | 60,5 % |
| Nordeste | 411.612 | 255.635 | 667.247 | 61,7 % | 428.116 | 253.651 | 681.767 | 62,8 % |
| Sudeste | 472.382 | 432.218 | 904.600 | 52,2 % | 491.473 | 432.697 | 924.170 | 53,2 % |
| Sul | 181.613 | 155.119 | 336.732 | 53,9 % | 195.578 | 156.002 | 351.580 | 55,6 % |
| Centro-Oeste | 106.793 | 108.707 | 215.500 | 49,6 % | 112.896 | 110.994 | 223.890 | 50,4 % |
| Brasil | 1.330.261 | 1.059.064 | 2.389.325 | 55,7 % | 1.394.595 | 1.062.093 | 2.456.688 | 56,8 % |

## 2. Indicadores do SINASC por região: unidades do painel e demais estabelecimentos

Cada tabela apresenta o valor nas unidades do painel, o valor nos demais estabelecimentos da região e a razão painel/demais, com o IC 95 % entre colchetes. Razão > 1 indica frequência maior nas unidades do painel. Os valores da região como um todo e por residência estão na planilha (abas "Por região" e "Por UF").

### Cesariana (% dos partos)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 54,0 | 55,0 | 0,98 [0,98–0,99] | 56,3 | 56,2 | 1,00 [0,99–1,01] |
| Nordeste | 56,8 | 62,6 | 0,91 [0,90–0,91] | 58,2 | 64,1 | 0,91 [0,91–0,91] |
| Sudeste | 50,5 | 73,0 | 0,69 [0,69–0,69] | 51,7 | 73,7 | 0,70 [0,70–0,70] |
| Sul | 54,1 | 73,7 | 0,73 [0,73–0,74] | 55,2 | 73,5 | 0,75 [0,75–0,76] |
| Centro-Oeste | 55,4 | 77,6 | 0,71 [0,71–0,72] | 55,4 | 78,1 | 0,71 [0,70–0,71] |
| Brasil | 53,8 | 69,2 | 0,78 [0,77–0,78] | 55,0 | 70,0 | 0,79 [0,78–0,79] |

### Prematuridade < 37 semanas (% dos NV)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 13,6 | 11,8 | 1,15 [1,13–1,18] | 13,3 | 11,5 | 1,15 [1,13–1,18] |
| Nordeste | 14,6 | 9,7 | 1,51 [1,49–1,53] | 13,8 | 9,2 | 1,51 [1,49–1,53] |
| Sudeste | 13,3 | 11,0 | 1,22 [1,20–1,23] | 12,9 | 10,5 | 1,23 [1,21–1,24] |
| Sul | 13,9 | 9,8 | 1,42 [1,39–1,44] | 13,8 | 9,3 | 1,48 [1,45–1,50] |
| Centro-Oeste | 14,5 | 10,6 | 1,37 [1,34–1,40] | 13,9 | 10,2 | 1,36 [1,33–1,39] |
| Brasil | 13,9 | 10,5 | 1,32 [1,31–1,33] | 13,4 | 10,1 | 1,33 [1,32–1,34] |

### Baixo peso < 2.500 g (% dos NV)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 9,4 | 7,3 | 1,30 [1,26–1,33] | 9,3 | 6,8 | 1,36 [1,33–1,40] |
| Nordeste | 10,8 | 6,0 | 1,81 [1,78–1,84] | 10,3 | 5,9 | 1,73 [1,70–1,76] |
| Sudeste | 11,5 | 8,6 | 1,35 [1,33–1,37] | 11,2 | 8,3 | 1,35 [1,33–1,37] |
| Sul | 11,3 | 7,1 | 1,58 [1,55–1,62] | 10,9 | 6,7 | 1,64 [1,60–1,67] |
| Centro-Oeste | 11,8 | 7,7 | 1,54 [1,50–1,58] | 11,2 | 7,4 | 1,51 [1,47–1,55] |
| Brasil | 11,0 | 7,5 | 1,47 [1,46–1,48] | 10,6 | 7,2 | 1,47 [1,46–1,48] |

### Muito baixo peso < 1.500 g (por 1.000 NV)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 15,1 | 9,6 | 1,58 [1,47–1,70] | 15,3 | 9,1 | 1,67 [1,55–1,79] |
| Nordeste | 18,3 | 8,4 | 2,17 [2,07–2,28] | 17,0 | 8,7 | 1,96 [1,87–2,05] |
| Sudeste | 19,0 | 12,5 | 1,52 [1,47–1,57] | 18,2 | 11,8 | 1,54 [1,49–1,59] |
| Sul | 18,4 | 9,1 | 2,03 [1,91–2,16] | 17,7 | 8,4 | 2,11 [1,98–2,24] |
| Centro-Oeste | 19,1 | 8,9 | 2,15 [2,00–2,32] | 18,2 | 9,5 | 1,93 [1,79–2,07] |
| Brasil | 18,2 | 10,3 | 1,76 [1,72–1,80] | 17,4 | 10,1 | 1,73 [1,69–1,77] |

### Apgar no 5º minuto < 7 (por 1.000 NV com Apgar informado)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 8,9 | 9,4 | 0,95 [0,87–1,03] | 9,8 | 9,0 | 1,08 [1,00–1,17] |
| Nordeste | 12,7 | 8,9 | 1,42 [1,35–1,49] | 12,4 | 9,6 | 1,29 [1,23–1,35] |
| Sudeste | 11,5 | 8,2 | 1,39 [1,34–1,45] | 11,2 | 8,1 | 1,38 [1,32–1,44] |
| Sul | 13,6 | 7,6 | 1,79 [1,67–1,92] | 13,3 | 7,3 | 1,82 [1,70–1,95] |
| Centro-Oeste | 11,2 | 7,2 | 1,55 [1,41–1,69] | 10,2 | 7,3 | 1,41 [1,29–1,54] |
| Brasil | 11,8 | 8,3 | 1,42 [1,38–1,46] | 11,6 | 8,4 | 1,39 [1,35–1,42] |

### Asfixia com denominador restrito (regra da Coordenação, 2025): Apgar < 7 em NV ≥ 2.500 g sem anomalia (%)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 0,47 | 0,59 | 0,80 [0,72–0,90] | 0,54 | 0,57 | 0,95 [0,85–1,06] |
| Nordeste | 0,66 | 0,58 | 1,15 [1,07–1,23] | 0,65 | 0,62 | 1,04 [0,97–1,11] |
| Sudeste | 0,59 | 0,47 | 1,24 [1,17–1,32] | 0,59 | 0,45 | 1,32 [1,24–1,40] |
| Sul | 0,73 | 0,44 | 1,66 [1,51–1,83] | 0,69 | 0,44 | 1,57 [1,43–1,73] |
| Centro-Oeste | 0,50 | 0,41 | 1,22 [1,07–1,40] | 0,50 | 0,42 | 1,19 [1,04–1,35] |
| Brasil | 0,61 | 0,50 | 1,22 [1,18–1,27] | 0,61 | 0,50 | 1,22 [1,18–1,27] |

### Anomalia congênita (por 10.000 NV)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 126,0 | 60,7 | 2,08 [1,90–2,27] | 187,4 | 67,7 | 2,77 [2,56–3,00] |
| Nordeste | 138,2 | 62,8 | 2,20 [2,08–2,33] | 161,9 | 62,6 | 2,59 [2,45–2,73] |
| Sudeste | 157,5 | 115,5 | 1,36 [1,32–1,41] | 169,9 | 112,3 | 1,51 [1,46–1,57] |
| Sul | 133,9 | 81,9 | 1,64 [1,53–1,75] | 179,7 | 85,3 | 2,11 [1,98–2,24] |
| Centro-Oeste | 98,0 | 81,1 | 1,21 [1,11–1,32] | 96,7 | 90,4 | 1,07 [0,98–1,17] |
| Brasil | 139,8 | 88,7 | 1,58 [1,54–1,61] | 164,9 | 89,6 | 1,84 [1,80–1,89] |

### Parto vaginal assistido por enfermeira/obstetriz (%)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 52,0 | 34,9 | 1,49 [1,47–1,51] | 54,2 | 33,4 | 1,62 [1,60–1,65] |
| Nordeste | 39,5 | 30,0 | 1,32 [1,30–1,33] | 40,6 | 32,5 | 1,25 [1,24–1,27] |
| Sudeste | 37,6 | 14,3 | 2,63 [2,59–2,67] | 38,8 | 14,6 | 2,65 [2,61–2,69] |
| Sul | 8,8 | 3,7 | 2,36 [2,24–2,49] | 7,4 | 4,3 | 1,73 [1,64–1,82] |
| Centro-Oeste | 29,2 | 9,7 | 3,01 [2,89–3,14] | 29,2 | 10,6 | 2,75 [2,64–2,86] |
| Brasil | 35,2 | 20,3 | 1,74 [1,73–1,75] | 35,9 | 20,8 | 1,72 [1,71–1,74] |

### Mãe adolescente < 20 anos (%)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 18,3 | 18,9 | 0,96 [0,95–0,98] | 18,2 | 18,9 | 0,96 [0,95–0,98] |
| Nordeste | 15,1 | 11,5 | 1,31 [1,29–1,33] | 14,8 | 11,3 | 1,31 [1,29–1,33] |
| Sudeste | 11,1 | 6,3 | 1,77 [1,75–1,80] | 11,0 | 6,2 | 1,78 [1,76–1,81] |
| Sul | 9,7 | 6,6 | 1,46 [1,43–1,50] | 9,3 | 6,6 | 1,42 [1,39–1,46] |
| Centro-Oeste | 13,5 | 9,5 | 1,42 [1,39–1,45] | 13,2 | 9,1 | 1,44 [1,41–1,48] |
| Brasil | 13,2 | 9,2 | 1,43 [1,42–1,44] | 13,0 | 9,1 | 1,43 [1,42–1,44] |

### Mãe com 35 anos ou mais (%)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 11,9 | 12,9 | 0,92 [0,90–0,94] | 11,7 | 12,8 | 0,91 [0,89–0,93] |
| Nordeste | 15,1 | 19,1 | 0,79 [0,78–0,80] | 14,9 | 19,1 | 0,78 [0,77–0,79] |
| Sudeste | 16,3 | 25,2 | 0,65 [0,64–0,65] | 16,1 | 25,0 | 0,64 [0,64–0,65] |
| Sul | 17,0 | 22,8 | 0,75 [0,74–0,76] | 16,8 | 22,5 | 0,75 [0,74–0,76] |
| Centro-Oeste | 14,5 | 19,7 | 0,74 [0,73–0,75] | 14,4 | 19,8 | 0,73 [0,72–0,74] |
| Brasil | 15,4 | 21,6 | 0,71 [0,71–0,72] | 15,2 | 21,4 | 0,71 [0,70–0,71] |

### Pré-natal com 7 ou mais consultas (%)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 65,5 | 69,0 | 0,95 [0,95–0,96] | 67,8 | 70,4 | 0,96 [0,96–0,97] |
| Nordeste | 75,9 | 81,9 | 0,93 [0,92–0,93] | 77,1 | 82,3 | 0,94 [0,93–0,94] |
| Sudeste | 80,5 | 85,5 | 0,94 [0,94–0,94] | 81,3 | 85,9 | 0,95 [0,95–0,95] |
| Sul | 84,6 | 87,7 | 0,97 [0,96–0,97] | 86,1 | 88,2 | 0,98 [0,97–0,98] |
| Centro-Oeste | 74,5 | 84,3 | 0,88 [0,88–0,89] | 74,7 | 84,4 | 0,89 [0,88–0,89] |
| Brasil | 77,4 | 83,2 | 0,93 [0,93–0,93] | 78,6 | 83,6 | 0,94 [0,94–0,94] |

### Gestação múltipla (%)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 1,96 | 1,25 | 1,57 [1,47–1,67] | 1,98 | 1,26 | 1,58 [1,49–1,68] |
| Nordeste | 2,51 | 1,26 | 1,99 [1,91–2,07] | 2,44 | 1,24 | 1,97 [1,90–2,05] |
| Sudeste | 2,71 | 2,40 | 1,13 [1,10–1,16] | 2,72 | 2,37 | 1,15 [1,12–1,18] |
| Sul | 2,96 | 1,89 | 1,57 [1,50–1,64] | 3,02 | 1,88 | 1,61 [1,54–1,68] |
| Centro-Oeste | 2,67 | 1,95 | 1,37 [1,29–1,44] | 2,47 | 2,03 | 1,22 [1,15–1,29] |
| Brasil | 2,59 | 1,89 | 1,37 [1,35–1,39] | 2,57 | 1,88 | 1,37 [1,35–1,39] |

### Nascimento em hospital (% dos NV)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] |
|---|---|---|---|---|---|---|
| Norte | 99,9 | 88,7 | 1,13 [1,12–1,13] | 99,9 | 89,1 | 1,12 [1,12–1,12] |
| Nordeste | 99,6 | 95,9 | 1,04 [1,04–1,04] | 99,6 | 95,9 | 1,04 [1,04–1,04] |
| Sudeste | 99,9 | 98,3 | 1,02 [1,02–1,02] | 100,0 | 98,4 | 1,02 [1,02–1,02] |
| Sul | 100,0 | 98,1 | 1,02 [1,02–1,02] | 99,9 | 97,9 | 1,02 [1,02–1,02] |
| Centro-Oeste | 100,0 | 97,6 | 1,02 [1,02–1,03] | 99,9 | 97,5 | 1,02 [1,02–1,03] |
| Brasil | 99,8 | 96,7 | 1,03 [1,03–1,03] | 99,9 | 96,7 | 1,03 [1,03–1,03] |

## 3. Indicadores por local de residência

Indicadores selecionados, calculados pelo município de residência da mãe; recorte adequado para estimar prevalência e incidência na população da região.

### 2024

| Região | Cesariana | Prematuridade < 37 semanas | Baixo peso < 2.500 g | Apgar no 5º minuto < 7 | Anomalia congênita | Mãe adolescente < 20 anos | Pré-natal com 7 ou mais consultas |
|---|---|---|---|---|---|---|---|
| Norte | 54,4 [54,3–54,6] | 12,9 [12,7–13,0] | 8,6 [8,5–8,7] | 9,2 [8,8–9,5] | 100,9 [97,1–104,8] | 18,5 [18,4–18,7] | 67,0 [66,8–67,1] |
| Nordeste | 59,0 [58,9–59,1] | 12,7 [12,6–12,8] | 8,9 [8,9–9,0] | 11,3 [11,0–11,5] | 110,0 [107,5–112,5] | 13,7 [13,7–13,8] | 78,2 [78,1–78,3] |
| Sudeste | 61,2 [61,1–61,3] | 12,2 [12,1–12,3] | 10,1 [10,1–10,2] | 9,9 [9,7–10,1] | 136,2 [133,8–138,6] | 8,8 [8,8–8,9] | 82,9 [82,8–83,0] |
| Sul | 63,1 [63,0–63,3] | 12,0 [11,9–12,1] | 9,4 [9,3–9,5] | 10,8 [10,5–11,2] | 110,5 [107,0–114,1] | 8,3 [8,2–8,3] | 86,0 [85,9–86,1] |
| Centro-Oeste | 66,6 [66,4–66,8] | 12,5 [12,3–12,6] | 9,7 [9,5–9,8] | 9,2 [8,8–9,6] | 90,2 [86,3–94,3] | 11,5 [11,3–11,6] | 79,5 [79,3–79,6] |
| Brasil | 60,6 [60,6–60,7] | 12,4 [12,4–12,4] | 9,5 [9,4–9,5] | 10,3 [10,2–10,4] | 117,1 [115,8–118,5] | 11,4 [11,4–11,5] | 80,0 [79,9–80,0] |

### 2025

| Região | Cesariana | Prematuridade < 37 semanas | Baixo peso < 2.500 g | Apgar no 5º minuto < 7 | Anomalia congênita | Mãe adolescente < 20 anos | Pré-natal com 7 ou mais consultas |
|---|---|---|---|---|---|---|---|
| Norte | 56,3 [56,1–56,5] | 12,6 [12,5–12,7] | 8,3 [8,2–8,4] | 9,5 [9,2–9,9] | 141,3 [137,0–145,8] | 18,5 [18,3–18,6] | 68,8 [68,6–69,0] |
| Nordeste | 60,4 [60,3–60,5] | 12,1 [12,0–12,2] | 8,7 [8,6–8,7] | 11,4 [11,1–11,7] | 125,4 [122,8–128,1] | 13,5 [13,4–13,6] | 79,0 [78,9–79,1] |
| Sudeste | 62,0 [61,9–62,1] | 11,8 [11,7–11,8] | 9,8 [9,8–9,9] | 9,8 [9,6–10,0] | 141,9 [139,5–144,3] | 8,7 [8,7–8,8] | 83,4 [83,4–83,5] |
| Sul | 63,3 [63,2–63,5] | 11,8 [11,7–11,9] | 9,0 [9,0–9,1] | 10,6 [10,3–11,0] | 138,1 [134,3–142,0] | 8,1 [8,0–8,2] | 87,0 [86,9–87,1] |
| Centro-Oeste | 66,7 [66,5–66,9] | 12,0 [11,9–12,2] | 9,3 [9,2–9,4] | 8,8 [8,4–9,2] | 94,7 [90,8–98,8] | 11,1 [11,0–11,3] | 79,5 [79,3–79,7] |
| Brasil | 61,5 [61,5–61,6] | 12,0 [11,9–12,0] | 9,2 [9,1–9,2] | 10,2 [10,1–10,4] | 132,4 [130,9–133,8] | 11,3 [11,2–11,3] | 80,8 [80,7–80,8] |

## 4. Taxa de cesariana bruta e padronizada pelos grupos de Robson

Padronização direta, com pesos dados pela distribuição dos grupos de Robson no Brasil (local de ocorrência, 2024). A padronização remove da comparação o efeito das diferenças de perfil obstétrico.

| Região | 2024 painel bruta | 2024 painel padronizada | 2024 demais bruta | 2024 demais padronizada | 2025 painel bruta | 2025 painel padronizada | 2025 demais bruta | 2025 demais padronizada |
|---|---|---|---|---|---|---|---|---|
| Norte | 54,0 | 58,9 | 55,0 | 62,1 | 56,3 | 60,9 | 56,2 | 63,0 |
| Nordeste | 56,8 | 59,5 | 62,6 | 65,9 | 58,2 | 60,7 | 64,1 | 66,6 |
| Sudeste | 50,5 | 50,8 | 73,0 | 68,2 | 51,7 | 51,6 | 73,7 | 68,6 |
| Sul | 54,1 | 51,7 | 73,7 | 67,0 | 55,2 | 52,3 | 73,5 | 66,7 |
| Centro-Oeste | 55,4 | 57,0 | 77,6 | 73,7 | 55,4 | 56,5 | 78,1 | 74,1 |
| Brasil | 53,8 | 55,2 | 69,2 | 67,3 | 55,0 | 56,1 | 70,0 | 67,7 |

### Cesariana por grupo de Robson, Brasil, 2025: unidades do painel e demais estabelecimentos

| Grupo | % dos NV (painel) | % dos NV (demais) | % cesariana (painel) | % cesariana (demais) | contribuição em p.p. (painel) | contribuição em p.p. (demais) |
|---|---|---|---|---|---|---|
| 1 | 15,8 | 15,0 | 38,6 | 55,8 | 6,1 | 8,4 |
| 2 | 13,8 | 17,9 | 67,2 | 87,1 | 9,3 | 15,6 |
| 3 | 19,1 | 15,8 | 18,2 | 23,9 | 3,5 | 3,8 |
| 4 | 11,1 | 9,1 | 47,7 | 72,2 | 5,3 | 6,6 |
| 5 | 22,5 | 26,8 | 84,4 | 91,2 | 19,0 | 24,4 |
| 6 | 1,3 | 1,5 | 92,1 | 94,3 | 1,2 | 1,4 |
| 7 | 2,0 | 1,9 | 90,3 | 89,4 | 1,8 | 1,7 |
| 8 | 2,5 | 1,8 | 87,7 | 90,0 | 2,2 | 1,7 |
| 9 | 0,2 | 0,2 | 96,9 | 97,5 | 0,2 | 0,2 |
| 10 | 10,7 | 8,1 | 55,1 | 64,0 | 5,9 | 5,2 |
| não classificado | 1,1 | 2,0 | 57,9 | 58,6 | 0,6 | 1,2 |

## 5. Mortalidade (SIM): unidades do painel, demais estabelecimentos e residência

Óbitos registrados no SIM (DO de todas as UFs e DOFET), segundo as regras auditadas no processamento da mortalidade (fichas IDB C.1.4, C.1.1, C.1.2, C.2 e C.3; óbito materno pela regra do MS/OOBr). Nos recortes painel e demais estab., o numerador é o óbito ocorrido no estabelecimento (CODESTAB) e o denominador são os NV nascidos no mesmo estabelecimento. Maternidades com UTI neonatal de referência recebem recém-nascidos (RN) de outros serviços, e a DO não informa o local de nascimento; por isso, a razão painel/demais superestima a mortalidade nas unidades do painel. A coluna residência (óbitos de residentes ÷ NV de residentes) corresponde à taxa populacional da região e não está sujeita a esse viés.

### Mortalidade neonatal 0–27 dias (por 1.000 NV)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2024 residência [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] | 2025 residência [IC] |
|---|---|---|---|---|---|---|---|---|
| Norte | 10,35 | 9,30 | 1,11 [1,03–1,20] | 10,02 [9,65–10,41] | 10,75 | 9,08 | 1,18 [1,10–1,28] | 10,15 [9,79–10,53] |
| Nordeste | 11,36 | 5,68 | 2,00 [1,88–2,12] | 9,20 [8,98–9,43] | 10,79 | 5,82 | 1,85 [1,75–1,97] | 8,95 [8,73–9,18] |
| Sudeste | 9,33 | 6,36 | 1,47 [1,40–1,54] | 7,86 [7,68–8,05] | 9,08 | 6,32 | 1,44 [1,37–1,51] | 7,75 [7,57–7,93] |
| Sul | 9,09 | 5,11 | 1,78 [1,64–1,94] | 7,27 [6,99–7,57] | 9,18 | 4,71 | 1,95 [1,79–2,12] | 7,19 [6,92–7,48] |
| Centro-Oeste | 9,99 | 6,31 | 1,58 [1,44–1,74] | 8,13 [7,76–8,51] | 9,68 | 6,31 | 1,54 [1,40–1,69] | 8,05 [7,69–8,43] |
| Brasil | 10,10 | 6,31 | 1,60 [1,55–1,65] | 8,42 [8,30–8,53] | 9,87 | 6,24 | 1,58 [1,53–1,63] | 8,30 [8,19–8,41] |

### Mortalidade neonatal precoce 0–6 dias (por 1.000 NV)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2024 residência [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] | 2025 residência [IC] |
|---|---|---|---|---|---|---|---|---|
| Norte | 8,24 | 7,12 | 1,16 [1,06–1,26] | 7,85 [7,52–8,19] | 8,29 | 6,45 | 1,29 [1,18–1,41] | 7,60 [7,28–7,93] |
| Nordeste | 8,71 | 4,08 | 2,14 [2,00–2,29] | 6,95 [6,76–7,15] | 8,22 | 4,12 | 2,00 [1,86–2,14] | 6,70 [6,51–6,90] |
| Sudeste | 6,84 | 4,48 | 1,53 [1,44–1,61] | 5,68 [5,53–5,84] | 6,58 | 4,42 | 1,49 [1,41–1,57] | 5,55 [5,40–5,70] |
| Sul | 6,70 | 3,62 | 1,85 [1,67–2,04] | 5,29 [5,05–5,54] | 6,81 | 3,45 | 1,97 [1,79–2,18] | 5,32 [5,08–5,56] |
| Centro-Oeste | 7,54 | 4,50 | 1,68 [1,50–1,87] | 5,98 [5,66–6,31] | 7,50 | 4,47 | 1,68 [1,50–1,88] | 6,02 [5,70–6,35] |
| Brasil | 7,62 | 4,53 | 1,68 [1,63–1,74] | 6,25 [6,15–6,35] | 7,39 | 4,42 | 1,67 [1,62–1,73] | 6,11 [6,01–6,21] |

### Mortalidade neonatal tardia 7–27 dias (por 1.000 NV)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2024 residência [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] | 2025 residência [IC] |
|---|---|---|---|---|---|---|---|---|
| Norte | 2,11 | 2,18 | 0,97 [0,82–1,14] | 2,18 [2,01–2,36] | 2,46 | 2,63 | 0,93 [0,80–1,09] | 2,55 [2,37–2,75] |
| Nordeste | 2,65 | 1,61 | 1,65 [1,47–1,84] | 2,25 [2,14–2,37] | 2,57 | 1,70 | 1,51 [1,35–1,69] | 2,26 [2,15–2,37] |
| Sudeste | 2,49 | 1,88 | 1,32 [1,21–1,45] | 2,18 [2,08–2,28] | 2,50 | 1,90 | 1,32 [1,21–1,44] | 2,20 [2,10–2,29] |
| Sul | 2,38 | 1,48 | 1,61 [1,37–1,89] | 1,98 [1,84–2,14] | 2,37 | 1,26 | 1,88 [1,59–2,22] | 1,88 [1,74–2,03] |
| Centro-Oeste | 2,45 | 1,81 | 1,35 [1,13–1,63] | 2,15 [1,96–2,35] | 2,18 | 1,84 | 1,19 [0,98–1,43] | 2,04 [1,86–2,23] |
| Brasil | 2,48 | 1,78 | 1,39 [1,31–1,47] | 2,17 [2,11–2,23] | 2,47 | 1,83 | 1,35 [1,28–1,43] | 2,19 [2,13–2,25] |

### Mortalidade infantil < 1 ano (por 1.000 NV)

Só por residência: o óbito infantil raramente ocorre no estabelecimento do nascimento.

| Região | 2024 residência [IC] | 2025 residência [IC] |
|---|---|---|
| Norte | 15,65 [15,18–16,13] | 15,21 [14,76–15,68] |
| Nordeste | 13,52 [13,24–13,80] | 13,09 [12,83–13,37] |
| Sudeste | 11,71 [11,49–11,93] | 11,37 [11,16–11,59] |
| Sul | 10,40 [10,07–10,75] | 10,04 [9,71–10,37] |
| Centro-Oeste | 12,62 [12,15–13,10] | 12,18 [11,73–12,64] |
| Brasil | 12,55 [12,41–12,69] | 12,16 [12,03–12,30] |

### Mortalidade fetal ≥ 22 semanas ou ≥ 500 g (por 1.000 nascimentos)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2024 residência [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] | 2025 residência [IC] |
|---|---|---|---|---|---|---|---|---|
| Norte | 11,12 | 10,08 | 1,10 [1,02–1,19] | 10,74 [10,36–11,14] | 11,17 | 10,43 | 1,07 [1,00–1,15] | 10,92 [10,54–11,31] |
| Nordeste | 12,01 | 7,54 | 1,59 [1,51–1,68] | 10,29 [10,05–10,53] | 11,90 | 7,50 | 1,59 [1,51–1,67] | 10,27 [10,03–10,51] |
| Sudeste | 9,83 | 6,95 | 1,42 [1,35–1,48] | 8,45 [8,27–8,64] | 9,64 | 6,88 | 1,40 [1,34–1,47] | 8,33 [8,15–8,52] |
| Sul | 8,25 | 5,55 | 1,49 [1,37–1,62] | 7,01 [6,73–7,29] | 7,85 | 5,08 | 1,55 [1,42–1,68] | 6,63 [6,36–6,90] |
| Centro-Oeste | 10,89 | 6,77 | 1,61 [1,47–1,76] | 8,83 [8,45–9,23] | 10,64 | 6,48 | 1,64 [1,50–1,80] | 8,62 [8,25–9,01] |
| Brasil | 10,53 | 7,19 | 1,47 [1,43–1,51] | 9,05 [8,93–9,17] | 10,35 | 7,09 | 1,46 [1,42–1,50] | 8,94 [8,83–9,06] |

### Mortalidade perinatal: fetais + 0–6 dias (por 1.000 nascimentos)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2024 residência [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] | 2025 residência [IC] |
|---|---|---|---|---|---|---|---|---|
| Norte | 19,27 | 17,13 | 1,12 [1,06–1,19] | 18,51 [18,00–19,02] | 19,37 | 16,81 | 1,15 [1,09–1,22] | 18,44 [17,95–18,95] |
| Nordeste | 20,62 | 11,58 | 1,78 [1,71–1,86] | 17,17 [16,86–17,48] | 20,03 | 11,59 | 1,73 [1,66–1,80] | 16,90 [16,60–17,20] |
| Sudeste | 16,60 | 11,40 | 1,46 [1,41–1,51] | 14,09 [13,85–14,33] | 16,15 | 11,27 | 1,43 [1,38–1,48] | 13,83 [13,60–14,07] |
| Sul | 14,89 | 9,15 | 1,63 [1,53–1,73] | 12,26 [11,89–12,63] | 14,61 | 8,51 | 1,72 [1,61–1,83] | 11,91 [11,56–12,27] |
| Centro-Oeste | 18,35 | 11,24 | 1,63 [1,52–1,75] | 14,75 [14,26–15,27] | 18,06 | 10,92 | 1,65 [1,54–1,77] | 14,58 [14,10–15,09] |
| Brasil | 18,07 | 11,68 | 1,55 [1,51–1,58] | 15,24 [15,09–15,40] | 17,67 | 11,48 | 1,54 [1,51–1,57] | 15,00 [14,85–15,15] |

### Razão de mortalidade materna (por 100.000 NV)

| Região | 2024 painel | 2024 demais estab. | 2024 razão painel/demais [IC] | 2024 residência [IC] | 2025 painel | 2025 demais estab. | 2025 razão painel/demais [IC] | 2025 residência [IC] |
|---|---|---|---|---|---|---|---|---|
| Norte | 44,3 | 98,7 | 0,45 [0,33–0,61] | 67,0 [57,9–77,6] | 52,2 | 92,9 | 0,56 [0,42–0,75] | 68,2 [59,1–78,6] |
| Nordeste | 55,4 | 64,9 | 0,85 [0,70–1,04] | 58,9 [53,4–65,0] | 50,9 | 70,2 | 0,73 [0,60–0,88] | 58,2 [52,8–64,3] |
| Sudeste | 50,2 | 49,3 | 1,02 [0,85–1,22] | 49,8 [45,4–54,6] | 46,0 | 45,3 | 1,02 [0,84–1,23] | 45,8 [41,6–50,4] |
| Sul | 58,9 | 46,4 | 1,27 [0,94–1,71] | 53,1 [45,9–61,5] | 34,8 | 41,7 | 0,83 [0,59–1,17] | 37,5 [31,7–44,5] |
| Centro-Oeste | 59,9 | 58,0 | 1,03 [0,73–1,46] | 58,5 [49,1–69,6] | 42,5 | 45,9 | 0,93 [0,62–1,37] | 43,8 [35,9–53,4] |
| Brasil | 53,1 | 58,5 | 0,91 [0,81–1,01] | 55,5 [52,6–58,6] | 46,4 | 55,6 | 0,83 [0,75–0,93] | 50,4 [47,7–53,3] |

Número de óbitos (Brasil, por local de ocorrência):

| Ano | Neonatais (0–27 dias) | Neonatais precoces (0–6 dias) | Neonatais tardios (7–27 dias) | Infantis (< 1 ano) | Fetais (≥ 22 semanas ou ≥ 500 g) | Fetais sem IG e sem peso | Maternos (regra MS/OOBr) | Maternos tardios (O96–O97) |
|---|---|---|---|---|---|---|---|---|
| 2024 | 20.113 | 14.933 | 5.180 | 29.984 | 21.824 | 522 | 1.326 | 258 |
| 2025 | 20.391 | 15.005 | 5.386 | 29.881 | 22.168 | 529 | 1.238 | 223 |

## 6. Interpretação e limitações

- As unidades do painel são maternidades de maior porte (mais de 1.000 partos pelo SUS no ano) e, em grande parte, referência para alto risco; concentram prematuridade, baixo peso, Apgar baixo, anomalias e, por consequência, óbitos neonatais da região. Nesses indicadores, razão > 1 reflete principalmente a seleção de casos e as transferências e não deve ser lida como medida de qualidade assistencial.
- O recorte "demais estabelecimentos" reúne hospitais privados sem atendimento pelo SUS, hospitais do SUS com até 1.000 partos no ano e partos fora de hospital; é, portanto, um grupo heterogêneo.
- Os recortes por residência e por ocorrência divergem onde há deslocamento de gestantes para o parto (Norte, interior do Nordeste e entorno do DF). Para prevalência e incidência populacionais, devem ser usadas as colunas de residência.
- Os dados de 2025 são preliminares (SINASC de 31/08/2026; SIM preliminar). O número de óbitos, em especial os maternos, ainda aumenta com a investigação e com a inclusão tardia de registros. Registros com Apgar, peso ou idade gestacional ignorados foram excluídos dos denominadores; óbitos fetais sem IG e sem peso foram excluídos do numerador e do denominador (quantidade na tabela de número de óbitos, acima).
- Taxas com denominador populacional (por 100.000 mulheres ou por 1.000 mulheres em idade fértil) dependem de estimativas populacionais do IBGE e não foram calculadas.

Planilha completa (abas Cobertura, Por região, Por UF, Robson, Pesos Robson, Diagnóstico SIM): `planilhas/COMPARACAO_REGIONAL_2024_2025.xlsx`.
