import requests
import json
import pandas as pd
import logging
import time
from datetime import datetime, timedelta
import os
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/social_media_monitor.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("social_media_monitor")

class SocialMediaMonitor:
    """
    Classe para monitorar tendências e conteúdo relevante em redes sociais,
    focando na identificação de produtos e oportunidades de franquia sem estoque
    que estão ganhando popularidade.
    """
    
    def __init__(self, config_path='config/social_media.json'):
        """
        Inicializa o monitor com configurações das redes sociais.
        
        Args:
            config_path: Caminho para o arquivo de configuração JSON
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.platforms = config['platforms']
                self.api_keys = config['api_keys']
                self.keywords = config['keywords']
                self.hashtags = config['hashtags']
                self.lookback_days = config.get('lookback_days', 30)
                
            logger.info(f"Inicializado com {len(self.platforms)} plataformas configuradas")
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            # Configuração padrão caso o arquivo não seja encontrado
            self.platforms = ["instagram", "twitter", "tiktok"]
            self.api_keys = {}
            self.keywords = [
                "dropshipping", "revenda sem estoque", "franquia digital",
                "renda extra", "trabalhar em casa", "marketing digital"
            ]
            self.hashtags = [
                "dropshipping", "revender", "franquiadigital",
                "rendaextra", "empreendedorismo", "marketingdigital"
            ]
            self.lookback_days = 30
    
    def get_trends(self):
        """
        Coleta tendências de todas as redes sociais configuradas.
        
        Returns:
            pandas.DataFrame: DataFrame com as tendências coletadas
        """
        all_trends = []
        
        for platform in self.platforms:
            try:
                platform_method = getattr(self, f"_get_{platform}_trends", None)
                
                if not platform_method:
                    logger.warning(f"Método para coletar tendências do {platform} não implementado")
                    continue
                
                logger.info(f"Coletando tendências do {platform}")
                trends = platform_method()
                
                if trends:
                    logger.info(f"Coletadas {len(trends)} tendências do {platform}")
                    all_trends.extend(trends)
                else:
                    logger.warning(f"Nenhuma tendência encontrada no {platform}")
                
                # Pausa para evitar limitações de API
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Erro ao coletar tendências do {platform}: {e}")
        
        # Converter para DataFrame
        df = pd.DataFrame(all_trends)
        
        if not df.empty:
            # Adicionar timestamp da coleta
            df['collected_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Filtrar tendências relevantes
            filtered_df = self._filter_relevant_trends(df)
            
            logger.info(f"Total de tendências relevantes: {len(filtered_df)}")
            return filtered_df
        else:
            logger.warning("Nenhuma tendência encontrada")
            return pd.DataFrame()
    
    def _get_instagram_trends(self):
        """
        Coleta tendências do Instagram usando API ou simulação.
        
        Returns:
            list: Lista de tendências do Instagram
        """
        # Verificar se temos API key para Instagram
        if 'instagram' not in self.api_keys or not self.api_keys['instagram']:
            logger.info("API key para Instagram não configurada, usando dados simulados")
            return self._simulate_instagram_trends()
        
        try:
            # Construir URL da API
            api_key = self.api_keys['instagram']
            api_url = f"https://graph.instagram.com/v12.0/hashtag_search"
            
            trends = []
            
            # Buscar tendências para cada hashtag
            for hashtag in self.hashtags:
                params = {
                    'user_id': self.api_keys.get('instagram_user_id', ''),
                    'q': hashtag,
                    'access_token': api_key
                }
                
                response = requests.get(api_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'data' in data:
                        # Obter posts recentes com essa hashtag
                        hashtag_id = data['data'][0]['id']
                        recent_posts = self._get_instagram_recent_media(hashtag_id, api_key)
                        
                        if recent_posts:
                            for post in recent_posts:
                                trends.append({
                                    'platform': 'instagram',
                                    'type': 'hashtag',
                                    'term': f"#{hashtag}",
                                    'content': post.get('caption', ''),
                                    'engagement': post.get('like_count', 0) + post.get('comments_count', 0),
                                    'url': f"https://www.instagram.com/p/{post.get('id', '')}/",
                                    'timestamp': post.get('timestamp', '')
                                })
                else:
                    logger.warning(f"Falha ao obter dados do Instagram para #{hashtag}: {response.status_code}")
                    logger.debug(response.text)
            
            return trends
            
        except Exception as e:
            logger.error(f"Erro ao coletar tendências do Instagram: {e}")
            return self._simulate_instagram_trends()
    
    def _get_instagram_recent_media(self, hashtag_id, api_key):
        """
        Coleta posts recentes de um hashtag no Instagram.
        
        Args:
            hashtag_id: ID do hashtag
            api_key: Chave de API para Instagram
            
        Returns:
            list: Lista de posts recentes
        """
        try:
            api_url = f"https://graph.instagram.com/v12.0/{hashtag_id}/recent_media"
            
            params = {
                'user_id': self.api_keys.get('instagram_user_id', ''),
                'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count',
                'access_token': api_key
            }
            
            response = requests.get(api_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            else:
                logger.warning(f"Falha ao obter posts recentes: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Erro ao coletar posts recentes: {e}")
            return []
    
    def _get_twitter_trends(self):
        """
        Coleta tendências do Twitter (X) usando API ou simulação.
        
        Returns:
            list: Lista de tendências do Twitter
        """
        # Verificar se temos API key para Twitter
        if 'twitter' not in self.api_keys or not self.api_keys['twitter']:
            logger.info("API key para Twitter não configurada, usando dados simulados")
            return self._simulate_twitter_trends()
        
        try:
            # Construir cabeçalhos de autenticação
            api_key = self.api_keys['twitter']
            api_key_secret = self.api_keys.get('twitter_secret', '')
            bearer_token = self.api_keys.get('twitter_bearer_token', '')
            
            headers = {
                'Authorization': f'Bearer {bearer_token}'
            }
            
            trends = []
            
            # Buscar tweets para cada keyword e hashtag
            for term in self.keywords + ['#' + tag for tag in self.hashtags]:
                # URL da API de busca (v2)
                api_url = "https://api.twitter.com/2/tweets/search/recent"
                
                # Parâmetros de busca
                params = {
                    'query': term,
                    'max_results': 10,
                    'tweet.fields': 'created_at,public_metrics,entities',
                    'expansions': 'author_id',
                    'user.fields': 'username'
                }
                
                response = requests.get(api_url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'data' in data:
                        for tweet in data['data']:
                            # Mapear dados de usuário
                            author_username = None
                            if 'includes' in data and 'users' in data['includes']:
                                for user in data['includes']['users']:
                                    if user['id'] == tweet['author_id']:
                                        author_username = user['username']
                                        break
                            
                            # Métricas de engajamento
                            engagement = 0
                            if 'public_metrics' in tweet:
                                metrics = tweet['public_metrics']
                                engagement = metrics.get('retweet_count', 0) + metrics.get('like_count', 0) + metrics.get('reply_count', 0)
                            
                            trends.append({
                                'platform': 'twitter',
                                'type': 'tweet',
                                'term': term,
                                'content': tweet['text'],
                                'author': author_username,
                                'engagement': engagement,
                                'url': f"https://twitter.com/{author_username}/status/{tweet['id']}",
                                'timestamp': tweet.get('created_at', '')
                            })
                else:
                    logger.warning(f"Falha ao obter dados do Twitter para {term}: {response.status_code}")
                    logger.debug(response.text)
            
            return trends
            
        except Exception as e:
            logger.error(f"Erro ao coletar tendências do Twitter: {e}")
            return self._simulate_twitter_trends()
    
    def _get_tiktok_trends(self):
        """
        Coleta tendências do TikTok usando API ou simulação.
        
        Returns:
            list: Lista de tendências do TikTok
        """
        # Verificar se temos API key para TikTok
        if 'tiktok' not in self.api_keys or not self.api_keys['tiktok']:
            logger.info("API key para TikTok não configurada, usando dados simulados")
            return self._simulate_tiktok_trends()
        
        try:
            # Usando TikTok API
            api_key = self.api_keys['tiktok']
            
            # Implementação da chamada à API do TikTok
            # Nota: A implementação real dependeria da API específica disponível
            
            # Como a API do TikTok é mais restrita, usamos simulação por enquanto
            return self._simulate_tiktok_trends()
            
        except Exception as e:
            logger.error(f"Erro ao coletar tendências do TikTok: {e}")
            return self._simulate_tiktok_trends()
    
    def _simulate_instagram_trends(self):
        """
        Gera dados simulados de tendências do Instagram para desenvolvimento.
        
        Returns:
            list: Lista de tendências simuladas
        """
        trends = []
        
        # Data base para simulação
        base_date = datetime.now()
        
        # Simular tendências para hashtags
        for hashtag in self.hashtags:
            # Número de posts simulados
            num_posts = min(3, max(1, hash(hashtag) % 5))
            
            for i in range(num_posts):
                # Gerar data aleatória nos últimos dias
                days_ago = hash(f"{hashtag}_{i}") % self.lookback_days
                post_date = (base_date - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
                
                # Gerar engajamento simulado
                engagement = 100 + (hash(f"{hashtag}_{i}_engagement") % 10000)
                
                # Conteúdo simulado relacionado a dropshipping/franquia
                content_templates = [
                    f"Quer ganhar uma renda extra? Comece agora com #{hashtag}! Sem necessidade de estoque, trabalhe de casa. #empreendedorismo #rendaextra",
                    f"Já pensou em começar seu próprio negócio sem investimento inicial? #{hashtag} é a solução! Veja como eu comecei. #marketingdigital",
                    f"Resultados reais com #{hashtag}! Vendi mais de R$5000 no primeiro mês sem precisar comprar produtos. #dropshipping #liberdadefinanceira",
                    f"Curso completo de #{hashtag} disponível agora. Aprenda como montar seu negócio digital e ganhar em dólar! #cursoonline",
                    f"Como eu consegui renda extra com #{hashtag} trabalhando apenas 3 horas por dia. #trabalheemcasa #rendapassiva"
                ]
                
                content_index = hash(f"{hashtag}_{i}_content") % len(content_templates)
                
                trends.append({
                    'platform': 'instagram',
                    'type': 'hashtag',
                    'term': f"#{hashtag}",
                    'content': content_templates[content_index],
                    'engagement': engagement,
                    'url': f"https://www.instagram.com/p/Simulated_{hashtag}_{i}/",
                    'timestamp': post_date
                })
        
        return trends
    
    def _simulate_twitter_trends(self):
        """
        Gera dados simulados de tendências do Twitter para desenvolvimento.
        
        Returns:
            list: Lista de tendências simuladas
        """
        trends = []
        
        # Data base para simulação
        base_date = datetime.now()
        
        # Simular tweets para keywords e hashtags
        all_terms = self.keywords + ['#' + tag for tag in self.hashtags]
        
        for term in all_terms:
            # Número de tweets simulados
            num_tweets = min(2, max(1, hash(term) % 4))
            
            for i in range(num_tweets):
                # Gerar data aleatória nos últimos dias
                days_ago = hash(f"{term}_{i}") % self.lookback_days
                tweet_date = (base_date - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
                
                # Gerar engajamento simulado
                engagement = 50 + (hash(f"{term}_{i}_engagement") % 5000)
                
                # Nome de usuário simulado
                usernames = ["empreendedor_digital", "dropship_guru", "ganhe_online", "rendaextra", "marketing_dicas", "revenda_facil"]
                username_index = hash(f"{term}_{i}_user") % len(usernames)
                
                # Conteúdo simulado relacionado a dropshipping/franquia
                content_templates = [
                    f"Como iniciei meu negócio de {term} com apenas R$500. Agora faturo 5 dígitos mensais! Quer saber como? Link na bio! #empreendedorismo",
                    f"Guia rápido: {term} em 5 passos simples. Comece hoje mesmo sem precisar de estoque ou investimento alto. #rendaextra",
                    f"{term} é a tendência do momento! Já ajudei mais de 200 alunos a começarem seus negócios online. Quer ser o próximo? #oportunidade",
                    f"Acabei de receber meu pagamento de comissões do mês: R$7.300 com {term}! E você, ainda está perdendo tempo com trabalho CLT? #liberdade",
                    f"ATENÇÃO: O segredo para ter sucesso com {term} que ninguém te conta. Veja o link no meu perfil! #revelado",
                    f"Meu faturamento multiplicou depois que descobri essa estratégia de {term}. Sem enrolação, resultado real! #provas"
                ]
                
                content_index = hash(f"{term}_{i}_content") % len(content_templates)
                
                trends.append({
                    'platform': 'twitter',
                    'type': 'tweet',
                    'term': term,
                    'content': content_templates[content_index],
                    'author': usernames[username_index],
                    'engagement': engagement,
                    'url': f"https://twitter.com/{usernames[username_index]}/status/Simulated_{hash(term + str(i))}",
                    'timestamp': tweet_date
                })
        
        return trends
    
    def _simulate_tiktok_trends(self):
        """
        Gera dados simulados de tendências do TikTok para desenvolvimento.
        
        Returns:
            list: Lista de tendências simuladas
        """
        trends = []
        
        # Data base para simulação
        base_date = datetime.now()
        
        # Simular vídeos para hashtags
        for hashtag in self.hashtags:
            # Número de vídeos simulados
            num_videos = min(2, max(1, hash(hashtag) % 4))
            
            for i in range(num_videos):
                # Gerar data aleatória nos últimos dias
                days_ago = hash(f"{hashtag}_{i}") % self.lookback_days
                video_date = (base_date - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
                
                # Gerar engajamento simulado (TikTok tem engajamento mais alto)
                views = 10000 + (hash(f"{hashtag}_{i}_views") % 1000000)
                likes = int(views * 0.2)
                comments = int(views * 0.01)
                shares = int(views * 0.05)
                engagement = likes + comments + shares
                
                # Nome de usuário simulado
                usernames = ["tiktok_empreendedr", "guru_dropshipping", "renda_online", "marketingdigital", "ganhedinheiro", "dicasbusiness"]
                username_index = hash(f"{hashtag}_{i}_user") % len(usernames)
                
                # Conteúdo simulado relacionado a dropshipping/franquia
                content_templates = [
                    f"Olha quanto eu ganhei esse mês com #{hashtag}! 🤯 Sem precisar comprar produtos! #rendaextra #trabalheemcasa",
                    f"3 produtos que você PRECISA vender em #{hashtag} AGORA! Método sem estoque! #dinheiroonline",
                    f"Passo a passo: Como eu comecei do ZERO com #{hashtag} e hoje faturo mais de 10K por mês! #tutorial",
                    f"Resposta sincera: #{hashtag} vale a pena em 2025? Veja meus resultados reais! #sinceridade",
                    f"Você pode começar seu negócio com apenas R$100! #{hashtag} é a solução! Arrasta pra cima! #oportunidade",
                    f"Como eu trabalho apenas 2 horas por dia e ganho mais que um médico usando #{hashtag}! #liberdade"
                ]
                
                content_index = hash(f"{hashtag}_{i}_content") % len(content_templates)
                
                trends.append({
                    'platform': 'tiktok',
                    'type': 'video',
                    'term': f"#{hashtag}",
                    'content': content_templates[content_index],
                    'author': usernames[username_index],
                    'views': views,
                    'engagement': engagement,
                    'url': f"https://www.tiktok.com/@{usernames[username_index]}/video/Simulated_{hash(hashtag + str(i))}",
                    'timestamp': video_date
                })
        
        return trends
    
    def _filter_relevant_trends(self, df):
        """
        Filtra tendências relevantes para franquias sem estoque.
        
        Args:
            df: DataFrame com todas as tendências
            
        Returns:
            DataFrame: Tendências filtradas
        """
        if df.empty:
            return df
            
        # Palavras-chave para filtragem
        relevant_keywords = [
            'dropshipping', 'revenda', 'sem estoque', 'franquia', 'digital',
            'renda extra', 'comissão', 'afiliado', 'passiva', 'online',
            'automatizado', 'casa', 'próprio negócio', 'empreendedorismo',
            'curso', 'mentoria', 'treinamento'
        ]
        
        # Criar função para verificar relevância
        def is_relevant(row):
            content = str(row['content']).lower()
            term = str(row['term']).lower()
            
            # Verificar conteúdo e termo
            for keyword in relevant_keywords:
                if keyword in content or keyword in term:
                    return True
            
            return False
        
        # Aplicar filtro
        filtered_df = df[df.apply(is_relevant, axis=1)].copy()
        
        # Ordenar por engajamento
        if not filtered_df.empty and 'engagement' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('engagement', ascending=False)
        
        return filtered_df
    
    def get_influential_accounts(self, platform=None, min_followers=1000, limit=10):
        """
        Identifica contas influentes relacionadas a dropshipping/franquias sem estoque.
        
        Args:
            platform: Plataforma específica ou None para todas
            min_followers: Número mínimo de seguidores
            limit: Limite de contas para retornar
            
        Returns:
            pandas.DataFrame: DataFrame com as contas influentes
        """
        # Implementação simulada por enquanto
        return self._simulate_influential_accounts(platform, min_followers, limit)
    
    def _simulate_influential_accounts(self, platform=None, min_followers=1000, limit=10):
        """
        Gera dados simulados de contas influentes para desenvolvimento.
        
        Args:
            platform: Plataforma específica ou None para todas
            min_followers: Número mínimo de seguidores
            limit: Limite de contas para retornar
            
        Returns:
            pandas.DataFrame: DataFrame com as contas influentes simuladas
        """
        accounts = []
        
        platforms = [platform] if platform else self.platforms
        
        # Nomes simulados de influenciadores
        names = [
            "Carlos Empreendedor", "Ana Digital", "Roberto Negócios", 
            "
