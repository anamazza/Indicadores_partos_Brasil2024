# Comparação regional — unidades do painel × conjunto da região (2024 e 2025)

Protótipo gerado por `scripts/extracao/regional.py` e `scripts/extracao/relatorio_regional.py` a partir do SINASC completo (todos os estabelecimentos). **Unidades do painel** = CNES da planilha do ano (mais os CNES antigos/complexos que o painel soma), por UF de ocorrência. **Região** = todos os nascidos vivos ocorridos na região, em qualquer estabelecimento ou domicílio. **Residência** = nascidos vivos de mães residentes na região, onde quer que tenham nascido (prevalência populacional). IC 95 % de Wilson para as proporções; a razão painel/região usa o IC pelo logaritmo.

- **2024:** 2.389.325 NV no `SINASC_2024_csv.zip`; lista do painel `ESTABELECIMENTOS_ACIMA_DE_1000_PARTOS_2024__INDICADORES_01072026.xlsx` (544 CNES com apelidos).
- **2025:** 2.456.688 NV no `SINASC_2025_csv.zip`; lista do painel `PLANILHA_2025_prelim_internacao.xlsx` (558 CNES com apelidos).

## 1. Cobertura: quanto dos nascimentos da região acontece nas unidades do painel

| Região | 2024 NV painel | 2024 NV região | 2024 cobertura | 2025 NV painel | 2025 NV região | 2025 cobertura |
|---|---|---|---|---|---|---|
| Norte | 157.861 | 265.246 | 59,5 % | 166.532 | 275.281 | 60,5 % |
| Nordeste | 411.612 | 667.247 | 61,7 % | 428.116 | 681.767 | 62,8 % |
| Sudeste | 472.382 | 904.600 | 52,2 % | 491.473 | 924.170 | 53,2 % |
| Sul | 181.613 | 336.732 | 53,9 % | 195.578 | 351.580 | 55,6 % |
| Centro-Oeste | 106.793 | 215.500 | 49,6 % | 112.896 | 223.890 | 50,4 % |
| Brasil | 1.330.261 | 2.389.325 | 55,7 % | 1.394.595 | 2.456.688 | 56,8 % |

## 2. Indicadores por região: painel × região (ocorrência) e razão

Valor do painel, valor da região e razão painel/região [IC 95 %]. Razão > 1: o indicador é mais frequente nas unidades do painel do que no conjunto da região.

### Cesárea (% dos partos)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 54,0 | 54,4 | 0,99 [0,99–1,00] | 56,3 | 56,3 | 1,00 [1,00–1,01] |
| Nordeste | 56,8 | 59,0 | 0,96 [0,96–0,97] | 58,2 | 60,4 | 0,96 [0,96–0,97] |
| Sudeste | 50,5 | 61,3 | 0,82 [0,82–0,83] | 51,7 | 62,0 | 0,83 [0,83–0,84] |
| Sul | 54,1 | 63,1 | 0,86 [0,85–0,86] | 55,2 | 63,3 | 0,87 [0,87–0,88] |
| Centro-Oeste | 55,4 | 66,6 | 0,83 [0,83–0,84] | 55,4 | 66,7 | 0,83 [0,83–0,84] |
| Brasil | 53,8 | 60,6 | 0,89 [0,89–0,89] | 55,0 | 61,5 | 0,89 [0,89–0,90] |

### Prematuridade < 37 semanas (% dos NV)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 13,6 | 12,8 | 1,06 [1,04–1,07] | 13,3 | 12,6 | 1,06 [1,04–1,07] |
| Nordeste | 14,6 | 12,7 | 1,15 [1,14–1,16] | 13,8 | 12,1 | 1,14 [1,13–1,15] |
| Sudeste | 13,3 | 12,2 | 1,09 [1,08–1,10] | 12,9 | 11,8 | 1,09 [1,08–1,10] |
| Sul | 13,9 | 12,0 | 1,16 [1,14–1,17] | 13,8 | 11,8 | 1,17 [1,15–1,18] |
| Centro-Oeste | 14,5 | 12,5 | 1,16 [1,13–1,18] | 13,9 | 12,1 | 1,15 [1,13–1,17] |
| Brasil | 13,9 | 12,4 | 1,12 [1,11–1,13] | 13,4 | 12,0 | 1,12 [1,11–1,13] |

