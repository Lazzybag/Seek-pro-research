"""
Main Universal V2 Vulnerability Scanner
"""

import os
from scanners.v2_detector import V2Detector
from detectors.pattern_matcher import PatternMatcher
from detectors.risk_assessor import RiskAssessor
from utils.logger import setup_logger

logger = setup_logger(__name__)

class UniversalV2Scanner:
    def __init__(self):
        self.v2_detector = V2Detector()
        self.pattern_matcher = PatternMatcher()
        self.risk_assessor = RiskAssessor()
    
    def scan_protocol(self, protocol, repo_path):
        """Complete vulnerability scan for a protocol"""
        logger.info(f"🔍 Starting comprehensive scan for: {protocol.get('name')}")
        
        scan_results = {
            'protocol': protocol,
            'v2_detection': None,
            'vulnerabilities': [],
            'risk_assessment': None,
            'scan_summary': {}
        }
        
        try:
            # Step 1: Detect V2 AMM usage
            scan_results['v2_detection'] = self.v2_detector.detect_v2_usage(repo_path)
            
            # Step 2: Only scan for vulnerabilities if V2 usage detected
            if scan_results['v2_detection']['confidence_score'] > 30:
                scan_results['vulnerabilities'] = self.pattern_matcher.scan_repository(repo_path)
            
            # Step 3: Risk assessment
            scan_results['risk_assessment'] = self.risk_assessor.assess_protocol_risk(
                protocol, 
                scan_results['vulnerabilities'],
                scan_results['v2_detection']
            )
            
            # Step 4: Generate summary
            scan_results['scan_summary'] = self._generate_summary(scan_results)
            
            logger.info(f"✅ Scan completed for {protocol.get('name')}")
            
        except Exception as e:
            logger.error(f"❌ Scan failed for {protocol.get('name')}: {e}")
            scan_results['error'] = str(e)
        
        return scan_results
    
    def _generate_summary(self, scan_results):
        """Generate scan summary"""
        vulnerabilities = scan_results['vulnerabilities']
        v2_detection = scan_results['v2_detection']
        
        critical_count = len([v for v in vulnerabilities if v['severity'] == 'CRITICAL'])
        high_count = len([v for v in vulnerabilities if v['severity'] == 'HIGH'])
        medium_count = len([v for v in vulnerabilities if v['severity'] == 'MEDIUM'])
        
        return {
            'total_vulnerabilities': len(vulnerabilities),
            'critical_vulnerabilities': critical_count,
            'high_vulnerabilities': high_count,
            'medium_vulnerabilities': medium_count,
            'v2_confidence': v2_detection.get('confidence_score', 0),
            'amm_type': v2_detection.get('amm_type', 'UNKNOWN'),
            'v2_files_found': len(v2_detection.get('v2_files', [])),
            'scan_timestamp': scan_results['risk_assessment'].get('scan_timestamp') if scan_results['risk_assessment'] else None
        }
    
    def batch_scan_protocols(self, protocols_with_repos):
        """Scan multiple protocols in batch"""
        results = []
        
        for protocol, repo_path in protocols_with_repos:
            if repo_path and os.path.exists(repo_path):
                result = self.scan_protocol(protocol, repo_path)
                results.append(result)
            else:
                logger.warning(f"⚠️ Skipping {protocol.get('name')} - no valid repository")
        
        # Sort by risk score (highest first)
        results.sort(key=lambda x: x.get('risk_assessment', {}).get('overall_score', 0), reverse=True)
        
        return results
