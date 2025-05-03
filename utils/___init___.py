# Inicialização do pacote collectors

from .franchise_scraper import FranchiseScraper
from .marketplace_scraper import MarketplaceScraper
from .social_media_monitor import SocialMediaMonitor
from .sales_data_collector import SalesDataCollector
from .affiliate_finder import AffiliateFinder
__all__ = [
    'FranchiseScraper',
    'MarketplaceScraper', 
    'SocialMediaMonitor',
    'SalesDataCollector'
]
