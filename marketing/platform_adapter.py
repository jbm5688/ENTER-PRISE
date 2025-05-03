import logging
import random
from datetime import datetime

logger = logging.getLogger("franquia_finder")

class PlatformAdapter:
    """
    Classe responsável por adaptar conteúdo criativo para diferentes plataformas.
    """
    
    def __init__(self, platforms=None, config=None):
        """
        Inicializa o adaptador de plataformas.
        
        Args:
            platforms (list): Lista de plataformas ativas
            config (dict): Configurações para adaptação de conteúdo
        """
        self.config = config or {}
        self.platforms = platforms or ["facebook", "instagram", "google", "linkedin", "email"]
    
    def adapt_content(self, creative_content, opportunity):
        """
        Adapta conteúdo criativo para diferentes plataformas.
        
        Args:
            creative_content (dict): Conteúdo criativo gerado
            opportunity (dict): Dados da oportunidade
            
        Returns:
            dict: Conteúdo adaptado para cada plataforma
        """
        print(f"PlatformAdapter: Adaptando criativos para diferentes plataformas")
        
        # Verificar se há conteúdo criativo
        if not creative_content:
            return {}
        
        # Extrair informações relevantes
        opportunity_name = opportunity.get('name', '')
        category = opportunity.get('category', '')
        value_proposition = creative_content.get('value_proposition', '')
        headlines = creative_content.get('headlines', [])
        descriptions = creative_content.get('descriptions', [])
        cta_examples = creative_content.get('cta_examples', [])
        
        # Dicionário para armazenar adaptações por plataforma
        platform_content = {}
        
        # Adaptar para cada plataforma ativa
        for platform in self.platforms:
            adapter_method = getattr(self, f"_adapt_for_{platform}", None)
            
            if adapter_method:
                platform_content[platform] = adapter_method(
                    opportunity_name, 
                    category, 
                    value_proposition, 
                    headlines, 
                    descriptions, 
                    cta_examples, 
                    creative_content
                )
        
        return platform_content
    
    def _adapt_for_facebook(self, name, category, value_proposition, headlines, descriptions, cta_examples, creative_content):
        """
        Adapta conteúdo para Facebook.
        
        Args:
            name (str): Nome da oportunidade
            category (str): Categoria do negócio
            value_proposition (str): Proposta de valor
            headlines (list): Lista de títulos
            descriptions (list): Lista de descrições
            cta_examples (list): Lista de CTAs
            creative_content (dict): Conteúdo criativo completo
            
        Returns:
            dict: Conteúdo adaptado para Facebook
        """
        # Selecionar elementos aleatórios
        headline = random.choice(headlines) if headlines else f"Invista na franquia {name}"
        description = random.choice(descriptions) if descriptions else f"Conheça a oportunidade de negócio {name} no setor de {category}."
        cta = random.choice(cta_examples) if cta_examples else "Saiba mais"
        
        # Gerar posts para feed
        feed_posts = [
            f"{headline}\n\n{description}\n\n#franquia#{category.replace(' ', '')}\n\n{cta}",
            f"🚀 OPORTUNIDADE DE NEGÓCIO 🚀\n\n{value_proposition}\n\nSeja um franqueado {name} e transforme sua carreira!\n\n#empreendedorismo #franquia#{category.replace(' ', '')}\n\n{cta}",
            f"Procurando um negócio próprio com modelo comprovado?\n\n{name} é a sua oportunidade no mercado de {category}.\n\n✅ Suporte completo\n✅ Treinamento\n✅ Marca reconhecida\n\n#franquia #empreender #{category.replace(' ', '')}\n\n{cta}"
        ]
        
        # Adaptar para diferentes formatos do Facebook
        facebook_content = {
            'platform': 'facebook',
            'content_type': 'social_media',
            'format': 'feed_post',
            'headline': headline,
            'description': description,
            'cta': cta,
            'feed_posts': feed_posts,
            'carousel_cards': self._generate_carousel_cards(name, category, value_proposition, cta),
            'topics': creative_content.get('content_topics', [])[:5],
            'recommended_hashtags': [
                f"franquia{name.replace(' ', '')}",
                "empreendedorismo",
                "franquia",
                "negóciopróprio",
                f"{category.replace(' ', '')}"
            ]
        }
        
        return facebook_content
    
    def _adapt_for_instagram(self, name, category, value_proposition, headlines, descriptions, cta_examples, creative_content):
        """
        Adapta conteúdo para Instagram.
        
        Args:
            name (str): Nome da oportunidade
            category (str): Categoria do negócio
            value_proposition (str): Proposta de valor
            headlines (list): Lista de títulos
            descriptions (list): Lista de descrições
            cta_examples (list): Lista de CTAs
            creative_content (dict): Conteúdo criativo completo
            
        Returns:
            dict: Conteúdo adaptado para Instagram
        """
        # Selecionar elementos aleatórios
        headline = random.choice(headlines) if headlines else f"Invista na franquia {name}"
        cta = random.choice(cta_examples) if cta_examples else "Saiba mais"
        
        # Gerar legendas para feed
        captions = [
            f"Você já pensou em ter seu próprio negócio?\n\n{value_proposition}\n\nConheça a franquia {name} e descubra como transformar sua carreira.\n\nLink na bio 👆\n\n.\n.\n.\n#franquia #{category.replace(' ', '')} #empreendedorismo #negóciolucrativo #investimento #liberdadefinanceira",
            f"🚀 OPORTUNIDADE DE NEGÓCIO 🚀\n\nApresentamos {name}: a franquia ideal para quem quer empreender no setor de {category}.\n\n✅ Baixo investimento\n✅ Alto retorno\n✅ Suporte completo\n\nClique no link da bio para saber mais!\n\n.\n.\n.\n#franquia #{category.replace(' ', '')} #empreender #oportunidade #negóciopróprio #investimento",
            f"Quer investir em um negócio próprio em 2025?\n\n{name} oferece um modelo de franquia testado e aprovado no mercado de {category}.\n\nDescubra como se tornar um franqueado de sucesso! 💼\n\nLink na bio!\n\n.\n.\n.\n#empreendedorismo #franquia #{category.replace(' ', '')} #negóciopróprio #sucesso #investimento"
        ]
        
        # Gerar ideias para stories
        stories_ideas = [
            f"Depoimento em vídeo de um franqueado {name} de sucesso",
            f"Tour pela unidade modelo da franquia {name}",
            f"Infográfico com os principais números da franquia",
            "Quiz sobre empreendedorismo e franchising",
            f"Contagem regressiva para o próximo evento de {name}"
        ]
        
        # Adaptar para diferentes formatos do Instagram
        instagram_content = {
            'platform': 'instagram',
            'content_type': 'social_media',
            'format': 'feed_post',
            'headline': headline,
            'feed_captions': captions,
            'stories_ideas': stories_ideas,
            'reels_concepts': [
                f"Antes/Depois: Transformação profissional ao se tornar franqueado {name}",
                f"Um dia na vida de um franqueado {name}",
                "5 mitos sobre franquias - desmistificados"
            ],
            'recommended_hashtags': [
                f"franquia{name.replace(' ', '')}",
                "empreendedorismo",
                "franquia",
                "negóciopróprio",
                f"{category.replace(' ', '')}",
                "investimento",
                "oportunidade",
                "empreender",
                "sucesso",
                "liberdadefinanceira"
            ]
        }
        
        return instagram_content
    
    def _adapt_for_google(self, name, category, value_proposition, headlines, descriptions, cta_examples, creative_content):
        """
        Adapta conteúdo para Google Ads.
        
        Args:
            name (str): Nome da oportunidade
            category (str): Categoria do negócio
            value_proposition (str): Proposta de valor
            headlines (list): Lista de títulos
            descriptions (list): Lista de descrições
            cta_examples (list): Lista de CTAs
            creative_content (dict): Conteúdo criativo completo
            
        Returns:
            dict: Conteúdo adaptado para Google Ads
        """
        # Selecionar elementos aleatórios
        headline = random.choice(headlines) if headlines else f"Invista na franquia {name}"
        description_text = random.choice(descriptions) if descriptions else f"Conheça a oportunidade de negócio {name} no setor de {category}."
        cta = random.choice(cta_examples) if cta_examples else "Saiba mais"
        
        # Gerar títulos de anúncio curtos
        short_headlines = [
            f"Franquia {name} - Invista Agora",
            f"{name} - Melhor Franquia de {category}",
            f"Seja Dono de {name}",
            f"Franquia {name} - Até {random.randint(25, 40)}% de ROI",
            f"Empreenda com {name}"
        ]
        
        # Gerar descrições curtas
        short_descriptions = [
            f"Modelo comprovado no setor de {category}. Suporte completo para o franqueado.",
            f"Franquia de sucesso em {category}. Baixo investimento, alto retorno.",
            f"Negócio próprio com marca reconhecida. Treinamento e suporte.",
            f"Seja franqueado {name}. Mercado em expansão e operação simplificada."
        ]
        
        # Gerar palavras-chave
        keywords = [
            f"franquia {name.lower()}",
            f"franquia de {category.lower()}",
            "franquias lucrativas",
            "franquias baratas",
            "como abrir uma franquia",
            f"melhor franquia de {category.lower()}",
            "franquias de sucesso",
            "investir em franquia",
            "franquias com baixo investimento",
            "franquias rentáveis"
        ]
        
        # Adaptar para diferentes formatos do Google Ads
        google_content = {
            'platform': 'google',
            'content_type': 'ads',
            'format': 'search_ad',
            'headlines': short_headlines,
            'descriptions': short_descriptions,
            'cta': cta,
            'keywords': keywords,
            'negative_keywords': [
                "empregos",
                "gratuito",
                "falência",
                "problemas",
                "reclamações"
            ],
            'campaign_types': [
                {
                    'type': 'search',
                    'objective': 'Captar leads interessados em franquias'
                },
                {
                    'type': 'display',
                    'objective': 'Aumentar reconhecimento da marca'
                },
                {
                    'type': 'discovery',
                    'objective': 'Alcançar potenciais franqueados'
                }
            ]
        }
        
        return google_content
    
    def _adapt_for_linkedin(self, name, category, value_proposition, headlines, descriptions, cta_examples, creative_content):
        """
        Adapta conteúdo para LinkedIn.
        
        Args:
            name (str): Nome da oportunidade
            category (str): Categoria do negócio
            value_proposition (str): Proposta de valor
            headlines (list): Lista de títulos
            descriptions (list): Lista de descrições
            cta_examples (list): Lista de CTAs
            creative_content (dict): Conteúdo criativo completo
            
        Returns:
            dict: Conteúdo adaptado para LinkedIn
        """
        # Selecionar elementos aleatórios
        headline = random.choice(headlines) if headlines else f"Invista na franquia {name}"
        description_text = random.choice(descriptions) if descriptions else f"Conheça a oportunidade de negócio {name} no setor de {category}."
        cta = random.choice(cta_examples) if cta_examples else "Saiba mais"
        
        # Gerar posts para LinkedIn
        posts = [
            f"🚀 OPORTUNIDADE DE NEGÓCIO | FRANQUIA {name.upper()} 🚀\n\n{value_proposition}\n\nO mercado de {category} está em expansão, e a franquia {name} oferece uma oportunidade única para empreendedores que buscam um negócio próprio com modelo comprovado.\n\n✅ Modelo de negócio testado e aprovado\n✅ Suporte completo para o franqueado\n✅ Treinamento operacional e de gestão\n✅ Marca reconhecida no mercado\n\nQuer saber mais sobre como se tornar um franqueado {name}? Deixe um comentário abaixo ou entre em contato diretamente.\n\n#franquia #empreendedorismo #{category.replace(' ', '')} #negóciopróprio #investimento",
            
            f"Você já pensou em ter seu próprio negócio?\n\nA franquia {name} pode ser a oportunidade que você estava esperando para empreender no setor de {category}.\n\n{value_proposition}\n\nO que oferecemos aos nossos franqueados:\n\n• Modelo de negócio com processos padronizados\n• Treinamento completo operacional e gerencial\n• Suporte contínuo em marketing e vendas\n• Marca reconhecida no mercado\n\nSe você está buscando uma oportunidade de investimento com potencial de crescimento, vamos conversar!\n\n#empreendedorismo #franquia #{category.replace(' ', '')} #investimento",
            
            f"Análise de mercado: O setor de {category} em 2025\n\nComo empreendedor, você sabe da importância de avaliar bem um mercado antes de investir. Por isso, compartilho alguns insights sobre o setor de {category} que podem ajudar em sua decisão:\n\n1. O mercado de {category} cresceu {random.randint(10, 25)}% nos últimos 12 meses\n2. A demanda por produtos/serviços de {category} mantém tendência de alta\n3. Modelos de negócio com processos padronizados apresentam maior taxa de sucesso\n\nÉ neste cenário que a franquia {name} se destaca como uma oportunidade de investimento sólida.\n\n{value_proposition}\n\nVocê está considerando empreender neste setor? Vamos trocar ideias!\n\n#análisedemercado #{category.replace(' ', '')} #empreendedorismo #franquia #oportunidade"
        ]
        
        # Gerar ideias para artigos
        article_ideas = [
            f"5 fatores essenciais para o sucesso no mercado de {category}",
            f"Como o modelo de franquia revolucionou o setor de {category}",
            f"Análise de mercado: o potencial de crescimento do setor de {category} em 2025",
            "Franquia vs. negócio independente: qual é a melhor opção para empreender?",
            f"A jornada do empreendedor: da decisão ao sucesso como franqueado {name}"
        ]
        
        # Adaptar para diferentes formatos do LinkedIn
        linkedin_content = {
            'platform': 'linkedin',
            'content_type': 'social_media',
            'format': 'post',
            'headline': headline,
            'posts': posts,
            'article_ideas': article_ideas,
            'targeting': {
                'job_titles': [
                    'Empresário',
                    'Empreendedor',
                    'Investidor',
                    'Gestor',
                    'Diretor',
                    'Consultor',
                    'Profissional Autônomo'
                ],
                'industries': [
                    'Negócios',
                    'Empreendedorismo',
                    'Finanças',
                    'Consultoria',
                    category
                ],
                'company_size': ['1-10', '11-50', '51-200']
            },
            'recommended_hashtags': [
                'franquia',
                'empreendedorismo',
                f"{category.replace(' ', '')}",
                'investimento',
                'negóciopróprio',
                'oportunidade'
            ]
        }
        
        return linkedin_content
    
    def _adapt_for_email(self, name, category, value_proposition, headlines, descriptions, cta_examples, creative_content):
        """
        Adapta conteúdo para campanhas de email.
        
        Args:
            name (str): Nome da oportunidade
            category (str): Categoria do negócio
            value_proposition (str): Proposta de valor
            headlines (list): Lista de títulos
            descriptions (list): Lista de descrições
            cta_examples (list): Lista de CTAs
            creative_content (dict): Conteúdo criativo completo
            
        Returns:
            dict: Conteúdo adaptado para email marketing
        """
        # Selecionar elementos aleatórios
        headline = random.choice(headlines) if headlines else f"Invista na franquia {name}"
        cta = random.choice(cta_examples) if cta_examples else "Quero saber mais"
        
        # Gerar assuntos para emails
        subjects = [
            f"Conheça a franquia {name} - Uma oportunidade no setor de {category}",
            f"[OPORTUNIDADE] Invista na franquia {name} e seja seu próprio chefe",
            f"Você está procurando um negócio próprio? Conheça {name}",
            f"Transforme sua carreira com a franquia {name} | ROI estimado de até {random.randint(25, 40)}%",
            f"Última chance: Vagas limitadas para franqueados {name} em sua região"
        ]
        
        # Gerar corpo de email
        email_body = f"""
        Olá {{nome}},
        
        Esperamos que esteja tudo bem com você.
        
        Gostaríamos de apresentar uma oportunidade de negócio que pode transformar sua carreira e realizar seu sonho de empreender com segurança.
        
        A franquia {name} é uma das mais promissoras do mercado de {category}, oferecendo:
        
        • {value_proposition}
        • Modelo de negócio testado e aprovado
        • Suporte completo para o franqueado
        • Treinamento operacional e de gestão
        • Marca reconhecida no mercado
        
        Com um investimento inicial a partir de R$ {{investimento_inicial}} e retorno estimado em {{tempo_retorno}} meses, a franquia {name} é ideal para quem busca empreender com segurança no setor de {category}.
        
        Quer saber mais? Temos vagas limitadas para novos franqueados em sua região.
        
        Clique no botão abaixo para agendar uma conversa com nosso consultor e receber uma apresentação completa, sem compromisso:
        
        [ {cta.upper()} ]
        
        Atenciosamente,
        
        Equipe {name}
        """
        
        # Gerar sequência de emails
        email_sequence = [
            {
                'subject': f"Conheça a franquia {name} - Uma oportunidade no setor de {category}",
                'content': f"Apresentação inicial da franquia {name}, destacando a oportunidade e o valor do negócio",
                'timing': 'Dia 1'
            },
            {
                'subject': f"Números e resultados da franquia {name}",
                'content': f"Dados sobre desempenho, ROI e tempo de retorno da franquia {name}",
                'timing': 'Dia 3'
            },
            {
                'subject': f"Depoimentos de franqueados {name} de sucesso",
                'content': f"Histórias reais de empreendedores que transformaram suas carreiras com a franquia {name}",
                'timing': 'Dia 5'
            },
            {
                'subject': f"Última chance: Vagas limitadas para franqueados {name}",
                'content': f"Criação de senso de urgência e chamada final para ação",
                'timing': 'Dia 7'
            }
        ]
        
        # Adaptar para diferentes formatos de email
        email_content = {
            'platform': 'email',
            'content_type': 'email_marketing',
            'format': 'newsletter',
            'subject_lines': subjects,
            'email_body': email_body,
            'email_sequence': email_sequence,
            'segmentation': [
                'Leads interessados em franquias',
                'Empreendedores iniciantes',
                'Investidores',
                'Pessoas em transição de carreira'
            ],
            'testing_variables': [
                'Assunto do email',
                'Formato do CTA',
                'Personalização do conteúdo',
                'Horário de envio'
            ]
        }
        
        return email_content
    
    def _generate_carousel_cards(self, name, category, value_proposition, cta):
        """
        Gera cards para carrossel de anúncios.
        
        Args:
            name (str): Nome da oportunidade
            category (str): Categoria do negócio
            value_proposition (str): Proposta de valor
            cta (str): Chamada para ação
            
        Returns:
            list: Lista de cards para carrossel
        """
        carousel_cards = [
            {
              'title': f"Franquia {name}",
                'description': value_proposition,
                'cta': cta
            },
            {
                'title': "Modelo de Negócio",
                'description': f"Processos padronizados e testados para o sucesso no setor de {category}.",
                'cta': cta
            },
            {
                'title': "Suporte Completo",
                'description': "Treinamento operacional e de gestão para o franqueado.",
                'cta': cta
            },
            {
                'title': "Investimento",
                'description': f"Investimento acessível com alto potencial de retorno no mercado de {category}.",
                'cta': cta
            },
            {
                'title': "Seja um Franqueado",
                'description': f"Transforme sua carreira com a franquia {name}.",
                'cta': cta
            }
        ]
        
        return carousel_cards
