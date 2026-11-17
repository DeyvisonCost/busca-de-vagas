"""Cobertura ATS: quais termos da vaga aparecem no currículo.

Uso:
    python3 ats_check.py <vaga.txt> [cv.json] [--termos <extra.json>]

<vaga.txt>  descrição completa da vaga (copiada da página).
[cv.json]   currículo no formato de build_cv.py (padrão: cv/cv-pt.json da pasta atual).
--termos    JSON opcional {"Termo canônico": ["apelido", "outro apelido"]} que soma ao dicionário
            abaixo — use para áreas fora de tecnologia ou termos que faltam. O tailor.py usa
            automaticamente <pasta>/ats-termos.json se existir.

Também é usado pelo tailor.py quando o lote traz "vaga_texto": ele grava <arquivo>-ats.md.
Cada termo tem apelidos porque o ATS costuma casar a forma exata que está na vaga; o relatório
lista os termos da vaga presentes e os que faltam. Termo faltando só entra no currículo se for
verdade (confirmado pelo usuário no perfil-mestre / questionário ATS).
Só biblioteca padrão.
"""
import json
import re
import sys
import unicodedata

TERMS = {
    # liderança e gestão
    "Tech Lead": ["tech lead", "technical lead", "tech leader", "líder técnico", "lider tecnico", "liderança técnica"],
    "Engineering Manager": ["engineering manager", "gerente de engenharia", "engineering management"],
    "Gestão de pessoas": ["gestão de pessoas", "people management", "gestão de time", "gestão de equipe"],
    "Contratação": ["contratação", "recrutamento", "hiring", "recruiting", "entrevista técnica"],
    "1:1": ["1:1", "one-on-one", "1on1"],
    "PDI": ["pdi", "plano de desenvolvimento"],
    "Avaliação de desempenho": ["avaliação de desempenho", "performance review"],
    "Mentoria": ["mentoria", "mentoring", "mentor", "coaching"],
    "Roadmap": ["roadmap"],
    "OKR": ["okr"],
    "KPIs": ["kpi"],
    "Stakeholders": ["stakeholder"],
    "Orçamento": ["orçamento", "budget"],
    "Fornecedores": ["fornecedor", "vendor"],
    "Scrum": ["scrum"], "Kanban": ["kanban"], "SAFe": ["safe"], "Lean": ["lean"],
    "Ágil": ["ágil", "agile", "metodologias ágeis"],
    "Estimativas": ["estimativa", "estimation", "dimensionamento"],
    "Lead time": ["lead time"], "Cycle time": ["cycle time"], "DORA": ["dora"], "SLA": ["sla", "slo", "sli"],
    "Gestão de incidentes": ["incidente", "incident"],
    "Dívida técnica": ["dívida técnica", "technical debt", "tech debt"],
    # front/mobile
    "React Native": ["react native"], "Expo": ["expo"], "React": ["react"], "Next.js": ["next.js", "nextjs"],
    "TypeScript": ["typescript"], "JavaScript": ["javascript"], "Redux": ["redux"], "Flutter": ["flutter"],
    "Swift": ["swift"], "Kotlin": ["kotlin"], "Angular": ["angular"], "Vue": ["vue"],
    "Micro-frontends": ["micro-frontend", "microfrontend"], "Design System": ["design system"],
    "Mobile": ["mobile"], "Front-end": ["front-end", "frontend"],
    # back
    "Node.js": ["node.js", "nodejs", "node"], "NestJS": ["nestjs", "nest.js"], "Express": ["express"],
    "REST": ["rest", "restful"], "GraphQL": ["graphql"], "gRPC": ["grpc"], "WebSockets": ["websocket"],
    "Python": ["python"], "Java": ["java"], "Spring": ["spring"], "Go": ["golang", " go "], "C#/.NET": [".net", "c#", "dotnet"],
    "PHP": ["php", "laravel"], "Ruby on Rails": ["ruby", "rails"], "Back-end": ["back-end", "backend"],
    "APIs": ["api"], "Full Stack": ["full stack", "fullstack", "full-stack"],
    # arquitetura
    "System Design": ["system design", "design de sistemas"],
    "Arquitetura de software": ["arquitetura de software", "software architecture", "arquitetura"],
    "Microsserviços": ["microsserviço", "microserviço", "microservice", "micro-serviço"],
    "Event-driven": ["orientada a eventos", "event-driven", "event driven", "eventos"],
    "DDD": ["ddd", "domain-driven"], "Clean Architecture": ["clean architecture", "arquitetura limpa"],
    "Hexagonal": ["hexagonal"], "SOLID": ["solid"], "Design Patterns": ["design pattern", "padrões de projeto"],
    "CQRS": ["cqrs"], "Serverless": ["serverless"],
    "Sistemas distribuídos": ["sistemas distribuídos", "distributed systems"],
    "Escalabilidade": ["escalabilidade", "escaláve", "scalab"],
    "Alta disponibilidade": ["alta disponibilidade", "high availability"],
    "Legado": ["legado", "legacy", "modernização"], "C4 Model": ["c4"], "API Gateway": ["api gateway"],
    # dados/mensageria
    "PostgreSQL": ["postgres"], "MySQL": ["mysql"], "SQL Server": ["sql server"], "Oracle": ["oracle"], "SQL": ["sql"],
    "MongoDB": ["mongo"], "Redis": ["redis"], "DynamoDB": ["dynamo"], "Elasticsearch": ["elasticsearch", "opensearch"],
    "Kafka": ["kafka"], "RabbitMQ": ["rabbitmq", "rabbit"], "SQS/SNS": ["sqs", "sns"],
    "Mensageria": ["mensageria", "messaging", "filas", "queue"],
    "dbt": ["dbt"], "Airflow": ["airflow"], "Spark": ["spark", "pyspark"], "Databricks": ["databricks"],
    "Snowflake": ["snowflake"], "BigQuery": ["bigquery"], "Redshift": ["redshift"],
    "Data warehouse": ["data warehouse", "dwh", "data lake", "lakehouse"], "ETL/ELT": ["etl", "elt", "pipeline de dados", "data pipeline"],
    "Modelagem de dados": ["modelagem de dados", "data modeling", "modelagem dimensional"],
    "Qualidade de dados": ["qualidade de dados", "data quality", "testes de dados", "data testing"],
    "Power BI": ["power bi"], "Looker": ["looker"], "Tableau": ["tableau"],
    # cloud/devops
    "AWS": ["aws", "amazon web services"], "GCP": ["gcp", "google cloud"], "Azure": ["azure"],
    "Docker": ["docker", "container"], "Kubernetes": ["kubernetes", "k8s", "eks", "aks"], "Terraform": ["terraform"],
    "IaC": ["infraestrutura como código", "infrastructure as code", "iac"],
    "CI/CD": ["ci/cd", "ci cd", "pipeline", "integração contínua"],
    "GitHub Actions": ["github actions"], "GitLab CI": ["gitlab"], "Azure DevOps": ["azure devops"], "Jenkins": ["jenkins"],
    "DevOps": ["devops"], "Cloud": ["cloud", "nuvem"], "Linux": ["linux"], "Git": ["git"],
    # qualidade/observabilidade
    "Testes automatizados": ["testes automatizados", "automated test", "testes unitários", "unit test",
                             "testes de integração", "e2e"],
    "TDD": ["tdd"], "BDD": ["bdd"], "Jest": ["jest"], "Cypress": ["cypress"], "Playwright": ["playwright"],
    "Code review": ["code review", "revisão de código"], "SonarQube": ["sonar"],
    "Observabilidade": ["observabilidade", "observability", "monitoramento", "monitoring"],
    "Grafana": ["grafana"], "Prometheus": ["prometheus"], "Datadog": ["datadog"], "New Relic": ["new relic"],
    "ELK/Kibana": ["kibana", "elk"], "Sentry": ["sentry"], "OpenTelemetry": ["opentelemetry"], "APM": ["apm"],
    # segurança
    "Segurança": ["segurança", "security"], "OWASP": ["owasp"], "LGPD": ["lgpd"], "OAuth": ["oauth"],
    "JWT": ["jwt"], "SSO": ["sso"],
    # IA
    "IA": ["inteligência artificial", "artificial intelligence", " ia ", " ai ", "ai-first", "ia generativa",
           "genai", "generative ai"],
    "LLM": ["llm"], "RAG": ["rag"], "Agentes de IA": ["agente", "agent", "agêntic", "agentic"],
    "MCP": ["mcp", "model context protocol"], "Prompt engineering": ["prompt"], "Claude Code": ["claude"],
    "Cursor": ["cursor"], "Copilot": ["copilot"], "OpenAI": ["openai", "gpt"], "Bedrock": ["bedrock"],
    "LangChain": ["langchain"], "Embeddings": ["embedding", "vetorial", "vector"],
    "Machine Learning": ["machine learning", "aprendizado de máquina"], "OCR": ["ocr"],
    # domínio
    "Fintech": ["fintech"], "Pagamentos": ["pagamento", "payment"], "Pix": ["pix"], "Health tech": ["saúde", "health"],
    "E-commerce": ["e-commerce", "ecommerce"], "Marketplace": ["marketplace"], "SaaS": ["saas"], "B2B": ["b2b"],
    # ferramentas
    "Jira": ["jira"], "Confluence": ["confluence"], "Figma": ["figma"],
}

