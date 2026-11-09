// Gera Metodologia_Indicadores_Painel.docx a partir de METODOLOGIA.md (títulos, parágrafos, listas, citações e tabelas).
// Uso: node scripts/gera_metodologia_docx.js <node_modules> [METODOLOGIA.md] [saida.docx]
//   - precisa do pacote npm "docx" (v9): passe a pasta node_modules onde ele está instalado.
const fs = require("fs");
const path = require("path");

const [MODULOS, ENTRADA = "METODOLOGIA.md", SAIDA = "Metodologia_Indicadores_Painel.docx"] = process.argv.slice(2);
if (MODULOS && MODULOS !== "-") module.paths.unshift(path.resolve(MODULOS));
const D = require("docx");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType,
  HeadingLevel, BorderStyle, PageNumber, Footer, Header, VerticalAlign, LevelFormat,
} = D;

const RAIZ = path.resolve(__dirname, "..");
const md = fs.readFileSync(path.resolve(RAIZ, ENTRADA), "utf8").split(/\r?\n/);

// ---- página A4 retrato, margens 2 cm ----
const PAG_L = 11906, PAG_A = 16838, MARG = 1134;
const UTIL = PAG_L - 2 * MARG; // 9638 DXA
const FONTE = "Calibri";
const COR_TITULO = "1F3864";
const BORDA = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
const BORDAS = { top: BORDA, bottom: BORDA, left: BORDA, right: BORDA };

// texto com **negrito**, *itálico*, `código` e [link](url) -> runs
function runs(texto, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\))/g;
  let i = 0, m;
  while ((m = re.exec(texto)) !== null) {
    if (m.index > i) out.push(new TextRun({ text: texto.slice(i, m.index), font: FONTE, ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), font: FONTE, bold: true, ...base }));
    else if (t.startsWith("`")) out.push(new TextRun({ text: t.slice(1, -1), font: "Consolas", size: (base.size || 20) - 2, ...base }));
    else if (t.startsWith("[")) out.push(new TextRun({ text: t.replace(/^\[([^\]]+)\]\(.*\)$/, "$1"), font: FONTE, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), font: FONTE, italics: true, ...base }));
    i = m.index + t.length;
  }
  if (i < texto.length) out.push(new TextRun({ text: texto.slice(i), font: FONTE, ...base }));
  return out;
}

function celula(texto, largura, cab = false) {
  return new TableCell({
    width: { size: largura, type: WidthType.DXA }, borders: BORDAS, verticalAlign: VerticalAlign.TOP,
    shading: cab ? { type: ShadingType.CLEAR, fill: COR_TITULO, color: "auto" } : undefined,
    margins: { top: 50, bottom: 50, left: 80, right: 80 },
    children: [new Paragraph({ spacing: { after: 0 }, children: runs(texto, { size: 17, bold: cab || undefined, color: cab ? "FFFFFF" : undefined }) })],
  });
}

function tabela(linhas) {
  const cel = (l) => l.replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
  const corpo = linhas.filter((l) => !/^\|?\s*:?-{2,}/.test(l)).map(cel);
  const ncol = Math.max(...corpo.map((r) => r.length));
  const larguras = Array(ncol).fill(Math.floor(UTIL / ncol));
  larguras[ncol - 1] += UTIL - larguras.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: UTIL, type: WidthType.DXA }, columnWidths: larguras,
    rows: corpo.map((r, i) => new TableRow({ tableHeader: i === 0, cantSplit: true,
      children: larguras.map((w, j) => celula(r[j] || "", w, i === 0)) })),
  });
}

const filhos = [];
let bufTab = [], primeiroTitulo = true;
const flush = () => { if (bufTab.length) { filhos.push(tabela(bufTab)); filhos.push(new Paragraph({ spacing: { after: 120 }, children: [] })); bufTab = []; } };
for (const l of md) {
  if (/^\s*\|/.test(l)) { bufTab.push(l); continue; }
  flush();
  if (!l.trim() || /^---+$/.test(l.trim())) continue;
  let m;
  if ((m = l.match(/^(#{1,3})\s+(.*)$/))) {
    const n = m[1].length;
    if (n === 1 && primeiroTitulo) { filhos.push(new Paragraph({ heading: HeadingLevel.TITLE, children: runs(m[2]) })); primeiroTitulo = false; }
    else filhos.push(new Paragraph({ heading: n <= 2 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2, children: runs(m[2]) }));
  } else if ((m = l.match(/^>\s?(.*)$/))) {
    filhos.push(new Paragraph({ indent: { left: 567 }, spacing: { after: 120 }, border: { left: { style: BorderStyle.SINGLE, size: 12, color: "9DC3E6", space: 8 } },
      children: runs(m[1], { size: 19, color: "404040" }) }));
  } else if ((m = l.match(/^\s*[-*]\s+(.*)$/))) {
    filhos.push(new Paragraph({ numbering: { reference: "marcadores", level: 0 }, spacing: { after: 60 }, children: runs(m[1]) }));
  } else {
    filhos.push(new Paragraph({ spacing: { after: 120, line: 276 }, alignment: AlignmentType.JUSTIFIED, children: runs(l) }));
  }
}
flush();

const pequeno = { size: 16, color: "7F7F7F" };
const doc = new Document({
  creator: "Painel de partos — Indicadores_partos_Brasil2024",
  title: "Nota metodológica — Indicadores da Atenção Obstétrica e Neonatal",
  numbering: { config: [{ reference: "marcadores", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 567, hanging: 283 } } } }] }] },
  styles: {
    default: { document: { run: { font: FONTE, size: 20 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal", run: { font: FONTE, size: 32, bold: true, color: COR_TITULO }, paragraph: { spacing: { before: 0, after: 200 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONTE, size: 26, bold: true, color: COR_TITULO }, paragraph: { spacing: { before: 320, after: 120 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: FONTE, size: 22, bold: true, color: COR_TITULO }, paragraph: { spacing: { before: 240, after: 80 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: PAG_L, height: PAG_A }, margin: { top: MARG, bottom: MARG, left: MARG, right: MARG } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Nota metodológica · painel de partos · gerada de METODOLOGIA.md", font: FONTE, ...pequeno })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "Página ", font: FONTE, ...pequeno }), new TextRun({ children: [PageNumber.CURRENT], font: FONTE, ...pequeno }),
      new TextRun({ text: " de ", font: FONTE, ...pequeno }), new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONTE, ...pequeno }) ] })] }) },
    children: filhos,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(path.resolve(RAIZ, SAIDA), buf);
  console.log("gravado", path.resolve(RAIZ, SAIDA), buf.length, "bytes;", filhos.length, "blocos");
});
