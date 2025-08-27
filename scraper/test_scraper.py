#!/usr/bin/env python3
"""
Test script for the FPS Benchmark Scraper
Tests individual components and basic functionality.
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add the scraper directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from scraper import BaseScraper, BenchmarkData, ScraperManager
        print("✅ Core scraper modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import core modules: {e}")
        return False
    
    try:
        from scrapers.gpucheck_scraper import GPUCheckScraper
        print("✅ GPUCheck scraper imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import GPUCheck scraper: {e}")
        return False
    
    try:
        from scrapers.userbenchmark_scraper import UserBenchmarkScraper
        print("✅ UserBenchmark scraper imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import UserBenchmark scraper: {e}")
        return False
    
    try:
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        print("✅ TechPowerUp scraper imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import TechPowerUp scraper: {e}")
        return False
    
    return True

def test_data_structure():
    """Test the BenchmarkData structure"""
    print("\n🧪 Testing data structure...")
    
    try:
        from scraper import BenchmarkData
        
        # Create test data
        test_data = BenchmarkData(
            gpu_name="RTX 3080",
            cpu_name="Ryzen 7 5800X",
            game_title="Cyberpunk 2077",
            resolution="1080p",
            settings="High",
            avg_fps=120.5,
            min_fps=95.2,
            max_fps=145.8,
            source_url="https://example.com",
            source_site="TestSite",
            timestamp=datetime.now().isoformat()
        )
        
        print("✅ BenchmarkData structure created successfully")
        print(f"   GPU: {test_data.gpu_name}")
        print(f"   CPU: {test_data.cpu_name}")
        print(f"   Game: {test_data.game_title}")
        print(f"   FPS: {test_data.avg_fps}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create test data: {e}")
        return False

def test_scraper_manager():
    """Test the ScraperManager"""
    print("\n🧪 Testing scraper manager...")
    
    try:
        from scraper import ScraperManager
        from scrapers.gpucheck_scraper import GPUCheckScraper
        from scrapers.userbenchmark_scraper import UserBenchmarkScraper
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        # Create manager
        manager = ScraperManager(output_dir="test_output")
        
        # Add scrapers
        manager.add_scraper(GPUCheckScraper())
        manager.add_scraper(UserBenchmarkScraper())
        manager.add_scraper(TechPowerUpScraper())
        
        print(f"✅ ScraperManager created with {len(manager.scrapers)} scrapers")
        
        # Test statistics
        stats = manager.get_statistics()
        print(f"   Initial stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test scraper manager: {e}")
        return False

def test_individual_scrapers():
    """Test individual scraper initialization"""
    print("\n🧪 Testing individual scrapers...")
    
    try:
        from scrapers.gpucheck_scraper import GPUCheckScraper
        from scrapers.userbenchmark_scraper import UserBenchmarkScraper
        from scrapers.techpowerup_scraper import TechPowerUpScraper
        
        # Test GPUCheck scraper
        gpucheck = GPUCheckScraper()
        print(f"✅ GPUCheck scraper initialized: {gpucheck.name}")
        print(f"   Base URL: {gpucheck.base_url}")
        
        # Test UserBenchmark scraper
        userbenchmark = UserBenchmarkScraper()
        print(f"✅ UserBenchmark scraper initialized: {userbenchmark.name}")
        print(f"   Base URL: {userbenchmark.base_url}")
        
        # Test TechPowerUp scraper
        techpowerup = TechPowerUpScraper()
        print(f"✅ TechPowerUp scraper initialized: {techpowerup.name}")
        print(f"   Base URL: {techpowerup.base_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test individual scrapers: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    
    try:
        import config
        
        print("✅ Configuration loaded successfully")
        print(f"   Max pages per site: {config.SCRAPING_CONFIG['max_pages_per_site']}")
        print(f"   Min delay: {config.SCRAPING_CONFIG['min_delay']}s")
        print(f"   Max delay: {config.SCRAPING_CONFIG['max_delay']}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False

def test_output_directory():
    """Test output directory creation"""
    print("\n🧪 Testing output directory...")
    
    try:
        output_dir = "test_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Test file creation
        test_file = os.path.join(output_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Test file created successfully")
        
        print(f"✅ Output directory '{output_dir}' created and writable")
        
        # Cleanup
        os.remove(test_file)
        os.rmdir(output_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to test output directory: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Running FPS Benchmark Scraper Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Structure Test", test_data_structure),
        ("Scraper Manager Test", test_scraper_manager),
        ("Individual Scrapers Test", test_individual_scrapers),
        ("Configuration Test", test_configuration),
        ("Output Directory Test", test_output_directory)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The scraper is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
