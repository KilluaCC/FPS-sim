#!/usr/bin/env python3
"""
Proxy Manager for FPS Benchmark Scraper
Handles proxy rotation, authentication, and failover to bypass anti-bot measures.
"""

import random
import time
import logging
import requests
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

@dataclass
class ProxyConfig:
    """Configuration for a single proxy"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"
    country: Optional[str] = None
    speed: Optional[float] = None
    last_used: float = 0.0
    fail_count: int = 0
    max_fails: int = 3
    
    @property
    def url(self) -> str:
        """Get proxy URL string"""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"
    
    @property
    def dict(self) -> Dict[str, str]:
        """Get proxy dict for requests"""
        if self.username and self.password:
            return {
                "http": f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}",
                "https": f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
            }
        return {
            "http": f"{self.protocol}://{self.host}:{self.port}",
            "https": f"{self.protocol}://{self.host}:{self.port}"
        }

class ProxyManager:
    """Manages proxy rotation and failover"""
    
    def __init__(self, proxy_list: Optional[List[ProxyConfig]] = None):
        self.proxies = proxy_list or []
        self.current_proxy_index = 0
        self.proxy_health = {}  # Track proxy health
        self.last_rotation = time.time()
        self.rotation_interval = 60  # Rotate every 60 seconds
        
        # Free proxy services (for testing)
        self.free_proxy_sources = [
            "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
        ]
        
        # Premium proxy services (you can add your own)
        self.premium_proxy_services = {
            "brightdata": {
                "username": "your_username",
                "password": "your_password",
                "host": "brd.superproxy.io",
                "port": 22225
            },
            "smartproxy": {
                "username": "your_username", 
                "password": "your_password",
                "host": "gate.smartproxy.com",
                "port": 7000
            }
        }
    
    def add_proxy(self, proxy: ProxyConfig):
        """Add a proxy to the pool"""
        self.proxies.append(proxy)
        logger.info(f"Added proxy: {proxy.host}:{proxy.port}")
    
    def add_proxy_from_dict(self, proxy_dict: Dict):
        """Add proxy from dictionary"""
        proxy = ProxyConfig(**proxy_dict)
        self.add_proxy(proxy)
    
    def load_free_proxies(self, max_proxies: int = 20):
        """Load free proxies from public sources"""
        logger.info("Loading free proxies from public sources...")
        
        for source in self.free_proxy_sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    lines = response.text.strip().split('\n')
                    for line in lines[:max_proxies]:
                        if ':' in line:
                            host, port = line.strip().split(':', 1)
                            try:
                                port = int(port)
                                proxy = ProxyConfig(host=host, port=port)
                                self.add_proxy(proxy)
                            except ValueError:
                                continue
                    break
            except Exception as e:
                logger.warning(f"Failed to load proxies from {source}: {e}")
                continue
        
        logger.info(f"Loaded {len(self.proxies)} free proxies")
    
    def load_premium_proxies(self, service_name: str):
        """Load premium proxies from a service"""
        if service_name not in self.premium_proxy_services:
            logger.error(f"Unknown premium proxy service: {service_name}")
            return
        
        service = self.premium_proxy_services[service_name]
        proxy = ProxyConfig(
            host=service["host"],
            port=service["port"],
            username=service["username"],
            password=service["password"],
            protocol="http"
        )
        self.add_proxy(proxy)
        logger.info(f"Added premium proxy from {service_name}")
    
    def get_next_proxy(self) -> Optional[ProxyConfig]:
        """Get next available proxy with rotation logic"""
        if not self.proxies:
            return None
        
        # Check if we need to rotate
        if time.time() - self.last_rotation > self.rotation_interval:
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
            self.last_rotation = time.time()
        
        # Find a working proxy
        attempts = 0
        while attempts < len(self.proxies):
            proxy = self.proxies[self.current_proxy_index]
            
            # Skip proxies that have failed too many times
            if proxy.fail_count >= proxy.max_fails:
                self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
                attempts += 1
                continue
            
            # Check if proxy is healthy
            if self.is_proxy_healthy(proxy):
                proxy.last_used = time.time()
                return proxy
            
            # Mark proxy as failed
            proxy.fail_count += 1
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
            attempts += 1
        
        # If all proxies failed, reset fail counts and try again
        logger.warning("All proxies failed, resetting fail counts")
        for proxy in self.proxies:
            proxy.fail_count = 0
        
        return self.proxies[0] if self.proxies else None
    
    def is_proxy_healthy(self, proxy: ProxyConfig) -> bool:
        """Check if a proxy is working"""
        try:
            test_url = "http://httpbin.org/ip"
            response = requests.get(
                test_url,
                proxies=proxy.dict,
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Proxy {proxy.host}:{proxy.port} health check failed: {e}")
            return False
    
    def mark_proxy_failed(self, proxy: ProxyConfig):
        """Mark a proxy as failed"""
        proxy.fail_count += 1
        logger.warning(f"Proxy {proxy.host}:{proxy.port} failed ({proxy.fail_count}/{proxy.max_fails})")
        
        if proxy.fail_count >= proxy.max_fails:
            logger.error(f"Proxy {proxy.host}:{proxy.port} marked as permanently failed")
    
    def get_proxy_stats(self) -> Dict:
        """Get statistics about proxy pool"""
        total = len(self.proxies)
        working = sum(1 for p in self.proxies if p.fail_count < p.max_fails)
        failed = total - working
        
        return {
            "total_proxies": total,
            "working_proxies": working,
            "failed_proxies": failed,
            "current_proxy": self.current_proxy_index,
            "rotation_interval": self.rotation_interval
        }
    
    def create_session_with_proxy(self, proxy: ProxyConfig) -> requests.Session:
        """Create a requests session with proxy configuration"""
        session = requests.Session()
        
        # Configure proxy
        session.proxies.update(proxy.dict)
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504, 521],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set headers to look more like a real browser
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        })
        
        return session

# Default proxy configurations for testing
DEFAULT_PROXIES = [
    # Add some example proxies here (replace with real ones)
    # ProxyConfig(host="proxy1.example.com", port=8080),
    # ProxyConfig(host="proxy2.example.com", port=8080),
]

def create_proxy_manager(use_free_proxies: bool = True, premium_service: Optional[str] = None) -> ProxyManager:
    """Factory function to create a proxy manager"""
    manager = ProxyManager()
    
    # Add default proxies if any
    for proxy in DEFAULT_PROXIES:
        manager.add_proxy(proxy)
    
    # Load free proxies if requested
    if use_free_proxies:
        manager.load_free_proxies()
    
    # Load premium proxies if specified
    if premium_service:
        manager.load_premium_proxies(premium_service)
    
    return manager
