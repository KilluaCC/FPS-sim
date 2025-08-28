#!/usr/bin/env python3
"""
Find TechPowerUp Benchmark Pages - Locate Actual FPS Data
Find the actual pages that contain the benchmark data with FPS values
"""

import sys
import os
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def find_benchmark_pages():
    """Find the actual benchmark pages with FPS data"""
    print("🔍 Finding TechPowerUp Benchmark Pages")
    print("=" * 50)
    
    try:
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        scraper = TechPowerUpScraper()
        
        # Start with the main review page
        main_url = "https://www.techpowerup.com/review/metal-gear-solid-delta-snake-eater/"
        print(f"🎯 Starting from: {main_url}")
        
        # Fetch the main page
        print("🌐 Fetching main review page...")
        main_soup = scraper.fetch_page(main_url)
        
        if not main_soup:
            print("❌ Failed to fetch main page")
            return False
        
        # Look for navigation links to other pages
        print("\n🔍 Looking for navigation links...")
        nav_links = []
        
        # Look for page navigation
        for link in main_soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text().lower()
            
            # Look for page navigation patterns
            if any(pattern in text for pattern in ['page', 'next', 'previous', '1', '2', '3', '4', '5']):
                if href.startswith('/'):
                    full_url = f"https://www.techpowerup.com{href}"
                else:
                    full_url = href
                
                if 'techpowerup.com' in full_url and 'review' in full_url:
                    nav_links.append((text.strip(), full_url))
        
        print(f"📋 Found {len(nav_links)} navigation links:")
        for i, (text, url) in enumerate(nav_links):
            print(f"   {i+1}. {text} -> {url}")
        
        # Look for benchmark-specific links
        print("\n🔍 Looking for benchmark-specific links...")
        benchmark_links = []
        
        for link in main_soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text().lower()
            
            # Look for benchmark-related links
            if any(keyword in text for keyword in ['benchmark', 'performance', 'fps', 'test', 'result']):
                if href.startswith('/'):
                    full_url = f"https://www.techpowerup.com{href}"
                else:
                    full_url = href
                
                if 'techpowerup.com' in full_url:
                    benchmark_links.append((text.strip(), full_url))
        
        print(f"📋 Found {len(benchmark_links)} benchmark links:")
        for i, (text, url) in enumerate(benchmark_links):
            print(f"   {i+1}. {text} -> {url}")
        
        # Look for section links within the same review
        print("\n🔍 Looking for section links...")
        section_links = []
        
        # Common TechPowerUp section patterns
        section_patterns = [
            r'/review/[^/]+/(\d+)\.html',  # /review/game/2.html
            r'/review/[^/]+/([^/]+)',      # /review/game/section
            r'/review/[^/]+/(\d+)$',       # /review/game/2
        ]
        
        for link in main_soup.find_all('a', href=True):
            href = link.get('href', '')
            
            for pattern in section_patterns:
                match = re.search(pattern, href)
                if match:
                    if href.startswith('/'):
                        full_url = f"https://www.techpowerup.com{href}"
                    else:
                        full_url = href
                    
                    if 'techpowerup.com' in full_url and 'review' in full_url:
                        section_links.append((match.group(1), full_url))
                    break
        
        print(f"📋 Found {len(section_links)} section links:")
        for i, (section, url) in enumerate(section_links):
            print(f"   {i+1}. Section {section} -> {url}")
        
        # Test a few potential benchmark pages
        test_urls = []
        test_urls.extend([url for _, url in nav_links[:3]])
        test_urls.extend([url for _, url in benchmark_links[:3]])
        test_urls.extend([url for _, url in section_links[:3]])
        
        # Remove duplicates
        test_urls = list(set(test_urls))
        
        print(f"\n🧪 Testing {len(test_urls)} potential benchmark pages...")
        
        for i, url in enumerate(test_urls):
            print(f"\n📄 Testing page {i+1}/{len(test_urls)}: {url}")
            
            try:
                page_soup = scraper.fetch_page(url)
                if not page_soup:
                    print("   ❌ Failed to fetch")
                    continue
                
                # Quick content check
                page_text = page_soup.get_text()
                fps_count = page_text.lower().count('fps')
                gpu_count = page_text.lower().count('gpu') + page_text.lower().count('graphics')
                cpu_count = page_text.lower().count('cpu') + page_text.lower().count('processor')
                
                print(f"   📊 FPS mentions: {fps_count}")
                print(f"   📊 GPU mentions: {gpu_count}")
                print(f"   📊 CPU mentions: {cpu_count}")
                
                if fps_count > 1:  # More than just the section header
                    print("   🎯 POTENTIAL BENCHMARK PAGE!")
                    
                    # Look for actual FPS values
                    fps_values = re.findall(r'(\d+(?:\.\d+)?)\s*FPS', page_text, re.IGNORECASE)
                    if fps_values:
                        print(f"   📊 FPS values found: {fps_values[:5]}")  # Show first 5
                    
                elif gpu_count > 10 or cpu_count > 10:
                    print("   ⚠️  Hardware-heavy page (might contain benchmarks)")
                else:
                    print("   ❌ Not a benchmark page")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the benchmark page finder"""
    print("🔍 TechPowerUp Benchmark Page Finder")
    print("=" * 50)
    
    success = find_benchmark_pages()
    
    if success:
        print("\n✅ Benchmark page search completed!")
        print("🎯 Now we know where the actual FPS data is located.")
    else:
        print("\n❌ Benchmark page search failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