### Baixo peso < 2.500 g (% dos NV)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 9,4 | 8,6 | 1,10 [1,08–1,12] | 9,3 | 8,3 | 1,12 [1,10–1,14] |
| Nordeste | 10,8 | 8,9 | 1,21 [1,19–1,22] | 10,3 | 8,7 | 1,19 [1,17–1,20] |
| Sudeste | 11,5 | 10,1 | 1,14 [1,13–1,15] | 11,2 | 9,8 | 1,14 [1,13–1,15] |
| Sul | 11,3 | 9,4 | 1,20 [1,18–1,22] | 10,9 | 9,0 | 1,21 [1,19–1,23] |
| Centro-Oeste | 11,8 | 9,7 | 1,21 [1,19–1,24] | 11,2 | 9,3 | 1,20 [1,18–1,23] |
| Brasil | 11,0 | 9,5 | 1,17 [1,16–1,17] | 10,6 | 9,2 | 1,16 [1,15–1,17] |

### Muito baixo peso < 1.500 g (por 1.000 NV)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 15,1 | 12,9 | 1,17 [1,11–1,24] | 15,3 | 12,8 | 1,19 [1,13–1,25] |
| Nordeste | 18,3 | 14,5 | 1,26 [1,22–1,30] | 17,0 | 13,9 | 1,22 [1,19–1,26] |
| Sudeste | 19,0 | 15,9 | 1,19 [1,16–1,23] | 18,2 | 15,2 | 1,20 [1,16–1,23] |
| Sul | 18,4 | 14,1 | 1,30 [1,25–1,36] | 17,7 | 13,6 | 1,30 [1,25–1,36] |
| Centro-Oeste | 19,1 | 14,0 | 1,37 [1,30–1,45] | 18,2 | 13,9 | 1,31 [1,24–1,39] |
| Brasil | 18,2 | 14,7 | 1,24 [1,22–1,26] | 17,4 | 14,2 | 1,22 [1,20–1,24] |

### Apgar 5º min < 7 (por 1.000 NV com Apgar informado)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 8,9 | 9,1 | 0,98 [0,92–1,04] | 9,8 | 9,5 | 1,03 [0,97–1,10] |
| Nordeste | 12,7 | 11,3 | 1,13 [1,09–1,17] | 12,4 | 11,4 | 1,09 [1,05–1,13] |
| Sudeste | 11,5 | 9,9 | 1,15 [1,12–1,19] | 11,2 | 9,8 | 1,15 [1,11–1,18] |
| Sul | 13,6 | 10,8 | 1,26 [1,19–1,32] | 13,3 | 10,6 | 1,25 [1,19–1,31] |
| Centro-Oeste | 11,2 | 9,2 | 1,22 [1,13–1,31] | 10,2 | 8,7 | 1,17 [1,09–1,25] |
| Brasil | 11,8 | 10,3 | 1,15 [1,13–1,17] | 11,6 | 10,2 | 1,14 [1,11–1,16] |

### Asfixia, regra do painel: Apgar < 7 em NV ≥ 2.500 g sem anomalia (%)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 0,47 | 0,52 | 0,91 [0,83–1,00] | 0,54 | 0,56 | 0,98 [0,90–1,07] |
| Nordeste | 0,66 | 0,63 | 1,05 [1,00–1,11] | 0,65 | 0,64 | 1,01 [0,96–1,07] |
| Sudeste | 0,59 | 0,53 | 1,10 [1,05–1,16] | 0,59 | 0,53 | 1,13 [1,08–1,19] |
| Sul | 0,73 | 0,59 | 1,23 [1,14–1,33] | 0,69 | 0,58 | 1,20 [1,11–1,29] |
| Centro-Oeste | 0,50 | 0,45 | 1,10 [0,99–1,23] | 0,50 | 0,46 | 1,09 [0,97–1,21] |
| Brasil | 0,61 | 0,56 | 1,09 [1,06–1,12] | 0,61 | 0,56 | 1,09 [1,06–1,12] |

