import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
import logging
from datetime import datetime
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/marketplace_scraper.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("marketplace_scraper")

class MarketplaceScraper:
    """
    Classe para coletar dados de produtos em marketplaces como
    Amazon, Mercado Livre e Shopee, focando em produtos que podem
    ser revendidos em modelo de franquia sem estoque.
    """
    
    def __init__(self, config_path='config/marketplace_sources.json'):
        """
        Inicializa o scraper com configurações dos marketplaces.
        
        Args:
            config_path: Caminho para o arquivo de configuração JSON
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.marketplaces = config['marketplaces']
                self.headers = config['headers']
                self.search_terms = config['search_terms']
                self.proxy = config.get('proxy', None)
                self.delay_range = config.get('delay_range', [1, 3])
                
            logger.info(f"Inicializado com {len(self.marketplaces)} marketplaces configurados")
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            # Configuração padrão caso o arquivo não seja encontrado
            self.marketplaces = [
                {
                    "name": "Amazon",
                    "base_url": "https://www.amazon.com.br/s",
                    "params": {"k": "{search_term}"},
                    "selectors": {
                        "item_container": "div[data-component-type='s-search-result']",
                        "title": "h2 a span",
                        "price": "span.a-price-whole",
                        "rating": "span.a-icon-alt",
                        "reviews_count": "span.a-size-base.s-underline-text",
                        "url": "h2 a",
                        "seller": "div.a-row.a-size-base.a-color-secondary span.a-size-base"
                    }
                },
                {
                    "name": "Mercado Livre",
                    "base_url": "https://lista.mercadolivre.com.br/{search_term}",
                    "params": {},
                    "selectors": {
                        "item_container": "div.ui-search-result",
                        "title": "h2.ui-search-item__title",
                        "price": "span.price-tag-amount",
                        "url": "a.ui-search-link",
                        "seller": "span.ui-search-item__brand-title"
                    }
                }
            ]
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            self.search_terms = ["dropshipping", "revenda sem estoque", "franquia digital"]
            self.proxy = None
            self.delay_range = [1, 3]
    
    def scrape_products(self, max_products_per_marketplace=20):
        """
        Coleta dados de produtos de todos os marketplaces configurados.
        
        Args:
            max_products_per_marketplace: Número máximo de produtos por marketplace
            
        Returns:
            pandas.DataFrame: DataFrame com os dados coletados
        """
        all_products = []
        
        for marketplace in self.marketplaces:
            marketplace_name = marketplace['name']
            logger.info(f"Iniciando coleta de {marketplace_name}")
            
            for search_term in self.search_terms:
                try:
                    logger.info(f"Buscando por '{search_term}' em {marketplace_name}")
                    
                    # Montar URL
                    url = self._build_search_url(marketplace, search_term)
                    
                    # Fazer requisição
                    response = self._make_request(url)
                    if not response:
                        continue
                    
                    # Processar resultados
                    soup = BeautifulSoup(response.content, 'html.parser')
                    products = self._extract_products(soup, marketplace, search_term)
                    
                    logger.info(f"Encontrados {len(products)} produtos para '{search_term}' em {marketplace_name}")
                    all_products.extend(products)
                    
                    # Limitar número de produtos por marketplace
                    if len(all_products) >= max_products_per_marketplace:
                        break
                    
                    # Pausa para evitar bloqueios
                    self._random_delay()
                    
                except Exception as e:
                    logger.error(f"Erro ao buscar '{search_term}' em {marketplace_name}: {e}")
        
        # Converter para DataFrame
        df = pd.DataFrame(all_products)
        
        if not df.empty:
            # Adicionar timestamp da coleta
            df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Remover duplicatas com base na URL
            df = df.drop_duplicates(subset=['url'])
            
            # Filtrar produtos que parecem ser dropshipping ou adequados para revenda
            df = self._filter_resellable_products(df)
            
            logger.info(f"Total de produtos coletados após filtros: {len(df)}")
            return df
        else:
            logger.warning("Nenhum produto encontrado")
            return pd.DataFrame()
    
    def _build_search_url(self, marketplace, search_term):
        """
        Constrói a URL de busca para um marketplace específico.
        
        Args:
            marketplace: Configuração do marketplace
            search_term: Termo de busca
            
        Returns:
            str: URL formatada para busca
        """
        base_url = marketplace['base_url']
        params = marketplace.get('params', {})
        
        # Substituir placeholder no base_url
        if '{search_term}' in base_url:
            url = base_url.format(search_term=search_term.replace(' ', '+'))
        else:
            url = base_url
            
        # Adicionar parâmetros
        if params:
            # Substituir placeholders nos parâmetros
            for key, value in params.items():
                if isinstance(value, str) and '{search_term}' in value:
                    params[key] = value.format(search_term=search_term)
            
            # Construir query string
            query_params = '&'.join([f"{k}={v}" for k, v in params.items()])
            url = f"{url}?{query_params}" if '?' not in url else f"{url}&{query_params}"
        
        return url
    
    def _make_request(self, url):
        """
        Realiza a requisição HTTP com tratamento de erros e retentativas.
        
        Args:
            url: URL para fazer a requisição
            
        Returns:
            Response object ou None em caso de falha
        """
        max_retries = 3
        proxies = {'http': self.proxy, 'https': self.proxy} if self.proxy else None
        
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    proxies=proxies,
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 403 or response.status_code == 429:
                    logger.warning(f"Possível bloqueio (status {response.status_code}). Aguardando...")
                    time.sleep(10 + attempt * 5)  # Aumentar espera progressivamente
                else:
                    logger.warning(f"Requisição falhou com status {response.status_code} para {url}")
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"Tentativa {attempt+1}/{max_retries} falhou: {e}")
                time.sleep(2)
                
        logger.error(f"Todas as tentativas falharam para {url}")
        return None
    
    def _extract_products(self, soup, marketplace, search_term):
        """
        Extrai informações de produtos usando seletores específicos.
        
        Args:
            soup: Objeto BeautifulSoup com o HTML da página
            marketplace: Configuração do marketplace
            search_term: Termo de busca usado
            
        Returns:
            list: Lista de dicionários com informações de produtos
        """
        products = []
        marketplace_name = marketplace['name']
        selectors = marketplace['selectors']
        
        try:
            # Encontrar contêineres de itens
            items = soup.select(selectors['item_container'])
            logger.info(f"Encontrados {len(items)} itens em {marketplace_name}")
            
            for item in items:
                try:
                    # Extrair dados básicos
                    title = self._get_text(item, selectors['title'])
                    url = self._get_full_url(
                        self._get_attribute(item, selectors['url'], 'href'), 
                        marketplace['base_url']
                    )
                    
                    # Pular item se não tiver título ou URL
                    if not title or not url:
                        continue
                    
                    # Criar produto base
                    product = {
                        'title': title,
                        'url': url,
                        'marketplace': marketplace_name,
                        'search_term': search_term,
                        'price': self._extract_price(item, selectors.get('price', '')),
                        'seller': self._get_text(item, selectors.get('seller', '')),
                        'rating': self._extract_rating(item, selectors.get('rating', '')),
                        'reviews_count': self._extract_reviews_count(item, selectors.get('reviews_count', '')),
                        'is_dropshipping': self._is_dropshipping_candidate(title)
                    }
                    
                    products.append(product)
                    
                except Exception as e:
                    logger.warning(f"Erro ao extrair produto: {e}")
            
        except Exception as e:
            logger.error(f"Erro ao processar produtos em {marketplace_name}: {e}")
        
        return products
    
    def _get_text(self, item, selector):
        """
        Extrai texto de um elemento.
        
        Args:
            item: Elemento HTML do produto
            selector: Seletor CSS para encontrar o texto
            
        Returns:
            str: Texto extraído ou string vazia
        """
        if not selector:
            return ""
            
        try:
            element = item.select_one(selector)
            return element.get_text().strip() if element else ""
        except Exception:
            return ""
    
    def _get_attribute(self, item, selector, attribute):
        """
        Extrai atributo de um elemento.
        
        Args:
            item: Elemento HTML do produto
            selector: Seletor CSS para encontrar o elemento
            attribute: Nome do atributo a extrair
            
        Returns:
            str: Valor do atributo ou string vazia
        """
        if not selector:
            return ""
            
        try:
            element = item.select_one(selector)
            return element.get(attribute, "") if element else ""
        except Exception:
            return ""
    
    def _get_full_url(self, relative_url, base_url):
        """
        Converte URL relativa em absoluta.
        
        Args:
            relative_url: URL relativa extraída
            base_url: URL base do site
            
        Returns:
            str: URL absoluta
        """
        if not relative_url:
            return ""
            
        if relative_url.startswith('http'):
            return relative_url
        
        # Extrair protocolo e domínio da base_url
        import re
        domain_match = re.match(r'(https?://[^/]+)', base_url)
        domain = domain_match.group(1) if domain_match else base_url
        
        # Se começa com /, juntar com o domínio
        if relative_url.startswith('/'):
            return domain + relative_url
        
        # Caso contrário, juntar com o path base
        return domain.rstrip('/') + '/' + relative_url.lstrip('/')
    
    def _extract_price(self, item, selector):
        """
        Extrai e normaliza informação de preço.
        
        Args:
            item: Elemento HTML do produto
            selector: Seletor CSS para o preço
            
        Returns:
            float: Valor do preço ou None
        """
        price_text = self._get_text(item, selector)
        if not price_text:
            return None
            
        try:
            # Remover símbolos de moeda e normalizar
            import re
            price_digits = re.sub(r'[^\d,.]', '', price_text)
            
            # Converter para formato numérico (considerando separador decimal)
            if ',' in price_digits and '.' not in price_digits:
                # Formato brasileiro: 1.234,56
                price_digits = price_digits.replace('.', '').replace(',', '.')
            elif ',' in price_digits and '.' in price_digits:
                # Formato com separador de milhar e decimal: 1,234.56
                price_digits = price_digits.replace(',', '')
            
            return float(price_digits)
        except Exception:
            return None
    
    def _extract_rating(self, item, selector):
        """
        Extrai e normaliza informação de avaliação.
        
        Args:
            item: Elemento HTML do produto
            selector: Seletor CSS para avaliação
            
        Returns:
            float: Valor da avaliação ou None
        """
        rating_text = self._get_text(item, selector)
        if not rating_text:
            return None
            
        try:
            import re
            # Procurar por um número decimal (ex: 4.5 de 5)
            match = re.search(r'(\d+[.,]\d+|\d+)', rating_text)
            if match:
                rating = match.group(1).replace(',', '.')
                return float(rating)
        except Exception:
            pass
            
        return None
    
    def _extract_reviews_count(self, item, selector):
        """
        Extrai e normaliza contagem de avaliações.
        
        Args:
            item: Elemento HTML do produto
            selector: Seletor CSS para contagem de avaliações
            
        Returns:
            int: Número de avaliações ou None
        """
        count_text = self._get_text(item, selector)
        if not count_text:
            return None
            
        try:
            import re
            # Extrair apenas dígitos
            digits = re.sub(r'[^\d]', '', count_text)
            return int(digits) if digits else None
        except Exception:
            return None
    
    def _is_dropshipping_candidate(self, title):
        """
        Verifica se o produto parece ser adequado para dropshipping/revenda.
        
        Args:
            title: Título do produto
            
        Returns:
            bool: True se parecer um candidato a dropshipping
        """
        title_lower = title.lower()
        
        # Palavras-chave relacionadas a dropshipping/revenda
        dropshipping_keywords = [
            'dropshipping', 'revenda', 'franquia', 'digital', 'curso', 'ebook',
            'online
