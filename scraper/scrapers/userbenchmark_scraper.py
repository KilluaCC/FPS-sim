#!/usr/bin/env python3
"""
UserBenchmark.com Scraper - OPTIMIZED VERSION
Extracts FPS benchmark data from UserBenchmark gaming performance database.
Enhanced for better accuracy and performance.
"""

import re
import time
import random
import pandas as pd
import logging
from typing import List, Optional, Dict, Tuple
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse

from scraper import BaseScraper, BenchmarkData

logger = logging.getLogger(__name__)

class UserBenchmarkScraper(BaseScraper):
    """Optimized scraper for UserBenchmark.com"""
    
    def __init__(self):
        super().__init__("https://www.userbenchmark.com", "UserBenchmark")
        self.processed_urls = set()
        self.benchmark_urls = set()
        
        # UserBenchmark specific selectors and patterns
        self.game_selectors = [
            'a[href*="/Software/Game"]',
            'a[href*="/Software/Benchmark"]',
            'a[href*="/Software/Game-FPS"]',
            '.game-link',
            '.benchmark-link',
            '[class*="game"]',
            '[class*="benchmark"]'
        ]
        
        self.performance_selectors = [
            '.performance-data',
            '.benchmark-result',
            '.fps-data',
            '.score-data',
            '[class*="performance"]',
            '[class*="benchmark"]',
            '[class*="fps"]',
            '[class*="score"]'
        ]
    
    def scrape_benchmarks(self) -> List[BenchmarkData]:
        """Main scraping method for UserBenchmark - OPTIMIZED"""
        benchmarks = []
        
        try:
            logger.info("🎯 Starting optimized UserBenchmark scraping...")
            
            # Step 1: Find game benchmark pages
            game_links = self.discover_benchmark_pages()
            logger.info(f"🎮 Found {len(game_links)} potential benchmark pages")
            
            # Step 2: Process each page with enhanced extraction
            for i, game_link in enumerate(game_links[:15]):  # Increased limit for better coverage
                try:
                    logger.info(f"🔄 Processing benchmark page {i+1}/{min(15, len(game_links))}: {game_link}")
                    
                    game_soup = self.fetch_page(game_link)
                    game_benchmarks = self.extract_benchmarks_enhanced(game_soup, game_link)
                    
                    if game_benchmarks:
                        benchmarks.extend(game_benchmarks)
                        logger.info(f"✅ Extracted {len(game_benchmarks)} benchmarks from {game_link}")
                    else:
                        logger.warning(f"⚠️  No benchmarks found in {game_link}")
                    
                    # Adaptive delay based on success
                    delay = random.uniform(1.5, 3.0) if game_benchmarks else random.uniform(3.0, 5.0)
                    time.sleep(delay)
                    
                except Exception as e:
                    logger.error(f"❌ Error processing {game_link}: {e}")
                    continue
            
            logger.info(f"🎉 Successfully scraped {len(benchmarks)} benchmarks from UserBenchmark")
            
        except Exception as e:
            logger.error(f"💥 Error scraping UserBenchmark: {e}")
        
        return benchmarks
    
    def discover_benchmark_pages(self) -> List[str]:
        """Enhanced method to discover actual benchmark pages"""
        benchmark_pages = []
        
        try:
            # Method 1: Direct benchmark URLs
            direct_urls = [
                f"{self.base_url}/Software/Game-FPS",
                f"{self.base_url}/Software/Benchmarks",
                f"{self.base_url}/Software/Game-Performance",
                f"{self.base_url}/Software/FPS"
            ]
            
            for url in direct_urls:
                try:
                    soup = self.fetch_page(url)
                    if soup:
                        # Extract links from these pages
                        page_links = self.extract_links_from_page(soup, url)
                        benchmark_pages.extend(page_links)
                        logger.info(f"📄 Found {len(page_links)} links from {url}")
                except Exception as e:
                    logger.warning(f"⚠️  Could not fetch {url}: {e}")
                    continue
            
            # Method 2: Popular game benchmarks
            popular_games = [
                'cyberpunk-2077', 'red-dead-redemption-2', 'call-of-duty-warzone',
                'fortnite', 'minecraft', 'gta-5', 'the-witcher-3', 'assassins-creed-valhalla',
                'battlefield-2042', 'fifa-23', 'nba-2k23', 'call-of-duty-modern-warfare-2',
                'overwatch-2', 'valorant', 'league-of-legends', 'dota-2'
            ]
            
            for game in popular_games:
                game_url = f"{self.base_url}/Software/Game/{game}"
                if game_url not in self.processed_urls:
                    benchmark_pages.append(game_url)
                    self.processed_urls.add(game_url)
            
            # Method 3: Hardware-specific benchmark pages
            hardware_urls = [
                f"{self.base_url}/Software/Game-FPS/RTX-4090",
                f"{self.base_url}/Software/Game-FPS/RTX-4080",
                f"{self.base_url}/Software/Game-FPS/RTX-4070",
                f"{self.base_url}/Software/Game-FPS/RX-7900-XTX",
                f"{self.base_url}/Software/Game-FPS/RX-7900-XT"
            ]
            
            for url in hardware_urls:
                if url not in self.processed_urls:
                    benchmark_pages.append(url)
                    self.processed_urls.add(url)
            
            # Remove duplicates and filter valid URLs
            unique_pages = list(set(benchmark_pages))
            valid_pages = [url for url in unique_pages if self.is_valid_benchmark_url(url)]
            
            logger.info(f"🔍 Discovered {len(valid_pages)} valid benchmark pages")
            return valid_pages
            
        except Exception as e:
            logger.error(f"💥 Error discovering benchmark pages: {e}")
            return []
    
    def extract_links_from_page(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract benchmark links from a page"""
        links = []
        
        try:
            # Look for links that match benchmark patterns
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text().lower()
                
                # Check if this looks like a benchmark link
                if self.is_benchmark_link(href, text):
                    full_url = urljoin(base_url, href)
                    if full_url not in self.processed_urls:
                        links.append(full_url)
                        self.processed_urls.add(full_url)
            
            # Also look for links in specific sections
            benchmark_sections = soup.find_all(['div', 'section'], class_=re.compile(r'benchmark|game|performance', re.I))
            for section in benchmark_sections:
                section_links = section.find_all('a', href=True)
                for link in section_links:
                    href = link.get('href', '')
                    if self.is_benchmark_link(href, link.get_text()):
                        full_url = urljoin(base_url, href)
                        if full_url not in self.processed_urls:
                            links.append(full_url)
                            self.processed_urls.add(full_url)
                            
        except Exception as e:
            logger.error(f"Error extracting links from {base_url}: {e}")
        
        return links
    
    def is_benchmark_link(self, href: str, text: str) -> bool:
        """Check if a link is likely a benchmark page"""
        benchmark_indicators = [
            '/Software/Game', '/Software/Benchmark', '/Software/Game-FPS',
            'game', 'benchmark', 'fps', 'performance', 'test'
        ]
        
        href_lower = href.lower()
        text_lower = text.lower()
        
        # Check URL patterns
        if any(indicator in href_lower for indicator in benchmark_indicators):
            return True
        
        # Check text patterns
        if any(indicator in text_lower for indicator in benchmark_indicators):
            return True
        
        # Check for game-like patterns
        if re.search(r'[a-z]+-[a-z0-9]+', href_lower):
            return True
        
        return False
    
    def is_valid_benchmark_url(self, url: str) -> bool:
        """Validate if a URL is likely a valid benchmark page"""
        # Skip non-HTTP URLs
        if not url.startswith('http'):
            return False
        
        # Skip non-UserBenchmark URLs
        if 'userbenchmark.com' not in url:
            return False
        
        # Skip URLs that are too long (likely not main pages)
        if len(url) > 100:
            return False
        
        return True
    
    def extract_benchmarks_enhanced(self, soup: BeautifulSoup, game_url: str) -> List[BenchmarkData]:
        """Enhanced benchmark extraction with multiple strategies"""
        benchmarks = []
        
        try:
            # Extract game title
            game_title = self.extract_game_title_enhanced(soup, game_url)
            logger.debug(f"🎮 Game title: {game_title}")
            
            # Strategy 1: Look for structured benchmark data
            structured_benchmarks = self.extract_structured_benchmarks(soup, game_title, game_url)
            benchmarks.extend(structured_benchmarks)
            
            # Strategy 2: Look for performance charts
            chart_benchmarks = self.extract_chart_benchmarks(soup, game_title, game_url)
            benchmarks.extend(chart_benchmarks)
            
            # Strategy 3: Look for text-based performance data
            text_benchmarks = self.extract_text_benchmarks(soup, game_title, game_url)
            benchmarks.extend(text_benchmarks)
            
            # Strategy 4: Look for UserBenchmark specific data
            ub_benchmarks = self.extract_userbenchmark_specific(soup, game_title, game_url)
            benchmarks.extend(ub_benchmarks)
            
            # Strategy 5: Fallback to general text extraction
            if not benchmarks:
                fallback_benchmarks = self.extract_fallback_benchmarks(soup, game_title, game_url)
                benchmarks.extend(fallback_benchmarks)
            
            # Remove duplicates and validate
            unique_benchmarks = self.remove_duplicate_benchmarks(benchmarks)
            valid_benchmarks = [b for b in unique_benchmarks if self.validate_benchmark(b)]
            
            logger.debug(f"🔍 Extracted {len(valid_benchmarks)} valid benchmarks from {game_title}")
            return valid_benchmarks
            
        except Exception as e:
            logger.error(f"💥 Error in enhanced benchmark extraction: {e}")
            return []
    
    def extract_game_title_enhanced(self, soup: BeautifulSoup, game_url: str) -> str:
        """Enhanced game title extraction"""
        # Method 1: Look for specific UserBenchmark selectors
        title_selectors = [
            'h1.software-name',
            '.software-title',
            'h1[class*="title"]',
            'h1[class*="name"]',
            '.game-title',
            '.benchmark-title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text().strip()
                if title and len(title) > 2:
                    return self.clean_text(title)
        
        # Method 2: Look for meta tags
        meta_title = soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            title = meta_title.get('content').strip()
            if title and len(title) > 2:
                return self.clean_text(title)
        
        # Method 3: Look for page title
        if soup.title:
            title = soup.title.string.strip()
            if title and len(title) > 2:
                return self.clean_text(title)
        
        # Method 4: Extract from URL
        url_path = urlparse(game_url).path
        if url_path:
            path_parts = url_path.split('/')
            if len(path_parts) > 2:
                potential_title = path_parts[-1].replace('-', ' ').title()
                if len(potential_title) > 2:
                    return potential_title
        
        return "Unknown Game"
    
    def extract_structured_benchmarks(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Extract benchmarks from structured data (tables, lists)"""
        benchmarks = []
        
        try:
            # Look for benchmark tables
            tables = soup.find_all('table')
            for table in tables:
                table_benchmarks = self.parse_benchmark_table(table, game_title, game_url)
                benchmarks.extend(table_benchmarks)
            
            # Look for structured lists
            lists = soup.find_all(['ul', 'ol'])
            for list_elem in lists:
                list_benchmarks = self.parse_benchmark_list(list_elem, game_title, game_url)
                benchmarks.extend(list_benchmarks)
            
            # Look for div-based structured data
            structured_divs = soup.find_all('div', class_=re.compile(r'benchmark|performance|result|data', re.I))
            for div in structured_divs:
                div_benchmarks = self.parse_structured_div(div, game_title, game_url)
                benchmarks.extend(div_benchmarks)
                
        except Exception as e:
            logger.error(f"Error extracting structured benchmarks: {e}")
        
        return benchmarks
    
    def parse_benchmark_table(self, table: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse benchmark data from HTML tables"""
        benchmarks = []
        
        try:
            rows = table.find_all('tr')
            if len(rows) < 2:  # Need at least header + data
                return benchmarks
            
            # Try to identify columns
            header_row = rows[0]
            headers = [th.get_text().lower() for th in header_row.find_all(['th', 'td'])]
            
            # Look for GPU, CPU, FPS columns
            gpu_col = self.find_column_index(headers, ['gpu', 'graphics', 'card', 'video'])
            cpu_col = self.find_column_index(headers, ['cpu', 'processor', 'chip'])
            fps_col = self.find_column_index(headers, ['fps', 'score', 'performance', 'result'])
            
            if gpu_col is not None and cpu_col is not None and fps_col is not None:
                # Parse data rows
                for row in rows[1:]:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) > max(gpu_col, cpu_col, fps_col):
                        benchmark = self.create_benchmark_from_table_row(
                            cells, gpu_col, cpu_col, fps_col, game_title, game_url
                        )
                        if benchmark:
                            benchmarks.append(benchmark)
                            
        except Exception as e:
            logger.error(f"Error parsing benchmark table: {e}")
        
        return benchmarks
    
    def find_column_index(self, headers: List[str], keywords: List[str]) -> Optional[int]:
        """Find the index of a column based on keywords"""
        for i, header in enumerate(headers):
            if any(keyword in header for keyword in keywords):
                return i
        return None
    
    def create_benchmark_from_table_row(self, cells: List[Tag], gpu_col: int, cpu_col: int, fps_col: int, 
                                       game_title: str, game_url: str) -> Optional[BenchmarkData]:
        """Create benchmark data from table row cells"""
        try:
            gpu_name = self.clean_text(cells[gpu_col].get_text())
            cpu_name = self.clean_text(cells[cpu_col].get_text())
            fps_text = cells[fps_col].get_text()
            
            # Extract FPS value
            fps_match = re.search(r'(\d+(?:\.\d+)?)', fps_text)
            if not fps_match:
                return None
            
            fps_value = float(fps_match.group(1))
            
            # Validate data
            if not self.is_valid_hardware_name(gpu_name) or not self.is_valid_hardware_name(cpu_name):
                return None
            
            if not (1 <= fps_value <= 1000):
                return None
            
            return BenchmarkData(
                gpu_name=gpu_name,
                cpu_name=cpu_name,
                game_title=game_title,
                resolution="1080p",  # Default
                settings="High",      # Default
                avg_fps=fps_value,
                min_fps=fps_value * 0.8,
                max_fps=fps_value * 1.2,
                source_url=game_url,
                source_site=self.name,
                timestamp=pd.Timestamp.now().isoformat()
            )
            
        except Exception as e:
            logger.debug(f"Error creating benchmark from table row: {e}")
            return None
    
    def parse_benchmark_list(self, list_elem: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse benchmark data from HTML lists"""
        benchmarks = []
        
        try:
            list_items = list_elem.find_all('li')
            for item in list_items:
                item_text = item.get_text()
                
                # Look for performance patterns
                benchmark = self.parse_performance_text(item_text, game_title, game_url)
                if benchmark:
                    benchmarks.append(benchmark)
                    
        except Exception as e:
            logger.error(f"Error parsing benchmark list: {e}")
        
        return benchmarks
    
    def parse_structured_div(self, div: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse benchmark data from structured divs"""
        benchmarks = []
        
        try:
            # Look for performance data in the div
            performance_elements = div.find_all(['span', 'div'], class_=re.compile(r'fps|score|performance', re.I))
            
            for elem in performance_elements:
                elem_text = elem.get_text()
                benchmark = self.parse_performance_text(elem_text, game_title, game_url)
                if benchmark:
                    benchmarks.append(benchmark)
                    
        except Exception as e:
            logger.error(f"Error parsing structured div: {e}")
        
        return benchmarks
    
    def parse_performance_text(self, text: str, game_title: str, game_url: str) -> Optional[BenchmarkData]:
        """Parse performance data from text"""
        try:
            # Enhanced performance patterns
            patterns = [
                # "RTX 3080 + Ryzen 7 5800X: 120 FPS"
                r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX|Radeon|GeForce)[A-Za-z0-9\s\-]*)\s*\+\s*([A-Za-z0-9\s\-]+(?:Intel|AMD|Ryzen|Core|i[3579])[A-Za-z0-9\s\-]*)[:\s]+(\d+(?:\.\d+)?)\s*FPS',
                # "RTX 3080 gets 120 FPS with Ryzen 7 5800X"
                r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX|Radeon|GeForce)[A-Za-z0-9\s\-]*)\s+(?:gets|achieves|runs|performs)\s+(\d+(?:\.\d+)?)\s*FPS\s+(?:with|on|using)\s+([A-Za-z0-9\s\-]+(?:Intel|AMD|Ryzen|Core|i[3579])[A-Za-z0-9\s\-]*)',
                # "120 FPS: RTX 3080 + Ryzen 7 5800X"
                r'(\d+(?:\.\d+)?)\s*FPS[:\s]+([A-Za-z0-9\s\-]+(?:RTX|GTX|RX|Radeon|GeForce)[A-Za-z0-9\s\-]*)\s*\+\s*([A-Za-z0-9\s\-]+(?:Intel|AMD|Ryzen|Core|i[3579])[A-Za-z0-9\s\-]*)',
                # UserBenchmark specific: "Score: 120"
                r'Score[:\s]+(\d+(?:\.\d+)?)',
                # "Effective FPS: 120"
                r'Effective\s+FPS[:\s]+(\d+(?:\.\d+)?)'
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        if len(match.groups()) == 3:
                            # Pattern with GPU + CPU + FPS
                            gpu_name = self.clean_text(match.group(1))
                            cpu_name = self.clean_text(match.group(2))
                            fps_value = float(match.group(3))
                            
                        elif len(match.groups()) == 2:
                            # Pattern with one hardware + FPS
                            hardware_name = self.clean_text(match.group(1))
                            fps_value = float(match.group(2))
                            
                            # Determine if it's GPU or CPU
                            if self.is_gpu_name(hardware_name):
                                gpu_name = hardware_name
                                cpu_name = "Unknown CPU"
                            else:
                                cpu_name = hardware_name
                                gpu_name = "Unknown GPU"
                                
                        elif len(match.groups()) == 1:
                            # Pattern with just FPS
                            fps_value = float(match.group(1))
                            gpu_name = "Unknown GPU"
                            cpu_name = "Unknown CPU"
                        else:
                            continue
                        
                        # Validate and create benchmark
                        if self.is_valid_hardware_name(gpu_name) and self.is_valid_hardware_name(cpu_name) and 1 <= fps_value <= 1000:
                            benchmark = BenchmarkData(
                                gpu_name=gpu_name,
                                cpu_name=cpu_name,
                                game_title=game_title,
                                resolution="1080p",
                                settings="High",
                                avg_fps=fps_value,
                                min_fps=fps_value * 0.8,
                                max_fps=fps_value * 1.2,
                                source_url=game_url,
                                source_site=self.name,
                                timestamp=pd.Timestamp.now().isoformat()
                            )
                            return benchmark
                            
                    except (IndexError, ValueError) as e:
                        logger.debug(f"Failed to parse match: {e}")
                        continue
            
            return None
            
        except Exception as e:
            logger.debug(f"Error parsing performance text: {e}")
            return None
    
    def extract_chart_benchmarks(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Extract benchmarks from performance charts"""
        benchmarks = []
        
        try:
            # Look for chart containers
            chart_containers = soup.find_all(['div', 'section'], class_=re.compile(r'chart|graph|performance', re.I))
            
            for container in chart_containers:
                # Look for chart data points
                data_points = container.find_all(['div', 'span'], class_=re.compile(r'data|point|value', re.I))
                
                for point in data_points:
                    benchmark = self.parse_chart_data_point(point, game_title, game_url)
                    if benchmark:
                        benchmarks.append(benchmark)
                        
        except Exception as e:
            logger.error(f"Error extracting chart benchmarks: {e}")
        
        return benchmarks
    
    def extract_text_benchmarks(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Extract benchmarks from text content"""
        benchmarks = []
        
        try:
            # Look for text sections that might contain performance data
            text_sections = soup.find_all(['div', 'p', 'span'], class_=re.compile(r'performance|benchmark|result', re.I))
            
            for section in text_sections:
                section_text = section.get_text()
                benchmark = self.parse_performance_text(section_text, game_title, game_url)
                if benchmark:
                    benchmarks.append(benchmark)
                    
        except Exception as e:
            logger.error(f"Error extracting text benchmarks: {e}")
        
        return benchmarks
    
    def extract_userbenchmark_specific(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Extract UserBenchmark specific performance data"""
        benchmarks = []
        
        try:
            # Look for UserBenchmark specific performance indicators
            performance_elements = soup.find_all(['div', 'span'], class_=re.compile(r'efps|effective|fps|performance|score', re.I))
            
            for element in performance_elements:
                element_text = element.get_text()
                
                # Look for FPS or score values
                value_match = re.search(r'(\d+(?:\.\d+)?)', element_text)
                if value_match:
                    value = float(value_match.group(1))
                    
                    # Try to extract hardware context
                    gpu_name = self.extract_gpu_from_context(element)
                    cpu_name = self.extract_cpu_from_context(element)
                    
                    if gpu_name and cpu_name:
                        benchmark = BenchmarkData(
                            gpu_name=gpu_name,
                            cpu_name=cpu_name,
                            game_title=game_title,
                            resolution="1080p",
                            settings="High",
                            avg_fps=value,
                            min_fps=value * 0.8,
                            max_fps=value * 1.2,
                            source_url=game_url,
                            source_site=self.name,
                            timestamp=pd.Timestamp.now().isoformat()
                        )
                        benchmarks.append(benchmark)
                        
        except Exception as e:
            logger.error(f"Error extracting UserBenchmark specific data: {e}")
        
        return benchmarks
    
    def extract_fallback_benchmarks(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Fallback method to extract benchmarks from general text"""
        benchmarks = []
        
        try:
            # Get all text content
            text_content = soup.get_text()
            
            # Look for general performance patterns
            benchmark = self.parse_performance_text(text_content, game_title, game_url)
            if benchmark:
                benchmarks.append(benchmark)
                
        except Exception as e:
            logger.error(f"Error in fallback benchmark extraction: {e}")
        
        return benchmarks
    
    def remove_duplicate_benchmarks(self, benchmarks: List[BenchmarkData]) -> List[BenchmarkData]:
        """Remove duplicate benchmarks based on GPU, CPU, and game"""
        unique_benchmarks = []
        seen = set()
        
        for benchmark in benchmarks:
            # Create a unique key
            key = (benchmark.gpu_name, benchmark.cpu_name, benchmark.game_title)
            
            if key not in seen:
                seen.add(key)
                unique_benchmarks.append(benchmark)
        
        return unique_benchmarks
    
    def validate_benchmark(self, benchmark: BenchmarkData) -> bool:
        """Validate benchmark data quality"""
        try:
            # Check required fields
            if not benchmark.gpu_name or not benchmark.cpu_name or not benchmark.game_title:
                return False
            
            # Check hardware names
            if not self.is_valid_hardware_name(benchmark.gpu_name) or not self.is_valid_hardware_name(benchmark.cpu_name):
                return False
            
            # Check FPS values
            if not benchmark.avg_fps or not (1 <= benchmark.avg_fps <= 1000):
                return False
            
            # Check for obvious errors
            if benchmark.gpu_name == benchmark.cpu_name:
                return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Error validating benchmark: {e}")
            return False
    
    def parse_chart_data_point(self, data_point: Tag, game_title: str, game_url: str) -> Optional[BenchmarkData]:
        """Parse individual chart data points"""
        try:
            text = data_point.get_text()
            
            # Look for FPS values in chart data
            fps_match = re.search(r'(\d+(?:\.\d+)?)\s*FPS', text, re.IGNORECASE)
            if not fps_match:
                return None
            
            fps_value = float(fps_match.group(1))
            
            # Try to extract hardware names from the data point
            gpu_name = self.extract_gpu_from_context(data_point)
            cpu_name = self.extract_cpu_from_context(data_point)
            
            if gpu_name and cpu_name:
                return BenchmarkData(
                    gpu_name=gpu_name,
                    cpu_name=cpu_name,
                    game_title=game_title,
                    resolution="1080p",
                    settings="High",
                    avg_fps=fps_value,
                    min_fps=fps_value * 0.8,
                    max_fps=fps_value * 1.2,
                    source_url=game_url,
                    source_site=self.name,
                    timestamp=pd.Timestamp.now().isoformat()
                )
            
        except Exception as e:
            logger.debug(f"Error parsing chart data point: {e}")
        
        return None
    
    def parse_benchmark_row(self, row: Tag, game_title: str, game_url: str) -> Optional[BenchmarkData]:
        """Parse a single benchmark row/entry"""
        try:
            # Extract text content
            cells = row.find_all(['td', 'div', 'span'], recursive=False)
            if len(cells) < 3:
                return None
            
            # Try to identify GPU, CPU, and FPS data
            gpu_name = self.extract_gpu_name(cells)
            cpu_name = self.extract_cpu_name(cells)
            fps_data = self.extract_fps_data(cells)
            
            if not gpu_name or not cpu_name or not fps_data:
                return None
            
            # Extract resolution and settings if available
            resolution = self.extract_resolution(cells) or "1080p"
            settings = self.extract_settings(cells) or "High"
            
            return BenchmarkData(
                gpu_name=gpu_name,
                cpu_name=cpu_name,
                game_title=game_title,
                resolution=resolution,
                settings=settings,
                avg_fps=fps_data.get('avg'),
                min_fps=fps_data.get('min'),
                max_fps=fps_data.get('max'),
                source_url=game_url,
                source_site=self.name,
                timestamp=pd.Timestamp.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error parsing benchmark row: {e}")
            return None
    
    def extract_gpu_name(self, cells: List[Tag]) -> Optional[str]:
        """Extract GPU name from cells"""
        gpu_keywords = ['rtx', 'gtx', 'rx', 'radeon', 'geforce', 'gpu', 'graphics', 'video']
        
        for cell in cells:
            text = cell.get_text().lower()
            if any(keyword in text for keyword in gpu_keywords):
                return self.clean_text(cell.get_text())
        
        return None
    
    def extract_cpu_name(self, cells: List[Tag]) -> Optional[str]:
        """Extract CPU name from cells"""
        cpu_keywords = ['intel', 'amd', 'ryzen', 'core', 'i3', 'i5', 'i7', 'i9', 'cpu', 'processor', 'pentium']
        
        for cell in cells:
            text = cell.get_text().lower()
            if any(keyword in text for keyword in cpu_keywords):
                return self.clean_text(cell.get_text())
        
        return None
    
    def extract_fps_data(self, cells: List[Tag]) -> Dict[str, Optional[float]]:
        """Extract FPS data from cells"""
        fps_data = {'avg': None, 'min': None, 'max': None}
        
        for cell in cells:
            text = cell.get_text()
            
            # Look for average FPS
            if any(keyword in text.lower() for keyword in ['avg', 'average', 'fps', 'score']):
                fps_data['avg'] = self.extract_fps_value(text)
            
            # Look for min/max FPS
            elif 'min' in text.lower():
                fps_data['min'] = self.extract_fps_value(text)
            elif 'max' in text.lower():
                fps_data['max'] = self.extract_fps_value(text)
        
        return fps_data
    
    def extract_resolution(self, cells: List[Tag]) -> Optional[str]:
        """Extract resolution from cells"""
        resolution_patterns = [r'(\d{3,4}p)', r'(\d{3,4}x\d{3,4})', r'(4k|1440p|1080p)', r'(\d{3,4})p']
        
        for cell in cells:
            text = cell.get_text()
            for pattern in resolution_patterns:
                match = re.search(pattern, text, re.I)
                if match:
                    return match.group(1)
        
        return None
    
    def extract_settings(self, cells: List[Tag]) -> Optional[str]:
        """Extract graphics settings from cells"""
        settings_keywords = ['low', 'medium', 'high', 'ultra', 'max', 'min', 'normal', 'extreme']
        
        for cell in cells:
            text = cell.get_text().lower()
            for setting in settings_keywords:
                if setting in text:
                    return setting.title()
        
        return None
    
    def parse_benchmark_page(self, soup: BeautifulSoup, url: str) -> Optional[BenchmarkData]:
        """Parse individual benchmark page to extract data"""
        # This method is not used in the current implementation
        # but is required by the abstract base class
        return None

    def extract_from_text(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Extract benchmark data from unstructured text when structured data isn't available"""
        benchmarks = []
        
        try:
            # Look for text patterns that might contain benchmark data
            text_content = soup.get_text()
            
            # Find patterns like "RTX 3080 + Ryzen 7 5800X: 120 FPS"
            benchmark_patterns = [
                r'([A-Za-z0-9\s\-]+)\s*\+\s*([A-Za-z0-9\s\-]+)[:\s]+(\d+)\s*FPS',
                r'([A-Za-z0-9\s\-]+)\s*with\s*([A-Za-z0-9\s\-]+)[:\s]+(\d+)\s*FPS',
                r'([A-Za-z0-9\s\-]+)\s*(\d+)\s*FPS\s*([A-Za-z0-9\s\-]+)',
                r'([A-Za-z0-9\s\-]+)\s*(\d+)\s*([A-Za-z0-9\s\-]+)\s*FPS'
            ]
            
            for pattern in benchmark_patterns:
                matches = re.finditer(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    try:
                        gpu_name = self.clean_text(match.group(1))
                        cpu_name = self.clean_text(match.group(2))
                        fps_value = float(match.group(3))
                        
                        # Basic validation
                        if len(gpu_name) > 3 and len(cpu_name) > 3 and 1 <= fps_value <= 1000:
                            benchmark = BenchmarkData(
                                gpu_name=gpu_name,
                                cpu_name=cpu_name,
                                game_title=game_title,
                                resolution="1080p",  # Default assumption
                                settings="High",     # Default assumption
                                avg_fps=fps_value,
                                min_fps=fps_value * 0.8,  # Estimate
                                max_fps=fps_value * 1.2,  # Estimate
                                source_url=game_url,
                                source_site=self.name,
                                timestamp=pd.Timestamp.now().isoformat()
                            )
                            benchmarks.append(benchmark)
                            
                    except (IndexError, ValueError) as e:
                        logger.debug(f"Failed to parse match: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error extracting from text: {e}")
        
        return benchmarks

    def is_gpu_name(self, name: str) -> bool:
        """Check if a name looks like a GPU"""
        gpu_indicators = ['rtx', 'gtx', 'rx', 'radeon', 'geforce', 'gpu', 'graphics', 'video']
        name_lower = name.lower()
        return any(indicator in name_lower for indicator in gpu_indicators)
    
    def is_cpu_name(self, name: str) -> bool:
        """Check if a name looks like a CPU"""
        cpu_indicators = ['intel', 'amd', 'ryzen', 'core', 'i3', 'i5', 'i7', 'i9', 'pentium', 'celeron', 'athlon']
        name_lower = name.lower()
        return any(indicator in name_lower for indicator in cpu_indicators)
    
    def is_valid_hardware_name(self, name: str) -> bool:
        """Check if a hardware name is valid"""
        if not name or name in ['Unknown GPU', 'Unknown CPU']:
            return False
        return len(name.strip()) >= 3
    
    def extract_gpu_from_context(self, element: Tag) -> Optional[str]:
        """Extract GPU name from surrounding context"""
        # Look in parent elements for GPU mentions
        parent = element.parent
        for _ in range(3):  # Look up to 3 levels up
            if parent:
                # Look for GPU mentions in parent text
                gpu_elements = parent.find_all(['div', 'span'], class_=re.compile(r'gpu|graphics|card', re.I))
                for gpu_elem in gpu_elements:
                    text = gpu_elem.get_text()
                    if self.is_gpu_name(text):
                        return self.clean_text(text)
                
                # Look in parent text
                parent_text = parent.get_text()
                gpu_match = re.search(r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX|Radeon|GeForce)[A-Za-z0-9\s\-]*)', parent_text)
                if gpu_match:
                    return self.clean_text(gpu_match.group(1))
                
                parent = parent.parent
        
        return None
    
    def extract_cpu_from_context(self, element: Tag) -> Optional[str]:
        """Extract CPU name from surrounding context"""
        # Look in parent elements for CPU mentions
        parent = element.parent
        for _ in range(3):  # Look up to 3 levels up
            if parent:
                # Look for CPU mentions in parent text
                cpu_elements = parent.find_all(['div', 'span'], class_=re.compile(r'cpu|processor', re.I))
                for cpu_elem in cpu_elements:
                    text = cpu_elem.get_text()
                    if self.is_cpu_name(text):
                        return self.clean_text(text)
                
                # Look in parent text
                parent_text = parent.get_text()
                cpu_match = re.search(r'([A-Za-z0-9\s\-]+(?:Intel|AMD|Ryzen|Core|i[3579])[A-Za-z0-9\s\-]*)', parent_text)
                if cpu_match:
                    return self.clean_text(cpu_match.group(1))
                
                parent = parent.parent
        
        return None
    
    def get_scraping_stats(self) -> Dict:
        """Get statistics about the scraping process"""
        return {
            "total_urls_processed": len(self.processed_urls),
            "total_benchmarks_found": len(self.benchmark_urls),
            "scraper_name": self.name,
            "base_url": self.base_url
        }