### Anomalia congênita (por 10.000 NV)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 126,0 | 99,1 | 1,27 [1,20–1,35] | 187,4 | 140,1 | 1,34 [1,28–1,40] |
| Nordeste | 138,2 | 109,5 | 1,26 [1,22–1,31] | 161,9 | 125,1 | 1,29 [1,25–1,34] |
| Sudeste | 157,5 | 137,4 | 1,15 [1,11–1,18] | 169,9 | 142,9 | 1,19 [1,16–1,22] |
| Sul | 133,9 | 109,9 | 1,22 [1,16–1,28] | 179,7 | 137,8 | 1,30 [1,25–1,36] |
| Centro-Oeste | 98,0 | 89,5 | 1,09 [1,02–1,18] | 96,7 | 93,6 | 1,03 [0,96–1,11] |
| Brasil | 139,8 | 117,1 | 1,19 [1,17–1,22] | 164,9 | 132,4 | 1,25 [1,23–1,27] |

### Parto vaginal assistido por enfermeira/obstetriz (%)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 52,0 | 45,2 | 1,15 [1,14–1,16] | 54,2 | 46,0 | 1,18 [1,17–1,19] |
| Nordeste | 39,5 | 36,2 | 1,09 [1,08–1,10] | 40,6 | 37,9 | 1,07 [1,06–1,08] |
| Sudeste | 37,6 | 29,8 | 1,26 [1,25–1,27] | 38,8 | 30,9 | 1,25 [1,24–1,26] |
| Sul | 8,8 | 7,1 | 1,23 [1,19–1,27] | 7,4 | 6,4 | 1,16 [1,12–1,19] |
| Centro-Oeste | 29,2 | 22,7 | 1,29 [1,26–1,31] | 29,2 | 23,2 | 1,26 [1,23–1,28] |
| Brasil | 35,2 | 30,1 | 1,17 [1,17–1,18] | 35,9 | 30,9 | 1,16 [1,16–1,17] |

### Mãe adolescente < 20 anos (%)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 18,3 | 18,5 | 0,99 [0,97–1,00] | 18,2 | 18,5 | 0,99 [0,97–1,00] |
| Nordeste | 15,1 | 13,7 | 1,10 [1,09–1,11] | 14,8 | 13,5 | 1,10 [1,09–1,11] |
| Sudeste | 11,1 | 8,8 | 1,26 [1,25–1,28] | 11,0 | 8,7 | 1,26 [1,25–1,27] |
| Sul | 9,7 | 8,3 | 1,17 [1,15–1,19] | 9,3 | 8,1 | 1,15 [1,13–1,17] |
| Centro-Oeste | 13,5 | 11,5 | 1,18 [1,15–1,20] | 13,2 | 11,2 | 1,18 [1,16–1,20] |
| Brasil | 13,2 | 11,4 | 1,15 [1,15–1,16] | 13,0 | 11,3 | 1,15 [1,14–1,16] |

