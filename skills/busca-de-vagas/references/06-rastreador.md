# Fase 6 — Rastreador

Página Artifact com banco compartilhado (coleção `vagas`): funil (na fila, enviadas, respostas, entrevistas
na semana × meta, Match ATS médio das enviadas), indicador "Match" por vaga, gráfico de horário de publicação, filtros por status, busca e troca de status pela própria
página. O HTML não contém dados pessoais: tudo vem do banco.

## Publicar
1. `<pasta>/rastreador.html` já foi gerado pelo `init_workspace.py` com título, subtítulo, idioma, fuso,
   corte e meta. Para mudar textos, apague o arquivo e rode o script de novo com outros `--title/--subtitle`.
   Não coloque nome completo, empresa atual ou salário no subtítulo (ex.: "Cargo-alvo · remoto").
2. Carregue a skill `artifact-capabilities` e publique o arquivo com a ferramenta `Artifact`, declarando as
   capacidades **db** (banco compartilhado) e **user** (para saber se quem vê pode editar). Ícone: `chart`.
3. Grave a URL retornada em `config.json` → `rastreador_url` e na memória do Claude, se disponível.
4. Ofereça fixar o rastreador na barra lateral (só se o usuário quiser).

Sem a ferramenta `Artifact` (ex.: outro ambiente), use como alternativa um `vagas.csv` na pasta de trabalho
com as mesmas colunas e diga ao usuário que o painel visual não estará disponível.

## Esquema do documento (`vagas/<doc_id>`)
| Campo | Tipo | Observação |
|---|---|---|
| `titulo`, `empresa`, `fonte`, `link` | texto | `link` = página da vaga (http/https) |
| `nota` | número | 0–10 |
| `motivo` | texto | 1 frase: por que entrou |
| `status` | texto | ver abaixo |
| `regime`, `salario` | texto | como a vaga informa |
| `publicadaEm`, `encontradaEm`, `atualizadoEm` | ISO 8601 com fuso | `publicadaEm` null se a fonte não informa |
| `envioManual` | bool | true para LinkedIn (padrão) e Indeed (CAPTCHA) |
| `cvArquivo` | texto | nome do DOCX em `<pasta>/vagas/` |
| `cobertura` | número | 0–100: % dos termos da vaga presentes no CV ajustado (`<arquivo>-ats.md`); ausente = não medido |
| `obs` | texto | prazo, idioma, pergunta bloqueante, resultado do envio |

`doc_id`: `li-<id>`, `gupy-<id>`, `indeed-<jk>`, `<fonte>-<slug-empresa-cargo>`.

## Indicador "Match"
Cada vaga mostra a `cobertura` como selo: **≥ 90 verde**, **70–89 âmbar**, **< 70 vermelho**, "–" quando não
foi medida (CV anterior ao fluxo ATS). O funil mostra o **Match ATS médio** das vagas já enviadas (enviada,
resposta, entrevista, proposta, recusada). Ao regerar o CV de uma vaga, atualize `cobertura` com `update`.

## Status
`nova` → `preparada` (CV + respostas prontos) → `enviada` → `resposta` → `entrevista` → `proposta`;
desvios: `bloqueada` (falta algo do usuário; motivo na `obs`), `recusada`, `descartada` (fora dos critérios,
vaga fechada, agregador).
Mudanças vindas de e-mail/agenda (referência 09) usam `resposta`, `entrevista`, `proposta` ou `recusada`
e acrescentam à `obs` `"[DD/MM] e-mail: <resumo>"`, sem dados sensíveis.
Ao mudar status, atualize `atualizadoEm` (a página faz isso sozinha quando o usuário troca no seletor).

## Ler e atualizar
- Ler: `ArtifactData` action `list`, collection `vagas`, limit 1000.
- Atualizar campos: action `update` (merge). Várias de uma vez: `batch`.
- Não republique a página para mudar dados; republique só se o layout mudar.
