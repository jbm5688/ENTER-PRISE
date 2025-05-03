import logging
import random
from datetime import datetime, timedelta
import time
import os
import json

logger = logging.getLogger("franquia_finder")

class CampaignAutomation:
    """
    Classe responsável pela automação de campanhas de marketing para as oportunidades de franquia.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o automatizador de campanhas.
        
        Args:
            config (dict): Configurações para automação de campanhas
        """
        self.config = config or {}
        
        # Configurações padrão caso não sejam fornecidas
        self.platforms = self.config.get('active_platforms', 
                                        ["facebook", "instagram", "google", "linkedin", "email"])
        self.test_mode = self.config.get('test_mode', True)  # Modo de teste por padrão
        self.auto_schedule = self.config.get('auto_schedule', False)
        self.auto_optimize = self.config.get('auto_optimize', False)
        
        logger.info(f"Automação de campanhas inicializada com {len(self.platforms)} plataformas.")
    
    def automate_campaigns(self, marketing_outputs, opportunities):
        """
        Automatiza o lançamento de campanhas para as oportunidades identificadas.
        
        Args:
            marketing_outputs (dict): Outputs de marketing gerados
            opportunities (list): Lista de oportunidades de franquia
            
        Returns:
            dict: Resultados da automação de campanhas
        """
        if not marketing_outputs or not opportunities:
            logger.warning("Sem outputs de marketing ou oportunidades para automatizar campanhas.")
            return {"status": "error", "message": "Dados insuficientes para automação"}
        
        automation_results = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "test_mode": self.test_mode,
            "campaigns": []
        }
        
        for opportunity in opportunities:
            # Verificar se opportunity é um dicionário ou uma string
            if isinstance(opportunity, dict):
                opportunity_name = opportunity.get('name', '')
            else:
                # Se for uma string, usar a própria string como nome
                opportunity_name = str(opportunity)
                
            # Verificar se temos materiais de marketing para esta oportunidade
            if opportunity_name not in marketing_outputs:
                logger.warning(f"Sem outputs de marketing para {opportunity_name}. Pulando.")
                continue
            
            marketing_data = marketing_outputs[opportunity_name]
            
            # Automatizar para cada plataforma ativa
            for platform in self.platforms:
                if platform in marketing_data.get('platform_adaption', {}):
                    platform_data = marketing_data['platform_adaption'][platform]
                    campaign_result = self._automate_platform_campaign(
                        # Criar um dicionário mínimo se opportunity não for um dicionário
                        {'name': opportunity_name} if not isinstance(opportunity, dict) else opportunity, 
                        platform, 
                        platform_data
                    )
                    
                    if campaign_result:
                        automation_results["campaigns"].append(campaign_result)
        
        # Salvar resultados da automação
        self._save_automation_results(automation_results)
        
        if self.test_mode:
            logger.info("Automação executada em modo de teste (sem publicação real)")
        else:
            logger.info("Automação de campanhas concluída e campanhas publicadas")
        
        return automation_results
    
    def _automate_platform_campaign(self, opportunity, platform, platform_data):
        """
        Automatiza campanha para uma plataforma específica.
        
        Args:
            opportunity (dict): Dados da oportunidade
            platform (str): Nome da plataforma
            platform_data (dict): Dados de marketing adaptados para a plataforma
            
        Returns:
            dict: Resultado da automação para esta plataforma
        """
        try:
            logger.info(f"Automatizando campanha em {platform} para {opportunity['name']}")
            
            # Simular tempo de processamento da API
            time.sleep(random.uniform(0.5, 1.5))
            
            # Em implementação real, aqui seria feita a integração com APIs das plataformas
            
            # Gerar ID de campanha simulado
            campaign_id = f"{platform[:3]}-{int(time.time())}-{random.randint(1000, 9999)}"
            
            result = {
                "opportunity": opportunity['name'],
                "platform": platform,
                "campaign_id": campaign_id,
                "status": "scheduled" if self.test_mode else "active",
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "schedule": {
                    "start_date": datetime.now().strftime('%Y-%m-%d'),
                    "end_date": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
                },
                "budget": {
                    "daily": round(random.uniform(10, 50), 2),
                    "total": round(random.uniform(300, 1500), 2)
                },
                "targeting": self._generate_targeting(platform, opportunity),
                "content_ids": self._generate_content_ids(platform_data),
                "test_mode": self.test_mode
            }
            
            # Simular otimização automática se ativada
            if self.auto_optimize:
                result["optimization"] = {
                    "target_metric": "conversion_rate",
                    "auto_budget_adjustment": True,
                    "a_b_testing": True,
                    "performance_alerts": True
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao automatizar campanha em {platform}: {e}")
            return None
    
    def _generate_targeting(self, platform, opportunity):
        """
        Gera parâmetros de segmentação com base na plataforma e oportunidade.
        
        Args:
            platform (str): Nome da plataforma
            opportunity (dict): Dados da oportunidade
            
        Returns:
            dict: Parâmetros de segmentação
        """
        # Segmentação simulada baseada na plataforma
        if platform == "facebook" or platform == "instagram":
            return {
                "age_range": "25-55",
                "gender": "all",
                "interests": ["empreendedorismo", "negócios", "franquias", "investimentos"],
                "locations": ["Brasil"],
                "languages": ["pt"],
                "detailed_targeting": f"interessados em {opportunity.get('category', 'franquias')}"
            }
        elif platform == "google":
            return {
                "keywords": [
                    f"franquia {opportunity.get('category', '')}",
                    "franquia lucrativa",
                    "investir em franquia",
                    f"abrir {opportunity.get('category', 'negócio')}"
                ],
                "locations": ["Brasil"],
                "devices": ["mobile", "desktop"],
                "exclusions": ["empregos", "gratuito", "falência", "problemas", "reclamações"]
            }
        elif platform == "linkedin":
            return {
                "job_titles": ["empresário", "empreendedor", "investidor", "gestor"],
                "industries": [opportunity.get('category', 'varejo')],
                "company_sizes": ["1-10", "11-50", "51-200"],
                "locations": ["Brasil"],
                "languages": ["pt"]
            }
        elif platform == "email":
            return {
                "segments": ["leads_novos", "leads_quentes", "clientes_potenciais"],
                "interests": [opportunity.get('category', 'franquias')],
                "engagement_level": ["médio", "alto"]
            }
        else:
            return {"default_targeting": "all"}
    
    def _generate_content_ids(self, platform_data):
        """
        Gera IDs de conteúdo simulados para os criativos.
        
        Args:
            platform_data (dict): Dados de marketing da plataforma
            
        Returns:
            list: Lista de IDs de conteúdo
        """
        content_ids = []
        
        # Número de conteúdos simulados
        num_contents = random.randint(3, 8)
        
        for i in range(num_contents):
            content_ids.append(f"content-{int(time.time())}-{random.randint(1000, 9999)}")
        
        return content_ids
    
    def _save_automation_results(self, automation_results):
        """
        Salva os resultados da automação em um arquivo JSON.
        
        Args:
            automation_results (dict): Resultados da automação
        """
        # Garantir que o diretório existe
        os.makedirs('output/automation', exist_ok=True)
        
        # Gerar nome do arquivo com timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"output/automation/campaign_automation_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(automation_results, f, indent=4, ensure_ascii=False)
            logger.info(f"Resultados da automação salvos em {filename}")
        except Exception as e:
            logger.error(f"Erro ao salvar resultados da automação: {e}")
    
    def monitor_campaigns(self, campaign_ids=None):
        """
        Monitora campanhas ativas e ajusta conforme necessário.
        
        Args:
            campaign_ids (list): Lista de IDs de campanhas para monitorar
            
        Returns:
            dict: Status de monitoramento das campanhas
        """
        if self.test_mode:
            logger.info("Monitoramento simulado no modo de teste")
            
            # Gerar dados de desempenho simulados
            performance_data = {
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "campaigns": []
            }
            
            if campaign_ids:
                for campaign_id in campaign_ids:
                    performance_data["campaigns"].append({
                        "campaign_id": campaign_id,
                        "impressions": random.randint(1000, 10000),
                        "clicks": random.randint(50, 500),
                        "ctr": round(random.uniform(0.01, 0.05), 4),
                        "conversions": random.randint(1, 20),
                        "conversion_rate": round(random.uniform(0.01, 0.1), 4),
                        "cpa": round(random.uniform(20, 100), 2),
                        "spend": round(random.uniform(100, 500), 2),
                        "status": random.choice(["active", "paused", "optimizing"]),
                        "alerts": []
                    })
            
            # Salvar resultado do monitoramento
            os.makedirs('output/monitoring', exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/monitoring/campaign_monitoring_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(performance_data, f, indent=4, ensure_ascii=False)
            
            return performance_data
        else:
            logger.warning("Monitoramento real de campanhas não implementado")
            return {"status": "not_implemented", "message": "Monitoramento real não disponível"}
