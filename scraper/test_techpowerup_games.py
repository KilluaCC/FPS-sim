#!/usr/bin/env python3
"""
Test TechPowerUp Game Review Pages - Extract Real FPS Data
Tests specific game review pages to see what benchmark data we can actually extract
"""

import sys
import os
import time
import random
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_specific_game_pages():
    """Test specific game review pages for FPS data"""
    print("🎮 Testing TechPowerUp Game Review Pages")
    print("=" * 60)
    
    # Specific game review pages to test
    game_pages = [
        {
            "name": "Metal Gear Solid Delta: Snake Eater",
            "url": "https://www.techpowerup.com/review/metal-gear-solid-delta-snake-eater/",
            "expected": "Game review with performance data"
        },
        {
            "name": "Intel Arc B580 Review",
            "url": "https://www.techpowerup.com/review/intel-arc-b580/31.html",
            "expected": "GPU review with gaming benchmarks"
        },
        {
            "name": "Corsair Xeneon Edge Review",
            "url": "https://www.techpowerup.com/review/corsair-xeneon-edge/",
            "expected": "Monitor review with gaming performance"
        }
    ]
    
    total_benchmarks = 0
    successful_pages = 0
    
    for i, game in enumerate(game_pages, 1):
        print(f"\n🎯 Testing Game {i}/{len(game_pages)}: {game['name']}")
        print("-" * 50)
        print(f"🌐 URL: {game['url']}")
        print(f"📋 Expected: {game['expected']}")
        
        try:
            # Test the page
            benchmarks = test_game_page(game['url'], game['name'])
            
            if benchmarks:
                print(f"✅ SUCCESS: Found {len(benchmarks)} benchmarks!")
                successful_pages += 1
                total_benchmarks += len(benchmarks)
                
                # Show sample benchmarks
                for j, benchmark in enumerate(benchmarks[:3]):
                    print(f"   📊 Benchmark {j+1}:")
                    print(f"      GPU: {benchmark.gpu_name}")
                    print(f"      CPU: {benchmark.cpu_name}")
                    print(f"      FPS: {benchmark.avg_fps}")
                    print(f"      Resolution: {benchmark.resolution}")
                    print(f"      Settings: {benchmark.settings}")
            else:
                print("⚠️  No benchmarks found, but page accessible")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        # Be respectful with delays
        if i < len(game_pages):
            delay = random.uniform(3, 5)
            print(f"⏳ Waiting {delay:.1f} seconds...")
            time.sleep(delay)
    
    # Summary
    print(f"\n" + "=" * 60)
    print("📊 GAME PAGE TESTING SUMMARY")
    print("=" * 60)
    print(f"✅ Successful pages: {successful_pages}/{len(game_pages)}")
    print(f"📊 Total benchmarks found: {total_benchmarks}")
    print(f"🎯 Average benchmarks per page: {total_benchmarks/successful_pages if successful_pages > 0 else 0:.1f}")
    
    return successful_pages > 0

def test_game_page(url: str, game_name: str):
    """Test a specific game page and extract benchmarks"""
    try:
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        scraper = TechPowerUpScraper()
        
        # Fetch the page
        print("🌐 Fetching page...")
        soup = scraper.fetch_page(url)
        
        if not soup:
            print("❌ Failed to fetch page")
            return []
        
        # Extract page title
        title = soup.title.string if soup.title else "No title"
        print(f"📝 Page title: {title}")
        
        # Look for FPS mentions in the page
        text_content = soup.get_text()
        fps_mentions = text_content.lower().count('fps')
        print(f"🔍 FPS mentions found: {fps_mentions}")
        
        # Look for hardware mentions
        gpu_mentions = text_content.lower().count('gpu') + text_content.lower().count('graphics')
        cpu_mentions = text_content.lower().count('cpu') + text_content.lower().count('processor')
        print(f"🔍 GPU mentions: {gpu_mentions}")
        print(f"🔍 CPU mentions: {cpu_mentions}")
        
        # Look for benchmark mentions
        benchmark_mentions = text_content.lower().count('benchmark')
        print(f"🔍 Benchmark mentions: {benchmark_mentions}")
        
        # Try to extract benchmarks using our parsing methods
        print("🔧 Testing parsing methods...")
        
        # 1. Structured benchmarks
        structured = scraper.extract_structured_benchmarks(soup, game_name, url)
        print(f"   📊 Structured: {len(structured)} benchmarks")
        
        # 2. Chart benchmarks
        charts = scraper.extract_chart_benchmarks(soup, game_name, url)
        print(f"   📈 Charts: {len(charts)} benchmarks")
        
        # 3. Text benchmarks
        text = scraper.extract_text_benchmarks(soup, game_name, url)
        print(f"   📝 Text: {len(text)} benchmarks")
        
        # 4. Fallback
        fallback = scraper.extract_fallback_benchmarks(soup, game_name, url)
        print(f"   🆘 Fallback: {len(fallback)} benchmarks")
        
        # Combine all benchmarks
        all_benchmarks = structured + charts + text + fallback
        
        # Remove duplicates based on GPU+CPU+Game combination
        unique_benchmarks = remove_duplicate_benchmarks(all_benchmarks)
        
        print(f"📊 Total unique benchmarks: {len(unique_benchmarks)}")
        
        return unique_benchmarks
        
    except Exception as e:
        print(f"❌ Error testing game page: {e}")
        import traceback
        traceback.print_exc()
        return []

