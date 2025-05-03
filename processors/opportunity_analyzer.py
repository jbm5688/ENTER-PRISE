# processors/opportunity_analyzer.py
import random

class OpportunityAnalyzer:
    """
    Classe responsável por analisar dados limpos e identificar oportunidades de franquias
    """
    
    def __init__(self, analysis_params=None):
        """
        Inicializa o analisador de oportunidades
        
        Args:
            analysis_params (dict): Parâmetros para análise das oportunidades
        """
        self.analysis_params = analysis_params or {}
        self.min_roi = self.analysis_params.get('min_roi', 0.15)
        self.market_weight = self.analysis_params.get('market_weight', 0.4)
        self.competition_weight = self.analysis_params.get('competition_weight', 0.3)
        self.trend_weight = self.analysis_params.get('trend_weight', 0.3)
        
    def analyze(self, clean_data):
        """
        Analisa os dados limpos e identifica oportunidades potenciais
        
        Args:
            clean_data (dict): Dados limpos e normalizados
            
        Returns:
            list: Lista de oportunidades identificadas
        """
        print("OpportunityAnalyzer: Analisando dados para identificar oportunidades...")
        
        # Implementação básica que retorna dados fictícios
        opportunities = []
        
        # Se existirem dados de franquias, usar esses dados
        if 'franchise_data' in clean_data and clean_data['franchise_data']:
            for franchise in clean_data['franchise_data']:
                # Gerar pontuação fictícia com base em alguns critérios básicos
                opportunity = self._evaluate_franchise(franchise)
                opportunities.append(opportunity)
        else:
            # Caso não existam dados, gerar algumas oportunidades fictícias para teste
            opportunities = self._generate_sample_opportunities()
        
        # Ordenar oportunidades por pontuação
        opportunities.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return opportunities
    
    def _evaluate_franchise(self, franchise):
        """Avalia uma franquia e gera um objeto de oportunidade"""
        
        # Gerar alguns valores fictícios para simular uma análise
        market_score = random.uniform(0.5, 1.0)
        competition_score = random.uniform(0.3, 0.9)
        trend_score = random.uniform(0.4, 0.95)
        
        # Calcular pontuação geral ponderada
        overall_score = (
            market_score * self.market_weight +
            competition_score * self.competition_weight +
            trend_score * self.trend_weight
        )
        
        # Criar um objeto de oportunidade com base nos dados da franquia
        opportunity = {
            'name': franchise.get('name', 'Franquia Desconhecida'),
            'sector': franchise.get('sector', 'Setor Não Especificado'),
            'investment': {
                'min': franchise.get('min_investment', random.uniform(30000, 100000)),
                'max': franchise.get('max_investment', random.uniform(100000, 500000))
            },
            'roi_estimate': random.uniform(0.15, 0.45),
            'payback_months': random.randint(18, 60),
            'market_score': market_score,
            'competition_score': competition_score,
            'trend_score': trend_score,
            'score': overall_score,
            'website': franchise.get('website', 'https://www.exemplo-franquia.com.br'),
            'contact': franchise.get('contact', 'contato@exemplo-franquia.com.br')
        }
        
        return opportunity
    
    def _generate_sample_opportunities(self):
        """Gera algumas oportunidades de amostra para testes"""
        sample_opportunities = [
            {
                'name': 'PetFood Express',
                'sector': 'Pet Shop',
                'investment': {
                    'min': 80000,
                    'max': 150000
                },
                'roi_estimate': 0.32,
                'payback_months': 24,
                'market_score': 0.85,
                'competition_score': 0.70,
                'trend_score': 0.90,
                'score': 0.82,
                'website': 'https://www.petfoodexpress.com.br',
                'contact': 'contato@petfoodexpress.com.br'
            },
            {
                'name': 'CleanTech',
                'sector': 'Limpeza Ecológica',
                'investment': {
                    'min': 50000,
                    'max': 120000
                },
                'roi_estimate': 0.28,
                'payback_months': 30,
                'market_score': 0.75,
                'competition_score': 0.65,
                'trend_score': 0.85,
                'score': 0.75,
                'website': 'https://www.cleantechbrasil.com.br',
                'contact': 'franquias@cleantechbrasil.com.br'
            },
            {
                'name': 'EducaMais',
                'sector': 'Educação',
                'investment': {
                    'min': 120000,
                    'max': 280000
                },
                'roi_estimate': 0.25,
                'payback_months': 36,
                'market_score': 0.90,
                'competition_score': 0.55,
                'trend_score': 0.80,
                'score': 0.78,
                'website': 'https://www.educamais.com.br',
                'contact': 'expansao@educamais.com.br'
            },
            {
                'name': 'FastFit Academia',
                'sector': 'Fitness',
                'investment': {
                    'min': 200000,
                    'max': 450000
                },
                'roi_estimate': 0.22,
                'payback_months': 40,
                'market_score': 0.80,
                'competition_score': 0.60,
                'trend_score': 0.85,
                'score': 0.77,
                'website': 'https://www.fastfitacademia.com.br',
                'contact': 'franquia@fastfit.com.br'
            },
            {
                'name': 'TechRepair',
                'sector': 'Assistência Técnica',
                'investment': {
                    'min': 40000,
                    'max': 90000
                },
                'roi_estimate': 0.35,
                'payback_months': 20,
                'market_score': 0.70,
                'competition_score': 0.75,
                'trend_score': 0.65,
                'score': 0.70,
                'website': 'https://www.techrepair.com.br',
                'contact': 'negocios@techrepair.com.br'
            }
        ]
        
        return sample_opportunities
