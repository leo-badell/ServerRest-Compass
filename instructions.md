# Instructions — Assistência de IA para os testes E2E

Estas instruções orientam o uso de IA neste projeto Python + Pytest + Requests.

## Script generation

- Seguir a estrutura existente.
- Reutilizar helpers, fixtures e factories.
- Manter requisições HTTP nos helpers.
- Criar happy paths e falhas documentadas.
- Não inventar status codes ou regras não definidas pelo contrato.
- Usar nomes de testes descritivos.
- Incluir cleanup quando houver persistência de massa.
- Antes de criar um novo helper ou fixture, verificar se já existe uma implementação reutilizável.
- Manter os testes independentes sempre que possível.
- Não depender da ordem de execução dos testes.
- Utilizar parametrização do Pytest quando vários cenários validarem a mesma regra com massas diferentes.

## Refactoring

- Preservar comportamento.
- Remover duplicação e imports não utilizados.
- Manter HTTP em `helpers/`, massas em `fixtures/`, configuração em `config.py` e assertions nos testes.
- Evitar imports internos sem necessidade.
- Fazer alterações pequenas e verificáveis.
- Rodar regressão após refatorar.
- Não alterar assertions apenas para fazer um teste falho passar.
- Não alterar comportamento funcional durante uma refatoração sem informar explicitamente.
- Priorizar legibilidade e manutenção em vez de abstrações desnecessárias.

A arquitetura esperada é:

```text
Data Factory
     ↓
Fixtures
     ↓
Helpers HTTP
     ↓
Testes E2E
     ↓
Assertions
     ↓
Cleanup
```

## Fixtures

- Usar `yield` quando houver setup + cleanup.
- Reutilizar autenticação.
- Evitar dependências circulares.
- Compor fixtures quando útil: usuário → token → produto → carrinho.
- Não esconder na fixture a assertion principal do cenário.
- Garantir cleanup mesmo quando o teste falhar, sempre que possível.
- Evitar massas fixas que possam gerar conflito entre execuções.
- Preferir dados únicos gerados pelas factories.
- Não criar fixtures duplicadas quando uma fixture existente puder ser reutilizada.

## Debugging

Ao investigar uma falha:

1. Ler o traceback completo.
2. Identificar se a falha está na coleta, fixture, helper, HTTP ou assertion.
3. Diferenciar problema do teste de problema da API/ambiente.
4. Conferir payload, headers, token, status e body.
5. Verificar contaminação de massa.
6. Verificar timeout e disponibilidade do ambiente.
7. Rodar o teste isoladamente.
8. Comparar o comportamento observado com o contrato da API.
9. Só então alterar código.

Nunca alterar um `assert` apenas para transformar um teste vermelho em verde.

Se o comportamento observado for diferente do contrato documentado, reportar a diferença antes de modificar o teste.

Comandos úteis:

```bash
pytest tests/caminho/teste.py -v --tb=short
pytest tests/caminho/teste.py::nome_do_teste -v
pytest tests --collect-only -v
pytest tests -v --tb=short
```

## Suggestions

- Diferenciar correção necessária de melhoria opcional.
- Priorizar legibilidade, manutenção, isolamento e confiabilidade.
- Explicar o benefício de cada sugestão.
- Evitar complexidade sem ganho claro.
- Informar possíveis impactos antes de alterações estruturais.
- Não adicionar bibliotecas sem justificar sua necessidade.
- Manter sugestões compatíveis com a arquitetura atual do projeto.
- Priorizar melhorias incrementais que possam ser verificadas pela suíte existente.

## Coverage review

Revisar:

- endpoints e métodos HTTP;
- happy paths;
- erros documentados;
- autenticação e autorização;
- campos obrigatórios e tipos;
- IDs inexistentes;
- duplicidades e filtros;
- persistência após POST/PUT;
- remoção após DELETE;
- regras de negócio e efeitos entre recursos;
- cenários de integração entre usuário, produto e carrinho;
- possíveis edge cases documentados.

Distinguir:

### Endpoint coverage

Verifica quais endpoints e métodos HTTP possuem testes.

### Scenario coverage

Verifica quais happy paths, cenários negativos e edge cases foram implementados.

### Business rule coverage

Verifica quais regras de negócio foram realmente validadas pelos testes.

### Code coverage

Representa o percentual de código executado e exige instrumentação específica.

Não inferir percentual de cobertura de código apenas porque todos os testes passaram.

Por exemplo:

```text
63 passed
```

não significa:

```text
100% code coverage
```

## Validação final

Antes de considerar uma alteração concluída, verificar a coleta:

```bash
pytest tests --collect-only -v
```

Depois executar a regressão:

```bash
pytest tests -v --tb=short
```

Uma alteração é considerada estável quando os testes esperados são coletados e a suíte relevante passa, salvo falha conhecida e documentada do ambiente ou aplicação.

---

# Dashboard and reporting

O projeto possui uma camada de visualização e análise dos resultados:

```text
tests
  ↓
Pytest
  ↓
pytest-json-report
  ↓
reports/test_results.json
  ↓
Pandas
  ↓
Streamlit / Plotly
  ↓
dashboard/app.py
```

O dashboard deve utilizar exclusivamente resultados provenientes da execução real dos testes.

## Responsabilidades do dashboard

O dashboard pode apresentar:

- total de testes;
- testes aprovados;
- testes com falha;
- testes ignorados;
- taxa de sucesso;
- resultados por módulo;
- duração dos testes;
- testes mais lentos;
- tabelas de detalhamento;
- tendências históricas, caso sejam implementadas futuramente.

Os módulos atualmente considerados são:

```text
login
usuarios
produtos
carrinhos
```

## Geração do relatório

O relatório utilizado pelo dashboard deve ser produzido pelo Pytest:

```bash
pytest tests -v --json-report --json-report-file=reports/test_results.json
```

O dashboard não deve criar resultados fictícios quando o relatório não existir.

## Execução do dashboard

```bash
streamlit run dashboard/app.py
```

O dashboard deve ler:

```text
reports/test_results.json
```

e transformar os dados utilizando Pandas antes da visualização.

## Test result integrity

Os indicadores apresentados devem representar os dados reais existentes no relatório do Pytest.

Nunca:

- escrever manualmente números de Passed, Failed ou Skipped para representar uma execução;
- alterar resultados para melhorar visualmente o dashboard;
- esconder testes que falharam;
- converter `failed` em `passed`;
- remover testes lentos apenas para melhorar métricas;
- inventar resultados ausentes;
- afirmar cobertura de código baseada apenas na quantidade de testes aprovados.

Passed, Failed, Skipped, duração e taxa de sucesso devem ser calculados a partir dos resultados reais.

A taxa de sucesso pode ser calculada a partir dos testes executados, deixando claro o critério utilizado.

## Performance analysis

A duração registrada pelo Pytest pode ser utilizada para identificar testes relativamente mais lentos.

Entretanto, um teste mais lento não significa automaticamente que existe um problema de performance no endpoint.

O tempo pode ser influenciado por:

- rede;
- ambiente;
- disponibilidade da API;
- setup da fixture;
- cleanup;
- autenticação;
- criação de dados;
- dependências entre recursos.

Antes de classificar um endpoint como problema de performance, devem existir medições apropriadas e repetíveis.

## Dashboard debugging

Quando o dashboard apresentar erro:

1. verificar se `reports/test_results.json` existe;
2. verificar se o Pytest terminou corretamente;
3. verificar se `pytest-json-report` está instalado;
4. validar se o JSON pode ser lido;
5. verificar o caminho configurado em `REPORT_PATH`;
6. verificar a transformação realizada pelo Pandas;
7. verificar se as colunas esperadas existem;
8. somente depois investigar Streamlit ou Plotly.

A ausência do relatório não deve causar um `FileNotFoundError` para o usuário.

O dashboard deve apresentar uma mensagem amigável informando que é necessário executar os testes e gerar o relatório.

O caminho do relatório deve ser resolvido com base na localização do projeto, evitando depender do diretório atual do terminal.

Exemplo:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = BASE_DIR / "reports" / "test_results.json"
```

## Dashboard refactoring

Ao alterar `dashboard/app.py`:

- preservar a leitura dos resultados reais;
- evitar duplicação de transformação de dados;
- manter nomes de métricas claros;
- não misturar execução dos testes com visualização;
- preferir funções pequenas para carregar, transformar e apresentar dados;
- tratar arquivos ausentes ou inválidos;
- evitar valores de resultados hardcoded;
- preservar compatibilidade com o relatório produzido pelo Pytest.

A execução dos testes e a visualização devem permanecer independentes:

```text
Pytest gera dados
        ↓
Dashboard consome dados
```

O dashboard não deve executar silenciosamente a suíte de testes apenas para conseguir abrir.

## Dependencies

As dependências utilizadas pelo dashboard devem estar documentadas em `requirements.txt`.

Entre elas:

```text
pandas
streamlit
plotly
pytest-json-report
```

Não adicionar uma nova biblioteca de visualização ou análise sem verificar se Pandas, Streamlit ou Plotly já atendem à necessidade.

---

# Definition of Done

Antes de considerar uma alteração pronta para commit:

### 1. Verificar coleta

```bash
pytest tests --collect-only -v
```

Confirmar que todos os testes esperados foram encontrados.

### 2. Executar regressão

```bash
pytest tests -v --tb=short
```

Confirmar que não foram introduzidas regressões inesperadas.

### 3. Gerar relatório atualizado

```bash
pytest tests -v --json-report --json-report-file=reports/test_results.json
```

### 4. Validar dashboard

```bash
streamlit run dashboard/app.py
```

Confirmar que:

- o dashboard abre corretamente;
- o JSON é carregado;
- Total corresponde à execução;
- Passed corresponde à execução;
- Failed corresponde à execução;
- Skipped corresponde à execução;
- a taxa de sucesso está correta;
- os módulos são identificados corretamente;
- os gráficos correspondem aos dados reais;
- os testes mais lentos são calculados a partir das durações reais.

### 5. Revisar código

Antes do commit:

- remover imports não utilizados;
- verificar arquivos temporários;
- verificar `.gitignore`;
- não versionar `.venv`;
- não versionar `__pycache__`;
- não versionar `.pytest_cache`;
- verificar se nenhuma credencial ou token foi incluído;
- confirmar que `requirements.txt` está atualizado.

## Regra principal

A IA deve ajudar a encontrar problemas reais, melhorar a qualidade dos testes e reduzir manutenção.

Ela não deve modificar testes, dados ou métricas apenas para produzir uma execução verde ou um dashboard visualmente melhor.