def remove_duplicate_benchmarks(benchmarks):
    """Remove duplicate benchmarks based on GPU+CPU+Game combination"""
    seen = set()
    unique = []
    
    for benchmark in benchmarks:
        # Create a unique key
        key = (benchmark.gpu_name, benchmark.cpu_name, benchmark.game_title)
        
        if key not in seen:
            seen.add(key)
            unique.append(benchmark)
    
    return unique

def test_gpu_database_page():
    """Test the GPU database page for hardware data"""
    print("\n🖥️  Testing TechPowerUp GPU Database Page")
    print("-" * 50)
    
    try:
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        scraper = TechPowerUpScraper()
        url = "https://www.techpowerup.com/gpudb/"
        
        print(f"🌐 Testing: {url}")
        
        # Fetch the page
        soup = scraper.fetch_page(url)
        if not soup:
            print("❌ Failed to fetch GPU database page")
            return False
        
        # Look for GPU listings
        gpu_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text()
            
            # Look for GPU model links
            if any(keyword in text.lower() for keyword in ['rtx', 'gtx', 'rx', 'radeon', 'geforce']):
                if href.startswith('/'):
                    full_url = f"https://www.techpowerup.com{href}"
                else:
                    full_url = href
                
                if 'techpowerup.com' in full_url and 'gpu' in full_url.lower():
                    gpu_links.append((text.strip(), full_url))
        
        print(f"🔍 Found {len(gpu_links)} GPU model links")
        
        # Show some examples
        if gpu_links:
            print("📋 Sample GPU models:")
            for i, (name, url) in enumerate(gpu_links[:5]):
                print(f"   {i+1}. {name}")
                print(f"      URL: {url}")
        
        # Test a few GPU model pages
        test_gpu_pages = gpu_links[:3]  # Test first 3
        
        for i, (gpu_name, gpu_url) in enumerate(test_gpu_pages):
            print(f"\n🔍 Testing GPU {i+1}/{len(test_gpu_pages)}: {gpu_name}")
            
            try:
                gpu_soup = scraper.fetch_page(gpu_url)
                if gpu_soup:
                    # Look for performance data
                    text = gpu_soup.get_text()
                    fps_mentions = text.lower().count('fps')
                    benchmark_mentions = text.lower().count('benchmark')
                    
                    print(f"   📊 FPS mentions: {fps_mentions}")
                    print(f"   📊 Benchmark mentions: {benchmark_mentions}")
                    
                    if fps_mentions > 0 or benchmark_mentions > 0:
                        print("   ✅ Found performance data!")
                    else:
                        print("   ⚠️  No performance data found")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            # Small delay between GPU pages
            time.sleep(1)
        
        return len(gpu_links) > 0
        
    except Exception as e:
        print(f"❌ Error testing GPU database: {e}")
        return False

def test_cpu_database_page():
    """Test the CPU database page for hardware data"""
    print("\n🖥️  Testing TechPowerUp CPU Database Page")
    print("-" * 50)
    
    try:
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        scraper = TechPowerUpScraper()
        url = "https://www.techpowerup.com/cpudb/"
        
        print(f"🌐 Testing: {url}")
        
        # Fetch the page
        soup = scraper.fetch_page(url)
        if not soup:
            print("❌ Failed to fetch CPU database page")
            return False
        
        # Look for CPU listings
        cpu_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text()
            
            # Look for CPU model links
            if any(keyword in text.lower() for keyword in ['intel', 'amd', 'ryzen', 'core', 'i3', 'i5', 'i7', 'i9']):
                if href.startswith('/'):
                    full_url = f"https://www.techpowerup.com{href}"
                else:
                    full_url = href
                
                if 'techpowerup.com' in full_url and 'cpu' in full_url.lower():
                    cpu_links.append((text.strip(), full_url))
        
        print(f"🔍 Found {len(cpu_links)} CPU model links")
        
        # Show some examples
        if cpu_links:
            print("📋 Sample CPU models:")
            for i, (name, url) in enumerate(cpu_links[:5]):
                print(f"   {i+1}. {name}")
                print(f"      URL: {url}")
        
        return len(cpu_links) > 0
        
    except Exception as e:
        print(f"❌ Error testing CPU database: {e}")
        return False

def main():
    """Run all game page tests"""
    print("🚀 TechPowerUp Game Page Testing")
    print("=" * 60)
    
    # Test 1: Specific game review pages
    print("\n🧪 TEST 1: Game Review Pages")
    test1_success = test_specific_game_pages()
    
    # Test 2: GPU database page
    print("\n🧪 TEST 2: GPU Database Page")
    test2_success = test_gpu_database_page()
    
    # Test 3: CPU database page
    print("\n🧪 TEST 3: CPU Database Page")
    test3_success = test_cpu_database_page()
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎯 FINAL TEST RESULTS")
    print("=" * 60)
    print(f"✅ Game review pages: {'PASSED' if test1_success else 'FAILED'}")
    print(f"✅ GPU database page: {'PASSED' if test2_success else 'FAILED'}")
    print(f"✅ CPU database page: {'PASSED' if test3_success else 'FAILED'}")
    
    passed_tests = sum([test1_success, test2_success, test3_success])
    total_tests = 3
    
    print(f"\n📊 Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! TechPowerUp game pages are accessible.")
        return True
    elif passed_tests > total_tests / 2:
        print("\n⚠️  MOST TESTS PASSED. TechPowerUp game pages are mostly accessible.")
        return True
    else:
        print("\n❌ MANY TESTS FAILED. TechPowerUp game pages have issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
