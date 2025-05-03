# Sistema de Identificação e Marketing de Franquias sem Estoque

Este projeto implementa um sistema automatizado para identificar, analisar e promover oportunidades de franquia sem estoque, permitindo que o franqueado trabalhe apenas com marketing digital e receba comissões por vendas, sem necessidade de gerenciar estoque ou logística.

## Estrutura do Projeto

```
franquia-finder/
│
├── collectors/                  # Scripts para coleta de dados
│   ├── __init__.py
│   ├── franchise_scraper.py     # Coleta dados de sites de franquias
│   ├── marketplace_scraper.py   # Coleta dados de marketplaces
│   ├── social_media_monitor.py  # Analisa tendências em redes sociais
│   └── sales_data_collector.py  # Coleta estatísticas de vendas
│
├── processors/                  # Processamento de dados coletados
│   ├── __init__.py
│   ├── data_cleaner.py          # Limpa e normaliza dados brutos
│   ├── opportunity_analyzer.py  # Analisa e pontua oportunidades
│   ├── market_trend_analyzer.py # Identifica tendências de mercado
│   └── profit_estimator.py      # Estima potencial de lucro
│
├── analysis/                    # Scripts de análise aprofundada
│   ├── __init__.py
│   ├── competition_analysis.py  # Analisa concorrência para cada produto
│   ├── demographic_matcher.py   # Identifica demografia alvo ideal 
│   └── roi_calculator.py        # Calcula ROI projetado detalhado
│
├── marketing/                   # Sistema de geração de marketing
│   ├── __init__.py
│   ├── creative_generator.py    # Gera criativos automáticos
│   ├── platform_adapter.py      # Adapta criativos para diferentes plataformas
│   └── campaign_scheduler.py    # Agenda e distribui campanhas
│
├── automation/                  # Sistema de automação
│   ├── __init__.py
│   ├── platform_publisher.py    # Publica conteúdo nas plataformas
│   ├── performance_tracker.py   # Acompanha desempenho de campanhas
│   └── optimization_engine.py   # Otimiza campanhas com base em resultados
│
├── config/                      # Configurações do sistema
│   ├── api_keys.json            # Chaves de API (não incluídas no git)
│   ├── platform_settings.json   # Configurações das plataformas
│   └── analysis_params.json     # Parâmetros para modelos de análise
│
├── static/                      # Recursos estáticos
│   ├── templates/               # Templates para criativos
│   │   ├── instagram_templates/
│   │   ├── tiktok_templates/
│   │   └── marketplace_templates/
│   └── assets/                  # Imagens e outros recursos
│
├── templates/                   # Templates para relatórios e UI
│   ├── report_template.html
│   ├── dashboard_template.html
│   └── creative_template.html
│
├── dashboard/                   # Aplicação web para visualização
│   ├── __init__.py
│   ├── app.py                   # Aplicação Dash
│   ├── components/              # Componentes da UI
│   │   ├── __init__.py
│   │   ├── header.py
│   │   ├── opportunity_card.py
│   │   ├── performance_charts.py
│   │   └── creative_display.py
│   └── callbacks.py             # Callbacks para interatividade
│
├── tests/                       # Testes unitários e de integração
│   ├── __init__.py
│   ├── test_collectors.py
│   ├── test_processors.py
│   ├── test_marketing.py
│   └── test_automation.py
│
├── output/                      # Diretório para resultados gerados
│   ├── reports/                 # Relatórios gerados
│   ├── data/                    # Dados processados
│   └── creatives/               # Criativos gerados
│
├── logs/                        # Logs do sistema
│
├── main.py                      # Ponto de entrada principal
└── requirements.txt             # Dependências do projeto
```

## Requisitos

- Python 3.8+
- Bibliotecas especificadas em `requirements.txt`

## Instalação

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/franquia-finder.git
cd franquia-finder
```

2. (Opcional) Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as APIs (opcional)
   - Edite os arquivos em `config/` para adicionar suas chaves de API
   - Sem as chaves de API, o sistema usará dados simulados

## Uso

### Execução completa

Para executar o sistema completo:
```bash
python main.py
```

### Execução por módulos

Para executar apenas módulos específicos:

```bash
# Coletar dados de franquias
python -m collectors.franchise_scraper

# Monitorar redes sociais
python -m collectors.social_media_monitor

# Coletar dados de marketplaces
python -m collectors.marketplace_scraper

# Coletar estatísticas de vendas
python -m collectors.sales_data_collector

# Iniciar dashboard
python -m dashboard.app
```

## Funcionalidades Principais

1. **Coleta de Dados**: Scraper automático de sites de franquias, marketplaces e redes sociais.
2. **Análise de Oportunidades**: Identificação das melhores oportunidades com base em comissão, investimento inicial e potencial de vendas.
3. **Geração de Criativos**: Criação automática de materiais de marketing para cada oportunidade.
4. **Publicação Multiplataforma**: Distribuição automatizada em marketplaces (Amazon, Mercado Livre, Shopee) e redes sociais (Instagram, TikTok).
5. **Dashboard de Monitoramento**: Visualização de métricas e desempenho em tempo real.

## Configuração

As configurações do sistema estão nos arquivos JSON na pasta `config/`. Você pode personalizar:

- **franchise_sources.json**: Fontes de dados de franquias e seletores HTML para scraping
- **marketplace_sources.json**: Configurações de marketplaces para scraping
- **social_media.json**: Configurações de monitoramento de redes sociais
- **sales_data.json**: Fontes de dados de vendas e categorias

## Desenvolvimento

Para contribuir com o projeto:

1. Crie um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Testes

Para executar os testes:
```bash
python -m unittest discover tests
```

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.
