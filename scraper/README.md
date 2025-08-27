# FPS Benchmark Data Scraper 🚀

A modular Python web scraper for extracting FPS performance data from gaming benchmark sites like GPUCheck and UserBenchmark. This scraper is designed to integrate seamlessly with your existing FPS Estimator project.

## 🎯 Features

- **Modular Design**: Easy to add new scraping sources
- **Respectful Scraping**: Built-in delays and user agent rotation
- **Error Handling**: Graceful handling of HTTP errors and network issues
- **Multiple Output Formats**: CSV, JSON, and Excel export
- **Data Validation**: Ensures data quality and completeness
- **Progress Tracking**: Real-time progress updates and logging
- **Configurable**: Easy to adjust scraping parameters

## 📋 Requirements

- Python 3.8+
- Internet connection
- Respect for website terms of service

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd scraper
pip install -r requirements.txt
```

### 2. Run the Scraper

```bash
python run_scraper.py
```

### 3. Check Results

The scraper will create an `output/` directory with:
- `benchmarks.csv` - Main data file
- `benchmarks.json` - JSON format for easy processing
- `benchmarks.xlsx` - Excel format for manual review
- `scraping_summary.txt` - Summary statistics
- `detailed_report.txt` - Comprehensive analysis

## 🏗️ Architecture

### Core Components

```
scraper/
├── scraper.py              # Base classes and utilities
├── run_scraper.py          # Main runner script
├── config.py               # Configuration settings
├── scrapers/               # Site-specific scrapers
│   ├── gpucheck_scraper.py
│   └── userbenchmark_scraper.py
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Class Structure

- **`BaseScraper`**: Abstract base class for all scrapers
- **`ScraperManager`**: Coordinates multiple scrapers
- **`BenchmarkData`**: Data structure for benchmark results
- **Site-specific scrapers**: Implement scraping logic for each site

## 🔧 Configuration

### Environment Variables

```bash
# Enable development mode (faster, fewer pages)
export SCRAPER_DEV_MODE=true

# Custom output directory
export SCRAPER_OUTPUT_DIR=custom_output
```

### Configuration File

Edit `config.py` to customize:
- Scraping delays and limits
- Site-specific settings
- Output formats
- Logging levels
- Validation rules

## 📊 Data Structure

Each benchmark record contains:

```python
@dataclass
class BenchmarkData:
    gpu_name: str          # Graphics card name
    cpu_name: str          # Processor name
    game_title: str        # Game title
    resolution: str        # Resolution (e.g., "1080p")
    settings: str          # Graphics settings (e.g., "High")
    avg_fps: float         # Average FPS
    min_fps: float         # Minimum FPS
    max_fps: float         # Maximum FPS
    source_url: str        # Source page URL
    source_site: str       # Source website name
    timestamp: str         # Scraping timestamp
```

## 🆕 Adding New Scrapers

### 1. Create a New Scraper Class

```python
from scraper import BaseScraper, BenchmarkData

class NewSiteScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://newsite.com", "NewSite")
    
    def scrape_benchmarks(self) -> List[BenchmarkData]:
        # Implement scraping logic
        pass
    
    def parse_benchmark_page(self, soup: BeautifulSoup, url: str) -> Optional[BenchmarkData]:
        # Implement parsing logic
        pass
```

### 2. Add to Configuration

```python
# In config.py
SITE_CONFIGS['newsite'] = {
    'base_url': 'https://newsite.com',
    'enabled': True,
    'max_pages': 10,
    'delay_range': (2, 4),
    'selectors': {
        # Site-specific CSS selectors
    }
}
```

### 3. Register in Runner

```python
# In run_scraper.py
from scrapers.newsite_scraper import NewSiteScraper

manager.add_scraper(NewSiteScraper())
```

## 🛡️ Ethical Scraping

### Best Practices

- **Respect robots.txt**: Check site policies before scraping
- **Use delays**: Built-in delays between requests
- **Rotate user agents**: Avoid detection as a bot
- **Handle errors gracefully**: Don't overwhelm servers
- **Limit scope**: Only scrape necessary data
- **Monitor impact**: Check if you're affecting site performance

### Rate Limiting

The scraper includes:
- Random delays between requests (1-3 seconds)
- Exponential backoff for retries
- Maximum page limits per site
- Session management for efficiency

## 📈 Integration with Your Project

