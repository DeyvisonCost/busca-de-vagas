# Fase 5 — Esteira (varredura agendada)

Busca → pontua → registra no rastreador → gera CV ajustado por vaga. **Nunca envia.**
Pré-requisitos: `criterios.md`, `config.json`, `cv/cv-pt.json` (e `cv-en.json` se houver vagas em inglês)
e o rastreador publicado (fase 6) com a URL gravada em `config.json` → `rastreador_url`.

## 1. Fazer uma varredura manual primeiro
Rode o passo a passo de `templates/tarefa-varredura.md` uma vez na sessão, com o usuário vendo, para calibrar
termos de busca e nota. Ajuste o `criterios.md` (com aprovação) antes de agendar.

## 2. Fontes e métodos

**LinkedIn (sem login, API pública de visitante)**
- Lista: `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=<termo>&location=<país>&f_WT=2&f_TPR=r7200&start=0`
  - `f_WT`: 1 presencial, 2 remoto, 3 híbrido. `f_TPR=r<segundos>`: publicadas nos últimos N segundos
    (r3600 = 1h, r86400 = 24h). `start` pagina de 25 em 25.
  - Os ids vêm como `urn:li:jobPosting:<id>`; o HTML traz título, empresa, local e `<time datetime>`.
- Detalhe: `https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/<id>` (descrição, senioridade, tipo).
- Link público da vaga: `https://www.linkedin.com/jobs/view/<id>`.
- Confira se a candidatura é "Candidatura simplificada" (fica no LinkedIn) ou externa (veja o destino; se for
  agregador proibido, procure a vaga no ATS da empresa).

**Gupy**
- No navegador, abra `https://portal.gupy.io/job-search/term=<termo>` e, na própria página, rode
  `fetch('/api/job-search/jobs?jobName=<termo>&limit=100&offset=0').then(r => r.json())`.
- Campos úteis: `id`, `name`, `careerPageName`, `jobUrl`, `workplaceType` (`remote`/`hybrid`/`on-site`),
  `publishedDate`, `city`, `state`, `type` (regime).

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

## 4. CV ajustado por vaga
Escreva `<pasta>/lotes/<AAAA-MM-DD-HHMM>.json` (formato em `templates/lote-exemplo.json`) e rode:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/tailor.py" "<pasta>/lotes/<arquivo>.json"
```
- `titulo`: título do CV alinhado ao cargo da vaga, sem prometer o que o usuário não é.
- `foco`: 1 frase com fatos do perfil mestre que respondem às exigências da vaga. **Nunca** acrescente
  tecnologia, número ou experiência que não estão no perfil.
- `competencias_primeiro`: rótulos dos grupos `kv` da seção `skills` mais relevantes para a vaga.
- `lang`: idioma da vaga.
- `notas`: observações de envio (manual, prazo, perguntas a confirmar).

## 5. Agendar
Preencha os `{{...}}` de `<pasta>/tarefa-varredura.md` (caminhos absolutos, URL do rastreador, resumo de 1
linha do perfil) e crie a tarefa com a ferramenta de agendamento disponível no ambiente:
- **App Claude (desktop):** ferramenta de tarefas agendadas (`scheduled-tasks`), com a cadência do
  `criterios.md` (ex.: cron `0 8-20 * * 1-5` e outra `0 10 * * 0,6`).
- **CLI:** a skill `schedule`/rotinas, ou um cron do sistema chamando `claude -p "<prompt>"` na pasta.
Confirme com o usuário o horário e mostre como pausar/remover a tarefa.

Com Gmail/Google Calendar conectados, a mesma tarefa faz a checagem de e-mail e agenda
([09-email-e-agenda](09-email-e-agenda.md)) na frequência de `checagem_email`. Confira que a tarefa
agendada tem acesso aos conectores; se não tiver, a checagem fica para as sessões com o usuário.

A tarefa agendada roda sem o usuário: ela **não** pode enviar, mandar mensagem, editar perfil nem publicar.
Se uma fonte pedir login, ela pula e relata.
