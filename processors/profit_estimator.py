# processors/profit_estimator.py
import random
import math

class ProfitEstimator:
    """
    Classe responsável por estimar o potencial de lucro das oportunidades
    """
    
    def __init__(self, analysis_params=None):
        """
        Inicializa o estimador de lucro
        
        Args:
            analysis_params (dict): Parâmetros para estimativa de lucro
        """
        self.analysis_params = analysis_params or {}
        self.market_growth_weight = self.analysis_params.get('market_growth_weight', 0.3)
        self.competition_weight = self.analysis_params.get('competition_weight', 0.25)
        self.trend_weight = self.analysis_params.get('trend_weight', 0.2)
        self.seasonality_weight = self.analysis_params.get('seasonality_weight', 0.15)
        self.risk_weight = self.analysis_params.get('risk_weight', 0.1)
        
    def estimate(self, opportunities, market_trends):
        """
        Estima o potencial de lucro para as oportunidades identificadas
        
        Args:
            opportunities (list): Lista de oportunidades identificadas
            market_trends (list): Lista de tendências de mercado
            
        Returns:
            list: Lista de oportunidades com estimativas de lucro
        """
        print("ProfitEstimator: Estimando potencial de lucro para oportunidades...")
        
        # Versão básica que adiciona estimativas fictícias às oportunidades
        enriched_opportunities = []
        
        for opportunity in opportunities:
            # Encontrar tendências relevantes para esta oportunidade
            relevant_trends = self._find_relevant_trends(opportunity, market_trends)
            
            # Calcular fatores que influenciam o lucro
            market_growth_factor = self._calculate_market_growth(opportunity, relevant_trends)
            competition_factor = opportunity.get('competition_score', random.uniform(0.5, 0.9))
            trend_alignment = self._calculate_trend_alignment(opportunity, relevant_trends)
            seasonality_factor = random.uniform(0.7, 1.0)  # Fator fictício
            risk_factor = 1 - random.uniform(0.1, 0.3)  # Menor é melhor (menos risco)
            
            # Calcular ROI estimado
            base_roi = opportunity.get('roi_estimate', random.uniform(0.15, 0.35))
            
            # Ajustar ROI com base nos fatores
            adjusted_roi = base_roi * (
                1 + (market_growth_factor * self.market_growth_weight) +
                (competition_factor * self.competition_weight) +
                (trend_alignment * self.trend_weight) +
                (seasonality_factor * self.seasonality_weight) -
                ((1 - risk_factor) * self.risk_weight)  # Maior risco reduz ROI
            )
            
            # Calcular outros indicadores financeiros
            monthly_revenue = self._estimate_monthly_revenue(opportunity)
            monthly_costs = self._estimate_monthly_costs(opportunity)
            monthly_profit = monthly_revenue - monthly_costs
            
            # Investimento médio
            avg_investment = (opportunity.get('investment', {}).get('min', 0) + 
                             opportunity.get('investment', {}).get('max', 0)) / 2
            
            # Payback em meses
            payback_months = math.ceil(avg_investment / monthly_profit) if monthly_profit > 0 else 60
            
            # Adicionar estimativas à oportunidade
            enriched_opportunity = opportunity.copy()
            enriched_opportunity.update({
                'estimated_roi': adjusted_roi,
                'monthly_revenue': monthly_revenue,
                'monthly_costs': monthly_costs,
                'monthly_profit': monthly_profit,
                'payback_months': payback_months,
                'market_growth_factor': market_growth_factor,
                'competition_factor': competition_factor,
                'trend_alignment': trend_alignment,
                'seasonality_factor': seasonality_factor,
                'risk_factor': risk_factor,
                'relevant_trends': [trend['name'] for trend in relevant_trends]
            })
            
            enriched_opportunities.append(enriched_opportunity)
        
        # Ordenar por ROI estimado (do maior para o menor)
        enriched_opportunities.sort(key=lambda x: x.get('estimated_roi', 0), reverse=True)
        
        return enriched_opportunities
    
    def _find_relevant_trends(self, opportunity, market_trends):
        """Encontra tendências relevantes para uma oportunidade"""
        
        # Versão básica - encontra tendências no mesmo setor
        opportunity_sector = opportunity.get('sector', '')
        
        relevant_trends = []
        for trend in market_trends:
            # Se o setor for o mesmo ou não especificado, considerar relevante
            if trend.get('sector', '') == opportunity_sector or not opportunity_sector:
                relevant_trends.append(trend)
            # Adicionar algumas tendências aleatoriamente para diversificar
            elif random.random() < 0.2:
                relevant_trends.append(trend)
        
        # Limitar a no máximo 3 tendências relevantes
        if len(relevant_trends) > 3:
            relevant_trends = random.sample(relevant_trends, 3)
            
        return relevant_trends
    
    def _calculate_market_growth(self, opportunity, relevant_trends):
        """Calcula o fator de crescimento de mercado"""
        
        # Se houver tendências relevantes, usar a média das taxas de crescimento
        if relevant_trends:
            growth_rates = [trend.get('growth_rate', 0) for trend in relevant_trends]
            return sum(growth_rates) / len(growth_rates)
        
        # Caso contrário, usar um valor fictício
        return random.uniform(0.05, 0.2)
    
    def _calculate_trend_alignment(self, opportunity, relevant_trends):
        """Calcula o alinhamento da oportunidade com as tendências atuais"""
        
        # Versão básica - valor fictício entre 0.6 e 1.0
        # Quanto mais tendências relevantes, maior o alinhamento
        base_alignment = 0.6
        trend_bonus = min(len(relevant_trends) * 0.1, 0.4)
        
        return base_alignment + trend_bonus
    
    def _estimate_monthly_revenue(self, opportunity):
        """Estima a receita mensal com base no tipo de franquia"""
        
        # Versão básica - valores fictícios
        min_investment = opportunity.get('investment', {}).get('min', 50000)
        
        # Usar o investimento para estimar receita
        # Franquias menores tendem a ter um percentual maior de receita em relação ao investimento
        if min_investment < 70000:
            revenue_factor = random.uniform(0.08, 0.12)  # 8-12% do investimento por mês
        elif min_investment < 150000:
            revenue_factor = random.uniform(0.06, 0.09)  # 6-9% do investimento por mês
        else:
            revenue_factor = random.uniform(0.05, 0.07)  # 5-7% do investimento por mês
            
        return min_investment * revenue_factor
    
    def _estimate_monthly_costs(self, opportunity):
        """Estima os custos mensais"""
        
        # Versão básica - custos como percentual da receita estimada
        monthly_revenue = opportunity.get('monthly_revenue', self._estimate_monthly_revenue(opportunity))
        
        # Diferentes tipos de franquias têm diferentes estruturas de custos
        sector = opportunity.get('sector', '').lower()
        
        # Setores com margens tipicamente maiores
        if sector in ['tecnologia', 'serviços', 'educação']:
            cost_percentage = random.uniform(0.55, 0.65)  # 55-65% da receita
        # Setores com margens médias
        elif sector in ['saúde', 'pet', 'beleza']:
            cost_percentage = random.uniform(0.65, 0.75)  # 65-75% da receita
        # Setores com margens menores
        else:
            cost_percentage = random.uniform(0.70, 0.80)  # 70-80% da receita
            
        return monthly_revenue * cost_percentage
