"""Gera currículos ajustados por vaga a partir dos currículos-base do usuário.

Uso:
    python3 tailor.py <lote.json> [--workspace <pasta>] [--no-pdf]

<pasta> é a pasta de trabalho criada por init_workspace.py (padrão: a pasta pai de lotes/).
Ela precisa ter config.json e os currículos-base indicados nele (cv/cv-pt.json, cv/cv-en.json).

lote.json = lista de objetos (veja templates/lote-exemplo.json):
  {"arquivo": "empresa-cargo",           # nome do arquivo de saída, sem extensão
   "vaga": "Empresa — Cargo",            # rótulo legível
   "lang": "pt",                         # "pt" ou "en"
   "titulo": "Título do CV para esta vaga",
   "foco": "Frase de abertura do resumo ligada à vaga (só fatos do perfil-mestre).",
   "competencias_primeiro": ["Grupo A", "Grupo B"],   # rótulos "kv" da seção skills
   "pretensao": "texto da pretensão para esta vaga",
   "notas": "observações e respostas específicas"}

Saída em <pasta>/vagas/: <arquivo>.docx, <arquivo>.pdf e <arquivo>-respostas.md.
O ajuste só reordena e prefixa; nunca acrescenta experiência que não está no currículo-base.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_cv  # noqa: E402


def tailor(base, spec):
    cv = copy.deepcopy(base)
    if spec.get("titulo"):
        cv["title"] = spec["titulo"]
    for s in cv["sections"]:
        if s.get("id") == "summary" and spec.get("foco") and s["items"] and s["items"][0][0] == "p":
            s["items"][0] = ["p", spec["foco"].strip() + " " + s["items"][0][1]]
        if s.get("id") == "skills" and spec.get("competencias_primeiro"):
            first = [i for k in spec["competencias_primeiro"] for i in s["items"] if i[0] == "kv" and i[1] == k]
            s["items"] = first + [i for i in s["items"] if i not in first]
    return cv


def write_answers(path, spec, cfg):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Respostas prontas — {spec.get('vaga', spec['arquivo'])}\n\n")
        if spec.get("pretensao"):
            f.write(f"- Pretensão: {spec['pretensao']}\n")
        for line in cfg.get("respostas_padrao", []):
            f.write(f"- {line}\n")
        if spec.get("notas"):
            f.write(f"\n## Mensagem / observações\n\n{spec['notas']}\n")


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
        method = build_cv.build(tailor(bases[lang], spec), out, pdf="--no-pdf" not in argv)
        write_answers(out + "-respostas.md", spec, cfg)
        print("ok", spec["arquivo"], "(pdf: " + (method or "não gerado") + ")")


if __name__ == "__main__":
    main(sys.argv[1:])
