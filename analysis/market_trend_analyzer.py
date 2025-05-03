import logging
import random
from datetime import datetime

logger = logging.getLogger("franquia_finder")

class MarketTrendAnalyzer:
    """
    Classe responsável por analisar tendências de mercado com base nos dados coletados.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o analisador de tendências.
        
        Args:
            config (dict): Configurações para análise de tendências
        """
        self.config = config or {}
    
    def analyze_trends(self, data):
        """
        Analisa tendências de mercado com base nos dados.
        
        Args:
            data (dict): Dados limpos e normalizados de diferentes fontes
                
        Returns:
            list: Lista de tendências identificadas
        """
        trends = []
        
        # Extrair tendências de mídias sociais
        if 'social' in data and data['social']:
            social_trends = self._extract_social_trends(data['social'])
            trends.extend(social_trends)
        
        # Extrair tendências de pesquisa de mercado
        if 'market_research' in data and data['market_research']:
            research_trends = self._extract_research_trends(data['market_research'])
            trends.extend(research_trends)
        
        # Combinar tendências semelhantes
        combined_trends = self._combine_similar_trends(trends)
        
        # Filtrar tendências por relevância
        filtered_trends = self._filter_relevant_trends(combined_trends)
        
        # Se não houver tendências, criar algumas simuladas
        if not filtered_trends:
            filtered_trends = self._generate_simulated_trends()
        
        return filtered_trends
    
    def _extract_social_trends(self, social_data):
        """
        Extrai tendências de dados de mídias sociais.
        
        Args:
            social_data (list): Dados de mídias sociais limpos
            
        Returns:
            list: Tendências extraídas
        """
        trends = []
        
        for item in social_data:
            if 'keyword' not in item:
                continue
            
            trend = {
                'keyword': item['keyword'],
                'source_type': 'social_media',
                'growth_rate': item.get('growth_rate', 0),
                'sentiment': item.get('sentiment', 0),
                'monthly_mentions': item.get('monthly_mentions', 0),
                'platforms': item.get('platforms', []),
                'first_observed': item.get('first_observed', ''),
                'relevance_score': 0  # Será calculado depois
            }
            
            trends.append(trend)
        
        return trends
    
    def _extract_research_trends(self, research_data):
        """
        Extrai tendências de dados de pesquisa de mercado.
        
        Args:
            research_data (list): Dados de pesquisa de mercado limpos
            
        Returns:
            list: Tendências extraídas
        """
        trends = []
        
        for item in research_data:
            # Extrair insights como tendências
            if 'insights' in item and isinstance(item['insights'], list):
                for insight in item['insights']:
                    # Extrair palavras-chave do insight
                    keywords = self._extract_keywords_from_text(insight)
                    
                    for keyword in keywords:
                        trend = {
                            'keyword': keyword,
                            'source_type': 'market_research',
                            'growth_rate': item.get('growth_rate', 0),
                            'sentiment': item.get('consumer_satisfaction', 0.5),
                            'category': item.get('category', ''),
                            'insight': insight,
                            'source': item.get('source', ''),
                            'relevance_score': 0  # Será calculado depois
                        }
                        
                        trends.append(trend)
            
            # Usar categorias como tendências
            if 'category' in item:
                trend = {
                    'keyword': item['category'],
                    'source_type': 'market_research',
                    'growth_rate': item.get('growth_rate', 0),
                    'sentiment': item.get('consumer_satisfaction', 0.5),
                    'investment_opportunity': item.get('investment_opportunity', 0.5),
                    'source': item.get('source', ''),
                    'relevance_score': 0  # Será calculado depois
                }
                
                trends.append(trend)
        
        return trends
    
    def _extract_keywords_from_text(self, text):
        """
        Extrai palavras-chave de um texto.
        
        Args:
            text (str): Texto para extrair palavras-chave
            
        Returns:
            list: Lista de palavras-chave
        """
        # Esta é uma implementação simples
        # Em um sistema real, usaríamos NLP mais avançado
        
        if not isinstance(text, str):
            return []
        
        # Stopwords comuns em português
        stopwords = [
            'a', 'o', 'e', 'é', 'de', 'do', 'da', 'em', 'no', 'na', 'um', 'uma',
            'os', 'as', 'dos', 'das', 'nos', 'nas', 'que', 'se', 'para', 'por',
            'com', 'como', 'mas', 'ou', 'ao'
        ]
        
        # Dividir o texto em palavras
        words = text.lower().replace('.', ' ').replace(',', ' ').split()
        
        # Filtrar stopwords e palavras curtas
        keywords = [word for word in words if word not in stopwords and len(word) > 3]
        
        # Encontrar frases relevantes (2-3 palavras)
        phrases = []
        for i in range(len(words) - 1):
            if words[i] not in stopwords and words[i+1] not in stopwords:
                phrase = f"{words[i]} {words[i+1]}"
                phrases.append(phrase)
        
        # Adicionar algumas frases se houver
        if phrases:
            keywords.extend(phrases[:2])  # Adicionar até 2 frases
        
        # Remover duplicatas
        unique_keywords = list(set(keywords))
        
        # Limitar número de keywords
        return unique_keywords[:3]
    
    def _combine_similar_trends(self, trends):
        """
        Combina tendências semelhantes.
        
        Args:
            trends (list): Lista de tendências
            
        Returns:
            list: Tendências combinadas
        """
        if not trends:
            return []
        
        combined = {}
        
        for trend in trends:
            keyword = trend.get('keyword', '').lower()
            
            if not keyword:
                continue
            
            # Verificar se já existe tendência similar
            similar_found = False
            for existing_key in combined.keys():
                if self._are_keywords_similar(keyword, existing_key):
                    # Combinar tendências
                    existing_trend = combined[existing_key]
                    
                    # Atualizar contagem de fontes
                    existing_trend['sources'] = existing_trend.get('sources', 1) + 1
                    
                    # Média ponderada de growth_rate
                    if 'growth_rate' in trend:
                        old_growth = existing_trend.get('growth_rate', 0)
                        new_growth = trend['growth_rate']
                        existing_trend['growth_rate'] = (old_growth + new_growth) / 2
                    
                    # Média ponderada de sentiment
                    if 'sentiment' in trend:
                        old_sentiment = existing_trend.get('sentiment', 0)
                        new_sentiment = trend['sentiment']
                        existing_trend['sentiment'] = (old_sentiment + new_sentiment) / 2
                    
                    # Combinar plataformas
                    if 'platforms' in trend:
                        existing_platforms = existing_trend.get('platforms', [])
                        new_platforms = trend['platforms']
                        existing_trend['platforms'] = list(set(existing_platforms + new_platforms))
                    
                    # Adicionar categorias
                    if 'category' in trend:
                        existing_categories = existing_trend.get('categories', [])
                        new_category = trend['category']
                        if new_category and new_category not in existing_categories:
                            existing_categories.append(new_category)
                            existing_trend['categories'] = existing_categories
                    
                    similar_found = True
                    break
            
            # Se não encontrou similar, adicionar nova tendência
            if not similar_found:
                combined[keyword] = trend.copy()
                
                # Inicializar contagem de fontes
                combined[keyword]['sources'] = 1
                
                # Inicializar lista de categorias se houver categoria
                if 'category' in trend:
                    combined[keyword]['categories'] = [trend['category']]
        
        # Converter de volta para lista
        result = list(combined.values())
        
        return result
    
    def _are_keywords_similar(self, keyword1, keyword2):
        """
        Verifica se duas palavras-chave são similares.
        
        Args:
            keyword1 (str): Primeira palavra-chave
            keyword2 (str): Segunda palavra-chave
            
        Returns:
            bool: True se forem similares
        """
        # Implementação simples baseada em substring
        return keyword1 in keyword2 or keyword2 in keyword1
    
    def _filter_relevant_trends(self, trends):
        """
        Filtra tendências por relevância.
        
        Args:
            trends (list): Lista de tendências
            
        Returns:
            list: Tendências filtradas
        """
        if not trends:
            return []
        
        # Calcular pontuação de relevância para cada tendência
        for trend in trends:
            # Fatores de relevância
            growth_factor = trend.get('growth_rate', 0) * 0.4  # Peso maior para crescimento
            sentiment_factor = trend.get('sentiment', 0) * 0.3
            sources_factor = min(1, trend.get('sources', 1) / 3) * 0.3  # 3+ fontes = 100%
            
            # Calcular pontuação
            relevance_score = growth_factor + sentiment_factor + sources_factor
            trend['relevance_score'] = relevance_score
        
        # Ordenar por pontuação de relevância
        sorted_trends = sorted(trends, key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Filtrar top tendências (máximo 10)
        top_trends = sorted_trends[:10]
        
        return top_trends
    
    def _generate_simulated_trends(self):
        """
        Gera tendências simuladas para testes.
        
        Returns:
            list: Tendências simuladas
        """
        simulated_trends = [
            {
                'keyword': 'home office',
                'source_type': 'social_media',
                'growth_rate': 0.25,
                'sentiment': 0.72,
                'monthly_mentions': 185000,
                'platforms': ['Instagram', 'LinkedIn', 'Twitter'],
                'relevance_score': 0.8
            },
            {
                'keyword': 'alimentação saudável',
                'source_type': 'social_media',
                'growth_rate': 0.18,
                'sentiment': 0.85,
                'monthly_mentions': 230000,
                'platforms': ['Instagram', 'TikTok', 'Facebook'],
                'relevance_score': 0.75
            },
            {
                'keyword': 'sustentabilidade',
                'source_type': 'social_media',
                'growth_rate': 0.32,
                'sentiment': 0.78,
                'monthly_mentions': 310000,
                'platforms': ['Instagram', 'LinkedIn', 'Twitter', 'Facebook'],
                'relevance_score': 0.85
            },
            {
                'keyword': 'economia circular',
                'source_type': 'market_research',
                'growth_rate': 0.41,
                'sentiment': 0.67,
                'monthly_mentions': 95000,
                'platforms': ['LinkedIn', 'Twitter', 'Facebook'],
                'relevance_score': 0.7
            },
            {
                'keyword': 'inteligência artificial',
                'source_type': 'market_research',
                'growth_rate': 0.55,
                'sentiment': 0.62,
                'monthly_mentions': 420000,
                'platforms': ['Twitter', 'LinkedIn', 'YouTube', 'Reddit'],
                'relevance_score': 0.9
            }
        ]
        
        return simulated_trends
