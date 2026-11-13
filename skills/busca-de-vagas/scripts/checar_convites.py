"""Confere o tamanho dos convites do LinkedIn num arquivo de contatos (limite padrão: 200 caracteres).

Uso: python3 checar_convites.py <contatos.md> [--limite 200]

Considera convite o primeiro bloco de citação ("> ...") depois de uma linha que começa
com "**Convite" ou "**Invite". Sai com código 1 se algum passar do limite.
"""
import sys


def main(argv):
    if not argv:
        sys.exit(__doc__)
    limit = int(argv[argv.index("--limite") + 1]) if "--limite" in argv else 200
    lines = open(argv[0], encoding="utf-8").read().splitlines()
    waiting, n, bad = False, 0, 0
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("**Convite") or s.startswith("**Invite"):
            waiting = True
            continue
        if waiting and s.startswith(">"):
            text = s[1:].strip()
            n += 1
            ok = len(text) <= limit
            bad += not ok
            print(f"{'ok ' if ok else 'ACIMA'} linha {i}: {len(text)} caracteres")
            waiting = False
    print(f"{n} convite(s), {bad} acima de {limit}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
