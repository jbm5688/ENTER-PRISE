# automation/optimization_engine.py
import random
import json
import os
from datetime import datetime, timedelta

class OptimizationEngine:
    """
    Classe responsável por otimizar campanhas com base nos resultados de desempenho
    """
    
    def __init__(self, analysis_params=None):
        """
        Inicializa o motor de otimização
        
        Args:
            analysis_params (dict): Parâmetros para análise e otimização
        """
        self.analysis_params = analysis_params or {}
        
        # Definir limites de otimização
        self.optimization_limits = {
            'budget_max_increase': 0.5,  # Aumento máximo de 50% no orçamento
            'budget_max_decrease': 0.3,  # Redução máxima de 30% no orçamento
            'bid_max_increase': 0.4,     # Aumento máximo de 40% no lance
            'bid_max_decrease': 0.25,    # Redução máxima de 25% no lance
            'audience_expansion_limit': 0.2,  # Expansão máxima de 20% na audiência
            'audience_narrowing_limit': 0.3   # Estreitamento máximo de 30% na audiência
        }
        
        # Definir limiares de desempenho para otimização
        self.performance_thresholds = {
            'ctr': {'low': 0.8, 'medium': 1.5, 'high': 3.0},
            'cpc': {'low': 0.5, 'medium': 3.0, 'high': 8.0},
            'cpl': {'low': 30, 'medium': 100, 'high': 300},
            'conversion_rate': {'low': 1, 'medium': 5, 'high': 10}
        }
        
        # Regras de otimização por plataforma
        self.optimization_rules = {
            'facebook': {
                'high_cpl_low_ctr': ['decrease_budget', 'review_creative', 'narrow_audience'],
                'high_cpl_high_ctr': ['review_landing_page', 'optimize_conversion_event'],
                'low_cpl_low_ctr': ['expand_audience', 'increase_budget'],
                'low_cpl_high_ctr': ['increase_budget', 'expand_audience', 'scale_campaign']
            },
            'instagram': {
                'high_cpl_low_ctr': ['decrease_budget', 'review_creative', 'narrow_audience'],
                'high_cpl_high_ctr': ['review_landing_page', 'optimize_conversion_event'],
                'low_cpl_low_ctr': ['expand_audience', 'increase_budget'],
                'low_cpl_high_ctr': ['increase_budget', 'expand_audience', 'scale_campaign']
            },
            'google_search': {
                'high_cpc_low_ctr': ['review_keywords', 'improve_quality_score', 'decrease_bids'],
                'high_cpc_high_ctr': ['review_landing_page', 'add_negative_keywords'],
                'low_cpc_low_ctr': ['increase_bids', 'expand_keywords'],
                'low_cpc_high_ctr': ['increase_budget', 'expand_keywords', 'scale_campaign']
            },
            'google_display': {
                'high_cpc_low_ctr': ['review_placements', 'review_creative', 'narrow_audience'],
                'high_cpc_high_ctr': ['review_landing_page', 'optimize_conversion_event'],
                'low_cpc_low_ctr': ['expand_audience', 'try_new_placements'],
                'low_cpc_high_ctr': ['increase_budget', 'expand_audience', 'scale_campaign']
            },
            'linkedin': {
                'high_cpl_low_ctr': ['review_targeting', 'review_creative', 'decrease_bids'],
                'high_cpl_high_ctr': ['review_landing_page', 'optimize_form_fields'],
                'low_cpl_low_ctr': ['expand_targeting', 'increase_bids'],
                'low_cpl_high_ctr': ['increase_budget', 'expand_targeting', 'scale_campaign']
            },
            'email': {
                'low_open_rate': ['improve_subject_line', 'segment_audience', 'test_send_time'],
                'low_click_rate': ['review_content', 'improve_cta', 'test_layout'],
                'high_bounce_rate': ['clean_list', 'review_sender_reputation'],
                'high_unsubscribe_rate': ['review_frequency', 'review_content_relevance']
            },
            'whatsapp': {
                'low_open_rate': ['review_first_message', 'segment_audience'],
                'low_reply_rate': ['improve_content', 'add_clear_cta'],
                'high_block_rate': ['review_frequency', 'review_message_content']
            }
        }
    
    def setup_optimization(self, performance_data):
        """
        Configura plano de otimização com base nos dados de desempenho
        
        Args:
            performance_data (dict): Dados de desempenho das campanhas
            
        Returns:
            dict: Plano de otimização
        """
        print("OptimizationEngine: Configurando plano de otimização baseado em desempenho")
        
        # Inicializar plano de otimização
        optimization_plan = {
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'optimization_schedule': self._create_optimization_schedule(),
            'campaigns': []
        }
        
        # Analisar dados de desempenho
        projection = performance_data.get('performance_projection', {})
        platform_metrics = projection.get('by_platform', {})
        
        # Para cada plataforma, criar ações de otimização
        for platform, metrics in platform_metrics.items():
            print(f"Analisando desempenho da plataforma: {platform}")
            
            # Criar plano para esta plataforma
            platform_plan = self._create_platform_optimization_plan(platform, metrics)
            
            # Aplicar regras de negócio para a plataforma
            platform_recommendations = self._apply_optimization_rules(platform, metrics)
            
            # Adicionar recomendações ao plano
            platform_plan['recommendations'] = platform_recommendations
            
            # Adicionar ações automatizadas
            platform_plan['automated_actions'] = self._generate_automated_actions(platform, metrics, platform_recommendations)
            
            # Adicionar plano da plataforma ao plano geral
            optimization_plan['campaigns'].append({
                'platform': platform,
                'optimization_plan': platform_plan
            })
        
        # Adicionar recomendações globais
        optimization_plan['global_recommendations'] = self._generate_global_recommendations(performance_data)
        
        # Salvar plano de otimização (opcional)
        self._save_optimization_plan(optimization_plan)
        
        return optimization_plan
    
    def _create_optimization_schedule(self):
        """Cria cronograma para otimizações"""
        
        # Data atual
        current_date = datetime.now()
        
        # Criar cronograma para os próximos 30 dias
        schedule = []
        
        # Dia 1-3: Monitoramento inicial
        schedule.append({
            'phase': 'Initial Monitoring',
            'start_date': current_date.strftime('%Y-%m-%d'),
            'end_date': (current_date + timedelta(days=3)).strftime('%Y-%m-%d'),
            'actions': [
                'Monitor CTR and Quality Score',
                'Identify underperforming creatives',
                'Collect initial performance data'
            ],
            'decision_points': [
                'Continue as is or make initial adjustments'
            ]
        })
        
        # Dia 4-7: Primeiras otimizações
        schedule.append({
            'phase': 'First Optimization Round',
            'start_date': (current_date + timedelta(days=4)).strftime('%Y-%m-%d'),
            'end_date': (current_date + timedelta(days=7)).strftime('%Y-%m-%d'),
            'actions': [
                'Pause underperforming ads',
                'Adjust bids based on performance',
                'Refine targeting for low CTR audiences'
            ],
            'decision_points': [
                'Keep or adjust budget allocation',
                'Decide on creative refresh'
            ]
        })
        
        # Dia 8-14: Otimização de conversão
        schedule.append({
            'phase': 'Conversion Optimization',
            'start_date': (current_date + timedelta(days=8)).strftime('%Y-%m-%d'),
            'end_date': (current_date + timedelta(days=14)).strftime('%Y-%m-%d'),
            'actions': [
                'Optimize for CPL/CPA',
                'Test landing page variations',
                'Refine audience based on conversion data'
            ],
            'decision_points': [
                'Scale high-performing campaigns',
                'Reallocate budget from low to high performers'
            ]
        })
        
        # Dia 15-21: Expansão e escala
        schedule.append({
            'phase': 'Expansion and Scaling',
            'start_date': (current_date + timedelta(days=15)).strftime('%Y-%m-%d'),
            'end_date': (current_date + timedelta(days=21)).strftime('%Y-%m-%d'),
            'actions': [
                'Scale successful campaigns',
                'Test new audience segments',
                'Introduce new creative variations'
            ],
            'decision_points': [
                'Go/No-go on campaign expansion',
                'Budget adjustment based on ROI'
            ]
        })
        
        # Dia 22-30: Otimização final e relatório
        schedule.append({
            'phase': 'Final Optimization and Reporting',
            'start_date': (current_date + timedelta(days=22)).strftime('%Y-%m-%d'),
            'end_date': (current_date + timedelta(days=30)).strftime('%Y-%m-%d'),
            'actions': [
                'Final bid and budget adjustments',
                'Prepare performance report',
                'Develop long-term strategy recommendations'
            ],
            'decision_points': [
                'Campaign continuation strategy',
                'Long-term budget planning'
            ]
        })
        
        return schedule
    
    def _create_platform_optimization_plan(self, platform, metrics):
        """Cria plano de otimização para uma plataforma específica"""
        
        # Inicializar plano
        platform_plan = {
            'current_metrics': {
                'impressions': metrics.get('impressions', 0),
                'clicks': metrics.get('clicks', 0),
                'ctr': metrics.get('ctr', 0),
                'cpc': metrics.get('cpc', 0),
                'spend': metrics.get('spend', 0),
                'conversions': metrics.get('conversions', 0),
                'conversion_rate': metrics.get('conversion_rate', 0),
                'cpl': metrics.get('cpl', 0)
            },
            'performance_analysis': self._analyze_platform_performance(platform, metrics),
            'improvement_targets': self._set_improvement_targets(platform, metrics),
            'recommendations': [],
            'automated_actions': []
        }
        
        return platform_plan
    
    # automation/optimization_engine.py (continuação)
    def _analyze_platform_performance(self, platform, metrics):
        """Analisa o desempenho de uma plataforma"""
        
        # Avaliar métricas-chave em relação aos benchmarks
        performance_vs_benchmark = metrics.get('performance_vs_benchmark', {})
        
        # Determinar status geral
        if not performance_vs_benchmark:
            status = "Undetermined"
            explanation = "Insufficient data for complete analysis"
        else:
            # Contagem de métricas por nível de desempenho
            above_avg = 0
            avg = 0
            below_avg = 0
            
            for metric, perf in performance_vs_benchmark.items():
                if perf.get('performance') == 'Above Average':
                    above_avg += 1
                elif perf.get('performance') == 'Average':
                    avg += 1
                elif perf.get('performance') == 'Below Average':
                    below_avg += 1
            
            # Determinar status com base na maioria
            if above_avg > avg and above_avg > below_avg:
                status = "Strong"
                explanation = "Multiple metrics performing above average"
            elif below_avg > avg and below_avg > above_avg:
                status = "Weak"
                explanation = "Multiple metrics performing below average"
            elif above_avg + avg > below_avg:
                status = "Average"
                explanation = "Most metrics performing at or above average"
            else:
                status = "Mixed"
                explanation = "Mixed performance across different metrics"
        
        # Pontos fortes e fracos
        strengths = []
        weaknesses = []
        opportunities = []
        
        # Analisar cada métrica-chave
        ctr = metrics.get('ctr', 0)
        cpc = metrics.get('cpc', 0)
        cpl = metrics.get('cpl', 0)
        conversion_rate = metrics.get('conversion_rate', 0)
        
        # Análise específica por plataforma
        if platform.lower() in ['facebook', 'instagram']:
            if ctr > self.performance_thresholds['ctr']['medium']:
                strengths.append("Strong creative engagement (CTR)")
            else:
                weaknesses.append("Creative performance needs improvement")
                
            if cpl < self.performance_thresholds['cpl']['medium']:
                strengths.append("Efficient lead generation (CPL)")
            else:
                weaknesses.append("High cost per lead")
                
            if conversion_rate > self.performance_thresholds['conversion_rate']['medium']:
                strengths.append("Good conversion rate")
            else:
                weaknesses.append("Low landing page conversion")
                
            # Oportunidades
            if ctr < self.performance_thresholds['ctr']['medium'] and cpl > self.performance_thresholds['cpl']['medium']:
                opportunities.append("Test new creative variants to improve engagement")
            if ctr > self.performance_thresholds['ctr']['medium'] and cpl > self.performance_thresholds['cpl']['medium']:
                opportunities.append("Optimize landing page for better conversion")
            if ctr > self.performance_thresholds['ctr']['high'] and cpl < self.performance_thresholds['cpl']['medium']:
                opportunities.append("Scale campaign with increased budget")
                
        elif platform.lower() in ['google_search', 'google_display']:
            if ctr > self.performance_thresholds['ctr']['medium']:
                strengths.append("Strong ad relevance (CTR)")
            else:
                weaknesses.append("Low click-through rate")
                
            if cpc < self.performance_thresholds['cpc']['medium']:
                strengths.append("Efficient cost per click")
            else:
                weaknesses.append("High cost per click")
                
            if conversion_rate > self.performance_thresholds['conversion_rate']['medium']:
                strengths.append("Good landing page conversion")
            else:
                weaknesses.append("Poor landing page performance")
                
            # Oportunidades
            if platform.lower() == 'google_search':
                if cpc > self.performance_thresholds['cpc']['medium']:
                    opportunities.append("Review keyword match types and add negative keywords")
                if ctr < self.performance_thresholds['ctr']['medium']:
                    opportunities.append("Improve ad copy and keyword relevance")
            else:  # google_display
                if ctr < self.performance_thresholds['ctr']['low']:
                    opportunities.append("Test new creative formats and placements")
                if conversion_rate < self.performance_thresholds['conversion_rate']['low']:
                    opportunities.append("Review audience targeting and landing page relevance")
                    
        elif platform.lower() == 'linkedin':
            if ctr > self.performance_thresholds['ctr']['medium']:
                strengths.append("Strong ad engagement for B2B (CTR)")
            else:
                weaknesses.append("Low engagement with target audience")
                
            if cpl < self.performance_thresholds['cpl']['high']:
                strengths.append("Reasonable cost per lead for LinkedIn")
            else:
                weaknesses.append("Very high cost per lead")
                
            # Oportunidades
            if ctr < self.performance_thresholds['ctr']['medium']:
                opportunities.append("Refine professional audience targeting")
            if cpl > self.performance_thresholds['cpl']['medium']:
                opportunities.append("Test Lead Gen Forms vs website conversion")
                
        elif platform.lower() == 'email':
            open_rate = metrics.get('open_rate', 0)
            click_rate = metrics.get('click_rate', 0)
            
            if open_rate > 25:
                strengths.append("Good email open rate")
            else:
                weaknesses.append("Low email open rate")
                
            if click_rate > 3:
                strengths.append("Strong email engagement")
            else:
                weaknesses.append("Low click-through from emails")
                
            # Oportunidades
            if open_rate < 20:
                opportunities.append("Test different subject lines and sender names")
            if click_rate < 3:
                opportunities.append("Improve email content and CTA placement")
                
        elif platform.lower() == 'whatsapp':
            open_rate = metrics.get('open_rate', 0)
            reply_rate = metrics.get('reply_rate', 0)
            
            if open_rate > 80:
                strengths.append("Excellent message visibility")
            else:
                weaknesses.append("Lower than expected message open rate")
                
            if reply_rate > 30:
                strengths.append("Strong audience engagement")
            else:
                weaknesses.append("Low audience response rate")
                
            # Oportunidades
            if reply_rate < 25:
                opportunities.append("Improve message content and call to action")
            if metrics.get('blocks', 0) > (metrics.get('messages_sent', 0) * 0.01):
                opportunities.append("Review message frequency and relevance to reduce blocks")
        
        # Compilar análise
        analysis = {
            'status': status,
            'explanation': explanation,
            'strengths': strengths[:3],  # Limitar a 3 pontos fortes
            'weaknesses': weaknesses[:3],  # Limitar a 3 pontos fracos
            'opportunities': opportunities[:3]  # Limitar a 3 oportunidades
        }
        
        return analysis
    
    def _set_improvement_targets(self, platform, metrics):
        """Define metas de melhoria com base no desempenho atual"""
        
        improvement_targets = {}
        
        # Métricas comuns
        if 'ctr' in metrics:
            current_ctr = metrics['ctr']
            target_ctr = current_ctr * 1.2  # Meta: aumentar CTR em 20%
            improvement_targets['ctr'] = {
                'current': round(current_ctr, 2),
                'target': round(target_ctr, 2),
                'improvement': '20%'
            }
        
        if 'cpc' in metrics:
            current_cpc = metrics['cpc']
            target_cpc = current_cpc * 0.9  # Meta: reduzir CPC em 10%
            improvement_targets['cpc'] = {
                'current': round(current_cpc, 2),
                'target': round(target_cpc, 2),
                'improvement': '10%'
            }
        
        if 'cpl' in metrics:
            current_cpl = metrics['cpl']
            target_cpl = current_cpl * 0.85  # Meta: reduzir CPL em 15%
            improvement_targets['cpl'] = {
                'current': round(current_cpl, 2),
                'target': round(target_cpl, 2),
                'improvement': '15%'
            }
        
        if 'conversion_rate' in metrics:
            current_conv_rate = metrics['conversion_rate']
            target_conv_rate = current_conv_rate * 1.25  # Meta: aumentar taxa de conversão em 25%
            improvement_targets['conversion_rate'] = {
                'current': round(current_conv_rate, 2),
                'target': round(target_conv_rate, 2),
                'improvement': '25%'
            }
        
        # Métricas específicas por plataforma
        if platform.lower() == 'email':
            if 'open_rate' in metrics:
                current_open_rate = metrics['open_rate']
                target_open_rate = min(current_open_rate * 1.15, 40)  # Meta: aumentar open rate em 15%, máximo 40%
                improvement_targets['open_rate'] = {
                    'current': round(current_open_rate, 2),
                    'target': round(target_open_rate, 2),
                    'improvement': '15%'
                }
                
            if 'click_rate' in metrics:
                current_click_rate = metrics['click_rate']
                target_click_rate = min(current_click_rate * 1.2, 8)  # Meta: aumentar click rate em 20%, máximo 8%
                improvement_targets['click_rate'] = {
                    'current': round(current_click_rate, 2),
                    'target': round(target_click_rate, 2),
                    'improvement': '20%'
                }
                
        elif platform.lower() == 'whatsapp':
            if 'reply_rate' in metrics:
                current_reply_rate = metrics['reply_rate']
                target_reply_rate = min(current_reply_rate * 1.2, 50)  # Meta: aumentar reply rate em 20%, máximo 50%
                improvement_targets['reply_rate'] = {
                    'current': round(current_reply_rate, 2),
                    'target': round(target_reply_rate, 2),
                    'improvement': '20%'
                }
        
        return improvement_targets
    
    def _apply_optimization_rules(self, platform, metrics):
        """Aplica regras de otimização com base nas métricas"""
        
        # Obter regras para a plataforma
        platform_rules = self.optimization_rules.get(platform.lower(), {})
        
        if not platform_rules:
            return ["Platform-specific optimization rules not available"]
        
        # Determinar situação de desempenho
        if platform.lower() in ['facebook', 'instagram', 'linkedin']:
            # Avaliar CTR e CPL
            ctr = metrics.get('ctr', 0)
            cpl = metrics.get('cpl', 0)
            
            ctr_threshold_medium = self.performance_thresholds['ctr']['medium']
            cpl_threshold_medium = self.performance_thresholds['cpl']['medium']
            
            if ctr < ctr_threshold_medium and cpl > cpl_threshold_medium:
                rule_key = 'high_cpl_low_ctr'
            elif ctr >= ctr_threshold_medium and cpl > cpl_threshold_medium:
                rule_key = 'high_cpl_high_ctr'
            elif ctr < ctr_threshold_medium and cpl <= cpl_threshold_medium:
                rule_key = 'low_cpl_low_ctr'
            else:
                rule_key = 'low_cpl_high_ctr'
                
        elif platform.lower() in ['google_search', 'google_display']:
            # Avaliar CTR e CPC
            ctr = metrics.get('ctr', 0)
            cpc = metrics.get('cpc', 0)
            
            ctr_threshold_medium = self.performance_thresholds['ctr']['medium']
            cpc_threshold_medium = self.performance_thresholds['cpc']['medium']
            
            if ctr < ctr_threshold_medium and cpc > cpc_threshold_medium:
                rule_key = 'high_cpc_low_ctr'
            elif ctr >= ctr_threshold_medium and cpc > cpc_threshold_medium:
                rule_key = 'high_cpc_high_ctr'
            elif ctr < ctr_threshold_medium and cpc <= cpc_threshold_medium:
                rule_key = 'low_cpc_low_ctr'
            else:
                rule_key = 'low_cpc_high_ctr'
                
        elif platform.lower() == 'email':
            # Avaliar métricas de email
            open_rate = metrics.get('open_rate', 0)
            click_rate = metrics.get('click_rate', 0)
            bounce_rate = metrics.get('bounce_rate', 0)
            unsubscribe_rate = metrics.get('unsubscribe_rate', 0)
            
            if open_rate < 20:
                rule_key = 'low_open_rate'
            elif click_rate < 3:
                rule_key = 'low_click_rate'
            elif bounce_rate > 3:
                rule_key = 'high_bounce_rate'
            elif unsubscribe_rate > 0.5:
                rule_key = 'high_unsubscribe_rate'
            else:
                return ["Current email performance is good, continue monitoring"]
                
        elif platform.lower() == 'whatsapp':
            # Avaliar métricas de WhatsApp
            open_rate = metrics.get('open_rate', 0)
            reply_rate = metrics.get('reply_rate', 0)
            block_rate = metrics.get('blocks', 0) / max(metrics.get('messages_sent', 1), 1) * 100
            
            if open_rate < 70:
                rule_key = 'low_open_rate'
            elif reply_rate < 20:
                rule_key = 'low_reply_rate'
            elif block_rate > 1:
                rule_key = 'high_block_rate'
            else:
                return ["Current WhatsApp performance is good, continue monitoring"]
        else:
            return ["Platform not supported for automated optimization"]
        
        # Obter recomendações para a situação
        return platform_rules.get(rule_key, ["No specific recommendations available"])
    
    def _generate_automated_actions(self, platform, metrics, recommendations):
        """Gera ações automatizadas com base nas recomendações"""
        
        automated_actions = []
        
        for recommendation in recommendations:
            if recommendation == 'increase_budget':
                # Calcular aumento de orçamento (10-30% dependendo do desempenho)
                cpl = metrics.get('cpl', 0)
                cpl_threshold_low = self.performance_thresholds['cpl']['low']
                
                if cpl <= cpl_threshold_low:
                    increase_percentage = 0.3  # 30% de aumento para desempenho excelente
                else:
                    increase_percentage = 0.1  # 10% de aumento para desempenho bom
                
                current_budget = metrics.get('spend', 0) / 30  # Orçamento diário estimado
                new_budget = current_budget * (1 + increase_percentage)
                
                action = {
                    'type': 'budget_adjustment',
                    'platform': platform,
                    'current_value': round(current_budget, 2),
                    'new_value': round(new_budget, 2),
                    'change_percentage': f"+{increase_percentage * 100}%",
                    'schedule': 'Immediate',
                    'automatic': True
                }
                automated_actions.append(action)
                
            elif recommendation == 'decrease_budget':
                # Calcular redução de orçamento (10-20% dependendo do desempenho)
                cpl = metrics.get('cpl', 0)
                cpl_threshold_high = self.performance_thresholds['cpl']['high']
                
                if cpl >= cpl_threshold_high:
                    decrease_percentage = 0.2  # 20% de redução para desempenho ruim
                else:
                    decrease_percentage = 0.1  # 10% de redução para desempenho abaixo da média
                
                current_budget = metrics.get('spend', 0) / 30  # Orçamento diário estimado
                new_budget = current_budget * (1 - decrease_percentage)
                
                action = {
                    'type': 'budget_adjustment',
                    'platform': platform,
                    'current_value': round(current_budget, 2),
                    'new_value': round(new_budget, 2),
                    'change_percentage': f"-{decrease_percentage * 100}%",
                    'schedule': 'Immediate',
                    'automatic': True
                }
                automated_actions.append(action)
                
            elif recommendation == 'increase_bids':
                # Aumento de lances (5-15%)
                increase_percentage = 0.1  # 10% de aumento
                
                action = {
                    'type': 'bid_adjustment',
                    'platform': platform,
                    'change_percentage': f"+{increase_percentage * 100}%",
                    'schedule': 'Immediate',
                    'automatic': True,
                    'note': 'Increase bids to improve ad position and CTR'
                }
                automated_actions.append(action)
                
            elif recommendation == 'decrease_bids':
                # Redução de lances (5-15%)
                decrease_percentage = 0.1  # 10% de redução
                
                action = {
                    'type': 'bid_adjustment',
                    'platform': platform,
                    'change_percentage': f"-{decrease_percentage * 100}%",
                    'schedule': 'Immediate',
                    'automatic': True,
                    'note': 'Decrease bids to improve cost efficiency'
                }
                automated_actions.append(action)
                
            elif recommendation == 'expand_audience':
                # Expansão de audiência
                action = {
                    'type': 'audience_adjustment',
                    'platform': platform,
                    'adjustment': 'Expansion',
                    'criteria': 'Similar Audiences',
                    'schedule': 'Next 48 hours',
                    'automatic': False,
                    'note': 'Requires manual review before implementation'
                }
                automated_actions.append(action)
                
            elif recommendation == 'narrow_audience':
                # Estreitamento de audiência
                action = {
                    'type': 'audience_adjustment',
                    'platform': platform,
                    'adjustment': 'Narrowing',
                    'criteria': 'Performance-based',
                    'schedule': 'Next 48 hours',
                    'automatic': False,
                    'note': 'Requires manual review before implementation'
                }
                automated_actions.append(action)
                
            elif recommendation == 'pause_underperforming_ads':
                # Pausar anúncios com baixo desempenho
                action = {
                    'type': 'ad_status_change',
                    'platform': platform,
                    'change': 'Pause',
                    'criteria': 'CTR < 50% of average or CPC > 150% of average',
                    'schedule': 'Immediate',
                    'automatic': True
                }
                automated_actions.append(action)
                
            elif recommendation == 'review_creative':
                # Revisão de criativo (ação manual)
                action = {
                    'type': 'creative_review',
                    'platform': platform,
                    'status': 'Pending',
                    'priority': 'High',
                    'schedule': 'Next 24 hours',
                    'automatic': False,
                    'note': 'Manual action required: Review and refresh creative elements'
                }
                automated_actions.append(action)
                
            elif recommendation == 'review_landing_page':
                # Revisão de landing page (ação manual)
                action = {
                    'type': 'landing_page_review',
                    'platform': platform,
                    'status': 'Pending',
                    'priority': 'High',
                    'schedule': 'Next 48 hours',
                    'automatic': False,
                    'note': 'Manual action required: Improve landing page conversion elements'
                }
                automated_actions.append(action)
                
            elif recommendation in ['improve_subject_line', 'improve_content', 'test_send_time']:
                # Ações específicas para email
                if platform.lower() == 'email':
                    action = {
                        'type': 'email_optimization',
                        'platform': platform,
                        'optimization': recommendation,
                        'status': 'Pending',
                        'schedule': 'Next email campaign',
                        'automatic': False,
                        'note': f'Manual action required: {recommendation.replace("_", " ").title()}'
                    }
                    automated_actions.append(action)
        
        return automated_actions
    
    def _generate_global_recommendations(self, performance_data):
        """Gera recomendações globais para todas as campanhas"""
        
        # Analisar projeção de desempenho
        projection = performance_data.get('performance_projection', {})
        summary = projection.get('summary', {})
        
        roi = summary.get('roi', 0)
        cpl = summary.get('avg_cpl', 0)
        leads = summary.get('total_leads', 0)
        
        # Recomendações globais
        global_recommendations = []
        
        # Recomendações baseadas em ROI
        if roi < 100:
            global_recommendations.append({
                'area': 'Budget Allocation',
                'priority': 'High',
                'recommendation': 'Review overall marketing strategy due to low projected ROI',
                'expected_impact': 'Improved campaign efficiency',
                'timeline': 'Immediate review required'
            })
        elif roi > 300:
            global_recommendations.append({
                'area': 'Budget Allocation',
                'priority': 'Medium',
                'recommendation': 'Consider increasing overall budget to scale successful campaigns',
                'expected_impact': 'Increased lead volume while maintaining efficiency',
                'timeline': 'Next 7-14 days'
            })
        
        # Recomendações baseadas em CPL médio
        if cpl > 150:
            global_recommendations.append({
                'area': 'Conversion Optimization',
                'priority': 'High',
                'recommendation': 'Implement comprehensive landing page testing to reduce overall CPL',
                'expected_impact': 'Lower acquisition costs across channels',
                'timeline': 'Next 7-14 days'
            })
        
        # Recomendações baseadas no número de leads
        if leads < 100:
            global_recommendations.append({
                'area': 'Lead Generation',
                'priority': 'High',
                'recommendation': 'Expand targeting to increase lead volume, even at slightly higher CPL',
                'expected_impact': 'Increased lead flow to sales team',
                'timeline': 'Next 7 days'
            })
        
        # Recomendações padrão (independente dos números)
        global_recommendations.extend([
            {
                'area': 'Cross-Channel Integration',
                'priority': 'Medium',
                'recommendation': 'Implement consistent messaging and tracking across all marketing channels',
                'expected_impact': 'Improved attribution and user experience',
                'timeline': 'Next 14-21 days'
            },
            {
                'area': 'Creative Testing',
                'priority': 'Medium',
                'recommendation': 'Develop and test new creative approaches, especially video content',
                'expected_impact': 'Improved engagement metrics',
                'timeline': 'Next 21-30 days'
            },
            {
                'area': 'Lead Nurturing',
                'priority': 'Medium',
                'recommendation': 'Enhance email and WhatsApp sequences for leads that don\'t convert immediately',
                'expected_impact': 'Increased conversion rate from existing leads',
                'timeline': 'Next 14-21 days'
            }
        ])
        
        return global_recommendations
    
    def _save_optimization_plan(self, optimization_plan):
        """Salva o plano de otimização (opcional)"""
        
        # Diretório para salvar resultados
        base_dir = os.path.join('output', 'automation')
        
        # Verificar se o diretório existe, se não, criar
        try:
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
                print(f"Diretório criado: {base_dir}")
            
            # Nome do arquivo baseado na data
            filename = f"optimization_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path = os.path.join(base_dir, filename)
            
            # Salvar plano em JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(optimization_plan, f, ensure_ascii=False, indent=2)
                
            print(f"Plano de otimização salvo em: {file_path}")
            
        except Exception as e:
            print(f"Erro ao salvar plano de otimização: {e}")
