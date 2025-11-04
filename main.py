#!/usr/bin/env python3
"""
Seek-Pro-Research: Professional Uniswap V2 Fork Vulnerability Scanner
Main Application Entry Point
"""

import sys
import os
from scanners.fork_target_discoverer import ForkTargetDiscoverer
from scanners.repo_cloner import RepoCloner
from detectors.universal_v2_scanner import UniversalV2Scanner
from data.reports.report_generator import ReportGenerator
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SeekProResearch:
    def __init__(self):
        self.fork_discoverer = ForkTargetDiscoverer()
        self.repo_cloner = RepoCloner()
        self.v2_scanner = UniversalV2Scanner()
        self.report_generator = ReportGenerator()
    
    def scan_all_forks(self):
        """Scan all identified Uniswap V2 forks"""
        logger.info("🚀 SEEK-PRO-RESEARCH: UNISWAP V2 FORK SCAN")
        logger.info("===========================================")
        
        # Step 1: Get fork targets
        targets = self.fork_discoverer.get_fork_targets()
        logger.info(f"🎯 Targeting {len(targets)} Uniswap V2 forks")
        
        # Step 2: Clone repositories
        logger.info("📥 Phase 1: Repository Acquisition")
        protocols_with_repos = []
        
        for target in targets:
            # Convert target to protocol format
            protocol = {
                'name': target['name'],
                'github': target['github'],
                'type': target['type'],
                'risk_priority': target['risk_priority'],
                'tvl': 10000000,
                'audits': 2,
                'age_days': 365
            }
            
            repo_path = self.repo_cloner.clone_or_update_repo(protocol)
            if repo_path:
                protocols_with_repos.append((protocol, repo_path))
                logger.info(f"✅ Acquired: {target['name']}")
            else:
                logger.warning(f"⚠️ Failed to acquire: {target['name']}")
        
        # Step 3: Vulnerability scanning
        logger.info("�� Phase 2: Vulnerability Scanning")
        scan_results = self.v2_scanner.batch_scan_protocols(protocols_with_repos)
        
        # Step 4: Generate reports
        logger.info("📊 Phase 3: Analysis & Reporting")
        reports = self.report_generator.generate_comprehensive_reports(scan_results)
        
        # Step 5: Display results
        self._display_results(scan_results, reports)
        
        return scan_results
    
    def _display_results(self, scan_results, reports):
        """Display scan results in terminal"""
        print("\n" + "="*60)
        print("🎉 UNISWAP V2 FORK SCAN COMPLETED!")
        print("="*60)
        
        total_vulnerabilities = 0
        critical_count = 0
        
        for result in scan_results:
            protocol = result.get('protocol', {})
            vulnerabilities = result.get('vulnerabilities', [])
            risk_assessment = result.get('risk_assessment', {})
            
            vuln_count = len(vulnerabilities)
            critical_vulns = len([v for v in vulnerabilities if v['severity'] == 'CRITICAL'])
            
            total_vulnerabilities += vuln_count
            critical_count += critical_vulns
            
            print(f"\n📋 {protocol.get('name', 'Unknown')}:")
            print(f"   Risk Level: {risk_assessment.get('risk_level', 'UNKNOWN')}")
            print(f"   Vulnerabilities: {vuln_count} (Critical: {critical_vulns})")
            
            # Show critical vulnerabilities
            for vuln in vulnerabilities[:3]:
                if vuln['severity'] in ['CRITICAL', 'HIGH']:
                    print(f"   🚨 {vuln['severity']}: {vuln.get('file', 'Unknown')}:{vuln.get('line_number', '?')}")
        
        print("\n" + "="*60)
        print(f"📊 TOTAL FINDINGS:")
        print(f"   Protocols Scanned: {len(scan_results)}")
        print(f"   Total Vulnerabilities: {total_vulnerabilities}")
        print(f"   Critical Vulnerabilities: {critical_count}")
        print(f"   Reports Generated: {len(reports)}")
        print("="*60)
        
        if critical_count > 0:
            print("\n🚨 CRITICAL VULNERABILITIES DETECTED!")
            print("   Check the reports in data/reports/ for details")
        else:
            print("\n✅ No critical vulnerabilities found in scanned forks")

def main():
    scanner = SeekProResearch()
    
    try:
        print("🚀 SEEK-PRO-RESEARCH: UNISWAP V2 FORK VULNERABILITY SCANNER")
        print("Scanning established forks for critical security issues...")
        print("")
        
        results = scanner.scan_all_forks()
        
        print("\n🎯 SCAN COMPLETE!")
        print("Next: Review detailed reports in data/reports/")
        
    except KeyboardInterrupt:
        print("\n⏹️ Scan interrupted by user")
    except Exception as e:
        logger.error(f"❌ Scan failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
