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
    
    def __init__(self, config_path='config/sales_data.json'):
        """
        Inicializa o coletor com configurações das fontes de dados.
        
        Args:
            config_path: Caminho para o arquivo de configuração JSON
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.sources = config['sources']
                self.api_keys = config['api_keys']
                self.categories = config['categories']
                self.lookback_days = config.get('lookback_days', 90)
                
            logger.info(f"Inicializado com {len(self.sources)} fontes configuradas")
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            # Configuração padrão caso o arquivo não seja encontrado
            self.sources = ["marketplace_api", "affiliate_networks", "ecommerce"]
            self.api_keys = {}
            self.categories = [
                "Eletrônicos", "Moda e Acessórios", "Casa e Decoração", 
                "Saúde e Beleza", "Cursos Online", "Infoprodutos", 
                "Suplementos", "Esportes", "Ferramentas"
            ]
            self.lookback_days = 90
    
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
    
    def _collect_from_marketplace_api(self, categories, lookback_days):
        """
        Coleta dados de vendas de APIs de marketplaces.
        
        Args:
            categories: Lista de categorias para filtrar
            lookback_days: Número de dias para análise
            
        Returns:
            list: Lista de dados de vendas de marketplace
        """
        # Verificar se temos API key para marketplace
        if 'marketplace' not in self.api_keys or not self.api_keys['marketplace']:
            logger.info("API key para marketplace não configurada, usando dados simulados")
            return self._simulate_marketplace_data(categories, lookback_days)
        
        try:
            # Implementação da coleta real de dados via API
            # (Esta seria substituída pela implementação real com as APIs)
            
            # Como muitas APIs são proprietárias ou restritas, usaremos simulação
            return self._simulate_marketplace_data(categories, lookback_days)
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados de marketplace: {e}")
            return self._simulate_marketplace_data(categories, lookback_days)
    
    def _collect_from_affiliate_networks(self, categories, lookback_days):
        """
        Coleta dados de vendas de redes de afiliados.
        
        Args:
            categories: Lista de categorias para filtrar
            lookback_days: Número de dias para análise
            
        Returns:
            list: Lista de dados de vendas de afiliados
        """
        # Verificar se temos API keys para redes de afiliados
        has_apis = False
        for key in self.api_keys:
            if 'affiliate' in key:
                has_apis = True
                break
                
        if not has_apis:
            logger.info("API keys para redes de afiliados não configuradas, usando dados simulados")
            return self._simulate_affiliate_data(categories, lookback_days)
        
        try:
            # Implementação da coleta real de dados via API
            # (Esta seria substituída pela implementação real com as APIs)
            
            # Como muitas APIs são proprietárias ou restritas, usaremos simulação
            return self._simulate_affiliate_data(categories, lookback_days)
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados de redes de afiliados: {e}")
            return self._simulate_affiliate_data(categories, lookback_days)
    
    def _collect_from_ecommerce(self, categories, lookback_days):
        """
        Coleta dados de vendas de plataformas de e-commerce.
        
        Args:
            categories: Lista de categorias para filtrar
            lookback_days: Número de dias para análise
            
        Returns:
            list: Lista de dados de vendas de e-commerce
        """
        # Verificar se temos API keys para e-commerce
        has_apis = False
        for key in self.api_keys:
            if 'ecommerce' in key or 'shop' in key:
                has_apis = True
                break
                
        if not has_apis:
            logger.info("API keys para e-commerce não configuradas, usando dados simulados")
            return self._simulate_ecommerce_data(categories, lookback_days)
        
        try:
            # Implementação da coleta real de dados via API
            # (Esta seria substituída pela implementação real com as APIs)
            
            # Como muitas APIs são proprietárias ou restritas, usaremos simulação
            return self._simulate_ecommerce_data(categories, lookback_days)
            
        except Exception as e:
            logger.error(f"Erro ao coletar dados de e-commerce: {e}")
            return self._simulate_ecommerce_data(categories, lookback_days)
    
    def _simulate_marketplace_data(self, categories, lookback_days):
        """
        Gera dados simulados de vendas de marketplace para desenvolvimento.
        
        Args:
            categories: Lista de categorias para filtrar
            lookback_days: Número de dias para análise
            
        Returns:
            list: Lista de dados de vendas simulados
        """
        sales_data = []
        
        # Data base para simulação
        base_date = datetime.now()
        
        # Marketplaces simulados
        marketplaces = ["Amazon", "Mercado Livre", "Shopee", "AliExpress", "Magazine Luiza"]
        
        # Produtos por categoria (simulados)
        products_by_category = {
            "Eletrônicos": [
                "Fone de Ouvido Bluetooth", "Smartwatch", "Carregador Portátil", 
                "Caixa de Som Bluetooth", "Suporte para Celular", "Cabo USB Magnético"
            ],
            "Moda e Acessórios": [
                "Relógio Minimalista", "Óculos de Sol", "Pulseira Magnética",
                "Carteira Slim", "Boné Unissex", "Colar Personalizado"
            ],
            "Casa e Decoração": [
                "Organizador Multiuso", "Luminária LED", "Difusor de Aromas",
                "Almofada Decorativa", "Kit Banheiro", "Quadro Decorativo"
            ],
            "Saúde e Beleza": [
                "Escova Secadora", "Massageador Facial", "Kit Skincare",
                "Removedor de Cravos", "Escovas de Maquiagem", "Hidratante Corporal"
            ],
            "Cursos Online": [
                "Curso de Marketing Digital", "Curso de Vendas Online", "Curso de Dropshipping",
                "Curso de Design Gráfico", "Curso de Desenvolvimento Web", "Curso de Idiomas"
            ],
            "Infoprodutos": [
                "Ebook Empreendedorismo", "Guia de Vendas Online", "Planilhas de Gestão",
                "Mentoria Digital", "Templates de Redes Sociais", "Kit PLR"
            ],
            "Suplementos": [
                "Colágeno em Pó", "Whey Protein", "Vitamina C", 
                "Ômega 3", "Multivitamínico", "Termogênico"
            ],
            "Esportes": [
                "Corda de Pular", "Faixa Elástica", "Luvas de Treino",
                "Garrafa Squeeze", "Mochila Esportiva", "Tapete de Yoga"
            ],
            "Ferramentas": [
                "Kit Ferramentas", "Furadeira Portátil", "Lanterna Tática",
                "Chave de Fenda Magnética", "Alicate Multifuncional", "Fita Métrica"
            ]
        }
        
        for category in categories:
            if category not in products_by_category:
                continue
                
            products = products_by_category[category]
            
            for product in products:
                # Gerar dados para cada marketplace
                for marketplace in marketplaces:
                    # Defina uma semente para garantir consistência entre execuções
                    seed = hash(f"{category}_{product}_{marketplace}")
                    random.seed(seed)
                    
                    # Gerar preço base consistente por produto
                    if "Curso" in product or "Ebook" in product or "Mentoria" in product:
                        base_price = random.uniform(97, 997)
                    elif category in ["Eletrônicos", "Ferramentas"]:
                        base_price = random.uniform(50, 300)
                    elif category in ["Suplementos", "Saúde e Beleza"]:
                        base_price = random.uniform(30, 150)
                    else:
                        base_price = random.uniform(20, 200)
                    
                    # Gerar taxa de comissão consistente por categoria e marketplace
                    if category in ["Cursos Online", "Infoprodutos"]:
                        commission_rate = random.uniform(30, 70)  # Comissões altas para produtos digitais
                    elif category in ["Eletrônicos", "Ferramentas"]:
                        commission_rate = random.uniform(5, 15)  # Comissões baixas para eletrônicos
                    else:
                        commission_rate = random.uniform(10, 30)  # Comissões médias para outros produtos
                    
                    # Ajustar comissão base no marketplace
                    if marketplace == "Amazon":
                        commission_rate *= 0.8  # Amazon tende a ter comissões menores
                    elif marketplace in ["Shopee", "AliExpress"]:
                        commission_rate *= 1.2  # Plataformas asiáticas podem ter comissões maiores
                    
                    # Gerar dados diários para o período especificado
                    for day in range(lookback_days):
                        # Restaurar a semente para o dia específico
                        day_seed = seed + day
                        random.seed(day_seed)
                        
                        # Data do registro
                        record_date = (base_date - timedelta(days=day)).strftime('%Y-%m-%d')
                        
                        # Gerar variação diária nos preços (pequena)
                        daily_price = base_price * random.uniform(0.95, 1.05)
                        
                        # Gerar variação diária nas vendas
                        # Produtos digitais tendem a ter mais vendas
                        if "Curso" in product or "Ebook" in product or "Mentoria" in product:
                            base_sales = random.randint(5, 50)
                        else:
                            base_sales = random.randint(1, 20)
                        
                        # Ajustar vendas com base no marketplace
                        if marketplace in ["Amazon", "Mercado Livre"]:
                            base_sales = int(base_sales * 1.5)  # Mais vendas em marketplaces populares
                        
                        # Adicionar sazonalidade semanal
                        day_of_week = (base_date - timedelta(days=day)).weekday()
                        if day_of_week >= 5:  # Fim de semana
                            base_sales = int(base_sales * 1.3)  # Mais vendas no fim de semana
                        
                        # Calcular receita e comissão
                        revenue = daily_price * base_sales
                        commission = revenue * (commission_rate / 100)
                        
                        # Adicionar registro
                        sales_data.append({
                            'date': record_date,
                            'product': product,
                            'category': category,
                            'marketplace': marketplace,
                            'price': round(daily_price, 2),
                            'sales_count': base_sales,
                            'revenue': round(revenue, 2),
                            'commission_rate': round(commission_rate, 2),
                            'commission_amount': round(commission, 2),
                            'has_stock_requirement': False,  # Produtos para dropshipping
                            'product_type': 'digital' if "Curso" in product or "Ebook" in product or "Mentoria" in product else 'physical',
                            'source': f"{marketplace} API (simulado)"
                        })
        
        return sales_data
    
    def _simulate_affiliate_data(self, categories, lookback_days):
        """
        Gera dados simulados de vendas de programas de afiliados para desenvolvimento.
        
        Args:
            categories: Lista de categorias para filtrar
            lookback_days: Número de dias para análise
            
        Returns:
            list: Lista de dados de vendas simulados
        """
        sales_data = []
        
        # Data base para simulação
        base_date = datetime.now()
        
        # Redes de afiliados simuladas
        networks = ["Hotmart", "Monetizze", "Eduzz", "ClickBank", "Braip"]
        
        # Produtos por categoria (simulados - focado em infoprodutos)
        products_by_category = {
            "Cursos Online": [
                "Curso Completo de Dropshipping", "Formação em Marketing Digital", 
                "Academia de Vendas Online", "Especialista em E-commerce", 
                "Mentoria Tráfego Pago", "Curso de Importação"
            ],
            "Infoprodutos": [
                "Método Revenda Lucrativa", "Ebook Segredos do Dropshipping", 
                "Kit PLR Nichos Lucrativos", "Fórmula Negócio Online", 
                "Guia Completo do Afiliado", "Sistema Franquia Digital"
            ],
            "Saúde e Beleza": [
                "Programa Emagrecimento Saudável", "Método Anti-idade Natural", 
                "Guia Completo de Suplementação", "Curso de Estética Avançada", 
                "Treinamento Fitness em Casa", "Ebook Alimentação Consciente"
            ],
            "Finanças": [
                "Curso Investimentos Inteligentes", "Mentoria Liberdade Financeira", 
                "Fórmula da Renda Extra", "Guia do Day Trader", 
                "Ebook Criptomoedas para Iniciantes", "Método Geração de Riqueza"
            ],
            "Desenvolvimento Pessoal": [
                "Método Produtividade Máxima", "Treinamento Oratória e Comunicação", 
                "Curso Inteligência Emocional", "Método Propósito de Vida", 
                "Mentoria Liderança Efetiva", "Programa Transformação Pessoal"
            ]
        }
        
        # Filtrar categorias relevantes para afiliados
        relevant_categories = [cat for cat in categories if cat in products_by_category]
        
        # Se não houver categorias relevantes, usar todas disponíveis
        if not relevant_categories:
            relevant_categories = list(products_by_category.keys())
        
        for category in relevant_categories:
            products = products_by_category[category]
            
            for product in products:
                # Gerar dados para cada rede de afiliados
                for network in networks:
                    # Definir semente para consistência
                    seed = hash(f"{category}_{product}_{network}")
                    random.seed(seed)
                    
                    # Gerar preço base consistente por produto e categoria
                    if category == "Cursos Online":
                        if "Mentoria" in product or "Formação" in product:
                            base_price = random.uniform(497, 1997)
                        else:
                            base_price = random.uniform(197, 997)
                    elif category == "Infoprodutos":
                        if "Sistema" in product or "Método" in product:
                            base_price = random.uniform(297, 797)
                        else:
                            base_price = random.uniform(47, 197)
                    elif category == "Finanças":
                        base_price = random.uniform(297, 1497)
                    else:
                        base_price = random.uniform(97, 497)
                    
                    # Gerar taxa de comissão consistente por categoria e rede
                    # Infoprodutos tendem a ter comissões mais altas
                    if category in ["Cursos Online", "Infoprodutos"]:
                        commission_rate = random.uniform(40, 70)  # Comissões altas para infoprodutos
                    elif category == "Finanças":
                        commission_rate = random.uniform(30, 50)  # Comissões boas para finanças
                    else:
                        commission_rate = random.uniform(20, 40)  # Comissões médias para outros
                    
                    # Ajustar comissão com base na rede
                    if network == "ClickBank":
                        commission_rate *= 1.1  # ClickBank tende a ter comissões maiores
                    elif network == "Hotmart":
                        commission_rate *= 0.9  # Hotmart pode ter comissões um pouco menores
                    
                    # Gerar dados diários para o período especificado
                    for day in range(lookback_days):
                        # Restaurar semente para o dia
                        day_seed = seed + day
                        random.seed(day_seed)
                        
                        # Data do registro
                        record_date = (base_date - timedelta(days=day)).strftime('%Y-%m-%d')
                        
                        # Gerar variação diária nas vendas
                        # Produtos mais caros tendem a vender menos
                        if base_price > 500:
                            base_sales = random.randint(0, 5)
                        elif base_price > 200:
                            base_sales = random.randint(1, 10)
                        else:
                            base_sales = random.randint(2, 20)
                        
                        # Ajustar vendas com base na rede
                        if network in ["Hotmart", "Eduzz"]:
                            base_sales = int(base_sales * 1.3)  # Mais vendas em redes brasileiras populares
                        
                        # Adicionar sazonalidade
                        day_of_week = (base_date - timedelta(days=day)).weekday()
                        if day_of_week >= 5:  # Fim de semana
                            base_sales = int(base_sales * 1.2)  # Mais vendas no fim de semana
                        
                        # Calcular receita e comissão
                        revenue = base_price * base_sales
                        commission = revenue * (commission_rate / 100)
                        
                        # Adicionar registro (apenas se houver vendas)
                        if base_sales > 0:
                            sales_data.append({
                                'date': record_date,
                                'product': product,
                                'category': category,
                                'affiliate_network': network,
                                'price': round(base_price, 2),
                                'sales_count': base_sales,
                                'revenue': round(revenue, 2),
                                'commission_rate': round(commission_rate, 2),
                                'commission_amount': round(commission, 2),
                                'has_stock_requirement': False,  # Infoprodutos não requerem estoque
                                'product_type': 'digital',  # Todos são produtos digitais
                                'source': f"{network} API (simulado)"
                            })
        
        return sales_data
    
    def _simulate_ecommerce_data(self, categories, lookback_days):
        """
        Gera dados simulados de vendas de plataformas de e-commerce para desenvolvimento.
        
        Args:
            categories: Lista de categorias para filtrar
            lookback_days: Número de dias para análise
            
        Returns:
            list: Lista de dados de vendas simulados
        """
        sales_data = []
        
        # Data base para simulação
        base_date = datetime.now()
        
        # Plataformas de e-commerce simuladas
        platforms = ["Shopify", "WooCommerce", "Magento", "Nuvemshop", "Loja Integrada"]
        
        # Produtos por categoria (simulados - foco em produtos físicos)
        products_by_category = {
            "Eletrônicos": [
                "Fone de Ouvido Bluetooth", "Smartwatch", "Carregador Portátil", 
                "Mini Câmera Espiã", "Projetor Portátil", "Drone Mini"
            ],
            "Moda e Acessórios": [
                "Relógio Minimalista", "Óculos de Sol Premium", "Pulseira Magnética",
                "Boné Estilizado", "Conjunto Unissex", "Jaqueta Corta-Vento"
            ],
            "Casa e Decoração": [
                "Luminária Led Recarregável", "Organizador Multiuso", "Difusor Elétrico",
                "Conjunto Porta-Retratos", "Kit Banheiro Premium", "Manta Decorativa"
            ],
            "Saúde e Beleza": [
                "Escova Alisadora", "Massageador Facial", "Kit Skincare Coreano",
                "Perfume Importado", "Kit Maquiagem Profissional", "Aparador de Pelos"
            ],
            "Pet Shop": [
                "Cama Pet Luxo", "Brinquedo Inteligente", "Coleira Personalizada",
                "Fonte de Água Automática", "Roupa Pet Estilizada", "Arranhador Gato"
            ]
        }
        
        # Filtrar categorias relevantes
        relevant_categories = [cat for cat in categories if cat in products_by_category]
        
        # Se não houver categorias relevantes, usar todas disponíveis
        if not relevant_categories:
            relevant_categories = list(products_by_category.keys())
        
        for category in relevant_categories:
            products = products_by_category[category]
            
            for product in products:
                # Gerar dados para cada plataforma de e-commerce
                for platform in platforms:
                    # Definir semente para consistência
                    seed = hash(f"{category}_{product}_{platform}")
                    random.seed(seed)
                    
                    # Gerar preço base consistente por produto
                    if category == "Eletrônicos":
                        base_price = random.uniform(80, 350)
                    elif category == "Saúde e Beleza" and "Kit" in product:
                        base_price = random.uniform(100, 300)
                    elif category == "Pet Shop":
                        base_price = random.uniform(50, 200)
                    else:
                        base_price = random.uniform(40, 150)
                    
                    # Gerar custos e margens
                    cost_price = base_price * random.uniform(0.3, 0.5)  # Custo entre 30-50% do preço de venda
                    profit_margin = ((base_price - cost_price) / base_price) * 100
                    
                    # Gerar dados diários para o período especificado
                    for day in range(lookback_days):
                        # Restaurar semente para o dia
                        day_seed = seed + day
                        random.seed(day_seed)
                        
                        # Data do registro
                        record_date = (base_date - timedelta(days=day)).strftime('%Y-%m-%d')
                        
                        # Gerar variação diária nos preços (pequena)
                        daily_price = base_price * random.uniform(0.95, 1.05)
                        daily_cost = cost_price * random.uniform(0.98, 1.02)
                        
                        # Gerar variação diária nas vendas
                        base_sales = random.randint(0, 8)  # Vendas tendem a ser menores em lojas individuais
                        
                        # Ajustar vendas com base na plataforma
                        if platform in ["Shopify", "WooCommerce"]:
                            base_sales = int(base_sales * 1.5)  # Mais vendas em plataformas populares
                        
                        # Adicionar sazonalidade
                        day_of_week = (base_date - timedelta(days=day)).weekday()
                        if day_of_week >= 5:  # Fim de semana
                            base_sales = int(base_sales * 1.3)  # Mais vendas no fim de semana
                        
                        # Calcular métricas
                        revenue = daily_price * base_sales
                        cost = daily_cost * base_sales
                        profit = revenue - cost
                        
                        # Adicionar registro (apenas se houver vendas)
                        if base_sales > 0:
                            sales_data.append({
                                'date': record_date,
                                'product': product,
                                'category': category,
                                'platform': platform,
                                'price': round(daily_price, 2),
                                'cost': round(daily_cost, 2),
                                'sales_count': base_sales,
                                'revenue': round(revenue, 2),
                                'profit': round(profit, 2),
                                'profit_margin': round(profit_margin, 2),
                                'has_stock_requirement': True,  # E-commerce tradicional requer estoque
                                'product_type': 'physical',  # Produtos físicos
                                'source': f"{platform} API (simulado)"
                            })
        
        return sales_data
    
    def _filter_relevant_data(self, df):
        """
        Filtra dados relevantes para franquias sem estoque.
        
        Args:
            df: DataFrame com todos os dados
            
        Returns:
            DataFrame: Dados filtrados
        """
        if df.empty:
            return df
            
        # Criar função para verificar relevância
        def is_relevant(row):
            # Priorizar produtos sem requisito de estoque
            if 'has_stock_requirement' in row and row['has_stock_requirement'] == False:
                return True
                
            # Priorizar produtos digitais
            if 'product_type' in row and row['product_type'] == 'digital':
                return True
                
            # Verificar categorias relevantes para dropshipping
            relevant_categories = ["Eletrônicos", "Moda e Acessórios", "Casa e Decoração", 
                                  "Saúde e Beleza", "Cursos Online", "Infoprodutos"]
            
            if 'category' in row and row['category'] in relevant_categories:
                return True
                
            return False
        
        # Aplicar filtro
        filtered_df = df[df.apply(is_relevant, axis=1)].copy()
        
        return filtered_df
    
    def get_top_performers(self, df, metric='commission_amount', n=10):
        """
        Identifica os produtos com melhor desempenho.
        
        Args:
            df: DataFrame com dados de vendas
            metric: Métrica para ordenação ('commission_amount', 'revenue', 'profit_margin')
            n: Número de produtos para retornar
            
        Returns:
            pandas.DataFrame: Top produtos por desempenho
        """
        if df.empty or metric not in df.columns:
            return pd.DataFrame()
            
        # Agrupar por produto e calcular métricas
        product_performance = df.groupby(['product', 'category']).agg({
            'sales_count': 'sum',
            'revenue': 'sum',
            metric: 'sum'
        }).reset_index()
        
        # Calcular média diária
        days = len(df['date'].unique())
        if days > 0:
            product_performance['avg_daily_sales'] = product_performance['sales_count'] / days
            product_performance['avg_daily_revenue'] = product_performance['revenue'] / days
            product_performance[f'avg_daily_{metric}'] = product_performance[metric] / days
        
        # Ordenar por métrica selecionada
        top_products = product_performance.sort_values(metric, ascending=False).head(n)
        
        return top_products
    
    def get_category_performance(self, df):
        """
        Analisa o desempenho por categoria.
        
        Args:
            df: DataFrame com dados de vendas
            
        Returns:
            pandas.DataFrame: Desempenho por categoria
        """
        if df.empty or 'category' not in df.columns:
            return pd.DataFrame()
            
        # Agrupar por categoria e calcular métricas
        category_performance = df.groupby('category').agg({
            'sales_count': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        # Calcular comissão média se disponível
        if 'commission_amount' in df.columns:
            commission_by_category = df.groupby('category')['commission_amount'].sum()
            category_performance = category_performance.merge(
                commission_by_category.reset_index(),
                on='category',
                how='left'
            )
        
        # Calcular lucro médio se disponível
        if 'profit' in df.columns:
            profit_by_category = df.groupby('category')['profit'].sum()
            category_performance = category_performance.merge(
                profit_by_category.reset_index(),
                on='category',
                how='left'
            )
        
        # Calcular média diária
        days = len(df['date'].unique())
        if days > 0:
            category_performance['avg_daily_sales'] = category_performance['sales_count'] / days
            category_performance['avg_daily_revenue'] = category_performance['revenue'] / days
        
        # Ordenar por receita
        category_performance = category_performance.sort_values('revenue', ascending=False)
        
        return category_performance
    
    def save_to_csv(self, df, filename='output/data/sales_data.csv'):
        """
        Salva os dados em um arquivo CSV.
        
        Args:
            df: DataFrame com os dados
            filename: Caminho do arquivo para salvar
        """
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Dados salvos em {filename}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar dados: {e}")
            return False


# Execução standalone para testes
if __name__ == "__main__":
    import os
    
    # Criar diretório de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    collector = SalesDataCollector()
    
    # Coletar dados de vendas
    sales_data = collector.collect_sales_data(days=30)  # Últimos 30 dias
    
    if not sales_data.empty:
        print(f"Coletados {len(sales_data)} registros de vendas.")
        
        # Salvar resultados
        os.makedirs('output/data', exist_ok=True)
        collector.save_to_csv(sales_data)
        
        # Analisar top produtos
        top_products = collector.get_top_performers(sales_data, metric='commission_amount', n=5)
        print("\nTop 5 produtos por comissão:")
        print(top_products[['product', 'category', 'sales_count', 'revenue', 'commission_amount']])
        
        # Analisar categorias
        category_performance = collector.get_category_performance(sales_data)
        print("\nDesempenho por categoria:")
        print(category_performance[['category', 'sales_count', 'revenue']])
    else:
        print("Nenhum dado de vendas encontrado ou erro na coleta.")
