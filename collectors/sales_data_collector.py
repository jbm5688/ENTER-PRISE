import requests
import pandas as pd
import json
import logging
import time
from datetime import datetime, timedelta
import os
import re
import random

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/sales_data_collector.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("sales_data_collector")

class SalesDataCollector:
    """
    Classe para coletar estatísticas de vendas de produtos e oportunidades de franquia,
    focando em vendas online e oportunidades sem estoque.
    """
    
    def __init__(self, config_path='config/sales_data.json', api_keys=None):
        """
        Inicializa o coletor com configurações das fontes de dados.
        
        Args:
            config_path: Caminho para o arquivo de configuração JSON
            api_keys: Chaves de API para acessar diferentes serviços
        """
        self.api_keys = api_keys or {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.sources = config['sources']
                # Mesclar api_keys do parâmetro com as do arquivo de configuração
                if 'api_keys' in config:
                    self.api_keys.update(config['api_keys'])
                self.categories = config['categories']
                self.lookback_days = config.get('lookback_days', 90)
                
            logger.info(f"Inicializado com {len(self.sources)} fontes configuradas")
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            # Configuração padrão caso o arquivo não seja encontrado
            self.sources = ["marketplace_api", "affiliate_networks", "ecommerce"]
            self.categories = [
                "Eletrônicos", "Moda e Acessórios", "Casa e Decoração", 
                "Saúde e Beleza", "Cursos Online", "Infoprodutos", 
                "Suplementos", "Esportes", "Ferramentas"
            ]
            self.lookback_days = 90
    
    def collect_data(self, period='30d'):
        """
        Coleta dados de vendas (versão simulada para testes)
        
        Args:
            period (str): Período para coleta de dados ('7d', '30d', '90d', etc)
            
        Returns:
            list: Lista de dados de vendas
        """
        print(f"Simulando coleta de dados de vendas para o período: {period}")
        
        # Converter período para número de dias
        days = int(period.replace('d', ''))
        
        # Data atual para referência
        now = datetime.now()
        
        # Dados simulados para teste
        sample_sales_data = [
            {
                'product': 'Software de Gestão',
                'category': 'Tecnologia',
                'period': period,
                'total_sales': 185000 * (days / 30),  # Escala com base no período
                'growth_rate': 0.22,
                'average_ticket': 1250.00,
                'conversion_rate': 0.058
            },
            {
                'product': 'Cursos Online',
                'category': 'Educação',
                'period': period,
                'total_sales': 320000 * (days / 30),
                'growth_rate': 0.35,
                'average_ticket': 497.00,
                'conversion_rate': 0.082
            },
            {
                'product': 'Suplementos Alimentares',
                'category': 'Saúde',
                'period': period,
                'total_sales': 420000 * (days / 30),
                'growth_rate': 0.18,
                'average_ticket': 120.00,
                'conversion_rate': 0.045
            },
            {
                'product': 'Roupas Fitness',
                'category': 'Moda',
                'period': period,
                'total_sales': 290000 * (days / 30),
                'growth_rate': 0.25,
                'average_ticket': 180.00,
                'conversion_rate': 0.062
            },
            {
                'product': 'Itens para Pets',
                'category': 'Pet',
                'period': period,
                'total_sales': 370000 * (days / 30),
                'growth_rate': 0.28,
                'average_ticket': 85.00,
                'conversion_rate': 0.073
            }
        ]
        
        return sample_sales_data
    
    def collect_sales_data(self, categories=None, days=None):
        """
        Coleta dados de vendas de todas as fontes configuradas.
        
        Args:
            categories: Lista de categorias para filtrar ou None para todas
            days: Número de dias para análise ou None para usar configuração
            
        Returns:
            pandas.DataFrame: DataFrame com os dados coletados
        """
        all_sales_data = []
        
        # Usar parâmetros ou valores padrão
        target_categories = categories if categories else self.categories
        lookback_days = days if days else self.lookback_days
        
        for source in self.sources:
            try:
                source_method = getattr(self, f"_collect_from_{source}", None)
                
                if not source_method:
                    logger.warning(f"Método para coletar dados de {source} não implementado")
                    continue
                
                logger.info(f"Coletando dados de vendas de {source}")
                sales_data = source_method(target_categories, lookback_days)
                
                if sales_data:
                    logger.info(f"Coletados {len(sales_data)} registros de vendas de {source}")
                    all_sales_data.extend(sales_data)
                else:
                    logger.warning(f"Nenhum dado de vendas encontrado em {source}")
                
                # Pausa entre requisições
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Erro ao coletar dados de {source}: {e}")
        
        # Converter para DataFrame
        df = pd.DataFrame(all_sales_data)
        
        if not df.empty:
            # Adicionar timestamp da coleta
            df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Filtrar dados relevantes para franquias sem estoque
            filtered_df = self._filter_relevant_data(df)
            
            logger.info(f"Total de dados de vendas relevantes: {len(filtered_df)}")
            return filtered_df
        else:
            logger.warning("Nenhum dado de vendas encontrado")
            return pd.DataFrame()
    
    # Restante do código permanece inalterado...
    # (todos os outros métodos existentes)
