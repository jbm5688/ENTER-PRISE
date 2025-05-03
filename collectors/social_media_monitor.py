import requests
import json
import pandas as pd
import logging
import time
from datetime import datetime, timedelta
import os
import re
# collectors/social_media_monitor.py
import random
import logging
from datetime import datetime, timedelta

# Configuração de logging
logger = logging.getLogger('social_media_monitor')

class SocialMediaMonitor:
    """
    Classe responsável por monitorar tendências em redes sociais
    """
    
    def __init__(self, api_keys=None):
        """
        Inicializa o monitor de redes sociais
        
        Args:
            api_keys (dict): Chaves de API para acessar diferentes serviços
        """
        self.api_keys = api_keys or {}
        
    def collect_trends(self, keywords=None):
        """
        Coleta tendências de redes sociais (versão simulada para testes)
        
        Args:
            keywords (list): Palavras-chave para filtrar tendências
            
        Returns:
            list: Lista de tendências
        """
        print(f"Simulando coleta de tendências de redes sociais para keywords: {keywords if keywords else 'todas'}")
        
        # Data atual para referência
        now = datetime.now()
        
        # Dados simulados para teste
        sample_trends = [
            {
                'keyword': 'home office',
                'platforms': ['Instagram', 'LinkedIn', 'Twitter'],
                'monthly_mentions': 185000,
                'sentiment': 0.72,  # Positivo
                'growth_rate': 0.25,
                'first_observed': (now - timedelta(days=90)).strftime('%Y-%m-%d')
            },
            {
                'keyword': 'alimentação saudável',
                'platforms': ['Instagram', 'TikTok', 'Facebook'],
                'monthly_mentions': 230000,
                'sentiment': 0.85,  # Muito positivo
                'growth_rate': 0.18,
                'first_observed': (now - timedelta(days=120)).strftime('%Y-%m-%d')
            },
            {
                'keyword': 'sustentabilidade',
                'platforms': ['Instagram', 'LinkedIn', 'Twitter', 'Facebook'],
                'monthly_mentions': 310000,
                'sentiment': 0.78,  # Positivo
                'growth_rate': 0.32,
                'first_observed': (now - timedelta(days=150)).strftime('%Y-%m-%d')
            },
            {
                'keyword': 'economia circular',
                'platforms': ['LinkedIn', 'Twitter', 'Facebook'],
                'monthly_mentions': 95000,
                'sentiment': 0.67,  # Moderadamente positivo
                'growth_rate': 0.41,
                'first_observed': (now - timedelta(days=60)).strftime('%Y-%m-%d')
            },
            {
                'keyword': 'inteligência artificial',
                'platforms': ['Twitter', 'LinkedIn', 'YouTube', 'Reddit'],
                'monthly_mentions': 420000,
                'sentiment': 0.62,  # Moderadamente positivo
                'growth_rate': 0.55,
                'first_observed': (now - timedelta(days=200)).strftime('%Y-%m-%d')
            }
        ]
        
        # Filtra por palavras-chave se fornecidas
        if keywords:
            filtered_trends = []
            for trend in sample_trends:
                for keyword in keywords:
                    if keyword.lower() in trend['keyword'].lower():
                        filtered_trends.append(trend)
                        break
            return filtered_trends
        
        return sample_trends
    
    def analyze_sentiment(self, text):
        """
        Analisa o sentimento de um texto (simulação simplificada)
        
        Args:
            text (str): Texto para análise
            
        Returns:
            float: Pontuação de sentimento entre -1 (negativo) e 1 (positivo)
        """
        # Palavras positivas e negativas para simulação
        positive_words = ['bom', 'ótimo', 'excelente', 'incrível', 'maravilhoso', 'feliz', 'satisfeito']
        negative_words = ['ruim', 'péssimo', 'terrível', 'horrível', 'triste', 'insatisfeito', 'decepcionado']
        
        # Contagem simples de palavras
        text = text.lower()
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        # Calcular pontuação
        total = positive_count + negative_count
        if total == 0:
            return 0
        
        return (positive_count - negative_count) / total
    
    def export_to_csv(self, trends, filename='social_media_trends.csv'):
        """
        Exporta tendências para um arquivo CSV
        
        Args:
            trends (list): Lista de tendências
            filename (str): Nome do arquivo
        """
        if not trends:
            logger.warning("Nenhuma tendência para exportar.")
            return False
        
        try:
            # Converte para DataFrame e exporta
            df = pd.DataFrame(trends)
            
            # Converte a lista de plataformas para string
            df['platforms'] = df['platforms'].apply(lambda x: ', '.join(x))
            
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Tendências exportadas para {filename}")
            return True
        except Exception as e:
            logger.error(f"Erro ao exportar tendências: {e}")
            return False
    
    def get_platform_distribution(self, trends):
        """
        Calcula a distribuição das tendências por plataforma
        
        Args:
            trends (list): Lista de tendências
            
        Returns:
            dict: Dicionário com contagem por plataforma
        """
        platform_counts = {}
        
        for trend in trends:
            for platform in trend['platforms']:
                if platform in platform_counts:
                    platform_counts[platform] += 1
                else:
                    platform_counts[platform] = 1
        
        return platform_counts
    
    def generate_report(self, trends, output_format='json'):
        """
        Gera um relatório de tendências
        
        Args:
            trends (list): Lista de tendências
            output_format (str): Formato de saída ('json' ou 'texto')
            
        Returns:
            str: Relatório formatado
        """
        if not trends:
            return "Nenhuma tendência encontrada para gerar relatório."
        
        # Cálculos para o relatório
        total_mentions = sum(trend['monthly_mentions'] for trend in trends)
        avg_sentiment = sum(trend['sentiment'] for trend in trends) / len(trends)
        avg_growth = sum(trend['growth_rate'] for trend in trends) / len(trends)
        platform_distribution = self.get_platform_distribution(trends)
        
        # Determina as tendências de maior crescimento
        sorted_by_growth = sorted(trends, key=lambda x: x['growth_rate'], reverse=True)
        top_growing = sorted_by_growth[:3] if len(sorted_by_growth) >= 3 else sorted_by_growth
        
        if output_format == 'json':
            report = {
                'data_geração': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_tendências': len(trends),
                'menções_totais': total_mentions,
                'sentimento_médio': round(avg_sentiment, 2),
                'crescimento_médio': round(avg_growth, 2),
                'distribuição_plataformas': platform_distribution,
                'tendências_maior_crescimento': [
                    {'keyword': trend['keyword'], 'growth_rate': trend['growth_rate']} 
                    for trend in top_growing
                ]
            }
            return json.dumps(report, indent=4, ensure_ascii=False)
        else:
            # Relatório em formato texto
            report_lines = [
                "=== RELATÓRIO DE TENDÊNCIAS EM REDES SOCIAIS ===",
                f"Data de geração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Total de tendências analisadas: {len(trends)}",
                f"Total de menções mensais: {total_mentions:,}".replace(',', '.'),
                f"Sentimento médio: {avg_sentiment:.2f} (0=negativo, 1=positivo)",
                f"Taxa média de crescimento: {avg_growth:.2f}",
                "\nDistribuição por plataforma:",
            ]
            
            for platform, count in platform_distribution.items():
                report_lines.append(f"  - {platform}: {count} tendências")
            
            report_lines.append("\nTendências com maior crescimento:")
            for i, trend in enumerate(top_growing, 1):
                report_lines.append(f"  {i}. {trend['keyword']} (crescimento: {trend['growth_rate']:.2f})")
            
            return "\n".join(report_lines)

# Função para teste
def test_social_media_monitor():
    monitor = SocialMediaMonitor()
    trends = monitor.collect_trends()
    print(f"Coletadas {len(trends)} tendências")
    
    # Teste de exportação
    monitor.export_to_csv(trends, 'test_trends.csv')
    
    # Teste de relatório
    print("\nRelatório em JSON:")
    print(monitor.generate_report(trends, 'json'))
    
    print("\nRelatório em texto:")
    print(monitor.generate_report(trends, 'texto'))

if __name__ == "__main__":
    test_social_media_monitor()
