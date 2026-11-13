# Fase 2 — Perfil mestre e currículos ATS

## Perfil mestre (`<pasta>/perfil-mestre.md`)
Fonte única de verdade. Tudo que vai para CV, LinkedIn, plataformas, respostas e mensagens sai daqui.
- Parta de `templates/perfil-mestre.md` (já copiado pelo `init_workspace.py`).
- Cada fato tem origem no usuário. Lacuna ou dúvida → `[CONFIRMAR]`. Uso interno (pretensão, último salário,
  motivo de saída) → marque **(uso interno)**.
- Resultados no formato verbo + o quê + número. Sem adjetivos vazios ("proativo", "apaixonado").
- Proponha headline do LinkedIn e pitch curto; o usuário aprova.

## Currículos-base (`<pasta>/cv/cv-pt.json` e `cv-en.json`)
Formato em `templates/cv-exemplo-pt.json` (exemplo fictício — não reaproveite conteúdo dele). Regras ATS:
- Uma coluna, sem tabelas, imagens, ícones ou cabeçalho/rodapé; fonte Arial; títulos de seção em texto.
- Seções com `id`: `summary` (1 parágrafo; o `tailor.py` prefixa o foco da vaga aqui), `highlights` (opcional),
  `experience`, `skills` (itens `kv`: o `tailor.py` reordena pelos rótulos), `education`.
- Cargo-alvo no `title`; palavras-chave reais da área nas competências.
- Contato: cidade/UF + "(remoto)" se for o caso, telefone, e-mail pessoal, LinkedIn/GitHub. Nada de CPF, foto,
  idade, estado civil.
- 1–2 páginas. Experiências antigas podem virar uma linha.
- A versão EN é tradução fiel, não reescrita com fatos novos. Datas e números iguais.
- Não liste nível de idioma no CV se o usuário pediu para informar só quando perguntado.

## Gerar os arquivos
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build_cv.py" <pasta>/cv/cv-pt.json "<pasta>/cv/Nome_Sobrenome_CV_PT"
python3 "${CLAUDE_SKILL_DIR}/scripts/build_cv.py" <pasta>/cv/cv-en.json "<pasta>/cv/Nome_Sobrenome_CV_EN"
```
- O DOCX é gerado só com a biblioteca padrão. O PDF usa Chrome/Chromium/Edge headless; se não houver, tenta
  LibreOffice; se nenhum existir, fica o `.html` para o usuário imprimir em PDF (avise).
- Variável `CV_BROWSER=/caminho/do/navegador` força um navegador específico.
- Leia o PDF gerado (ferramenta Read) para conferir quebra de página e se cabe em 1–2 páginas.

## Antes de dar a fase por concluída
- Liste os `[CONFIRMAR]`; nenhum pode estar no CV final.
- Mostre ao usuário os caminhos dos arquivos e peça aprovação.
