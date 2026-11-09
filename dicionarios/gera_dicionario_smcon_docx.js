// Gera a versão Word (.docx) do dicionário do SMCON a partir do JSON
// produzido por gera_dicionario_smcon.py (mesma pasta).
// Uso: node gera_dicionario_smcon_docx.js [caminho/para/node_modules]
//   - precisa do pacote npm "docx" (v9). Se não estiver instalado globalmente,
//     passe a pasta node_modules como primeiro argumento.
const fs = require("fs");
const path = require("path");

if (process.argv[2]) module.paths.unshift(process.argv[2]);
const D = require("docx");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, ShadingType, AlignmentType, HeadingLevel, BorderStyle,
  PageOrientation, PageNumber, Footer, Header, VerticalAlign,
} = D;

const AQUI = __dirname;
const DATA = "2026-11-09";
const ENTRADA = path.join(AQUI, `DICIONARIO_SMCON_${DATA}.json`);
const SAIDA = path.join(AQUI, `DICIONARIO_SMCON_${DATA}.docx`);

const blocos = JSON.parse(fs.readFileSync(ENTRADA, "utf8"));

// ---- página: A4 paisagem, margens 1,5 cm ----
const PAG_L = 16838, PAG_A = 11906, MARG = 850;
const UTIL = PAG_L - 2 * MARG; // 15138 DXA

const FONTE = "Calibri";
const COR_TITULO = "1F3864";
const COR_SECAO = "D9E2F3";
const COR_CAB = "1F3864";
const BORDA = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const BORDAS = { top: BORDA, bottom: BORDA, left: BORDA, right: BORDA };

function run(texto, extra = {}) {
  return new TextRun({ text: texto, font: FONTE, ...extra });
}

// Negrita a frase introdutória ("O que é o SMCON.", "Fontes:", "1. Regras gerais…")
function paragrafoCorpo(texto, opts = {}) {
  let m = texto.match(/^(\d+\.\s[^.]{1,70}\.)\s([\s\S]*)$/)
       || texto.match(/^([^.:]{1,45}[.:])\s([\s\S]*)$/);
  const runs = m ? [run(m[1], { bold: true }), run(" " + m[2])] : [run(texto)];
  return new Paragraph({
    children: runs,
    spacing: { after: 120, line: 276 },
    alignment: AlignmentType.JUSTIFIED,
    ...opts,
  });
}

function celula(paragrafos, largura, extra = {}) {
  const { bold, cor, cabecalho, span, align } = extra;
  return new TableCell({
    width: { size: largura, type: WidthType.DXA },
    columnSpan: span,
    borders: BORDAS,
    verticalAlign: VerticalAlign.TOP,
    shading: cor ? { type: ShadingType.CLEAR, fill: cor, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    children: paragrafos.map(
      (t) =>
        new Paragraph({
          alignment: align || AlignmentType.LEFT,
          spacing: { after: 40 },
          children: [run(t, { size: 18, bold: !!bold, color: cabecalho ? "FFFFFF" : undefined })],
        })
    ),
  });
}

function tabela(linhas) {
  const ncol = linhas[0].length;
  const larguras =
    ncol === 4 ? [3300, 1250, 3300, UTIL - 3300 - 1250 - 3300]
    : ncol === 3 ? [4000, 5200, UTIL - 4000 - 5200]
    : Array(ncol).fill(Math.floor(UTIL / ncol));
  const rows = linhas.map((linha, i) => {
    if (i === 0) {
      return new TableRow({
        tableHeader: true,
        cantSplit: true,
        children: linha.map((cel, j) => celula(cel, larguras[j], { bold: true, cor: COR_CAB, cabecalho: true })),
      });
    }
    if (linha.length === 1 && ncol > 1) {
      // linha de seção: uma célula mesclada em toda a largura
      return new TableRow({
        cantSplit: true,
        children: [celula(linha[0], UTIL, { bold: true, cor: COR_SECAO, span: ncol })],
      });
    }
    return new TableRow({
      cantSplit: true,
      children: linha.map((cel, j) =>
        celula(cel, larguras[j], { bold: j === 0 && ncol === 4, align: j === 1 && ncol === 4 ? AlignmentType.CENTER : undefined })
      ),
    });
  });
  return new Table({
    width: { size: UTIL, type: WidthType.DXA },
    columnWidths: larguras,
    rows,
  });
}

const filhos = [];
blocos.forEach((b, i) => {
  if (b.tipo === "p") {
    const t = b.texto;
    if (i === 0) {
      filhos.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [run(t)] }));
    } else if (/^Tabela \d+\./.test(t) || t === "Notas") {
      filhos.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [run(t)] }));
    } else if (i === 1) {
      filhos.push(new Paragraph({ children: [run(t, { italics: true, color: "595959" })], spacing: { after: 200 } }));
    } else {
      filhos.push(paragrafoCorpo(t));
    }
  } else if (b.tipo === "tabela") {
    filhos.push(tabela(b.linhas));
    filhos.push(new Paragraph({ children: [], spacing: { after: 120 } }));
  }
});

const doc = new Document({
  creator: "Painel de partos — Indicadores_partos_Brasil2024",
  title: "Dicionário de dados do SMCON",
  styles: {
    default: { document: { run: { font: FONTE, size: 20 } } },
    paragraphStyles: [
      {
        id: "Title", name: "Title", basedOn: "Normal", next: "Normal",
        run: { font: FONTE, size: 32, bold: true, color: COR_TITULO },
        paragraph: { spacing: { before: 0, after: 160 }, keepNext: true },
      },
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONTE, size: 26, bold: true, color: COR_TITULO },
        paragraph: { spacing: { before: 320, after: 120 }, keepNext: true, outlineLevel: 0 },
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: PAG_A, height: PAG_L, orientation: PageOrientation.LANDSCAPE },
          margin: { top: MARG, bottom: MARG, left: MARG, right: MARG },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              children: [run("Dicionário de dados do SMCON — painel de partos, versão de 09/11/2026", { size: 16, color: "7F7F7F" })],
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [
                run("Página ", { size: 16, color: "7F7F7F" }),
                new TextRun({ children: [PageNumber.CURRENT], font: FONTE, size: 16, color: "7F7F7F" }),
                run(" de ", { size: 16, color: "7F7F7F" }),
                new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONTE, size: 16, color: "7F7F7F" }),
              ],
            }),
          ],
        }),
      },
      children: filhos,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(SAIDA, buf);
  console.log("gravado", SAIDA, buf.length, "bytes");
});
