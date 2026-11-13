"""Gera currículo ATS (uma coluna) em DOCX + PDF a partir de um JSON.

Uso:
    python3 build_cv.py <cv.json> <saida_sem_extensao> [--no-pdf] [--keep-html]

Formato do JSON (veja templates/cv-exemplo-pt.json):
{
  "lang": "pt-BR",                       # ou "en"
  "name": "NOME COMPLETO",
  "title": "Cargo-alvo | Especialidade",
  "contact": "Cidade, UF (remoto) · telefone · e-mail · linkedin",
  "sections": [
    {"id": "summary", "title": "RESUMO", "items": [["p", "texto"]]},
    {"id": "experience", "title": "EXPERIÊNCIA", "items": [
        ["job", "Empresa", "Cargo", "2022 – atual"],
        ["b", "Conquista com número"]]},
    {"id": "skills", "title": "COMPETÊNCIAS", "items": [["kv", "Grupo", "item, item"]]}
  ]
}
Tipos de item: "p" parágrafo, "b" bullet, "job" (empresa, cargo, período), "kv" (rótulo, valor).

O DOCX é escrito só com a biblioteca padrão (docx_min.py), sem instalar nada.
O PDF é gerado a partir de um HTML equivalente com Chrome/Chromium/Edge headless;
se não houver navegador, tenta LibreOffice a partir do DOCX. Sem nenhum dos dois,
fica só o DOCX (e o HTML, para imprimir como PDF manualmente).
"""
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from docx_min import Doc  # noqa: E402

FONT = "Arial"


def load(path):
    with open(path, encoding="utf-8") as f:
        cv = json.load(f)
    for key in ("name", "title", "contact", "sections"):
        if key not in cv:
            sys.exit(f"{path}: campo obrigatório ausente: {key}")
    return cv


def build_docx(cv, out_docx):
    lang = cv.get("lang", "pt-BR")
    d = Doc(font=FONT, size_pt=10, lang="en-US" if lang == "en" else lang)
    d.para([(cv["name"], {"bold": True, "size": 18})], after=0)
    d.para([(cv["title"], {"bold": True, "size": 11.5, "color": "333333"})], after=2)
    d.para([(cv["contact"], {"size": 9.5})], after=6)
    for s in cv["sections"]:
        d.para([(s["title"], {"bold": True, "size": 11})], before=8, after=4, rule=True)
        for it in s["items"]:
            kind = it[0]
            if kind == "p":
                d.para([(it[1], {})], after=2)
            elif kind == "b":
                d.para([(it[1], {})], after=2, bullet=True)
            elif kind == "job":
                _, company, role, dates = it
                d.para([(f"{role} | {company}", {"bold": True, "size": 10.5}), ("\t" + dates, {"size": 10})],
                       before=6, after=1, right_tab=d.text_width)
            elif kind == "kv":
                d.para([(it[1] + ": ", {"bold": True}), (it[2], {})], after=2)
            else:
                sys.exit(f"Tipo de item desconhecido: {kind!r}")
    d.save(out_docx)


def build_html(cv, out_html):
    e = html.escape
    lang = cv.get("lang", "pt-BR")
    h = [f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{e(cv['name'])}</title><style>
    @page {{ size: A4; margin: 15mm 18mm; }}
    body {{ font-family: Arial, 'Liberation Sans', sans-serif; font-size: 10pt; line-height: 1.3; color: #111; margin: 0; }}
    h1 {{ font-size: 18pt; margin: 0; }} .t {{ font-size: 11.5pt; font-weight: bold; color: #333; margin: 2pt 0; }}
    .c {{ font-size: 9.5pt; margin-bottom: 4pt; }}
    h2 {{ font-size: 11pt; border-bottom: 1px solid #555; padding-bottom: 1pt; margin: 10pt 0 4pt; }}
    .job {{ display: flex; justify-content: space-between; font-weight: bold; font-size: 10.5pt; margin: 7pt 0 1pt; break-after: avoid; }}
    .job span:last-child {{ font-weight: normal; font-size: 10pt; }}
    ul {{ margin: 0; padding-left: 14pt; }} li {{ margin: 0 0 2pt; }} p {{ margin: 0 0 2pt; }}
    </style></head><body>
    <h1>{e(cv['name'])}</h1><div class="t">{e(cv['title'])}</div><div class="c">{e(cv['contact'])}</div>"""]
    for s in cv["sections"]:
        h.append(f"<h2>{e(s['title'])}</h2>")
        open_ul = False
        for it in s["items"]:
            if it[0] == "b":
                if not open_ul:
                    h.append("<ul>")
                    open_ul = True
                h.append(f"<li>{e(it[1])}</li>")
                continue
            if open_ul:
                h.append("</ul>")
                open_ul = False
            if it[0] == "p":
                h.append(f"<p>{e(it[1])}</p>")
            elif it[0] == "job":
                h.append(f'<div class="job"><span>{e(it[2])} | {e(it[1])}</span><span>{e(it[3])}</span></div>')
            elif it[0] == "kv":
                h.append(f"<p><b>{e(it[1])}:</b> {e(it[2])}</p>")
        if open_ul:
            h.append("</ul>")
    h.append("</body></html>")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write("\n".join(h))


BROWSERS = [
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "msedge", "chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def _find(cands):
    for c in cands:
        p = shutil.which(c) or (c if os.path.isfile(c) else None)
        if p:
            return p
    return None


def build_pdf(out_base):
    """Gera <out_base>.pdf. Retorna o método usado ou None."""
    pdf, src_html, src_docx = out_base + ".pdf", out_base + ".html", out_base + ".docx"
    browser = _find([os.environ.get("CV_BROWSER", "")] + BROWSERS)
    if browser:
        uri = "file:///" + os.path.abspath(src_html).replace(os.sep, "/").lstrip("/")
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={os.path.abspath(pdf)}", uri],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, timeout=120)
        if os.path.isfile(pdf) and os.path.getsize(pdf) > 0:
            return "navegador"
    office = _find(["libreoffice", "soffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice"])
    if office:
        outdir = os.path.dirname(os.path.abspath(pdf))
        # snaps do LibreOffice não escrevem fora de $HOME: converte num temporário dentro dele se preciso
        with tempfile.TemporaryDirectory(dir=os.path.expanduser("~")) as tmp:
            subprocess.run([office, "--headless", "--convert-to", "pdf", "--outdir", tmp, os.path.abspath(src_docx)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, timeout=180)
            produced = os.path.join(tmp, os.path.splitext(os.path.basename(src_docx))[0] + ".pdf")
            if os.path.isfile(produced):
                shutil.move(produced, os.path.join(outdir, os.path.basename(pdf)))
                return "libreoffice"
    return None


def build(cv, out_base, pdf=True, keep_html=False):
    os.makedirs(os.path.dirname(os.path.abspath(out_base)), exist_ok=True)
    build_docx(cv, out_base + ".docx")
    build_html(cv, out_base + ".html")
    method = build_pdf(out_base) if pdf else None
    if method and not keep_html:
        os.remove(out_base + ".html")
    return method


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    cv = load(args[0])
    method = build(cv, args[1], pdf="--no-pdf" not in argv, keep_html="--keep-html" in argv)
    print(f"ok {args[1]}.docx" + (f" + .pdf ({method})" if method else " (sem PDF: abra o .html e imprima em PDF)"))


if __name__ == "__main__":
    main(sys.argv[1:])