# apelidos curtos ou ambíguos que só casam como palavra inteira
WHOLE_WORD = {"react", "node", "rest", "java", "git", "lean", "safe", "solid", "sql", "rails", "ruby", "go", "spark"}


def norm(t):
    t = unicodedata.normalize("NFKC", t).lower()
    return " " + re.sub(r"[\s/|·,;()]+", " ", t) + " "


def has(text, alias):
    a = alias.lower()
    if a.startswith(" ") or len(a) <= 4 or a in WHOLE_WORD:
        return re.search(r"(?<![a-z0-9])" + re.escape(a.strip()) + r"(?![a-z0-9])", text) is not None
    return a in text


def found(text, terms=None):
    t = norm(text)
    return [k for k, al in (terms or TERMS).items() if any(has(t, a) for a in al)]


def load_terms(extra_path=None):
    terms = dict(TERMS)
    if extra_path:
        with open(extra_path, encoding="utf-8") as f:
            for k, v in json.load(f).items():
                terms[k] = list(v) if isinstance(v, list) else [str(v)]
    return terms


def cv_text(cv):
    """Texto corrido de um currículo no formato de build_cv.py (title + todas as seções)."""
    parts = [cv.get("title", "")]
    for s in cv.get("sections", []):
        for it in s.get("items", []):
            parts += [str(x) for x in it[1:]]
    return "\n".join(parts)