### Mãe com 35 anos ou mais (%)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 11,9 | 12,3 | 0,97 [0,95–0,98] | 11,7 | 12,2 | 0,96 [0,95–0,98] |
| Nordeste | 15,1 | 16,6 | 0,91 [0,90–0,92] | 14,9 | 16,5 | 0,90 [0,90–0,91] |
| Sudeste | 16,3 | 20,6 | 0,79 [0,79–0,80] | 16,1 | 20,3 | 0,79 [0,79–0,80] |
| Sul | 17,0 | 19,7 | 0,86 [0,85–0,88] | 16,8 | 19,3 | 0,87 [0,86–0,88] |
| Centro-Oeste | 14,5 | 17,1 | 0,85 [0,83–0,86] | 14,4 | 17,1 | 0,84 [0,83–0,86] |
| Brasil | 15,4 | 18,1 | 0,85 [0,84–0,85] | 15,2 | 17,9 | 0,85 [0,84–0,85] |

### Pré-natal com 7 ou mais consultas (%)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 65,5 | 66,9 | 0,98 [0,97–0,98] | 67,8 | 68,8 | 0,98 [0,98–0,99] |
| Nordeste | 75,9 | 78,2 | 0,97 [0,97–0,97] | 77,1 | 79,0 | 0,98 [0,97–0,98] |
| Sudeste | 80,5 | 82,9 | 0,97 [0,97–0,97] | 81,3 | 83,4 | 0,97 [0,97–0,98] |
| Sul | 84,6 | 86,0 | 0,98 [0,98–0,99] | 86,1 | 87,0 | 0,99 [0,99–0,99] |
| Centro-Oeste | 74,5 | 79,4 | 0,94 [0,93–0,94] | 74,7 | 79,5 | 0,94 [0,94–0,94] |
| Brasil | 77,4 | 80,0 | 0,97 [0,97–0,97] | 78,6 | 80,8 | 0,97 [0,97–0,97] |

### Gestação múltipla (%)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 1,96 | 1,67 | 1,17 [1,12–1,23] | 1,98 | 1,70 | 1,17 [1,12–1,22] |
| Nordeste | 2,51 | 2,03 | 1,23 [1,20–1,27] | 2,44 | 1,99 | 1,22 [1,19–1,26] |
| Sudeste | 2,71 | 2,56 | 1,06 [1,03–1,08] | 2,72 | 2,56 | 1,07 [1,04–1,09] |
| Sul | 2,96 | 2,47 | 1,20 [1,16–1,24] | 3,02 | 2,51 | 1,20 [1,16–1,24] |
| Centro-Oeste | 2,67 | 2,31 | 1,16 [1,11–1,21] | 2,47 | 2,25 | 1,10 [1,05–1,15] |
| Brasil | 2,59 | 2,28 | 1,14 [1,12–1,15] | 2,57 | 2,27 | 1,13 [1,12–1,15] |

### Nascimento em hospital (% dos NV)

| Região | 2024 painel | 2024 região | 2024 razão [IC] | 2025 painel | 2025 região | 2025 razão [IC] |
|---|---|---|---|---|---|---|
| Norte | 99,9 | 95,4 | 1,05 [1,05–1,05] | 99,9 | 95,7 | 1,04 [1,04–1,05] |
| Nordeste | 99,6 | 98,2 | 1,01 [1,01–1,01] | 99,6 | 98,2 | 1,01 [1,01–1,01] |
| Sudeste | 99,9 | 99,2 | 1,01 [1,01–1,01] | 100,0 | 99,2 | 1,01 [1,01–1,01] |
| Sul | 100,0 | 99,1 | 1,01 [1,01–1,01] | 99,9 | 99,0 | 1,01 [1,01–1,01] |
| Centro-Oeste | 100,0 | 98,8 | 1,01 [1,01–1,01] | 99,9 | 98,7 | 1,01 [1,01–1,01] |
| Brasil | 99,8 | 98,4 | 1,01 [1,01–1,01] | 99,9 | 98,5 | 1,01 [1,01–1,01] |

## 3. Prevalência por residência (toda a população da região)

Mesmos indicadores pelo local de residência da mãe — é o denominador correto para falar de prevalência/incidência na população da região.

**2024**

