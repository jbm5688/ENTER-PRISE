import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
import logging
from datetime import datetime
import os
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/affiliate_finder.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("affiliate_finder")

class AffiliateFinder:
    """
    Classe para identificar programas de afiliados para produtos específicos,
    permitindo revenda sem estoque através de comissão.
    """
    
    def __init__(self, config_path='config/affiliate_platforms.json'):
        """
        Inicializa o finder com configurações das plataformas de afiliados.
        
        Args:
            config_path: Caminho para o arquivo de configuração JSON
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.platforms = config['platforms']
                self.headers = config['headers']
                self.keywords = config['keywords']
                self.categories = config['categories']
                self.proxy = config.get('proxy', None)
                self.delay_range = config.get('delay_range', [1, 3])
                
            logger.info(f"Inicializado com {len(self.platforms)} plataformas de afiliados configuradas")
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            # Configuração padrão caso o arquivo não seja encontrado
            self.platforms = [
                {
                    "name": "Hotmart",
                    "base_url": "https://www.hotmart.com/marketplace",
                    "search_url": "https://www.hotmart.com/marketplace/search?q={search_term}",
                    "commission_selector": "span.commission-value",
                    "product_selector": "div.product-card",
                    "title_selector": "h3.product-title",
                    "price_selector": "span.product-price",
                    "seller_selector": "span.seller-name",
                    "category_selector": "span.category-name",
                    "url_selector": "a.product-link"
                },
                {
                    "name": "Monetizze",
                    "base_url": "https://www.monetizze.com.br/marketplace",
                    "search_url": "https://www.monetizze.com.br/marketplace?q={search_term}",
                    "commission_selector": "div.commission-info",
                    "product_selector": "div.product-item",
                    "title_selector": "h2.product-name",
                    "price_selector": "span.price",
                    "seller_selector": "div.seller",
                    "category_selector": "span.category",
                    "url_selector": "a.product-url"
                },
                {
                    "name": "Eduzz",
                    "base_url": "https://www.eduzz.com/marketplace",
                    "search_url": "https://www.eduzz.com/marketplace?q={search_term}",
                    "commission_selector": "div.commission",
                    "product_selector": "div.product-block",
                    "title_selector": "h3.title",
                    "price_selector": "span.price",
                    "seller_selector": "span.producer",
                    "category_selector": "span.category",
                    "url_selector": "a.details-link"
                },
                {
                    "name": "ClickBank",
                    "base_url": "https://accounts.clickbank.com/marketplace.htm",
                    "search_url": "https://accounts.clickbank.com/marketplace.htm?q={search_term}",
                    "commission_selector": "span.commission-rate",
                    "product_selector": "div.product-item",
                    "title_selector": "h4.product-title",
                    "price_selector": "span.product-price",
                    "seller_selector": "span.vendor-name",
                    "category_selector": "span.product-category",
                    "url_selector": "a.product-link"
                },
                {
                    "name": "Braip",
                    "base_url": "https://www.braip.com/marketplace",
                    "search_url": "https://www.braip.com/marketplace?busca={search_term}",
                    "commission_selector": "div.product-commission",
                    "product_selector": "div.product-card",
                    "title_selector": "h3.product-title",
                    "price_selector": "div.product-price",
                    "seller_selector": "div.producer-name",
                    "category_selector": "div.product-category",
                    "url_selector": "a.product-link"
                }
            ]
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            self.keywords = [
                "curso vendas online", "curso de vendas", "vendas online", 
                "dropshipping", "curso dropshipping", "ebook empreendedorismo", 
                "empreendedorismo digital", "marketing digital", "afiliado"
            ]
            self.categories = [
                "Cursos Online", "Infoprodutos", "Marketing Digital", 
                "Empreendedorismo", "Negócios", "E-commerce"
            ]
            self.proxy = None
            self.delay_range = [1, 3]
    
    def find_affiliate_programs(self, product_names, max_programs_per_platform=5):
        """
        Encontra programas de afiliados para produtos específicos.
        
        Args:
            product_names: Lista de nomes de produtos para pesquisar
            max_programs_per_platform: Número máximo de programas por plataforma
            
        Returns:
            pandas.DataFrame: DataFrame com os programas encontrados
        """
        all_programs = []
        
        # Expandir termos de busca para cada produto
        search_terms = []
        for product in product_names:
            # Criar variações de termos de busca para maior cobertura
            product_terms = [product]
            
            # Adicionar termos sem "Curso de" ou "Ebook" para ampliar resultados
            if product.lower().startswith("curso de "):
                product_terms.append(product[9:])
            elif product.lower().startswith("curso "):
                product_terms.append(product[6:])
            elif product.lower().startswith("ebook "):
                product_terms.append(product[6:])
            
            search_terms.extend(product_terms)
        
        # Adicionar keywords gerais para complementar
        search_terms.extend(self.keywords)
        
        logger.info(f"Buscando programas de afiliados para {len(product_names)} produtos usando {len(search_terms)} termos de busca")
        
        for platform in self.platforms:
            platform_name = platform['name']
            logger.info(f"Buscando em {platform_name}")
            
            platform_programs = []
            
            # Buscar por cada termo
            for term in search_terms:
                try:
                    logger.info(f"Pesquisando por '{term}' em {platform_name}")
                    
                    # Tentar coletar dados reais
                    url = platform['search_url'].format(search_term=term.replace(' ', '+'))
                    programs = self._scrape_platform(platform, url, term)
                    
                    if programs:
                        logger.info(f"Encontrados {len(programs)} programas para '{term}' em {platform_name}")
                        platform_programs.extend(programs)
                    
                    # Limitar número de programas por plataforma
                    if len(platform_programs) >= max_programs_per_platform:
                        break
                        
                    # Pausa para evitar bloqueios
                    self._random_delay()
                    
                except Exception as e:
                    logger.error(f"Erro ao buscar '{term}' em {platform_name}: {e}")
            
            # Se nenhum programa foi encontrado com scraping, usar dados simulados
            if not platform_programs:
                logger.info(f"Sem resultados reais para {platform_name}, usando dados simulados")
                simulated_programs = self._simulate_affiliate_programs(platform_name, product_names)
                platform_programs.extend(simulated_programs)
            
            # Adicionar programas encontrados na plataforma
            all_programs.extend(platform_programs)
            
            # Pausa entre plataformas
            time.sleep(2)
        
        # Converter para DataFrame
        df = pd.DataFrame(all_programs)
        
        if not df.empty:
            # Adicionar timestamp da coleta
            df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Remover duplicatas e ordenar por score
            df = df.drop_duplicates(subset=['title', 'platform']).sort_values('score', ascending=False)
            
            # Filtrar para programas relevantes para os produtos específicos
            df = self._filter_relevant_programs(df, product_names)
            
            logger.info(f"Total de programas de afiliados encontrados: {len(df)}")
            return df
        else:
            logger.warning("Nenhum programa de afiliados encontrado")
            return pd.DataFrame()
    
    def _scrape_platform(self, platform, url, search_term):
        """
        Coleta dados de programas de afiliados de uma plataforma.
        
        Args:
            platform: Configuração da plataforma
            url: URL de busca
            search_term: Termo de busca
            
        Returns:
            list: Lista de programas de afiliados
        """
        programs = []
        
        # Fazer requisição
        response = self._make_request(url)
        if not response:
            return programs
        
        # Processar HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extrair programas
        program_elements = soup.select(platform['product_selector'])
        logger.info(f"Encontrados {len(program_elements)} elementos de produto na página")
        
        for element in program_elements:
            try:
                # Extrair informações básicas
                title = self._get_text(element, platform['title_selector'])
                price_text = self._get_text(element, platform['price_selector'])
                commission_text = self._get_text(element, platform['commission_selector'])
                seller = self._get_text(element, platform['seller_selector'])
                category = self._get_text(element, platform['category_selector'])
                url = self._get_attribute(element, platform['url_selector'], 'href')
                
                # Converter URL relativa para absoluta
                full_url = self._get_full_url(url, platform['base_url'])
                
                # Extrair valores numéricos
                price = self._extract_price(price_text)
                commission_rate = self._extract_commission_rate(commission_text)
                
                # Calcular comissão estimada
                estimated_commission = self._calculate_estimated_commission(price, commission_rate)
                
                # Calcular pontuação de relevância
                relevance_score = self._calculate_relevance_score(title, search_term)
                
                # Adicionar programa apenas se tiver título
                if title:
                    program = {
                        'title': title,
                        'platform': platform['name'],
                        'seller': seller,
                        'category': category or "Sem categoria",
                        'price': price,
                        'commission_rate': commission_rate,
                        'estimated_commission': estimated_commission,
                        'url': full_url,
                        'relevance': relevance_score,
                        'search_term': search_term,
                        'is_real_data': True,
                        'score': self._calculate_program_score(price, commission_rate, relevance_score)
                    }
                    programs.append(program)
            
            except Exception as e:
                logger.warning(f"Erro ao extrair programa: {e}")
                continue
        
        return programs
    
    def _get_text(self, element, selector):
        """
        Extrai texto de um elemento HTML.
        
        Args:
            element: Elemento BeautifulSoup
            selector: Seletor CSS
            
        Returns:
            str: Texto extraído ou string vazia
        """
        if not selector:
            return ""
            
        try:
            target = element.select_one(selector)
            return target.get_text().strip() if target else ""
        except Exception:
            return ""
    
    def _get_attribute(self, element, selector, attribute):
        """
        Extrai atributo de um elemento HTML.
        
        Args:
            element: Elemento BeautifulSoup
            selector: Seletor CSS
            attribute: Nome do atributo
            
        Returns:
            str: Valor do atributo ou string vazia
        """
        if not selector:
            return ""
            
        try:
            target = element.select_one(selector)
            return target.get(attribute, "") if target else ""
        except Exception:
            return ""
    
    def _get_full_url(self, url, base_url):
        """
        Converte URL relativa em absoluta.
        
        Args:
            url: URL relativa ou absoluta
            base_url: URL base da plataforma
            
        Returns:
            str: URL absoluta
        """
        if not url:
            return ""
            
        if url.startswith(('http://', 'https://')):
            return url
        
        # Extrair domínio da base_url
        import re
        domain_match = re.match(r'(https?://[^/]+)', base_url)
        domain = domain_match.group(1) if domain_match else base_url
        
        if url.startswith('/'):
            return domain + url
        else:
            return domain + '/' + url
    
    def _extract_price(self, price_text):
        """
        Extrai valor numérico de preço.
        
        Args:
            price_text: Texto contendo preço
            
        Returns:
            float: Valor do preço ou None
        """
        if not price_text:
            return None
            
        try:
            # Remover símbolos de moeda e normalizar
            import re
            price_digits = re.sub(r'[^\d,.]', '', price_text)
            
            # Converter para formato numérico
            if ',' in price_digits and '.' not in price_digits:
                # Formato brasileiro (1.234,56)
                price_digits = price_digits.replace('.', '').replace(',', '.')
            elif ',' in price_digits and '.' in price_digits:
                # Formato com separador de milhar (1,234.56)
                price_digits = price_digits.replace(',', '')
            
            return float(price_digits)
        except Exception:
            return None
    
    def _extract_commission_rate(self, commission_text):
        """
        Extrai taxa de comissão de um texto.
        
        Args:
            commission_text: Texto contendo taxa de comissão
            
        Returns:
            float: Taxa de comissão em porcentagem ou None
        """
        if not commission_text:
            return None
            
        try:
            # Buscar padrão de porcentagem (30%, 50% etc)
            import re
            match = re.search(r'(\d+(?:[.,]\d+)?)%', commission_text)
            if match:
                return float(match.group(1).replace(',', '.'))
            
            # Buscar formato X de Y (ex: "R$ 50 de R$ 100" = 50%)
            commission_parts = re.findall(r'(\d+(?:[.,]\d+)?)', commission_text)
            if len(commission_parts) >= 2:
                commission = float(commission_parts[0].replace(',', '.'))
                total = float(commission_parts[1].replace(',', '.'))
                if total > 0:
                    return (commission / total) * 100
            
            # Buscar valor absoluto e calcular porcentagem se possível
            value_match = re.search(r'R?\$?\s*(\d+(?:[.,]\d+)?)', commission_text)
            if value_match:
                return None  # Precisaria do valor do produto para calcular a porcentagem
        
        except Exception:
            pass
            
        return None
    
    def _calculate_estimated_commission(self, price, commission_rate):
        """
        Calcula a comissão estimada com base no preço e taxa.
        
        Args:
            price: Preço do produto
            commission_rate: Taxa de comissão em porcentagem
            
        Returns:
            float: Valor estimado da comissão ou None
        """
        if price is None or commission_rate is None:
            return None
            
        return price * (commission_rate / 100)
    
    def _calculate_relevance_score(self, title, search_term):
        """
        Calcula pontuação de relevância entre título e termo de busca.
        
        Args:
            title: Título do programa
            search_term: Termo de busca
            
        Returns:
            float: Pontuação de relevância entre 0 e 1
        """
        if not title or not search_term:
            return 0.0
            
        title_lower = title.lower()
        search_term_lower = search_term.lower()
        
        # Pontuação base
        score = 0.0
        
        # Correspondência exata
        if search_term_lower in title_lower:
            score += 0.7
            
            # Bônus para correspondência no início do título
            if title_lower.startswith(search_term_lower):
                score += 0.2
        
        # Correspondência parcial (palavras individuais)
        search_words = search_term_lower.split()
        matched_words = sum(1 for word in search_words if word in title_lower)
        word_score = (matched_words / len(search_words)) * 0.3
        
        # Combinar pontuações (máximo 1.0)
        final_score = min(1.0, score + word_score)
        
        return final_score
    
    def _calculate_program_score(self, price, commission_rate, relevance_score):
        """
        Calcula pontuação geral do programa de afiliados.
        
        Args:
            price: Preço do produto
            commission_rate: Taxa de comissão
            relevance_score: Pontuação de relevância
            
        Returns:
            float: Pontuação geral de 0 a 100
        """
        # Pontuação base
        base_score = 50.0
        
        # Componente de preço (produtos mais caros tendem a dar mais comissão)
        price_score = 0.0
        if price is not None and price > 0:
            # Escala logarítmica para preço (favorece produtos mais caros, mas com limite)
            import math
            price_score = min(25.0, 5.0 * math.log10(max(1, price)))
        
        # Componente de comissão
        commission_score = 0.0
        if commission_rate is not None:
            # Escala linear para comissão (mais é melhor)
            commission_score = min(35.0, commission_rate * 0.7)
        
        # Componente de relevância
        relevance_component = relevance_score * 40.0
        
        # Combinar componentes
        final_score = base_score + price_score + commission_score + relevance_component
        
        # Normalizar para 0-100
        normalized_score = min(100.0, max(0.0, final_score))
        
        return round(normalized_score, 2)
    
    def _make_request(self, url):
        """
        Faz requisição HTTP com tratamento de erros.
        
        Args:
            url: URL para requisição
            
        Returns:
            Response: Objeto de resposta ou None
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
                elif response.status_code in [403, 429]:
                    logger.warning(f"Possível bloqueio (status {response.status_code}). Aguardando...")
                    time.sleep(10 + attempt * 5)  # Aumento progressivo do tempo de espera
                else:
                    logger.warning(f"Requisição falhou com status {response.status_code} para {url}")
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"Tentativa {attempt+1}/{max_retries} falhou: {e}")
                time.sleep(2)
                
        logger.error(f"Todas as tentativas falharam para {url}")
        return None
    
    def _random_delay(self):
        """
        Adiciona atraso aleatório para evitar bloqueios.
        """
        delay = random.uniform(self.delay_range[0], self.delay_range[1])
        time.sleep(delay)
    
    def _simulate_affiliate_programs(self, platform_name, product_names):
        """
        Simula dados de programas de afiliados para desenvolvimento.
        
        Args:
            platform_name: Nome da plataforma
            product_names: Lista de nomes de produtos para simular
            
        Returns:
            list: Lista de programas de afiliados simulados
        """
        programs = []
        
        # Configurações específicas por plataforma
        platform_configs = {
            "Hotmart": {
                "base_commission": [40, 70],
                "price_range": [97, 1997],
                "seller_prefix": "Academia ",
                "url_template": "https://www.hotmart.com/product/{}",
                "categories": ["Marketing Digital", "E-commerce", "Empreendedorismo"]
            },
            "Monetizze": {
                "base_commission": [30, 60],
                "price_range": [67, 1497],
                "seller_prefix": "Instituto ",
                "url_template": "https://app.monetizze.com.br/produto/{}",
                "categories": ["Negócios Online", "Marketing", "Vendas"]
            },
            "Eduzz": {
                "base_commission": [35, 65],
                "price_range": [47, 997],
                "seller_prefix": "Escola ",
                "url_template": "https://www.eduzz.com/produto/{}",
                "categories": ["Infoprodutos", "Educação", "Empreendedorismo Digital"]
            },
            "ClickBank": {
                "base_commission": [50, 75],
                "price_range": [27, 997],
                "seller_prefix": "Pro ",
                "url_template": "https://vendor.clickbank.net/{}",
                "categories": ["Business", "E-business", "Marketing"]
            },
            "Braip": {
                "base_commission": [30, 55],
                "price_range": [97, 1497],
                "seller_prefix": "Grupo ",
                "url_template": "https://www.braip.com/produto/{}",
                "categories": ["Educação", "Marketing Digital", "Empreendedorismo"]
            }
        }
        
        # Usar configuração padrão se a plataforma não estiver configurada
        config = platform_configs.get(platform_name, {
            "base_commission": [30, 60],
            "price_range": [97, 997],
            "seller_prefix": "Tech ",
            "url_template": "https://example.com/produto/{}",
            "categories": ["Cursos Online", "Infoprodutos", "Marketing Digital"]
        })
        
        # Nomes de vendedores simulados
        seller_names = [
            "Digital", "Expert", "Master", "Pro", "Academy",
            "School", "Institute", "University", "Learning", "Education"
        ]
        
        # Sufixos para produtos
        product_suffixes = [
            "Premium", "Pro", "Master", "Elite", "VIP",
            "2.0", "Avançado", "Completo", "Ultimate", "Academy"
        ]
        
        # Gerar programas para cada produto
        for product_name in product_names:
            # Número de variações por produto (1-3)
            variations = random.randint(1, 3)
            
            for i in range(variations):
                # Gerar título com variação
                if i > 0:
                    suffix_index = (hash(f"{product_name}_{i}") % len(product_suffixes))
                    title = f"{product_name} {product_suffixes[suffix_index]}"
                else:
                    title = product_name
                
                # Gerar nome do vendedor
                seller_index = (hash(f"{platform_name}_{product_name}_{i}_seller") % len(seller_names))
                seller_name = f"{config['seller_prefix']}{seller_names[seller_index]}"
                
                # Gerar categoria
                category_index = (hash(f"{platform_name}_{product_name}_{i}_category") % len(config['categories']))
                category = config['categories'][category_index]
                
                # Gerar preço
                seed = hash(f"{platform_name}_{product_name}_{i}_price")
                random.seed(seed)
                price_min, price_max = config['price_range']
                
                # Preços tendem a seguir padrões de marketing (97, 197, 297, etc.)
                price_base = random.randint(price_min // 100, price_max // 100)
                price = price_base * 100 - 3
                
                # Gerar taxa de comissão
                comm_min, comm_max = config['base_commission']
                commission_rate = random.randint(comm_min, comm_max)
                
                # Calcular comissão estimada
                estimated_commission = price * (commission_rate / 100)
                
                # Calcular relevância simulada (alta para o produto original)
                relevance = 1.0 if i == 0 else random.uniform(0.7, 0.9)
                
                # Gerar URL simulada
                url_segment = re.sub(r'[^a-zA-Z0-9]', '-', title.lower())
                url = config['url_template'].format(url_segment)
                
                # Calcular pontuação geral
                score = self._calculate_program_score(price, commission_rate, relevance)
                
                # Adicionar programa simulado
                program = {
                    'title': title,
                    'platform': platform_name,
                    'seller': seller_name,
                    'category': category,
                    'price': price,
                    'commission_rate': commission_rate,
                    'estimated_commission': estimated_commission,
                    'url': url,
                    'relevance': relevance,
                    'search_term': product_name,
                    'is_real_data': False,
                    'score': score
                }
                
                programs.append(program)
        
        return programs
    
    def _filter_relevant_programs(self, df, product_names):
        """
        Filtra programas de afiliados relevantes para os produtos especificados.
        
        Args:
            df: DataFrame com todos os programas
            product_names: Lista de nomes de produtos de interesse
            
        Returns:
            DataFrame: Programas filtrados
        """
        if df.empty:
            return df
            
        # Se houver poucos programas, não filtrar
        if len(df) <= 10:
            return df
            
        # Criar conjunto de palavras-chave dos produtos
        product_keywords = []
        for product in product_names:
            parts = product.lower().split()
            product_keywords.extend(parts)
            
            # Adicionar palavra sem prefixos comuns
            if product.lower().startswith("curso de "):
                product_keywords.append(product[9:].lower())
            elif product.lower().startswith("curso "):
                product_keywords.append(product[6:].lower())
            elif product.lower().startswith("ebook "):
                product_keywords.append(product[6:].lower())
        
        # Remover palavras muito comuns
        common_words = {"de", "e", "a", "o", "para", "como", "em", "um", "uma", "com"}
        product_keywords = [word for word in product_keywords if word not in common_words]
        
        # Criar função para verificar relevância
        def is_relevant(row):
            title = row['title'].lower()
            
            # Alta relevância se for um dos produtos especificados
            for product in product_names:
                if product.lower() in title:
                    return True
            
            # Relevância baseada em palavras-chave
            matches = sum(keyword in title for keyword in product_keywords)
            return matches >= 1  # Pelo menos uma palavra-chave deve corresponder
        
        # Filtrar programas relevantes
        relevant_df = df[df.apply(is_relevant, axis=1)].copy()
        
        # Se filtrou demais, retornar todos
        if len(relevant_df) < 5:
            return df
        
        return relevant_df
    
    def get_top_programs(self, df, n=10):
        """
        Obtém os N melhores programas de afiliados.
        
        Args:
            df: DataFrame com programas de afiliados
            n: Número de programas para retornar
            
        Returns:
            pandas.DataFrame: Top programas
        """
        if df.empty:
            return df
            
        # Ordenar por pontuação
        return df.sort_values('score', ascending=False).head(n)
    
    def get_top_programs_by_platform(self, df, n_per_platform=3):
        """
        Obtém os N melhores programas de cada plataforma.
        
        Args:
            df: DataFrame com programas de afiliados
            n_per_platform: Número de programas por plataforma
            
        Returns:
            dict: Dicionário com os melhores programas por plataforma
        """
        if df.empty:
            return {}
            
        result = {}
        
        # Agrupar por plataforma
        for platform, group in df.groupby('platform'):
            # Ordenar por pontuação
            
            top_programs = group.sort_values('score', ascending=False).head(n_per_platform);                                                                
    # Aqui coloquei a segunda parte, lembrando que a ultima linha ficou incompleta
    def get_top_programs_by_platform(self, df, n_per_platform=3):
        """
        Obtém os N melhores programas de cada plataforma.
        
        Args:
            df: DataFrame com programas de afiliados
            n_per_platform: Número de programas por plataforma
            
        Returns:
            dict: Dicionário com os melhores programas por plataforma
        """
        if df.empty:
            return {}
            
        result = {}
        
        # Agrupar por plataforma
        for platform, group in df.groupby('platform'):
            # Ordenar por pontuação
            top_programs = group.sort_values('score', ascending=False).head(n_per_platform)
            
            if not top_programs.empty:
                result[platform] = top_programs
        
        return result
    
    def get_programs_by_category(self, df):
        """
        Agrupa programas de afiliados por categoria.
        
        Args:
            df: DataFrame com programas de afiliados
            
        Returns:
            dict: Dicionário com programas por categoria
        """
        if df.empty:
            return {}
            
        result = {}
        
        # Agrupar por categoria
        for category, group in df.groupby('category'):
            # Ordenar por pontuação
            category_programs = group.sort_values('score', ascending=False)
            
            if not category_programs.empty:
                result[category] = category_programs
        
        return result
    
    def save_to_csv(self, df, filename='output/data/affiliate_programs.csv'):
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
    
    def generate_affiliate_report(self, top_programs, product_names, report_path='output/reports/affiliate_opportunities.html'):
        """
        Gera um relatório HTML com os melhores programas de afiliados.
        
        Args:
            top_programs: DataFrame com os melhores programas
            product_names: Lista de nomes de produtos alvo
            report_path: Caminho para salvar o relatório
            
        Returns:
            str: Caminho do relatório gerado
        """
        if top_programs.empty:
            logger.warning("Sem programas para gerar relatório")
            return None
            
        try:
            # Criar estrutura do relatório
            html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oportunidades de Afiliados</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        .header {{
            background-color: #3498db;
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 30px;
            border-radius: 5px;
        }}
        .product-section {{
            margin-bottom: 40px;
        }}
        .program-card {{
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
            background-color: #f9f9f9;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .program-card h3 {{
            margin-top: 0;
            color: #3498db;
        }}
        .program-info {{
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }}
        .info-item {{
            flex-basis: 48%;
            margin-bottom: 10px;
        }}
        .label {{
            font-weight: bold;
            color: #7f8c8d;
        }}
        .value {{
            color: #2c3e50;
        }}
        .score {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
            background-color: #2ecc71;
            color: white;
        }}
        .cta {{
            text-align: center;
            margin-top: 15px;
        }}
        .cta a {{
            display: inline-block;
            background-color: #e74c3c;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s;
        }}
        .cta a:hover {{
            background-color: #c0392b;
        }}
        .platform-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            font-weight: bold;
            background-color: #34495e;
            color: white;
            margin-right: 10px;
        }}
        .disclaimer {{
            margin-top: 50px;
            padding: 15px;
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            font-style: italic;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Melhores Oportunidades de Afiliados</h1>
        <p>Programas de afiliados recomendados para produtos sem necessidade de estoque</p>
        <p>Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    
    <div class="product-section">
        <h2>Produtos Alvo</h2>
        <p>Este relatório analisa os melhores programas de afiliados para os seguintes produtos:</p>
        <ul>
            {"".join(f"<li>{product}</li>" for product in product_names)}
        </ul>
    </div>
    
    <h2>Top Programas de Afiliados</h2>
"""
            
            # Adicionar programas ao relatório
            for _, program in top_programs.iterrows():
                # Calcular cor da pontuação baseada no valor
                score = program['score']
                if score >= 80:
                    score_color = "#2ecc71"  # Verde
                elif score >= 60:
                    score_color = "#f39c12"  # Laranja
                else:
                    score_color = "#e74c3c"  # Vermelho
                
                # Formatação dos valores monetários
                price_str = f"R$ {program['price']:.2f}" if program['price'] else "Não informado"
                commission_rate_str = f"{program['commission_rate']:.1f}%" if program['commission_rate'] else "Não informado"
                estimated_commission_str = f"R$ {program['estimated_commission']:.2f}" if program['estimated_commission'] else "Não calculado"
                
                # Adicionar card do programa
                html_content += f"""
    <div class="program-card">
        <span class="platform-badge">{program['platform']}</span>
        <h3>{program['title']}</h3>
        <div class="program-info">
            <div class="info-item">
                <span class="label">Vendedor:</span> 
                <span class="value">{program['seller']}</span>
            </div>
            <div class="info-item">
                <span class="label">Categoria:</span> 
                <span class="value">{program['category']}</span>
            </div>
            <div class="info-item">
                <span class="label">Preço:</span> 
                <span class="value">{price_str}</span>
            </div>
            <div class="info-item">
                <span class="label">Taxa de Comissão:</span> 
                <span class="value">{commission_rate_str}</span>
            </div>
            <div class="info-item">
                <span class="label">Comissão Estimada:</span> 
                <span class="value">{estimated_commission_str}</span>
            </div>
            <div class="info-item">
                <span class="label">Pontuação:</span> 
                <span class="score" style="background-color: {score_color};">{score:.1f}</span>
            </div>
        </div>
        <div class="cta">
            <a href="{program['url']}" target="_blank">Ver Programa</a>
        </div>
    </div>
"""
            
            # Adicionar rodapé e fechar tags HTML
            html_content += """
    <div class="disclaimer">
        <p>Observação: As comissões e valores apresentados são estimativas e podem variar. Recomenda-se verificar as condições atuais diretamente nas plataformas de afiliados antes de tomar decisões.</p>
    </div>
</body>
</html>
"""
            
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            
            # Salvar relatório
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            logger.info(f"Relatório gerado em: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            return None


# Execução standalone para testes
if __name__ == "__main__":
    import os
    
    # Criar diretório de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    # Produtos de exemplo (pode ser substituído pelos resultados reais do sistema)
    test_products = [
        "Curso de Vendas Online",
        "Curso de Dropshipping",
        "Ebook Empreendedorismo"
    ]
    
    finder = AffiliateFinder()
    
    print(f"Buscando programas de afiliados para: {', '.join(test_products)}")
    affiliate_programs = finder.find_affiliate_programs(test_products)
    
    if not affiliate_programs.empty:
        print(f"Encontrados {len(affiliate_programs)} programas de afiliados.")
        
        # Salvar todos os programas encontrados
        os.makedirs('output/data', exist_ok=True)
        finder.save_to_csv(affiliate_programs)
        
        # Obter top programas
        top_programs = finder.get_top_programs(affiliate_programs, n=10)
        
        print("\nTop 10 Programas de Afiliados:")
        for i, (_, program) in enumerate(top_programs.iterrows()):
            print(f"\n{i+1}. {program['title']} ({program['platform']})")
            print(f"   Preço: R$ {program['price']}" if program['price'] else "   Preço: Não informado")
            print(f"   Comissão: {program['commission_rate']}%" if program['commission_rate'] else "   Comissão: Não informada")
            print(f"   Pontuação: {program['score']}")
        
        # Gerar relatório HTML
        os.makedirs('output/reports', exist_ok=True)
        report_path = finder.generate_affiliate_report(top_programs, test_products)
        
        if report_path:
            print(f"\nRelatório gerado: {report_path}")
    else:
        print("Nenhum programa de afiliados encontrado.")                                                                           
