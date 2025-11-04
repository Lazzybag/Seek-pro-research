"""
Uniswap V2 Fork Detection Engine
"""

import os
import re
from config.settings import V2_AMM_PATTERNS

class V2Detector:
    def __init__(self):
        self.patterns = V2_AMM_PATTERNS
    
    def detect_v2_usage(self, repo_path):
        """Detect if repository uses any Uniswap V2 fork"""
        print(f"🔍 Scanning for V2 AMM usage in: {repo_path}")
        
        v2_indicators = {
            'amm_type': None,
            'interfaces_found': [],
            'v2_files': [],
            'confidence_score': 0
        }
        
        solidity_files = self._find_solidity_files(repo_path)
        
        for file_path in solidity_files:
            file_indicators = self._analyze_file(file_path)
            if file_indicators['is_v2_related']:
                v2_indicators['v2_files'].append(file_path)
                v2_indicators['interfaces_found'].extend(file_indicators['interfaces'])
        
        # Determine AMM type and confidence
        v2_indicators['amm_type'] = self._determine_amm_type(v2_indicators['interfaces_found'])
        v2_indicators['confidence_score'] = self._calculate_confidence(v2_indicators)
        
        return v2_indicators
    
    def _find_solidity_files(self, repo_path):
        """Find all Solidity files in repository"""
        solidity_files = []
        
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.sol'):
                    solidity_files.append(os.path.join(root, file))
        
        return solidity_files
    
    def _analyze_file(self, file_path):
        """Analyze a single Solidity file for V2 indicators"""
        indicators = {
            'is_v2_related': False,
            'interfaces': [],
            'vulnerability_patterns': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for V2 interfaces
            for interface in self.patterns['interfaces']:
                if interface in content:
                    indicators['interfaces'].append(interface)
                    indicators['is_v2_related'] = True
            
            # Check for vulnerability patterns
            for pattern in self.patterns['vulnerabilities']:
                if pattern in content:
                    indicators['vulnerability_patterns'].append(pattern)
            
        except Exception as e:
            print(f"⚠️ Error analyzing file {file_path}: {e}")
        
        return indicators
    
    def _determine_amm_type(self, interfaces_found):
        """Determine which specific AMM fork is being used"""
        if not interfaces_found:
            return "UNKNOWN"
        
        interface_mapping = {
            'IUniswapV2Pair': 'Uniswap V2',
            'IPancakePair': 'PancakeSwap',
            'IJoePair': 'Trader Joe',
            'ISushiSwapPair': 'SushiSwap',
            'IQuickSwapPair': 'QuickSwap',
            'ISpookySwapPair': 'SpookySwap',
            'IPangolinPair': 'Pangolin'
        }
        
        for interface in interfaces_found:
            if interface in interface_mapping:
                return interface_mapping[interface]
        
        return "Generic V2 Fork"
    
    def _calculate_confidence(self, indicators):
        """Calculate confidence score for V2 detection"""
        confidence = 0
        
        # Interface presence
        if indicators['interfaces_found']:
            confidence += 40
        
        # Number of V2-related files
        file_count = len(indicators['v2_files'])
        if file_count >= 3:
            confidence += 30
        elif file_count >= 1:
            confidence += 15
        
        # Specific AMM type identified
        if indicators['amm_type'] != "UNKNOWN":
            confidence += 30
        
        return min(confidence, 100)
