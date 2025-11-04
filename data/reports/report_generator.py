"""
Professional Report Generation System
"""

import os
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.reports_dir = "data/reports/"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create reports directory"""
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_comprehensive_reports(self, scan_results):
        """Generate comprehensive reports from scan results"""
        print("📊 Generating scan reports...")
        reports_generated = []
        
        # Generate overall summary report
        summary_report = self._generate_summary_report(scan_results)
        if summary_report:
            reports_generated.append(summary_report)
        
        # Generate individual protocol reports for critical/high risk
        for result in scan_results:
            risk_level = result.get('risk_assessment', {}).get('risk_level')
            if risk_level in ['CRITICAL', 'HIGH']:
                protocol_report = self._generate_protocol_report(result)
                if protocol_report:
                    reports_generated.append(protocol_report)
        
        print(f"📄 Generated {len(reports_generated)} reports in {self.reports_dir}")
        return reports_generated
    
    def _generate_summary_report(self, scan_results):
        """Generate overall summary report"""
        timestamp = datetime.now()
        
        # Calculate statistics
        total_protocols = len(scan_results)
        critical_count = len([r for r in scan_results if r.get('risk_assessment', {}).get('risk_level') == 'CRITICAL'])
        total_vulnerabilities = sum(len(r.get('vulnerabilities', [])) for r in scan_results)
        
        summary_data = {
            'report_type': 'SCAN_SUMMARY',
            'timestamp': timestamp.isoformat(),
            'scan_statistics': {
                'total_protocols_scanned': total_protocols,
                'critical_risk_protocols': critical_count,
                'total_vulnerabilities_found': total_vulnerabilities,
                'scan_duration_estimate': 'Completed successfully'
            },
            'recommendations': [
                "Review critical vulnerabilities in protocol reports",
                "Check individual protocol details for specific issues"
            ]
        }
        
        filename = f"scan_summary_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.reports_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(summary_data, f, indent=2)
            return {'type': 'summary', 'filepath': filepath}
        except Exception as e:
            print(f"❌ Failed to save summary report: {e}")
            return None
    
    def _generate_protocol_report(self, scan_result):
        """Generate detailed report for a single protocol"""
        protocol = scan_result.get('protocol', {})
        vulnerabilities = scan_result.get('vulnerabilities', [])
        risk_assessment = scan_result.get('risk_assessment', {})
        
        report_data = {
            'report_type': 'PROTOCOL_DETAILED',
            'timestamp': datetime.now().isoformat(),
            'protocol_info': {
                'name': protocol.get('name', 'Unknown'),
                'github': protocol.get('github', ''),
                'risk_level': risk_assessment.get('risk_level', 'UNKNOWN')
            },
            'vulnerabilities': vulnerabilities,
            'security_recommendations': [
                "Review all critical vulnerabilities",
                "Consider security audit for production deployment"
            ]
        }
        
        protocol_name_clean = protocol.get('name', 'unknown').replace(' ', '_').lower()
        filename = f"protocol_{protocol_name_clean}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.reports_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report_data, f, indent=2)
            return {'type': 'protocol', 'filepath': filepath, 'protocol': protocol.get('name')}
        except Exception as e:
            print(f"❌ Failed to save protocol report: {e}")
            return None
