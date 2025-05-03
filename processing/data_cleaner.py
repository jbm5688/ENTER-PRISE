import pandas as pd
import re
import logging
from datetime import datetime
import numpy as np

logger = logging.getLogger("franquia_finder")

class DataCleaner:
    """
    Classe responsável por limpar e normalizar dados coletados de diferentes fontes.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o limpador de dados.
        
        Args:
            config (dict): Configurações para limpeza de dados
        """
        self.config = config or {}
    
    def clean_data(self, data_dict):
        """
        Limpa e normaliza dados de diferentes fontes.
        
        Args:
            data_dict (dict): Dicionário com dados de diferentes fontes
                - 'sales': Dados de vendas
                - 'social': Dados de mídias sociais
                - 'market_research': Dados de pesquisa de mercado
                - 'web': Dados coletados da web
                
        Returns:
            dict: Dicionário com dados limpos e normalizados
        """
        cleaned_data = {}
        
        # Limpar dados de vendas
        if 'sales' in data_dict and data_dict['sales']:
            cleaned_data['sales'] = self._clean_sales_data(data_dict['sales'])
        
        # Limpar dados de mídias sociais
        if 'social' in data_dict and data_dict['social']:
            cleaned_data['social'] = self._clean_social_data(data_dict['social'])
        
        # Limpar dados de pesquisa de mercado
        if 'market_research' in data_dict and data_dict['market_research']:
            cleaned_data['market_research'] = self._clean_market_research_data(data_dict['market_research'])
        
        # Limpar dados da web
        if 'web' in data_dict and data_dict['web']:
            cleaned_data['web'] = self._clean_web_data(data_dict['web'])
        
        # Normalizar categorias entre as fontes de dados
        cleaned_data = self._normalize_categories(cleaned_data)
        
        return cleaned_data
    
    def _clean_sales_data(self, sales_data):
        """
        Limpa e padroniza dados de vendas.
        
        Args:
            sales_data (list): Lista de dados de vendas
            
        Returns:
            list: Dados de vendas limpos
        """
        cleaned_sales = []
        
        for item in sales_data:
            # Criar cópia do item
            cleaned_item = item.copy()
            
            # Normalizar nomes de colunas (converter para snake_case)
            cleaned_item = {self._to_snake_case(k): v for k, v in cleaned_item.items()}
            
            # Garantir que valores numéricos são números
            for key in ['total_sales', 'growth_rate', 'average_ticket', 'conversion_rate']:
                if key in cleaned_item:
                    cleaned_item[key] = self._convert_to_numeric(cleaned_item[key])
            
            # Garantir que categorias são strings
            if 'category' in cleaned_item:
                cleaned_item['category'] = str(cleaned_item['category'])
            
            # Adicionar timestamp de limpeza
            cleaned_item['cleaned_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cleaned_sales.append(cleaned_item)
        
        return cleaned_sales
    
    def _clean_social_data(self, social_data):
        """
        Limpa e padroniza dados de mídias sociais.
        
        Args:
            social_data (list): Lista de dados de mídias sociais
            
        Returns:
            list: Dados de mídias sociais limpos
        """
        cleaned_social = []
        
        for item in social_data:
            # Criar cópia do item
            cleaned_item = item.copy()
            
            # Normalizar nomes de colunas (converter para snake_case)
            cleaned_item = {self._to_snake_case(k): v for k, v in cleaned_item.items()}
            
            # Garantir que valores numéricos são números
            for key in ['monthly_mentions', 'sentiment', 'growth_rate']:
                if key in cleaned_item:
                    cleaned_item[key] = self._convert_to_numeric(cleaned_item[key])
            
            # Garantir que plataformas é uma lista
            if 'platforms' in cleaned_item and not isinstance(cleaned_item['platforms'], list):
                if isinstance(cleaned_item['platforms'], str):
                    cleaned_item['platforms'] = [p.strip() for p in cleaned_item['platforms'].split(',')]
                else:
                    cleaned_item['platforms'] = [str(cleaned_item['platforms'])]
            
            # Adicionar timestamp de limpeza
            cleaned_item['cleaned_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cleaned_social.append(cleaned_item)
        
        return cleaned_social
    
    def _clean_market_research_data(self, market_data):
        """
        Limpa e padroniza dados de pesquisa de mercado.
        
        Args:
            market_data (list): Lista de dados de pesquisa de mercado
            
        Returns:
            list: Dados de pesquisa de mercado limpos
        """
        cleaned_market = []
        
        for item in market_data:
            # Criar cópia do item
            cleaned_item = item.copy()
            
            # Normalizar nomes de colunas (converter para snake_case)
            cleaned_item = {self._to_snake_case(k): v for k, v in cleaned_item.items()}
            
            # Garantir que valores numéricos são números
            for key in ['market_size', 'growth_rate', 'consumer_satisfaction', 'investment_opportunity']:
                if key in cleaned_item:
                    cleaned_item[key] = self._convert_to_numeric(cleaned_item[key])
            
            # Garantir que insights e success_criteria são listas
            for key in ['insights', 'success_criteria', 'keywords']:
                if key in cleaned_item and not isinstance(cleaned_item[key], list):
                    if isinstance(cleaned_item[key], str):
                        cleaned_item[key] = [p.strip() for p in cleaned_item[key].split(',')]
                    else:
                        cleaned_item[key] = [str(cleaned_item[key])]
            
            # Adicionar timestamp de limpeza
            cleaned_item['cleaned_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cleaned_market.append(cleaned_item)
        
        return cleaned_market
    
    def _clean_web_data(self, web_data):
        """
        Limpa e padroniza dados coletados da web.
        
        Args:
            web_data (list): Lista de dados coletados da web
            
        Returns:
            list: Dados da web limpos
        """
        cleaned_web = []
        
        for item in web_data:
            # Criar cópia do item
            cleaned_item = item.copy()
            
            # Normalizar nomes de colunas (converter para snake_case)
            cleaned_item = {self._to_snake_case(k): v for k, v in cleaned_item.items()}
            
            # Garantir que valores numéricos são números
            for key in ['initial_investment', 'franchise_fee', 'royalty_fee_percentage', 
                       'avg_monthly_revenue', 'roi_percentage', 'payback_period_months']:
                if key in cleaned_item:
                    cleaned_item[key] = self._convert_to_numeric(cleaned_item[key])
            
            # Remover caracteres especiais do nome
            if 'name' in cleaned_item:
                cleaned_item['name'] = re.sub(r'[^\w\s]', '', cleaned_item['name'])
            
            # Adicionar timestamp de limpeza
            cleaned_item['cleaned_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cleaned_web.append(cleaned_item)
        
        return cleaned_web
    
    def _normalize_categories(self, cleaned_data):
        """
        Normaliza categorias entre diferentes fontes de dados.
        
        Args:
            cleaned_data (dict): Dados limpos de diferentes fontes
            
        Returns:
            dict: Dados com categorias normalizadas
        """
        # Mapeamento de categorias para padronizar
        category_mapping = {
            # Alimentação
            'food': 'Alimentação',
            'restaurant': 'Alimentação',
            'fast food': 'Alimentação',
            'alimentos': 'Alimentação',
            'alimentação saudável': 'Alimentação Saudável',
            'saudável': 'Alimentação Saudável',
            'healthy food': 'Alimentação Saudável',
            
            # Educação
            'education': 'Educação',
            'ensino': 'Educação',
            'curso': 'Educação',
            'cursos online': 'Educação',
            'educação': 'Educação',
            
            # Tecnologia
            'tech': 'Tecnologia',
            'tecnologia': 'Tecnologia',
            'informática': 'Tecnologia',
            'digital': 'Tecnologia',
            
            # Pet
            'pet': 'Pet',
            'animais': 'Pet',
            'pet shop': 'Pet',
            
            # Outros setores
            'saúde': 'Saúde',
            'health': 'Saúde',
            'beleza': 'Beleza',
            'beauty': 'Beleza',
            'fitness': 'Fitness',
            'academia': 'Fitness',
            'moda': 'Moda',
            'fashion': 'Moda',
            'home': 'Casa e Decoração',
            'casa': 'Casa e Decoração',
            'decoração': 'Casa e Decoração',
        }
        
        # Normalizar categorias em cada fonte
        for source, data_list in cleaned_data.items():
            for item in data_list:
                if 'category' in item:
                    category = item['category'].lower() if isinstance(item['category'], str) else ''
                    
                    # Verificar no mapeamento
                    if category in category_mapping:
                        item['category'] = category_mapping[category]
                    elif category:
                        # Capitalizar primeira letra
                        item['category'] = category.capitalize()
        
        return cleaned_data
    
    def _to_snake_case(self, name):
        """
        Converte string para snake_case.
        
        Args:
            name (str): String para converter
            
        Returns:
            str: String em snake_case
        """
        # Substituir espaços e outros separadores por underscore
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1)
        # Substituir caracteres não alfanuméricos por underscore
        s3 = re.sub(r'[^a-zA-Z0-9]', '_', s2)
        # Converter para minúsculas e remover underscores duplicados
        return re.sub(r'_+', '_', s3).lower().strip('_')
    
    def _convert_to_numeric(self, value):
        """
        Converte um valor para numérico.
        
        Args:
            value: Valor a ser convertido
            
        Returns:
            float: Valor numérico ou 0 se não for possível converter
        """
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str):
            # Remover símbolos de moeda e outros caracteres não numéricos
            cleaned = re.sub(r'[^\d.,\-]', '', value.replace(',', '.'))
            try:
                return float(cleaned)
            except (ValueError, TypeError):
                return 0.0
        
        return 0.0
