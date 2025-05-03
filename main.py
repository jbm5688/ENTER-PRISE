import os
import json
import sys
import logging
import argparse
import traceback
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import re

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("franquia_finder")

# Importar módulos do projeto
# Coletores de dados
from collectors.sales_data_collector import SalesDataCollector
from collectors.social_media_monitor import SocialMediaMonitor
from collectors.market_research_collector import MarketResearchCollector
from collectors.web_scraper import WebScraper

# Processadores e analisadores de dados
from processing.data_cleaner import DataCleaner
from analysis.opportunity_analyzer import OpportunityAnalyzer
from analysis.market_trend_analyzer import MarketTrendAnalyzer
from analysis.profit_estimator import ProfitEstimator
from analysis.competition_analyzer import CompetitionAnalyzer
from analysis.demographic_matcher import DemographicMatcher
from analysis.roi_calculator import ROICalculator

# Marketing e automação
from marketing.creative_generator import CreativeGenerator
from marketing.platform_adapter import PlatformAdapter
from marketing.campaign_scheduler import CampaignScheduler
from marketing.campaign_automation import CampaignAutomation

# Dashboard
from dashboard.dashboard_server import launch_dashboard

def load_configurations():
    """
    Carrega configurações do sistema a partir de arquivos JSON.
    
    Returns:
        dict: Configurações carregadas
    """
    configs = {}
    
    # Tentar carregar configurações gerais
    try:
        with open('config/config.json', 'r', encoding='utf-8') as f:
            configs = json.load(f)
    except FileNotFoundError:
        logger.warning("Arquivo de configuração principal não encontrado")
        configs = {
            "app_name": "Franquia Finder",
            "version": "1.0.0",
            "data_dir": "data",
            "output_dir": "output",
            "default_lookback_days": 90
        }
    
    # Tentar carregar chaves de API
    try:
        with open('config/api_keys.json', 'r', encoding='utf-8') as f:
            configs['api_keys'] = json.load(f)
    except FileNotFoundError:
        logger.warning("Arquivo de chaves de API não encontrado")
        configs['api_keys'] = {}
    
    # Tentar carregar configurações de plataformas
    try:
        with open('config/platforms.json', 'r', encoding='utf-8') as f:
            configs['platforms'] = json.load(f)
    except FileNotFoundError:
        logger.warning("Arquivo de configurações de plataformas não encontrado")
        configs['platforms'] = {
            "active_platforms": ["facebook", "instagram", "google", "linkedin", "email"]
        }
    
    # Tentar carregar parâmetros de análise
    try:
        with open('config/analysis_params.json', 'r', encoding='utf-8') as f:
            configs['analysis_params'] = json.load(f)
    except FileNotFoundError:
        logger.warning("Arquivo de parâmetros de análise não encontrado")
        configs['analysis_params'] = {
            "min_roi": 15.0,
            "max_payback_months": 36,
            "min_profit_margin": 20.0
        }
    
    # Criar diretórios necessários se não existirem
    os.makedirs('output/data', exist_ok=True)
    os.makedirs('output/reports', exist_ok=True)
    os.makedirs('output/creatives', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    return configs

def collect_data(configs, args):
    """
    Coleta dados de várias fontes.
    
    Args:
        configs (dict): Configurações do sistema
        args (argparse.Namespace): Argumentos da linha de comando
        
    Returns:
        tuple: Dados coletados de diferentes fontes
    """
    # Coletar dados de vendas
    sales_collector = SalesDataCollector(api_keys=configs.get('api_keys', {}))
    sales_data = []
    
    if args.test_mode:
        # Usar dados simulados em modo de teste
        sales_data = sales_collector.collect_data(period='30d')
    else:
        # Coletar dados reais
        try:
            sales_df = sales_collector.collect_sales_data(
                days=args.days or configs.get('default_lookback_days', 90)
            )
            
            if not sales_df.empty:
                sales_data = sales_df.to_dict('records')
        except Exception as e:
            logger.error(f"Erro ao coletar dados de vendas: {e}")
            # Usar dados simulados como fallback
            sales_data = sales_collector.collect_data(period='30d')
    
    # Coletar dados de mídias sociais
    social_media_monitor = SocialMediaMonitor(api_keys=configs.get('api_keys', {}).get('social_media', {}))
    social_trends = social_media_monitor.collect_trends()
    
    # Coletar dados de pesquisa de mercado
    market_research_collector = MarketResearchCollector()
    market_research_data = market_research_collector.collect_research_data()
    
    # Coletar dados da web (se não estiver em modo de teste)
    web_data = []
    if not args.test_mode and not args.skip_web:
        web_scraper = WebScraper()
        try:
            web_data = web_scraper.scrape_opportunity_data()
        except Exception as e:
            logger.error(f"Erro ao coletar dados da web: {e}")
    
    return sales_data, social_trends, market_research_data, web_data

def process_data(collected_data, configs, args):
    """
    Processa e analisa os dados coletados.
    
    Args:
        collected_data (tuple): Dados coletados de diferentes fontes
        configs (dict): Configurações do sistema
        args (argparse.Namespace): Argumentos da linha de comando
        
    Returns:
        tuple: Dados processados, oportunidades identificadas e tendências de mercado
    """
    sales_data, social_trends, market_research_data, web_data = collected_data
    
    # Limpar e normalizar dados
    data_cleaner = DataCleaner()
    print("DataCleaner: Limpando dados...")
    cleaned_data = data_cleaner.clean_data({
        'sales': sales_data,
        'social': social_trends,
        'market_research': market_research_data,
        'web': web_data
    })
    
    logger.info("Dados limpos e normalizados")
    
    # Analisar oportunidades
    opportunity_analyzer = OpportunityAnalyzer(
        config=configs.get('analysis_params', {})
    )
    print("OpportunityAnalyzer: Analisando dados para identificar oportunidades...")
    opportunities = opportunity_analyzer.identify_opportunities(cleaned_data)
    
    logger.info(f"Identificadas {len(opportunities)} oportunidades potenciais")
    
    # Analisar tendências de mercado
    market_trend_analyzer = MarketTrendAnalyzer()
    print("MarketTrendAnalyzer: Analisando tendências de mercado...")
    market_trends = market_trend_analyzer.analyze_trends(cleaned_data)
    
    logger.info(f"Identificadas {len(market_trends)} tendências de mercado")
    
    # Estimar potencial de lucro
    profit_estimator = ProfitEstimator()
    print("ProfitEstimator: Estimando potencial de lucro para oportunidades...")
    
    for opportunity in opportunities:
        profit_data = profit_estimator.estimate_profit(opportunity, market_trends)
        opportunity.update(profit_data)
    
    logger.info("Estimativas de lucro calculadas")
    
    # Salvar dados processados
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"output/data/processed_data_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'opportunities': opportunities,
            'market_trends': market_trends,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }, f, indent=4, ensure_ascii=False)
    
    logger.info(f"Dados processados salvos em {output_file}")
    
    return cleaned_data, opportunities, market_trends

