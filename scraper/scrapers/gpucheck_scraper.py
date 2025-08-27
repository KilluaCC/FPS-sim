#!/usr/bin/env python3
"""
GPUCheck.com Scraper
Extracts FPS benchmark data from GPUCheck gaming performance database.
"""

import re
import time
import random
import pandas as pd
import logging
from typing import List, Optional, Dict
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse
import requests

from scraper import BaseScraper, BenchmarkData
from proxy_manager import ProxyManager, ProxyConfig

logger = logging.getLogger(__name__)

class GPUCheckScraper(BaseScraper):
    """Scraper for GPUCheck.com with proxy rotation"""
    
    def __init__(self, use_proxies: bool = True, proxy_manager: Optional[ProxyManager] = None):
        super().__init__("https://gpucheck.com", "GPUCheck")
        self.processed_urls = set()
        self.use_proxies = use_proxies
        self.proxy_manager = proxy_manager or self._create_default_proxy_manager()
        self.current_proxy = None
        self.proxy_failures = 0
        self.max_proxy_failures = 5
    
    def scrape_benchmarks(self) -> List[BenchmarkData]:
        """Main scraping method for GPUCheck"""
        benchmarks = []
        
        try:
            # Start with the main page to find game categories
            main_soup = self._fetch_with_proxy_rotation(self.base_url)
            game_links = self.extract_game_links(main_soup)
            
            logger.info(f"Found {len(game_links)} game links on GPUCheck")
            
            for i, game_link in enumerate(game_links[:10]):  # Limit to first 10 games for demo
                try:
                    logger.info(f"Processing game {i+1}/{min(10, len(game_links))}: {game_link}")
                    
                    game_soup = self._fetch_with_proxy_rotation(game_link)
                    game_benchmarks = self.extract_game_benchmarks(game_soup, game_link)
                    benchmarks.extend(game_benchmarks)
                    
                    # Be respectful with delays
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    logger.error(f"Error processing game {game_link}: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(benchmarks)} benchmarks from GPUCheck")
            
        except Exception as e:
            logger.error(f"Error scraping GPUCheck: {e}")
        
        return benchmarks
    
    def extract_game_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract links to individual game benchmark pages"""
        game_links = []
        
        # Look for common patterns in GPUCheck
        # This will need to be adjusted based on actual site structure
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text().lower()
            
            # Look for game-related links
            if any(keyword in text for keyword in ['game', 'benchmark', 'fps', 'performance']):
                full_url = urljoin(self.base_url, href)
                if full_url not in self.processed_urls:
                    game_links.append(full_url)
                    self.processed_urls.add(full_url)
        
        # Also look for specific game titles
        popular_games = [
            'cyberpunk-2077', 'red-dead-redemption-2', 'call-of-duty', 
            'fortnite', 'minecraft', 'gta-5', 'the-witcher-3'
        ]
        
        for game in popular_games:
            game_url = f"{self.base_url}/games/{game}"
            if game_url not in self.processed_urls:
                game_links.append(game_url)
                self.processed_urls.add(game_url)
        
        return game_links
    
    def extract_game_benchmarks(self, soup: BeautifulSoup, game_url: str) -> List[BenchmarkData]:
        """Extract benchmark data from a game page"""
        benchmarks = []
        
        try:
            # Extract game title
            game_title = self.extract_game_title(soup)
            
            # Look for benchmark tables or performance data
            benchmark_sections = soup.find_all(['table', 'div'], class_=re.compile(r'benchmark|performance|fps|result|chart', re.I))
            
            for section in benchmark_sections:
                section_benchmarks = self.parse_benchmark_section(section, game_title, game_url)
                benchmarks.extend(section_benchmarks)
            
            # Look for performance charts and graphs
            chart_sections = soup.find_all(['div', 'section'], class_=re.compile(r'chart|graph|performance|fps', re.I))
            for chart in chart_sections:
                chart_benchmarks = self.parse_chart_section(chart, game_title, game_url)
                benchmarks.extend(chart_benchmarks)
            
            # Look for text-based performance data
            text_sections = soup.find_all(['div', 'p', 'span'], class_=re.compile(r'performance|fps|benchmark|result', re.I))
            for text_section in text_sections:
                text_benchmarks = self.parse_text_section(text_section, game_title, game_url)
                benchmarks.extend(text_benchmarks)
            
            # If no structured data found, try to extract from text
            if not benchmarks:
                text_benchmarks = self.extract_from_text(soup, game_title, game_url)
                benchmarks.extend(text_benchmarks)
                
        except Exception as e:
            logger.error(f"Error extracting benchmarks from {game_url}: {e}")
        
        return benchmarks
    
    def extract_game_title(self, soup: BeautifulSoup) -> str:
        """Extract game title from page"""
        # Try multiple selectors for game title
        title_selectors = [
            'h1', 'h2', '.game-title', '.title', '[class*="title"]',
            'title', 'meta[property="og:title"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text().strip() if hasattr(element, 'get_text') else element.get('content', '')
                if title:
                    return self.clean_text(title)
        
        # Fallback: extract from URL
        url_path = urlparse(self.base_url).path
        if url_path:
            return url_path.split('/')[-1].replace('-', ' ').title()
        
        return "Unknown Game"
    
    def parse_benchmark_section(self, section: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse a benchmark section to extract performance data"""
        benchmarks = []
        
        try:
            # Look for table rows or structured data
            rows = section.find_all(['tr', 'div'], recursive=False)
            
            for row in rows:
                benchmark = self.parse_benchmark_row(row, game_title, game_url)
                if benchmark:
                    benchmarks.append(benchmark)
                    
        except Exception as e:
            logger.error(f"Error parsing benchmark section: {e}")
        
        return benchmarks
    
    def parse_chart_section(self, chart: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse performance charts and graphs"""
        benchmarks = []
        
        try:
            # Look for chart data, tooltips, or performance indicators
            chart_data = chart.find_all(['div', 'span'], class_=re.compile(r'data|value|fps|performance', re.I))
            
            for data_point in chart_data:
                benchmark = self.parse_chart_data_point(data_point, game_title, game_url)
                if benchmark:
                    benchmarks.append(benchmark)
                    
        except Exception as e:
            logger.error(f"Error parsing chart section: {e}")
        
        return benchmarks
    
    def parse_text_section(self, text_section: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse text-based performance data"""
        benchmarks = []
        
        try:
            # Look for performance mentions in text
            text_content = text_section.get_text()
            
            # Enhanced patterns for finding performance data
            performance_patterns = [
                # "RTX 3080 gets 120 FPS in Cyberpunk 2077"
                r'([A-Za-z0-9\s\-]+)\s+(?:gets|achieves|runs|performs)\s+(\d+(?:\.\d+)?)\s*FPS',
                # "RTX 3080: 120 FPS average"
                r'([A-Za-z0-9\s\-]+):\s*(\d+(?:\.\d+)?)\s*FPS\s*(?:average|avg|mean)',
                # "120 FPS with RTX 3080"
                r'(\d+(?:\.\d+)?)\s*FPS\s+(?:with|on|using)\s+([A-Za-z0-9\s\-]+)',
                # "RTX 3080 + Ryzen 7 5800X = 120 FPS"
                r'([A-Za-z0-9\s\-]+)\s*\+\s*([A-Za-z0-9\s\-]+)\s*=\s*(\d+(?:\.\d+)?)\s*FPS'
            ]
            
            for pattern in performance_patterns:
                matches = re.finditer(pattern, text_content, re.IGNORECASE)
                for match in matches:
                    try:
                        if len(match.groups()) == 2:
                            # Pattern: "RTX 3080 gets 120 FPS"
                            hardware_name = self.clean_text(match.group(1))
                            fps_value = float(match.group(2))
                            
                            # Try to determine if it's GPU or CPU
                            if self.is_gpu_name(hardware_name):
                                gpu_name = hardware_name
                                cpu_name = "Unknown CPU"  # We'll need to extract this from context
                            else:
                                cpu_name = hardware_name
                                gpu_name = "Unknown GPU"  # We'll need to extract this from context
                                
                        elif len(match.groups()) == 3:
                            # Pattern: "RTX 3080 + Ryzen 7 5800X = 120 FPS"
                            gpu_name = self.clean_text(match.group(1))
                            cpu_name = self.clean_text(match.group(2))
                            fps_value = float(match.group(3))
                        else:
                            continue
                        
                        # Basic validation
                        if self.is_valid_hardware_name(gpu_name) and self.is_valid_hardware_name(cpu_name) and 1 <= fps_value <= 1000:
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
            logger.error(f"Error parsing text section: {e}")
        
        return benchmarks
    
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
        gpu_keywords = ['rtx', 'gtx', 'rx', 'radeon', 'geforce', 'gpu', 'graphics']
        
        for cell in cells:
            text = cell.get_text().lower()
            if any(keyword in text for keyword in gpu_keywords):
                return self.clean_text(cell.get_text())
        
        return None
    
    def extract_cpu_name(self, cells: List[Tag]) -> Optional[str]:
        """Extract CPU name from cells"""
        cpu_keywords = ['intel', 'amd', 'ryzen', 'core', 'i3', 'i5', 'i7', 'i9', 'cpu', 'processor']
        
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
            if any(keyword in text.lower() for keyword in ['avg', 'average', 'fps']):
                fps_data['avg'] = self.extract_fps_value(text)
            
            # Look for min/max FPS
            elif 'min' in text.lower():
                fps_data['min'] = self.extract_fps_value(text)
            elif 'max' in text.lower():
                fps_data['max'] = self.extract_fps_value(text)
        
        return fps_data
    
    def extract_resolution(self, cells: List[Tag]) -> Optional[str]:
        """Extract resolution from cells"""
        resolution_patterns = [r'(\d{3,4}p)', r'(\d{3,4}x\d{3,4})', r'(4k|1440p|1080p)']
        
        for cell in cells:
            text = cell.get_text()
            for pattern in resolution_patterns:
                match = re.search(pattern, text, re.I)
                if match:
                    return match.group(1)
        
        return None
    
    def extract_settings(self, cells: List[Tag]) -> Optional[str]:
        """Extract graphics settings from cells"""
        settings_keywords = ['low', 'medium', 'high', 'ultra', 'max', 'min']
        
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
                r'([A-Za-z0-9\s\-]+)\s*(\d+)\s*FPS\s*([A-Za-z0-9\s\-]+)'
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

    def _create_default_proxy_manager(self) -> ProxyManager:
        """Create a default proxy manager for GPUCheck"""
        from proxy_manager import create_proxy_manager
        return create_proxy_manager(use_free_proxies=True)
    
    def _get_proxy_session(self) -> requests.Session:
        """Get a session with the next available proxy"""
        if not self.use_proxies or not self.proxy_manager:
            return self.session
        
        # Get next available proxy
        proxy = self.proxy_manager.get_next_proxy()
        if not proxy:
            logger.warning("No working proxies available, using direct connection")
            return self.session
        
        self.current_proxy = proxy
        logger.info(f"Using proxy: {proxy.host}:{proxy.port}")
        
        # Create session with proxy
        return self.proxy_manager.create_session_with_proxy(proxy)
    
    def _handle_proxy_failure(self, proxy: ProxyConfig, error: Exception):
        """Handle proxy failure and rotate if necessary"""
        if not self.use_proxies:
            return
        
        self.proxy_manager.mark_proxy_failed(proxy)
        self.proxy_failures += 1
        
        logger.warning(f"Proxy {proxy.host}:{proxy.port} failed: {error}")
        
        # If too many failures, try to get a new proxy
        if self.proxy_failures >= self.max_proxy_failures:
            logger.warning("Too many proxy failures, rotating proxy pool")
            self.proxy_failures = 0
            self.current_proxy = None
    
    def _fetch_with_proxy_rotation(self, url: str, params: Optional[Dict] = None) -> BeautifulSoup:
        """Fetch page with proxy rotation and retry logic"""
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                # Get session with proxy
                session = self._get_proxy_session()
                
                # Make request
                logger.info(f"Fetching with proxy (attempt {attempt + 1}): {url}")
                response = session.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                # Reset failure counter on success
                self.proxy_failures = 0
                
                # Add delay to be respectful
                time.sleep(random.uniform(2, 4))
                
                return BeautifulSoup(response.content, 'lxml')
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                
                # Handle proxy failure
                if self.current_proxy:
                    self._handle_proxy_failure(self.current_proxy, e)
                
                # If this was the last attempt, raise the error
                if attempt == max_attempts - 1:
                    raise
                
                # Wait before retry
                time.sleep(random.uniform(5, 10))
        
        # This should never be reached, but just in case
        raise requests.exceptions.RequestException("All proxy attempts failed")
    
    def get_proxy_stats(self) -> Dict:
        """Get proxy statistics"""
        if not self.proxy_manager:
            return {"error": "No proxy manager"}
        
        stats = self.proxy_manager.get_proxy_stats()
        stats.update({
            "current_proxy": f"{self.current_proxy.host}:{self.current_proxy.port}" if self.current_proxy else "None",
            "proxy_failures": self.proxy_failures,
            "max_proxy_failures": self.max_proxy_failures
        })
        return stats
