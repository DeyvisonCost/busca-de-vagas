# Fase 1 — Entrevista

Objetivo: coletar tudo que as fases seguintes precisam, sem o usuário ter que escrever um texto longo.

## Como conduzir
- Use `AskUserQuestion` para perguntas de múltipla escolha (até 4 por chamada, com opção "Outro" automática)
  e perguntas abertas no chat para o que é texto livre. Encadeie: a resposta de um bloco decide o próximo.
- **Peça fontes primeiro**: CV antigo (PDF/DOCX), link ou export do LinkedIn, áudios/transcrições, avaliações
  de desempenho, portfólio. Extraia o máximo delas e só pergunte o que faltar ou estiver ambíguo.
  Se o usuário mandar áudio, transcreva/resuma e confirme os números.
- Nunca preencha lacunas por dedução ("deve ter uns 5 anos"). Pergunte ou marque `[CONFIRMAR]`.
- Registre as respostas direto no `perfil-mestre.md` e no `criterios.md` à medida que avança, para não perder
  nada se a sessão cair.

## Antes de perguntar: pré-requisitos
Confira na sessão (sem perguntar o que dá para checar) se há: ferramenta Artifact com banco, navegador
interno, tarefas agendadas e conectores **Gmail** e **Google Calendar** (Drive opcional). Diga ao usuário em
2–3 linhas o que está disponível e o que falta, com o passo para ativar (SKILL.md, "Pré-requisitos").
Sem conector, siga e avise o que fica manual. Registre em `config.json` → `conectores`.

## Blocos de perguntas (nesta ordem)

1. **Idioma de trabalho** — conversar e gerar arquivos em PT, EN ou ambos? (decide `--lang` e quais CVs).
2. **Alvo** — cargo-alvo; cargos alternativos aceitos e em que condição; senioridade; anos de experiência
   total e, se houver, de liderança (pessoas lideradas diretamente/indiretamente).
3. **Competências** — stack/ferramentas/métodos que domina de verdade × que conhece; o que NÃO quer mais fazer.
4. **Histórico** — por empresa: nome, cargo, datas (mm/aaaa), contexto do produto, time, decisões.
   Empresas que devem ficar fora do CV. Formação e certificações.
5. **Conquistas com números** — para cada empresa, 2–4 resultados: antes → depois, tamanho, prazo, receita,
   custo, usuários. Pergunte quais números podem ser citados e quais só como ordem de grandeza.
6. **Idiomas** — nível real separado: leitura, escrita, conversação, entrevista. Está estudando? Isso alimenta
   o ajuste de nota (vaga que exige fluência acima do nível real perde pontos).
7. **Modelo e local** — remoto/híbrido/presencial (o que é eliminatório), cidade/UF/país, aceita mudar?
8. **Regime e dinheiro** — CLT/PJ/contractor/USD; pretensão e **piso** por cargo e regime; último salário
   (uso interno). Benefícios que pesam.
9. **Urgência e sigilo** — está empregado? prazo? **pode notificar a empresa atual?** Perfis podem ficar
   pesquisáveis? Open to Work visível ou só recrutadores?
10. **Volume e cadência** — quantas candidaturas por dia; horários de varredura (ex.: dias úteis de hora em
    hora 08–20h; fim de semana 1x); fuso.
11. **Plataformas** — onde já tem conta (LinkedIn, Gupy, Indeed, Glassdoor, Revelo, Programathor, GeekHunter,
    Wellfound, Turing, Strider…) e se estão atualizadas.
12. **Autonomia** — o que pode ser enviado sem revisão; o que precisa de aprovação (ex.: LinkedIn sempre
    manual; mensagens sempre revisadas); respostas-padrão (disponibilidade, aviso prévio, links).
13. **E-mail e agenda** (se os conectores existirem) — pode ler o Gmail e a agenda para acompanhar
    processos? Com que frequência (cada varredura ou 1x/dia → `checagem_email`)? Algum e-mail/remetente fora
    de limites? Lembre que é só leitura: nada é enviado, arquivado ou aceito sem pedido.

## Saída
- `perfil-mestre.md` com seções Dados, Posicionamento, Experiência, Competências, Formação, Decisões e
  Pendências preenchidas (ver fase 2).
- Rascunho de `criterios.md` com cargos, pisos, eliminatórios, idioma, volume, fontes e regras de envio
  (ver fase 4).
- Lista de `[CONFIRMAR]` restantes, mostrada ao usuário.
