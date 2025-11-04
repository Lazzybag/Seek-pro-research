"""
Universal V2 Vulnerability Pattern Matching
"""

import re
import os
from config.settings import V2_AMM_PATTERNS

class PatternMatcher:
    def __init__(self):
        self.patterns = self._compile_vulnerability_patterns()
    
    def _compile_vulnerability_patterns(self):
        """Compile regex patterns for vulnerability detection"""
        return {
            'CRITICAL': [
                # Direct getReserves() usage without validation
                re.compile(r'getReserves\s*\(\s*\)[^}]*?=[^}]*?reserve', re.IGNORECASE),
                # getReserves in view functions without TWAP
                re.compile(r'function.*view.*getReserves', re.IGNORECASE),
            ],
            'HIGH': [
                # Manual token0/token1 division
                re.compile(r'token0\s*\(\s*\)[^/]*/[^}]*token1\s*\(\s*\)', re.IGNORECASE),
                # Direct reserve division
                re.compile(r'reserve0\s*/\s*reserve1', re.IGNORECASE),
            ],
            'MEDIUM': [
                # Raw balanceOf usage on pool addresses
                re.compile(r'balanceOf\s*\(\s*0x[a-fA-F0-9]{40}\s*\)', re.IGNORECASE),
                # Direct pool interactions without checks
                re.compile(r'IUniswapV2Pair.*balanceOf', re.IGNORECASE),
            ]
        }
    
    def scan_file_for_vulnerabilities(self, file_path):
        """Scan a single file for vulnerability patterns"""
        vulnerabilities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            for severity, patterns in self.patterns.items():
                for pattern in patterns:
                    matches = pattern.finditer(content)
                    for match in matches:
                        # Find line number
                        line_number = self._find_line_number(content, match.start())
                        line_content = lines[line_number].strip() if line_number < len(lines) else ""
                        
                        vulnerability = {
                            'file': file_path,
                            'line_number': line_number + 1,  # 1-based for humans
                            'severity': severity,
                            'pattern': pattern.pattern,
                            'matched_text': match.group()[:100],  # First 100 chars
                            'line_content': line_content
                        }
                        vulnerabilities.append(vulnerability)
        
        except Exception as e:
            print(f"⚠️ Error scanning file {file_path}: {e}")
        
        return vulnerabilities
    
    def _find_line_number(self, content, position):
        """Find line number for a character position"""
        return content[:position].count('\n')
    
    def scan_repository(self, repo_path):
        """Scan entire repository for vulnerabilities"""
        print(f"🔍 Scanning repository for vulnerabilities: {repo_path}")
        
        all_vulnerabilities = []
        solidity_files = self._find_solidity_files(repo_path)
        
        for file_path in solidity_files:
            file_vulnerabilities = self.scan_file_for_vulnerabilities(file_path)
            all_vulnerabilities.extend(file_vulnerabilities)
        
        # Sort by severity
        severity_order = {'CRITICAL': 3, 'HIGH': 2, 'MEDIUM': 1}
        all_vulnerabilities.sort(key=lambda x: severity_order.get(x['severity'], 0), reverse=True)
        
        return all_vulnerabilities
    
    def _find_solidity_files(self, repo_path):
        """Find all Solidity files in repository"""
        solidity_files = []
        
        for root, dirs, files in os.walk(repo_path):
            # Skip node_modules and other common non-source directories
            if 'node_modules' in root or 'test' in root.lower():
                continue
                
            for file in files:
                if file.endswith('.sol'):
                    solidity_files.append(os.path.join(root, file))
        
        return solidity_files
