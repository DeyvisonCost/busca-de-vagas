# Fase 7 — Envio do lote

Só começa quando o usuário pede na sessão ("envia o lote", "aplica nessas", "send the batch").
Esse pedido vale para o lote daquele momento; não vale para varreduras futuras.

## Preparar
1. Leia o rastreador (status `preparada`) e mostre a fila: empresa, cargo, nota, fonte, se é manual.
   Se o usuário escolheu revisão prévia no `criterios.md`, peça o OK da lista antes de começar.
2. Confira que existem `<pasta>/vagas/<arquivo>.pdf` e `-respostas.md` de cada vaga.

## Para cada vaga
1. Abra o link no navegador — de preferência no Claude in Chrome, que permite o upload do CV (passo 4).
   **Antes de pedir login, leia a página**: se o usuário já estiver logado, siga. Se precisar de login, peça
   uma vez para todas as plataformas pendentes e continue com as outras enquanto isso.
2. Confirme que a vaga continua aberta e compatível (modelo, cargo — confira de novo o selo remoto/híbrido
   na página). Se não, `descartada` com motivo.
3. Preencha com dados do `perfil-mestre.md`, do `-respostas.md` e dos "Dados confirmados" do `criterios.md`
   (não pergunte de novo o que já está lá; corrija dado velho salvo na plataforma, ex.: telefone antigo).
   Pretensão conforme o regime da vaga.
   - **Pergunta eliminatória de salário** (opções em faixa ou corte automático): use a faixa aceitável do
     `criterios.md` — a opção que contém o piso cheio; uma faixa abaixo só se a vaga sinaliza teto menor;
     nunca abaixo do mínimo. Campo aberto: o piso ou a faixa.
   - Resposta factual nova que o usuário der → grave em `criterios.md` → "Dados confirmados".
4. **Upload do CV** (o PDF ajustado `<pasta>/vagas/<arquivo>.pdf`): faça você mesmo com Claude in Chrome
   (`file_upload`, que injeta o arquivo no campo da página sem abrir seletor). O navegador interno do app não
   tem ferramenta de upload — nele, ou sem Claude in Chrome, avise no chat.
   - **LinkedIn Easy Apply** não tem campo de arquivo no diálogo: suba antes o PDF em
     `https://www.linkedin.com/jobs/application-settings/` (Upload resume) e escolha-o no Easy Apply.
   - **Nunca** abra um seletor de arquivo nativo nem deixe o usuário numa tela que pede ação sem dizer no
     chat: **qual vaga, qual arquivo (caminho completo) e qual aba/navegador**.
5. **Ficam com o usuário** (deixe o campo e avise): senhas, criação de conta com senha e aceite de termos,
   CPF/RG/documentos, dados bancários, dados demográficos/diversidade (gênero, raça, deficiência,
   orientação), declarações legais, CAPTCHA. Se o usuário recusar criar conta numa plataforma, registre em
   `criterios.md` e descarte as vagas que dependem dela.
6. **Pergunta factual que o perfil mestre não responde** (ex.: "tem experiência com X?", "aceita viajar?",
   "qual moeda/horário?") → não chute. Pare essa vaga, status `bloqueada`, pergunta literal na `obs`.
   Na Gupy isso é crítico: respostas não são editáveis depois.
7. Pare **no botão final** (Enviar/Submit/Candidatar). Clique só se o pedido do usuário cobre o envio sem
   revisão e a plataforma permite; senão deixe na tela de revisão para ele clicar.
   - **LinkedIn:** por padrão sempre manual (risco de restrição de conta por automação).
   - **Indeed:** reCAPTCHA no envio → usuário clica.
8. Atualize o rastreador: `enviada` (com data na `obs`), `bloqueada` (com o motivo) ou mantenha `preparada`
   com `envioManual=true` e "pronta na aba X" na `obs`.

## Fechamento
Relatório curto: enviadas, prontas para o usuário clicar (com a aba/URL), bloqueadas com a pergunta de cada
uma. Quando o usuário responder as bloqueadas, registre a resposta no `perfil-mestre.md` (se for um fato
reutilizável) e retome só essas.
