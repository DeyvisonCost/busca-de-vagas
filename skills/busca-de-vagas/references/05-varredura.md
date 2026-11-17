# Fase 5 — Esteira (varredura agendada)

Busca → pontua → registra no rastreador → gera CV ajustado por vaga. **Nunca envia.**
Pré-requisitos: `criterios.md`, `config.json`, `cv/cv-pt.json` (e `cv-en.json` se houver vagas em inglês)
e o rastreador publicado (fase 6) com a URL gravada em `config.json` → `rastreador_url`.

## 1. Fazer uma varredura manual primeiro
Rode o passo a passo de `templates/tarefa-varredura.md` uma vez na sessão, com o usuário vendo, para calibrar
termos de busca e nota. Ajuste o `criterios.md` (com aprovação) antes de agendar.

## 2. Fontes e métodos

**Janela de busca: mínimo 72h.** O LinkedIn indexa vagas com atraso e mantém a data de publicação original;
janelas de 1–2h (`f_TPR=r3600`/`r7200`) perdem vagas que aparecem "publicadas há 5h" só depois. Use sempre
`f_TPR=r259200` (72h) ou mais no LinkedIn e `publishedDate >= agora − 72h` na Gupy, e **deduplique contra o
rastreador** (id já registrado → pular). Some uma **busca combinada tipo alerta**, com os cargos-alvo do
`criterios.md` unidos por OR (ex.: `"Cargo A" OR "Cargo B" OR "Sinônimo"`), além dos termos isolados.

**LinkedIn (sem login, API pública de visitante)**
- Lista: `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=<termo>&location=<país>&f_WT=2&f_TPR=r259200&start=0`
  - `f_WT`: 1 presencial, 2 remoto, 3 híbrido. `f_TPR=r<segundos>`: publicadas nos últimos N segundos
    (r86400 = 24h, r259200 = 72h — mínimo recomendado). `start` pagina de 25 em 25.
  - O filtro `f_WT=2` (remoto) **devolve vagas híbridas e presenciais**: confirme o selo de modelo na página
    da vaga (e local/descrição) antes de registrar.
  - Os ids vêm como `urn:li:jobPosting:<id>`; o HTML traz título, empresa, local e `<time datetime>`.
- Detalhe: `https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/<id>` (descrição, senioridade, tipo).
- Link público da vaga: `https://www.linkedin.com/jobs/view/<id>`.
- Confira se a candidatura é "Candidatura simplificada" (fica no LinkedIn) ou externa (veja o destino; se for
  agregador proibido, procure a vaga no ATS da empresa).

**Gupy**
- No navegador, abra `https://portal.gupy.io/job-search/term=<termo>` e, na própria página, rode
  `fetch('/api/job-search/jobs?jobName=<termo>&limit=100&offset=0').then(r => r.json())`.
- Campos úteis: `id`, `name`, `careerPageName`, `jobUrl`, `workplaceType` (`remote`/`hybrid`/`on-site`),
  `publishedDate`, `city`, `state`, `type` (regime). Filtre `publishedDate >= agora − 72h`.

**Indeed**
- `https://<br|www|...>.indeed.com/jobs?q=<termos>&l=<Remoto|Remote>&fromage=1&sort=date`; o painel da vaga
  abre com `&vjk=<jk>`. Leia pelo navegador (a página costuma bloquear fetch direto). Se aparecer CAPTCHA,
  pule a fonte e cite no resumo — não tente resolver.

**ATS de empresas (Greenhouse, Lever, Ashby, Workday)**
- Busca web: `site:boards.greenhouse.io OR site:job-boards.greenhouse.io OR site:jobs.lever.co OR site:jobs.ashbyhq.com`
  + termos + "remote" + país/região. Abra a vaga para confirmar que está aberta e a data.

**Outras fontes da área/país** listadas em `criterios.md` (Revelo, Programathor, GeekHunter, Wellfound,
repositórios de vagas no GitHub etc.): use o navegador ou busca web; registre só se a candidatura acontecer
numa fonte permitida.

