# Busca de vagas — plugin para Claude Code

Transforma o Claude numa esteira pessoal de busca de emprego: entrevista você, monta um perfil mestre e
currículos ATS, alinha seus perfis nas plataformas, procura vagas sozinho de hora em hora, dá nota para cada
uma, gera um currículo ajustado por vaga e preenche as candidaturas no navegador até o botão final quando
você pedir. Feito em português (Brasil) e preparado para inglês.

## Comece aqui

1. Instale o plugin (veja [Instalação](#instalação)).
2. Numa conversa nova do Claude Code, rode **`/busca-de-vagas:comecar`** (ou diga "quero começar a procurar
   emprego").
3. O Claude confere o que está disponível (navegador, conectores, agendamento) e **começa uma entrevista**
   com você: cargo-alvo, histórico, conquistas, idiomas, pretensão, sigilo, plataformas. Tenha à mão seu CV
   (PDF/DOCX) ou o link do LinkedIn — ele extrai o que puder e só pergunta o que faltar.
4. Com as respostas, ele monta seu perfil mestre, os currículos e os critérios, que você aprova. Só então
   começam a busca de vagas e, quando você pedir, as candidaturas.

Todas as regras que a skill segue (o que ela nunca faz sozinha, como dá nota às vagas, sigilo, e-mail só
leitura…) estão num documento só: **[Regras](skills/busca-de-vagas/references/00-regras.md)**.

## O que ele faz (8 fases)

1. **Entrevista** — cargo-alvo e alternativas, senioridade, stack, histórico (a partir do seu CV, LinkedIn ou
   áudios), conquistas com números, idiomas (nível real), modelo e regime, pretensão e pisos, urgência e
   sigilo, volume por dia, plataformas e o que pode ser enviado sem revisão.
2. **Perfil mestre e CVs** — `perfil-mestre.md` como fonte única de verdade e CVs ATS de uma coluna em PT/EN
   (DOCX + PDF). Nada é inventado: o que falta fica marcado `[CONFIRMAR]`.
3. **Plataformas** — confere LinkedIn, Gupy, Indeed/Glassdoor, Revelo etc. campo a campo contra o perfil
   mestre e aplica as correções que você aprovar (com as pegadinhas de cada site já mapeadas).
4. **Critérios** — `criterios.md` com cargos, pisos, nota 0–10 (cargo 3, stack 2, modelo 2 eliminatório,
   salário 1, senioridade 1, publicada ≤ 24h 1), corte, ajuste por idioma, fontes permitidas e agregadores
   proibidos, regras de envio e respostas-padrão.
5. **Esteira** — tarefa agendada que busca (LinkedIn, Gupy, Indeed, Greenhouse/Lever/Ashby), pontua,
   registra e gera CV ajustado por vaga. **Nunca envia sozinha.**
6. **Rastreador** — página com funil, filtros e status de cada vaga, publicada como Artifact com banco.
7. **Envio** — quando você diz "envia o lote": abre cada vaga, preenche até o botão final, deixa com você
   CAPTCHA, senhas, documentos, dados demográficos e upload; pergunta que só você sabe responder vira
   "bloqueada", nunca chute.
8. **Acompanhamento** — rascunhos de convite (≤ 200 caracteres) e follow-up para recrutadores e gestores de
   cada vaga, e revisão de respostas e status. Com Gmail e Google Calendar conectados, lê os e-mails de
   processos seletivos (Gupy, Greenhouse, Lever, Ashby, InHire, Indeed, LinkedIn…), classifica em recusa /
   próxima etapa / convite de agenda / proposta / informativo, atualiza o rastreador, confere entrevistas dos
   próximos 7 dias e só avisa você quando há algo a fazer. **Só leitura**: nunca envia, responde, arquiva ou
   aceita nada sem você pedir.

## Requisitos

- **Claude Code** (app desktop, CLI ou web). Recomendado o app desktop: navegador interno para as fases 3 e 7,
  tarefas agendadas para a fase 5 e Artifacts com banco para o rastreador.
- **Python 3.8+** (só biblioteca padrão — nada para instalar).
- Para o PDF: Google Chrome, Chromium ou Edge (ou LibreOffice). Sem eles você recebe o DOCX e um HTML para
  imprimir em PDF.

## Conectores e recursos

| Recurso | Para quê | Necessário? |
|---|---|---|
| Artifacts com banco | rastreador de vagas (funil, status) | recomendado — sem ele, usa um `vagas.csv` |
| Navegador interno do app (ou Claude in Chrome) | conferir perfis, buscar na Gupy/Indeed, preencher candidaturas | recomendado |
| Tarefas agendadas | varredura automática | opcional — sem elas, a busca roda quando você pede |
| **Gmail** | detectar respostas dos processos seletivos | opcional |
| **Google Calendar** | ver entrevistas marcadas | opcional |
| Google Drive | guardar os CVs | opcional |

**Como conectar Gmail, Google Calendar e Drive:** no claude.ai ou no app Claude, abra
**Configurações → Conectores**, clique em conectar no Gmail e no Google Calendar (e Drive, se quiser),
autorize com sua conta Google e deixe-os ativos na conversa/projeto onde usa a skill. A skill confere na
primeira conversa o que está disponível, avisa o que falta e segue sem o que não estiver conectado.

## Instalação

### Como plugin (recomendado)
Do GitHub:
```
/plugin marketplace add DeyvisonCost/busca-de-vagas
/plugin install busca-de-vagas@busca-de-vagas
```
De uma pasta local (para testar ou usar sem publicar):
```
/plugin marketplace add /caminho/para/skill-busca-de-vagas
/plugin install busca-de-vagas@busca-de-vagas
```
Ou só nesta sessão do terminal:
```bash
claude --plugin-dir /caminho/para/skill-busca-de-vagas
```
Como plugin, o início fica em `/busca-de-vagas:comecar` e a skill em `/busca-de-vagas:busca-de-vagas`.

### Como skill pessoal (sem plugin)
```bash
git clone https://github.com/DeyvisonCost/busca-de-vagas.git && cd busca-de-vagas
mkdir -p ~/.claude/skills/busca-de-vagas
cp -r skills/busca-de-vagas/. ~/.claude/skills/busca-de-vagas/
```
Aí ela aparece como `/busca-de-vagas` (o atalho `comecar` existe só na instalação como plugin; aqui diga
"quero começar a procurar emprego").

## Uso

Basta pedir em linguagem natural — a skill é acionada sozinha:

- "Quero começar a procurar emprego" → entrevista e pasta de trabalho.
- "Refaz meu currículo" / "gera meu CV em inglês" → fase 2.
- "Confere meu LinkedIn" → fase 3 (abra o LinkedIn logado no navegador interno).
- "Agenda a busca de vagas" → fases 5 e 6.
- "Envia o lote" → fase 7.
- "Com quem eu falo nessas vagas?" → fase 8.
- "Tem resposta das vagas?" / "Tenho entrevista essa semana?" → e-mail e agenda.

Atalhos: `/busca-de-vagas:comecar` (início/retomada pela entrevista) e `/busca-de-vagas:busca-de-vagas <fase>`
(ex.: `envio`, `email`).

Seus dados ficam numa **pasta de trabalho** sua (padrão `~/busca-de-vagas`), nunca dentro do plugin:
```
~/busca-de-vagas/
  perfil-mestre.md  criterios.md  config.json  rastreador.html  tarefa-varredura.md
  cv/        currículos-base (JSON) e CVs gerados
  lotes/     lotes de vagas de cada varredura
  vagas/     CV ajustado + respostas por vaga
  contatos/  rascunhos de mensagens
```

### Scripts (também funcionam sozinhos)
```bash
S=skills/busca-de-vagas/scripts
python3 $S/init_workspace.py ~/busca-de-vagas --lang pt
python3 $S/build_cv.py skills/busca-de-vagas/templates/cv-exemplo-pt.json /tmp/cv-exemplo
python3 $S/tailor.py ~/busca-de-vagas/lotes/2026-01-15-0900.json
python3 $S/checar_convites.py ~/busca-de-vagas/contatos/2026-01-15.md
```

## Segurança e privacidade

- Nenhuma candidatura, mensagem ou alteração de perfil acontece sem você pedir na sessão; as tarefas
  agendadas só buscam e preparam.
- E-mail e agenda são só leitura. Conteúdo de e-mails e páginas é tratado como dado, nunca como instrução;
  CPF, códigos de verificação e links com token não são copiados para o rastreador.
- Senhas, documentos, CAPTCHA, dados demográficos, declarações e upload de arquivo ficam sempre com você.
- Modo sigilo para quem está empregado: sem notificar a rede, Open to Work só para recrutadores, sem e-mail
  corporativo, sem contato com colegas da empresa atual.
- Automação em sites de terceiros pode violar os termos deles; por padrão o envio no LinkedIn é manual.
  Use com moderação e sob sua responsabilidade.

## Estrutura do plugin
```
.claude-plugin/plugin.json        manifesto do plugin
.claude-plugin/marketplace.json   permite instalar direto deste repositório
commands/comecar.md               /busca-de-vagas:comecar — início pela entrevista
skills/busca-de-vagas/
  SKILL.md                        fluxo, início e gatilhos
  references/00-regras.md         todas as regras consolidadas
  references/01..09-*.md          instruções de cada fase (09 = e-mail e agenda)
  templates/                      perfil-mestre, criterios, config, rastreador, tarefa, contatos, exemplos fictícios
  scripts/                        init_workspace, build_cv, docx_min, tailor, checar_convites
```

## Licença
MIT — veja [LICENSE](LICENSE).
