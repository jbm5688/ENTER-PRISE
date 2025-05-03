import logging
import random
from datetime import datetime, timedelta

logger = logging.getLogger("franquia_finder")

class CampaignScheduler:
    """
    Classe responsável por criar planos de campanhas de marketing.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o agendador de campanhas.
        
        Args:
            config (dict): Configurações para agendamento de campanhas
        """
        self.config = config or {}
        self.platforms = self.config.get('active_platforms', ["facebook", "instagram", "google", "linkedin", "email"])
    
    def create_campaign_plan(self, opportunity, platform_content):
        """
        Cria um plano de campanhas para uma oportunidade.
        
        Args:
            opportunity (dict): Dados da oportunidade
            platform_content (dict): Conteúdo adaptado para plataformas
            
        Returns:
            dict: Plano de campanhas
        """
        print(f"CampaignScheduler: Agendando campanhas para {opportunity.get('name', 'Oportunidade')}")
        
        # Extrair informações relevantes
        opportunity_name = opportunity.get('name', '')
        category = opportunity.get('category', '')
        
        # Data atual para referência
        now = datetime.now()
        
        # Gerar plano de campanhas
        campaign_plan = {
            'opportunity_name': opportunity_name,
            'category': category,
            'start_date': now.strftime('%Y-%m-%d'),
            'end_date': (now + timedelta(days=90)).strftime('%Y-%m-%d'),
            'campaigns': [],
            'budget_allocation': {},
            'timeline': [],
            'kpis': self._generate_kpis(),
            'created_at': now.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Gerar campanhas para cada plataforma ativa
        for platform in self.platforms:
            if platform in platform_content:
                campaigns = self._generate_platform_campaigns(
                    platform,
                    platform_content[platform],
                    opportunity_name,
                    category,
                    now
                )
                
                campaign_plan['campaigns'].extend(campaigns)
        
        # Distribuir orçamento entre plataformas
        campaign_plan['budget_allocation'] = self._allocate_budget(self.platforms)
        
        # Criar timeline de atividades
        campaign_plan['timeline'] = self._create_timeline(campaign_plan['campaigns'], now)
        
        return campaign_plan
    
    def _generate_platform_campaigns(self, platform, content, name, category, start_date):
        """
        Gera campanhas para uma plataforma específica.
        
        Args:
            platform (str): Nome da plataforma
            content (dict): Conteúdo adaptado para a plataforma
            name (str): Nome da oportunidade
            category (str): Categoria do negócio
            start_date (datetime): Data de início
            
        Returns:
            list: Campanhas para a plataforma
        """
        campaigns = []
        
        # Gerar campanhas baseadas na plataforma
        if platform == "facebook" or platform == "instagram":
            # Campanha de conscientização
            campaigns.append({
                'name': f"Awareness - {name} ({platform.capitalize()})",
                'platform': platform,
                'objective': 'Brand Awareness',
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': (start_date + timedelta(days=30)).strftime('%Y-%m-%d'),
                'budget': round(random.uniform(1000, 3000), 2),
                'target_audience': "Empreendedores interessados em franquias",
                'content_type': 'Imagem/Vídeo',
                'main_message': f"Conheça a franquia {name}"
            })
            
            # Campanha de consideração
            campaigns.append({
                'name': f"Consideration - {name} ({platform.capitalize()})",
                'platform': platform,
                'objective': 'Website Traffic',
                'start_date': (start_date + timedelta(days=10)).strftime('%Y-%m-%d'),
                'end_date': (start_date + timedelta(days=40)).strftime('%Y-%m-%d'),
                'budget': round(random.uniform(1500, 3500), 2),
                'target_audience': "Pessoas interessadas em empreendedorismo e franquias",
                'content_type': 'Carrossel',
                'main_message': f"Vantagens da franquia {name}"
            })
            
            # Campanha de conversão
            campaigns.append({
                'name': f"Conversion - {name} ({platform.capitalize()})",
                'platform': platform,
                'objective': 'Lead Generation',
                'start_date': (start_date + timedelta(days=20)).strftime('%Y-%m-%d'),
                'end_date': (start_date + timedelta(days=50)).strftime('%Y-%m-%d'),
                'budget': round(random.uniform(2000, 4000), 2),
                'target_audience': "Empreendedores com intenção de investir",
                'content_type': 'Formulário de Lead',
                'main_message': f"Torne-se um franqueado {name}"
            })
        
        elif platform == "google":
            # Campanha de pesquisa
            campaigns.append({
                'name': f"Search - {name} (Google)",
                'platform': 'google',
                'objective': 'Lead Generation',
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': (start_date + timedelta(days=60)).strftime('%Y-%m-%d'),
                'budget': round(random.uniform(2000, 4000), 2),
                'target_audience': "Pessoas buscando por franquias",
                'content_type': 'Anúncios de texto',
                'main_message': f"Franquia {name} - {category}"
            })
            
            # Campanha de display
            campaigns.append({
                'name': f"Display - {name} (Google)",
                'platform': 'google',
                'objective': 'Brand Awareness',
                'start_date': (start_date + timedelta(days=5)).strftime('%Y-%m-%d'),
                'end_date': (start_date + timedelta(days=35)).strftime('%Y-%m-%d'),
                'budget': round(random.uniform(1000, 3000), 2),
                'target_audience': "Empreendedores e investidores",
                'content_type': 'Banners',
                'main_message': f"Invista na franquia {name}"
            })
        
        elif platform == "linkedin":
            # Campanha de alcance
            campaigns.append({
                'name': f"Reach - {name} (LinkedIn)",
                'platform': 'linkedin',
                'objective': 'Brand Awareness',
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': (start_date + timedelta(days=30)).strftime('%Y-%m-%d'),
                'budget': round(random.uniform(1500, 3500), 2),
                'target_audience': "Profissionais de negócios e investidores",
                'content_type': 'Sponsored Content',
                'main_message': f"Oportunidade de franquia: {name}"
            })
            
            # Campanha de geração de leads
            campaigns.append({
                'name': f"Leads - {name} (LinkedIn)",
                'platform': 'linkedin',
                'objective': 'Lead Generation',
                'start_date': (start_date + timedelta(days=15)).strftime('%Y-%m-%d'),
                'end_date': (start_date + timedelta(days=45)).strftime('%Y-%m-%d'),
                'budget': round(random.uniform(2000, 4000), 2),
                'target_audience': "Executivos e empreendedores",
                'content_type': 'Lead Gen Forms',
                'main_message': f"Seja um franqueado {name}"
            })
        
        elif platform == "email":
            # Campanha de email
            campaigns.append({
                'name': f"Nurture - {name} (Email)",
                'platform': 'email',
                'objective': 'Nurturing',
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': (start_date + timedelta(days=30)).strftime('%Y-%m-%d'),
                'budget': round(random.uniform(500, 1500), 2),
                'target_audience': "Leads captados",
                'content_type': 'Sequência de emails',
                'main_message': f"Conheça a franquia {name}"
            })
        
        return campaigns
    
    def _allocate_budget(self, platforms):
        """
        Aloca orçamento entre plataformas.
        
        Args:
            platforms (list): Lista de plataformas ativas
            
        Returns:
            dict: Alocação de orçamento
        """
        # Alocações padrão
        default_allocations = {
            'facebook': 0.25,
            'instagram': 0.20,
            'google': 0.30,
            'linkedin': 0.15,
            'email': 0.10
        }
        
        # Filtrar apenas plataformas ativas
        budget_allocation = {}
        
        # Calcular total da alocação padrão
        total_allocation = sum(default_allocations.get(p, 0) for p in platforms)
        
        # Normalizar alocações
        for platform in platforms:
            if platform in default_allocations:
                normalized_allocation = default_allocations[platform] / total_allocation
                budget_allocation[platform] = round(normalized_allocation, 2)
        
        return budget_allocation
    
    def _create_timeline(self, campaigns, start_date):
        """
        Cria timeline de atividades para o plano de campanhas.
        
        Args:
            campaigns (list): Lista de campanhas
            start_date (datetime): Data de início
            
        Returns:
            list: Timeline de atividades
        """
        timeline = []
        
        # Atividades de preparação
        timeline.append({
            'phase': 'Preparação',
            'activity': 'Definição de estratégia e objetivos',
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': (start_date + timedelta(days=3)).strftime('%Y-%m-%d'),
            'status': 'Planejado'
        })
        
        timeline.append({
            'phase': 'Preparação',
            'activity': 'Criação de materiais de campanha',
            'start_date': (start_date + timedelta(days=3)).strftime('%Y-%m-%d'),
            'end_date': (start_date + timedelta(days=10)).strftime('%Y-%m-%d'),
            'status': 'Planejado'
        })
        
        # Atividades de lançamento
        timeline.append({
            'phase': 'Lançamento',
            'activity': 'Início das campanhas de brand awareness',
            'start_date': (start_date + timedelta(days=10)).strftime('%Y-%m-%d'),
            'end_date': (start_date + timedelta(days=11)).strftime('%Y-%m-%d'),
            'status': 'Planejado'
        })
        
        # Atividades de otimização
        timeline.append({
            'phase': 'Otimização',
            'activity': 'Primeira análise de desempenho',
            'start_date': (start_date + timedelta(days=20)).strftime('%Y-%m-%d'),
            'end_date': (start_date + timedelta(days=21)).strftime('%Y-%m-%d'),
            'status': 'Planejado'
        })
        
        timeline.append({
            'phase': 'Otimização',
            'activity': 'Ajustes de segmentação e orçamento',
            'start_date': (start_date + timedelta(days=21)).strftime('%Y-%m-%d'),
            'end_date': (start_date + timedelta(days=23)).strftime('%Y-%m-%d'),
            'status': 'Planejado'
        })
        
        # Atividades de escala
        timeline.append({
            'phase': 'Escala',
            'activity': 'Ampliação das campanhas de melhor desempenho',
            'start_date': (start_date + timedelta(days=30)).strftime('%Y-%m-%d'),
            'end_date': (start_date + timedelta(days=35)).strftime('%Y-%m-%d'),
            'status': 'Planejado'
        })
        
        # Atividades de relatório
        timeline.append({
            'phase': 'Relatório',
            'activity': 'Análise final de resultados',
            'start_date': (start_date + timedelta(days=60)).strftime('%Y-%m-%d'),
            'end_date': (start_date + timedelta(days=62)).strftime('%Y-%m-%d'),
            'status': 'Planejado'
        })
        
        return timeline
    
    def _generate_kpis(self):
        """
        Gera KPIs para monitoramento de campanhas.
        
        Returns:
            dict: KPIs por plataforma
        """
        kpis = {
            'facebook': {
                'reach': {
                    'description': 'Alcance das campanhas',
                    'target': 'Pelo menos 50.000 pessoas alcançadas'
                },
                'engagement': {
                    'description': 'Taxa de engajamento',
                    'target': 'Taxa de engajamento média de 3%'
                },
                'leads': {
                    'description': 'Geração de leads',
                    'target': '150 leads qualificados'
                }
            },
            'instagram': {
                'reach': {
                    'description': 'Alcance das campanhas',
                    'target': 'Pelo menos 40.000 pessoas alcançadas'
                },
                'engagement': {
                    'description': 'Taxa de engajamento',
                    'target': 'Taxa de engajamento média de 4%'
                },
                'leads': {
                    'description': 'Geração de leads',
                    'target': '100 leads qualificados'
                }
            },
            'google': {
                'impressions': {
                    'description': 'Impressões de anúncios',
                    'target': 'Pelo menos 100.000 impressões'
                },
                'clicks': {
                    'description': 'Cliques em anúncios',
                    'target': '5.000 cliques'
                },
                'conversions': {
                    'description': 'Conversões',
                    'target': '200 conversões'
                }
            },
            'linkedin': {
                'impressions': {
                    'description': 'Impressões de anúncios',
                    'target': 'Pelo menos 30.000 impressões'
                },
                'clicks': {
                    'description': 'Cliques em anúncios',
                    'target': '1.500 cliques'
                },
                'leads': {
                    'description': 'Geração de leads',
                    'target': '80 leads qualificados'
                }
            },
            'email': {
                'open_rate': {
                    'description': 'Taxa de abertura',
                    'target': 'Taxa de abertura média de 25%'
                },
                'click_rate': {
                    'description': 'Taxa de clique',
                    'target': 'Taxa de clique média de 4%'
                },
                'conversions': {
                    'description': 'Conversões',
                    'target': '50 conversões'
                }
            }
        }
        
        return kpis
