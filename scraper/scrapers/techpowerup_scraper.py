#!/usr/bin/env python3
"""
TechPowerUp.com Scraper
Extracts FPS benchmark data from TechPowerUp gaming performance database.
"""

import re
import time
import random
import pandas as pd
import logging
from typing import List, Optional, Dict
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, urlparse

from scraper import BaseScraper, BenchmarkData

logger = logging.getLogger(__name__)

class TechPowerUpScraper(BaseScraper):
    """Scraper for TechPowerUp.com"""
    
    def __init__(self):
        super().__init__("https://www.techpowerup.com", "TechPowerUp")
        self.processed_urls = set()
    
    def scrape_benchmarks(self) -> List[BenchmarkData]:
        """Main scraping method for TechPowerUp"""
        benchmarks = []
        
        try:
            # Start with the main page to find game categories
            main_soup = self.fetch_page(self.base_url)
            game_links = self.extract_game_links(main_soup)
            
            logger.info(f"Found {len(game_links)} game links on TechPowerUp")
            
            for i, game_link in enumerate(game_links[:10]):  # Limit to first 10 games for demo
                try:
                    logger.info(f"Processing game {i+1}/{min(10, len(game_links))}: {game_link}")
                    
                    game_soup = self.fetch_page(game_link)
                    game_benchmarks = self.extract_game_benchmarks(game_soup, game_link)
                    benchmarks.extend(game_benchmarks)
                    
                    # Be respectful with delays
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    logger.error(f"Error processing game {game_link}: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(benchmarks)} benchmarks from TechPowerUp")
            
        except Exception as e:
            logger.error(f"Error scraping TechPowerUp: {e}")
        
        return benchmarks
    
    def extract_game_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract links to individual game benchmark pages"""
        game_links = []
        
        # Look for common patterns in TechPowerUp
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text().lower()
            
            # Look for game-related links
            if any(keyword in text for keyword in ['game', 'benchmark', 'fps', 'performance', 'review']):
                full_url = urljoin(self.base_url, href)
                if full_url not in self.processed_urls:
                    game_links.append(full_url)
                    self.processed_urls.add(full_url)
        
        # Also look for specific game titles and benchmark categories
        popular_games = [
            'cyberpunk-2077', 'red-dead-redemption-2', 'call-of-duty', 
            'fortnite', 'minecraft', 'gta-5', 'the-witcher-3', 'assassins-creed'
        ]
        
        # TechPowerUp specific paths
        benchmark_paths = [
            '/gpu-specs/', '/gpu-db/', '/benchmarks/', '/reviews/',
            '/game-benchmarks/', '/performance/', '/fps/'
        ]
        
        for path in benchmark_paths:
            full_url = f"{self.base_url}{path}"
            if full_url not in self.processed_urls:
                game_links.append(full_url)
                self.processed_urls.add(full_url)
        
        for game in popular_games:
            game_url = f"{self.base_url}/game/{game}"
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
            benchmark_sections = soup.find_all(['table', 'div'], class_=re.compile(r'benchmark|performance|fps|result|chart|score', re.I))
            
            for section in benchmark_sections:
                section_benchmarks = self.parse_benchmark_section(section, game_title, game_url)
                benchmarks.extend(section_benchmarks)
            
            # Look for performance charts and graphs
            chart_sections = soup.find_all(['div', 'section'], class_=re.compile(r'chart|graph|performance|fps|score|benchmark', re.I))
            for chart in chart_sections:
                chart_benchmarks = self.parse_chart_section(chart, game_title, game_url)
                benchmarks.extend(chart_benchmarks)
            
            # Look for text-based performance data
            text_sections = soup.find_all(['div', 'p', 'span'], class_=re.compile(r'performance|fps|benchmark|result|score', re.I))
            for text_section in text_sections:
                text_benchmarks = self.parse_text_section(text_section, game_title, game_url)
                benchmarks.extend(text_benchmarks)
            
            # Look for TechPowerUp specific performance indicators
            performance_indicators = soup.find_all(['div', 'span'], class_=re.compile(r'fps|performance|benchmark|result', re.I))
            for indicator in performance_indicators:
                indicator_benchmarks = self.parse_performance_indicator(indicator, game_title, game_url)
                benchmarks.extend(indicator_benchmarks)
            
            # If no structured data found, try to extract from text
            if not benchmarks:
                text_benchmarks = self.extract_from_text(soup, game_title, game_url)
                benchmarks.extend(text_benchmarks)
                
        except Exception as e:
            logger.error(f"Error extracting benchmarks from {game_url}: {e}")
        
        return benchmarks
    
    def extract_fallback_benchmarks(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Extract benchmarks using fallback methods when structured data isn't available"""
        benchmarks = []
        
        try:
            # Try to extract from any remaining text content
            text_benchmarks = self.extract_from_text(soup, game_title, game_url)
            benchmarks.extend(text_benchmarks)
            
            # Look for any performance mentions in the page
            performance_mentions = soup.find_all(text=re.compile(r'\d+\s*FPS', re.I))
            
            for mention in performance_mentions:
                try:
                    # Extract FPS value
                    fps_match = re.search(r'(\d+(?:\.\d+)?)\s*FPS', mention, re.IGNORECASE)
                    if not fps_match:
                        continue
                    
                    fps_value = float(fps_match.group(1))
                    
                    # Try to find hardware context
                    parent = mention.parent
                    gpu_name = "Unknown GPU"
                    cpu_name = "Unknown CPU"
                    
                    # Look for hardware names in nearby elements
                    if parent:
                        # Look for GPU mentions
                        gpu_elements = parent.find_all(text=re.compile(r'RTX|GTX|RX|Radeon|GeForce', re.I))
                        if gpu_elements:
                            gpu_name = self.clean_text(gpu_elements[0])
                        
                        # Look for CPU mentions
                        cpu_elements = parent.find_all(text=re.compile(r'Intel|AMD|Ryzen|Core|i[3579]', re.I))
                        if cpu_elements:
                            cpu_name = self.clean_text(cpu_elements[0])
                    
                    # Create benchmark if we have valid data
                    if gpu_name != "Unknown GPU" or cpu_name != "Unknown CPU":
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
                        benchmarks.append(benchmark)
                        
                except Exception as e:
                    logger.debug(f"Failed to parse performance mention: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in fallback extraction: {e}")
        
        return benchmarks

    def extract_structured_benchmarks(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Extract benchmarks from structured data like tables and lists"""
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
            
            # Look for structured divs with performance data
            performance_divs = soup.find_all('div', class_=re.compile(r'benchmark|performance|result|score', re.I))
            for div in performance_divs:
                div_benchmarks = self.parse_structured_div(div, game_title, game_url)
                benchmarks.extend(div_benchmarks)
                
        except Exception as e:
            logger.error(f"Error extracting structured benchmarks: {e}")
        
        return benchmarks

    def extract_chart_benchmarks(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Extract benchmarks from charts and graphs"""
        benchmarks = []
        
        try:
            # Look for chart containers
            chart_containers = soup.find_all(['div', 'section'], class_=re.compile(r'chart|graph|performance|benchmark', re.I))
            
            for chart in chart_containers:
                # Look for chart data points
                data_points = chart.find_all(['div', 'span'], class_=re.compile(r'data|point|value|fps', re.I))
                
                for point in data_points:
                    benchmark = self.parse_chart_data_point(point, game_title, game_url)
                    if benchmark:
                        benchmarks.append(benchmark)
                
                # Look for chart tooltips or legends
                tooltips = chart.find_all(['div', 'span'], class_=re.compile(r'tooltip|legend|label', re.I))
                for tooltip in tooltips:
                    benchmark = self.parse_chart_data_point(tooltip, game_title, game_url)
                    if benchmark:
                        benchmarks.append(benchmark)
                        
        except Exception as e:
            logger.error(f"Error extracting chart benchmarks: {e}")
        
        return benchmarks

    def extract_text_benchmarks(self, soup: BeautifulSoup, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Extract benchmarks from text content - TUNED FOR TECHPOWERUP WITH EXPANDED CONTEXT"""
        benchmarks = []
        
        try:
            # Get all text content
            text_content = soup.get_text()
            
            # TUNED: Look for TechPowerUp specific FPS patterns
            print(f"🔍 Analyzing text content for FPS data...")
            
            # Pattern 1: "X FPS" format (most common)
            fps_pattern1 = re.findall(r'(\d+(?:\.\d+)?)\s*FPS', text_content, re.IGNORECASE)
            print(f"   Pattern 'X FPS': {len(fps_pattern1)} matches - {fps_pattern1[:5]}")
            
            # Pattern 2: "X fps" format
            fps_pattern2 = re.findall(r'(\d+(?:\.\d+)?)\s*fps', text_content, re.IGNORECASE)
            print(f"   Pattern 'X fps': {len(fps_pattern2)} matches - {fps_pattern2[:5]}")
            
            # Pattern 3: "FPS: X" format
            fps_pattern3 = re.findall(r'FPS[:\s]+(\d+(?:\.\d+)?)', text_content, re.IGNORECASE)
            print(f"   Pattern 'FPS: X': {len(fps_pattern3)} matches - {fps_pattern3[:5]}")
            
            # Combine all FPS values
            all_fps_values = list(set(fps_pattern1 + fps_pattern2 + fps_pattern3))
            print(f"   Total unique FPS values: {len(all_fps_values)} - {all_fps_values}")
            
            if not all_fps_values:
                print("   ❌ No FPS values found in text")
                return benchmarks
            
            # ENHANCED: Look for hardware context in larger text blocks
            print(f"🔍 Looking for hardware context with expanded search...")
            
            # Split text into larger chunks (paragraphs) for better context
            paragraphs = re.split(r'\n\s*\n', text_content)
            print(f"   Found {len(paragraphs)} text paragraphs")
            
            for fps_value in all_fps_values:
                print(f"   🔍 Processing FPS value: {fps_value}")
                
                # Find paragraphs containing this FPS value
                relevant_paragraphs = []
                for paragraph in paragraphs:
                    if fps_value in paragraph and ('fps' in paragraph.lower() or 'FPS' in paragraph):
                        relevant_paragraphs.append(paragraph.strip())
                
                print(f"      Found {len(relevant_paragraphs)} relevant paragraphs")
                
                # Process each relevant paragraph
                for i, paragraph in enumerate(relevant_paragraphs[:3]):  # Process first 3 paragraphs
                    print(f"      Analyzing paragraph {i+1}: {paragraph[:150]}...")
                    
                    # ENHANCED: Look for hardware names in this paragraph
                    gpu_names = self.extract_gpu_names_from_text(paragraph)
                    cpu_names = self.extract_cpu_names_from_text(paragraph)
                    
                    print(f"         GPU names found: {gpu_names}")
                    print(f"         CPU names found: {cpu_names}")
                    
                    # ENHANCED: If no hardware found in this paragraph, look in nearby paragraphs
                    if not gpu_names or not cpu_names:
                        print(f"         🔍 Expanding search to nearby paragraphs...")
                        
                        # Look in paragraphs before and after this one
                        # Use a more robust approach to find nearby paragraphs
                        try:
                            # Find the index of this paragraph in the list
                            paragraph_index = -1
                            for idx, para in enumerate(paragraphs):
                                if paragraph in para or para in paragraph:
                                    paragraph_index = idx
                                    break
                            
                            if paragraph_index >= 0:
                                print(f"            Found paragraph at index: {paragraph_index}")
                                
                                # Check previous paragraph
                                if paragraph_index > 0:
                                    prev_paragraph = paragraphs[paragraph_index - 1]
                                    prev_gpu = self.extract_gpu_names_from_text(prev_paragraph)
                                    prev_cpu = self.extract_cpu_names_from_text(prev_paragraph)
                                    
                                    if prev_gpu and not gpu_names:
                                        gpu_names.extend(prev_gpu)
                                        print(f"            Found GPUs in previous paragraph: {prev_gpu}")
                                    
                                    if prev_cpu and not cpu_names:
                                        cpu_names.extend(prev_cpu)
                                        print(f"            Found CPUs in previous paragraph: {prev_cpu}")
                                
                                # Check next paragraph
                                if paragraph_index < len(paragraphs) - 1:
                                    next_paragraph = paragraphs[paragraph_index + 1]
                                    next_gpu = self.extract_gpu_names_from_text(next_paragraph)
                                    next_cpu = self.extract_cpu_names_from_text(next_paragraph)
                                    
                                    if next_gpu and not gpu_names:
                                        gpu_names.extend(next_gpu)
                                        print(f"            Found GPUs in next paragraph: {next_gpu}")
                                    
                                    if next_cpu and not cpu_names:
                                        cpu_names.extend(next_cpu)
                                        print(f"            Found CPUs in next paragraph: {next_cpu}")
                            else:
                                print(f"            Could not find paragraph index, searching nearby text blocks...")
                                
                                # Fallback: search in nearby text blocks by looking for similar content
                                for idx, para in enumerate(paragraphs):
                                    if any(word in para.lower() for word in ['graphics', 'settings', 'fps', 'performance']):
                                        nearby_gpu = self.extract_gpu_names_from_text(para)
                                        nearby_cpu = self.extract_cpu_names_from_text(para)
                                        
                                        if nearby_gpu and not gpu_names:
                                            gpu_names.extend(nearby_gpu)
                                            print(f"            Found GPUs in nearby paragraph: {nearby_gpu}")
                                        
                                        if nearby_cpu and not cpu_names:
                                            cpu_names.extend(nearby_cpu)
                                            print(f"            Found CPUs in nearby paragraph: {nearby_cpu}")
                                        
                                        if len(gpu_names) > 0 and len(cpu_names) > 0:
                                            break
                                
                        except Exception as e:
                            print(f"            Error in nearby paragraph search: {e}")
                            print(f"            Falling back to page-wide search...")
                        
                        # Remove duplicates
                        gpu_names = list(set(gpu_names))
                        cpu_names = list(set(cpu_names))
                        print(f"         Final hardware list - GPUs: {gpu_names}, CPUs: {cpu_names}")
                    
                    # ENHANCED: Also look for hardware in the entire page context
                    if not gpu_names or not cpu_names:
                        print(f"         🔍 Searching entire page for hardware context...")
                        
                        # Look for hardware mentions in the whole page
                        all_gpu_mentions = self.extract_gpu_names_from_text(text_content)
                        all_cpu_mentions = self.extract_cpu_names_from_text(text_content)
                        
                        if all_gpu_mentions and not gpu_names:
                            gpu_names = all_gpu_mentions[:3]  # Take first 3
                            print(f"            Found GPUs in page context: {gpu_names}")
                        
                        if all_cpu_mentions and not cpu_names:
                            cpu_names = all_cpu_mentions[:3]  # Take first 3
                            print(f"            Found CPUs in page context: {cpu_names}")
                    
                    # Create benchmarks for each hardware combination
                    if gpu_names and cpu_names:
                        for gpu_name in gpu_names[:2]:  # Limit to first 2 GPUs
                            for cpu_name in cpu_names[:2]:  # Limit to first 2 CPUs
                                benchmark = BenchmarkData(
                                    gpu_name=gpu_name,
                                    cpu_name=cpu_name,
                                    game_title=game_title,
                                    resolution="1080p",  # Default assumption
                                    settings="High",     # Default assumption
                                    avg_fps=float(fps_value),
                                    min_fps=float(fps_value) * 0.8,  # Estimate
                                    max_fps=float(fps_value) * 1.2,  # Estimate
                                    source_url=game_url,
                                    source_site=self.name,
                                    timestamp=pd.Timestamp.now().isoformat()
                                )
                                benchmarks.append(benchmark)
                                print(f"         ✅ Created benchmark: {gpu_name} + {cpu_name} = {fps_value} FPS")
                    
                    elif gpu_names:
                        # Only GPU found, use generic CPU
                        for gpu_name in gpu_names[:2]:
                            benchmark = BenchmarkData(
                                gpu_name=gpu_name,
                                cpu_name="Unknown CPU",
                                game_title=game_title,
                                resolution="1080p",
                                settings="High",
                                avg_fps=float(fps_value),
                                min_fps=float(fps_value) * 0.8,
                                max_fps=float(fps_value) * 1.2,
                                source_url=game_url,
                                source_site=self.name,
                                timestamp=pd.Timestamp.now().isoformat()
                            )
                            benchmarks.append(benchmark)
                            print(f"         ✅ Created benchmark: {gpu_name} + Unknown CPU = {fps_value} FPS")
                    
                    elif cpu_names:
                        # Only CPU found, use generic GPU
                        for cpu_name in cpu_names[:2]:
                            benchmark = BenchmarkData(
                                gpu_name="Unknown GPU",
                                cpu_name=cpu_name,
                                game_title=game_title,
                                resolution="1080p",
                                settings="High",
                                avg_fps=float(fps_value),
                                min_fps=float(fps_value) * 0.8,
                                max_fps=float(fps_value) * 1.2,
                                source_url=game_url,
                                source_site=self.name,
                                timestamp=pd.Timestamp.now().isoformat()
                            )
                            benchmarks.append(benchmark)
                            print(f"         ✅ Created benchmark: Unknown GPU + {cpu_name} = {fps_value} FPS")
                    
                    else:
                        # No hardware found, create generic benchmark
                        benchmark = BenchmarkData(
                            gpu_name="Unknown GPU",
                            cpu_name="Unknown CPU",
                            game_title=game_title,
                            resolution="1080p",
                            settings="High",
                            avg_fps=float(fps_value),
                            min_fps=float(fps_value) * 0.8,
                            max_fps=float(fps_value) * 1.2,
                            source_url=game_url,
                            source_site=self.name,
                            timestamp=pd.Timestamp.now().isoformat()
                        )
                        benchmarks.append(benchmark)
                        print(f"         ✅ Created generic benchmark: Unknown GPU + Unknown CPU = {fps_value} FPS")
            
            print(f"🔍 Text extraction completed: {len(benchmarks)} benchmarks created")
            
            # Also use the existing text parsing methods as backup
            existing_benchmarks = self.extract_from_text(soup, game_title, game_url)
            benchmarks.extend(existing_benchmarks)
            
            return benchmarks
            
        except Exception as e:
            logger.error(f"Error extracting text benchmarks: {e}")
            return benchmarks

    def extract_gpu_names_from_text(self, text: str) -> List[str]:
        """Extract GPU names from text - ENHANCED FOR TECHPOWERUP"""
        gpu_names = []
        
        # Enhanced TechPowerUp specific GPU patterns
        gpu_patterns = [
            # Full GPU names with model numbers
            r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX|Radeon|GeForce)\s+\d+[A-Za-z0-9\s\-]*)',
            r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX)\s+\d+[A-Za-z0-9\s\-]*)',
            r'([A-Za-z0-9\s\-]+(?:Radeon|GeForce)\s+[A-Za-z0-9\s\-]*)',
            
            # GPU names without model numbers
            r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX|Radeon|GeForce)[A-Za-z0-9\s\-]*)',
            
            # Specific GPU series
            r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX)\s+\d+)',
            r'([A-Za-z0-9\s\-]+(?:Radeon|GeForce)\s+[A-Za-z0-9\s\-]*)',
            
            # Common GPU abbreviations
            r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX)\s+\d+[A-Za-z0-9\s\-]*)',
            r'([A-Za-z0-9\s\-]+(?:Radeon|GeForce)[A-Za-z0-9\s\-]*)',
        ]
        
        for pattern in gpu_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                clean_name = self.clean_text(match)
                if clean_name and len(clean_name) > 3 and clean_name not in gpu_names:
                    # Additional validation
                    if any(keyword in clean_name.lower() for keyword in ['rtx', 'gtx', 'rx', 'radeon', 'geforce']):
                        gpu_names.append(clean_name)
        
        return gpu_names

    def extract_cpu_names_from_text(self, text: str) -> List[str]:
        """Extract CPU names from text - ENHANCED FOR TECHPOWERUP"""
        cpu_names = []
        
        # Enhanced TechPowerUp specific CPU patterns
        cpu_patterns = [
            # Full CPU names with model numbers
            r'([A-Za-z0-9\s\-]+(?:Intel|AMD|Ryzen|Core)\s+[A-Za-z0-9\s\-]*)',
            r'([A-Za-z0-9\s\-]+(?:Intel|AMD)\s+[A-Za-z0-9\s\-]*)',
            r'([A-Za-z0-9\s\-]+(?:Ryzen|Core)\s+[A-Za-z0-9\s\-]*)',
            
            # CPU names without model numbers
            r'([A-Za-z0-9\s\-]+(?:Intel|AMD|Ryzen|Core)[A-Za-z0-9\s\-]*)',
            
            # Specific CPU series
            r'([A-Za-z0-9\s\-]+(?:Intel|AMD)\s+[A-Za-z0-9\s\-]*)',
            r'([A-Za-z0-9\s\-]+(?:Ryzen|Core)\s+[A-Za-z0-9\s\-]*)',
            
            # Common CPU abbreviations
            r'([A-Za-z0-9\s\-]+(?:Intel|AMD)[A-Za-z0-9\s\-]*)',
            r'([A-Za-z0-9\s\-]+(?:Ryzen|Core)[A-Za-z0-9\s\-]*)',
        ]
        
        for pattern in cpu_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                clean_name = self.clean_text(match)
                if clean_name and len(clean_name) > 3 and clean_name not in cpu_names:
                    # Additional validation
                    if any(keyword in clean_name.lower() for keyword in ['intel', 'amd', 'ryzen', 'core', 'i3', 'i5', 'i7', 'i9']):
                        cpu_names.append(clean_name)
        
        return cpu_names

    def parse_benchmark_table(self, table: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse benchmark data from HTML tables"""
        benchmarks = []
        
        try:
            rows = table.find_all('tr')
            if len(rows) < 2:  # Need at least header + data row
                return benchmarks
            
            # Try to identify column headers
            headers = rows[0].find_all(['th', 'td'])
            header_texts = [h.get_text().lower().strip() for h in headers]
            
            # Find column indices
            gpu_col = self.find_column_index(header_texts, ['gpu', 'graphics', 'card', 'video'])
            cpu_col = self.find_column_index(header_texts, ['cpu', 'processor', 'chip'])
            fps_col = self.find_column_index(header_texts, ['fps', 'performance', 'score', 'result'])
            res_col = self.find_column_index(header_texts, ['resolution', 'res', 'pixel'])
            settings_col = self.find_column_index(header_texts, ['settings', 'quality', 'preset'])
            
            # Parse data rows
            for row in rows[1:]:  # Skip header row
                cells = row.find_all(['td', 'th'])
                if len(cells) < max(filter(None, [gpu_col, cpu_col, fps_col])) + 1:
                    continue
                
                benchmark = self.create_benchmark_from_table_row(
                    cells, gpu_col, cpu_col, fps_col, res_col, settings_col, 
                    game_title, game_url
                )
                if benchmark:
                    benchmarks.append(benchmark)
                    
        except Exception as e:
            logger.error(f"Error parsing benchmark table: {e}")
        
        return benchmarks

    def parse_benchmark_list(self, list_elem: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse benchmark data from HTML lists"""
        benchmarks = []
        
        try:
            list_items = list_elem.find_all('li')
            
            for item in list_items:
                # Look for performance data in list items
                text = item.get_text()
                
                # Try to extract FPS and hardware info
                fps_match = re.search(r'(\d+(?:\.\d+)?)\s*FPS', text, re.IGNORECASE)
                if not fps_match:
                    continue
                
                fps_value = float(fps_match.group(1))
                
                # Extract hardware names
                gpu_name = self.extract_hardware_name(text, 'gpu')
                cpu_name = self.extract_hardware_name(text, 'cpu')
                
                if gpu_name or cpu_name:
                    benchmark = BenchmarkData(
                        gpu_name=gpu_name or "Unknown GPU",
                        cpu_name=cpu_name or "Unknown CPU",
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
                    benchmarks.append(benchmark)
                    
        except Exception as e:
            logger.error(f"Error parsing benchmark list: {e}")
        
        return benchmarks

    def parse_structured_div(self, div: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse benchmark data from structured div elements"""
        benchmarks = []
        
        try:
            # Look for performance data in structured divs
            performance_elements = div.find_all(['div', 'span'], class_=re.compile(r'fps|performance|score|result', re.I))
            
            for elem in performance_elements:
                benchmark = self.parse_performance_element(elem, game_title, game_url)
                if benchmark:
                    benchmarks.append(benchmark)
                    
        except Exception as e:
            logger.error(f"Error parsing structured div: {e}")
        
        return benchmarks

    def parse_performance_text(self, text_elem: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse performance data from text elements"""
        benchmarks = []
        
        try:
            text = text_elem.get_text()
            
            # Look for FPS mentions
            fps_matches = re.finditer(r'(\d+(?:\.\d+)?)\s*FPS', text, re.IGNORECASE)
            
            for match in fps_matches:
                fps_value = float(match.group(1))
                
                # Try to extract hardware context from surrounding text
                gpu_name = self.extract_hardware_name(text, 'gpu')
                cpu_name = self.extract_hardware_name(text, 'cpu')
                
                if gpu_name or cpu_name:
                    benchmark = BenchmarkData(
                        gpu_name=gpu_name or "Unknown GPU",
                        cpu_name=cpu_name or "Unknown CPU",
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
                    benchmarks.append(benchmark)
                    
        except Exception as e:
            logger.error(f"Error parsing performance text: {e}")
        
        return benchmarks

    def find_column_index(self, headers: List[str], keywords: List[str]) -> Optional[int]:
        """Find the index of a column based on header keywords"""
        for i, header in enumerate(headers):
            if any(keyword in header for keyword in keywords):
                return i
        return None

    def create_benchmark_from_table_row(self, cells: List[Tag], gpu_col: Optional[int], 
                                      cpu_col: Optional[int], fps_col: Optional[int],
                                      res_col: Optional[int], settings_col: Optional[int],
                                      game_title: str, game_url: str) -> Optional[BenchmarkData]:
        """Create a benchmark from table row data"""
        try:
            # Extract values from cells
            gpu_name = cells[gpu_col].get_text().strip() if gpu_col is not None and gpu_col < len(cells) else "Unknown GPU"
            cpu_name = cells[cpu_col].get_text().strip() if cpu_col is not None and cpu_col < len(cells) else "Unknown CPU"
            
            # Extract FPS value
            fps_value = None
            if fps_col is not None and fps_col < len(cells):
                fps_text = cells[fps_col].get_text()
                fps_value = self.extract_fps_value(fps_text)
            
            if not fps_value:
                return None
            
            # Extract resolution and settings
            resolution = "1080p"
            if res_col is not None and res_col < len(cells):
                res_text = cells[res_col].get_text()
                extracted_res = self.extract_resolution_from_text(res_text)
                if extracted_res:
                    resolution = extracted_res
            
            settings = "High"
            if settings_col is not None and settings_col < len(cells):
                settings_text = cells[settings_col].get_text()
                extracted_settings = self.extract_settings_from_text(settings_text)
                if extracted_settings:
                    settings = extracted_settings
            
            return BenchmarkData(
                gpu_name=self.clean_text(gpu_name),
                cpu_name=self.clean_text(cpu_name),
                game_title=game_title,
                resolution=resolution,
                settings=settings,
                avg_fps=fps_value,
                min_fps=fps_value * 0.8,
                max_fps=fps_value * 1.2,
                source_url=game_url,
                source_site=self.name,
                timestamp=pd.Timestamp.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error creating benchmark from table row: {e}")
            return None

    def extract_hardware_name(self, text: str, hardware_type: str) -> Optional[str]:
        """Extract hardware name from text based on type"""
        if hardware_type == 'gpu':
            # Look for GPU patterns
            gpu_patterns = [
                r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX|Radeon|GeForce)[A-Za-z0-9\s\-]*)',
                r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX)\s+\d+[A-Za-z0-9\s\-]*)',
                r'([A-Za-z0-9\s\-]+(?:Radeon|GeForce)[A-Za-z0-9\s\-]*)'
            ]
        else:  # CPU
            # Look for CPU patterns
            gpu_patterns = [
                r'([A-Za-z0-9\s\-]+(?:Intel|AMD|Ryzen|Core|i[3579])[A-Za-z0-9\s\-]*)',
                r'([A-Za-z0-9\s\-]+(?:Intel|AMD)[A-Za-z0-9\s\-]*)',
                r'([A-Za-z0-9\s\-]+(?:Ryzen|Core)[A-Za-z0-9\s\-]*)'
            ]
        
        for pattern in gpu_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return self.clean_text(match.group(1))
        
        return None

    def extract_fps_value(self, text: str) -> Optional[float]:
        """Extract FPS value from text"""
        fps_match = re.search(r'(\d+(?:\.\d+)?)', text)
        if fps_match:
            try:
                return float(fps_match.group(1))
            except ValueError:
                pass
        return None

    def extract_resolution_from_text(self, text: str) -> Optional[str]:
        """Extract resolution from text"""
        resolution_patterns = [r'(\d{3,4}p)', r'(\d{3,4}x\d{3,4})', r'(4k|1440p|1080p)', r'(\d{3,4})p']
        
        for pattern in resolution_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1)
        
        return None

    def extract_settings_from_text(self, text: str) -> Optional[str]:
        """Extract graphics settings from text"""
        settings_keywords = ['low', 'medium', 'high', 'ultra', 'max', 'min', 'normal', 'extreme']
        
        text_lower = text.lower()
        for setting in settings_keywords:
            if setting in text_lower:
                return setting.title()
        
        return None

    def parse_performance_element(self, elem: Tag, game_title: str, game_url: str) -> Optional[BenchmarkData]:
        """Parse performance data from individual elements"""
        try:
            text = elem.get_text()
            
            # Extract FPS value
            fps_match = re.search(r'(\d+(?:\.\d+)?)\s*FPS', text, re.IGNORECASE)
            if not fps_match:
                return None
            
            fps_value = float(fps_match.group(1))
            
            # Extract hardware names from context
            gpu_name = self.extract_gpu_from_context(elem)
            cpu_name = self.extract_cpu_from_context(elem)
            
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
            logger.debug(f"Error parsing performance element: {e}")
        
        return None
    
    def extract_game_title(self, soup: BeautifulSoup) -> str:
        """Extract game title from page"""
        # Try multiple selectors for game title
        title_selectors = [
            'h1', 'h2', '.game-title', '.title', '[class*="title"]',
            'title', 'meta[property="og:title"]', '.software-name'
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
            path_parts = url_path.split('/')
            if len(path_parts) > 2:
                return path_parts[-1].replace('-', ' ').title()
        
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
            chart_data = chart.find_all(['div', 'span'], class_=re.compile(r'data|value|fps|performance|score', re.I))
            
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
                r'([A-Za-z0-9\s\-]+)\s*\+\s*([A-Za-z0-9\s\-]+)\s*=\s*(\d+(?:\.\d+)?)\s*FPS',
                # TechPowerUp specific: "Performance: 120 FPS"
                r'Performance:\s*(\d+(?:\.\d+)?)\s*FPS',
                # "Score: 120"
                r'Score:\s*(\d+(?:\.\d+)?)'
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
                                cpu_name = "Unknown CPU"
                            else:
                                cpu_name = hardware_name
                                gpu_name = "Unknown GPU"
                                
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
                                resolution="1080p",
                                settings="High",
                                avg_fps=fps_value,
                                min_fps=fps_value * 0.8,
                                max_fps=fps_value * 1.2,
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
    
    def parse_performance_indicator(self, indicator: Tag, game_title: str, game_url: str) -> List[BenchmarkData]:
        """Parse TechPowerUp specific performance indicators"""
        benchmarks = []
        
        try:
            text = indicator.get_text()
            
            # Look for FPS values
            fps_match = re.search(r'(\d+(?:\.\d+)?)\s*FPS', text, re.IGNORECASE)
            if not fps_match:
                return benchmarks
            
            fps_value = float(fps_match.group(1))
            
            # Try to extract hardware names from context
            gpu_name = self.extract_gpu_from_context(indicator)
            cpu_name = self.extract_cpu_from_context(indicator)
            
            if gpu_name and cpu_name:
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
                benchmarks.append(benchmark)
            
        except Exception as e:
            logger.debug(f"Error parsing performance indicator: {e}")
        
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
        gpu_keywords = ['rtx', 'gtx', 'rx', 'radeon', 'geforce', 'gpu', 'graphics', 'video']
        
        for cell in cells:
            text = cell.get_text().lower()
            if any(keyword in text for keyword in gpu_keywords):
                return self.clean_text(cell.get_text())
        
        return None
    
    def extract_cpu_name(self, cells: List[Tag]) -> Optional[str]:
        """Extract CPU name from cells"""
        cpu_keywords = ['intel', 'amd', 'ryzen', 'core', 'i3', 'i5', 'i7', 'i9', 'pentium']
        
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
