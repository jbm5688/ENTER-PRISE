# automation/performance_tracker.py
import random
import json
import os
from datetime import datetime, timedelta

class PerformanceTracker:
    """
    Classe responsável por monitorar e rastrear o desempenho das campanhas
    """
    
    def __init__(self, api_keys=None):
        """
        Inicializa o rastreador de desempenho
        
        Args:
            api_keys (dict): Chaves de API para as diferentes plataformas
        """
        self.api_keys = api_keys or {}
        
        # Métricas que serão monitoradas por plataforma
        self.tracked_metrics = {
            'facebook': [
                'impressions', 'reach', 'frequency', 'clicks', 'ctr', 'cpc', 
                'spend', 'leads', 'cpl', 'landing_page_views', 'video_views'
            ],
            'instagram': [
                'impressions', 'reach', 'frequency', 'clicks', 'ctr', 'cpc', 
                'spend', 'leads', 'cpl', 'profile_visits', 'story_replies'
            ],
            'google_search': [
                'impressions', 'clicks', 'ctr', 'cpc', 'spend', 'conversions', 
                'conversion_rate', 'cpa', 'average_position', 'quality_score'
            ],
            'google_display': [
                'impressions', 'clicks', 'ctr', 'cpc', 'spend', 'conversions', 
                'conversion_rate', 'cpa', 'viewability_rate', 'video_completion_rate'
            ],
            'linkedin': [
                'impressions', 'clicks', 'ctr', 'cpc', 'spend', 'leads', 
                'cpl', 'opens', 'form_completion_rate', 'engagement_rate'
            ],
            'email': [
                'sends', 'opens', 'open_rate', 'clicks', 'click_rate', 
                'ctr', 'bounces', 'bounce_rate', 'unsubscribes', 'conversions'
            ],
            'whatsapp': [
                'messages_sent', 'delivered', 'delivery_rate', 'opens', 
                'open_rate', 'replies', 'reply_rate', 'blocks', 'conversions'
            ]
        }
        
        # Benchmarks para cada métrica por plataforma
        self.benchmarks = {
            'facebook': {
                'ctr': {'min': 0.8, 'avg': 1.5, 'max': 3.0},
                'cpc': {'min': 0.5, 'avg': 1.2, 'max': 3.0},
                'cpl': {'min': 20, 'avg': 80, 'max': 150}
            },
            'instagram': {
                'ctr': {'min': 0.6, 'avg': 1.2, 'max': 2.5},
                'cpc': {'min': 0.7, 'avg': 1.8, 'max': 3.5},
                'cpl': {'min': 25, 'avg': 100, 'max': 180}
            },
            'google_search': {
                'ctr': {'min': 3.0, 'avg': 5.5, 'max': 8.0},
                'cpc': {'min': 1.5, 'avg': 3.5, 'max': 8.0},
                'conversion_rate': {'min': 2.0, 'avg': 5.0, 'max': 10.0}
            },
            'google_display': {
                'ctr': {'min': 0.2, 'avg': 0.5, 'max': 1.0},
                'cpc': {'min': 0.3, 'avg': 0.8, 'max': 2.0},
                'conversion_rate': {'min': 0.5, 'avg': 1.5, 'max': 3.0}
            },
            'linkedin': {
                'ctr': {'min': 0.4, 'avg': 0.6, 'max': 1.0},
                'cpc': {'min': 5.0, 'avg': 8.0, 'max': 15.0},
                'cpl': {'min': 50, 'avg': 150, 'max': 300}
            },
            'email': {
                'open_rate': {'min': 15, 'avg': 25, 'max': 40},
                'click_rate': {'min': 2, 'avg': 4, 'max': 8},
                'conversion_rate': {'min': 0.5, 'avg': 2, 'max': 5}
            },
            'whatsapp': {
                'open_rate': {'min': 70, 'avg': 85, 'max': 95},
                'reply_rate': {'min': 15, 'avg': 30, 'max': 50},
                'conversion_rate': {'min': 2, 'avg': 5, 'max': 10}
            }
        }
    
    def setup_tracking(self, publication_results):
        """
        Configura o rastreamento de desempenho para campanhas publicadas
        
        Args:
            publication_results (dict): Resultados da publicação de campanhas
            
        Returns:
            dict: Configuração de rastreamento e projeções iniciais
        """
        print("PerformanceTracker: Configurando rastreamento de desempenho das campanhas")
        
        # Inicializar resultados de rastreamento
        tracking_setup = {
            'setup_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'campaigns': [],
            'automated_reports': self._setup_automated_reports(),
            'alerts': self._setup_performance_alerts(),
            'performance_projection': {}
        }
        
        # Configurar rastreamento para cada campanha publicada com sucesso
        for campaign_result in publication_results.get('campaigns', []):
            campaign_name = campaign_result.get('campaign_name', 'Unnamed Campaign')
            
            # Pular campanhas que falharam completamente
            if campaign_result.get('overall_status') == 'Failed':
                continue
            
            # Dados de rastreamento para esta campanha
            campaign_tracking = {
                'campaign_name': campaign_name,
                'tracking_id': f"tr_{random.randint(10000, 99999)}",
                'objective': campaign_result.get('objective', 'Not specified'),
                'platforms': {},
                'utm_parameters': self._generate_utm_parameters(campaign_name),
                'conversion_tracking': self._setup_conversion_tracking(campaign_name),
                'initial_metrics': {}
            }
            
            # Configurar rastreamento para cada plataforma
            for platform, platform_result in campaign_result.get('platforms', {}).items():
                # Pular plataformas que falharam
                if platform_result.get('status') == 'Failed':
                    continue
                
                # Dados de rastreamento para esta plataforma
                platform_tracking = {
                    'platform_id': platform_result.get('platform_id', 'Unknown'),
                    'tracking_status': 'Active',
                    'metrics_to_track': self.tracked_metrics.get(platform.lower(), []),
                    'tracking_pixel': self._generate_tracking_pixel(platform, campaign_name),
                    'platform_specific': platform_result.get('platform_specific', {})
                }
                
                # Métricas iniciais (zero)
                initial_metrics = {}
                for metric in platform_tracking['metrics_to_track']:
                    initial_metrics[metric] = 0
                
                platform_tracking['initial_metrics'] = initial_metrics
                
                # Adicionar rastreamento da plataforma
                campaign_tracking['platforms'][platform] = platform_tracking
            
            # Simular métricas iniciais (primeiro dia)
            campaign_tracking['initial_metrics'] = self._simulate_initial_metrics(campaign_tracking)
            
            # Adicionar rastreamento da campanha
            tracking_setup['campaigns'].append(campaign_tracking)
        
        # Criar projeção de desempenho para o período completo
        tracking_setup['performance_projection'] = self._project_performance(tracking_setup['campaigns'])
        
        # Salvar configuração (opcional)
        self._save_tracking_setup(tracking_setup)
        
        return tracking_setup
    
    def _generate_utm_parameters(self, campaign_name):
        """Gera parâmetros UTM para rastreamento"""
        
        # Remover espaços e caracteres especiais
        campaign_name_clean = campaign_name.lower().replace(' ', '_').replace('-', '_')
        
        utms = {
            'utm_source': 'franquia_finder',
            'utm_medium': 'franchise_marketing',
            'utm_campaign': campaign_name_clean,
            'utm_content': '{platform}_{ad_type}',
            'utm_term': '{keyword}'
        }
        
        return utms
    
    def _setup_conversion_tracking(self, campaign_name):
        """Configura o rastreamento de conversões"""
        
        # Eventos de conversão a serem rastreados
        events = [
            {
                'event_name': 'form_submission',
                'event_id': f"ev_form_{random.randint(1000, 9999)}",
                'tracking_method': 'pixel',
                'value': 10
            },
            {
                'event_name': 'call_request',
                'event_id': f"ev_call_{random.randint(1000, 9999)}",
                'tracking_method': 'gtm',
                'value': 20
            },
            {
                'event_name': 'download_material',
                'event_id': f"ev_download_{random.randint(1000, 9999)}",
                'tracking_method': 'gtm',
                'value': 5
            },
            {
                'event_name': 'meeting_scheduled',
                'event_id': f"ev_meeting_{random.randint(1000, 9999)}",
                'tracking_method': 'crm',
                'value': 30
            },
            {
                'event_name': 'contract_signed',
                'event_id': f"ev_contract_{random.randint(1000, 9999)}",
                'tracking_method': 'crm',
                'value': 100
            }
        ]
        
        # Código de exemplo para implementação (JavaScript)
        javascript_code = """
// Rastreamento de conversão no site
function trackConversion(eventName, value) {
    // Enviar evento para o Google Analytics
    gtag('event', eventName, {
        'event_category': 'conversion',
        'event_label': 'franchise_lead',
        'value': value
    });
    
    // Enviar evento para o Facebook Pixel
    fbq('track', eventName, {
        value: value,
        currency: 'BRL'
    });
    
    // Enviar evento para o LinkedIn Insight Tag
    window.lintrk('track', {
        conversion_id: LINKEDIN_CONVERSION_ID,
        custom_value: value
    });
    
    console.log('Conversion tracked:', eventName, value);
}

// Exemplo de uso:
// trackConversion('form_submission', 10);
        """
        
        return {
            'events': events,
            'implementation_code': javascript_code,
            'tracking_status': 'Active',
            'conversion_attribution_window': '30 days'
        }
    
    def _generate_tracking_pixel(self, platform, campaign_name):
        """Gera pixel de rastreamento para a plataforma"""
        
        pixel = {}
        
        if platform.lower() in ['facebook', 'instagram']:
            pixel = {
                'type': 'Facebook Pixel',
                'id': f"{random.randint(100000000000000, 999999999999999)}",
                'events': ['PageView', 'Lead', 'CompleteRegistration'],
                'implementation_status': 'Active'
            }
        elif platform.lower() in ['google_search', 'google_display']:
            pixel = {
                'type': 'Google Tag',
                'id': f"G-{random.randint(10000000, 99999999)}",
                'events': ['page_view', 'generate_lead', 'sign_up'],
                'implementation_status': 'Active'
            }
        elif platform.lower() == 'linkedin':
            pixel = {
                'type': 'LinkedIn Insight Tag',
                'id': f"{random.randint(1000000, 9999999)}",
                'events': ['Lead', 'Registration'],
                'implementation_status': 'Active'
            }
        elif platform.lower() == 'email':
            pixel = {
                'type': 'Email Tracking',
                'id': f"em_{random.randint(10000, 99999)}",
                'events': ['Open', 'Click', 'Conversion'],
                'implementation_status': 'Active'
            }
        elif platform.lower() == 'whatsapp':
            pixel = {
                'type': 'WhatsApp Tracking',
                'id': f"wa_{random.randint(10000, 99999)}",
                'events': ['Delivered', 'Read', 'Reply'],
                'implementation_status': 'Active'
            }
        
        return pixel
    
    def _setup_automated_reports(self):
        """Configura relatórios automatizados"""
        
        reports = [
            {
                'name': 'Daily Performance Report',
                'frequency': 'Daily',
                'time': '08:00',
                'metrics': ['impressions', 'clicks', 'ctr', 'spend', 'leads', 'cpl'],
                'recipients': ['marketing@example.com', 'franquias@example.com'],
                'format': 'Email',
                'compare_to': 'Previous Day'
            },
            {
                'name': 'Weekly Campaign Summary',
                'frequency': 'Weekly',
                'day': 'Monday',
                'time': '09:00',
                'metrics': ['impressions', 'clicks', 'ctr', 'spend', 'leads', 'cpl', 'conversion_rate'],
                'recipients': ['marketing@example.com', 'franquias@example.com', 'director@example.com'],
                'format': 'Email + PDF',
                'compare_to': 'Previous Week'
            },
            {
                'name': 'Monthly Performance Review',
                'frequency': 'Monthly',
                'day': 1,
                'time': '10:00',
                'metrics': ['impressions', 'clicks', 'ctr', 'spend', 'leads', 'cpl', 'conversion_rate', 'roi'],
                'recipients': ['marketing@example.com', 'franquias@example.com', 'director@example.com', 'ceo@example.com'],
                'format': 'Email + PDF + Presentation',
                'compare_to': 'Previous Month, Target'
            }
        ]
        
        return reports
    
    def _setup_performance_alerts(self):
        """Configura alertas de desempenho"""
        
        alerts = [
            {
                'name': 'High CPC Alert',
                'condition': 'cpc > benchmark_avg * 1.5',
                'platforms': ['facebook', 'instagram', 'google_search', 'linkedin'],
                'check_frequency': 'Daily',
                'notification_method': 'Email',
                'recipients': ['marketing@example.com'],
                'severity': 'Medium'
            },
            {
                'name': 'Low CTR Alert',
                'condition': 'ctr < benchmark_min',
                'platforms': ['facebook', 'instagram', 'google_search', 'google_display', 'linkedin'],
                'check_frequency': 'Daily',
                'notification_method': 'Email + SMS',
                'recipients': ['marketing@example.com'],
                'severity': 'High'
            },
            {
                'name': 'High CPL Alert',
                'condition': 'cpl > benchmark_avg * 2',
                'platforms': ['facebook', 'instagram', 'google_search', 'linkedin'],
                'check_frequency': 'Daily',
                'notification_method': 'Email + SMS',
                'recipients': ['marketing@example.com', 'director@example.com'],
                'severity': 'Critical'
            },
            {
                # automation/performance_tracker.py (continuação)
                'name': 'Budget Depletion Alert',
                'condition': 'spend > daily_budget * 0.8',
                'platforms': ['facebook', 'instagram', 'google_search', 'google_display', 'linkedin'],
                'check_frequency': 'Hourly',
                'notification_method': 'Email + SMS',
                'recipients': ['marketing@example.com'],
                'severity': 'High'
            },
            {
                'name': 'Lead Volume Drop Alert',
                'condition': 'daily_leads < previous_day_leads * 0.7',
                'platforms': ['all'],
                'check_frequency': 'Daily',
                'notification_method': 'Email',
                'recipients': ['marketing@example.com', 'director@example.com'],
                'severity': 'Medium'
            }
        ]
        
        return alerts
    
    def _simulate_initial_metrics(self, campaign_tracking):
        """Simula métricas iniciais para o primeiro dia"""
        
        # Métricas consolidadas
        initial_metrics = {
            'impressions': 0,
            'clicks': 0,
            'spend': 0,
            'leads': 0
        }
        
        # Somar métricas de todas as plataformas
        for platform, platform_data in campaign_tracking.get('platforms', {}).items():
            platform_metrics = self._simulate_platform_metrics(platform, campaign_tracking.get('objective', ''))
            
            # Adicionar métricas da plataforma
            for metric, value in platform_metrics.items():
                if metric in initial_metrics:
                    initial_metrics[metric] += value
                else:
                    initial_metrics[metric] = value
        
        # Calcular métricas derivadas
        if initial_metrics['impressions'] > 0:
            initial_metrics['ctr'] = (initial_metrics['clicks'] / initial_metrics['impressions']) * 100
        else:
            initial_metrics['ctr'] = 0
            
        if initial_metrics['clicks'] > 0:
            initial_metrics['cpc'] = initial_metrics['spend'] / initial_metrics['clicks']
        else:
            initial_metrics['cpc'] = 0
            
        if initial_metrics['leads'] > 0:
            initial_metrics['cpl'] = initial_metrics['spend'] / initial_metrics['leads']
        else:
            initial_metrics['cpl'] = 0
        
        return initial_metrics
    
    def _simulate_platform_metrics(self, platform, objective):
        """Simula métricas iniciais para uma plataforma específica"""
        
        # Métricas base para todas as plataformas
        metrics = {}
        
        # Ajustar parâmetros com base no objetivo
        if objective.lower() == 'awareness':
            ctr_factor = 0.8
            conv_factor = 0.7
        elif objective.lower() == 'consideration':
            ctr_factor = 1.0
            conv_factor = 0.9
        elif objective.lower() in ['conversion', 'lead generation']:
            ctr_factor = 1.2
            conv_factor = 1.3
        elif objective.lower() == 'remarketing':
            ctr_factor = 1.5
            conv_factor = 1.5
        else:
            ctr_factor = 1.0
            conv_factor = 1.0
        
        # Simular métricas específicas da plataforma
        if platform.lower() in ['facebook', 'instagram']:
            # Parâmetros base
            daily_budget = random.uniform(50, 200)
            cpm = random.uniform(15, 40)
            ctr_base = random.uniform(0.8, 2.0) * ctr_factor
            conv_rate = random.uniform(2, 5) * conv_factor / 100
            
            # Calcular métricas
            impressions = (daily_budget / cpm) * 1000
            clicks = impressions * (ctr_base / 100)
            leads = clicks * conv_rate
            
            # Adicionar à lista de métricas
            metrics.update({
                'impressions': round(impressions),
                'reach': round(impressions * random.uniform(0.7, 0.9)),
                'clicks': round(clicks),
                'ctr': round(ctr_base, 2),
                'spend': round(daily_budget, 2),
                'leads': round(leads),
                'cpl': round(daily_budget / leads if leads > 0 else 0, 2),
                'frequency': round(random.uniform(1.1, 1.8), 2),
                'landing_page_views': round(clicks * random.uniform(0.7, 0.9))
            })
            
        elif platform.lower() in ['google_search', 'google_display']:
            # Parâmetros base
            daily_budget = random.uniform(70, 250)
            
            if platform.lower() == 'google_search':
                cpc = random.uniform(2, 6)
                ctr_base = random.uniform(3, 7) * ctr_factor
                conv_rate = random.uniform(3, 8) * conv_factor / 100
            else:  # google_display
                cpc = random.uniform(0.5, 2)
                ctr_base = random.uniform(0.3, 0.8) * ctr_factor
                conv_rate = random.uniform(0.5, 2) * conv_factor / 100
            
            # Calcular métricas
            clicks = daily_budget / cpc
            impressions = clicks * 100 / ctr_base
            conversions = clicks * conv_rate
            
            # Adicionar à lista de métricas
            metrics.update({
                'impressions': round(impressions),
                'clicks': round(clicks),
                'ctr': round(ctr_base, 2),
                'cpc': round(cpc, 2),
                'spend': round(daily_budget, 2),
                'conversions': round(conversions),
                'conversion_rate': round(conv_rate * 100, 2),
                'cpa': round(daily_budget / conversions if conversions > 0 else 0, 2)
            })
            
        elif platform.lower() == 'linkedin':
            # Parâmetros base
            daily_budget = random.uniform(100, 300)
            cpc = random.uniform(6, 12)
            ctr_base = random.uniform(0.4, 0.8) * ctr_factor
            conv_rate = random.uniform(3, 7) * conv_factor / 100
            
            # Calcular métricas
            clicks = daily_budget / cpc
            impressions = clicks * 100 / ctr_base
            leads = clicks * conv_rate
            
            # Adicionar à lista de métricas
            metrics.update({
                'impressions': round(impressions),
                'clicks': round(clicks),
                'ctr': round(ctr_base, 2),
                'cpc': round(cpc, 2),
                'spend': round(daily_budget, 2),
                'leads': round(leads),
                'cpl': round(daily_budget / leads if leads > 0 else 0, 2),
                'form_completion_rate': round(random.uniform(40, 70), 2)
            })
            
        elif platform.lower() == 'email':
            # Parâmetros base
            sends = random.randint(1000, 5000)
            open_rate = random.uniform(20, 40)
            click_rate = random.uniform(2, 7) * ctr_factor
            conv_rate = random.uniform(1, 3) * conv_factor / 100
            
            # Calcular métricas
            opens = sends * (open_rate / 100)
            clicks = opens * (click_rate / 100)
            conversions = clicks * conv_rate
            
            # Adicionar à lista de métricas
            metrics.update({
                'sends': round(sends),
                'opens': round(opens),
                'open_rate': round(open_rate, 2),
                'clicks': round(clicks),
                'click_rate': round(click_rate, 2),
                'ctr': round((clicks / opens) * 100 if opens > 0 else 0, 2),
                'conversions': round(conversions),
                'conversion_rate': round(conv_rate * 100, 2),
                'bounces': round(sends * random.uniform(0.01, 0.03)),
                'bounce_rate': round(random.uniform(1, 3), 2),
                'spend': round(sends * random.uniform(0.05, 0.10), 2)
            })
            
        elif platform.lower() == 'whatsapp':
            # Parâmetros base
            sends = random.randint(500, 2000)
            delivery_rate = random.uniform(95, 99)
            open_rate = random.uniform(80, 95)
            reply_rate = random.uniform(20, 40) * ctr_factor
            conv_rate = random.uniform(5, 15) * conv_factor / 100
            
            # Calcular métricas
            delivered = sends * (delivery_rate / 100)
            opens = delivered * (open_rate / 100)
            replies = opens * (reply_rate / 100)
            conversions = replies * conv_rate
            
            # Adicionar à lista de métricas
            metrics.update({
                'messages_sent': round(sends),
                'delivered': round(delivered),
                'delivery_rate': round(delivery_rate, 2),
                'opens': round(opens),
                'open_rate': round((opens / delivered) * 100 if delivered > 0 else 0, 2),
                'replies': round(replies),
                'reply_rate': round((replies / opens) * 100 if opens > 0 else 0, 2),
                'conversions': round(conversions),
                'conversion_rate': round((conversions / replies) * 100 if replies > 0 else 0, 2),
                'blocks': round(sends * random.uniform(0.001, 0.01)),
                'spend': round(sends * random.uniform(0.02, 0.05), 2)
            })
        
        return metrics
    
    def _project_performance(self, campaigns):
        """Projeta desempenho para o período completo da campanha"""
        
        # Período de projeção (30 dias)
        projection_days = 30
        
        # Métricas totais
        total_metrics = {
            'total_impressions': 0,
            'total_clicks': 0,
            'total_spend': 0,
            'total_leads': 0,
            'total_conversions': 0,
            'avg_ctr': 0,
            'avg_cpc': 0,
            'avg_cpl': 0,
            'roi': 0
        }
        
        # Métricas por plataforma
        platform_metrics = {}
        
        # Calcular projeção para cada campanha
        for campaign in campaigns:
            # Métricas iniciais
            initial_metrics = campaign.get('initial_metrics', {})
            
            # Multiplicar por número de dias (com fatores de ajuste para crescimento/saturação)
            daily_growth_factor = 1.05  # 5% de crescimento diário inicial
            saturation_factor = 0.96   # 4% de queda na taxa de crescimento por dia
            
            # Fator cumulativo ao longo do período
            cumulative_factor = 0
            current_growth = daily_growth_factor
            
            for day in range(projection_days):
                cumulative_factor += current_growth
                current_growth *= saturation_factor
            
            # Projeção total para a campanha
            for metric, value in initial_metrics.items():
                if metric in ['ctr', 'cpc', 'cpl', 'conversion_rate']:
                    # Métricas de taxa não devem ser somadas
                    continue
                    
                projected_value = value * cumulative_factor
                
                # Adicionar à projeção total
                if metric in total_metrics:
                    total_metrics[f'total_{metric}'] += projected_value
                else:
                    total_metrics[f'total_{metric}'] = projected_value
            
            # Métricas por plataforma para esta campanha
            for platform, platform_data in campaign.get('platforms', {}).items():
                if platform not in platform_metrics:
                    platform_metrics[platform] = {
                        'impressions': 0,
                        'clicks': 0,
                        'spend': 0,
                        'leads': 0,
                        'conversions': 0
                    }
                
                # Métricas iniciais da plataforma
                platform_initial = platform_data.get('initial_metrics', {})
                
                # Projeção para a plataforma
                for metric, value in platform_initial.items():
                    if metric in ['ctr', 'cpc', 'cpl', 'conversion_rate']:
                        # Métricas de taxa não devem ser somadas
                        continue
                        
                    projected_value = value * cumulative_factor
                    
                    # Adicionar à projeção da plataforma
                    if metric in platform_metrics[platform]:
                        platform_metrics[platform][metric] += projected_value
                    else:
                        platform_metrics[platform][metric] = projected_value
        
        # Calcular métricas derivadas
        if total_metrics['total_impressions'] > 0:
            total_metrics['avg_ctr'] = (total_metrics['total_clicks'] / total_metrics['total_impressions']) * 100
        
        if total_metrics['total_clicks'] > 0:
            total_metrics['avg_cpc'] = total_metrics['total_spend'] / total_metrics['total_clicks']
            
        if total_metrics['total_leads'] > 0:
            total_metrics['avg_cpl'] = total_metrics['total_spend'] / total_metrics['total_leads']
        
        # Projetar conversões finais (franqueados)
        lead_to_franchise_rate = 0.05  # 5% dos leads se tornam franqueados
        projected_franchises = total_metrics.get('total_leads', 0) * lead_to_franchise_rate
        
        # Valor médio da taxa de franquia (30% do investimento médio de 150k)
        avg_franchise_fee = 150000 * 0.3
        
        # Receita projetada
        projected_revenue = projected_franchises * avg_franchise_fee
        
        # ROI
        if total_metrics['total_spend'] > 0:
            total_metrics['roi'] = (projected_revenue - total_metrics['total_spend']) / total_metrics['total_spend'] * 100
        
        # Resultados da projeção
        projection_results = {
            'period_days': projection_days,
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=projection_days)).strftime('%Y-%m-%d'),
            'summary': {
                'total_impressions': round(total_metrics['total_impressions']),
                'total_clicks': round(total_metrics['total_clicks']),
                'total_spend': round(total_metrics['total_spend'], 2),
                'total_leads': round(total_metrics['total_leads']),
                'avg_ctr': round(total_metrics['avg_ctr'], 2),
                'avg_cpc': round(total_metrics['avg_cpc'], 2),
                'avg_cpl': round(total_metrics['avg_cpl'], 2),
                'projected_franchises': round(projected_franchises, 1),
                'projected_revenue': round(projected_revenue, 2),
                'roi': round(total_metrics['roi'], 2)
            },
            'by_platform': {}
        }
        
        # Adicionar métricas por plataforma
        for platform, metrics in platform_metrics.items():
            platform_summary = {
                'impressions': round(metrics['impressions']),
                'clicks': round(metrics['clicks']),
                'spend': round(metrics['spend'], 2),
                'leads': round(metrics.get('leads', 0)),
                'conversions': round(metrics.get('conversions', 0))
            }
            
            # Métricas derivadas
            if metrics['impressions'] > 0:
                platform_summary['ctr'] = round((metrics['clicks'] / metrics['impressions']) * 100, 2)
            else:
                platform_summary['ctr'] = 0
                
            if metrics['clicks'] > 0:
                platform_summary['cpc'] = round(metrics['spend'] / metrics['clicks'], 2)
            else:
                platform_summary['cpc'] = 0
                
            if metrics.get('leads', 0) > 0:
                platform_summary['cpl'] = round(metrics['spend'] / metrics['leads'], 2)
            else:
                platform_summary['cpl'] = 0
            
            # Comparar com benchmarks
            platform_benchmarks = self.benchmarks.get(platform.lower(), {})
            
            platform_summary['performance_vs_benchmark'] = {}
            
            for metric, benchmark in platform_benchmarks.items():
                if metric in platform_summary:
                    actual_value = platform_summary[metric]
                    
                    if metric in ['ctr', 'open_rate', 'conversion_rate']:
                        # Para métricas onde maior é melhor
                        if actual_value >= benchmark['avg']:
                            performance = 'Above Average'
                        elif actual_value >= benchmark['min']:
                            performance = 'Average'
                        else:
                            performance = 'Below Average'
                    else:  # cpc, cpl, etc. (menor é melhor)
                        if actual_value <= benchmark['avg']:
                            performance = 'Above Average'
                        elif actual_value <= benchmark['max']:
                            performance = 'Average'
                        else:
                            performance = 'Below Average'
                    
                    platform_summary['performance_vs_benchmark'][metric] = {
                        'actual': actual_value,
                        'benchmark_min': benchmark['min'],
                        'benchmark_avg': benchmark['avg'],
                        'benchmark_max': benchmark['max'],
                        'performance': performance
                    }
            
            # Adicionar à projeção
            projection_results['by_platform'][platform] = platform_summary
        
        return projection_results
    
    def _save_tracking_setup(self, tracking_setup):
        """Salva a configuração de rastreamento (opcional)"""
        
        # Diretório para salvar resultados
        base_dir = os.path.join('output', 'automation')
        
        # Verificar se o diretório existe, se não, criar
        try:
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
                print(f"Diretório criado: {base_dir}")
            
            # Nome do arquivo baseado na data
            filename = f"tracking_setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path = os.path.join(base_dir, filename)
            
            # Salvar configuração em JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(tracking_setup, f, ensure_ascii=False, indent=2)
                
            print(f"Configuração de rastreamento salva em: {file_path}")
            
        except Exception as e:
            print(f"Erro ao salvar configuração de rastreamento: {e}")
