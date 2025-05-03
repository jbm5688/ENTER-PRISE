# dashboard/app.py
import os
import json
from datetime import datetime, timedelta
import random

# Função para criar um aplicativo de dashboard
def create_dashboard(dashboard_data):
    """
    Cria um aplicativo de dashboard para visualização dos resultados
    
    Args:
        dashboard_data (dict): Dados para o dashboard
        
    Returns:
        object: Aplicativo de dashboard
    """
    print("Dashboard: Criando aplicativo de dashboard para visualização dos resultados")
    
    # Simulação do objeto de aplicativo de dashboard
    dashboard_app = DashboardApp(dashboard_data)
    
    return dashboard_app

# Classe simulada para representar o aplicativo Dash
class DashboardApp:
    """
    Classe que simula um aplicativo Dash para o dashboard
    """
    
    def __init__(self, dashboard_data):
        """
        Inicializa o aplicativo de dashboard
        
        Args:
            dashboard_data (dict): Dados para o dashboard
        """
        self.data = dashboard_data
        self.layouts = self._create_layouts()
        
        print("Dashboard: Aplicativo inicializado com sucesso")
        print("Dashboard: Disponível em: http://127.0.0.1:8050/ (simulação)")
        
        # Salvar dados do dashboard para uso posterior (opcional)
        self._save_dashboard_data()
    
    def _create_layouts(self):
        """Cria layouts para o dashboard"""
        
        # Definição de layouts de página
        layouts = {
            'main': {
                'title': 'Franquia Finder - Dashboard Principal',
                'components': [
                    {
                        'type': 'header',
                        'content': 'Dashboard de Análise de Franquias'
                    },
                    {
                        'type': 'kpi_cards',
                        'items': self._generate_kpi_cards()
                    },
                    {
                        'type': 'chart',
                        'title': 'Top Oportunidades de Franquia',
                        'chart_type': 'bar',
                        'data': self._generate_opportunities_chart_data()
                    },
                    {
                        'type': 'chart',
                        'title': 'Desempenho de Marketing por Canal',
                        'chart_type': 'line',
                        'data': self._generate_marketing_performance_data()
                    }
                ]
            },
            'opportunities': {
                'title': 'Análise de Oportunidades',
                'components': [
                    {
                        'type': 'header',
                        'content': 'Oportunidades de Franquia Detalhadas'
                    },
                    {
                        'type': 'table',
                        'title': 'Ranking de Oportunidades',
                        'data': self._generate_opportunities_table_data()
                    },
                    {
                        'type': 'chart',
                        'title': 'Comparativo de ROI por Setor',
                        'chart_type': 'bar',
                        'data': self._generate_roi_by_sector_data()
                    },
                    {
                        'type': 'chart',
                        'title': 'Relação Investimento vs. Retorno',
                        'chart_type': 'scatter',
                        'data': self._generate_investment_return_data()
                    }
                ]
            },
            'marketing': {
                'title': 'Análise de Marketing',
                'components': [
                    {
                        'type': 'header',
                        'content': 'Desempenho de Marketing'
                    },
                    {
                        'type': 'chart',
                        'title': 'Desempenho por Plataforma',
                        'chart_type': 'bar',
                        'data': self._generate_platform_performance_data()
                    },
                    {
                        'type': 'chart',
                        'title': 'Tendência de Custo por Lead',
                        'chart_type': 'line',
                        'data': self._generate_cpl_trend_data()
                    },
                    {
                        'type': 'chart',
                        'title': 'Funil de Conversão',
                        'chart_type': 'funnel',
                        'data': self._generate_conversion_funnel_data()
                    }
                ]
            },  # Não faltava a virgula aqui, faltava na linha 155
            'optimization': {
                'title': 'Recomendações de Otimização',
                'components': [
                    {
                        'type': 'header',
                        'content': 'Plano de Otimização de Campanhas'
                    },
                    {
                        'type': 'table',
                        'title': 'Recomendações Prioritárias',
                        'data': self._generate_recommendations_table_data()
                    },
                    {
                        'type': 'chart',
                        'title': 'Impacto Projetado das Otimizações',
                        'chart_type': 'bar',
                        'data': self._generate_optimization_impact_data()
                    },
                    {
                        'type': 'timeline',
                        'title': 'Cronograma de Otimização',
                        'data': self._generate_optimization_timeline_data()
                    }
                    
                ]
            }, #Fecha o dicionário 'optimization'
            'reports': {
                'title': 'Relatórios e Exportação',
                'components': [
                    {
                        'type': 'header',
                        'content': 'Relatórios e Exportação de Dados'
                    },
                    {
                        'type': 'report_cards',
                        'items': self._generate_report_cards()
                    },
                    {
                        'type': 'export_options',
                        'formats': ['PDF', 'Excel', 'CSV', 'JSON', 'PowerPoint']
                    }
                ]
            }
        }
        
        return layouts
    
    def _generate_kpi_cards(self):
        """Gera dados para os cards de KPI"""
        
        # Extrair dados relevantes
        opportunities = self.data.get('opportunities', [])
        marketing = self.data.get('marketing', [])
        
        # Calcular KPIs
        total_opportunities = len(opportunities)
        avg_roi = sum(opp.get('estimated_roi', 0) for opp in opportunities) / max(total_opportunities, 1)
        avg_investment = sum(opp.get('investment', {}).get('min', 0) for opp in opportunities) / max(total_opportunities, 1)
        
        # Criar cards de KPI
        kpi_cards = [
            {
                'title': 'Oportunidades Identificadas',
                'value': total_opportunities,
                'trend': '+12%',
                'trend_direction': 'up',
                'period': 'vs. mês anterior'
            },
            {
                'title': 'ROI Médio Projetado',
                'value': f"{avg_roi:.1f}%",
                'trend': '+5.2%',
                'trend_direction': 'up',
                'period': 'vs. mês anterior'
            },
            {
                'title': 'Investimento Médio',
                'value': f"R$ {avg_investment:,.2f}".replace(',', '.').replace('.', ','),
                'trend': '-3.5%',
                'trend_direction': 'down',
                'period': 'vs. mês anterior'
            },
            {
                'title': 'Leads Gerados',
                'value': '324',
                'trend': '+18.7%',
                'trend_direction': 'up',
                'period': 'vs. mês anterior'
            }
        ]
        
        return kpi_cards
    
    def _generate_opportunities_chart_data(self):
        """Gera dados para o gráfico de oportunidades"""
        
        # Extrair oportunidades
        opportunities = self.data.get('opportunities', [])
        
        # Selecionar as top 5 oportunidades ou criar exemplos
        if opportunities:
            top_opportunities = sorted(opportunities, key=lambda x: x.get('estimated_roi', 0), reverse=True)[:5]
            
            chart_data = {
                'labels': [opp.get('name', f'Oportunidade {i+1}') for i, opp in enumerate(top_opportunities)],
                'datasets': [
                    {
                        'label': 'ROI Estimado (%)',
                        'data': [opp.get('estimated_roi', 0) for opp in top_opportunities]
                    },
                    {
                        'label': 'Investimento Mínimo (R$ mil)',
                        'data': [opp.get('investment', {}).get('min', 0) / 1000 for opp in top_opportunities]
                    }
                ]
            }
        else:
            # Dados de exemplo
            chart_data = {
                'labels': ['Franquia A', 'Franquia B', 'Franquia C', 'Franquia D', 'Franquia E'],
                'datasets': [
                    {
                        'label': 'ROI Estimado (%)',
                        'data': [28.5, 26.2, 24.8, 22.3, 21.0]
                    },
                    {
                        'label': 'Investimento Mínimo (R$ mil)',
                        'data': [150, 80, 200, 120, 100]
                    }
                ]
            }
        
        return chart_data
    
    def _generate_marketing_performance_data(self):
        """Gera dados para o gráfico de desempenho de marketing"""
        
        # Extrair dados de marketing
        marketing = self.data.get('marketing', [])
        
        # Criar dados do gráfico de exemplo
        chart_data = {
            'labels': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'datasets': [
                {
                    'label': 'Facebook/Instagram',
                    'data': [45, 52, 58, 60, 65, 70]
                },
                {
                    'label': 'Google Ads',
                    'data': [30, 35, 38, 45, 48, 52]
                },
                {
                    'label': 'LinkedIn',
                    'data': [20, 22, 25, 28, 30, 35]
                },
                {
                    'label': 'Email Marketing',
                    'data': [15, 18, 20, 22, 25, 28]
                }
            ]
        }
        
        return chart_data
    
    def _generate_opportunities_table_data(self):
        """Gera dados para a tabela de oportunidades"""
        
        # Extrair oportunidades
        opportunities = self.data.get('opportunities', [])
        
        # Criar dados da tabela
        if opportunities:
            table_data = {
                'columns': ['Franquia', 'Setor', 'Investimento Min.', 'Investimento Max.', 'ROI Estimado', 'Payback', 'Score'],
                'rows': []
            }
            
            for opp in opportunities:
                row = [
                    opp.get('name', 'Não especificado'),
                    opp.get('sector', 'Não especificado'),
                    f"R$ {opp.get('investment', {}).get('min', 0):,.2f}".replace(',', '.').replace('.', ','),
                    f"R$ {opp.get('investment', {}).get('max', 0):,.2f}".replace(',', '.').replace('.', ','),
                    f"{opp.get('estimated_roi', 0):.1f}%",
                    f"{opp.get('payback_months', 0)} meses",
                    f"{opp.get('score', 0):.2f}"
                ]
                table_data['rows'].append(row)
        else:
            # Dados de exemplo
            table_data = {
                'columns': ['Franquia', 'Setor', 'Investimento Min.', 'Investimento Max.', 'ROI Estimado', 'Payback', 'Score'],
                'rows': [
                    ['PetFood Express', 'Pet Shop', 'R$ 80.000,00', 'R$ 150.000,00', '32.0%', '24 meses', '0.82'],
                    ['CleanTech', 'Limpeza Ecológica', 'R$ 50.000,00', 'R$ 120.000,00', '28.0%', '30 meses', '0.75'],
                    ['EducaMais', 'Educação', 'R$ 120.000,00', 'R$ 280.000,00', '25.0%', '36 meses', '0.78'],
                    ['FastFit Academia', 'Fitness', 'R$ 200.000,00', 'R$ 450.000,00', '22.0%', '40 meses', '0.77'],
                    ['TechRepair', 'Assistência Técnica', 'R$ 40.000,00', 'R$ 90.000,00', '35.0%', '20 meses', '0.70']
                ]
            }
        
        return table_data
    
    def _generate_roi_by_sector_data(self):
        """Gera dados para o gráfico de ROI por setor"""
        
        # Extrair oportunidades
        opportunities = self.data.get('opportunities', [])
        
        # Agrupar por setor
        sectors = {}
        
        if opportunities:
            for opp in opportunities:
                sector = opp.get('sector', 'Não especificado')
                roi = opp.get('estimated_roi', 0)
                
                if sector not in sectors:
                    sectors[sector] = {'count': 0, 'total_roi': 0}
                
                sectors[sector]['count'] += 1
                sectors[sector]['total_roi'] += roi
            
            # Calcular médias
            for sector in sectors:
                sectors[sector]['avg_roi'] = sectors[sector]['total_roi'] / sectors[sector]['count']
            
            # Criar dados do gráfico
            chart_data = {
                'labels': list(sectors.keys()),
                'datasets': [
                    {
                        'label': 'ROI Médio (%)',
                        'data': [sectors[sector]['avg_roi'] for sector in sectors]
                    }
                ]
            }
        else:
            # Dados de exemplo
            chart_data = {
                'labels': ['Pet Shop', 'Educação', 'Alimentação', 'Fitness', 'Tecnologia', 'Serviços'],
                'datasets': [
                    {
                        'label': 'ROI Médio (%)',
                        'data': [32.5, 25.8, 22.3, 24.1, 29.8, 27.4]
                    }
                ]
            }
        
        return chart_data
    
    def _generate_investment_return_data(self):
        """Gera dados para o gráfico de investimento vs retorno"""
        
        # Extrair oportunidades
        opportunities = self.data.get('opportunities', [])
        
        # Criar dados do gráfico
        if opportunities:
            chart_data = {
                'datasets': [
                    {
                        'label': 'Oportunidades',
                        'data': [
                            {
                                'x': opp.get('investment', {}).get('min', 0) / 1000,  # em R$ mil
                                'y': opp.get('estimated_roi', 0),
                                'r': 10,  # tamanho do ponto
                                'name': opp.get('name', f'Oportunidade {i+1}')
                            }
                            for i, opp in enumerate(opportunities)
                        ]
                    }
                ],
                'xAxisLabel': 'Investimento Mínimo (R$ mil)',
                'yAxisLabel': 'ROI Estimado (%)'
            }
        else:
            # Dados de exemplo
            chart_data = {
                'datasets': [
                    {
                        'label': 'Oportunidades',
                        'data': [
                            {'x': 80, 'y': 32.0, 'r': 10, 'name': 'PetFood Express'},
                            {'x': 50, 'y': 28.0, 'r': 10, 'name': 'CleanTech'},
                            {'x': 120, 'y': 25.0, 'r': 10, 'name': 'EducaMais'},
                            {'x': 200, 'y': 22.0, 'r': 10, 'name': 'FastFit Academia'},
                            {'x': 40, 'y': 35.0, 'r': 10, 'name': 'TechRepair'},
                            {'x': 150, 'y': 24.0, 'r': 10, 'name': 'CafeTeria'},
                            {'x': 90, 'y': 30.0, 'r': 10, 'name': 'BeautyStyle'},
                            {'x': 180, 'y': 18.0, 'r': 10, 'name': 'FoodExpress'}
                        ]
                    }
                ],
                'xAxisLabel': 'Investimento Mínimo (R$ mil)',
                'yAxisLabel': 'ROI Estimado (%)'
            }
        
        return chart_data
    
    def _generate_platform_performance_data(self):
        """Gera dados para o gráfico de desempenho por plataforma"""
        
        # Dados de exemplo
        chart_data = {
            'labels': ['Facebook', 'Instagram', 'Google Search', 'Google Display', 'LinkedIn', 'Email', 'WhatsApp'],
            'datasets': [
                {
                    'label': 'CTR (%)',
                    'data': [1.8, 1.5, 5.2, 0.7, 0.9, 3.2, 12.5]
                },
                {
                    'label': 'Custo por Lead (R$)',
                    'data': [75, 85, 95, 60, 180, 40, 35]
                },
                {
                    'label': 'Taxa de Conversão (%)',
                    'data': [3.5, 3.2, 4.8, 2.1, 4.5, 2.8, 6.5]
                }
            ]
        }
        
        return chart_data
    
    def _generate_cpl_trend_data(self):
        """Gera dados para o gráfico de tendência de CPL"""
        
        # Dados de exemplo
        chart_data = {
            'labels': ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4', 'Semana 5', 'Semana 6'],
            'datasets': [
                {
                    'label': 'Facebook/Instagram',
                    'data': [90, 85, 82, 78, 75, 72]
                },
                {
                    'label': 'Google Ads',
                    'data': [110, 105, 102, 98, 95, 92]
                },
                {
                    'label': 'LinkedIn',
                    'data': [210, 200, 195, 190, 185, 180]
                },
                {
                    'label': 'Email Marketing',
                    'data': [45, 43, 42, 40, 38, 35]
                }
            ]
        }
        
        return chart_data
    
    def _generate_conversion_funnel_data(self):
        """Gera dados para o funil de conversão"""
        
        # Dados de exemplo
        funnel_data = {
            'labels': ['Impressões', 'Cliques', 'Visitas à Landing Page', 'Leads', 'Reuniões Agendadas', 'Franqueados'],
            'values': [500000, 25000, 20000, 2000, 200, 10]
        }
        
        return funnel_data
    
    def _generate_recommendations_table_data(self):
        """Gera dados para a tabela de recomendações"""
        
        # Extrair dados de otimização
        automation = self.data.get('automation', {})
        
        # Criar dados da tabela
        table_data = {
            'columns': ['Plataforma', 'Recomendação', 'Impacto Projetado', 'Prioridade', 'Status'],
            'rows': [
                ['Facebook', 'Aumentar orçamento em 20%', 'Aumento de 15% em leads', 'Alta', 'Pendente'],
                ['Google Search', 'Adicionar palavras-chave negativas', 'Redução de 10% no CPC', 'Média', 'Em Andamento'],
                ['LinkedIn', 'Otimizar formulário de conversão', 'Aumento de 25% na taxa de conversão', 'Alta', 'Pendente'],
                ['Instagram', 'Testar novos criativos', 'Aumento de 18% no CTR', 'Média', 'Pendente'],
                ['Email', 'Melhorar linha de assunto', 'Aumento de 22% na taxa de abertura', 'Baixa', 'Concluído']
            ]
        }
        
        return table_data
    
    def _generate_optimization_impact_data(self):
        """Gera dados para o gráfico de impacto das otimizações"""
        
        # Dados de exemplo
        chart_data = {
            'labels': ['Cenário Atual', 'Após Otimizações'],
            'datasets': [
                {
                    'label': 'Custo por Lead (R$)',
                    'data': [85, 68]
                },
                {
                    'label': 'Taxa de Conversão (%)',
                    'data': [3.5, 4.7]
                },
                {
                    'label': 'ROI (%)',
                    'data': [280, 350]
                }
            ]
        }
        
        return chart_data
    
    def _generate_optimization_timeline_data(self):
        """Gera dados para o cronograma de otimização"""
        
        # Data atual
        current_date = datetime.now()
        
        # Criar dados do cronograma
        timeline_data = {
            'stages': [
                {
                    'name': 'Monitoramento Inicial',
                    'start_date': current_date.strftime('%Y-%m-%d'),
                    'end_date': (current_date + timedelta(days=3)).strftime('%Y-%m-%d'),
                    'status': 'Em Andamento'
                },
                {
                    'name': 'Primeira Rodada de Otimizações',
                    'start_date': (current_date + timedelta(days=4)).strftime('%Y-%m-%d'),
                    'end_date': (current_date + timedelta(days=7)).strftime('%Y-%m-%d'),
                    'status': 'Pendente'
                },
                {
                    'name': 'Otimização de Conversão',
                    'start_date': (current_date + timedelta(days=8)).strftime('%Y-%m-%d'),
                    'end_date': (current_date + timedelta(days=14)).strftime('%Y-%m-%d'),
                    'status': 'Pendente'
                },
                {
                    'name': 'Expansão e Escala',
                    'start_date': (current_date + timedelta(days=15)).strftime('%Y-%m-%d'),
                    'end_date': (current_date + timedelta(days=21)).strftime('%Y-%m-%d'),
                    'status': 'Pendente'
                },
                {
                    'name': 'Otimização Final e Relatório',
                    'start_date': (current_date + timedelta(days=22)).strftime('%Y-%m-%d'),
                    'end_date': (current_date + timedelta(days=30)).strftime('%Y-%m-%d'),
                    'status': 'Pendente'
                }
            ]
        }
        
        return timeline_data
    
    def _generate_report_cards(self):
        """Gera dados para os cards de relatórios"""
        
        # Criar cards de relatórios
        report_cards = [
            {
                'title': 'Relatório de Oportunidades',
                'description': 'Análise completa das oportunidades de franquia identificadas',
                'last_updated': (datetime.now() - timedelta(days=2)).strftime('%d/%m/%Y'),
                'formats': ['PDF', 'Excel']
            },
            {
                'title': 'Relatório de Desempenho de Marketing',
                'description': 'Métricas detalhadas de campanhas por plataforma',
                'last_updated': datetime.now().strftime('%d/%m/%Y'),
                'formats': ['PDF', 'PowerPoint', 'Excel']
            },
            {
                'title': 'Plano de Otimização',
                'description': 'Recomendações e cronograma para otimização de campanhas',
                'last_updated': datetime.now().strftime('%d/%m/%Y'),
                'formats': ['PDF', 'Excel']
            },
            {
                'title': 'Análise ROI por Setor',
                'description': 'Comparativo detalhado de ROI por setor de franquia',
                'last_updated': (datetime.now() - timedelta(days=5)).strftime('%d/%m/%Y'),
                'formats': ['PDF', 'Excel']
            }
        ]
        
        return report_cards
    
    def run_server(self, debug=False, host='127.0.0.1', port=8050):
        """
        Simula a execução do servidor Dash
        
        Args:
            debug (bool): Modo de depuração
            host (str): Host para o servidor
            port (int): Porta para o servidor
        """
        print(f"Dashboard: Iniciando servidor em {host}:{port}" + (" (modo debug)" if debug else ""))
        print("Dashboard: SIMULAÇÃO - O servidor não está realmente rodando")
    
    def _save_dashboard_data(self):
        """Salva os dados do dashboard para uso posterior (opcional)"""
        
        # Diretório para salvar dados
        base_dir = os.path.join('output', 'dashboard')
        
        # Verificar se o diretório existe, se não, criar
        try:
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
                print(f"Diretório criado: {base_dir}")
            
            # Nome do arquivo baseado na data
            filename = f"dashboard_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path = os.path.join(base_dir, filename)
            
            # Criar uma versão serializável dos layouts
            serializable_layouts = {}
            for key, layout in self.layouts.items():
                serializable_layouts[key] = {
                    'title': layout['title'],
                    'components_count': len(layout['components'])
                }
            
            # Dados para salvar
            save_data = {
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'layouts': serializable_layouts,
                'data_summary': {
                    'opportunities_count': len(self.data.get('opportunities', [])),
                    'marketing_outputs_count': len(self.data.get('marketing', []))
                }
            }
            
            # Salvar dados em JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
                
            print(f"Dados do dashboard salvos em: {file_path}")
            
        except Exception as e:
            print(f"Erro ao salvar dados do dashboard: {e}")
