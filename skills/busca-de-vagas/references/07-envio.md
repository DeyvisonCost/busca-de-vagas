# Fase 7 — Envio do lote

Só começa quando o usuário pede na sessão ("envia o lote", "aplica nessas", "send the batch").
Esse pedido vale para o lote daquele momento; não vale para varreduras futuras.

## Preparar
1. Leia o rastreador (status `preparada`) e mostre a fila: empresa, cargo, nota, fonte, se é manual.
   Se o usuário escolheu revisão prévia no `criterios.md`, peça o OK da lista antes de começar.
2. Confira que existem `<pasta>/vagas/<arquivo>.pdf` e `-respostas.md` de cada vaga.

## Para cada vaga
1. Abra o link no navegador interno. **Antes de pedir login, leia a página**: se o usuário já estiver logado,
   siga. Se precisar de login, peça uma vez para todas as plataformas pendentes e continue com as outras
   enquanto isso.
2. Confirme que a vaga continua aberta e compatível (modelo, cargo). Se não, `descartada` com motivo.
3. Preencha com dados do `perfil-mestre.md` e do `-respostas.md`. Pretensão conforme o regime da vaga.
4. **Ficam com o usuário** (deixe o campo e avise): senhas, CPF/RG/documentos, dados bancários, dados
   demográficos (gênero, raça, deficiência, orientação), declarações legais/termos, **upload de arquivo**
   (indique o caminho do PDF certo), CAPTCHA.
5. **Pergunta factual que o perfil mestre não responde** (ex.: "tem experiência com X?", "aceita viajar?",
   "qual moeda/horário?") → não chute. Pare essa vaga, status `bloqueada`, pergunta literal na `obs`.
   Na Gupy isso é crítico: respostas não são editáveis depois.
6. Pare **no botão final** (Enviar/Submit/Candidatar). Clique só se o pedido do usuário cobre o envio sem
   revisão e a plataforma permite; senão deixe na tela de revisão para ele clicar.
   - **LinkedIn:** por padrão sempre manual (risco de restrição de conta por automação).
   - **Indeed:** reCAPTCHA no envio → usuário clica.
7. Atualize o rastreador: `enviada` (com data na `obs`), `bloqueada` (com o motivo) ou mantenha `preparada`
   com `envioManual=true` e "pronta na aba X" na `obs`.

## Fechamento
Relatório curto: enviadas, prontas para o usuário clicar (com a aba/URL), bloqueadas com a pergunta de cada
uma. Quando o usuário responder as bloqueadas, registre a resposta no `perfil-mestre.md` (se for um fato
reutilizável) e retome só essas.