| Região | Cesárea | Prematuridade < 37 semanas | Baixo peso < 2.500 g | Apgar 5º min < 7 | Anomalia congênita | Mãe adolescente < 20 anos | Pré-natal com 7 ou mais consultas |
|---|---|---|---|---|---|---|---|
| Norte | 54,4 [54,3–54,6] | 12,9 [12,7–13,0] | 8,6 [8,5–8,7] | 9,2 [8,8–9,5] | 100,9 [97,1–104,8] | 18,5 [18,4–18,7] | 67,0 [66,8–67,1] |
| Nordeste | 59,0 [58,9–59,1] | 12,7 [12,6–12,8] | 8,9 [8,9–9,0] | 11,3 [11,0–11,5] | 110,0 [107,5–112,5] | 13,7 [13,7–13,8] | 78,2 [78,1–78,3] |
| Sudeste | 61,2 [61,1–61,3] | 12,2 [12,1–12,3] | 10,1 [10,1–10,2] | 9,9 [9,7–10,1] | 136,2 [133,8–138,6] | 8,8 [8,8–8,9] | 82,9 [82,8–83,0] |
| Sul | 63,1 [63,0–63,3] | 12,0 [11,9–12,1] | 9,4 [9,3–9,5] | 10,8 [10,5–11,2] | 110,5 [107,0–114,1] | 8,3 [8,2–8,3] | 86,0 [85,9–86,1] |
| Centro-Oeste | 66,6 [66,4–66,8] | 12,5 [12,3–12,6] | 9,7 [9,5–9,8] | 9,2 [8,8–9,6] | 90,2 [86,3–94,3] | 11,5 [11,3–11,6] | 79,5 [79,3–79,6] |
| Brasil | 60,6 [60,6–60,7] | 12,4 [12,4–12,4] | 9,5 [9,4–9,5] | 10,3 [10,2–10,4] | 117,1 [115,8–118,5] | 11,4 [11,4–11,5] | 80,0 [79,9–80,0] |

**2025**

| Região | Cesárea | Prematuridade < 37 semanas | Baixo peso < 2.500 g | Apgar 5º min < 7 | Anomalia congênita | Mãe adolescente < 20 anos | Pré-natal com 7 ou mais consultas |
|---|---|---|---|---|---|---|---|
| Norte | 56,3 [56,1–56,5] | 12,6 [12,5–12,7] | 8,3 [8,2–8,4] | 9,5 [9,2–9,9] | 141,3 [137,0–145,8] | 18,5 [18,3–18,6] | 68,8 [68,6–69,0] |
| Nordeste | 60,4 [60,3–60,5] | 12,1 [12,0–12,2] | 8,7 [8,6–8,7] | 11,4 [11,1–11,7] | 125,4 [122,8–128,1] | 13,5 [13,4–13,6] | 79,0 [78,9–79,1] |
| Sudeste | 62,0 [61,9–62,1] | 11,8 [11,7–11,8] | 9,8 [9,8–9,9] | 9,8 [9,6–10,0] | 141,9 [139,5–144,3] | 8,7 [8,7–8,8] | 83,4 [83,4–83,5] |
| Sul | 63,3 [63,2–63,5] | 11,8 [11,7–11,9] | 9,0 [9,0–9,1] | 10,6 [10,3–11,0] | 138,1 [134,3–142,0] | 8,1 [8,0–8,2] | 87,0 [86,9–87,1] |
| Centro-Oeste | 66,7 [66,5–66,9] | 12,0 [11,9–12,2] | 9,3 [9,2–9,4] | 8,8 [8,4–9,2] | 94,7 [90,8–98,8] | 11,1 [11,0–11,3] | 79,5 [79,3–79,7] |
| Brasil | 61,5 [61,5–61,6] | 12,0 [11,9–12,0] | 9,2 [9,1–9,2] | 10,2 [10,1–10,4] | 132,4 [130,9–133,8] | 11,3 [11,2–11,3] | 80,8 [80,7–80,8] |

## 4. Cesárea: bruta × padronizada pela distribuição de Robson

