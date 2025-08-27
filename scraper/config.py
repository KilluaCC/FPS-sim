#!/usr/bin/env python3
"""
Configuration file for the FPS Benchmark Scraper
"""

import os
from typing import Dict, List

# Scraping Configuration
SCRAPING_CONFIG = {
    # Delays between requests (in seconds)
    'min_delay': 1.0,
    'max_delay': 3.0,
    
    # Retry configuration
    'max_retries': 3,
    'retry_delay': 1000,  # milliseconds
    
    # Request limits
    'max_pages_per_site': 10,  # Limit pages per site for demo
    'timeout': 30,  # Request timeout in seconds
    
    # User agent rotation
    'rotate_user_agents': True,
    
    # Output configuration
    'output_dir': 'output',
    'save_formats': ['csv', 'json', 'excel'],
    
    # Logging
    'log_level': 'INFO',
    'log_file': 'scraper.log'
}

# Site-specific configurations
SITE_CONFIGS = {
    'gpucheck': {
        'base_url': 'https://gpucheck.com',
        'enabled': True,
        'max_pages': 10,
        'delay_range': (2, 4),
        'selectors': {
            'game_links': ['a[href*="game"]', 'a[href*="benchmark"]'],
            'benchmark_tables': ['table', '.benchmark', '.performance'],
            'gpu_selectors': ['[class*="gpu"]', '[class*="graphics"]'],
            'cpu_selectors': ['[class*="cpu"]', '[class*="processor"]'],
            'fps_selectors': ['[class*="fps"]', '[class*="performance"]']
        }
    },
    
    'userbenchmark': {
        'base_url': 'https://www.userbenchmark.com',
        'enabled': True,
        'max_pages': 10,
        'delay_range': (2, 4),
        'selectors': {
            'game_links': ['a[href*="Software/Game"]', 'a[href*="benchmark"]'],
            'benchmark_tables': ['table', '.benchmark', '.result'],
            'gpu_selectors': ['[class*="gpu"]', '[class*="graphics"]'],
            'cpu_selectors': ['[class*="cpu"]', '[class*="processor"]'],
            'fps_selectors': ['[class*="fps"]', '[class*="score"]']
        }
    },
    
    'techpowerup': {
        'base_url': 'https://www.techpowerup.com',
        'enabled': True,
        'max_pages': 10,
        'delay_range': (2, 4),
        'selectors': {
            'game_links': ['a[href*="game"]', 'a[href*="benchmark"]', 'a[href*="review"]'],
            'benchmark_tables': ['table', '.benchmark', '.performance'],
            'gpu_selectors': ['[class*="gpu"]', '[class*="graphics"]'],
            'cpu_selectors': ['[class*="cpu"]', '[class*="processor"]'],
            'fps_selectors': ['[class*="fps"]', '[class*="performance"]']
        }
    }
}

# Data validation rules
VALIDATION_RULES = {
    'fps_range': (1, 1000),  # Valid FPS range
    'min_gpu_name_length': 3,
    'min_cpu_name_length': 3,
    'min_game_name_length': 2,
    
    # Required fields for a valid benchmark
    'required_fields': ['gpu_name', 'cpu_name', 'game_title', 'avg_fps'],
    
    # Field cleaning rules
    'text_cleaning': {
        'remove_chars': ['\n', '\r', '\t', '\xa0'],
        'normalize_whitespace': True,
        'strip_edges': True
    }
}

# Output file configurations
OUTPUT_CONFIG = {
    'csv': {
        'encoding': 'utf-8',
        'index': False,
        'date_format': '%Y-%m-%d %H:%M:%S'
    },
    'json': {
        'orient': 'records',
        'indent': 2,
        'date_format': 'iso'
    },
    'excel': {
        'engine': 'openpyxl',
        'index': False,
        'sheet_name': 'Benchmarks'
    }
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'scraper.log',
            'mode': 'w'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# Performance monitoring
PERFORMANCE_CONFIG = {
    'track_scraping_speed': True,
    'track_memory_usage': True,
    'track_success_rate': True,
    'save_performance_metrics': True
}

# Error handling
ERROR_HANDLING = {
    'continue_on_error': True,
    'log_errors': True,
    'save_error_log': True,
    'max_errors_per_site': 5
}

# Development/testing mode
DEV_MODE = os.getenv('SCRAPER_DEV_MODE', 'false').lower() == 'true'

if DEV_MODE:
    # Reduce limits for development
    SCRAPING_CONFIG['max_pages_per_site'] = 3
    SCRAPING_CONFIG['min_delay'] = 0.5
    SCRAPING_CONFIG['max_delay'] = 1.0
    LOGGING_CONFIG['loggers']['']['level'] = 'DEBUG'
