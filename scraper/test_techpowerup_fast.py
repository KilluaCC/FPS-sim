#!/usr/bin/env python3
"""
Fast TechPowerUp Test - Quick FPS Data Check
Quickly tests one game review page to see what benchmark data we can extract
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_single_game_page():
    """Quick test of one game review page"""
    print("🎮 Fast TechPowerUp Test - Single Game Page")
    print("=" * 50)
    
    try:
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        scraper = TechPowerUpScraper()
        
        # Test just one game review page
        test_url = "https://www.techpowerup.com/review/metal-gear-solid-delta-snake-eater/"
        game_name = "Metal Gear Solid Delta: Snake Eater"
        
        print(f"🎯 Testing: {game_name}")
        print(f"🌐 URL: {test_url}")
        
        # Fetch the page
        print("🌐 Fetching page...")
        soup = scraper.fetch_page(test_url)
        
        if not soup:
            print("❌ Failed to fetch page")
            return False
        
        # Quick content analysis
        text_content = soup.get_text()
        fps_mentions = text_content.lower().count('fps')
        gpu_mentions = text_content.lower().count('gpu') + text_content.lower().count('graphics')
        cpu_mentions = text_content.lower().count('cpu') + text_content.lower().count('processor')
        benchmark_mentions = text_content.lower().count('benchmark')
        
        print(f"📊 Content Analysis:")
        print(f"   FPS mentions: {fps_mentions}")
        print(f"   GPU mentions: {gpu_mentions}")
        print(f"   CPU mentions: {cpu_mentions}")
        print(f"   Benchmark mentions: {benchmark_mentions}")
        
        # Quick parsing test
        print("\n🔧 Quick Parsing Test:")
        
        # Test structured extraction
        structured = scraper.extract_structured_benchmarks(soup, game_name, test_url)
        print(f"   📊 Structured: {len(structured)} benchmarks")
        
        # Test text extraction
        text = scraper.extract_text_benchmarks(soup, game_name, test_url)
        print(f"   📝 Text: {len(text)} benchmarks")
        
        # Test fallback
        fallback = scraper.extract_fallback_benchmarks(soup, game_name, test_url)
        print(f"   🆘 Fallback: {len(fallback)} benchmarks")
        
        total = len(structured) + len(text) + len(fallback)
        print(f"\n📊 Total benchmarks found: {total}")
        
        if total > 0:
            print("✅ SUCCESS: Found benchmark data!")
            # Show first benchmark
            all_benchmarks = structured + text + fallback
            if all_benchmarks:
                first = all_benchmarks[0]
                print(f"\n📋 Sample benchmark:")
                print(f"   GPU: {first.gpu_name}")
                print(f"   CPU: {first.cpu_name}")
                print(f"   FPS: {first.avg_fps}")
                print(f"   Resolution: {first.resolution}")
                print(f"   Settings: {first.settings}")
        else:
            print("⚠️  No benchmarks found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gpu_db_quick():
    """Quick test of GPU database page"""
    print("\n🖥️  Quick GPU Database Test")
    print("-" * 30)
    
    try:
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        scraper = TechPowerUpScraper()
        url = "https://www.techpowerup.com/gpudb/"
        
        print(f"🌐 Testing: {url}")
        
        soup = scraper.fetch_page(url)
        if not soup:
            print("❌ Failed to fetch GPU database")
            return False
        
        # Quick GPU count
        gpu_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text()
            
            if any(keyword in text.lower() for keyword in ['rtx', 'gtx', 'rx', 'radeon', 'geforce']):
                if 'gpu' in href.lower():
                    gpu_links.append(text.strip())
        
        print(f"🔍 Found {len(gpu_links)} GPU models")
        
        if gpu_links:
            print("📋 Sample GPUs:")
            for i, name in enumerate(gpu_links[:3]):
                print(f"   {i+1}. {name}")
        
        return len(gpu_links) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run fast tests"""
    print("⚡ Fast TechPowerUp Data Check")
    print("=" * 50)
    
    # Test 1: Single game page
    print("\n🧪 TEST 1: Single Game Review Page")
    test1_success = test_single_game_page()
    
    # Test 2: GPU database
    print("\n🧪 TEST 2: GPU Database Page")
    test2_success = test_gpu_db_quick()
    
    # Quick summary
    print("\n" + "=" * 50)
    print("🎯 QUICK TEST RESULTS")
    print("=" * 50)
    print(f"✅ Game page: {'PASSED' if test1_success else 'FAILED'}")
    print(f"✅ GPU database: {'PASSED' if test2_success else 'FAILED'}")
    
    passed = sum([test1_success, test2_success])
    print(f"\n📊 Overall: {passed}/2 tests passed")
    
    if passed == 2:
        print("🎉 TechPowerUp is working and accessible!")
    elif passed == 1:
        print("⚠️  TechPowerUp is partially working.")
    else:
        print("❌ TechPowerUp has issues.")
    
    return passed > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
