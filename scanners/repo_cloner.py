"""
GitHub Repository Management and Cloning - FIXED VERSION
"""

import os
import subprocess
import requests
from utils.logger import setup_logger
from config.api_config import get_github_token, get_delay
import time

logger = setup_logger(__name__)

class RepoCloner:
    def __init__(self):
        self.base_dir = "data/protocols/repos/"
        os.makedirs(self.base_dir, exist_ok=True)
        self.github_token = get_github_token()
    
    def clone_or_update_repo(self, protocol):
        """Clone or update a protocol repository - FIXED VERSION"""
        github_url = protocol.get('github')
        
        # FIX: Handle cases where github is a list or invalid format
        if isinstance(github_url, list):
            if github_url:
                github_url = github_url[0]  # Take first URL from list
            else:
                github_url = None
                
        if not github_url or not isinstance(github_url, str):
            logger.warning(f"❌ No valid GitHub URL for protocol: {protocol.get('name')}")
            return None
        
        repo_name = self._extract_repo_name(github_url)
        repo_path = os.path.join(self.base_dir, repo_name)
        
        if os.path.exists(repo_path):
            logger.info(f"🔄 Updating existing repo: {repo_name}")
            return self._update_repo(repo_path)
        else:
            logger.info(f"📥 Cloning new repo: {repo_name}")
            return self._clone_repo(github_url, repo_path)
    
    def _extract_repo_name(self, github_url):
        """Extract repository name from GitHub URL - FIXED VERSION"""
        if not isinstance(github_url, str):
            return "invalid_url"
            
        # Handle both https and git URLs
        if 'github.com/' in github_url:
            parts = github_url.split('github.com/')[-1]
            if parts.endswith('.git'):
                parts = parts[:-4]
            return parts.replace('/', '__')
        return github_url.replace('/', '__').replace(':', '_')
    
    def _clone_repo(self, url, path):
        """Clone a repository"""
        try:
            # Use token if available for higher rate limits
            if self.github_token and 'https://' in url:
                auth_url = url.replace('https://', f'https://{self.github_token}@')
            else:
                auth_url = url
            
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', auth_url, path],
                capture_output=True, text=True, timeout=300
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Successfully cloned: {path}")
                return path
            else:
                logger.error(f"❌ Failed to clone {url}: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"⏰ Clone timeout for: {url}")
            return None
        except Exception as e:
            logger.error(f"❌ Error cloning {url}: {e}")
            return None
    
    def _update_repo(self, path):
        """Update an existing repository"""
        try:
            result = subprocess.run(
                ['git', '-C', path, 'pull'],
                capture_output=True, text=True, timeout=180
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Successfully updated: {path}")
                return path
            else:
                logger.warning(f"⚠️ Update failed for {path}: {result.stderr}")
                return path  # Still return path even if update failed
                
        except subprocess.TimeoutExpired:
            logger.warning(f"⏰ Update timeout for: {path}")
            return path
        except Exception as e:
            logger.error(f"❌ Error updating {path}: {e}")
            return path
    
    def batch_clone_protocols(self, protocols):
        """Clone multiple protocols in batch with rate limiting"""
        cloned_protocols = []
        
        for i, protocol in enumerate(protocols):
            logger.info(f"📦 Processing {i+1}/{len(protocols)}: {protocol.get('name')}")
            
            repo_path = self.clone_or_update_repo(protocol)
            if repo_path:
                cloned_protocols.append((protocol, repo_path))
            
            # Respect rate limits - small delay between operations
            if i < len(protocols) - 1:  # Don't delay after last item
                time.sleep(1)
        
        logger.info(f"✅ Successfully processed {len(cloned_protocols)}/{len(protocols)} protocols")
        return cloned_protocols
