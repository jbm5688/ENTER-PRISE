import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/franchise_scraper.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("franchise_scraper")

class FranchiseScraper:
    """
    Classe responsável por coletar dados de oportunidades de franquia de diferentes fontes.
    Foca em identificar franquias que não exigem estoque físico.
    """
    
    def __init__(self, config_path='config/franchise_sources.json'):
        """
        Inicializa o scraper com as fontes de dados e configurações.
        
        Args:
            config_path: Caminho para o arquivo de configuração JSON
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.sources = config['sources']
                self.headers = config['headers']
                self.no_stock_keywords = config['no_stock_keywords']
                
            logger.info(f"Inicializado com {len(self.sources)} fontes configuradas")
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            # Configuração padrão caso o arquivo não seja encontrado
            self.sources = []
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            self.no_stock_keywords = [
                'sem estoque', 'não precisa de estoque', 'estoque zero',
                'sem necessidade de estoque', 'dropshipping', 'digital'
            ]
    
    def scrape_franchise_opportunities(self):
        """
        Coleta dados de oportunidades de franquia de múltiplas fontes.
        
        Returns:
            pandas.DataFrame: DataFrame com os dados coletados
        """
        all_opportunities = []
        
        for source in self.sources:
            try:
                logger.info(f"Iniciando coleta da fonte: {source['name']}")
                response = self._make_request(source['url'])
                
                if not response:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                opportunities = self._extract_opportunities(soup, source)
                
                logger.info(f"Coletadas {len(opportunities)} oportunidades de {source['name']}")
                all_opportunities.extend(opportunities)
                
            except Exception as e:
                logger.error(f"Erro ao coletar dados de {source['name']}: {e}")
        
        # Converter para DataFrame e processar
        df = pd.DataFrame(all_opportunities)
        
        if not df.empty:
            # Adicionar timestamp da coleta
            df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Filtrar apenas franquias sem estoque
            no_stock_df = self._filter_no_stock_franchises(df)
            logger.info(f"Total de oportunidades: {len(df)}, Sem estoque: {len(no_stock_df)}")
            
            return no_stock_df
        else:
            logger.warning("Nenhuma oportunidade encontrada")
            return pd.DataFrame()
    
    def _make_request(self, url):
        """
        Realiza a requisição HTTP com tratamento de erros e retentativas.
        
        Args:
            url: URL para fazer a requisição
            
        Returns:
            Response object ou None em caso de falha
        """
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                
                if response.status_code == 200:
                    return response
                else:
                    logger.warning(f"Requisição falhou com status {response.status_code} para {url}")
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"Tentativa {attempt+1}/{max_retries} falhou: {e}")
                
        logger.error(f"Todas as tentativas falharam para {url}")
        return None
    
    def _extract_opportunities(self, soup, source):
        """
        Extrai informações de oportunidades de franquia usando seletores específicos.
        
        Args:
            soup: Objeto BeautifulSoup com o HTML da página
            source: Informações da fonte (incluindo seletores)
            
        Returns:
            list: Lista de dicionários com informações de oportunidades
        """
        opportunities = []
        selectors = source['selectors']
        
        try:
            # Encontrar contêineres de itens
            items = soup.select(selectors['item_container'])
            logger.info(f"Encontrados {len(items)} itens em {source['name']}")
            
            for item in items:
                try:
                    # Extrair dados básicos
                    opportunity = {
                        'title': self._get_text(item, selectors['title']),
                        'company': self._get_text(item, selectors.get('company', selectors['title'])),
                        'description': self._get_text(item, selectors.get('description', '')),
                        'url': self._get_full_url(
                            self._get_attribute(item, selectors['url'], 'href'), 
                            source['url']
                        ),
                        'source': source['name'],
                        'category': self._get_text(item, selectors.get('category', ''))
                    }
                    
                    # Extrair valores numéricos
                    opportunity['commission'] = self._extract_commission(
                        self._get_text(item, selectors.get('commission', ''))
                    )
                    
                    opportunity['min_investment'] = self._extract_value(
                        self._get_text(item, selectors.get('min_investment', ''))
                    )
                    
                    # Verificar requisito de estoque
                    opportunity['has_stock_requirement'] = self._check_stock_requirement(
                        self._get_text(item, selectors.get('description', ''))
                    )
                    
                    # Adicionar apenas se tiver pelo menos título e URL
                    if opportunity['title'] and opportunity['url']:
                        opportunities.append(opportunity)
                    
                except Exception as e:
                    logger.warning(f"Erro ao extrair oportunidade: {e}")
            
        except Exception as e:
            logger.error(f"Erro ao processar {source['name']}: {e}")
        
        return opportunities
    
    def _get_text(self, item, selector):
        """
        Extrai texto de um elemento.
        
        Args:
            item: Elemento HTML da oportunidade
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
            item: Elemento HTML da oportunidade
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
        
        # Remover query parameters da base_url
        base_parts = base_url.split('?')[0]
        
        # Se começa com /, juntar com o domínio
        if relative_url.startswith('/'):
            # Extrair protocolo e domínio
            domain_match = re.match(r'(https?://[^/]+)', base_parts)
            if domain_match:
                return domain_match.group(1) + relative_url
        
        # Caso contrário, juntar com o path base
        return base_parts.rstrip('/') + '/' + relative_url.lstrip('/')
    
    def _extract_commission(self, commission_text):
        """
        Extrai e normaliza informação de comissão.
        
        Args:
            commission_text: Texto contendo informação de comissão
            
        Returns:
            float: Valor da comissão ou None
        """
        if not commission_text:
            return None
            
        # Extrair porcentagem usando regex
        match = re.search(r'(\d+(?:[.,]\d+)?)%', commission_text)
        if match:
            # Substituir vírgula por ponto para float
            commission_str = match.group(1).replace(',', '.')
            return float(commission_str)
        
        return None
    
    def _extract_value(self, value_text):
        """
        Extrai e normaliza valores monetários.
        
        Args:
            value_text: Texto contendo valor monetário
            
        Returns:
            float: Valor monetário ou None
        """
        if not value_text:
            return None
            
        # Remover símbolos de moeda e converter para float
        try:
            # Procurar por padrão de valor (R$ 1.000,00 ou 1,000.00)
            match = re.search(r'R?\$?\s*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)', value_text)
            if match:
                # Normalizar o formato: remover pontos de milhar e converter vírgula para ponto decimal
                value_str = match.group(1)
                
                # Verificar formato brasileiro (vírgula decimal)
                if ',' in value_str and re.search(r'\d,\d{2}$', value_str):
                    value_str = value_str.replace('.', '').replace(',', '.')
                else:
                    # Formato americano ou misto
                    value_str = value_str.replace(',', '')
                
                return float(value_str)
        except Exception:
            pass
            
        return None
    
    def _check_stock_requirement(self, description):
        """
        Verifica se a franquia requer estoque baseado na descrição.
        
        Args:
            description: Texto de descrição da franquia
            
        Returns:
            bool: True se requer estoque, False se não requer, None se indeterminado
        """
        if not description:
            return None
            
        description_lower = description.lower()
        
        # Verificar palavras-chave para "sem estoque"
        for keyword in self.no_stock_keywords:
            if keyword in description_lower:
                return False
        
        # Palavras-chave que indicam necessidade de estoque
        stock_keywords = ['estoque necessário', 'manter estoque', 'estoque mínimo', 'produtos físicos']
        for keyword in stock_keywords:
            if keyword in description_lower:
                return True
                
        return None
    
    def _filter_no_stock_franchises(self, df):
        """
        Filtra o DataFrame para manter apenas franquias sem requisito de estoque.
        
        Args:
            df: DataFrame com todas as oportunidades
            
        Returns:
            DataFrame: Oportunidades filtradas
        """
        # Filtrar oportunidades explicitamente sem estoque
        no_stock_df = df[df['has_stock_requirement'] == False].copy()
        
        # Se não houver suficientes, incluir as indeterminadas
        if len(no_stock_df) < 10:
            indeterminate_df = df[df['has_stock_requirement'].isna()].copy()
            no_stock_df = pd.concat([no_stock_df, indeterminate_df])
            
        return no_stock_df
    
    def save_to_csv(self, df, filename='output/data/franchise_opportunities.csv'):
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
    
    scraper = FranchiseScraper()
    opportunities = scraper.scrape_franchise_opportunities()
    
    if not opportunities.empty:
        print(f"Coletadas {len(opportunities)} oportunidades de franquia sem estoque.")
        
        # Salvar resultados
        os.makedirs('output/data', exist_ok=True)
        scraper.save_to_csv(opportunities)
        
        # Mostrar primeiras linhas
        print("\nPrimeiras 5 oportunidades:")
        print(opportunities[['title', 'company', 'commission', 'min_investment']].head())
    else:
        print("Nenhuma oportunidade encontrada ou erro na coleta.")
    def collect_data(self, limit=100):
    """
    Coleta dados de franquias (versão simulada para testes)
    
    Args:
        limit (int): Número máximo de franquias a coletar
        
    Returns:
        list: Lista de dados de franquias
    """
    print(f"Simulando coleta de dados de {limit} franquias...")
    
    # Dados simulados para teste
    sample_franchises = [
        {
            'name': 'PetFood Express',
            'sector': 'Pet Shop',
            'investment': {
                'min': 80000,
                'max': 150000
            },
            'roi_estimate': 0.32,
            'payback_months': 24,
            'website': 'https://www.petfoodexpress.com.br',
            'contact': 'contato@petfoodexpress.com.br'
        },
        {
            'name': 'CleanTech',
            'sector': 'Limpeza Ecológica',
            'investment': {
                'min': 50000,
                'max': 120000
            },
            'roi_estimate': 0.28,
            'payback_months': 30,
            'website': 'https://www.cleantechbrasil.com.br',
            'contact': 'franquias@cleantechbrasil.com.br'
        },
        {
            'name': 'EducaMais',
            'sector': 'Educação',
            'investment': {
                'min': 120000,
                'max': 280000
            },
            'roi_estimate': 0.25,
            'payback_months': 36,
            'website': 'https://www.educamais.com.br',
            'contact': 'expansao@educamais.com.br'
        },
        {
            'name': 'FastFit Academia',
            'sector': 'Fitness',
            'investment': {
                'min': 200000,
                'max': 450000
            },
            'roi_estimate': 0.22,
            'payback_months': 40,
            'website': 'https://www.fastfitacademia.com.br',
            'contact': 'franquia@fastfit.com.br'
        },
        {
            'name': 'TechRepair',
            'sector': 'Assistência Técnica',
            'investment': {
                'min': 40000,
                'max': 90000
            },
            'roi_estimate': 0.35,
            'payback_months': 20,
            'website': 'https://www.techrepair.com.br',
            'contact': 'negocios@techrepair.com.br'
        }
    ]
    
    # Limitar ao número solicitado
    return sample_franchises[:limit]
