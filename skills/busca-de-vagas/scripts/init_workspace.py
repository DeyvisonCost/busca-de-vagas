"""Cria a pasta de trabalho da busca de vagas a partir dos templates.

Uso:
    python3 init_workspace.py <pasta> [--lang pt|en] [--title "Busca de vagas"] [--subtitle "Cargo · remoto"]
                              [--tz America/Sao_Paulo] [--cutoff 6] [--goal 5]

Nunca sobrescreve arquivo existente. Para só regerar o rastreador com outros textos,
apague <pasta>/rastreador.html e rode de novo.

Estrutura criada:
    <pasta>/perfil-mestre.md    fonte única de verdade (preenchida na entrevista)
    <pasta>/criterios.md        regras de busca, nota e envio
    <pasta>/config.json         configuração lida pelos scripts e pela varredura
    <pasta>/rastreador.html     página do rastreador (publicar como Artifact com banco)
    <pasta>/tarefa-varredura.md prompt da tarefa agendada (preencher e agendar)
    <pasta>/cv/  lotes/  vagas/  contatos/
"""
import argparse
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.normpath(os.path.join(HERE, "..", "templates"))


def copy_if_missing(src, dst):
    if os.path.exists(dst):
        print("mantido ", dst)
        return False
    shutil.copyfile(src, dst)
    print("criado  ", dst)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--lang", default="pt", choices=["pt", "en"])
    ap.add_argument("--title", default=None)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--tz", default="America/Sao_Paulo")
    ap.add_argument("--cutoff", type=int, default=6)
    ap.add_argument("--goal", type=int, default=5)
    a = ap.parse_args()

    ws = os.path.abspath(os.path.expanduser(a.pasta))
    for d in ("", "cv", "lotes", "vagas", "contatos"):
        os.makedirs(os.path.join(ws, d), exist_ok=True)

    suf = "-en" if a.lang == "en" else ""
    for name in ("perfil-mestre", "criterios"):
        src = os.path.join(TPL, f"{name}{suf}.md")
        if not os.path.isfile(src):
            src = os.path.join(TPL, f"{name}.md")
        copy_if_missing(src, os.path.join(ws, f"{name}.md"))
    copy_if_missing(os.path.join(TPL, "tarefa-varredura.md"), os.path.join(ws, "tarefa-varredura.md"))

    cfg_path = os.path.join(ws, "config.json")
    if copy_if_missing(os.path.join(TPL, "config.json"), cfg_path):
        with open(cfg_path, encoding="utf-8") as f:
            cfg = json.load(f)
        cfg.update({"idioma": a.lang, "fuso": a.tz, "corte_nota": a.cutoff, "meta_entrevistas_semana": a.goal})
        with open(cfg_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

    html_path = os.path.join(ws, "rastreador.html")
    if os.path.exists(html_path):
        print("mantido ", html_path)
    else:
        title = a.title or ("Job search" if a.lang == "en" else "Busca de vagas")
        with open(os.path.join(TPL, "rastreador.html"), encoding="utf-8") as f:
            page = f.read()
        esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        for k, v in {"TITLE": esc(title), "SUBTITLE": esc(a.subtitle), "LANG": a.lang, "TZ": a.tz,
                     "CUTOFF": str(a.cutoff), "GOAL": str(a.goal)}.items():
            page = page.replace("{{" + k + "}}", v)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page)
        print("criado  ", html_path)
    print("\nPasta pronta:", ws)


if __name__ == "__main__":
    main()
