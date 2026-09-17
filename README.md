## Estratégia

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

Além dos status codes, os cenários validam mensagens de resposta, payloads JSON, persistência dos dados, alterações realizadas, autenticação, autorização, regras de negócio, exclusão de recursos e efeitos no estoque.

## 📊 Dashboard de resultados

O projeto possui um dashboard para análise visual dos resultados da suíte E2E.

O fluxo de dados funciona da seguinte maneira:

```text
Pytest
   ↓
pytest-json-report
   ↓
reports/test_results.json
   ↓
Pandas
   ↓
Streamlit + Plotly
   ↓
Dashboard
```

O dashboard apresenta:

- total de testes executados;
- quantidade de testes aprovados (`Passed`);
- quantidade de testes com falha (`Failed`);
- quantidade de testes ignorados (`Skipped`);
- taxa de sucesso;
- resultados dos testes por módulo;
- Top 10 testes com maior duração.

Na execução atualmente registrada:

| Métrica | Resultado |
|---|---:|
| Total de testes | 63 |
| Passed | 63 |
| Failed | 0 |
| Skipped | 0 |
| Taxa de sucesso | 100% |

Os resultados são obtidos do relatório JSON gerado pelo Pytest e processados com Pandas. Os gráficos interativos são construídos com Plotly e apresentados através do Streamlit.

### Gerando os dados do dashboard

Antes de iniciar o dashboard, execute a suíte gerando o relatório JSON:

```bash
pytest tests -v --json-report --json-report-file=reports/test_results.json
```

O resultado será armazenado em:

```text
reports/test_results.json
```

### Executando o dashboard

Depois de gerar o relatório:

```bash
streamlit run dashboard/app.py
```

O Streamlit disponibilizará a aplicação localmente, normalmente em:

```text
http://localhost:8501
```

> Os indicadores apresentados pelo dashboard são calculados a partir da execução real registrada pelo Pytest e não representam valores fixos definidos no código.

### ⏱️ Análise de duração

O dashboard também permite identificar os testes com maior duração de execução.

Essa informação pode ajudar a localizar cenários E2E mais custosos e oportunidades de otimização da suíte.

A duração de um teste, entretanto, pode ser influenciada pela rede, ambiente, criação e remoção de massas, autenticação e tempo de resposta da API. Portanto, um teste mais lento não representa, isoladamente, um problema de performance do endpoint.

## Boas práticas aplicadas

- Separação de responsabilidades.
- Fixtures reutilizáveis.
- Dados dinâmicos.
- Cleanup de recursos temporários.
- Cenários positivos e negativos.
- Parametrização para reduzir duplicação.
- Organização por domínio da API.
- Relatórios baseados em execuções reais.
- Visualização de métricas da suíte.

## Próximas evoluções

- histórico das execuções;
- comparação entre execuções anteriores;
- evolução da taxa de sucesso;
- evolução do tempo total da regressão;
- identificação de testes com aumento de duração;
- relatório HTML;
- markers `smoke`, `regression` e `negative`;
- cobertura com `pytest-cov`, quando aplicável;
- pipeline CI/CD;
- logging estruturado;
- validação de contrato OpenAPI;
- execução paralela após garantir isolamento das massas.