# Fase 8 — Acompanhamento e contato

## Contatos no LinkedIn (rascunhos — o usuário envia)
Para cada vaga enviada (prioridade por nota):
1. Encontre 1–2 pessoas: recrutador(a)/talent acquisition da empresa, gestor(a) da área ou um par técnico do
   time. Use a busca do LinkedIn no navegador (o usuário logado) ou busca web
   `site:linkedin.com/in "<empresa>" recruiter`. **Nunca** pessoas da empresa atual do usuário se há sigilo.
2. Escreva em `<pasta>/contatos/<AAAA-MM-DD>.md` seguindo `templates/contatos.md`:
   - **Convite ≤ 200 caracteres** (limite de nota no plano gratuito): nome, vaga, 1 fato do perfil que conecta
     com a vaga, pedido leve. Sem anexos, sem "por favor me contrate".
   - **Follow-up** para quando aceitar: 2–4 frases, um resultado com número, onde se candidatou, abertura
     para conversa ou indicação.
   - Só fatos do perfil mestre. Não cite números marcados como "só ordem de grandeza".
3. Rode `python3 "${CLAUDE_SKILL_DIR}/scripts/checar_convites.py" <arquivo>` e corrija o que passar do limite.
4. Tabela de prioridade no topo (empresa, pessoa, por quê). Lembre que a conta gratuita tem limite mensal de
   convites com nota: priorize.
5. **Não envie** convites nem mensagens: ações no LinkedIn são do usuário (ou só com pedido explícito e
   confirmação de cada mensagem).

## Revisão de respostas e status
- Com os conectores Gmail e Google Calendar ativos, comece por [09-email-e-agenda](09-email-e-agenda.md):
  busca as respostas desde a última checagem, classifica (recusa / próxima etapa / convite de agenda /
  proposta / informativo), atualiza o rastreador e confere entrevistas dos próximos 7 dias. Só leitura.
- Quando o usuário contar novidades (e-mail de recrutador, teste técnico, recusa), atualize o rastreador
  (`resposta`, `entrevista`, `proposta`, `recusada`) com a data e próximo passo na `obs`.
- Resposta a recrutador: proponha o rascunho no chat; enviar só com pedido explícito e o texto aprovado.
- Semanalmente: resuma o funil (enviadas, taxa de resposta, entrevistas × meta), os horários de publicação
  mais frequentes (gráfico do rastreador) e proponha ajustes de critérios ou termos — aplicar só com aprovação.
- Prepare a entrevista quando marcada: resumo da empresa e da vaga, perguntas prováveis, histórias do perfil
  mestre (formato situação → ação → resultado).
