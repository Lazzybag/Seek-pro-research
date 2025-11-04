"""
Risk Assessment and Scoring Engine
"""

class RiskAssessor:
    def __init__(self):
        self.severity_weights = {
            'CRITICAL': 10,
            'HIGH': 6,
            'MEDIUM': 3,
            'LOW': 1
        }
    
    def assess_protocol_risk(self, protocol, vulnerabilities, v2_indicators):
        """Assess overall risk for a protocol"""
        risk_score = 0
        risk_factors = []
        
        # 1. Vulnerability-based risk
        vuln_risk = self._calculate_vulnerability_risk(vulnerabilities)
        risk_score += vuln_risk['score']
        risk_factors.extend(vuln_risk['factors'])
        
        # 2. Protocol maturity risk
        maturity_risk = self._assess_maturity_risk(protocol)
        risk_score += maturity_risk['score']
        risk_factors.extend(maturity_risk['factors'])
        
        # 3. AMM usage risk
        amm_risk = self._assess_amm_risk(v2_indicators)
        risk_score += amm_risk['score']
        risk_factors.extend(amm_risk['factors'])
        
        # 4. Economic risk
        economic_risk = self._assess_economic_risk(protocol)
        risk_score += economic_risk['score']
        risk_factors.extend(economic_risk['factors'])
        
        # Normalize score to 0-100
        risk_score = min(risk_score, 100)
        
        return {
            'overall_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'factors': risk_factors,
            'vulnerability_count': len(vulnerabilities),
            'critical_vulnerabilities': len([v for v in vulnerabilities if v['severity'] == 'CRITICAL'])
        }
    
    def _calculate_vulnerability_risk(self, vulnerabilities):
        """Calculate risk based on vulnerabilities"""
        score = 0
        factors = []
        
        critical_count = len([v for v in vulnerabilities if v['severity'] == 'CRITICAL'])
        high_count = len([v for v in vulnerabilities if v['severity'] == 'HIGH'])
        medium_count = len([v for v in vulnerabilities if v['severity'] == 'MEDIUM'])
        
        if critical_count > 0:
            score += critical_count * self.severity_weights['CRITICAL'] * 2
            factors.append(f"{critical_count} CRITICAL vulnerabilities found")
        
        if high_count > 0:
            score += high_count * self.severity_weights['HIGH'] * 1.5
            factors.append(f"{high_count} HIGH vulnerabilities found")
        
        if medium_count > 0:
            score += medium_count * self.severity_weights['MEDIUM']
            factors.append(f"{medium_count} MEDIUM vulnerabilities found")
        
        return {'score': score, 'factors': factors}
    
    def _assess_maturity_risk(self, protocol):
        """Assess risk based on protocol maturity"""
        score = 0
        factors = []
        
        # Age risk
        age_days = protocol.get('age_days', 0)
        if age_days < 30:
            score += 15
            factors.append("Protocol is very new (< 30 days)")
        elif age_days < 90:
            score += 8
            factors.append("Protocol is relatively new (< 90 days)")
        
        # Audit risk
        audits = protocol.get('audits', 0)
        if audits == 0:
            score += 12
            factors.append("No security audits conducted")
        elif audits == 1:
            score += 6
            factors.append("Only 1 security audit conducted")
        
        return {'score': score, 'factors': factors}
    
    def _assess_amm_risk(self, v2_indicators):
        """Assess risk based on AMM usage"""
        score = 0
        factors = []
        
        if v2_indicators.get('confidence_score', 0) > 50:
            score += 10
            factors.append("Uses V2 AMM for critical operations")
        
        if v2_indicators.get('amm_type') != "UNKNOWN":
            score += 5
            factors.append(f"Uses {v2_indicators['amm_type']} specifically")
        
        return {'score': score, 'factors': factors}
    
    def _assess_economic_risk(self, protocol):
        """Assess risk based on economic factors"""
        score = 0
        factors = []
        
        tvl = protocol.get('tvl', 0)
        if tvl > 1000000:  # $1M+ TVL
            score += 15
            factors.append("High TVL - significant user funds at risk")
        elif tvl > 100000:  # $100K+ TVL
            score += 8
            factors.append("Moderate TVL - user funds at risk")
        
        return {'score': score, 'factors': factors}
    
    def _get_risk_level(self, score):
        """Convert numerical score to risk level"""
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        elif score >= 20:
            return "LOW"
        else:
            return "MINIMAL"
