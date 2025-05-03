import logging
import random
from datetime import datetime

logger = logging.getLogger("franquia_finder")

class OpportunityAnalyzer:
    """
    Classe responsável por analisar dados e identificar oportunidades de franquia.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o analisador de oportunidades.
        
        Args:
            config (dict): Configurações para análise de oportunidades
        """
        self.config = config or {}
        
        # Configurações padrão
        self.min_roi = self.config.get('min_roi', 15.0)
        self.max_payback_months = self.config.get('max_payback_months', 36)
        self.min_profit_margin = self.config.get('min_profit_margin', 20.0)
        
        # Pesos para diferentes fatores
        self.weights = self.config.get('weight_factors', {
            'roi': 0.30,
            'investment': 0.25,
            'market_trend': 0.20,
            'competition': 0.15,
            'operational_complexity': 0.10
        })
    
    def identify_opportunities(self, data):
        """
        Identifica oportunidades de franquia com base nos dados processados.
        
        Args:
            data (dict): Dados limpos e normalizados de diferentes fontes
                
        Returns:
            list: Lista de oportunidades identificadas
        """
        opportunities = []
        
        # Verificar oportunidades nos dados da web
        if 'web' in data and data['web']:
            web_opportunities = self._extract_web_opportunities(data['web'])
            opportunities.extend(web_opportunities)
        
        # Identificar oportunidades com base em dados de vendas
        if 'sales' in data and data['sales']:
            sales_opportunities = self._extract_sales_opportunities(data['sales'])
            opportunities.extend(sales_opportunities)
        
        # Adicionar oportunidades simuladas para testes
        if not opportunities:
            opportunities = self._generate_simulated_opportunities()
        
        # Filtrar e classificar oportunidades
        filtered_opportunities = self._filter_opportunities(opportunities)
        
        # Enriquecer oportunidades com dados de tendências e pesquisa
        enriched_opportunities = self._enrich_opportunities(
            filtered_opportunities, data
        )
        
        return enriched_opportunities
    
    def _extract_web_opportunities(self, web_data):
        """
        Extrai oportunidades de franquia dos dados da web.
        
        Args:
            web_data (list): Dados da web limpos
            
        Returns:
            list: Oportunidades extraídas
        """
        opportunities = []
        
        for item in web_data:
            if 'name' not in item or 'initial_investment' not in item:
                continue
            
            # Calcular ROI se não estiver presente
            if 'roi_percentage' not in item or not item['roi_percentage']:
                if 'avg_monthly_revenue' in item and item['avg_monthly_revenue']:
                    # Estimar custos como 70% da receita
                    monthly_costs = item['avg_monthly_revenue'] * 0.7
                    monthly_profit = item['avg_monthly_revenue'] - monthly_costs
                    annual_profit = monthly_profit * 12
                    item['roi_percentage'] = (annual_profit / item['initial_investment']) * 100
                else:
                    # Valor padrão para ROI
                    item['roi_percentage'] = random.uniform(15, 40)
            
            # Calcular payback se não estiver presente
            if 'payback_period_months' not in item or not item['payback_period_months']:
                if 'avg_monthly_revenue' in item and item['avg_monthly_revenue']:
                    # Estimar custos como 70% da receita
                    monthly_costs = item['avg_monthly_revenue'] * 0.7
                    monthly_profit = item['avg_monthly_revenue'] - monthly_costs
                    
                    if monthly_profit > 0:
                        item['payback_period_months'] = item['initial_investment'] / monthly_profit
                    else:
                        item['payback_period_months'] = 48  # Valor default alto
                else:
                    # Valor padrão para payback
                    item['payback_period_months'] = 24
            
            # Adicionar à lista de oportunidades
            opportunities.append(item)
        
        return opportunities
    
    def _extract_sales_opportunities(self, sales_data):
        """
        Extrai oportunidades de franquia dos dados de vendas.
        
        Args:
            sales_data (list): Dados de vendas limpos
            
        Returns:
            list: Oportunidades extraídas
        """
        opportunities = []
        
        # Agrupar por produto/categoria
        grouped_data = {}
        
        for item in sales_data:
            if 'product' not in item or 'category' not in item:
                continue
            
            key = f"{item['product']}|{item['category']}"
            
            if key not in grouped_data:
                grouped_data[key] = {
                    'product': item['product'],
                    'category': item['category'],
                    'total_sales': 0,
                    'growth_rate': 0,
                    'data_points': 0
                }
            
            # Somar vendas
            if 'total_sales' in item:
                grouped_data[key]['total_sales'] += item['total_sales']
            
            # Média ponderada da taxa de crescimento
            if 'growth_rate' in item:
                current_points = grouped_data[key]['data_points']
                current_growth = grouped_data[key]['growth_rate']
                new_growth = item['growth_rate']
                
                weighted_growth = (current_growth * current_points + new_growth) / (current_points + 1)
                grouped_data[key]['growth_rate'] = weighted_growth
                grouped_data[key]['data_points'] += 1
        
        # Converter para oportunidades
        for key, data in grouped_data.items():
            if data['data_points'] == 0:
                continue
            
            # Estimar investimento inicial com base nas vendas
            initial_investment = data['total_sales'] * random.uniform(1.5, 3)
            
            # Estimar ROI com base na taxa de crescimento
            roi_percentage = 15 + (data['growth_rate'] * 100)
            
            # Estimar payback
            payback_period_months = 48 - (data['growth_rate'] * 100)
            payback_period_months = max(12, min(48, payback_period_months))
            
            opportunity = {
                'name': f"{data['product']} Franquia",
                'category': data['category'],
                'initial_investment': initial_investment,
                'roi_percentage': roi_percentage,
                'payback_period_months': payback_period_months,
                'estimated_monthly_revenue': data['total_sales'] / 12,
                'growth_rate': data['growth_rate'],
                'source': 'Análise de vendas'
            }
            
            opportunities.append(opportunity)
        
        return opportunities
    
    def _generate_simulated_opportunities(self):
        """
        Gera oportunidades simuladas para testes.
        
        Returns:
            list: Oportunidades simuladas
        """
        # Oportunidade simulada
        opportunity = {
            'name': 'PetFood Express',
            'category': 'Pet',
            'initial_investment': random.uniform(30000, 100000),
            'franchise_fee': random.uniform(10000, 30000),
            'royalty_fee_percentage': random.uniform(3, 8),
            'avg_monthly_revenue': random.uniform(15000, 50000),
            'roi_percentage': random.uniform(20, 60),
            'payback_period_months': random.uniform(12, 36),
            'min_area': random.randint(20, 100),
            'min_employees': random.randint(2, 8),
            'units': random.randint(10, 200),
            'description': 'Franquia de produtos para pets com modelo de negócio simplificado e sem necessidade de estoque.',
            'summary': 'PetFood Express é uma rede de franquias especializada em alimentação e produtos para pets, com foco em qualidade e praticidade.',
            'source': 'Dados simulados',
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return [opportunity]
    
    def _filter_opportunities(self, opportunities):
        """
        Filtra oportunidades com base nos critérios definidos.
        
        Args:
            opportunities (list): Lista de oportunidades
            
        Returns:
            list: Oportunidades filtradas
        """
        filtered = []
        
        for opp in opportunities:
            # Verificar ROI mínimo
            if 'roi_percentage' in opp and opp['roi_percentage'] < self.min_roi:
                continue
            
            # Verificar payback máximo
            if 'payback_period_months' in opp and opp['payback_period_months'] > self.max_payback_months:
                continue
            
            # Verificar margem de lucro se disponível
            if 'profit_margin' in opp and opp['profit_margin'] < self.min_profit_margin / 100:
                continue
            
            filtered.append(opp)
        
        return filtered
    
    def _enrich_opportunities(self, opportunities, data):
        """
        Enriquece as oportunidades com dados adicionais de outras fontes.
        
        Args:
            opportunities (list): Lista de oportunidades
            data (dict): Dados de diferentes fontes
            
        Returns:
            list: Oportunidades enriquecidas
        """
        # Dados de tendências sociais
        social_trends = data.get('social', [])
        
        # Dados de pesquisa de mercado
        market_research = data.get('market_research', [])
        
        for opp in opportunities:
            category = opp.get('category', '').lower()
            
            # Enriquecer com tendências sociais
            relevant_trends = []
            for trend in social_trends:
                trend_keyword = trend.get('keyword', '').lower()
                if trend_keyword in category or category in trend_keyword:
                    relevant_trends.append({
                        'keyword': trend.get('keyword', ''),
                        'growth_rate': trend.get('growth_rate', 0),
                        'sentiment': trend.get('sentiment', 0),
                        'monthly_mentions': trend.get('monthly_mentions', 0)
                    })
            
            if relevant_trends:
                opp['relevant_trends'] = relevant_trends
            
            # Enriquecer com pesquisa de mercado
            relevant_research = []
            for research in market_research:
                research_category = research.get('category', '').lower()
                if research_category == category or research_category in category or category in research_category:
                    relevant_research.append({
                        'title': research.get('title', ''),
                        'market_size': research.get('market_size', 0),
                        'growth_rate': research.get('growth_rate', 0),
                        'insights': research.get('insights', [])
                    })
            
            if relevant_research:
                opp['market_research'] = relevant_research
            
            # Calcular pontuação da oportunidade
            score_components = {
                'roi': min(1, opp.get('roi_percentage', 0) / 100),
                'investment': 1 - min(1, opp.get('initial_investment', 100000) / 200000),
                'market_trend': self._calculate_trend_score(relevant_trends),
                'competition': self._calculate_competition_score(relevant_research),
                'operational_complexity': self._calculate_operational_complexity(opp)
            }
            
            # Calcular pontuação ponderada
            weighted_score = 0
            for component, score in score_components.items():
                weighted_score += score * self.weights.get(component, 0.2)
            
            opp['opportunity_score'] = round(weighted_score * 100, 2)
        
        # Ordenar por pontuação
        enriched = sorted(opportunities, key=lambda x: x.get('opportunity_score', 0), reverse=True)
        
        return enriched
    
    def _calculate_trend_score(self, trends):
        """
        Calcula pontuação de tendência de mercado.
        
        Args:
            trends (list): Tendências relevantes
            
        Returns:
            float: Pontuação de 0 a 1
        """
        if not trends:
            return 0.5  # Pontuação neutra se não houver dados
        
        avg_growth = sum(t.get('growth_rate', 0) for t in trends) / len(trends)
        avg_sentiment = sum(t.get('sentiment', 0) for t in trends) / len(trends)
        
        # Combinar crescimento e sentimento
        score = (avg_growth + avg_sentiment) / 2
        
        return min(1, max(0, score))
    
    def _calculate_competition_score(self, research):
        """
        Calcula pontuação de concorrência com base em pesquisa de mercado.
        
        Args:
            research (list): Pesquisas de mercado relevantes
            
        Returns:
            float: Pontuação de 0 a 1 (1 = baixa concorrência, 0 = alta concorrência)
        """
        if not research:
            return 0.5  # Pontuação neutra se não houver dados
        
        # Invenção de score baseado no market size (mercados maiores têm mais concorrência)
        market_sizes = [r.get('market_size', 0) for r in research]
        max_market = max(market_sizes) if market_sizes else 0
        
        if max_market <= 0:
            return 0.5
        
        # Escala logarítmica: mercados muito grandes têm pontuação mais baixa (mais competição)
        import math
        competition_factor = min(1, math.log10(max_market) / 9)  # log10(1B) = 9
        
        return 1 - competition_factor
    
    def _calculate_operational_complexity(self, opportunity):
        """
        Calcula pontuação de complexidade operacional.
        
        Args:
            opportunity (dict): Dados da oportunidade
            
        Returns:
            float: Pontuação de 0 a 1 (1 = baixa complexidade, 0 = alta complexidade)
        """
        # Fatores que aumentam complexidade
        complexity_factors = []
        
        # Área mínima
        min_area = opportunity.get('min_area', 0)
        if min_area > 0:
            area_factor = min(1, max(0, 1 - (min_area / 200)))  # 0m² = 1, 200m² = 0
            complexity_factors.append(area_factor)
        
        # Número de funcionários
        min_employees = opportunity.get('min_employees', 0)
        if min_employees > 0:
            employee_factor = min(1, max(0, 1 - (min_employees / 10)))  # 0 = 1, 10 = 0
            complexity_factors.append(employee_factor)
        
        # Royalties
        royalty = opportunity.get('royalty_fee_percentage', 0)
        if royalty > 0:
            royalty_factor = min(1, max(0, 1 - (royalty / 20)))  # 0% = 1, 20% = 0
            complexity_factors.append(royalty_factor)
        
        # Se não houver dados suficientes
        if not complexity_factors:
            return 0.5
        
        # Média dos fatores
        avg_complexity = sum(complexity_factors) / len(complexity_factors)
        
        return avg_complexity
