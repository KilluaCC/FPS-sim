#!/usr/bin/env python3
"""
Test TechPowerUp Single Page - Extract Real FPS Data
Test the single-page review format that contains the actual benchmark data
"""

import sys
import os
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_single_page_review():
    """Test the single-page review format for FPS data"""
    print("🎯 Testing TechPowerUp Single Page Review")
    print("=" * 50)
    
    try:
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        scraper = TechPowerUpScraper()
        
        # Test the single-page version that has the FPS data
        test_url = "https://www.techpowerup.com/review/metal-gear-solid-delta-snake-eater/single-page.html"
        game_name = "Metal Gear Solid Delta: Snake Eater"
        
        print(f"🎮 Testing: {game_name}")
        print(f"🌐 URL: {test_url}")
        
        # Fetch the single-page review
        print("🌐 Fetching single-page review...")
        soup = scraper.fetch_page(test_url)
        
        if not soup:
            print("❌ Failed to fetch single-page review")
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
        
        # Look for actual FPS values
        print("\n🔍 Looking for FPS values...")
        fps_values = re.findall(r'(\d+(?:\.\d+)?)\s*FPS', text_content, re.IGNORECASE)
        if fps_values:
            print(f"✅ Found {len(fps_values)} FPS values:")
            # Show unique values
            unique_fps = list(set(fps_values))
            print(f"   Unique FPS values: {unique_fps[:10]}")  # Show first 10
        
        # Look for FPS patterns in context
        print("\n🔍 Looking for FPS patterns in context...")
        fps_patterns = [
            r'(\d+(?:\.\d+)?)\s*FPS',                    # "60 FPS"
            r'FPS[:\s]+(\d+(?:\.\d+)?)',                 # "FPS: 60"
            r'Performance[:\s]+(\d+(?:\.\d+)?)\s*FPS',   # "Performance: 60 FPS"
            r'(\d+(?:\.\d+)?)\s*fps',                    # "60 fps"
            r'(\d+(?:\.\d+)?)\s*Frames',                 # "60 Frames"
        ]
        
        for pattern in fps_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                print(f"   Pattern '{pattern}': {len(matches)} matches")
        
        # Look for hardware + FPS combinations
        print("\n🔍 Looking for hardware + FPS combinations...")
        
        # Pattern: "RTX 3080: 60 FPS" or similar
        hardware_fps_patterns = [
            r'([A-Za-z0-9\s\-]+(?:RTX|GTX|RX|Radeon|GeForce)[A-Za-z0-9\s\-]*)[:\s]+(\d+(?:\.\d+)?)\s*FPS',
            r'([A-Za-z0-9\s\-]+(?:Intel|AMD|Ryzen|Core|i[3579])[A-Za-z0-9\s\-]*)[:\s]+(\d+(?:\.\d+)?)\s*FPS',
            r'(\d+(?:\.\d+)?)\s*FPS[:\s]+([A-Za-z0-9\s\-]+(?:RTX|GTX|RX|Radeon|GeForce)[A-Za-z0-9\s\-]*)',
        ]
        
        for pattern in hardware_fps_patterns:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                print(f"   Hardware+FPS pattern '{pattern}': {len(matches)} matches")
                for i, match in enumerate(matches[:3]):  # Show first 3
                    print(f"     {i+1}. {match}")
        
        # Test our parsing methods on this page
        print("\n🔧 Testing parsing methods on single-page...")
        
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
        print(f"\n📊 Total benchmarks extracted: {total}")
        
        if total > 0:
            print("✅ SUCCESS: Our parsing methods are working!")
            # Show sample benchmarks
            all_benchmarks = structured + text + fallback
            for i, benchmark in enumerate(all_benchmarks[:3]):
                print(f"\n📋 Benchmark {i+1}:")
                print(f"   GPU: {benchmark.gpu_name}")
                print(f"   CPU: {benchmark.cpu_name}")
                print(f"   FPS: {benchmark.avg_fps}")
                print(f"   Resolution: {benchmark.resolution}")
                print(f"   Settings: {benchmark.settings}")
        else:
            print("⚠️  No benchmarks extracted - parsing needs tuning")
            
            # Let's look at the actual HTML structure
            print("\n🔍 Examining HTML structure for parsing clues...")
            
            # Look for tables
            tables = soup.find_all('table')
            print(f"   📋 Tables found: {len(tables)}")
            
            # Look for performance-related divs
            perf_divs = soup.find_all(['div', 'section'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['performance', 'benchmark', 'fps', 'result', 'test']))
            print(f"   📊 Performance divs: {len(perf_divs)}")
            
            # Look for specific content sections
            content_sections = soup.find_all(['div', 'section'], string=re.compile(r'benchmark|performance|fps|test|result', re.I))
            print(f"   📝 Content sections: {len(content_sections)}")
        
        return total > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the single page test"""
    print("🎯 TechPowerUp Single Page FPS Data Test")
    print("=" * 50)
    
    success = test_single_page_review()
    
    if success:
        print("\n✅ Single page test completed successfully!")
        print("🎯 We found and extracted FPS benchmark data!")
    else:
        print("\n⚠️  Single page test completed, but no data extracted.")
        print("🔧 Our parsing methods need further tuning.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
