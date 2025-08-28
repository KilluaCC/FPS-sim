#!/usr/bin/env python3
"""
Test Individual Hardware Review Pages - Find Real FPS Data
Test specific review pages that should contain actual benchmark data
"""

import sys
import os
import time
import random
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_individual_review(url: str, site_name: str, review_type: str):
    """Test an individual review page for FPS benchmark data"""
    print(f"🔍 Testing: {site_name} - {review_type}")
    print(f"   URL: {url}")
    
    try:
        # Test access
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print(f"   ✅ Accessible (Status: {response.status_code})")
            
            # Analyze content for FPS data
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text().lower()
            
            # Look for FPS data
            fps_mentions = text_content.count('fps')
            benchmark_mentions = text_content.count('benchmark')
            performance_mentions = text_content.count('performance')
            
            print(f"   📊 Content Analysis:")
            print(f"      FPS mentions: {fps_mentions}")
            print(f"      Benchmark mentions: {benchmark_mentions}")
            print(f"      Performance mentions: {performance_mentions}")
            
            # Look for actual FPS values
            import re
            fps_values = re.findall(r'(\d+(?:\.\d+)?)\s*FPS', text_content, re.IGNORECASE)
            fps_values.extend(re.findall(r'(\d+(?:\.\d+)?)\s*fps', text_content, re.IGNORECASE))
            
            if fps_values:
                unique_fps = list(set(fps_values))
                print(f"      FPS values found: {len(unique_fps)} unique values")
                print(f"      Sample FPS values: {unique_fps[:10]}")
                
                # Check if these look like real benchmarks
                high_fps_count = sum(1 for fps in unique_fps if fps.isdigit() and int(fps) > 100)
                if high_fps_count > 0:
                    print(f"      🎯 HIGH FPS VALUES: {high_fps_count} values above 100 FPS (real benchmarks!)")
                elif len(unique_fps) > 5:
                    print(f"      ⚠️  Multiple FPS values but mostly low (might be settings)")
                else:
                    print(f"      ⚠️  Limited FPS values")
            else:
                print(f"      ❌ No FPS values found")
            
            # Look for benchmark tables
            tables = soup.find_all('table')
            print(f"      📋 Tables found: {len(tables)}")
            
            # Look for performance charts/graphs
            charts = soup.find_all(['div', 'section'], class_=lambda x: x and any(keyword in str(x).lower() for keyword in ['chart', 'graph', 'benchmark', 'performance']))
            print(f"      📈 Charts/graphs found: {len(charts)}")
            
            # Look for game-specific performance data
            games = ['cyberpunk', 'red dead', 'call of duty', 'fortnite', 'minecraft', 'gta', 'witcher', 'assassin']
            game_mentions = sum(text_content.count(game) for game in games)
            print(f"      🎮 Game mentions: {game_mentions}")
            
            # Overall assessment
            if len(fps_values) > 10 and high_fps_count > 0:
                print(f"   🎯 EXCELLENT: Rich FPS benchmark data found!")
                return "EXCELLENT"
            elif len(fps_values) > 5:
                print(f"   ✅ GOOD: Some FPS benchmark data found")
                return "GOOD"
            elif len(fps_values) > 0:
                print(f"   ⚠️  LIMITED: Some FPS data but may be settings")
                return "LIMITED"
            else:
                print(f"   ❌ POOR: No FPS benchmark data found")
                return "POOR"
                
        else:
            print(f"   ❌ Not accessible (Status: {response.status_code})")
            return "BLOCKED"
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return "ERROR"