## 3. Pontuar e registrar
- Nota conforme `criterios.md` (ver fase 4). Elimine incompatíveis antes de pontuar o resto.
- Deduplicação: mesmo `doc_id`, ou mesma empresa + cargo (mesmo vindo de outra fonte).
- Teto diário (`teto_diario`) contado por `encontradaEm` de hoje no fuso do config.
- Grave com `ArtifactData` (`batch`, op `set`, collection `vagas`). Campos e ids em
  [06-rastreador](06-rastreador.md).

## 4. CV ajustado por vaga (por palavra-chave, para ATS)
Só trocar título + 1 frase + ordem das competências cobria ~55% dos termos das vagas; reescrever por
palavra-chave chega a ~95%. Para cada vaga:
1. Salve a descrição completa da vaga em `<pasta>/lotes/jd/<arquivo>.txt`.
2. Leia a seção "Inventário ATS" do `perfil-mestre.md` (fase 2).
3. Escreva `<pasta>/lotes/<AAAA-MM-DD-HHMM>.json` (formato em `templates/lote-exemplo.json`):
   - `titulo`: nome do cargo da vaga + 2–3 termos dela, sem prometer o que o usuário não é.
   - `resumo`: resumo **inteiro** reescrito (5–6 linhas) com os termos **exatos** da vaga (mesma grafia: se a
     vaga diz "Node.js", não escreva "Node") e só fatos do perfil mestre. (`foco` continua aceito: 1 frase
     prefixada ao resumo-base.)
   - `palavras_chave`: 12–25 termos da vaga que são verdadeiros no inventário, na grafia da vaga — viram a
     primeira linha de competências, "Aderência à vaga" ("Job match" em EN).
   - `bullets_extra` (opcional): `{"Empresa do CV-base": ["bullet"]}` — só fatos que o usuário descreveu.
   - `stack` (opcional): `{"Empresa do CV-base": "Stack: …"}` — linha sob o cargo; substitui a do CV-base.
   - `competencias_primeiro`, `lang`, `pretensao`, `notas` (envio manual, prazo, perguntas a confirmar).
   - `vaga_texto`: `"lotes/jd/<arquivo>.txt"`.
4. Rode:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/tailor.py" "<pasta>/lotes/<arquivo>.json"
```
   Ele grava `<pasta>/vagas/<arquivo>-ats.md` com a cobertura (termos da vaga presentes/faltando).
5. **Meta ≥ 90%.** Abaixo disso, acrescente em `palavras_chave`/`resumo` os termos faltantes **que forem
   verdade** no inventário e rode de novo. Termo nível 1 ou não marcado no questionário **não entra**; nunca
   invente experiência, empresa, número ou tecnologia. Cobertura menor que 90% com tudo verdadeiro é normal.
6. Grave a cobertura no rastreador: campo numérico `cobertura` (0–100) e o % na `obs`.

O dicionário de termos do `ats_check.py` é voltado a tecnologia. Para outra área, crie
`<pasta>/ats-termos.json` (`{"Termo": ["apelido", "outro"]}`); o `tailor.py` usa automaticamente.

## 5. Agendar
Preencha os `{{...}}` de `<pasta>/tarefa-varredura.md` (caminhos absolutos, URL do rastreador, resumo de 1
linha do perfil, cargos-alvo unidos por OR) e crie a tarefa com a ferramenta de agendamento disponível no ambiente:
- **App Claude (desktop):** ferramenta de tarefas agendadas (`scheduled-tasks`), com a cadência do
  `criterios.md` (ex.: cron `0 8-20 * * 1-5` e outra `0 10 * * 0,6`).
- **CLI:** a skill `schedule`/rotinas, ou um cron do sistema chamando `claude -p "<prompt>"` na pasta.
Confirme com o usuário o horário e mostre como pausar/remover a tarefa.

Com Gmail/Google Calendar conectados, a mesma tarefa faz a checagem de e-mail e agenda
([09-email-e-agenda](09-email-e-agenda.md)) na frequência de `checagem_email`. Confira que a tarefa
agendada tem acesso aos conectores; se não tiver, a checagem fica para as sessões com o usuário.

A tarefa agendada roda sem o usuário: ela **não** pode enviar, mandar mensagem, editar perfil nem publicar.
Se uma fonte pedir login, ela pula e relata.
