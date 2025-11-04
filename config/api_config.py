"""
API Configuration and Rate Limiting
"""

import os
import time

# GitHub API Configuration
GITHUB_CONFIG = {
    'base_url': 'https://api.github.com',
    'search_endpoint': '/search/code',
    'repo_endpoint': '/repos/{}',
    'rate_limit_endpoint': '/rate_limit'
}

# Rate Limiting Settings
RATE_LIMITS = {
    'github_requests_per_hour': 4500,  # Leave buffer from 5000 limit
    'delay_between_requests': 2,       # Seconds between API calls
    'batch_size': 30,                  # Protocols per batch
    'cooldown_period': 3600            # 1 hour cooldown if near limit
}

def get_github_token():
    """Get GitHub token from environment with fallback"""
    return os.getenv('GITHUB_TOKEN', '')

def should_pause(requests_made):
    """Check if we need to pause due to rate limits"""
    return requests_made >= RATE_LIMITS['github_requests_per_hour']

def get_delay():
    """Get delay between requests"""
    return RATE_LIMITS['delay_between_requests']
