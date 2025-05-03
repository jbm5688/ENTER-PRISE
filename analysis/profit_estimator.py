import logging
import random
from datetime import datetime

logger = logging.getLogger("franquia_finder")

class ProfitEstimator:
    """
    Classe responsável por estimar o potencial de lucro para oportunidades de franquia.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o estimador de lucro.
        
        Args:
            config (dict): Configurações para estimativa de lucro
        """
        self.config = config or {}
    
    def estimate_profit(self, opportunity, market_trends=None):
        """
        Estima o potencial de lucro para uma oportunidade de franquia.
        
        Args:
            opportunity (dict): Dados da oportunidade
            market_trends (list): Tendências de mercado relevantes
            
        Returns:
            dict: Estimativas de lucro
        """
        # Extrair dados relevantes
        initial_investment = opportunity.get('initial_investment', 0)
        avg_monthly_revenue = opportunity.get('avg_monthly_revenue', 0)
        category = opportunity.get('category', '')
        
        # Se não tiver receita mensal, estimar com base no investimento
        if not avg_monthly_revenue and initial_investment:
            # Retorno mensal estimado entre 2% e 5% do investimento inicial
            avg_monthly_revenue = initial_investment * random.uniform(0.02, 0.05)
        
        # Determinar margem de lucro com base na categoria
        profit_margin = self._estimate_profit_margin(category, market_trends)
        
        # Calcular custos mensais
        monthly_costs = avg_monthly_revenue * (1 - profit_margin)
        
        # Calcular lucro mensal e anual
        monthly_profit = avg_monthly_revenue - monthly_costs
        annual_profit = monthly_profit * 12
        
        # Calcular ROI anualizado
        if initial_investment > 0:
            roi_percentage = (annual_profit / initial_investment) * 100
        else:
            roi_percentage = 0
        
        # Calcular período de payback (em meses)
        if monthly_profit > 0:
            payback_period_months = initial_investment / monthly_profit
        else:
            payback_period_months = float('inf')
        
        # Estimar margem de lucro operacional
        operational_margin = monthly_profit / avg_monthly_revenue if avg_monthly_revenue > 0 else 0
        
        # Estimar despesas operacionais
        operating_expenses = {
            'aluguel': monthly_costs * random.uniform(0.15, 0.30),
            'pessoal': monthly_costs * random.uniform(0.25, 0.40),
            'marketing': monthly_costs * random.uniform(0.05, 0.15),
            'insumos': monthly_costs * random.uniform(0.20, 0.40),
            'administracao': monthly_costs * random.uniform(0.05, 0.15),
            'outros': monthly_costs * random.uniform(0.05, 0.10)
        }
        
        # Estimar receitas futuras (crescimento anual)
        growth_rate = self._estimate_growth_rate(category, market_trends)
        future_revenues = {
            'ano1': annual_profit,
            'ano2': annual_profit * (1 + growth_rate),
            'ano3': annual_profit * (1 + growth_rate) ** 2,
            'ano4': annual_profit * (1 + growth_rate) ** 3,
            'ano5': annual_profit * (1 + growth_rate) ** 4
        }
        
        # Compilar resultados
        profit_estimate = {
            'estimated_monthly_revenue': avg_monthly_revenue,
            'estimated_monthly_expenses': monthly_costs,
            'estimated_monthly_profit': monthly_profit,
            'annual_profit': annual_profit,
            'roi_percentage': roi_percentage,
            'payback_period_months': payback_period_months,
            'profit_margin': profit_margin,
            'operational_margin': operational_margin,
            'operating_expenses': operating_expenses,
            'growth_rate': growth_rate,
            'future_revenues': future_revenues
        }
        
        return profit_estimate
    
    def _estimate_profit_margin(self, category, market_trends):
        """
        Estima a margem de lucro com base na categoria e tendências.
        
        Args:
            category (str): Categoria do negócio
            market_trends (list): Tendências de mercado
            
        Returns:
            float: Margem de lucro estimada (0-1)
        """
        # Margens base por categoria
        base_margins = {
            'Tecnologia': 0.40,
            'Educação': 0.45,
            'Alimentação': 0.25,
            'Saúde': 0.35,
            'Beleza': 0.30,
            'Pet': 0.32,
            'Moda': 0.28,
            'Fitness': 0.35,
            'Casa e Decoração': 0.30
        }
        
        # Obter margem base da categoria ou usar padrão
        base_margin = base_margins.get(category, 0.30)
        
        # Ajustar margem com base nas tendências, se disponíveis
        if market_trends:
            trend_bonus = 0
            
            for trend in market_trends:
                # Verificar se a tendência é relevante para a categoria
                if category.lower() in trend.get('keyword', '').lower() or trend.get('keyword', '').lower() in category.lower():
                    # Bônus baseado no crescimento e sentimento
                    growth_bonus = trend.get('growth_rate', 0) * 0.1
                    sentiment_bonus = (trend.get('sentiment', 0.5) - 0.5) * 0.1
                    
                    trend_bonus += growth_bonus + sentiment_bonus
            
            # Limitar bônus de tendência
            trend_bonus = min(0.15, max(-0.1, trend_bonus))
            
            # Aplicar bônus à margem base
            base_margin += trend_bonus
        
        # Adicionar variação aleatória
        random_variation = random.uniform(-0.05, 0.05)
        
        # Calcular margem final
        final_margin = base_margin + random_variation
        
        # Garantir que a margem está entre 0.15 e 0.6
        final_margin = min(0.6, max(0.15, final_margin))
        
        return final_margin
    
    def _estimate_growth_rate(self, category, market_trends):
        """
        Estima a taxa de crescimento anual com base na categoria e tendências.
        
        Args:
            category (str): Categoria do negócio
            market_trends (list): Tendências de mercado
            
        Returns:
            float: Taxa de crescimento anual estimada (0-1)
        """
        # Taxas de crescimento base por categoria
        base_growth_rates = {
            'Tecnologia': 0.15,
            'Educação': 0.12,
            'Alimentação': 0.08,
            'Saúde': 0.10,
            'Beleza': 0.09,
            'Pet': 0.12,
            'Moda': 0.07,
            'Fitness': 0.11,
            'Casa e Decoração': 0.08
        }
        
        # Obter taxa base da categoria ou usar padrão
        base_growth = base_growth_rates.get(category, 0.10)
        
        # Ajustar com base nas tendências, se disponíveis
        if market_trends:
            trend_bonus = 0
            relevant_trends_count = 0
            
            for trend in market_trends:
                if category.lower() in trend.get('keyword', '').lower() or trend.get('keyword', '').lower() in category.lower():
                    trend_bonus += trend.get('growth_rate', 0)
                    relevant_trends_count += 1
            
            # Aplicar bônus médio das tendências relevantes
            if relevant_trends_count > 0:
                trend_bonus = trend_bonus / relevant_trends_count
                base_growth += trend_bonus
        
        # Adicionar variação aleatória
        random_variation = random.uniform(-0.03, 0.03)
        
        # Calcular taxa final
        final_growth = base_growth + random_variation
        
        # Garantir que a taxa está entre 0.05 e 0.25
        final_growth = min(0.25, max(0.05, final_growth))
        
        return final_growth
