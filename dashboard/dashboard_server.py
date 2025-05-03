# dashboard/dashboard_server.py
import os
import json
import logging
import webbrowser
from datetime import datetime

logger = logging.getLogger("franquia_finder")

class DashboardGenerator:
    """
    Classe responsável por gerar um dashboard HTML estático.
    """
    
    def __init__(self, config=None):
        """
        Inicializa o gerador de dashboard.
        
        Args:
            config (dict): Configurações para o dashboard
        """
        self.config = config or {}
        self.dashboard_dir = self.config.get('dashboard_dir', 'output/dashboard')
        self.auto_open = self.config.get('auto_open', True)
    
    def generate_dashboard(self, analysis_data, marketing_data, automation_data=None):
        """
        Gera um arquivo HTML estático com os dados do dashboard.
        
        Args:
            analysis_data (dict): Dados da análise de oportunidades
            marketing_data (dict): Dados de marketing gerados
            automation_data (dict): Dados da automação de campanhas
            
        Returns:
            bool: True se o dashboard foi gerado com sucesso
        """
        try:
            # Garantir que o diretório existe
            os.makedirs(self.dashboard_dir, exist_ok=True)
            
            # Gerar um único arquivo HTML auto-contido (sem JS ou CSS separados)
            html_content = self._generate_self_contained_html(analysis_data, marketing_data, automation_data)
            
            # Salvar o arquivo HTML
            dashboard_path = os.path.join(self.dashboard_dir, 'dashboard.html')
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Dashboard gerado em {dashboard_path}")
            
            # Abrir no navegador se desejado
            if self.auto_open:
                # Converter para caminho absoluto para garantir que o navegador o encontre
                full_path = os.path.abspath(dashboard_path)
                logger.info(f"Abrindo dashboard no navegador: {full_path}")
                webbrowser.open('file://' + full_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar dashboard: {e}")
            return False
    
    def _generate_self_contained_html(self, analysis_data, marketing_data, automation_data):
        """
        Gera um HTML auto-contido com os dados do dashboard.
        """
        # Extrair dados das oportunidades
        opportunities = []
        if analysis_data and 'opportunities' in analysis_data:
            if isinstance(analysis_data['opportunities'], dict):
                for name, data in analysis_data['opportunities'].items():
                    opp = {'name': name}
                    if 'basic_info' in data:
                        opp.update(data['basic_info'])
                    opportunities.append(opp)
            else:
                opportunities = analysis_data['opportunities']
        
        # Extrair tendências de mercado
        market_trends = analysis_data.get('market_trends', []) if analysis_data else []
        
        # Formatar oportunidades como HTML
        opportunities_html = ""
        for opp in opportunities:
            name = opp.get('name', 'N/A')
            category = opp.get('category', 'N/A')
            roi = opp.get('roi_percentage', 0)
            investment = opp.get('initial_investment', 0)
            
            opportunities_html += f"""
            <div class="card">
                <h3>{name}</h3>
                <p><strong>Categoria:</strong> {category}</p>
                <p><strong>ROI Estimado:</strong> {roi:.2f}%</p>
                <p><strong>Investimento Inicial:</strong> R$ {investment:,.2f}</p>
            </div>
            """
        
        # Formatar tendências como HTML
        trends_html = ""
        for trend in market_trends:
            keyword = trend.get('keyword', 'N/A')
            growth = trend.get('growth_rate', 0) * 100 if 'growth_rate' in trend else 0
            sentiment = trend.get('sentiment', 0) * 100 if 'sentiment' in trend else 0
            
            trends_html += f"""
            <div class="card">
                <h3>{keyword}</h3>
                <p><strong>Taxa de Crescimento:</strong> {growth:.1f}%</p>
                <p><strong>Sentimento:</strong> {sentiment:.1f}%</p>
            </div>
            """
        
        # Formatar campanhas como HTML
        campaigns_html = ""
        if automation_data and 'campaigns' in automation_data:
            for campaign in automation_data['campaigns']:
                opportunity = campaign.get('opportunity', 'N/A')
                platform = campaign.get('platform', 'N/A')
                status = campaign.get('status', 'N/A')
                
                campaigns_html += f"""
                <div class="card">
                    <h3>{opportunity} - {platform}</h3>
                    <p><strong>Status:</strong> {status}</p>
                    <p><strong>Criado em:</strong> {campaign.get('created_at', 'N/A')}</p>
                </div>
                """
        
        # HTML completo auto-contido
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guia de Oportunidades de Franquias</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .tabs {{
            display: flex;
            background-color: #f1f1f1;
            border-bottom: 1px solid #ddd;
        }}
        .tab {{
            background-color: inherit;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
            font-size: 17px;
        }}
        .tab:hover {{
            background-color: #ddd;
        }}
        .tab.active {{
            background-color: #3498db;
            color: white;
        }}
        .tabcontent {{
            display: none;
            padding: 20px;
            border: 1px solid #ddd;
            border-top: none;
        }}
        .visible {{
            display: block;
        }}
        .cards {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }}
        .card {{
            background: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            padding: 20px;
            flex: 1;
            min-width: 300px;
        }}
        .summary {{
            background: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }}
        .metric-name {{
            font-weight: bold;
        }}
        footer {{
            text-align: center;
            padding: 20px;
            color: #777;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Guia de Oportunidades de Franquias</h1>
        <p>Análise de Oportunidades de Franquia</p>
    </header>
    
    <div class="container">
        <div class="summary">
            <h2>Resumo</h2>
            <div class="metric">
                <span class="metric-name">Oportunidades Identificadas:</span>
                <span>{len(opportunities)}</span>
            </div>
            <div class="metric">
                <span class="metric-name">Tendências de Mercado:</span>
                <span>{len(market_trends)}</span>
            </div>
            <div class="metric">
                <span class="metric-name">Campanhas Ativas:</span>
                <span>{len(automation_data.get('campaigns', [])) if automation_data else 0}</span>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="openTab(event, 'opportunities')">Oportunidades</button>
            <button class="tab" onclick="openTab(event, 'trends')">Tendências</button>
            <button class="tab" onclick="openTab(event, 'campaigns')">Campanhas</button>
        </div>
        
        <div id="opportunities" class="tabcontent visible">
            <h2>Oportunidades de Franquia</h2>
            <div class="cards">
                {opportunities_html}
            </div>
        </div>
        
        <div id="trends" class="tabcontent">
            <h2>Tendências de Mercado</h2>
            <div class="cards">
                {trends_html}
            </div>
        </div>
        
        <div id="campaigns" class="tabcontent">
            <h2>Campanhas de Marketing</h2>
            <div class="cards">
                {campaigns_html if campaigns_html else "<p>Nenhuma campanha ativa no momento.</p>"}
            </div>
        </div>
    </div>
    
    <footer>
        <p>Franquia Finder - Dashboard gerado em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>
    
    <script>
        function openTab(evt, tabName) {{
            var i, tabcontent, tablinks;
            
            tabcontent = document.getElementsByClassName("tabcontent");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].classList.remove("visible");
            }}
            
            tablinks = document.getElementsByClassName("tab");
            for (i = 0; i < tablinks.length; i++) {{
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }}
            
            document.getElementById(tabName).classList.add("visible");
            evt.currentTarget.className += " active";
        }}
    </script>
</body>
</html>
"""
        return html

def launch_dashboard(analysis_data, marketing_data=None, automation_data=None, config=None):
    """
    Função auxiliar para gerar um dashboard HTML.
    
    Args:
        analysis_data (dict): Dados da análise de oportunidades
        marketing_data (dict): Dados de marketing gerados
        automation_data (dict): Dados da automação de campanhas
        config (dict): Configurações para o dashboard
        
    Returns:
        DashboardGenerator: Instância do gerador de dashboard
    """
    dashboard = DashboardGenerator(config)
    
    # Gerar arquivo HTML do dashboard
    dashboard.generate_dashboard(analysis_data, marketing_data, automation_data)
    
    return dashboard
