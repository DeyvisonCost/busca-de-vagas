"""Escritor mínimo de DOCX só com a biblioteca padrão (zipfile + XML).

Cobre o que um currículo ATS de uma coluna precisa: parágrafos com runs (negrito,
itálico, tamanho, cor), bullets reais (lista do Word), tabulação à direita e linha inferior
em títulos de seção. Sem dependências externas, roda em qualquer Python 3.8+.
"""
import zipfile
from xml.sax.saxutils import escape

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def cm(v):
    return int(round(v * 567))  # twips


class Doc:
    def __init__(self, font="Arial", size_pt=10, lang="pt-BR", page_cm=(21, 29.7), margins_cm=(1.5, 1.8, 1.5, 1.8)):
        self.font, self.size, self.lang = font, size_pt, lang
        self.page, self.margins = page_cm, margins_cm  # top, right, bottom, left
        self.body = []

    @property
    def text_width(self):
        return cm(self.page[0] - self.margins[1] - self.margins[3])

    def para(self, runs=(), after=2, before=0, line=1.1, bullet=False, rule=False, right_tab=None):
        """runs: lista de (texto, {"bold":bool, "italic":bool, "size":pt, "color":"RRGGBB"}). '\t' vira tabulação."""
        ppr = [f'<w:spacing w:before="{int(before * 20)}" w:after="{int(after * 20)}" w:line="{int(240 * line)}" w:lineRule="auto"/>']
        if bullet:
            ppr.insert(0, '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>')
        if rule:
            ppr.insert(0, '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="555555"/></w:pBdr>')
        if right_tab:
            ppr.insert(0, f'<w:tabs><w:tab w:val="right" w:pos="{right_tab}"/></w:tabs>')
        out = [f"<w:p><w:pPr>{''.join(ppr)}</w:pPr>"]
        for text, fmt in runs:
            rpr = ""
            if fmt.get("bold"):
                rpr += "<w:b/>"
            if fmt.get("italic"):
                rpr += "<w:i/>"
            if fmt.get("color"):
                rpr += f'<w:color w:val="{fmt["color"]}"/>'
            if fmt.get("size"):
                rpr += f'<w:sz w:val="{int(fmt["size"] * 2)}"/><w:szCs w:val="{int(fmt["size"] * 2)}"/>'
            parts = text.split("\t")
            inner = '<w:tab/>'.join(f'<w:t xml:space="preserve">{escape(p)}</w:t>' for p in parts)
            out.append(f"<w:r>{f'<w:rPr>{rpr}</w:rPr>' if rpr else ''}{inner}</w:r>")
        out.append("</w:p>")
        self.body.append("".join(out))

    def _document(self):
        t, r, b, l = (cm(m) for m in self.margins)
        sect = (f'<w:sectPr><w:pgSz w:w="{cm(self.page[0])}" w:h="{cm(self.page[1])}"/>'
                f'<w:pgMar w:top="{t}" w:right="{r}" w:bottom="{b}" w:left="{l}" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>')
        return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<w:document xmlns:w="{W_NS}" xmlns:r="{R_NS}"><w:body>{"".join(self.body)}{sect}</w:body></w:document>')

    def _styles(self):
        f, sz = escape(self.font), int(self.size * 2)
        return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="{W_NS}">'
                f'<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{f}" w:hAnsi="{f}" w:eastAsia="{f}" w:cs="{f}"/>'
                f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/><w:lang w:val="{escape(self.lang)}"/></w:rPr></w:rPrDefault>'
                f'<w:pPrDefault><w:pPr><w:spacing w:after="0"/></w:pPr></w:pPrDefault></w:docDefaults>'
                f'<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
                f'</w:styles>')

    def _numbering(self):
        return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="{W_NS}">'
                f'<w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/>'
                f'<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/>'
                f'<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="360" w:hanging="240"/></w:pPr></w:lvl></w:abstractNum>'
                f'<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>')

    def save(self, path):
        ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="xml" ContentType="application/xml"/>'
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
              '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
              '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
              '</Types>')
        rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                '</Relationships>')
        doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
                    '</Relationships>')
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", ct)
            z.writestr("_rels/.rels", rels)
            z.writestr("word/_rels/document.xml.rels", doc_rels)
            z.writestr("word/document.xml", self._document())
            z.writestr("word/styles.xml", self._styles())
            z.writestr("word/numbering.xml", self._numbering())
