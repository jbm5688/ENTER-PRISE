# marketing/creative_generator.py
import random
from datetime import datetime, timedelta
import os

class CreativeGenerator:
    """
    Classe responsável por gerar materiais de marketing para oportunidades de franquias
    """
    
    def __init__(self):
        """
        Inicializa o gerador de criativos
        """
        # Templates de títulos para diferentes tipos de conteúdo
        self.ad_title_templates = [
            "Conquiste seu futuro financeiro com a franquia {name}",
            "Seja dono do seu negócio: {name} tem a oportunidade perfeita",
            "Invista no seu sucesso: Conheça a franquia {name}",
            "Liberdade financeira é possível com a franquia {name}",
            "{name}: A franquia que está revolucionando o setor de {sector}",
            "Empreenda com segurança: {name} é a escolha certa",
            "Seu próximo negócio de sucesso: Franquia {name}"
        ]
        
        # Templates de descrições para anúncios
        self.ad_description_templates = [
            "Investimento a partir de R$ {min_investment}. Retorno em apenas {payback} meses. Seja parte da rede {name} e conquiste sua independência financeira.",
            "O mercado de {sector} não para de crescer. A {name} oferece suporte completo com um modelo de negócio comprovado. Comece agora!",
            "Mais de {success_count} empreendedores já alcançaram o sucesso com a {name}. Invista a partir de R$ {min_investment} e transforme seu futuro.",
            "Modelo de negócio validado, baixo risco e alto retorno. A {name} é sua oportunidade de empreender com segurança no setor de {sector}.",
            "Suporte completo, treinamento especializado e marca reconhecida. Tudo isso com a franquia {name}, líder no segmento de {sector}.",
            "Cansado do seu emprego? A franquia {name} é sua porta de saída. Investimento a partir de R$ {min_investment} e retorno em {payback} meses."
        ]
        
        # Templates para chamadas para ação (CTAs)
        # marketing/creative_generator.py (continuação)
        # Templates para chamadas para ação (CTAs)
        self.cta_templates = [
            "Quero ser franqueado",
            "Solicitar informações",
            "Falar com um consultor",
            "Saiba mais",
            "Investir agora",
            "Conhecer a franquia",
            "Ver oportunidades"
        ]
        
        # Templates para posts em redes sociais
        self.social_post_templates = [
            "Você já pensou em ser dono do seu próprio negócio? A franquia {name} pode ser a oportunidade que você estava esperando! 💼 Com investimento a partir de R$ {min_investment} e retorno em {payback} meses, é hora de transformar sua vida financeira. #EmpreendaComSegurança #Franquia{tag}",
            
            "O mercado de {sector} cresce {growth_rate}% ao ano! A franquia {name} traz um modelo de negócio validado, com mais de {success_count} unidades de sucesso pelo país. Quer saber como fazer parte dessa história? Clique no link da bio! 🚀 #Empreendedorismo #Franquia{tag}",
            
            "Liberdade financeira, flexibilidade de horários e um negócio próprio. Esse é o pacote completo que a franquia {name} oferece! 🎯 Com ROI de {roi}%, seu investimento retorna muito mais rápido do que você imagina. #Franquia{tag} #OportunidadeDeNegócio",
            
            "Cansado de trabalhar para realizar o sonho de outra pessoa? 🤔 A franquia {name} é sua chance de empreender com segurança no setor de {sector}! Investimento a partir de R$ {min_investment}. #SejaFranqueado #Franquia{tag}"
        ]
        
        # Templates para emails
        self.email_templates = [
            {
                "subject": "Conheça a franquia {name} - Oportunidade exclusiva no setor de {sector}",
                "body": """
Olá, empreendedor!

Você está em busca de uma oportunidade para investir no seu futuro? A franquia {name} é líder no segmento de {sector}, com um modelo de negócio comprovado e retorno acelerado.

✅ Investimento a partir de R$ {min_investment}
✅ Retorno em apenas {payback} meses
✅ ROI estimado de {roi}%
✅ Mais de {success_count} unidades em operação

Nossa equipe está pronta para tirar todas as suas dúvidas e apresentar detalhes sobre essa oportunidade.

Clique no botão abaixo para agendar uma conversa com um de nossos consultores.

[AGENDAR CONVERSA]

Atenciosamente,
Equipe {name}
                """
            },
            {
                "subject": "Transforme seu futuro com a franquia {name} - Oportunidade no setor de {sector}",
                "body": """
Olá!

O mercado de {sector} continua em expansão, mesmo em tempos desafiadores. A franquia {name} traz uma oportunidade para você empreender com segurança nesse setor promissor.

Por que escolher a franquia {name}?

- Modelo de negócio validado com mais de {success_count} unidades
- Suporte completo em todas as etapas
- Treinamento especializado para você e sua equipe
- Marketing e estratégias de vendas já desenvolvidos
- Território exclusivo para sua operação

Investimento a partir de R$ {min_investment}, com retorno projetado em apenas {payback} meses.

Responda este email ou clique no botão abaixo para saber mais detalhes e agendar uma apresentação personalizada.

[QUERO SABER MAIS]

Atenciosamente,
Equipe {name}
                """
            }
        ]
        
        # Templates para vídeos
        self.video_script_templates = [
            {
                "title": "Por que investir na franquia {name}?",
                "duration": "60 segundos",
                "script": """
[ABERTURA - 5s]
Logotipo da {name} com efeito dinâmico.

[NARRAÇÃO - 10s]
"Você já sonhou em ter seu próprio negócio, mas tem medo dos riscos? A franquia {name} pode ser a resposta que você procura."

[CENA 1 - 10s]
Mostrar franqueados bem-sucedidos em suas unidades, sorridentes e atendendo clientes.
"Mais de {success_count} empreendedores já transformaram suas vidas com a {name}."

[CENA 2 - 10s]
Gráficos animados mostrando crescimento do setor e ROI.
"O mercado de {sector} cresce {growth_rate}% ao ano, e nossos franqueados têm ROI médio de {roi}%."

[CENA 3 - 10s]
Imagens do treinamento e suporte oferecidos.
"Oferecemos suporte completo, desde a escolha do ponto até a inauguração e operação diária."

[CENA 4 - 10s]
Depoimento rápido de um franqueado de sucesso.
"A {name} mudou minha vida. Hoje tenho liberdade financeira e tempo para minha família."

[FECHAMENTO - 5s]
"Investimento a partir de R$ {min_investment}. Transforme seu futuro com a franquia {name}."
[MOSTRAR SITE E CTA]
                """
            },
            {
                "title": "Conheça a franquia {name} - Sua oportunidade no setor de {sector}",
                "duration": "30 segundos",
                "script": """
[ABERTURA - 3s]
Logo da {name} com slogan.

[NARRAÇÃO - 5s]
"O mercado de {sector} está em expansão. Você está pronto para aproveitar essa oportunidade?"

[CENA 1 - 7s]
Mostrar unidades da franquia em operação, clientes satisfeitos.
"A {name} é líder no segmento, com modelo de negócio validado e suporte completo."

[CENA 2 - 7s]
Mostrar números de crescimento e resultados.
"Investimento a partir de R$ {min_investment}, com retorno em apenas {payback} meses."

[CENA 3 - 5s]
Mostrar equipe de suporte e treinamento.
"Você não estará sozinho. Nossa equipe te acompanha em cada passo."

[FECHAMENTO - 3s]
"Seja parte do sucesso. {name} - seu futuro começa aqui."
[MOSTRAR SITE E TELEFONE]
                """
            }
        ]
        
        # Templates para banners
        self.banner_templates = [
            {
                "name": "Banner principal",
                "dimensions": "1200x628px",
                "elements": [
                    "Logotipo da franquia em destaque",
                    "Imagem de franqueado bem-sucedido ou unidade modelo",
                    "Título: 'Seja dono do seu negócio com a franquia {name}'",
                    "Subtítulo: 'Investimento a partir de R$ {min_investment} | ROI de {roi}%'",
                    "CTA: 'Quero ser franqueado'"
                ]
            },
            {
                "name": "Banner lateral",
                "dimensions": "300x600px",
                "elements": [
                    "Logotipo da franquia no topo",
                    "Imagem de unidade em operação",
                    "Título: 'Empreenda no setor de {sector}'",
                    "Bullets: '✓ Retorno em {payback} meses', '✓ Suporte completo', '✓ Marca reconhecida'",
                    "CTA: 'Saiba mais'"
                ]
            }
        ]
        
    def generate(self, opportunity):
        """
        Gera materiais de marketing para uma oportunidade
        
        Args:
            opportunity (dict): Dados da oportunidade
            
        Returns:
            dict: Criativos gerados para a oportunidade
        """
        print(f"CreativeGenerator: Gerando criativos para {opportunity.get('name', 'oportunidade')}")
        
        # Extrair dados necessários para os templates
        template_data = self._extract_template_data(opportunity)
        
        # Gerar diferentes tipos de criativos
        creatives = {
            'ads': self._generate_ads(template_data),
            'social_posts': self._generate_social_posts(template_data),
            'emails': self._generate_emails(template_data),
            'video_scripts': self._generate_video_scripts(template_data),
            'banners': self._generate_banners(template_data),
            'landing_page': self._generate_landing_page(template_data)
        }
        
        # Salvar criativos em pasta específica (opcional)
        self._save_creatives(opportunity.get('name', 'unnamed_opportunity'), creatives)
        
        return creatives
    
    def _extract_template_data(self, opportunity):
        """Extrai dados da oportunidade para uso nos templates"""
        
        # Dados básicos
        name = opportunity.get('name', 'Franquia')
        sector = opportunity.get('sector', 'Serviços')
        
        # Dados financeiros
        min_investment = opportunity.get('investment', {}).get('min', 100000)
        max_investment = opportunity.get('investment', {}).get('max', 200000)
        roi = opportunity.get('estimated_roi', 0.25) * 100  # Converter para percentual
        payback_months = opportunity.get('payback_months', 36)
        monthly_revenue = opportunity.get('monthly_revenue', 15000)
        monthly_profit = opportunity.get('monthly_profit', 5000)
        
        # Dados de mercado
        market_growth = opportunity.get('market_growth_factor', 0.1) * 100  # Converter para percentual
        
        # Dados fictícios para complementar
        success_count = random.randint(20, 500)  # Número de unidades/franqueados
        franchisee_satisfaction = random.uniform(4.0, 4.9)  # Satisfação dos franqueados (0-5)
        
        # Criar tag para hashtags
        tag = name.replace(' ', '').replace('-', '')
        
        # Dados compilados para os templates
        template_data = {
            'name': name,
            'sector': sector,
            'min_investment': f"{min_investment:,.2f}".replace(',', '.').replace('.', ','),
            'max_investment': f"{max_investment:,.2f}".replace(',', '.').replace('.', ','),
            'roi': round(roi),
            'payback': payback_months,
            'monthly_revenue': f"{monthly_revenue:,.2f}".replace(',', '.').replace('.', ','),
            'monthly_profit': f"{monthly_profit:,.2f}".replace(',', '.').replace('.', ','),
            'growth_rate': round(market_growth),
            'success_count': success_count,
            'satisfaction': round(franchisee_satisfaction, 1),
            'tag': tag
        }
        
        return template_data
    
    def _generate_ads(self, template_data):
        """Gera anúncios para diferentes plataformas"""
        
        ads = []
        
        # Gerar 3-5 variações de anúncios
        num_variations = random.randint(3, 5)
        
        for i in range(num_variations):
            # Selecionar templates aleatoriamente
            title_template = random.choice(self.ad_title_templates)
            description_template = random.choice(self.ad_description_templates)
            cta = random.choice(self.cta_templates)
            
            # Preencher os templates
            title = title_template.format(**template_data)
            description = description_template.format(**template_data)
            
            # Criar anúncio
            ad = {
                'id': f"ad_{i+1}",
                'title': title,
                'description': description,
                'cta': cta,
                'url': f"https://www.{template_data['name'].lower().replace(' ', '')}.com.br/franqueado"
            }
            
            ads.append(ad)
        
        return ads
    
    def _generate_social_posts(self, template_data):
        """Gera posts para redes sociais"""
        
        social_posts = []
        
        # Plataformas de redes sociais
        platforms = ['Instagram', 'Facebook', 'LinkedIn', 'Twitter']
        
        # Gerar um post para cada plataforma
        for platform in platforms:
            # Selecionar template aleatoriamente
            post_template = random.choice(self.social_post_templates)
            
            # Preencher o template
            post_text = post_template.format(**template_data)
            
            # Adicionar hashtags específicas da plataforma
            if platform == 'Instagram':
                post_text += " #Empreendedorismo #NegócioPróprio #Franquia #Investimento"
            elif platform == 'LinkedIn':
                post_text += " #Empreendedorismo #Negócios #Franchising #OportunidadeDeInvestimento"
            elif platform == 'Facebook':
                post_text += " #EmpreendaComSegurança #FranquiaDeSucesso"
            
            # Criar post
            post = {
                'platform': platform,
                'text': post_text,
                'recommended_image': f"Imagem de uma unidade da franquia {template_data['name']} em operação, com clientes.",
                'url': f"https://www.{template_data['name'].lower().replace(' ', '')}.com.br/franqueado"
            }
            
            social_posts.append(post)
        
        # Adicionar posts para datas especiais
        special_dates = [
            {'name': 'Dia do Empreendedor', 'date': '05/10'},
            {'name': 'Black Friday', 'date': 'Última sexta de novembro'},
            {'name': 'Fim de Ano', 'date': 'Última semana de dezembro'}
        ]
        
        for special in special_dates:
            post = {
                'platform': 'Todas',
                'special_date': special['name'],
                'text': f"Em comemoração ao {special['name']}, a franquia {template_data['name']} tem condições especiais para novos franqueados! 🎉 Investimento facilitado e bônus exclusivos para quem fechar até o final da campanha. Essa é sua chance de entrar no mercado de {template_data['sector']} com uma marca reconhecida. #Franquia{template_data['tag']} #{special['name'].replace(' ', '')}"
            }
            social_posts.append(post)
        
        return social_posts
    
    def _generate_emails(self, template_data):
        """Gera templates de emails para campanhas"""
        
        emails = []
        
        # Para cada template de email
        for template in self.email_templates:
            # Preencher o template
            subject = template['subject'].format(**template_data)
            body = template['body'].format(**template_data)
            
            # Criar email
            email = {
                'subject': subject,
                'body': body,
                'type': 'Prospecção de franqueados'
            }
            
            emails.append(email)
        
        # Adicionar email de acompanhamento
        follow_up_email = {
            'subject': f"Ainda tem dúvidas sobre a franquia {template_data['name']}?",
            'body': f"""
Olá!

Há alguns dias conversamos sobre a oportunidade de investir na franquia {template_data['name']}.

Gostaríamos de saber se você tem alguma dúvida adicional ou se precisa de mais informações para tomar sua decisão.

Nossa equipe está à disposição para ajudá-lo a entender melhor:

- Como funciona o modelo de negócio
- Detalhes sobre o investimento inicial
- Projeções financeiras detalhadas
- Processo de abertura e inauguração
- Suporte oferecido pela franqueadora

Responda este email ou clique no botão abaixo para agendar uma nova conversa.

[AGENDAR CONVERSA]

Atenciosamente,
Equipe {template_data['name']}
            """,
            'type': 'Follow-up após 7 dias'
        }
        
        emails.append(follow_up_email)
        
        return emails
    
    def _generate_video_scripts(self, template_data):
        """Gera roteiros para vídeos promocionais"""
        
        video_scripts = []
        
        # Para cada template de vídeo
        for template in self.video_script_templates:
            # Preencher o template
            title = template['title'].format(**template_data)
            script = template['script'].format(**template_data)
            
            # Criar roteiro de vídeo
            video_script = {
                'title': title,
                'duration': template['duration'],
                'script': script,
                'platforms': ['YouTube', 'Instagram', 'Facebook', 'Site']
            }
            
            video_scripts.append(video_script)
        
        # Adicionar roteiro para depoimento de franqueado
        testimonial_script = {
            'title': f"Depoimento real - Franqueado {template_data['name']}",
            'duration': '90 segundos',
            'script': f"""
[ABERTURA - 5s]
Mostrar logotipo da {template_data['name']} e título "Histórias de Sucesso"

[INTRODUÇÃO - 10s]
Narrador: "Conheça a história de João Silva, franqueado da {template_data['name']} há 2 anos. Ele deixou o emprego corporativo para empreender e hoje comanda uma das unidades mais lucrativas da rede."

[DEPOIMENTO PARTE 1 - 20s]
João: "Sempre sonhei em ter meu próprio negócio, mas tinha medo dos riscos. Quando conheci a {template_data['name']}, vi que era possível empreender com segurança. O modelo de negócio já estava validado e o suporte da franqueadora me deu confiança."

[CENAS DA UNIDADE - 15s]
Mostrar a unidade em funcionamento, clientes satisfeitos, João interagindo com sua equipe.
Narrador: "A unidade de João atingiu o ponto de equilíbrio em X meses e hoje fatura Y% acima da média da rede."

[DEPOIMENTO PARTE 2 - 20s]
João: "O que mais me surpreendeu foi o suporte constante. Desde a escolha do ponto até o treinamento da equipe, a franqueadora esteve presente em cada etapa. Hoje tenho qualidade de vida e segurança financeira que nunca tive como funcionário."

[FECHAMENTO - 20s]
João: "Se você está pensando em empreender, considere a {template_data['name']}. Foi a melhor decisão que tomei."
Narrador: "Seja como João e tantos outros empreendedores de sucesso. Invista na franquia {template_data['name']} e transforme seu futuro."
[MOSTRAR SITE E TELEFONE]
            """,
            'platforms': ['YouTube', 'Site', 'Apresentações para potenciais franqueados']
        }
        
        video_scripts.append(testimonial_script)
        
        return video_scripts
    
    def _generate_banners(self, template_data):
        """Gera especificações para banners publicitários"""
        
        banners = []
        
        # Para cada template de banner
        for template in self.banner_templates:
            # Preencher elementos do template
            elements = []
            for element in template['elements']:
                elements.append(element.format(**template_data))
            
            # Criar especificações do banner
            banner = {
                'name': template['name'],
                'dimensions': template['dimensions'],
                'elements': elements,
                'colors': self._generate_color_palette(),
                'platforms': ['Google Ads', 'Facebook Ads', 'Site']
            }
            
            banners.append(banner)
        
        # Adicionar banner específico para remarketing
        remarketing_banner = {
            'name': 'Banner de remarketing',
            'dimensions': '728x90px',
            'elements': [
                f"Logotipo da {template_data['name']}",
                f"Título: 'Ainda pensando em investir na franquia {template_data['name']}?'",
                f"Subtítulo: 'Condições especiais por tempo limitado'",
                "CTA: 'Retomar conversa'"
            ],
            'colors': self._generate_color_palette(),
            'platforms': ['Google Ads', 'Facebook Ads']
        }
        
        banners.append(remarketing_banner)
        
        return banners
    
    def _generate_color_palette(self):
        """Gera uma paleta de cores para materiais gráficos"""
        
        # Paletas pré-definidas para escolha aleatória
        palettes = [
            {
                'primary': '#0078D7',
                'secondary': '#83C4FF',
                'accent': '#FF8C00',
                'text': '#333333',
                'background': '#FFFFFF'
            },
            {
                'primary': '#2E7D32',
                'secondary': '#A5D6A7',
                'accent': '#FFC107',
                'text': '#212121',
                'background': '#F5F5F5'
            },
            {
                'primary': '#C2185B',
                'secondary': '#F48FB1',
                'accent': '#00BCD4',
                'text': '#212121',
                'background': '#FFFFFF'
            },
            {
                'primary': '#3F51B5',
                'secondary': '#C5CAE9',
                'accent': '#FF5722',
                'text': '#212121',
                'background': '#F5F5F5'
            },
            {
                'primary': '#455A64',
                'secondary': '#CFD8DC',
                'accent': '#FFC107',
                'text': '#212121',
                'background': '#FFFFFF'
            }
        ]
        
        return random.choice(palettes)
    
    def _generate_landing_page(self, template_data):
        """Gera estrutura para uma landing page de captação de leads"""
        
        # Seções da landing page
        sections = [
            {
                'name': 'Hero',
                'elements': [
                    f"Título principal: 'Seja dono do seu próprio negócio com a franquia {template_data['name']}'",
                    "Subtítulo: 'Invista em um modelo de negócio comprovado no setor de " + template_data['sector'] + "'",
                    "Imagem de destaque: Unidade modelo da franquia com clientes satisfeitos",
                    "Formulário de captação: Nome, Email, Telefone, Cidade",
                    "CTA principal: 'Quero ser um franqueado'"
                ]
            },
            {
                'name': 'Números da Franquia',
                'elements': [
                    "Título da seção: 'Por que investir nessa oportunidade'",
                    f"Card 1: '{template_data['success_count']}+ unidades em operação'",
                    f"Card 2: 'ROI médio de {template_data['roi']}%'",
                    f"Card 3: 'Retorno em {template_data['payback']} meses'",
                    f"Card 4: 'Mercado em crescimento de {template_data['growth_rate']}% ao ano'"
                ]
            },
            {
                'name': 'Como Funciona',
                'elements': [
                    "Título da seção: 'Como funciona uma franquia " + template_data['name'] + "'",
                    "Passo 1: 'Primeiro contato e análise de perfil'",
                    "Passo 2: 'Apresentação detalhada e Circular de Oferta de Franquia (COF)'",
                    "Passo 3: 'Assinatura do contrato e planejamento'",
                    "Passo 4: 'Treinamento e preparação para abertura'",
                    "Passo 5: 'Inauguração e operação com suporte contínuo'",
                    "Ilustrações para cada passo"
                ]
            },
            {
                'name': 'Investimento',
                'elements': [
                    "Título da seção: 'Investimento e Retorno'",
                    f"Texto: 'A franquia {template_data['name']} oferece uma oportunidade de negócio com investimento a partir de R$ {template_data['min_investment']}.'",
                    "Tabela detalhando a composição do investimento",
                    f"Projeção financeira: 'Faturamento médio mensal: R$ {template_data['monthly_revenue']}'",
                    f"Projeção financeira: 'Lucro médio mensal: R$ {template_data['monthly_profit']}'",
                    "CTA secundário: 'Solicitar planilha financeira detalhada'"
                ]
            },
            {
                'name': 'Perfil do Franqueado',
                'elements': [
                    "Título da seção: 'Perfil do Franqueado Ideal'",
                    "Lista de características desejáveis:",
                    "- Espírito empreendedor",
                    "- Identificação com o setor de " + template_data['sector'],
                    "- Capacidade de investimento compatível",
                    "- Comprometimento com a operação",
                    "- Habilidades de gestão e liderança",
                    "Imagem representando o perfil ideal"
                ]
            },
            {
                'name': 'Depoimentos',
                'elements': [
                    "Título da seção: 'O que dizem nossos franqueados'",
                    "3-4 cards com depoimentos de franqueados atuais",
                    f"Texto de satisfação: 'Nota média de satisfação dos franqueados: {template_data['satisfaction']}/5'",
                    "Fotos dos franqueados em suas unidades"
                ]
            },
            {
                'name': 'FAQ',
                'elements': [
                    "Título da seção: 'Perguntas Frequentes'",
                    "Pergunta 1: 'Preciso ter experiência no setor?'",
                    "Pergunta 2: 'Qual o prazo médio para abertura após a assinatura?'",
                    "Pergunta 3: 'A franqueadora ajuda na escolha do ponto comercial?'",
                    "Pergunta 4: 'Quais os tipos de unidades disponíveis?'",
                    "Pergunta 5: 'Quais regiões estão disponíveis para expansão?'",
                    "Pergunta 6: 'Qual o suporte oferecido pela franqueadora?'"
                ]
            },
            {
                'name': 'Contato',
                'elements': [
                    "Título da seção: 'Transforme seu futuro hoje mesmo'",
                    "Formulário de contato completo",
                    "Informações da franqueadora",
                    "CTA final: 'Quero receber mais informações'",
                    "Política de privacidade e termos de uso"
                ]
            }
        ]
        
        # SEO e metadados
        seo = {
            'title': f"Franquia {template_data['name']} | Invista no setor de {template_data['sector']}",
            'description': f"Conheça a franquia {template_data['name']}, oportunidade de investimento no setor de {template_data['sector']} com ROI de {template_data['roi']}% e retorno em {template_data['payback']} meses.",
            'keywords': [f"franquia {template_data['name'].lower()}", f"franquia de {template_data['sector'].lower()}", "investimento em franquia", "seja franqueado", "oportunidade de negócio"],
            'structured_data': {
                'type': 'Business',
                'name': template_data['name'],
                'description': f"Rede de franquias no setor de {template_data['sector']}",
                'url': f"https://www.{template_data['name'].lower().replace(' ', '')}.com.br"
            }
        }
        
        # Landing page completa
        landing_page = {
            'title': f"Seja um franqueado {template_data['name']}",
            'sections': sections,
            'seo': seo,
            'tracking': {
                'google_analytics': 'Configurar',
                'facebook_pixel': 'Configurar',
                'conversion_events': [
                    'Visualização da página',
                    'Envio de formulário',
                    'Clique em CTA',
                    'Download de material'
                ]
            }
        }
        
        return landing_page
    
    def generate_creatives(self, opportunity, market_data=None):
        """
        Gera conteúdo criativo para uma oportunidade de franquia.
        
        Args:
            opportunity (dict): Dados da oportunidade
            market_data (dict): Dados de mercado adicionais
            
        Returns:
            dict: Conteúdo criativo gerado
        """
        print(f"CreativeGenerator: Gerando criativos para {opportunity.get('name', 'Oportunidade')}")
        
        # Chamar o método generate existente
        creative_content = self.generate(opportunity)
        
        return creative_content
    
    def _save_creatives(self, opportunity_name, creatives):
        """Salva os criativos gerados em arquivos (opcional)"""
        
        # Diretório base para salvar os criativos
        base_dir = os.path.join('output', 'creatives', opportunity_name.replace(' ', '_').lower())
        
        # Verificar se o diretório existe, se não, criar
        try:
            if not os.path.exists(base_dir):
                os.makedirs(base_dir)
                print(f"Diretório criado: {base_dir}")
        except Exception as e:
            print(f"Erro ao criar diretório: {e}")
            return
        
        # Por enquanto, não implementaremos a gravação dos arquivos
        # Esta função pode ser expandida no futuro
        pass
