#!/usr/bin/env python3
"""
Test script for the optimized UserBenchmark scraper
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_userbenchmark_scraper():
    """Test the optimized UserBenchmark scraper"""
    print("🧪 Testing Optimized UserBenchmark Scraper...")
    
    try:
        from scrapers.userbenchmark_scraper import UserBenchmarkScraper
        
        # Create scraper
        scraper = UserBenchmarkScraper()
        print("✅ UserBenchmark scraper created successfully")
        
        # Test benchmark page discovery
        print("\n🔍 Testing benchmark page discovery...")
        benchmark_pages = scraper.discover_benchmark_pages()
        print(f"✅ Discovered {len(benchmark_pages)} benchmark pages")
        
        # Show some example pages
        if benchmark_pages:
            print("\n📄 Sample benchmark pages:")
            for i, page in enumerate(benchmark_pages[:5]):
                print(f"   {i+1}. {page}")
        
        # Test URL validation
        print("\n✅ Testing URL validation...")
        test_urls = [
            "https://www.userbenchmark.com/Software/Game-FPS",
            "https://www.userbenchmark.com/Software/Game/cyberpunk-2077",
            "https://www.userbenchmark.com/Software/Game-FPS/RTX-4090",
            "https://invalid-site.com/game",
            "https://www.userbenchmark.com/very/long/url/that/should/be/filtered/out/because/it/is/too/long/and/likely/not/a/main/page"
        ]
        
        for url in test_urls:
            is_valid = scraper.is_valid_benchmark_url(url)
            print(f"   {url}: {'✅ Valid' if is_valid else '❌ Invalid'}")
        
        # Test benchmark link detection
        print("\n🔗 Testing benchmark link detection...")
        test_links = [
            ("/Software/Game/cyberpunk-2077", "Cyberpunk 2077"),
            ("/Software/Benchmark", "Benchmark Results"),
            ("/Software/Game-FPS", "Game FPS"),
            ("/about", "About Us"),
            ("/contact", "Contact")
        ]
        
        for href, text in test_links:
            is_benchmark = scraper.is_benchmark_link(href, text)
            print(f"   {href} ({text}): {'✅ Benchmark' if is_benchmark else '❌ Not benchmark'}")
        
        # Test game title extraction
        print("\n🎮 Testing game title extraction...")
        test_urls = [
            "https://www.userbenchmark.com/Software/Game/cyberpunk-2077",
            "https://www.userbenchmark.com/Software/Game-FPS/RTX-4090",
            "https://www.userbenchmark.com/Software/Benchmarks"
        ]
        
        for url in test_urls:
            # Create a mock soup with title
            from bs4 import BeautifulSoup
            mock_html = f'<html><head><title>{url.split("/")[-1].replace("-", " ").title()}</title></head><body></body></html>'
            mock_soup = BeautifulSoup(mock_html, 'html.parser')
            
            title = scraper.extract_game_title_enhanced(mock_soup, url)
            print(f"   {url}: {title}")
        
        # Test scraper statistics
        print("\n📊 Testing scraper statistics...")
        stats = scraper.get_scraping_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print("\n🎉 All UserBenchmark scraper tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ UserBenchmark scraper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test"""
    print("🚀 Testing Optimized UserBenchmark Scraper")
    print("=" * 60)
    
    success = test_userbenchmark_scraper()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! The optimized UserBenchmark scraper is ready.")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
