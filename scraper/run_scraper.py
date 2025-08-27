#!/usr/bin/env python3
"""
Main scraper runner script
Orchestrates all scrapers and saves benchmark data to CSV.
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Add the scraper directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import ScraperManager
from scrapers.gpucheck_scraper import GPUCheckScraper
from scrapers.userbenchmark_scraper import UserBenchmarkScraper
from scrapers.techpowerup_scraper import TechPowerUpScraper

def main():
    """Main scraping function"""
    print("🚀 Starting FPS Benchmark Scraper")
    print("=" * 50)
    
    # Initialize scraper manager
    manager = ScraperManager(output_dir="output")
    
    # Add scrapers
    print("📋 Adding scrapers...")
    
    # GPUCheck with proxy rotation
    gpucheck_scraper = GPUCheckScraper(use_proxies=True)
    manager.add_scraper(gpucheck_scraper)
    
    manager.add_scraper(UserBenchmarkScraper())
    manager.add_scraper(TechPowerUpScraper())
    
    print(f"✅ Added {len(manager.scrapers)} scrapers")
    print()
    
    # Run all scrapers
    print("🔄 Running scrapers...")
    try:
        df = manager.run_all_scrapers()
        
        if not df.empty:
            print("\n📊 Scraping Results:")
            print(f"   Total benchmarks: {len(df)}")
            print(f"   Unique GPUs: {df['gpu_name'].nunique()}")
            print(f"   Unique CPUs: {df['cpu_name'].nunique()}")
            print(f"   Unique games: {df['game_title'].nunique()}")
            print(f"   Sources: {', '.join(df['source_site'].unique())}")
            
            # Show data completeness
            print("\n📈 Data Completeness:")
            for field in ['avg_fps', 'min_fps', 'max_fps', 'resolution', 'settings']:
                completeness = df[field].notna().sum() / len(df) * 100
                print(f"   {field}: {completeness:.1f}%")
            
            # Show sample data
            print("\n🔍 Sample Data:")
            print(df.head(3).to_string(index=False))
            
            # Show proxy statistics for GPUCheck
            if 'gpucheck_scraper' in locals() and hasattr(gpucheck_scraper, 'get_proxy_stats'):
                proxy_stats = gpucheck_scraper.get_proxy_stats()
                print("\n🌐 Proxy Statistics:")
                for key, value in proxy_stats.items():
                    print(f"   {key}: {value}")
            
            # Show UserBenchmark scraper statistics
            if hasattr(manager.scrapers[1], 'get_scraping_stats'):
                ub_stats = manager.scrapers[1].get_scraping_stats()
                print("\n📊 UserBenchmark Scraper Statistics:")
                for key, value in ub_stats.items():
                    print(f"   {key}: {value}")
            
            # Save additional formats
            print("\n💾 Saving data...")
            
            # Save as JSON for easy processing
            json_path = os.path.join("output", "benchmarks.json")
            df.to_json(json_path, orient='records', indent=2)
            print(f"   JSON: {json_path}")
            
            # Save as Excel for manual review
            excel_path = os.path.join("output", "benchmarks.xlsx")
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"   Excel: {excel_path}")
            
            # Create a summary report
            create_summary_report(df)
            
        else:
            print("❌ No data was scraped")
            
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return 1
    
    print("\n✅ Scraping completed successfully!")
    return 0

def create_summary_report(df: pd.DataFrame):
    """Create a detailed summary report"""
    report_path = os.path.join("output", "detailed_report.txt")
    
    with open(report_path, 'w') as f:
        f.write("FPS Benchmark Scraping Report\n")
        f.write("=" * 40 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("Overview\n")
        f.write("-" * 10 + "\n")
        f.write(f"Total benchmarks: {len(df)}\n")
        f.write(f"Unique GPUs: {df['gpu_name'].nunique()}\n")
        f.write(f"Unique CPUs: {df['cpu_name'].nunique()}\n")
        f.write(f"Unique games: {df['game_title'].nunique()}\n")
        f.write(f"Sources: {', '.join(df['source_site'].unique())}\n\n")
        
        f.write("Data Quality\n")
        f.write("-" * 12 + "\n")
        for field in ['avg_fps', 'min_fps', 'max_fps', 'resolution', 'settings']:
            completeness = df[field].notna().sum() / len(df) * 100
            f.write(f"{field}: {completeness:.1f}% complete\n")
        f.write("\n")
        
        f.write("Top GPUs by Frequency\n")
        f.write("-" * 22 + "\n")
        gpu_counts = df['gpu_name'].value_counts().head(10)
        for gpu, count in gpu_counts.items():
            f.write(f"{gpu}: {count} benchmarks\n")
        f.write("\n")
        
        f.write("Top CPUs by Frequency\n")
        f.write("-" * 21 + "\n")
        cpu_counts = df['cpu_name'].value_counts().head(10)
        for cpu, count in cpu_counts.items():
            f.write(f"{cpu}: {count} benchmarks\n")
        f.write("\n")
        
        f.write("Top Games by Frequency\n")
        f.write("-" * 22 + "\n")
        game_counts = df['game_title'].value_counts().head(10)
        for game, count in game_counts.items():
            f.write(f"{game}: {count} benchmarks\n")
        f.write("\n")
        
        f.write("Performance Distribution\n")
        f.write("-" * 24 + "\n")
        if df['avg_fps'].notna().any():
            fps_stats = df['avg_fps'].describe()
            f.write(f"Average FPS - Mean: {fps_stats['mean']:.1f}, Median: {fps_stats['50%']:.1f}\n")
            f.write(f"FPS Range: {fps_stats['min']:.1f} - {fps_stats['max']:.1f}\n")
    
    print(f"   Detailed Report: {report_path}")

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
