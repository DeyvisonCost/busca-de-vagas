# Fase 4 — Critérios e plano

Gere `<pasta>/criterios.md` a partir de `templates/criterios.md` com as respostas da entrevista, e ajuste
`<pasta>/config.json`. Mostre ao usuário e peça aprovação; mudanças futuras também só com aprovação,
anotando a data ao lado do item alterado.

## Nota de compatibilidade (0–10)
| Critério | Peso | Como pontuar |
|---|---|---|
| Cargo | 3 | 3 = cargo-alvo ou sinônimo; 2 = ampliação aprovada; 0 = fora |
| Stack/competências | 2 | 2 = maioria das exigências no perfil; 1 = parte; 0 = pouca |
| Modelo de trabalho | 2 | **eliminatório** se incompatível (ex.: híbrido quando só aceita remoto) |
| Salário | 1 | 1 = informado ≥ piso ou não informado; 0 = abaixo do piso |
| Senioridade | 1 | 1 = compatível com anos de experiência/liderança |
| Publicada há ≤ 24h | 1 | 1 = sim; 0 = mais antiga ou sem data |

- **Corte configurável** (`corte_nota` no config.json; padrão 6). Abaixo do corte, não registra.
- **Ajuste por idioma:** −3 quando a vaga exige fluência acima do nível real do usuário; sem desconto quando
  pede só leitura/escrita, não menciona ou aceita o nível dele.
- Os pesos podem mudar por usuário (ex.: quem aceita híbrido tira o eliminatório). Mantenha soma 10.

## Fontes
- **Permitidas:** LinkedIn, Gupy, Indeed, Glassdoor, Revelo, Programathor, GeekHunter, Wellfound, Turing,
  Strider, repositórios de vagas no GitHub da área, e ATS das empresas (Greenhouse, Lever, Ashby, Workday,
  página de carreiras). Ajuste ao país e à área do usuário.
- **Proibidas (agregadores/intermediários):** Jobbol, DivulgaVagas, BuscarVagas, Empregando Brasil,
  Joblet-AI e qualquer site que peça cadastro próprio para "liberar" a vaga, cobre taxa ou não identifique o
  empregador. Antes de descartar uma vaga do LinkedIn que leva a agregador, procure a mesma vaga no Indeed ou
  no ATS da empresa.

## Regras de envio e respostas-padrão
Defina com o usuário (seções correspondentes do template): o que pode ir sem revisão, o que é sempre manual
(LinkedIn por padrão), como tratar CAPTCHA, perguntas factuais, pretensão por regime, disponibilidade,
links. Copie as respostas-padrão também para `respostas_padrao` no `config.json` (o `tailor.py` as escreve
em cada `-respostas.md`).

## Plano
Termine a fase com um plano curto: volume diário, horários de varredura, meta de entrevistas por semana
(`meta_entrevistas_semana`), e o que o usuário faz por dia (ex.: 10 min para revisar e dizer "envia o lote").