def coverage(jd, cv, terms=None):
    """Retorna (pct, presentes, faltando)."""
    want = found(jd, terms)
    got = set(found(cv, terms))
    hit = [k for k in want if k in got]
    miss = [k for k in want if k not in got]
    return round(100 * len(hit) / max(len(want), 1)), hit, miss


def report(jd, cv, terms=None):
    pct, hit, miss = coverage(jd, cv, terms)
    out = ["# Cobertura ATS", "",
           f"Cobertura: {pct}% ({len(hit)} de {len(hit) + len(miss)} termos da vaga aparecem no currículo)", "",
           "## Presentes", ", ".join(hit) or "—", "",
           "## Faltando (incluir só se for verdade — via palavras_chave, resumo ou bullets_extra)",
           ", ".join(miss) or "—", ""]
    return "\n".join(out)


def main(argv):
    extra = None
    if "--termos" in argv:
        i = argv.index("--termos")
        extra = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        sys.exit(__doc__)
    with open(argv[0], encoding="utf-8") as f:
        jd = f.read()
    cv_path = argv[1] if len(argv) > 1 else "cv/cv-pt.json"
    with open(cv_path, encoding="utf-8") as f:
        cv = json.load(f)
    print(report(jd, cv_text(cv), load_terms(extra)))


if __name__ == "__main__":
    main(sys.argv[1:])
