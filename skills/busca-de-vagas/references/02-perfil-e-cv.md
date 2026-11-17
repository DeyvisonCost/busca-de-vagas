# Fase 2 — Perfil mestre e currículos ATS

## Perfil mestre (`<pasta>/perfil-mestre.md`)
Fonte única de verdade. Tudo que vai para CV, LinkedIn, plataformas, respostas e mensagens sai daqui.
- Parta de `templates/perfil-mestre.md` (já copiado pelo `init_workspace.py`).
- Cada fato tem origem no usuário. Lacuna ou dúvida → `[CONFIRMAR]`. Uso interno (pretensão, último salário,
  motivo de saída) → marque **(uso interno)**.
- Resultados no formato verbo + o quê + número. Sem adjetivos vazios ("proativo", "apaixonado").
- Proponha headline do LinkedIn e pitch curto; o usuário aprova.

## Questionário ATS (inventário de palavras-chave)
Objetivo: saber, termo a termo, o que o usuário domina de verdade, para o CV por vaga usar os termos exatos
das vagas sem inventar nada.
1. `<pasta>/questionario-ats.html` já foi copiado pelo `init_workspace.py` (título "Questionário ATS", sem
   dados pessoais). Os blocos vêm prontos para tecnologia/liderança — liderança, agilidade e métricas,
   front/mobile, back-end, arquitetura, dados e mensageria, cloud/DevOps, observabilidade e qualidade,
   segurança, IA, domínios, ferramentas e idiomas (~250 termos). Para outra área, troque os termos dos blocos
   antes de publicar.
2. Carregue a skill `artifact-capabilities` e publique com a ferramenta `Artifact`, capacidades **db** e
   **user**. Ícone: `list`. Grave a URL em `config.json` → `questionario_url`.
3. O usuário marca o nível de cada termo (1 conheço · 2 já usei · 3 uso bem · 4 referência; em branco = nunca
   usou), escreve por bloco **onde e como usou** (empresa, projeto, números) e responde as perguntas abertas:
   maior time liderado, contratações/desligamentos, orçamento, anos (total, liderança, gestão), resultados com
   número, uso de IA no time, uma decisão de arquitetura, certificações e o que **não** deve aparecer.
4. Leia com `ArtifactData` (action `get`, collection `questionario`, doc_id `ats`) e escreva a seção
   **"Inventário ATS"** no `perfil-mestre.md`: termos por nível, contexto de cada bloco e respostas abertas.
   Pergunte o que ficou ambíguo.
5. Regras de uso: nível ≥ 2 pode ir para competências e linhas "Stack:"; **bullets só com fatos que o usuário
   descreveu**; nível 1 ou sem marcação, **nunca**. Se o usuário marcar quase tudo no nível máximo, mantenha os
   bullets factuais (só o que ele contou) e ponha a amplitude nas competências e nas linhas "Stack:".

## Currículos-base (`<pasta>/cv/cv-pt.json` e `cv-en.json`)
Formato em `templates/cv-exemplo-pt.json` (exemplo fictício — não reaproveite conteúdo dele). Regras ATS:
- Uma coluna, sem tabelas, imagens, ícones ou cabeçalho/rodapé; fonte Arial; títulos de seção em texto.
- Seções com `id`: `summary` (1 parágrafo; o `tailor.py` reescreve com o `resumo` da vaga ou prefixa o
  `foco`), `highlights` (opcional), `experience`, `skills` (itens `kv`: o `tailor.py` reordena pelos rótulos e
  põe a linha "Aderência à vaga" no topo), `education`.
- Em `experience`, cada cargo pode terminar com um item `["stack", "Stack: tecnologia, tecnologia"]` (linha
  curta em itálico): ajuda o ATS a casar termos sem inflar os bullets. Só tecnologias nível ≥ 2 no inventário.
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
