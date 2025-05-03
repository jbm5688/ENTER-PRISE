import random
import logging
from datetime import datetime, timedelta
import time

logger = logging.getLogger("franquia_finder")

class WebScraper:
    """
    Classe responsável por coletar dados de oportunidades de franquia da web.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o web scraper.
        
        Args:
            config (dict): Configurações para web scraping
        """
        self.config = config or {}
        
    def scrape_opportunity_data(self, max_items=20):
        """
        Coleta dados de oportunidades de franquia da web (versão simulada).
        
        Args:
            max_items (int): Número máximo de itens para coletar
            
        Returns:
            list: Lista de oportunidades coletadas
        """
        print("Simulando coleta de dados da web...")
        
        # Simular tempo de processamento
        time.sleep(1)
        
        # Franquias simuladas
        franchise_names = [
            "PetFood Express", "TechFix", "EduKids", "GourmetBurger", 
            "FitLife Gym", "Beauty Spot", "Coffee Express", "CleanHome",
            "SaladBar", "SmartPhone Repair", "BookCorner", "HealthySnacks",
            "FashionStore", "KidsPlay", "HomeDecor", "GreenMarket"
        ]
        
        # Categorias
        categories = [
            "Pet", "Tecnologia", "Educação", "Alimentação", 
            "Fitness", "Beleza", "Café", "Serviços",
            "Alimentação Saudável", "Tecnologia", "Livraria", "Alimentação",
            "Moda", "Entretenimento", "Casa e Decoração", "Varejo"
        ]
        
        # Gerar dados simulados
        opportunities = []
        
        # Limitar número de itens
        num_items = min(len(franchise_names), max_items)
        
        for i in range(num_items):
            franchise_name = franchise_names[i]
            category = categories[i]
            
            # Gerar investimento inicial simulado
            if category in ["Tecnologia", "Fitness", "Café"]:
                initial_investment = random.uniform(80000, 200000)  # Franquias mais caras
            elif category in ["Alimentação", "Educação", "Livraria"]:
                initial_investment = random.uniform(50000, 150000)  # Franquias de custo médio
            else:
                initial_investment = random.uniform(30000, 100000)  # Franquias mais baratas
            
            # Gerar ROI simulado
            roi_percentage = random.uniform(15, 60)
            
            # Gerar faturamento médio mensal
            avg_monthly_revenue = initial_investment * random.uniform(0.1, 0.25)
            
            # Gerar prazo de retorno (em meses)
            payback_period_months = random.uniform(12, 48)
            
            # Gerar número de unidades
            units = random.randint(5, 200)
            
            # Gerar taxa de franquia e royalties
            franchise_fee = initial_investment * random.uniform(0.1, 0.2)
            royalty_fee_percentage = random.uniform(2, 12)
            
            # Gerar área mínima
            if category in ["Fitness", "Alimentação", "Livraria"]:
                min_area = random.randint(50, 200)  # m²
            else:
                min_area = random.randint(20, 100)  # m²
            
            # Gerar funcionários necessários
            min_employees = random.randint(2, 8)
            
            # Gerar descrição simulada
            descriptions = [
                f"Franquia de {category} com excelente retorno sobre investimento.",
                f"Oportunidade no setor de {category} com modelo de negócio comprovado.",
                f"Invista em uma franquia de {category} em expansão no mercado.",
                f"Modelo de negócio simplificado no setor de {category} com suporte completo.",
                f"Franquia inovadora no segmento de {category} com alta rentabilidade."
            ]
            
            description = random.choice(descriptions)
            
            # Gerar resumo simulado
            summaries = [
                f"{franchise_name} é uma rede de franquias no setor de {category} com {units} unidades em operação no Brasil.",
                f"Com investimento inicial a partir de R$ {initial_investment/1000:.1f} mil, {franchise_name} oferece uma excelente oportunidade no mercado de {category}.",
                f"{franchise_name} se destaca no segmento de {category} com retorno estimado em {payback_period_months:.1f} meses.",
                f"Rede {franchise_name} possui mais de {units} unidades e atua no mercado de {category} há mais de {random.randint(5, 20)} anos."
            ]
            
            summary = random.choice(summaries)
            
            # Criar oportunidade simulada
            opportunity = {
                "name": franchise_name,
                "category": category,
                "initial_investment": initial_investment,
                "franchise_fee": franchise_fee,
                "royalty_fee_percentage": royalty_fee_percentage,
                "avg_monthly_revenue": avg_monthly_revenue,
                "roi_percentage": roi_percentage,
                "payback_period_months": payback_period_months,
                "min_area": min_area,
                "min_employees": min_employees,
                "units": units,
                "description": description,
                "summary": summary,
                "source": "Web (simulado)",
                "scraped_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            opportunities.append(opportunity)
        
        logger.info(f"Coletadas {len(opportunities)} oportunidades de franquia da web")
        return opportunities
