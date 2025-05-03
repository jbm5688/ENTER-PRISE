import logging
import random
from datetime import datetime

logger = logging.getLogger("franquia_finder")

class CompetitionAnalyzer:
    """
    Classe responsável por analisar a concorrência para oportunidades de franquia.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o analisador de concorrência.
        
        Args:
            config (dict): Configurações para análise de concorrência
        """
        self.config = config or {}
    
    def analyze_competition(self, opportunity):
        """
        Analisa a concorrência para uma oportunidade de franquia.
        
        Args:
            opportunity (dict): Dados da oportunidade
            
        Returns:
            dict: Dados da análise de concorrência
        """
        print(f"CompetitionAnalyzer: Analisando concorrência para {opportunity.get('name', 'Oportunidade')}")
        
        # Extrair categoria
        category = opportunity.get('category', '')
        
        # Número de unidades como indicador de competição
        units = opportunity.get('units', 0)
        
        # Gerar dados de competição
        competition_data = self._generate_competition_data(category, units)
        
        return competition_data
    
    def _generate_competition_data(self, category, units):
        """
        Gera dados de competição simulados.
        
        Args:
            category (str): Categoria do negócio
            units (int): Número de unidades
            
        Returns:
            dict: Dados de competição simulados
        """
        # Determinar nível de competição com base na categoria
        competition_levels = {
            'Tecnologia': 'high',
            'Educação': 'medium',
            'Alimentação': 'high',
            'Saúde': 'medium',
            'Beleza': 'high',
            'Pet': 'medium',
            'Moda': 'high',
            'Fitness': 'medium',
            'Casa e Decoração': 'medium'
        }
        
        # Obter nível base de competição ou usar 'medium' como padrão
        base_level = competition_levels.get(category, 'medium')
        
        # Ajustar com base no número de unidades
        if units > 0:
            if units < 20:
                competition_factor = 'low'
            elif units < 100:
                competition_factor = 'medium'
            else:
                competition_factor = 'high'
                
            # Combinar fatores (mais peso para o número de unidades)
            if base_level == competition_factor:
                competition_level = base_level
            elif base_level == 'medium' or competition_factor == 'medium':
                # Se um dos fatores é médio, usar o outro
                competition_level = competition_factor if base_level == 'medium' else base_level
            else:
                # Se um é alto e outro é baixo, usar médio
                competition_level = 'medium'
        else:
            competition_level = base_level
        
        # Número simulado de concorrentes
        if competition_level == 'low':
            num_competitors = random.randint(2, 10)
        elif competition_level == 'medium':
            num_competitors = random.randint(10, 30)
        else:
            num_competitors = random.randint(30, 100)
        
        # Gerar concorrentes simulados
        competitors = []
        for i in range(min(5, num_competitors)):
            competitor = {
                'name': self._generate_competitor_name(category),
                'market_share': random.uniform(0.05, 0.3),
                'units': random.randint(10, 200),
                'years_in_market': random.randint(2, 20),
                'competitive_advantages': self._generate_competitive_advantages()
            }
            competitors.append(competitor)
        
        # Simular saturação de mercado
        if competition_level == 'low':
            market_saturation = random.uniform(0.2, 0.4)
        elif competition_level == 'medium':
            market_saturation = random.uniform(0.4, 0.6)
        else:
            market_saturation = random.uniform(0.6, 0.8)
        
        # Gerar resumo de competição
        summary = self._generate_competition_summary(category, competition_level, num_competitors, market_saturation)
        
        # Compilar dados
        competition_data = {
            'competition_level': competition_level,
            'num_competitors': num_competitors,
            'top_competitors': competitors,
            'market_saturation': market_saturation,
            'category': category,
            'entry_barriers': self._generate_entry_barriers(competition_level),
            'summary': summary
        }
        
        return competition_data
    
    def _generate_competitor_name(self, category):
        """
        Gera nomes de concorrentes simulados com base na categoria.
        
        Args:
            category (str): Categoria do negócio
            
        Returns:
            str: Nome simulado de concorrente
        """
        # Prefixos comuns para nomes de empresas
        prefixes = ['Super', 'Mega', 'Ultra', 'Top', 'Prime', 'Eco', 'Smart', 'Max', 'Global', 'Brasil']
        
        # Sufixos específicos por categoria
        category_terms = {
            'Tecnologia': ['Tech', 'Digital', 'Byte', 'Sys', 'Soft', 'Connect'],
            'Educação': ['Edu', 'Learn', 'School', 'Academy', 'Ensino', 'Cursos'],
            'Alimentação': ['Food', 'Gourmet', 'Sabor', 'Delícia', 'Chef', 'Express'],
            'Saúde': ['Saúde', 'Vida', 'Med', 'Care', 'Bem-estar', 'Health'],
            'Beleza': ['Beauty', 'Beleza', 'Style', 'Estética', 'Glamour', 'Charm'],
            'Pet': ['Pet', 'Animal', 'Dog', 'Cat', 'Vet', 'Patas'],
            'Moda': ['Fashion', 'Style', 'Trend', 'Look', 'Moda', 'Chic'],
            'Fitness': ['Fit', 'Gym', 'Sport', 'Health', 'Life', 'Body'],
            'Casa e Decoração': ['Home', 'Deco', 'Casa', 'Living', 'Design', 'Art']
        }
        
        # Obter termos para a categoria ou usar termos genéricos
        terms = category_terms.get(category, ['Express', 'Brasil', 'Top', 'Prime', 'Super'])
        
        # Gerar nome aleatório
        prefix = random.choice(prefixes)
        term = random.choice(terms)
        
        return f"{prefix} {term}"
    
    def _generate_competitive_advantages(self):
        """
        Gera vantagens competitivas simuladas.
        
        Returns:
            list: Lista de vantagens competitivas
        """
        advantages = [
            'Preços competitivos',
            'Localização estratégica',
            'Forte presença online',
            'Atendimento diferenciado',
            'Produtos exclusivos',
            'Tecnologia avançada',
            'Marca reconhecida',
            'Qualidade superior',
            'Fidelização de clientes',
            'Investimento em marketing',
            'Equipe especializada',
            'Logística eficiente'
        ]
        
        # Selecionar 2-4 vantagens aleatoriamente
        num_advantages = random.randint(2, 4)
        selected_advantages = random.sample(advantages, num_advantages)
        
        return selected_advantages
    
    def _generate_entry_barriers(self, competition_level):
        """
        Gera barreiras de entrada simuladas com base no nível de competição.
        
        Args:
            competition_level (str): Nível de competição ('low', 'medium', 'high')
            
        Returns:
            list: Lista de barreiras de entrada
        """
        barriers = {
            'low': [
                'Investimento inicial moderado',
                'Poucos concorrentes estabelecidos',
                'Regulamentação simples'
            ],
            'medium': [
                'Investimento inicial considerável',
                'Necessidade de diferenciação',
                'Concorrentes com presença estabelecida',
                'Fidelização de clientes pelos concorrentes'
            ],
            'high': [
                'Alto investimento inicial',
                'Mercado saturado',
                'Concorrentes com forte reconhecimento de marca',
                'Guerra de preços',
                'Altos custos de marketing para entrar no mercado',
                'Regulamentação complexa'
            ]
        }
        
        return barriers.get(competition_level, [])
    
    def _generate_competition_summary(self, category, competition_level, num_competitors, market_saturation):
        """
        Gera um resumo da análise de competição.
        
        Args:
            category (str): Categoria do negócio
            competition_level (str): Nível de competição
            num_competitors (int): Número de concorrentes
            market_saturation (float): Saturação do mercado
            
        Returns:
            str: Resumo da competição
        """
        # Resumos por nível de competição
        summaries = {
            'low': [
                f"O mercado de {category} apresenta competição relativamente baixa, com aproximadamente {num_competitors} concorrentes relevantes. Com uma saturação de mercado estimada em {market_saturation:.0%}, ainda há espaço para novos entrantes que ofereçam diferenciais competitivos.",
                f"A análise de competição para o setor de {category} indica um cenário favorável para novos negócios. Com poucos concorrentes estabelecidos ({num_competitors}) e saturação de mercado de {market_saturation:.0%}, há oportunidades para franquias que consigam se diferenciar."
            ],
            'medium': [
                f"O setor de {category} apresenta nível médio de competição, com cerca de {num_competitors} players relevantes. A saturação de mercado está em aproximadamente {market_saturation:.0%}, o que indica um equilíbrio entre oportunidades e desafios para novos entrantes.",
                f"A competição no mercado de {category} é moderada, com {num_competitors} concorrentes importantes. Com uma saturação de {market_saturation:.0%}, o sucesso dependerá da capacidade de oferecer diferenciais claros e estabelecer uma presença de mercado consistente."
            ],
            'high': [
                f"O mercado de {category} apresenta alta competitividade, com aproximadamente {num_competitors} concorrentes estabelecidos. A saturação de mercado de {market_saturation:.0%} indica que novos entrantes enfrentarão desafios significativos e precisarão de estratégias robustas de diferenciação.",
                f"A análise indica um cenário altamente competitivo no setor de {category}, com {num_competitors} players disputando mercado. Com saturação de {market_saturation:.0%}, recomenda-se cautela e um plano de negócios detalhado para novos entrantes."
            ]
        }
        
        # Selecionar resumo aleatório do nível apropriado
        competition_summaries = summaries.get(competition_level, summaries['medium'])
        selected_summary = random.choice(competition_summaries)
        
        return selected_summary
