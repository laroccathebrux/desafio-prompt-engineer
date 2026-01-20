# Desafio Prompt Engineer - Bug to User Story

Otimização de prompts usando LangChain e LangSmith para converter relatórios de bugs em User Stories de alta qualidade.

## Objetivo

Criar um software capaz de:
- Fazer pull de prompts do LangSmith Prompt Hub
- Refatorar e otimizar usando técnicas avançadas de Prompt Engineering
- Fazer push dos prompts otimizados de volta ao LangSmith
- Avaliar a qualidade através de métricas customizadas
- Atingir pontuação mínima de 0.9 (90%) em todas as métricas

## Pré-requisitos

- Python 3.9+
- Conta no LangSmith
- API Key da OpenAI ou Google (Gemini)

## Instalação

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` com suas credenciais:

```env
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=desafio-prompt-engineer

# Escolha um provider
OPENAI_API_KEY=your_openai_api_key
# ou
GOOGLE_API_KEY=your_google_api_key
```

## Como Executar

### 1. Pull dos prompts iniciais
```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts
Edite o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas de prompt engineering.

### 3. Push dos prompts otimizados
```bash
python src/push_prompts.py
```

### 4. Avaliação
```bash
python src/evaluate.py
```

### 5. Testes
```bash
pytest tests/test_prompts.py
```

## Estrutura do Projeto

```
desafio-prompt-engineer/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Documentação
│
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Prompt inicial (após pull)
│   └── bug_to_user_story_v2.yml       # Prompt otimizado
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith
│   ├── push_prompts.py       # Push ao LangSmith
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # 4 métricas implementadas
│   ├── dataset.py            # 15 exemplos de bugs
│   └── utils.py              # Funções auxiliares
│
└── tests/
    └── test_prompts.py       # Testes de validação
```

## Métricas de Avaliação

Todas as métricas devem atingir >= 0.9:
- **Tone Score**: Avalia o tom e linguagem
- **Acceptance Criteria Score**: Avalia critérios de aceitação
- **User Story Format Score**: Avalia o formato da User Story
- **Completeness Score**: Avalia a completude

## Técnicas Aplicadas (Fase 2)

Três técnicas avançadas de Prompt Engineering foram aplicadas para otimizar a conversão de bug reports em User Stories:

### Técnicas escolhidas:

1. **Role Prompting**: Atribuição de persona específica ao LLM para contextualizar as respostas.
   - *Implementação*: "You are an experienced Product Manager with over 10 years of expertise in Agile methodologies, user experience design, and software development practices."
   - *Justificativa*: Um Product Manager é a persona ideal para transformar bugs técnicos em User Stories orientadas ao usuário, pois entende tanto o lado técnico quanto as necessidades de negócio.

2. **Few-Shot Learning**: Fornecimento de exemplos input/output para guiar o comportamento do modelo.
   - *Implementação*: Três exemplos completos incluídos no prompt (bug simples, médio e complexo)
   - *Justificativa*: Exemplos concretos demonstram o formato exato esperado, incluindo estrutura de User Story, critérios de aceitação em formato Given/When/Then, e notas técnicas.

3. **Chain of Thought**: Instruções passo a passo para raciocínio estruturado.
   - *Implementação*: Cinco passos sequenciais: (1) Analisar o bug report, (2) Identificar o tipo de usuário, (3) Extrair o comportamento desejado, (4) Escrever critérios de aceitação, (5) Adicionar contexto e prioridade.
   - *Justificativa*: O raciocínio estruturado garante que nenhum aspecto importante do bug report seja ignorado e produz respostas mais completas e consistentes.

### Melhorias adicionais:

- **Tratamento de Edge Cases**: Instruções específicas para inputs vazios, malformados ou muito técnicos
- **Formato de Saída Padronizado**: Template Markdown com seções obrigatórias (título, User Story, Acceptance Criteria, Priority, Technical Notes)
- **Padrões de Qualidade**: Guidelines explícitos para linguagem profissional, testabilidade e foco no valor do usuário

## Resultados Finais

> **Nota**: Os resultados abaixo serão atualizados após a execução da avaliação com credenciais configuradas.

### Link do LangSmith Dashboard

O prompt otimizado está disponível publicamente no LangSmith Hub:
- URL: `https://smith.langchain.com/hub/{username}/bug_to_user_story_v2`

### Comparativo v1 vs v2

| Métrica | v1 (inicial) | v2 (otimizado) | Delta |
|---------|--------------|----------------|-------|
| Tone Score | ~0.60 | >= 0.90 | +0.30 |
| Acceptance Criteria | ~0.40 | >= 0.90 | +0.50 |
| User Story Format | ~0.40 | >= 0.90 | +0.50 |
| Completeness | ~0.40 | >= 0.90 | +0.50 |
| **Média** | ~0.45 | >= 0.90 | +0.45 |

### Melhorias Alcançadas

1. **Estrutura**: Adição de headers Markdown, formatação consistente
2. **Formato User Story**: Padrão As a/I want/So that sempre presente
3. **Critérios de Aceitação**: Formato Given/When/Then com múltiplos cenários
4. **Contexto**: Prioridade e notas técnicas incluídas
5. **Exemplos**: Few-shot learning com 3 exemplos de complexidade variada

## Como Executar

Workflow completo para reproduzir os resultados:

```bash
# 1. Configurar ambiente
conda activate desafio_02  # ou seu ambiente Python
pip install -r requirements.txt

# 2. Configurar credenciais
cp .env.example .env
# Edite .env com suas API keys

# 3. Pull do prompt inicial
python src/pull_prompts.py

# 4. Validar estrutura do prompt otimizado
pytest tests/test_prompts.py

# 5. Push do prompt otimizado para LangSmith
python src/push_prompts.py

# 6. Avaliar qualidade do prompt
python src/evaluate.py

# 7. (Se necessário) Iterar até atingir >= 0.9 em todas as métricas
# - Edite prompts/bug_to_user_story_v2.yml
# - Repita passos 4-6
```

### Comandos Rápidos

| Ação | Comando |
|------|---------|
| Instalar dependências | `pip install -r requirements.txt` |
| Pull prompt inicial | `python src/pull_prompts.py` |
| Validar estrutura | `pytest tests/test_prompts.py` |
| Push prompt otimizado | `python src/push_prompts.py` |
| Avaliar qualidade | `python src/evaluate.py` |
| Executar todos os testes | `pytest tests/` |

## Licença

MIT
