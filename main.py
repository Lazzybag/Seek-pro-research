#!/usr/bin/env python3
"""
Seek-Pro-Research: Professional Uniswap V2 Fork Vulnerability Scanner
ENHANCED VERSION with Focused Terminal Analysis
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanners.fork_target_discoverer import ForkTargetDiscoverer
from scanners.repo_cloner import RepoCloner
from detectors.universal_v2_scanner import UniversalV2Scanner
from utils.logger import setup_logger

logger = setup_logger(__name__)

class FocusedVulnerabilityAnalyzer:
    """Focused analysis showing detailed vulnerability info in terminal"""
    
    def analyze_vulnerability(self, vulnerability, file_content=None):
        analysis = vulnerability.copy()
        
        # Determine specific vulnerability type
        vuln_type = self._classify_vulnerability(vulnerability, file_content)
        analysis['vulnerability_type'] = vuln_type
        analysis.update(self._get_vulnerability_details(vuln_type))
        analysis['affected_pools'] = self._extract_pool_info(vulnerability.get('file', ''), file_content)
        
        return analysis
    
    def _classify_vulnerability(self, vulnerability, file_content):
        pattern = vulnerability.get('pattern', '')
        matched_text = vulnerability.get('matched_text', '')
        line_content = vulnerability.get('line_content', '')
        
        if 'getReserves()' in pattern:
            if 'view' in line_content or 'returns' in line_content:
                return 'direct_reserves_oracle'
            else:
                return 'reserves_manipulation'
        elif 'token0()' in pattern and 'token1()' in pattern and '/' in matched_text:
            return 'token_division_oracle'
        elif 'balanceOf' in pattern and '0x' in matched_text:
            return 'balance_manipulation'
        
        return 'amm_price_manipulation'
    
    def _get_vulnerability_details(self, vuln_type):
        details_map = {
            'direct_reserves_oracle': {
                'name': 'Direct Reserves Price Oracle',
                'type': 'CRITICAL - Oracle Manipulation',
                'exploit_scenario': 'Flash loan to manipulate pool reserves and exploit price-dependent functions',
                'affected_contracts': ['Price Oracles', 'Lending Protocols', 'Yield Farms'],
                'impact': 'HIGH - Fund theft through price manipulation'
            },
            'reserves_manipulation': {
                'name': 'Reserves-Based Price Calculation', 
                'type': 'CRITICAL - Economic Attack',
                'exploit_scenario': 'Large swaps to manipulate spot prices for arbitrage or collateral exploitation',
                'affected_contracts': ['AMM Pairs', 'Router Contracts', 'Price Feeds'],
                'impact': 'HIGH - Economic exploitation'
            },
            'token_division_oracle': {
                'name': 'Manual Token Price Calculation',
                'type': 'CRITICAL - Price Oracle',
                'exploit_scenario': 'Manipulate token ratios to create false pricing for DeFi operations',
                'affected_contracts': ['Custom Oracles', 'Price Calculators', 'Swap Functions'],
                'impact': 'HIGH - Direct price manipulation'
            },
            'balance_manipulation': {
                'name': 'Raw Balance Manipulation',
                'type': 'HIGH - Economic Attack', 
                'exploit_scenario': 'Temporarily inflate pool balances to manipulate derived values',
                'affected_contracts': ['Liquidity Pools', 'Balance Checks', 'Value Calculations'],
                'impact': 'MEDIUM-HIGH - Economic attacks'
            },
            'amm_price_manipulation': {
                'name': 'AMM Price Manipulation',
                'type': 'CRITICAL - DeFi Exploit', 
                'exploit_scenario': 'Standard AMM price manipulation through large swaps',
                'affected_contracts': ['AMM Contracts', 'Price Feeds'],
                'impact': 'HIGH - Economic loss'
            }
        }
        
        return details_map.get(vuln_type, {
            'name': 'AMM Vulnerability',
            'type': 'CRITICAL - Security Issue',
            'exploit_scenario': 'Price manipulation through pool reserves',
            'affected_contracts': ['Unknown contracts'],
            'impact': 'Requires investigation'
        })
    
    def _extract_pool_info(self, file_path, file_content):
        pools = []
        if file_content:
            pool_patterns = [
                r'(\w+)[Pp]air\s*=\s*[^;]+',
                r'IPancakePair|IUniswapV2Pair|IJoePair',
                r'pairFor\([^)]+\)',
                r'getPair\([^)]+\)'
            ]
            for pattern in pool_patterns:
                matches = re.finditer(pattern, file_content)
                for match in matches:
                    pool_name = match.group(1) if match.groups() else 'AMM_Pair'
                    pools.append(f"{pool_name}Pair")
        return list(set(pools)) if pools else ['Primary AMM Pool']

class SeekProResearchEnhanced:
    def __init__(self):
        self.fork_discoverer = ForkTargetDiscoverer()
        self.repo_cloner = RepoCloner()
        self.v2_scanner = UniversalV2Scanner()
        self.vuln_analyzer = FocusedVulnerabilityAnalyzer()
    
    def scan_all_forks(self):
        print("🚀 SEEK-PRO-RESEARCH: ENHANCED VULNERABILITY ANALYSIS")
        print("=" * 60)
        
        targets = self.fork_discoverer.get_fork_targets()
        print(f"🎯 Scanning {len(targets)} Uniswap V2 forks...")
        
        protocols_with_repos = []
        for target in targets:
            protocol = {
                'name': target['name'],
                'github': target['github'],
                'type': target['type'],
                'risk_priority': target['risk_priority']
            }
            repo_path = self.repo_cloner.clone_or_update_repo(protocol)
            if repo_path:
                protocols_with_repos.append((protocol, repo_path))
        
        scan_results = self.v2_scanner.batch_scan_protocols(protocols_with_repos)
        self._display_enhanced_analysis(scan_results)
        return scan_results
    
    def _display_enhanced_analysis(self, scan_results):
        print("\n" + "=" * 80)
        print("🎯 ENHANCED VULNERABILITY ANALYSIS RESULTS")
        print("=" * 80)
        
        for result in scan_results:
            protocol = result.get('protocol', {})
            vulnerabilities = result.get('vulnerabilities', [])
            
            if not vulnerabilities:
                continue
                
            print(f"\n🔴 PROTOCOL: {protocol.get('name', 'Unknown')}")
            print("-" * 50)
            
            critical_vulns = [v for v in vulnerabilities if v.get('severity') in ['CRITICAL', 'HIGH']]
            
            for i, vuln in enumerate(critical_vulns[:10]):
                try:
                    with open(vuln.get('file', ''), 'r') as f:
                        file_content = f.read()
                    enhanced_vuln = self.vuln_analyzer.analyze_vulnerability(vuln, file_content)
                except:
                    enhanced_vuln = self.vuln_analyzer.analyze_vulnerability(vuln)
                
                print(f"\n💀 VULNERABILITY #{i+1}:")
                print(f"   📍 File: {vuln.get('file', 'Unknown')}:{vuln.get('line_number', '?')}")
                print(f"   🏷️  Name: {enhanced_vuln.get('name', 'Unknown')}")
                print(f"   🔧 Type: {enhanced_vuln.get('type', 'Unknown')}")
                print(f"   ⚠️  Impact: {enhanced_vuln.get('impact', 'Unknown')}")
                print(f"   🎯 Exploit: {enhanced_vuln.get('exploit_scenario', 'Unknown')}")
                print(f"   �� Contracts: {', '.join(enhanced_vuln.get('affected_contracts', []))}")
                print(f"   �� Pools: {', '.join(enhanced_vuln.get('affected_pools', []))}")
                
                line_content = vuln.get('line_content', '')
                if line_content and len(line_content) < 100:
                    print(f"   📝 Code: {line_content.strip()}")
                
                print("   " + "-" * 40)

def main():
    scanner = SeekProResearchEnhanced()
    try:
        scanner.scan_all_forks()
        print("\n✅ ENHANCED ANALYSIS COMPLETE!")
    except Exception as e:
        logger.error(f"❌ Scan failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