Padronização direta: taxa de cesárea de cada grupo de Robson do território, ponderada pela distribuição dos grupos no Brasil (ocorrência, 2024). Remove o efeito do perfil obstétrico (mais cesárea anterior, mais indução etc.) na comparação.

| Região | 2024 painel bruta | 2024 painel padron. | 2024 região bruta | 2024 região padron. | 2025 painel bruta | 2025 painel padron. | 2025 região bruta | 2025 região padron. |
|---|---|---|---|---|---|---|---|---|
| Norte | 54,0 | 58,9 | 54,4 | 60,1 | 56,3 | 60,9 | 56,3 | 61,6 |
| Nordeste | 56,8 | 59,5 | 59,0 | 62,1 | 58,2 | 60,7 | 60,4 | 63,0 |
| Sudeste | 50,5 | 50,8 | 61,3 | 59,0 | 51,7 | 51,6 | 62,0 | 59,4 |
| Sul | 54,1 | 51,7 | 63,1 | 58,6 | 55,2 | 52,3 | 63,3 | 58,7 |
| Centro-Oeste | 55,4 | 57,0 | 66,6 | 65,2 | 55,4 | 56,5 | 66,7 | 64,9 |
| Brasil | 53,8 | 55,2 | 60,6 | 60,6 | 55,0 | 56,1 | 61,5 | 61,1 |

### Cesárea por grupo de Robson, Brasil 2025: painel × região

| Grupo | % dos NV (painel) | % dos NV (região) | % cesárea (painel) | % cesárea (região) | contribuição p.p. (painel) | contribuição p.p. (região) |
|---|---|---|---|---|---|---|
| 1 | 15,8 | 15,4 | 38,6 | 45,8 | 6,1 | 7,1 |
| 2 | 13,8 | 15,5 | 67,2 | 77,1 | 9,3 | 12,0 |
| 3 | 19,1 | 17,6 | 18,2 | 20,4 | 3,5 | 3,6 |
| 4 | 11,1 | 10,2 | 47,7 | 57,1 | 5,3 | 5,8 |
| 5 | 22,5 | 24,4 | 84,4 | 87,6 | 19,0 | 21,4 |
| 6 | 1,3 | 1,4 | 92,1 | 93,1 | 1,2 | 1,3 |
| 7 | 2,0 | 2,0 | 90,3 | 89,9 | 1,8 | 1,8 |
| 8 | 2,5 | 2,2 | 87,7 | 88,5 | 2,2 | 2,0 |
| 9 | 0,2 | 0,2 | 96,9 | 97,2 | 0,2 | 0,2 |
| 10 | 10,7 | 9,6 | 55,1 | 58,4 | 5,9 | 5,6 |
| não classificado | 1,1 | 1,5 | 57,9 | 58,3 | 0,6 | 0,9 |

## 5. Leitura e limites

- As unidades do painel são maternidades de maior porte (> 1.000 partos SUS) e, em grande parte, referência para alto risco; espera-se que concentrem prematuridade, baixo peso, Apgar baixo e anomalias da região (razão > 1). Isso é efeito de seleção, não de qualidade.
- A região (ocorrência) inclui a própria rede do painel; a comparação mais limpa seria painel × *demais* estabelecimentos, que se obtém por subtração (os numeradores e denominadores estão na planilha).
- Residência × ocorrência divergem onde há migração para parir (Norte, interior do Nordeste, entorno do DF). Para prevalência populacional use a seção 3.
- 2025 é SINASC preliminar; os valores mudam a cada versão. Apgar, peso e idade gestacional ignorados foram excluídos dos denominadores.
- Mortalidade (neonatal, materna) e taxas por população (por 100 mil mulheres) não estão aqui: exigem SIM e estimativas populacionais do IBGE.

Planilha completa (por região, por UF, Robson, cobertura): `planilhas/COMPARACAO_REGIONAL_2024_2025.xlsx`.
