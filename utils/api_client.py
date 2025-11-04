"""
Smart API Client with Rate Limiting
"""

import requests
import time
import json
from utils.logger import setup_logger
from config.api_config import get_github_token, should_pause, get_delay

logger = setup_logger(__name__)

class SmartAPIClient:
    def __init__(self):
        self.requests_made = 0
        self.session = requests.Session()
        self.github_token = get_github_token()
        
        # Set default headers
        if self.github_token:
            self.session.headers.update({
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def get(self, url, params=None, headers=None, retries=3):
        """Smart GET request with rate limiting"""
        if should_pause(self.requests_made):
            logger.warning("⏸️ Approaching rate limit - pausing for 1 hour")
            time.sleep(3600)
            self.requests_made = 0
        
        # Respect rate limits
        time.sleep(get_delay())
        
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=30)
            self.requests_made += 1
            
            if response.status_code == 403 and 'rate limit' in response.text.lower():
                logger.warning("⚠️ Rate limit hit, implementing backoff...")
                time.sleep(60)  # 1 minute backoff
                return self.get(url, params, headers, retries - 1)
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API request failed: {e}")
            if retries > 0:
                logger.info(f"🔄 Retrying... ({retries} attempts left)")
                time.sleep(5)
                return self.get(url, params, headers, retries - 1)
            raise
    
    def post(self, url, data=None, json_data=None, headers=None, retries=3):
        """Smart POST request with rate limiting"""
        if should_pause(self.requests_made):
            logger.warning("⏸️ Approaching rate limit - pausing for 1 hour")
            time.sleep(3600)
            self.requests_made = 0
        
        time.sleep(get_delay())
        
        try:
            response = self.session.post(url, data=data, json=json_data, headers=headers, timeout=30)
            self.requests_made += 1
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API POST failed: {e}")
            if retries > 0:
                time.sleep(5)
                return self.post(url, data, json_data, headers, retries - 1)
            raise
    
    def get_github_rate_limit(self):
        """Check GitHub API rate limits"""
        if not self.github_token:
            return {"remaining": 0, "message": "No GitHub token"}
        
        try:
            response = self.get('https://api.github.com/rate_limit')
            data = response.json()
            return data['resources']['core']
        except Exception as e:
            logger.error(f"❌ Failed to get rate limit: {e}")
            return {"remaining": 0}
    
    def reset_counter(self):
        """Reset request counter (call periodically)"""
        self.requests_made = 0
        logger.info("🔄 API request counter reset")
