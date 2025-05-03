# analysis/competition_analysis.py
import random
from datetime import datetime, timedelta

class CompetitionAnalyzer:
    """
    Classe responsável por analisar a concorrência para oportunidades de franquias
    """
    
    def __init__(self):
        """
        Inicializa o analisador de concorrência
        """
        # Lista de concorrentes comuns por setor para simulação
        self.sector_competitors = {
            'Alimentação': ['McDonald\'s', 'Burger King', 'Subway', 'Habib\'s', 'Bob\'s'],
            'Educação': ['Kumon', 'Wizard', 'CNA', 'CCAA', 'Microcamp'],
            'Saúde': ['Farmácias São Paulo', 'Drogasil', 'Farmácias Pague Menos', 'Clínica Viver', 'OdontoCompany'],
            'Beleza': ['O Boticário', 'L\'Acqua di Fiori', 'Beleza Natural', 'Onodera Estética', 'Jacques Janine'],
            'Moda': ['Hering', 'Puket', 'Arezzo', 'Havaianas', 'Chilli Beans'],
            'Tecnologia': ['iPlace', 'CellShop', 'Computer Store', 'TecToy', 'Geek.Etc.Br'],
            'Serviços': ['5àSec', 'Kumon', 'Maria Brasileira', 'Seguralta', 'HomeAngels'],
            'Pet': ['Cobasi', 'Petz', 'Pet Cursos', 'Animal Pet', 'Meu Amigo Pet'],
            'Fitness': ['Smart Fit', 'Bodytech', 'Bluefit', 'Curves', 'CrossFit'],
            'Casa e Decoração': ['Camicado', 'Etna', 'Imaginarium', 'Pontto Lavanderia', 'Casa & Video']
        }
        
    def analyze(self, opportunity):
        """
        Realiza análise de concorrência para uma oportunidade específica
        
        Args:
            opportunity (dict): Dados da oportunidade a ser analisada
            
        Returns:
            dict: Dados da análise de concorrência
        """
        print(f"CompetitionAnalyzer: Analisando concorrência para {opportunity.get('name', 'oportunidade')}")
        
        # Obter o setor da oportunidade
        sector = opportunity.get('sector', 'Serviços')
        
        # Identificar concorrentes para este setor
        competitors = self._identify_competitors(sector)
        
        # Analisar a densidade de concorrentes
        density_analysis = self._analyze_density(competitors)
        
        # Analisar forças e fraquezas da concorrência
        strengths_weaknesses = self._analyze_strengths_weaknesses(competitors)
        
        # Analisar diferenciação possível
        differentiation = self._analyze_differentiation(opportunity, competitors)
        
        # Análise resumida de concorrência
        competition_analysis = {
            'competitors': competitors,
            'density': density_analysis,
            'strengths_weaknesses': strengths_weaknesses,
            'differentiation': differentiation,
            'competition_level': self._calculate_competition_level(density_analysis, competitors),
            'market_gap_score': self._calculate_market_gap_score(density_analysis, differentiation),
            'entry_barrier': self._calculate_entry_barrier(opportunity, competitors),
            'analysis_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        return competition_analysis
    
    def _identify_competitors(self, sector):
        """Identifica os principais concorrentes para um setor"""
        
        # Obter concorrentes do setor ou usar uma lista genérica
        sector_competitors = self.sector_competitors.get(sector, [])
        
        if not sector_competitors:
            # Gerar nomes fictícios caso o setor não esteja na lista
            generic_competitors = [
                f"Empresa {chr(65 + i)}" for i in range(5)
            ]
            return generic_competitors
        
        # Selecionar aleatoriamente 3 a 5 concorrentes
        num_competitors = random.randint(3, min(5, len(sector_competitors)))
        selected_competitors = random.sample(sector_competitors, num_competitors)
        
        # Adicionar detalhes fictícios para cada concorrente
        enriched_competitors = []
        for competitor in selected_competitors:
            company = {
                'name': competitor,
                'market_share': round(random.uniform(5, 30), 2),
                'years_active': random.randint(3, 25),
                'num_units': random.randint(10, 500),
                'avg_rating': round(random.uniform(3.0, 4.9), 1),
                'price_level': random.choice(['baixo', 'médio', 'alto']),
                'strengths': self._generate_strengths(),
                'weaknesses': self._generate_weaknesses()
            }
            enriched_competitors.append(company)
        
        return enriched_competitors
    
    def _generate_strengths(self):
        """Gera pontos fortes fictícios para um concorrente"""
        all_strengths = [
            'Marca reconhecida', 'Boa localização', 'Preços competitivos', 
            'Atendimento de qualidade', 'Processos eficientes', 'Produtos exclusivos',
            'Marketing forte', 'Fidelidade dos clientes', 'Tecnologia avançada',
            'Boa relação com fornecedores', 'Treinamento eficaz'
        ]
        
        # Selecionar 2-4 pontos fortes
        num_strengths = random.randint(2, 4)
        return random.sample(all_strengths, num_strengths)
    
    def _generate_weaknesses(self):
        """Gera pontos fracos fictícios para um concorrente"""
        all_weaknesses = [
            'Preços elevados', 'Atendimento deficiente', 'Pouca variedade', 
            'Processos lentos', 'Marketing fraco', 'Localizações ruins',
            'Alta rotatividade de funcionários', 'Problemas de qualidade',
            'Tecnologia obsoleta', 'Pouca adaptação ao mercado', 'Gestão centralizada'
        ]
        
        # Selecionar 2-3 pontos fracos
        num_weaknesses = random.randint(2, 3)
        return random.sample(all_weaknesses, num_weaknesses)
    
    def _analyze_density(self, competitors):
        """Analisa a densidade de concorrentes no mercado"""
        
        # Verificar se competitors é uma lista de dicionários ou strings
        if competitors and isinstance(competitors[0], str):
            # Se forem strings, criar dicionários básicos
            competitors = [{'name': comp, 'num_units': random.randint(10, 500), 'years_active': random.randint(3, 25)} for comp in competitors]
        
        # Número de unidades totais dos concorrentes
        total_units = sum(comp.get('num_units', 0) for comp in competitors)
        
        # Calcular densidade por idade do mercado (simulação)
        avg_years = sum(comp.get('years_active', 5) for comp in competitors) / len(competitors)
        
        # Densidade relativa (índice fictício)
        if avg_years < 5:
            market_maturity = "Emergente"
            saturation_level = random.uniform(0.1, 0.3)
        elif avg_years < 10:
            market_maturity = "Em desenvolvimento"
            saturation_level = random.uniform(0.3, 0.6)
        else:
            market_maturity = "Maduro"
            saturation_level = random.uniform(0.6, 0.9)
        
        # Análise de densidade
        density_analysis = {
            'total_competitor_units': total_units,
            'market_maturity': market_maturity,
            'saturation_level': saturation_level,
            'geographic_concentration': random.choice(['Baixa', 'Média', 'Alta']),
            'density_trend': random.choice(['Crescente', 'Estável', 'Decrescente']),
            'comment': self._generate_density_comment(saturation_level, market_maturity)
        }
        
        return density_analysis
    
    def _generate_density_comment(self, saturation, maturity):
        """Gera comentário sobre a densidade do mercado"""
        
        if saturation < 0.3:
            if maturity == "Emergente":
                return "Mercado emergente com poucos players estabelecidos. Excelente momento para entrada."
            else:
                return "Densidade de concorrentes baixa, com boa oportunidade de estabelecer presença."
        elif saturation < 0.7:
            return "Mercado moderadamente competitivo. Diferenciação será importante para o sucesso."
        else:
            return "Mercado altamente saturado com forte competição. Recomenda-se estratégia de nicho."
    
    def _analyze_strengths_weaknesses(self, competitors):
        """Analisa pontos fortes e fracos comuns entre concorrentes"""
        
        # Verificar se competitors é uma lista de dicionários ou strings
        if competitors and isinstance(competitors[0], str):
            # Se forem strings, criar dicionários básicos com forças e fraquezas aleatórias
            enriched_competitors = []
            for comp in competitors:
                company = {
                    'name': comp,
                    'strengths': self._generate_strengths(),
                    'weaknesses': self._generate_weaknesses()
                }
                enriched_competitors.append(company)
            competitors = enriched_competitors
        
        # Contadores de forças e fraquezas
        all_strengths = {}
        all_weaknesses = {}
        
        # Contabilizar ocorrências
        for comp in competitors:
            for strength in comp.get('strengths', []):
                all_strengths[strength] = all_strengths.get(strength, 0) + 1
                
            for weakness in comp.get('weaknesses', []):
                all_weaknesses[weakness] = all_weaknesses.get(weakness, 0) + 1
        
        # Identificar padrões comuns
        common_strengths = [s for s, count in all_strengths.items() 
                           if count > len(competitors) / 3]
        common_weaknesses = [w for w, count in all_weaknesses.items() 
                            if count > len(competitors) / 3]
        
        # Análise de pontos fortes e fracos
        strengths_weaknesses_analysis = {
            'common_strengths': common_strengths,
            'common_weaknesses': common_weaknesses,
            'opportunity_areas': common_weaknesses,  # Áreas de oportunidade são as fraquezas comuns
            'threat_areas': common_strengths,  # Áreas de ameaça são as forças comuns
            'recommendation': self._generate_sw_recommendation(common_strengths, common_weaknesses)
        }
        
        return strengths_weaknesses_analysis
    
    def _generate_sw_recommendation(self, strengths, weaknesses):
        """Gera recomendação com base em forças e fraquezas comuns"""
        
        if not weaknesses:
            return "Concorrentes bem estabelecidos com poucos pontos fracos identificados. Considere inovação disruptiva."
        
        return f"Focar na exploração das fraquezas comuns: {', '.join(weaknesses)}. Desenvolver estratégias para mitigar forças concorrentes: {', '.join(strengths)}."
    
    def _analyze_differentiation(self, opportunity, competitors):
        """Analisa possíveis estratégias de diferenciação"""
        
        # Verificar se competitors é uma lista de dicionários ou strings
        if competitors and isinstance(competitors[0], str):
            # Se forem strings, criar dicionários básicos
            competitors = [{'name': comp} for comp in competitors]
        
        # Opções de diferenciação
        differentiation_options = [
            'Preço', 'Qualidade', 'Atendimento', 'Tecnologia', 
            'Localização', 'Exclusividade', 'Experiência', 'Personalização'
        ]
        
        # Selecionar aleatoriamente 2-3 estratégias
        num_strategies = random.randint(2, 3)
        selected_strategies = random.sample(differentiation_options, num_strategies)
        
        # Gerar detalhes para cada estratégia
        differentiation_details = {}
        for strategy in selected_strategies:
            differentiation_details[strategy] = self._generate_differentiation_detail(strategy, competitors)
        
        # Análise de diferenciação
        differentiation_analysis = {
            'recommended_strategies': selected_strategies,
            'details': differentiation_details,
            'differentiation_score': round(random.uniform(0.5, 0.9), 2),
            'implementation_difficulty': random.choice(['Baixa', 'Média', 'Alta']),
            'expected_impact': random.choice(['Moderado', 'Significativo', 'Alto']),
            'time_to_implementation': f"{random.randint(3, 12)} meses"
        }
        
        return differentiation_analysis
    
    def _generate_differentiation_detail(self, strategy, competitors):
        """Gera detalhe para uma estratégia de diferenciação"""
        
        if strategy == 'Preço':
            return "Oferecer preços mais competitivos ou estrutura de pagamento mais flexível que os concorrentes."
        elif strategy == 'Qualidade':
            return "Investir em produtos/serviços de qualidade superior, com materiais ou métodos diferenciados."
        elif strategy == 'Atendimento':
            return "Focar em atendimento personalizado e treinamento intensivo da equipe para superar expectativas."
        elif strategy == 'Tecnologia':
            return "Incorporar tecnologias inovadoras nos processos e na experiência do cliente."
        elif strategy == 'Localização':
            return "Explorar áreas não atendidas pelos concorrentes ou com maior potencial de crescimento."
        elif strategy == 'Exclusividade':
            return "Desenvolver produtos ou serviços exclusivos não oferecidos pelos concorrentes."
        elif strategy == 'Experiência':
            return "Criar uma experiência memorável para os clientes, com ambientação e processos diferenciados."
        else:  # Personalização
            return "Oferecer alto grau de personalização, permitindo ao cliente ajustar o produto/serviço às suas necessidades."
    
    def _calculate_competition_level(self, density_analysis, competitors):
        """Calcula o nível de competição no mercado"""
        
        # Verificar se competitors é uma lista de dicionários ou strings
        if competitors and isinstance(competitors[0], str):
            # Se forem strings, criar dicionários básicos
            competitors = [{'name': comp, 'market_share': random.uniform(5, 30)} for comp in competitors]
        
        # Fatores que influenciam o nível de competição
        saturation = density_analysis.get('saturation_level', 0.5)
        num_competitors = len(competitors)
        avg_market_share = sum(comp.get('market_share', 10) for comp in competitors) / len(competitors)
        
        # Fórmula fictícia para calcular nível de competição
        competition_level = (saturation * 0.5) + (num_competitors / 10 * 0.3) + (avg_market_share / 100 * 0.2)
        
        # Limitar entre 0 e 1
        competition_level = max(0, min(1, competition_level))
        
        # Classificação qualitativa
        if competition_level < 0.3:
            competition_class = "Baixa"
        elif competition_level < 0.7:
            competition_class = "Média"
        else:
            competition_class = "Alta"
        
        return {
            'level': round(competition_level, 2),
            'classification': competition_class,
            'reason': f"Baseado em saturação de {saturation:.2f}, {num_competitors} concorrentes principais e market share médio de {avg_market_share:.1f}%"
        }
    
    def _calculate_market_gap_score(self, density_analysis, differentiation):
        """Calcula a pontuação de oportunidade de mercado"""
        
        # Fatores que influenciam a oportunidade de mercado
        saturation = density_analysis.get('saturation_level', 0.5)
        diff_score = differentiation.get('differentiation_score', 0.6)
        
        # Fórmula para calcular pontuação
        gap_score = (1 - saturation) * 0.6 + diff_score * 0.4
        
        # Limitar entre 0 e 1
        gap_score = max(0, min(1, gap_score))
        
        # Classificação qualitativa
        if gap_score < 0.3:
            gap_class = "Pequena"
        elif gap_score < 0.7:
            gap_class = "Média"
        else:
            gap_class = "Grande"
        
        return {
            'score': round(gap_score, 2),
            'classification': gap_class,
            'comment': self._generate_gap_comment(gap_score)
        }
    
    def _generate_gap_comment(self, score):
        """Gera comentário sobre a oportunidade de mercado"""
        
        if score < 0.3:
            return "Mercado com poucas oportunidades claras. Exigirá inovação significativa para conquistar espaço."
        elif score < 0.7:
            return "Existem oportunidades de mercado moderadas que podem ser exploradas com estratégias adequadas."
        else:
            return "Excelentes oportunidades identificadas, com claros espaços para atuação no mercado."
    
    def _calculate_entry_barrier(self, opportunity, competitors):
        """Calcula barreiras de entrada para o mercado"""
        
        # Analisar investimento médio dos concorrentes
        avg_investment = opportunity.get('investment', {}).get('min', 100000)
        
        # Fatores que influenciam a barreira de entrada
        market_maturity = random.uniform(0.3, 0.8)  # Simulação
        regulatory_complexity = random.uniform(0.2, 0.7)  # Simulação
        technology_requirements = random.uniform(0.1, 0.6)  # Simulação
        brand_importance = random.uniform(0.3, 0.9)  # Simulação
        
        # Calcular pontuação de barreira
        barrier_factors = {
            'capital_requirement': avg_investment / 500000,  # Normalizado para 0-1
            'market_maturity': market_maturity,
            'regulatory_complexity': regulatory_complexity,
            'technology_requirements': technology_requirements,
            'brand_importance': brand_importance
        }
        
        # Média ponderada
        weights = {
            'capital_requirement': 0.3,
            'market_maturity': 0.2,
            'regulatory_complexity': 0.15,
            'technology_requirements': 0.15,
            'brand_importance': 0.2
        }
        
        barrier_score = sum(barrier_factors[k] * weights[k] for k in barrier_factors)
        
        # Limitar entre 0 e 1
        barrier_score = max(0, min(1, barrier_score))
        
        # Classificação qualitativa
        if barrier_score < 0.3:
            barrier_class = "Baixa"
        elif barrier_score < 0.7:
            barrier_class = "Média"
        else:
            barrier_class = "Alta"
        
        # Recomendações para superar barreiras
        recommendations = self._generate_barrier_recommendations(barrier_factors)
        
        return {
            'score': round(barrier_score, 2),
            'classification': barrier_class,
            'factors': {k: round(v, 2) for k, v in barrier_factors.items()},
            'recommendations': recommendations
        }
    
    def _generate_barrier_recommendations(self, factors):
        """Gera recomendações para superar barreiras de entrada"""
        
        recommendations = []
        
        # Analisar cada fator
        if factors['capital_requirement'] > 0.6:
            recommendations.append("Buscar financiamento ou investidores para superar a alta necessidade de capital inicial.")
            
        if factors['market_maturity'] > 0.6:
            recommendations.append("Desenvolver estratégia de nicho ou diferenciação em mercado maduro.")
            
        if factors['regulatory_complexity'] > 0.6:
            recommendations.append("Contratar consultoria especializada para navegar requisitos regulatórios complexos.")
            
        if factors['technology_requirements'] > 0.6:
            recommendations.append("Investir em parceiros tecnológicos ou desenvolvimento de capacidades internas.")
            
        if factors['brand_importance'] > 0.6:
            recommendations.append("Desenvolver estratégia de marketing agressiva para estabelecer reconhecimento de marca.")
            
        # Se não houver recomendações específicas
        if not recommendations:
            recommendations.append("Barreiras de entrada são relativamente baixas. Focar em execução e qualidade.")
            
        return recommendations
