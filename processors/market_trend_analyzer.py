# processors/market_trend_analyzer.py
import random
from datetime import datetime, timedelta

class MarketTrendAnalyzer:
    """
    Classe responsável por analisar tendências de mercado com base nos dados coletados
    """
    
    def __init__(self):
        """
        Inicializa o analisador de tendências de mercado
        """
        self.sectors = [
            'Alimentação', 'Educação', 'Saúde', 'Beleza', 'Moda', 
            'Tecnologia', 'Serviços', 'Pet', 'Fitness', 'Casa e Decoração'
        ]
        
    def analyze(self, data):
        """
        Analisa tendências de mercado com base nos dados coletados
        
        Args:
            data (dict): Dados limpos
            
        Returns:
            list: Lista de tendências de mercado identificadas
        """
        print("MarketTrendAnalyzer: Analisando tendências de mercado...")
        
        # Implementação básica que retorna dados fictícios
        trends = []
        
        # Se existem dados de redes sociais, criar tendências com base nesses dados
        if 'social_trends' in data and data['social_trends']:
            for trend_data in data['social_trends']:
                trend = self._create_trend_from_social(trend_data)
                trends.append(trend)
        
        # Se existem dados de vendas, criar tendências com base nesses dados
        if 'sales_data' in data and data['sales_data']:
            for sales_item in data['sales_data']:
                trend = self._create_trend_from_sales(sales_item)
                if trend not in trends:  # Evitar duplicações
                    trends.append(trend)
        
        # Se não há dados suficientes, gerar tendências fictícias
        if len(trends) < 5:
            additional_trends = self._generate_sample_trends(5 - len(trends))
            trends.extend(additional_trends)
        
        return trends
    
    def _create_trend_from_social(self, social_data):
        """Cria uma tendência com base em dados de redes sociais"""
        
        # Valores fictícios para simular tendências
        keyword = social_data.get('keyword', 'Tendência')
        growth = random.uniform(0.1, 0.5)
        
        trend = {
            'name': keyword,
            'sector': random.choice(self.sectors),
            'growth_rate': growth,
            'source': 'social_media',
            'confidence': random.uniform(0.6, 0.9),
            'first_observed': (datetime.now() - timedelta(days=random.randint(10, 90))).strftime('%Y-%m-%d'),
            'description': f'Tendência crescente para {keyword} identificada em redes sociais',
            'associated_keywords': self._generate_related_keywords(keyword)
        }
        
        return trend
    
    def _create_trend_from_sales(self, sales_data):
        """Cria uma tendência com base em dados de vendas"""
        
        # Valores fictícios para simular tendências
        product = sales_data.get('product', 'Produto')
        growth = random.uniform(0.05, 0.3)
        
        trend = {
            'name': product,
            'sector': sales_data.get('category', random.choice(self.sectors)),
            'growth_rate': growth,
            'source': 'sales_data',
            'confidence': random.uniform(0.7, 0.95),
            'first_observed': (datetime.now() - timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d'),
            'description': f'Aumento consistente nas vendas de {product} nos últimos meses',
            'associated_keywords': self._generate_related_keywords(product)
        }
        
        return trend
    
    def _generate_related_keywords(self, keyword):
        """Gera palavras-chave relacionadas a uma tendência"""
        
        # Versão básica - apenas gera alguns termos aleatórios
        prefixes = ['novo', 'melhor', 'premium', 'eco', 'smart', 'top']
        suffixes = ['plus', 'pro', 'express', 'max', 'brasil', 'tech']
        
        related = []
        for _ in range(3):
            if random.random() > 0.5:
                related.append(f"{random.choice(prefixes)} {keyword}")
            else:
                related.append(f"{keyword} {random.choice(suffixes)}")
        
        return related
    
    def _generate_sample_trends(self, count=5):
        """Gera tendências fictícias para teste"""
        
        sample_trends = [
            {
                'name': 'Alimentação Plant-Based',
                'sector': 'Alimentação',
                'growth_rate': 0.42,
                'source': 'market_research',
                'confidence': 0.85,
                'first_observed': '2024-02-15',
                'description': 'Crescimento acelerado no consumo de alimentos vegetais e substitutos de carne',
                'associated_keywords': ['plant-based', 'vegetariano', 'comida saudável']
            },
            {
                'name': 'Micromobilidade Urbana',
                'sector': 'Transporte',
                'growth_rate': 0.38,
                'source': 'market_research',
                'confidence': 0.80,
                'first_observed': '2024-01-10',
                'description': 'Aumento na demanda por soluções de transporte individual para curtas distâncias',
                'associated_keywords': ['patinetes elétricos', 'bikes compartilhadas', 'mobilidade sustentável']
            },
            {
                'name': 'Educação Híbrida',
                'sector': 'Educação',
                'growth_rate': 0.35,
                'source': 'market_research',
                'confidence': 0.90,
                'first_observed': '2024-03-05',
                'description': 'Modelos educacionais que combinam experiências presenciais e online',
                'associated_keywords': ['ensino híbrido', 'educação digital', 'cursos flexíveis']
            },
            {
                'name': 'Saúde Mental',
                'sector': 'Saúde',
                'growth_rate': 0.45,
                'source': 'market_research',
                'confidence': 0.95,
                'first_observed': '2023-11-20',
                'description': 'Crescente demanda por serviços e produtos relacionados ao bem-estar psicológico',
                'associated_keywords': ['terapia online', 'mindfulness', 'autocuidado']
            },
            {
                'name': 'Cosmética Natural',
                'sector': 'Beleza',
                'growth_rate': 0.32,
                'source': 'market_research',
                'confidence': 0.75,
                'first_observed': '2023-10-15',
                'description': 'Preferência crescente por produtos de beleza com ingredientes naturais e sustentáveis',
                'associated_keywords': ['beleza natural', 'cosmética vegana', 'clean beauty']
            },
            {
                'name': 'Casa Inteligente',
                'sector': 'Tecnologia',
                'growth_rate': 0.36,
                'source': 'market_research',
                'confidence': 0.85,
                'first_observed': '2023-12-10',
                'description': 'Popularização de dispositivos e sistemas para automação residencial',
                'associated_keywords': ['smart home', 'internet das coisas', 'automação residencial']
            },
            {
                'name': 'Serviços para Pets',
                'sector': 'Pet',
                'growth_rate': 0.40,
                'source': 'market_research',
                'confidence': 0.82,
                'first_observed': '2024-02-28',
                'description': 'Expansão acelerada no mercado de serviços especializados para animais de estimação',
                'associated_keywords': ['pet care', 'hotel para pets', 'creche de animais']
            }
        ]
        
        return sample_trends[:count]
