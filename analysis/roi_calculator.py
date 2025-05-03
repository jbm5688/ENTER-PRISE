import logging
import json
from datetime import datetime

logger = logging.getLogger("franquia_finder")

class ROICalculator:
    """
    Classe responsável por calcular o retorno sobre investimento (ROI) para oportunidades de franquia.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o calculador de ROI.
        
        Args:
            config (dict): Configurações para cálculos de ROI
        """
        self.config = config or {}
        self.tax_rate = self.config.get('tax_rate', 0.27)  # Taxa de impostos padrão
        self.inflation_rate = self.config.get('inflation_rate', 0.05)  # Taxa de inflação anual
        self.discount_rate = self.config.get('discount_rate', 0.1)  # Taxa de desconto para VPL
        
    def calculate_roi(self, opportunity):
        """
        Calcula ROI simples para uma oportunidade.
        
        Args:
            opportunity (dict): Dados da oportunidade
            
        Returns:
            dict: Métricas de ROI
        """
        initial_investment = opportunity.get('initial_investment', 100000)
        monthly_revenue = opportunity.get('estimated_monthly_revenue', 15000)
        monthly_expenses = opportunity.get('estimated_monthly_expenses', 10000)
        
        monthly_profit = monthly_revenue - monthly_expenses
        annual_profit = monthly_profit * 12
        
        # ROI simples (anualizado)
        simple_roi = (annual_profit / initial_investment) * 100
        
        # Payback period (em meses)
        payback_period = initial_investment / monthly_profit if monthly_profit > 0 else float('inf')
        
        return {
            'roi_percentage': round(simple_roi, 2),
            'payback_period_months': round(payback_period, 1),
            'annual_profit': round(annual_profit, 2),
            'monthly_profit': round(monthly_profit, 2)
        }
    
    def calculate_detailed_roi(self, opportunity, competition_data, demographic_data):
        """
        Calcula ROI detalhado com análise de fluxo de caixa descontado.
        
        Args:
            opportunity (dict): Dados da oportunidade
            competition_data (dict): Dados da análise de concorrência
            demographic_data (dict): Dados da análise demográfica
            
        Returns:
            dict: Análise detalhada de ROI
        """
        # Projeções de receita
        revenue_projections = self._project_revenue(opportunity, competition_data, demographic_data)
        
        # Projeções de custos
        cost_projections = self._project_costs(opportunity, revenue_projections)
        
        # Fluxo de caixa projetado
        cash_flow = self._calculate_cash_flow(opportunity, revenue_projections, cost_projections)
        
        # Calcular métricas de ROI
        npv = self._calculate_npv(cash_flow, self.discount_rate)
        irr = self._calculate_irr(cash_flow)
        payback = self._calculate_payback(cash_flow)
        
        return {
            'npv': round(npv, 2),
            'irr': round(irr * 100, 2),  # Converter para percentual
            'payback_years': round(payback, 1),
            'revenue_projections': revenue_projections,
            'cost_projections': cost_projections,
            'cash_flow': cash_flow
        }
    
    def _project_revenue(self, opportunity, competition_data, demographic_data):
        """
        Projeta receita estimada para uma oportunidade com base nos dados de concorrência e demografia.
        
        Args:
            opportunity (dict): Dados da oportunidade
            competition_data (dict): Dados da análise de concorrência
            demographic_data (dict): Dados da análise demográfica
            
        Returns:
            dict: Projeções de receita para diferentes cenários
        """
        print(f"Projetando receita para {opportunity['name']}")
        
        # Extrair variáveis relevantes dos dados
        market_size = demographic_data.get('market_size', 1000000)
        potential_customers = demographic_data.get('potential_customers', 5000)
        competition_level = competition_data.get('competition_level', 'medium')
        
        # Ajustar base de mercado conforme nível de competição
        if competition_level == 'high':
            market_capture = 0.03  # 3% do mercado
        elif competition_level == 'medium':
            market_capture = 0.07  # 7% do mercado
        else:
            market_capture = 0.12  # 12% do mercado
        
        # Obter preço médio do produto/serviço da oportunidade
        avg_price = opportunity.get('average_price', 100)
        
        # Calcular receita base mensal
        monthly_customers = int(potential_customers * market_capture)
        monthly_revenue = monthly_customers * avg_price
        
        # Projetar diferentes cenários
        revenue_projections = {
            'monthly': {
                'pessimistic': monthly_revenue * 0.7,
                'expected': monthly_revenue,
                'optimistic': monthly_revenue * 1.3
            },
            'annual': {
                'pessimistic': monthly_revenue * 12 * 0.7,
                'expected': monthly_revenue * 12,
                'optimistic': monthly_revenue * 12 * 1.3
            },
            'five_year': {
                'pessimistic': monthly_revenue * 12 * 5 * 0.7,
                'expected': monthly_revenue * 12 * 5,
                'optimistic': monthly_revenue * 12 * 5 * 1.3
            }
        }
        
        return revenue_projections
    
    def _project_costs(self, opportunity, revenue_projections):
        """
        Projeta custos estimados para uma oportunidade.
        
        Args:
            opportunity (dict): Dados da oportunidade
            revenue_projections (dict): Projeções de receita
            
        Returns:
            dict: Projeções de custos
        """
        # Extrair informações de custos da oportunidade
        initial_investment = opportunity.get('initial_investment', 100000)
        royalty_rate = opportunity.get('royalty_rate', 0.05)  # 5% de royalties
        cost_of_goods_rate = opportunity.get('cost_of_goods_rate', 0.4)  # 40% para COGS
        operation_costs_rate = opportunity.get('operation_costs_rate', 0.3)  # 30% para operação
        
        cost_projections = {
            'initial': initial_investment,
            'monthly': {},
            'annual': {},
            'five_year': {}
        }
        
        # Calcular custos para cada cenário
        for scenario in ['pessimistic', 'expected', 'optimistic']:
            monthly_revenue = revenue_projections['monthly'][scenario]
            annual_revenue = revenue_projections['annual'][scenario]
            five_year_revenue = revenue_projections['five_year'][scenario]
            
            # Custos mensais
            monthly_royalties = monthly_revenue * royalty_rate
            monthly_cogs = monthly_revenue * cost_of_goods_rate
            monthly_operation = monthly_revenue * operation_costs_rate
            monthly_total = monthly_royalties + monthly_cogs + monthly_operation
            
            # Custos anuais
            annual_royalties = annual_revenue * royalty_rate
            annual_cogs = annual_revenue * cost_of_goods_rate
            annual_operation = annual_revenue * operation_costs_rate
            annual_total = annual_royalties + annual_cogs + annual_operation
            
            # Custos em 5 anos
            five_year_royalties = five_year_revenue * royalty_rate
            five_year_cogs = five_year_revenue * cost_of_goods_rate
            five_year_operation = five_year_revenue * operation_costs_rate
            five_year_total = five_year_royalties + five_year_cogs + five_year_operation
            
            # Armazenar custos projetados
            cost_projections['monthly'][scenario] = {
                'royalties': monthly_royalties,
                'cogs': monthly_cogs,
                'operation': monthly_operation,
                'total': monthly_total
            }
            
            cost_projections['annual'][scenario] = {
                'royalties': annual_royalties,
                'cogs': annual_cogs,
                'operation': annual_operation,
                'total': annual_total
            }
            
            cost_projections['five_year'][scenario] = {
                'royalties': five_year_royalties,
                'cogs': five_year_cogs,
                'operation': five_year_operation,
                'total': five_year_total
            }
        
        return cost_projections
    
    def _calculate_cash_flow(self, opportunity, revenue_projections, cost_projections):
        """
        Calcula fluxo de caixa projetado para 5 anos.
        
        Args:
            opportunity (dict): Dados da oportunidade
            revenue_projections (dict): Projeções de receita
            cost_projections (dict): Projeções de custos
            
        Returns:
            dict: Fluxo de caixa projetado
        """
        # Número de anos para projetar
        projection_years = 5
        
        # Inicializar fluxo de caixa para cada cenário
        cash_flow = {
            'pessimistic': [-cost_projections['initial']],  # Investimento inicial (ano 0)
            'expected': [-cost_projections['initial']],
            'optimistic': [-cost_projections['initial']]
        }
        
        # Calcular fluxo de caixa anual para cada cenário
        for scenario in ['pessimistic', 'expected', 'optimistic']:
            annual_revenue = revenue_projections['annual'][scenario]
            annual_costs = cost_projections['annual'][scenario]['total']
            annual_profit_before_tax = annual_revenue - annual_costs
            annual_tax = annual_profit_before_tax * self.tax_rate
            annual_profit_after_tax = annual_profit_before_tax - annual_tax
            
            # Adicionar fluxo de caixa para cada ano
            for year in range(1, projection_years + 1):
                # Ajustar para inflação
                adjusted_profit = annual_profit_after_tax * ((1 + self.inflation_rate) ** (year - 1))
                cash_flow[scenario].append(adjusted_profit)
        
        return cash_flow
    
    def _calculate_npv(self, cash_flow, discount_rate):
        """
        Calcula o Valor Presente Líquido (VPL) para um fluxo de caixa.
        
        Args:
            cash_flow (dict): Fluxo de caixa projetado
            discount_rate (float): Taxa de desconto
            
        Returns:
            float: VPL para o cenário esperado
        """
        # Usar o cenário esperado
        expected_cash_flow = cash_flow['expected']
        
        npv = 0
        for year, cf in enumerate(expected_cash_flow):
            npv += cf / ((1 + discount_rate) ** year)
        
        return npv
    
    def _calculate_irr(self, cash_flow):
        """
        Calcula a Taxa Interna de Retorno (TIR) para um fluxo de caixa.
        
        Args:
            cash_flow (dict): Fluxo de caixa projetado
            
        Returns:
            float: TIR para o cenário esperado
        """
        # Usar o cenário esperado
        expected_cash_flow = cash_flow['expected']
        
        # Método de aproximação para TIR
        # Em um sistema real, seria usado um algoritmo mais preciso
        
        # Para simplificar, vamos usar uma aproximação básica
        # Testando diferentes taxas até encontrar uma que gere VPL próximo de zero
        test_rates = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
        best_rate = 0.0
        closest_npv = float('inf')
        
        for rate in test_rates:
            npv = 0
            for year, cf in enumerate(expected_cash_flow):
                npv += cf / ((1 + rate) ** year)
            
            if abs(npv) < abs(closest_npv):
                closest_npv = npv
                best_rate = rate
        
        return best_rate
    
    def _calculate_payback(self, cash_flow):
        """
        Calcula o período de payback para um fluxo de caixa.
        
        Args:
            cash_flow (dict): Fluxo de caixa projetado
            
        Returns:
            float: Período de payback para o cenário esperado (em anos)
        """
        # Usar o cenário esperado
        expected_cash_flow = cash_flow['expected']
        
        # Inicializar fluxo de caixa acumulado
        cumulative_cash_flow = [expected_cash_flow[0]]  # Investimento inicial (negativo)
        
        # Calcular fluxo de caixa acumulado
        for cf in expected_cash_flow[1:]:
            cumulative_cash_flow.append(cumulative_cash_flow[-1] + cf)
        
        # Encontrar período de payback
        for year, ccf in enumerate(cumulative_cash_flow):
            if ccf >= 0:
                # Se for o primeiro ano positivo, calcular fração do ano
                if year > 0 and cumulative_cash_flow[year-1] < 0:
                    # Interpolação linear para encontrar fração do ano
                    previous_ccf = abs(cumulative_cash_flow[year-1])
                    current_ccf = ccf
                    fraction = previous_ccf / (previous_ccf + current_ccf)
                    return year - 1 + fraction
                return year
        
        # Se nunca retornar o investimento
        return float('inf')
    
    def save_analysis(self, opportunity_id, roi_data, filename=None):
        """
        Salva a análise de ROI em um arquivo JSON.
        
        Args:
            opportunity_id (str): ID da oportunidade
            roi_data (dict): Dados da análise de ROI
            filename (str): Nome do arquivo (opcional)
            
        Returns:
            str: Caminho do arquivo salvo
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/analysis/roi_{opportunity_id}_{timestamp}.json"
        
        # Garantir que o diretório existe
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(roi_data, f, indent=4, ensure_ascii=False)
            logger.info(f"Análise de ROI salva em {filename}")
            return filename
        except Exception as e:
            logger.error(f"Erro ao salvar análise de ROI: {e}")
            return None