def test_individual_reviews():
    """Test individual hardware review pages for FPS data"""
    print("🔍 Testing Individual Hardware Review Pages")
    print("=" * 60)
    
    # Test specific review pages that should contain FPS data
    reviews_to_test = [
        # Tom's Hardware - GPU Reviews
        {
            "name": "Tom's Hardware",
            "url": "https://www.tomshardware.com/reviews/nvidia-rtx-4090-gpu-review",
            "type": "RTX 4090 GPU Review",
            "expected": "Should have FPS benchmarks"
        },
        {
            "name": "Tom's Hardware", 
            "url": "https://www.tomshardware.com/reviews/amd-radeon-rx-7900-xtx-review",
            "type": "RX 7900 XTX Review",
            "expected": "Should have FPS benchmarks"
        },
        
        # AnandTech - CPU Reviews
        {
            "name": "AnandTech",
            "url": "https://www.anandtech.com/show/17047/the-amd-ryzen-9-7950x-and-ryzen-5-7600x-review",
            "type": "Ryzen 7000 Review",
            "expected": "Should have performance data"
        },
        
        # Guru3D - GPU Reviews
        {
            "name": "Guru3D",
            "url": "https://www.guru3d.com/articles-pages/geforce-rtx-4090-founder-review,1.html",
            "type": "RTX 4090 Review",
            "expected": "Should have FPS benchmarks"
        },
        
        # TechSpot - Alternative URL
        {
            "name": "TechSpot",
            "url": "https://www.techspot.com/review/2391-rtx-4090/",
            "type": "RTX 4090 Review",
            "expected": "Should have FPS benchmarks"
        }
    ]
    
    results = []
    
    for i, review in enumerate(reviews_to_test, 1):
        print(f"\n🧪 Review {i}/{len(reviews_to_test)}")
        print("-" * 40)
        
        quality = test_individual_review(review['url'], review['name'], review['type'])
        
        results.append({
            'name': review['name'],
            'url': review['url'],
            'type': review['type'],
            'expected': review['expected'],
            'quality': quality
        })
        
        # Be respectful with delays
        if i < len(reviews_to_test):
            delay = random.uniform(3, 5)
            print(f"   ⏳ Waiting {delay:.1f} seconds...")
            time.sleep(delay)
    
    # Summary and recommendations
    print(f"\n" + "=" * 60)
    print("🎯 INDIVIDUAL REVIEW TESTING SUMMARY")
    print("=" * 60)
    
    excellent = [r for r in results if r['quality'] == 'EXCELLENT']
    good = [r for r in results if r['quality'] == 'GOOD']
    limited = [r for r in results if r['quality'] == 'LIMITED']
    poor = [r for r in results if r['quality'] == 'POOR']
    blocked = [r for r in results if r['quality'] == 'BLOCKED']
    errors = [r for r in results if r['quality'] == 'ERROR']
    
    print(f"📊 Results Summary:")
    print(f"   🎯 Excellent: {len(excellent)} reviews")
    print(f"   ✅ Good: {len(good)} reviews")
    print(f"   ⚠️  Limited: {len(limited)} reviews")
    print(f"   ❌ Poor: {len(poor)} reviews")
    print(f"   🚫 Blocked: {len(blocked)} reviews")
    print(f"   ❌ Errors: {len(errors)} reviews")
    
    if excellent or good:
        print(f"\n🎯 PROMISING SITES (Individual Reviews):")
        for review in excellent + good:
            print(f"   ✅ {review['name']} - {review['type']}")
            print(f"      Quality: {review['quality']}")
            print(f"      URL: {review['url']}")
    
    if limited:
        print(f"\n⚠️  MODERATE SITES:")
        for review in limited:
            print(f"   ⚠️  {review['name']} - {review['type']}")
            print(f"      Quality: {review['quality']}")
    
    if poor or blocked or errors:
        print(f"\n❌ PROBLEMATIC SITES:")
        for review in poor + blocked + errors:
            print(f"   ❌ {review['name']} - {review['type']}")
            print(f"      Issue: {review['quality']}")
    
    print(f"\n💡 STRATEGIC INSIGHTS:")
    
    if excellent or good:
        print(f"   1. 🎯 Individual review pages DO contain FPS benchmark data!")
        print(f"   2. 🔍 Main pages are just overviews - we need to drill down")
        print(f"   3. 📊 Focus on building scrapers for high-quality review sites")
        print(f"   4. 🚀 This approach will give us real performance data")
    else:
        print(f"   1. ⚠️  Even individual reviews have limited FPS data")
        print(f"   2. 🔍 May need to look at different types of content")
        print(f"   3. 📊 Consider alternative data sources")
    
    return results

def main():
    """Run the individual review testing"""
    print("🔍 Individual Hardware Review FPS Data Test")
    print("=" * 60)
    
    results = test_individual_reviews()
    
    if results:
        print(f"\n✅ Individual review testing completed!")
        promising = len([r for r in results if r['quality'] in ['EXCELLENT', 'GOOD']])
        print(f"🎯 Found {promising} promising review sites")
    else:
        print(f"\n❌ Individual review testing failed!")
    
    return len(results) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
