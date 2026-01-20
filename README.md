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

*A ser preenchido após a otimização dos prompts*

### Técnicas escolhidas:
1. **[Técnica 1]**: Justificativa...
2. **[Técnica 2]**: Justificativa...

### Exemplos práticos:
*Exemplos de como cada técnica foi aplicada...*

## Resultados Finais

*A ser preenchido após avaliação*

### Link do LangSmith Dashboard
*Link público do dashboard...*

### Comparativo v1 vs v2

| Métrica | v1 (inicial) | v2 (otimizado) |
|---------|--------------|----------------|
| Tone Score | - | - |
| Acceptance Criteria | - | - |
| User Story Format | - | - |
| Completeness | - | - |
| **Média** | - | - |

## Licença

MIT
