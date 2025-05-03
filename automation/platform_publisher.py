# automation/platform_publisher.py
import random
import json
import os
from datetime import datetime, timedelta

class PlatformPublisher:
    """
    Classe responsável por publicar campanhas automaticamente em diferentes plataformas
    """
    
    def __init__(self, api_keys=None, platform_settings=None):
        """
        Inicializa o publicador de plataformas
        
        Args:
            api_keys (dict): Chaves de API para as diferentes plataformas
            platform_settings (dict): Configurações específicas para cada plataforma
        """
        self.api_keys = api_keys or {}
        self.platform_settings = platform_settings or {}
        
        # Status possíveis para publicações
        self.status_options = ['Pending', 'Scheduled', 'Active', 'Paused', 'Completed', 'Failed']
        
        # Dicionário de códigos de erro comuns por plataforma
        self.error_codes = {
            'facebook': {
                1001: 'API authorization failed',
                1002: 'Ad account not found',
                1003: 'Budget too low',
                1004: 'Invalid creative format',
                1005: 'Targeting too narrow'
            },
            'google_ads': {
                2001: 'Invalid API credentials',
                2002: 'Payment method declined',
                2003: 'Daily budget below minimum',
                2004: 'Ad disapproved',
                2005: 'Landing page issue'
            },
            'linkedin': {
                3001: 'Authentication failed',
                3002: 'Insufficient account permissions',
                3003: 'Invalid creative format',
                3004: 'Targeting criteria too narrow',
                3005: 'Character limit exceeded'
            },
            'email': {
                4001: 'SMTP authentication failed',
                4002: 'Email template not found',
                4003: 'Daily sending limit reached',
                4004: 'Invalid receiver email',
                4005: 'Content flagged as spam'
            }
        }
    
    def publish(self, campaigns):
        """
        Publica campanhas nas plataformas configuradas
        
        Args:
            campaigns (list): Lista de campanhas a serem publicadas
            
        Returns:
            dict: Resultados da publicação
        """
        print("PlatformPublisher: Iniciando publicação de campanhas em diferentes plataformas")
        
        # Inicializar resultados
        publication_results = {
            'summary': {
                'total_campaigns': len(campaigns),
                'successful': 0,
                'pending': 0,
                'failed': 0,
                'platforms': {}
            },
            'campaigns': []
        }
        
        # Processar cada campanha
        for campaign in campaigns:
            campaign_name = campaign.get('name', 'Campanha sem nome')
            platforms = campaign.get('platforms', [])
            
            print(f"Publicando: {campaign_name} nas plataformas: {', '.join(platforms)}")
            
            # Resultados para esta campanha
            campaign_result = {
                'campaign_name': campaign_name,
                'objective': campaign.get('objective', 'Not specified'),
                'platforms': {},
                'overall_status': 'Pending',
                'publication_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Publicar em cada plataforma
            at_least_one_success = False
            at_least_one_failure = False
            
            for platform in platforms:
                platform_result = self._publish_to_platform(platform, campaign)
                campaign_result['platforms'][platform] = platform_result
                
                # Atualizar estatísticas da plataforma
                if platform not in publication_results['summary']['platforms']:
                    publication_results['summary']['platforms'][platform] = {
                        'total': 0,
                        'successful': 0,
                        'pending': 0,
                        'failed': 0
                    }
                
                publication_results['summary']['platforms'][platform]['total'] += 1
                
                # Atualizar contadores baseado no status
                status = platform_result.get('status', 'Pending')
                if status == 'Active' or status == 'Scheduled':
                    publication_results['summary']['platforms'][platform]['successful'] += 1
                    at_least_one_success = True
                elif status == 'Failed':
                    publication_results['summary']['platforms'][platform]['failed'] += 1
                    at_least_one_failure = True
                else:
                    publication_results['summary']['platforms'][platform]['pending'] += 1
            
            # Determinar status geral da campanha
            if at_least_one_failure and not at_least_one_success:
                campaign_result['overall_status'] = 'Failed'
                publication_results['summary']['failed'] += 1
            elif at_least_one_success and not at_least_one_failure:
                campaign_result['overall_status'] = 'Active'
                publication_results['summary']['successful'] += 1
            elif at_least_one_success and at_least_one_failure:
                campaign_result['overall_status'] = 'Partial'
                publication_results['summary']['successful'] += 1
            else:
                campaign_result['overall_status'] = 'Pending'
                publication_results['summary']['pending'] += 1
            
            # Adicionar resultado da campanha à lista
            publication_results['campaigns'].append(campaign_result)
        
        # Salvar resultados (opcional)
        self._save_publication_results(publication_results)
        
        return publication_results
    
    def _publish_to_platform(self, platform, campaign):
        """Publica uma campanha em uma plataforma específica"""
        
        # Verificar se temos a chave de API para esta plataforma
        if platform.lower() not in self.api_keys and platform.lower() != 'email' and platform.lower() != 'whatsapp':
            print(f"Erro: Chave de API não encontrada para a plataforma {platform}")
            return {
                'status': 'Failed',
                'platform_id': None,
                'error': 'API key not found',
                'error_code': None,
                'publication_date': None,
                'expiration_date': None,
                'notes': 'Missing API configuration'
            }
        
        # Inicializar resultado da publicação
        result = {
            'status': 'Pending',
            'platform_id': None,
            'error': None,
            'error_code': None,
            'publication_date': None,
            'expiration_date': None,
            'notes': None,
            'platform_specific': {}
        }
        
        # Simular um resultado de publicação (sucesso/falha aleatória)
        success = random.random() < 0.9  # 90% de chance de sucesso
        
        if success:
            # Gerar ID de plataforma
            platform_id = f"{platform.lower()}_{campaign.get('objective', 'campaign')}_{random.randint(10000, 99999)}"
            
            # Data de publicação (agora ou data agendada)
            if 'start_date' in campaign:
                publication_date = datetime.strptime(campaign['start_date'], '%Y-%m-%d')
            else:
                publication_date = datetime.now()
            
            # Data de expiração (se houver end_date ou duração fixa)
            if 'end_date' in campaign:
                expiration_date = datetime.strptime(campaign['end_date'], '%Y-%m-%d')
            else:
                # Duração padrão de 30 dias
                expiration_date = publication_date + timedelta(days=30)
            
            # Status da campanha (Scheduled ou Active)
            if publication_date > datetime.now():
                status = 'Scheduled'
            else:
                status = 'Active'
            
            # Informações específicas da plataforma
            platform_specific = self._get_platform_specific_data(platform, campaign)
            
            # Atualizar resultado
            result.update({
                'status': status,
                'platform_id': platform_id,
                'publication_date': publication_date.strftime('%Y-%m-%d %H:%M:%S'),
                'expiration_date': expiration_date.strftime('%Y-%m-%d %H:%M:%S'),
                'notes': f"Successfully published to {platform}",
                'platform_specific': platform_specific
            })
            
        else:
            # Simular um erro
            error_code = self._get_random_error_code(platform)
            error_message = self.error_codes.get(platform.lower(), {}).get(error_code, 'Unknown error')
            
            # Atualizar resultado
            result.update({
                'status': 'Failed',
                'error': error_message,
                'error_code': error_code,
                'notes': f"Failed to publish to {platform}: {error_message}"
            })
        
        return result
    
    def _get_random_error_code(self, platform):
        """Obtém um código de erro aleatório para uma plataforma"""
        
        platform_key = platform.lower()
        
        # Mapear plataformas para chaves do dicionário error_codes
        if platform_key in ['facebook', 'instagram']:
            platform_key = 'facebook'
        elif platform_key in ['google_search', 'google_display', 'google_ads']:
            platform_key = 'google_ads'
        
        # Obter códigos de erro para a plataforma
        error_codes = list(self.error_codes.get(platform_key, {1: 'Unknown error'}).keys())
        
        return random.choice(error_codes)
    
    def _get_platform_specific_data(self, platform, campaign):
        """Obtém dados específicos de cada plataforma"""
        
        platform_data = {}
        
        if platform.lower() in ['facebook', 'instagram']:
            platform_data = {
                'account_id': f"act_{random.randint(100000000, 999999999)}",
                'campaign_id': f"{random.randint(1000000000, 9999999999)}",
                'ad_set_ids': [f"{random.randint(1000000000, 9999999999)}" for _ in range(3)],
                'ad_ids': [f"{random.randint(1000000000, 9999999999)}" for _ in range(5)],
                'preview_url': f"https://www.facebook.com/ads/library/?id={random.randint(1000000000, 9999999999)}",
                'delivery_insights': {
                    'frequency': round(random.uniform(1.2, 3.5), 2),
                    'reach': random.randint(5000, 30000),
                    'relevance_score': random.randint(6, 10)
                }
            }
        elif platform.lower() in ['google_search', 'google_display', 'google_ads']:
            platform_data = {
                'customer_id': f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                'campaign_id': f"{random.randint(1000000000, 9999999999)}",
                'ad_group_ids': [f"{random.randint(1000000000, 9999999999)}" for _ in range(2)],
                'ad_ids': [f"{random.randint(1000000000, 9999999999)}" for _ in range(4)],
                'quality_score': random.randint(5, 10),
                'preview_url': f"https://ads.google.com/aw/overview?campaignId={random.randint(1000000000, 9999999999)}"
            }
        elif platform.lower() == 'linkedin':
            platform_data = {
                'account_id': f"{random.randint(100000, 999999)}",
                'campaign_id': f"{random.randint(100000, 999999)}",
                'creative_ids': [f"{random.randint(100000, 999999)}" for _ in range(3)],
                'preview_url': f"https://www.linkedin.com/ad-preview/{random.randint(100000, 999999)}",
                'campaign_group_id': f"{random.randint(100000, 999999)}"
            }
        elif platform.lower() == 'email':
            platform_data = {
                'template_id': f"template_{random.randint(1000, 9999)}",
                'list_id': f"list_{random.randint(1000, 9999)}",
                'sender_name': 'Equipe de Franquias',
                'sender_email': 'franquias@exemplo.com.br',
                'subject_line': campaign.get('name', 'Oportunidade de Franquia'),
                'estimated_audience': random.randint(2000, 10000)
            }
        elif platform.lower() == 'whatsapp':
            platform_data = {
                'template_id': f"waba_{random.randint(1000, 9999)}",
                'phone_number_id': f"{random.randint(100000000000, 999999999999)}",
                'namespace': f"namespace_{random.randint(10000, 99999)}",
                'language': 'pt_BR',
                'template_name': campaign.get('objective', 'default').lower().replace(' ', '_'),
                'estimated_audience': random.randint(500, 3000)
            }
        
        return platform_data
    
    def _save_publication_results(self, results):
        """Salva os resultados da publicação (opcional)"""
        
        # Diretório para salvar resultados
        base_dir = os.path.join('output', 'automation')
        
        # Verificar se o diretório existe, se não, criar
        try:
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
                print(f"Diretório criado: {base_dir}")
            
            # Nome do arquivo baseado na data
            filename = f"publication_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path = os.path.join(base_dir, filename)
            
            # Salvar resultados em JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
                
            print(f"Resultados de publicação salvos em: {file_path}")
            
        except Exception as e:
            print(f"Erro ao salvar resultados de publicação: {e}")
