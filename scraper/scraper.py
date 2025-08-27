#!/usr/bin/env python3
"""
FPS Benchmark Data Scraper
Modular web scraper for extracting FPS performance data from various gaming sites.
"""

import requests
import pandas as pd
import time
import random
import logging
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from retrying import retry
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class BenchmarkData:
    """Data structure for benchmark results"""
    gpu_name: str
    cpu_name: str
    game_title: str
    resolution: str
    settings: str
    avg_fps: Optional[float]
    min_fps: Optional[float]
    max_fps: Optional[float]
    source_url: str
    source_site: str
    timestamp: str

class BaseScraper(ABC):
    """Abstract base class for all scrapers"""
    
    def __init__(self, base_url: str, name: str):
        self.base_url = base_url
        self.name = name
        self.session = requests.Session()
        self.ua = UserAgent()
        self.setup_session()
    
    def setup_session(self):
        """Setup session with headers and retry logic"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    @retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def fetch_page(self, url: str, params: Optional[Dict] = None) -> BeautifulSoup:
        """Fetch a page with retry logic and error handling"""
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Random delay to be respectful
            time.sleep(random.uniform(1, 3))
            
            return BeautifulSoup(response.content, 'lxml')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            raise
    
    @abstractmethod
    def scrape_benchmarks(self) -> List[BenchmarkData]:
        """Main scraping method to be implemented by each scraper"""
        pass
    
    @abstractmethod
    def parse_benchmark_page(self, soup: BeautifulSoup, url: str) -> Optional[BenchmarkData]:
        """Parse individual benchmark page to extract data"""
        pass
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        if not text:
            return ""
        return text.strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    def extract_fps_value(self, text: str) -> Optional[float]:
        """Extract FPS value from text, handling various formats"""
        if not text:
            return None
        
        import re
        
        # Remove common text and extract numbers
        text = text.lower().replace('fps', '').replace('avg', '').replace('average', '')
        
        # Find numbers (including decimals)
        matches = re.findall(r'(\d+(?:\.\d+)?)', text)
        if matches:
            try:
                value = float(matches[0])
                # Validate reasonable FPS range
                if 1 <= value <= 1000:
                    return value
            except ValueError:
                pass
        
        return None

class ScraperManager:
    """Manages multiple scrapers and coordinates data collection"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.scrapers: List[BaseScraper] = []
        self.all_data: List[BenchmarkData] = []
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
    
    def add_scraper(self, scraper: BaseScraper):
        """Add a scraper to the manager"""
        self.scrapers.append(scraper)
        logger.info(f"Added scraper: {scraper.name}")
    
    def run_all_scrapers(self) -> pd.DataFrame:
        """Run all scrapers and collect data"""
        logger.info(f"Starting scraping with {len(self.scrapers)} scrapers")
        
        for scraper in self.scrapers:
            try:
                logger.info(f"Running scraper: {scraper.name}")
                data = scraper.scrape_benchmarks()
                self.all_data.extend(data)
                logger.info(f"Scraped {len(data)} benchmarks from {scraper.name}")
            except Exception as e:
                logger.error(f"Error running scraper {scraper.name}: {e}")
                continue
        
        # Convert to DataFrame
        df = pd.DataFrame([vars(data) for data in self.all_data])
        
        if not df.empty:
            # Save to CSV
            output_path = os.path.join(self.output_dir, "benchmarks.csv")
            df.to_csv(output_path, index=False)
            logger.info(f"Saved {len(df)} benchmarks to {output_path}")
            
            # Save summary
            summary_path = os.path.join(self.output_dir, "scraping_summary.txt")
            with open(summary_path, 'w') as f:
                f.write(f"Scraping Summary\n")
                f.write(f"================\n")
                f.write(f"Total benchmarks: {len(df)}\n")
                f.write(f"Unique GPUs: {df['gpu_name'].nunique()}\n")
                f.write(f"Unique CPUs: {df['cpu_name'].nunique()}\n")
                f.write(f"Unique games: {df['game_title'].nunique()}\n")
                f.write(f"Scraped from: {', '.join(df['source_site'].unique())}\n")
                f.write(f"Timestamp: {pd.Timestamp.now()}\n")
            
            logger.info(f"Saved summary to {summary_path}")
        else:
            logger.warning("No data was scraped")
        
        return df
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about scraped data"""
        if not self.all_data:
            return {}
        
        df = pd.DataFrame([vars(data) for data in self.all_data])
        
        return {
            'total_benchmarks': len(df),
            'unique_gpus': df['gpu_name'].nunique(),
            'unique_cpus': df['cpu_name'].nunique(),
            'unique_games': df['game_title'].nunique(),
            'sites_scraped': df['source_site'].unique().tolist(),
            'data_completeness': {
                'avg_fps': df['avg_fps'].notna().sum() / len(df),
                'min_fps': df['min_fps'].notna().sum() / len(df),
                'max_fps': df['max_fps'].notna().sum() / len(df),
                'resolution': df['resolution'].notna().sum() / len(df),
                'settings': df['settings'].notna().sum() / len(df)
            }
        }

if __name__ == "__main__":
    # Example usage
    manager = ScraperManager()
    
    # Add scrapers here
    # manager.add_scraper(GPUCheckScraper())
    # manager.add_scraper(UserBenchmarkScraper())
    
    # Run scraping
    # df = manager.run_all_scrapers()
    # print(manager.get_statistics())
    
    print("Scraper module loaded. Import and use with specific scraper implementations.")