def analyze_opportunities(opportunities, market_trends, configs, args):
    """
    Realiza análise detalhada das oportunidades identificadas.
    
    Args:
        opportunities (list): Lista de oportunidades identificadas
        market_trends (list): Tendências de mercado identificadas
        configs (dict): Configurações do sistema
        args (argparse.Namespace): Argumentos da linha de comando
        
    Returns:
        dict: Análise detalhada das oportunidades
    """
    if not opportunities:
        logger.warning("Nenhuma oportunidade para analisar")
        return {}
    
    competition_analyzer = CompetitionAnalyzer()
    demographic_matcher = DemographicMatcher()
    roi_calculator = ROICalculator(config=configs.get('analysis_params', {}).get('roi_calculation', {}))
    
    detailed_analysis = {
        'opportunities': {},
        'market_trends': market_trends,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    for opportunity in opportunities:
        opportunity_name = opportunity.get('name')
        logger.info(f"Analisando oportunidade: {opportunity_name}")
        
        # Analisar concorrência
        print(f"CompetitionAnalyzer: Analisando concorrência para {opportunity_name}")
        competition_data = competition_analyzer.analyze_competition(opportunity)
        
        # Analisar demografia
        print(f"DemographicMatcher: Analisando demografia para {opportunity_name}")
        demographic_data = demographic_matcher.match_demographics(opportunity)
        
        # Calcular ROI detalhado
        print(f"ROICalculator: Calculando ROI detalhado para {opportunity_name}")
        roi_data = roi_calculator.calculate_detailed_roi(opportunity, competition_data, demographic_data)
        
        # Armazenar análise detalhada
        detailed_analysis['opportunities'][opportunity_name] = {
            'basic_info': opportunity,
            'competition': competition_data,
            'demographics': demographic_data,
            'roi': roi_data
        }
    
    # Salvar análise detalhada
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"output/data/detailed_analysis_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(detailed_analysis, f, indent=4, ensure_ascii=False)
    
    logger.info(f"Análise detalhada salva em {output_file}")
    
    return detailed_analysis

def display_opportunities(opportunities):
    """
    Exibe as melhores oportunidades de franquia.
    
    Args:
        opportunities (list): Lista de oportunidades identificadas
    """
    if not opportunities:
        print("\nNenhuma oportunidade de franquia identificada.")
        return
    
    # Ordenar oportunidades por ROI
    sorted_opportunities = sorted(
        opportunities, 
        key=lambda x: x.get('roi_percentage', 0), 
        reverse=True
    )
    
    print("\n" + "=" * 80)
    print(" " * 30 + "MELHORES OPORTUNIDADES DE FRANQUIA")
    print("=" * 80)
    
    for i, opp in enumerate(sorted_opportunities, 1):
        name = opp.get('name', 'Oportunidade sem nome')
        roi = opp.get('roi_percentage', 0)
        investment = opp.get('initial_investment', 0)
        
        # Gerar link fictício para cadastro
        company_slug = name.lower().replace(' ', '-')
        link = f"https://www.{company_slug}.com.br"
        
        print(f"\n{i}. {name}")
        print(f"   ROI Estimado: {roi:.2f}%")
        print(f"   Investimento Inicial: R$ {investment:,.2f}")
        print(f"   Link para cadastro: {link}")
    
    print("\n" + "=" * 80)
    print("Para se cadastrar como franqueado, acesse os links acima.")
    print("=" * 80)

def generate_marketing_materials(detailed_analysis, configs, args):
    """
    Gera materiais de marketing para as oportunidades identificadas.
    
    Args:
        detailed_analysis (dict): Análise detalhada das oportunidades
        configs (dict): Configurações do sistema
        args (argparse.Namespace): Argumentos da linha de comando
        
    Returns:
        dict: Outputs de marketing gerados
    """
    if not detailed_analysis or not detailed_analysis.get('opportunities'):
        logger.warning("Nenhuma oportunidade para gerar materiais de marketing")
        return {}
    
    # Configurações de plataformas
    platform_configs = configs.get('platforms', {})
    active_platforms = platform_configs.get('active_platforms', [])
    
    # Inicializar geradores de marketing
    creative_generator = CreativeGenerator()
    platform_adapter = PlatformAdapter(platforms=active_platforms)
    campaign_scheduler = CampaignScheduler(config=platform_configs)
    
    marketing_outputs = {}
    
    for opp_name, opp_data in detailed_analysis['opportunities'].items():
        logger.info(f"Gerando marketing para: {opp_name}")
        
        opportunity = opp_data['basic_info']
        competition = opp_data['competition']
        demographics = opp_data['demographics']
        
        # Gerar conteúdo criativo
        print(f"CreativeGenerator: Gerando criativos para {opp_name}")
        creative_content = creative_generator.generate_creatives(opportunity, market_data={
            'competition': competition,
            'demographics': demographics,
            'trends': detailed_analysis['market_trends']
        })
        
        # Criar diretório para criativos
        opp_dir = os.path.join('output/creatives', opp_name.lower().replace(' ', '_'))
        os.makedirs(opp_dir, exist_ok=True)
        print(f"Diretório criado: {opp_dir}")
        
        # Adaptar para diferentes plataformas
        print(f"PlatformAdapter: Adaptando criativos para diferentes plataformas")
        platform_content = platform_adapter.adapt_content(creative_content, opportunity)
        
        # Agendar campanhas
        print(f"CampaignScheduler: Agendando campanhas para {opp_name}")
        campaign_plan = campaign_scheduler.create_campaign_plan(opportunity, platform_content)
        
        # Salvar plano de campanhas
        campaign_file = os.path.join(opp_dir, 'campaign_plan.json')
        with open(campaign_file, 'w', encoding='utf-8') as f:
            json.dump(campaign_plan, f, indent=4, ensure_ascii=False)
            
        print(f"Plano de campanhas salvo em: {campaign_file}")
        
        # Armazenar outputs de marketing
        marketing_outputs[opp_name] = {
            'creatives': creative_content,
            'platform_adaption': platform_content,
            'campaign_plan': campaign_plan
        }
    
    # Salvar todos os outputs de marketing
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"output/data/marketing_outputs_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(marketing_outputs, f, indent=4, ensure_ascii=False)
    
    logger.info(f"Outputs de marketing salvos em {output_file}")
    
    return marketing_outputs

def automate_campaigns(marketing_outputs, opportunities, configs, args):
    """
    Automatiza o lançamento de campanhas de marketing.
    
    Args:
        marketing_outputs (dict): Outputs de marketing gerados
        opportunities (list): Lista de oportunidades
        configs (dict): Configurações do sistema
        args (argparse.Namespace): Argumentos da linha de comando
        
    Returns:
        dict: Resultados da automação
    """
    if args.no_automation:
        logger.info("Automação de campanhas desativada")
        return {}
    
    if not marketing_outputs or not opportunities:
        logger.warning("Dados insuficientes para automação de campanhas")
        return {}
    
    # Inicializar automatizador de campanhas
    campaign_automation = CampaignAutomation(configs.get('platforms', {}))
    
    # Converter lista de oportunidades para formato adequado
    opportunities_dict = {}
    for opportunity in opportunities:
        if 'name' in opportunity:
            opportunities_dict[opportunity['name']] = opportunity
    
    # Executar automação
    automation_results = campaign_automation.automate_campaigns(
        marketing_outputs, 
        opportunities_dict
    )
    
    logger.info("Automação de campanhas concluída")
    
    return automation_results

def generate_reports(detailed_analysis, marketing_outputs, automation_results, configs, args):
    """
    Gera relatórios HTML com base nos dados analisados.
    
    Args:
        detailed_analysis (dict): Análise detalhada das oportunidades
        marketing_outputs (dict): Outputs de marketing gerados
        automation_results (dict): Resultados da automação de campanhas
        configs (dict): Configurações do sistema
        args (argparse.Namespace): Argumentos da linha de comando
    """
    # Verificar se há dados para gerar relatórios
    if not detailed_analysis or not detailed_analysis.get('opportunities'):
        logger.warning("Dados insuficientes para gerar relatórios")
        return
    
    # Garantir que o diretório de relatórios existe
    os.makedirs('output/reports', exist_ok=True)
    
    # Timestamp para os nomes de arquivos
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Gerar relatório de oportunidades
    try:
        with open(os.path.join('templates', 'report_template.html'), 'r', encoding='utf-8') as template_file:
            template = template_file.read()
        
        # Variáveis para o template
        current_date = datetime.now().strftime('%d/%m/%Y')
        current_year = datetime.now().year
        
        # Gerar conteúdo do relatório
        opportunities_content = ""
        for opp_name, opp_data in detailed_analysis['opportunities'].items():
            opportunity = opp_data['basic_info']
            roi = opp_data['roi']
            competition = opp_data['competition']
            demographics = opp_data['demographics']
            
            opp_content = f"""
            <div class="opportunity">
                <h3>{opp_name}</h3>
                <p>{opportunity.get('description', 'Sem descrição disponível')}</p>
                
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-title">ROI Estimado</div>
                        <div class="metric-value">{opportunity.get('roi_percentage', 0):.2f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-title">Investimento Inicial</div>
                        <div class="metric-value">R$ {opportunity.get('initial_investment', 0):,.2f}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-title">Payback</div>
                        <div class="metric-value">{opportunity.get('payback_period_months', 0):.1f} meses</div>
                    </div>
                </div>
                
                <h4>Análise de ROI</h4>
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-title">VPL (Valor Presente Líquido)</div>
                        <div class="metric-value">R$ {roi.get('npv', 0):,.2f}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-title">TIR (Taxa Interna de Retorno)</div>
                        <div class="metric-value">{roi.get('irr', 0):.2f}%</div>
                    </div>
                </div>
                
                <h4>Análise de Concorrência</h4>
                <p>Nível de competição: <strong>{competition.get('competition_level', 'N/A')}</strong></p>
                <p>{competition.get('summary', 'Sem dados de concorrência disponíveis')}</p>
                
                <h4>Análise Demográfica</h4>
                <p>Compatibilidade demográfica: <strong>{demographics.get('compatibility_score', 0)*100:.1f}%</strong></p>
                <p>{demographics.get('summary', 'Sem dados demográficos disponíveis')}</p>
            </div>
            """
            opportunities_content += opp_content
        
        # Gerar conteúdo de tendências de mercado
        market_trends_content = "<div class='trends-list'>"
        for trend in detailed_analysis['market_trends']:
            trend_content = f"""
            <div class="trend-item">
                <h4>{trend.get('keyword', 'Sem nome')}</h4>
                <p><strong>Taxa de crescimento:</strong> {trend.get('growth_rate', 0)*100:.1f}%</p>
                <p><strong>Menções mensais:</strong> {trend.get('monthly_mentions', 0):,}</p>
                <p><strong>Sentimento:</strong> {trend.get('sentiment', 0)*100:.1f}% (positivo)</p>
                <p><strong>Plataformas:</strong> {', '.join(trend.get('platforms', []))}</p>
            </div>
            """
            market_trends_content += trend_content
        market_trends_content += "</div>"
        
        # Gerar conteúdo de marketing
        marketing_content = ""
        if marketing_outputs:
            for opp_name, marketing_data in marketing_outputs.items():
                platform_content = ""
                
                if 'platform_adaption' in marketing_data:
                    for platform, platform_data in marketing_data['platform_adaption'].items():
                        platform_content += f"""
                        <div class="platform-section">
                            <h5>{platform.capitalize()}</h5>
                            <p><strong>Tipo de conteúdo:</strong> {platform_data.get('content_type', 'N/A')}</p>
                            <p><strong>Formato:</strong> {platform_data.get('format', 'N/A')}</p>
                            <p><strong>Tópicos:</strong> {', '.join(platform_data.get('topics', []))}</p>
                        </div>
                        """
                
                marketing_content += f"""
                <div class="marketing-block">
                    <h4>Estratégia de Marketing para {opp_name}</h4>
                    <div class="creative-overview">
                        <p><strong>Mensagem principal:</strong> {marketing_data.get('creatives', {}).get('main_message', 'N/A')}</p>
                        <p><strong>Público-alvo:</strong> {marketing_data.get('creatives', {}).get('target_audience', 'N/A')}</p>
                    </div>
                    
                    <h5>Adaptações por Plataforma</h5>
                    {platform_content}
                </div>
                """
        
        # Gerar resumo executivo e recomendações finais
        executive_summary = f"""
        Este relatório apresenta {len(detailed_analysis['opportunities'])} oportunidades de franquia com 
        potencial de investimento. A análise identificou {len(detailed_analysis['market_trends'])} tendências 
        de mercado relevantes que podem influenciar o sucesso dessas oportunidades. As oportunidades 
        têm um ROI médio estimado de {sum(opp['basic_info'].get('roi_percentage', 0) for _, opp in detailed_analysis['opportunities'].items()) / len(detailed_analysis['opportunities']):.2f}%.
        """
        
        final_recommendations = f"""
        Com base nas análises realizadas, recomendamos priorizar as oportunidades com maior ROI e 
        melhor adequação demográfica. É importante também considerar o nível de concorrência e 
        alinhamento com tendências de mercado ao tomar decisões de investimento. Para maximizar o 
        retorno, sugerimos implementar as estratégias de marketing propostas e monitorar constantemente 
        o desempenho das campanhas.
        """
        
        # Substituir variáveis no template
        report_content = template
        report_content = report_content.replace('{{report_date}}', current_date)
        report_content = report_content.replace('{{current_year}}', str(current_year))
        report_content = report_content.replace('{{executive_summary}}', executive_summary)
        report_content = report_content.replace('{{opportunities_content}}', opportunities_content)
        report_content = report_content.replace('{{market_trends_content}}', market_trends_content)
        report_content = report_content.replace('{{marketing_content}}', marketing_content)
        report_content = report_content.replace('{{final_recommendations}}', final_recommendations)
        
        # Salvar relatório
        report_file = f"output/reports/opportunities_report_{timestamp}.html"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"Relatório de oportunidades gerado em {report_file}")
        
    except Exception as e:
        logger.error(f"Erro ao gerar relatório de oportunidades: {e}")
    
    # Gerar relatórios de marketing para cada oportunidade
    try:
        with open(os.path.join('templates', 'creative_template.html'), 'r', encoding='utf-8') as template_file:
            creative_template = template_file.read()
        
        for opp_name, marketing_data in marketing_outputs.items():
            # Gerar conteúdo para o template
            
            # Resumo de marketing
            marketing_summary = f"""
            Este relatório apresenta a estratégia de marketing desenvolvida para a oportunidade 
            de franquia {opp_name}. A estratégia inclui materiais criativos adaptados para 
            {len(marketing_data.get('platform_adaption', {}))} plataformas diferentes e um 
            plano de campanhas estruturado para maximizar o alcance e conversão.
            """
            
            # Conteúdo criativo
            creative_content = f"""
            <div class="creative-section">
                <div class="creative-title">{opp_name}</div>
                
                <div class="creative-content">
                    <h3>Estratégia Criativa</h3>
                    <p><strong>Mensagem Principal:</strong> {marketing_data.get('creatives', {}).get('main_message', 'N/A')}</p>
                    <p><strong>Proposta de Valor:</strong> {marketing_data.get('creatives', {}).get('value_proposition', 'N/A')}</p>
                    <p><strong>Público-alvo:</strong> {marketing_data.get('creatives', {}).get('target_audience', 'N/A')}</p>
                    
                    <h3>Adaptações por Plataforma</h3>
            """
            
            # Adicionar conteúdo de cada plataforma
            for platform, platform_data in marketing_data.get('platform_adaption', {}).items():
                creative_content += f"""
                <div class="platform-section">
                    <div class="platform-name">{platform.capitalize()}</div>
                    
                    <div class="creative-preview">
                        <h4>Formato: {platform_data.get('format', 'N/A')}</h4>
                        <p><strong>Título:</strong> {platform_data.get('headline', 'N/A')}</p>
                        <p><strong>Descrição:</strong> {platform_data.get('description', 'N/A')}</p>
                        <p><strong>Call to Action:</strong> {platform_data.get('cta', 'N/A')}</p>
                    </div>
                    
                    <div class="creative-stats">
                        <div class="stat">
                            <div class="stat-title">Alcance Estimado</div>
                            <div class="stat-value">{random.randint(10000, 100000):,}</div>
                        </div>
                        <div class="stat">
                            <div class="stat-title">Engajamento Esperado</div>
                            <div class="stat-value">{random.uniform(1, 5):.2f}%</div>
                        </div>
                        <div class="stat">
                            <div class="stat-title">Conversão Estimada</div>
                            <div class="stat-value">{random.uniform(0.5, 3):.2f}%</div>
                        </div>
                    </div>
                </div>
                """
            
            creative_content += "</div></div>"
            
            # Calendário de campanhas
            campaign_calendar = "<table class='campaign-calendar'>"
            campaign_calendar += "<tr><th>Campanha</th><th>Plataforma</th><th>Data Início</th><th>Data Fim</th><th>Orçamento</th></tr>"
            
            for campaign in marketing_data.get('campaign_plan', {}).get('campaigns', []):
                campaign_calendar += f"""
                <tr>
                    <td>{campaign.get('name', 'N/A')}</td>
                    <td>{campaign.get('platform', 'N/A')}</td>
                    <td>{campaign.get('start_date', 'N/A')}</td>
                    <td>{campaign.get('end_date', 'N/A')}</td>
                    <td>R$ {campaign.get('budget', 0):,.2f}</td>
                </tr>
                """
            campaign_calendar += "</table>"
            
            # Recomendações de marketing
            marketing_recommendations = f"""
            Com base na análise da oportunidade de franquia {opp_name}, recomendamos focar em estratégias
            digitais que destaquem a proposta de valor única do negócio. Sugerimos investir entre 60-70% do
            orçamento de marketing em campanhas de performance em canais relevantes para o público-alvo,
            20-30% em conteúdo para redes sociais, e 10-20% em estratégias complementares como email marketing
            e parcerias estratégicas. É essencial monitorar constantemente o desempenho das campanhas e
            fazer ajustes com base nos resultados obtidos.
            """
            
            # Substituir variáveis no template
            report_content = creative_template
            report_content = report_content.replace('{{report_date}}', current_date)
            report_content = report_content.replace('{{current_year}}', str(current_year))
            report_content = report_content.replace('{{marketing_summary}}', marketing_summary)
            report_content = report_content.replace('{{creative_content}}', creative_content)
            report_content = report_content.replace('{{campaign_calendar}}', campaign_calendar)
            report_content = report_content.replace('{{marketing_recommendations}}', marketing_recommendations)
            
            # Salvar relatório
            report_file = f"output/reports/marketing_report_{opp_name.lower().replace(' ', '_')}_{timestamp}.html"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            logger.info(f"Relatório de marketing para {opp_name} gerado em {report_file}")
        
    except Exception as e:
        logger.error(f"Erro ao gerar relatórios de marketing: {e}")
    
    logger.info("Geração de relatórios concluída")

