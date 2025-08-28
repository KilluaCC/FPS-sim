#!/usr/bin/env python3
"""
Inspect TechPowerUp Page Structure - See Actual FPS Data Format
Quickly inspect the HTML to understand how FPS data is structured
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def inspect_game_page():
    """Inspect the actual HTML structure of a game page"""
    print("🔍 Inspecting TechPowerUp Page Structure")
    print("=" * 50)
    
    try:
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        scraper = TechPowerUpScraper()
        
        # Test the same game page
        test_url = "https://www.techpowerup.com/review/metal-gear-solid-delta-snake-eater/"
        game_name = "Metal Gear Solid Delta: Snake Eater"
        
        print(f"🎯 Inspecting: {game_name}")
        print(f"🌐 URL: {test_url}")
        
        # Fetch the page
        print("🌐 Fetching page...")
        soup = scraper.fetch_page(test_url)
        
        if not soup:
            print("❌ Failed to fetch page")
            return False
        
        # Look for FPS mentions in context
        print("\n🔍 Looking for FPS mentions in context...")
        fps_elements = soup.find_all(text=lambda text: text and 'fps' in text.lower())
        
        if fps_elements:
            print(f"✅ Found {len(fps_elements)} FPS mentions:")
            for i, element in enumerate(fps_elements[:5]):  # Show first 5
                print(f"\n   📊 FPS Mention {i+1}:")
                print(f"      Text: {element.strip()}")
                
                # Show parent context
                parent = element.parent
                if parent:
                    parent_text = parent.get_text().strip()
                    if len(parent_text) < 200:  # Not too long
                        print(f"      Context: {parent_text}")
        else:
            print("❌ No FPS mentions found")
        
        # Look for benchmark mentions in context
        print("\n🔍 Looking for benchmark mentions in context...")
        benchmark_elements = soup.find_all(text=lambda text: text and 'benchmark' in text.lower())
        
        if benchmark_elements:
            print(f"✅ Found {len(benchmark_elements)} benchmark mentions:")
            for i, element in enumerate(benchmark_elements[:3]):  # Show first 3
                print(f"\n   📊 Benchmark Mention {i+1}:")
                print(f"      Text: {element.strip()}")
                
                # Show parent context
                parent = element.parent
                if parent:
                    parent_text = parent.get_text().strip()
                    if len(parent_text) < 200:  # Not too long
                        print(f"      Context: {parent_text}")
        else:
            print("❌ No benchmark mentions found")
        
        # Look for performance data in tables
        print("\n🔍 Looking for performance tables...")
        tables = soup.find_all('table')
        print(f"📊 Found {len(tables)} tables")
        
        for i, table in enumerate(tables[:3]):  # Check first 3 tables
            print(f"\n   📋 Table {i+1}:")
            
            # Check table headers
            headers = table.find_all(['th', 'td'])
            if headers:
                header_texts = [h.get_text().strip() for h in headers[:5]]  # First 5 cells
                print(f"      Headers: {header_texts}")
            
            # Check if table has performance data
            table_text = table.get_text().lower()
            if 'fps' in table_text:
                print(f"      ✅ Contains FPS data!")
            if 'gpu' in table_text or 'graphics' in table_text:
                print(f"      ✅ Contains GPU data!")
            if 'cpu' in table_text or 'processor' in table_text:
                print(f"      ✅ Contains CPU data!")
        
        # Look for performance divs
        print("\n🔍 Looking for performance divs...")
        performance_divs = soup.find_all(['div', 'section'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['performance', 'benchmark', 'fps', 'result']))
        
        if performance_divs:
            print(f"✅ Found {len(performance_divs)} performance divs:")
            for i, div in enumerate(performance_divs[:3]):  # Show first 3
                print(f"\n   📊 Performance Div {i+1}:")
                div_text = div.get_text().strip()
                if len(div_text) < 300:  # Not too long
                    print(f"      Content: {div_text}")
                else:
                    print(f"      Content: {div_text[:300]}...")
        else:
            print("❌ No performance divs found")
        
        # Look for specific FPS patterns
        print("\n🔍 Looking for specific FPS patterns...")
        page_text = soup.get_text()
        
        # Pattern 1: "X FPS" format
        import re
        fps_pattern1 = re.findall(r'(\d+(?:\.\d+)?)\s*FPS', page_text, re.IGNORECASE)
        if fps_pattern1:
            print(f"✅ Pattern 'X FPS': {fps_pattern1}")
        
        # Pattern 2: "X fps" format
        fps_pattern2 = re.findall(r'(\d+(?:\.\d+)?)\s*fps', page_text, re.IGNORECASE)
        if fps_pattern2:
            print(f"✅ Pattern 'X fps': {fps_pattern2}")
        
        # Pattern 3: "FPS: X" format
        fps_pattern3 = re.findall(r'FPS[:\s]+(\d+(?:\.\d+)?)', page_text, re.IGNORECASE)
        if fps_pattern3:
            print(f"✅ Pattern 'FPS: X': {fps_pattern3}")
        
        # Pattern 4: "Performance: X FPS" format
        fps_pattern4 = re.findall(r'Performance[:\s]+(\d+(?:\.\d+)?)\s*FPS', page_text, re.IGNORECASE)
        if fps_pattern4:
            print(f"✅ Pattern 'Performance: X FPS': {fps_pattern4}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the inspection"""
    print("🔍 TechPowerUp Page Structure Inspection")
    print("=" * 50)
    
    success = inspect_game_page()
    
    if success:
        print("\n✅ Inspection completed successfully!")
        print("🔧 Now we can tune our parsing patterns based on what we found.")
    else:
        print("\n❌ Inspection failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