### 1. Import Scraped Data

```python
import pandas as pd

# Load scraped data
df = pd.read_csv('output/benchmarks.csv')

# Filter for specific hardware
rtx_3080_data = df[df['gpu_name'].str.contains('RTX 3080', case=False)]
```

### 2. Update Database

```python
# Use your existing database service
from services.database import dbService

for _, row in df.iterrows():
    await dbService.submitUserFPS({
        'gpuId': get_gpu_id(row['gpu_name']),
        'cpuId': get_cpu_id(row['cpu_name']),
        'gameId': get_game_id(row['game_title']),
        'resolution': row['resolution'],
        'settings': row['settings'],
        'avgFps': row['avg_fps'],
        'minFps': row['min_fps'],
        'maxFps': row['max_fps']
    })
```

### 3. Replace Estimation Logic

```python
# In your FPS estimation service
async def getFPSEstimate(gpuId, cpuId, gameId, resolution, settings):
    # First try to find real benchmark data
    benchmark = await find_benchmark(gpuId, cpuId, gameId, resolution, settings)
    
    if benchmark:
        return {
            'avgFPS': benchmark.avg_fps,
            'minFPS': benchmark.min_fps,
            'maxFPS': benchmark.max_fps,
            'source': 'real_benchmark'
        }
    
    # Fall back to estimation if no real data
    return await calculateEstimatedFPS(gpuId, cpuId, gameId, resolution, settings)
```

## 🧪 Testing

### Test Individual Scrapers

```python
# Test GPUCheck scraper
from scrapers.gpucheck_scraper import GPUCheckScraper

scraper = GPUCheckScraper()
benchmarks = scraper.scrape_benchmarks()
print(f"Scraped {len(benchmarks)} benchmarks")
```

### Test Data Processing

```python
# Test data validation and cleaning
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
    timestamp="2024-01-01T00:00:00"
)

print(test_data)
```

## 📝 Logging

The scraper provides comprehensive logging:

- **Console output**: Real-time progress updates
- **File logging**: Detailed logs saved to `scraper.log`
- **Error tracking**: Failed requests and parsing errors
- **Performance metrics**: Scraping speed and success rates

### Log Levels

- **INFO**: General progress and results
- **DEBUG**: Detailed parsing and request information
- **WARNING**: Non-critical issues
- **ERROR**: Failed requests or parsing errors

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're in the correct directory
2. **Network Timeouts**: Check internet connection and site availability
3. **Parsing Failures**: Sites may have changed their HTML structure
4. **Rate Limiting**: Increase delays if you encounter blocks

### Debug Mode

```bash
# Enable debug logging
export SCRAPER_DEV_MODE=true
python run_scraper.py
```

### Manual Testing

```python
# Test individual site accessibility
import requests

response = requests.get("https://gpucheck.com", timeout=30)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.content)}")
```

## 📚 Advanced Usage

### Custom Data Processing

```python
# Filter and process scraped data
df = pd.read_csv('output/benchmarks.csv')

# Filter for specific games
cyberpunk_data = df[df['game_title'].str.contains('Cyberpunk', case=False)]

# Group by GPU and calculate average FPS
gpu_performance = df.groupby('gpu_name')['avg_fps'].agg(['mean', 'count', 'std'])

# Export filtered data
cyberpunk_data.to_csv('output/cyberpunk_benchmarks.csv', index=False)
```

### Scheduled Scraping

```bash
# Add to crontab for daily updates
0 2 * * * cd /path/to/scraper && python run_scraper.py >> scraper_cron.log 2>&1
```

## 🤝 Contributing

### Adding New Sites

1. Study the target site's HTML structure
2. Create a new scraper class
3. Implement parsing logic
4. Add configuration
5. Test thoroughly
6. Update documentation

### Improving Existing Scrapers

1. Identify parsing issues
2. Update selectors and patterns
3. Add better error handling
4. Optimize performance
5. Test with real data

## 📄 License

This scraper is part of your FPS Estimator project. Use responsibly and in accordance with website terms of service.

## ⚠️ Disclaimer

- **Respect website terms**: Always check robots.txt and terms of service
- **Use responsibly**: Don't overload servers or violate rate limits
- **Data accuracy**: Scraped data may contain errors or be outdated
- **Legal compliance**: Ensure compliance with applicable laws and regulations

---

**Happy Scraping! 🎮📊**
