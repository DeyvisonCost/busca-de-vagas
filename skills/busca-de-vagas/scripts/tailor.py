"""Gera currículos ajustados por vaga (por palavra-chave, para ATS) a partir dos currículos-base.

Uso:
    python3 tailor.py <lote.json> [--workspace <pasta>] [--no-pdf]

<pasta> é a pasta de trabalho criada por init_workspace.py (padrão: a pasta pai de lotes/).
Ela precisa ter config.json e os currículos-base indicados nele (cv/cv-pt.json, cv/cv-en.json).

lote.json = lista de objetos (veja templates/lote-exemplo.json):
  {"arquivo": "empresa-cargo",           # nome do arquivo de saída, sem extensão
   "vaga": "Empresa — Cargo",            # rótulo legível
   "lang": "pt",                         # "pt" ou "en"
   "titulo": "Título do CV para esta vaga (cargo da vaga + 2–3 termos dela)",
   "resumo": "Resumo inteiro reescrito com os termos EXATOS da vaga (só fatos do perfil-mestre).",
   "foco": "(alternativa ao resumo) frase prefixada ao resumo-base.",
   "palavras_chave": ["12–25 termos da vaga que são verdade no perfil"],   # vira a 1ª linha de competências
   "bullets_extra": {"Empresa do currículo-base": ["bullet verdadeiro com termos da vaga"]},
   "stack": {"Empresa do currículo-base": "Stack: tecnologia, tecnologia"},  # linha sob o cargo
   "competencias_primeiro": ["Grupo A", "Grupo B"],   # rótulos "kv" da seção skills
   "vaga_texto": "lotes/jd/empresa-cargo.txt",        # descrição completa da vaga -> <arquivo>-ats.md
   "pretensao": "texto da pretensão para esta vaga",
   "notas": "observações e respostas específicas"}

Saída em <pasta>/vagas/: <arquivo>.docx, <arquivo>.pdf, <arquivo>-respostas.md e, com "vaga_texto",
<arquivo>-ats.md (cobertura dos termos da vaga). Caminhos relativos de "vaga_texto" partem da pasta de
trabalho (ou da pasta do lote). O ajuste reescreve resumo e acrescenta termos/bullets que vêm do lote:
quem monta o lote garante que tudo é verdade no perfil-mestre — o script não inventa nada.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ats_check  # noqa: E402
import build_cv  # noqa: E402

MATCH_LABEL = {"pt": "Aderência à vaga", "en": "Job match"}


def tailor(base, spec, lang="pt"):
    cv = copy.deepcopy(base)
    if spec.get("titulo"):
        cv["title"] = spec["titulo"]
    extra = spec.get("bullets_extra") or {}
    stack = spec.get("stack") or {}
    for s in cv["sections"]:
        items = s["items"]
        if s.get("id") == "summary" and items and items[0][0] == "p":
            if spec.get("resumo"):
                items[0] = ["p", spec["resumo"].strip()]
            elif spec.get("foco"):
                items[0] = ["p", spec["foco"].strip() + " " + items[0][1]]
        if s.get("id") == "experience" and (extra or stack):
            s["items"] = _experience(items, extra, stack)
        if s.get("id") == "skills":
            if spec.get("competencias_primeiro"):
                first = [i for k in spec["competencias_primeiro"] for i in s["items"] if i[0] == "kv" and i[1] == k]
                s["items"] = first + [i for i in s["items"] if i not in first]
            if spec.get("palavras_chave"):
                s["items"] = [["kv", MATCH_LABEL[lang], ", ".join(spec["palavras_chave"])]] + s["items"]
    return cv


def _experience(items, extra, stack):
    """Por cargo: cabeçalho, bullets_extra do lote (logo no topo), bullets do base e, por último, a linha "Stack:".
    A linha "Stack:" do lote substitui a do currículo-base daquela empresa."""
    blocks, cur = [], None
    for it in items:
        if it[0] == "job":
            cur = [it]
            blocks.append(cur)
        elif cur is None:
            blocks.append([it])
        else:
            cur.append(it)
    out = []
    for b in blocks:
        head = b[0]
        if head[0] != "job":
            out += b
            continue
        company = head[1]
        body = b[1:]
        stack_lines = [x for x in body if x[0] == "stack"]
        body = [x for x in body if x[0] != "stack"]
        body = [["b", t] for t in extra.get(company, [])] + body
        if company in stack:
            stack_lines = [["stack", stack[company]]]
        out += [head] + body + stack_lines
    return out


def write_answers(path, spec, cfg):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Respostas prontas — {spec.get('vaga', spec['arquivo'])}\n\n")
        if spec.get("pretensao"):
            f.write(f"- Pretensão: {spec['pretensao']}\n")
        for line in cfg.get("respostas_padrao", []):
            f.write(f"- {line}\n")
        if spec.get("notas"):
            f.write(f"\n## Mensagem / observações\n\n{spec['notas']}\n")


def resolve(path, ws, lote_dir):
    if os.path.isabs(path):
        return path
    for base in (ws, lote_dir):
        p = os.path.normpath(os.path.join(base, path))
        if os.path.isfile(p):
            return p
    return os.path.normpath(os.path.join(ws, path))


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    lote = os.path.abspath(args[0])
    ws = os.path.dirname(os.path.dirname(lote))
    if "--workspace" in argv:
        ws = os.path.abspath(argv[argv.index("--workspace") + 1])
        args = [a for a in args if os.path.abspath(a) != ws]
    cfg_path = os.path.join(ws, "config.json")
    if not os.path.isfile(cfg_path):
        sys.exit(f"config.json não encontrado em {ws}. Rode init_workspace.py ou passe --workspace.")
    with open(cfg_path, encoding="utf-8") as f:
        cfg = json.load(f)
    bases = {}
    for lang, rel in cfg.get("cv_base", {}).items():
        p = os.path.join(ws, rel)
        if os.path.isfile(p):
            bases[lang] = build_cv.load(p)
    extra_terms = os.path.join(ws, "ats-termos.json")
    terms = ats_check.load_terms(extra_terms if os.path.isfile(extra_terms) else None)
    with open(lote, encoding="utf-8") as f:
        specs = json.load(f)
    out_dir = os.path.join(ws, "vagas")
    os.makedirs(out_dir, exist_ok=True)
    for spec in specs:
        lang = "en" if spec.get("lang") == "en" else "pt"
        if lang not in bases:
            print(f"pulado {spec['arquivo']}: sem currículo-base '{lang}' em config.json")
            continue
        out = os.path.join(out_dir, spec["arquivo"])
        cv = tailor(bases[lang], spec, lang)
        method = build_cv.build(cv, out, pdf="--no-pdf" not in argv)
        write_answers(out + "-respostas.md", spec, cfg)
        msg = "ok " + spec["arquivo"] + " (pdf: " + (method or "não gerado") + ")"
        if spec.get("vaga_texto"):
            jd_path = resolve(spec["vaga_texto"], ws, os.path.dirname(lote))
            if os.path.isfile(jd_path):
                with open(jd_path, encoding="utf-8") as f:
                    rep = ats_check.report(f.read(), ats_check.cv_text(cv), terms)
                with open(out + "-ats.md", "w", encoding="utf-8") as f:
                    f.write(rep)
                msg += " · " + rep.splitlines()[2]
            else:
                msg += f" · vaga_texto não encontrado: {jd_path}"
        print(msg)


if __name__ == "__main__":
    main(sys.argv[1:])