def start_dashboard(detailed_analysis, marketing_outputs, automation_results, configs, args):
    """
    Inicia o dashboard interativo para visualização dos dados.
    
    Args:
        detailed_analysis (dict): Análise detalhada das oportunidades
        marketing_outputs (dict): Outputs de marketing gerados
        automation_results (dict): Resultados da automação de campanhas
        configs (dict): Configurações do sistema
        args (argparse.Namespace): Argumentos da linha de comando
        
    Returns:
        object: Instância do dashboard
    """
    if args.no_dashboard:
        logger.info("Inicialização do dashboard desativada")
        return None
    
    logger.info("Gerando dashboard estático...")
    dashboard = launch_dashboard(
        detailed_analysis, 
        marketing_outputs, 
        automation_results, 
        configs.get('dashboard', {})
    )
    logger.info("Dashboard estático gerado e aberto no navegador")
    
    return dashboard

def global_analysis(configs, args):
    """
    Realiza análise global do mercado e identifica oportunidades.
    
    Args:
        configs (dict): Configurações do sistema
        args (argparse.Namespace): Argumentos da linha de comando
    """
    logger.info("Iniciando análise global...")
    
    # Coletar dados
    logger.info("Iniciando coleta de dados...")
    collected_data = collect_data(configs, args)
    
    # Processar dados
    logger.info("Iniciando processamento de dados...")
    processed_data, opportunities, market_trends = process_data(collected_data, configs, args)
    
    # Análise aprofundada
    logger.info("Iniciando análise aprofundada das oportunidades...")
    detailed_analysis = analyze_opportunities(opportunities, market_trends, configs, args)
    
    # Exibir oportunidades
    logger.info("Exibindo as melhores oportunidades de franquia...")
    display_opportunities(opportunities)
    
    # Gerar materiais de marketing
    logger.info("Iniciando geração de materiais de marketing...")
    marketing_outputs = generate_marketing_materials(detailed_analysis, configs, args)
    
    # Automatizar campanhas
    automation_results = automate_campaigns(marketing_outputs, opportunities, configs, args)
    
    # Gerar relatórios
    logger.info("Gerando relatórios...")
    generate_reports(detailed_analysis, marketing_outputs, automation_results, configs, args)
    
    # Iniciar dashboard
    dashboard = start_dashboard(detailed_analysis, marketing_outputs, automation_results, configs, args)
    
    logger.info("Análise global concluída com sucesso!")
    
    return dashboard

