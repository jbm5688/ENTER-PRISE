import logging
import random
from datetime import datetime

logger = logging.getLogger("franquia_finder")

class DemographicMatcher:
    """
    Classe responsável por analisar a compatibilidade demográfica de oportunidades de franquia.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o analisador demográfico.
        
        Args:
            config (dict): Configurações para análise demográfica
        """
        self.config = config or {}
    
    def match_demographics(self, opportunity):
        """
        Analisa a compatibilidade demográfica para uma oportunidade de franquia.
        
        Args:
            opportunity (dict): Dados da oportunidade
            
        Returns:
            dict: Dados de compatibilidade demográfica
        """
        print(f"DemographicMatcher: Analisando demografia para {opportunity.get('name', 'Oportunidade')}")
        
        # Extrair categoria
        category = opportunity.get('category', '')
        
        # Gerar dados demográficos
        demographic_data = self._generate_demographic_data(category, opportunity)
        
        return demographic_data
    
    def _generate_demographic_data(self, category, opportunity):
        """
        Gera dados demográficos simulados.
        
        Args:
            category (str): Categoria do negócio
            opportunity (dict): Dados da oportunidade
            
        Returns:
            dict: Dados demográficos simulados
        """
        # Perfis demográficos por categoria
        demographic_profiles = {
            'Tecnologia': {
                'age_range': '25-45',
                'income_level': 'medium-high',
                'education_level': 'higher',
                'urban_concentration': 'high',
                'digital_engagement': 'high'
            },
            'Educação': {
                'age_range': '30-50',
                'income_level': 'medium-high',
                'education_level': 'higher',
                'urban_concentration': 'medium',
                'digital_engagement': 'medium'
            },
            'Alimentação': {
                'age_range': '20-60',
                'income_level': 'medium',
                'education_level': 'varied',
                'urban_concentration': 'high',
                'digital_engagement': 'medium'
            },
            'Saúde': {
                'age_range': '30-55',
                'income_level': 'medium-high',
                'education_level': 'higher',
                'urban_concentration': 'medium',
                'digital_engagement': 'medium'
            },
            'Beleza': {
                'age_range': '25-50',
                'income_level': 'medium',
                'education_level': 'varied',
                'urban_concentration': 'high',
                'digital_engagement': 'high'
            },
            'Pet': {
                'age_range': '25-55',
                'income_level': 'medium',
                'education_level': 'varied',
                'urban_concentration': 'medium',
                'digital_engagement': 'medium'
            },
            'Moda': {
                'age_range': '18-45',
                'income_level': 'medium',
                'education_level': 'varied',
                'urban_concentration': 'high',
                'digital_engagement': 'high'
            },
            'Fitness': {
                'age_range': '20-45',
                'income_level': 'medium-high',
                'education_level': 'varied',
                'urban_concentration': 'high',
                'digital_engagement': 'high'
            },
            'Casa e Decoração': {
                'age_range': '30-60',
                'income_level': 'medium-high',
                'education_level': 'varied',
                'urban_concentration': 'medium',
                'digital_engagement': 'medium'
            }
        }
        
        # Obter perfil demográfico base ou usar perfil genérico
        base_profile = demographic_profiles.get(category, {
            'age_range': '25-55',
            'income_level': 'medium',
            'education_level': 'varied',
            'urban_concentration': 'medium',
            'digital_engagement': 'medium'
        })
        
        # Calcular tamanho do mercado potencial
        market_size = self._calculate_market_size(category, opportunity, base_profile)
        
        # Calcular clientes potenciais
        potential_customers = int(market_size * random.uniform(0.001, 0.01))
        
        # Calcular compatibilidade demográfica
        compatibility_score = random.uniform(0.5, 0.95)
        
        # Regiões recomendadas
        recommended_regions = self._get_recommended_regions(category, base_profile)
        
        # Gerar resumo demográfico
        summary = self._generate_demographic_summary(
            category, base_profile, market_size, potential_customers, compatibility_score
        )
        
        # Compilar dados
        demographic_data = {
            'target_profile': base_profile,
            'market_size': market_size,
            'potential_customers': potential_customers,
            'compatibility_score': compatibility_score,
            'recommended_regions': recommended_regions,
            'category': category,
            'summary': summary
        }
        
        return demographic_data
    
    def _calculate_market_size(self, category, opportunity, profile):
        """
        Calcula o tamanho potencial do mercado.
        
        Args:
            category (str): Categoria do negócio
            opportunity (dict): Dados da oportunidade
            profile (dict): Perfil demográfico
            
        Returns:
            int: Tamanho estimado do mercado
        """
        # Base de cálculo
        base_size = random.randint(500000, 5000000)
        
        # Fatores de ajuste
        
        # Concentração urbana
        urban_factors = {
            'low': 0.6,
            'medium': 1.0,
            'high': 1.4
        }
        
        urban_factor = urban_factors.get(profile.get('urban_concentration', 'medium'), 1.0)
        
        # Nível de renda
        income_factors = {
            'low': 0.7,
            'medium': 1.0,
            'medium-high': 1.3,
            'high': 1.6
        }
        
        income_factor = income_factors.get(profile.get('income_level', 'medium'), 1.0)
        
        # Fatores específicos por categoria
        category_factors = {
            'Alimentação': 1.4,
            'Pet': 1.2,
            'Saúde': 1.3,
            'Tecnologia': 1.1,
            'Educação': 1.0,
            'Beleza': 1.2,
            'Moda': 1.3,
            'Fitness': 1.1,
            'Casa e Decoração': 1.0
        }
        
        category_factor = category_factors.get(category, 1.0)
        
        # Calcular tamanho total
        market_size = int(base_size * urban_factor * income_factor * category_factor)
        
        return market_size
    
    def _get_recommended_regions(self, category, profile):
        """
        Determina regiões recomendadas com base na categoria e perfil.
        
        Args:
            category (str): Categoria do negócio
            profile (dict): Perfil demográfico
            
        Returns:
            list: Lista de regiões recomendadas
        """
        # Regiões por concentração urbana
        regions_by_urban = {
            'high': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Brasília', 'Salvador'],
            'medium': ['Curitiba', 'Recife', 'Porto Alegre', 'Fortaleza', 'Goiânia', 'Campinas'],
            'low': ['Ribeirão Preto', 'São José dos Campos', 'Florianópolis', 'Joinville', 'Uberlândia']
        }
        
        # Regiões por categoria
        regions_by_category = {
            'Tecnologia': ['São Paulo', 'Campinas', 'Rio de Janeiro', 'Belo Horizonte', 'Florianópolis'],
            'Educação': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Recife'],
            'Alimentação': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Fortaleza'],
            'Saúde': ['São Paulo', 'Belo Horizonte', 'Brasília', 'Porto Alegre', 'Curitiba'],
            'Beleza': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Recife'],
            'Pet': ['São Paulo', 'Rio de Janeiro', 'Curitiba', 'Porto Alegre', 'Campinas'],
            'Moda': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Recife'],
            'Fitness': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Brasília', 'Goiânia'],
            'Casa e Decoração': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Curitiba', 'Goiânia']
        }
        
        # Obter regiões por concentração urbana
        urban_concentration = profile.get('urban_concentration', 'medium')
        urban_regions = regions_by_urban.get(urban_concentration, regions_by_urban['medium'])
        
        # Obter regiões por categoria
        category_regions = regions_by_category.get(category, regions_by_urban['medium'])
        
        # Combinar e selecionar regiões únicas
        combined_regions = list(set(urban_regions + category_regions))
        
        # Limitar número de regiões
        num_regions = random.randint(3, 5)
        recommended_regions = random.sample(combined_regions, min(num_regions, len(combined_regions)))
        
        return recommended_regions
    
    def _generate_demographic_summary(self, category, profile, market_size, potential_customers, compatibility_score):
        """
        Gera um resumo da análise demográfica.
        
        Args:
            category (str): Categoria do negócio
            profile (dict): Perfil demográfico
            market_size (int): Tamanho do mercado
            potential_customers (int): Clientes potenciais
            compatibility_score (float): Pontuação de compatibilidade
            
        Returns:
            str: Resumo demográfico
        """
        # Formatação de valores
        market_size_formatted = f"{market_size:,}".replace(',', '.')
        potential_customers_formatted = f"{potential_customers:,}".replace(',', '.')
        compatibility_percentage = f"{compatibility_score * 100:.1f}%"
        
        # Resumos por nível de compatibilidade
        if compatibility_score > 0.8:
            summary = f"A análise demográfica indica uma excelente compatibilidade ({compatibility_percentage}) para o segmento de {category}. Com um mercado potencial estimado em {market_size_formatted} pessoas e aproximadamente {potential_customers_formatted} clientes potenciais diretos, a oportunidade apresenta um perfil demográfico altamente favorável. O público-alvo principal está na faixa etária de {profile.get('age_range')}, com nível de renda {profile.get('income_level', 'médio')} e concentração urbana {profile.get('urban_concentration', 'média')}."
        elif compatibility_score > 0.6:
            summary = f"A análise demográfica mostra uma boa compatibilidade ({compatibility_percentage}) para o segmento de {category}. O mercado potencial é estimado em {market_size_formatted} pessoas, com cerca de {potential_customers_formatted} clientes potenciais diretos. O perfil demográfico é favorável, com público-alvo na faixa etária de {profile.get('age_range')}, nível de renda {profile.get('income_level', 'médio')} e concentração urbana {profile.get('urban_concentration', 'média')}."
        else:
            summary = f"A análise demográfica indica uma compatibilidade moderada ({compatibility_percentage}) para o segmento de {category}. O mercado potencial é estimado em {market_size_formatted} pessoas, com aproximadamente {potential_customers_formatted} clientes potenciais diretos. O perfil demográfico apresenta desafios a serem considerados, com público-alvo na faixa etária de {profile.get('age_range')}, nível de renda {profile.get('income_level', 'médio')} e concentração urbana {profile.get('urban_concentration', 'média')}."
            
        return summary