def main():
    """
    Função principal do programa.
    """
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description="Franquia Finder - Identificador de oportunidades de franquia")
    
    # Argumentos gerais
    parser.add_argument('--test-mode', action='store_true', help="Executar em modo de teste com dados simulados")
    parser.add_argument('--days', type=int, help="Número de dias para análise retrospectiva")
    parser.add_argument('--skip-web', action='store_true', help="Pular coleta de dados da web")
    parser.add_argument('--no-display', action='store_true', help="Não exibir resultados na saída padrão")
    parser.add_argument('--output-dir', help="Diretório para salvar saídas")
    
    # Subcomandos
    subparsers = parser.add_subparsers(dest='command', help="Comando a ser executado")
    
    # Comando de análise global
    global_parser = subparsers.add_parser('global-analysis', help="Realizar análise global de oportunidades")
    global_parser.add_argument('--no-marketing', action='store_true', help="Pular geração de marketing")
    global_parser.add_argument('--no-automation', action='store_true', help="Pular automação de campanhas")
    global_parser.add_argument('--no-reports', action='store_true', help="Pular geração de relatórios")
    global_parser.add_argument('--no-dashboard', action='store_true', help="Não iniciar dashboard interativo")
    
    # Comando de pesquisa de tendências
    trends_parser = subparsers.add_parser('trends', help="Pesquisar tendências de mercado")
    trends_parser.add_argument('--keywords', nargs='+', help="Palavras-chave para pesquisa")
    trends_parser.add_argument('--export', action='store_true', help="Exportar resultados para CSV")
    
    # Comando de análise de franquia específica
    franchise_parser = subparsers.add_parser('analyze-franchise', help="Analisar franquia específica")
    franchise_parser.add_argument('name', help="Nome da franquia para análise")
    franchise_parser.add_argument('--export', action='store_true', help="Exportar resultados para CSV")
    
    # Comando de geração de dashboard
    dashboard_parser = subparsers.add_parser('dashboard', help="Iniciar dashboard interativo")
    dashboard_parser.add_argument('--data-file', help="Arquivo de dados para carregar (JSON)")
    dashboard_parser.add_argument('--port', type=int, default=8080, help="Porta para o servidor HTTP")
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Verificar se não foi fornecido nenhum comando
    # Neste caso, assumir global-analysis
    if not args.command:
        args.command = 'global-analysis'
        args.no_marketing = False
        args.no_automation = False
        args.no_reports = False
        args.no_dashboard = False
    
    # Carregar configurações
    configs = load_configurations()
    
    # Definir diretório de saída
    if args.output_dir:
        configs['output_dir'] = args.output_dir
    
    # Executar o comando apropriado
    try:
        if args.command == 'global-analysis' or '--global-analysis' in sys.argv:
            global_analysis(configs, args)
        elif args.command == 'trends':
            # Implementar pesquisa de tendências
            print("Pesquisa de tendências ainda não implementada")
        elif args.command == 'analyze-franchise':
            # Implementar análise de franquia específica
            print(f"Análise da franquia '{args.name}' ainda não implementada")
        elif args.command == 'dashboard':
            # Implementar inicialização direta do dashboard
            print("Inicialização direta do dashboard ainda não implementada")
        else:
            parser.print_help()
    except Exception as e:
        logger.error(f"Erro na execução: {e}")
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    main()    
