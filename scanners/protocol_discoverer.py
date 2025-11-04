"""
DeFi Llama Protocol Discovery Engine - FIXED VERSION
"""

import requests
import json
from datetime import datetime, timedelta
from config.settings import DEFI_LLAMA_ENDPOINTS, RISK_THRESHOLDS

class ProtocolDiscoverer:
    def __init__(self):
        self.session = requests.Session()
    
    def get_all_protocols(self):
        """Get all protocols from DeFi Llama"""
        try:
            response = self.session.get(DEFI_LLAMA_ENDPOINTS['all_protocols'], timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error fetching protocols from DeFi Llama: {e}")
            return []
    
    def discover_high_risk_protocols(self):
        """Discover new high-risk protocols"""
        print("🔍 Discovering high-risk protocols from DeFi Llama...")
        
        all_protocols = self.get_all_protocols()
        high_risk_protocols = []
        
        for protocol in all_protocols:
            if self._is_high_risk_target(protocol):
                enhanced_protocol = self._enhance_protocol_data(protocol)
                high_risk_protocols.append(enhanced_protocol)
        
        print(f"✅ Found {len(high_risk_protocols)} high-risk protocols")
        return high_risk_protocols
    
    def _is_high_risk_target(self, protocol):
        """Check if protocol meets high-risk criteria - FIXED VERSION"""
        # Safely get listedAt with default
        listed_at = protocol.get('listedAt') or 0
        
        # Check age - handle missing or invalid dates
        if listed_at:
            try:
                listed_date = datetime.fromtimestamp(listed_at)
                age_days = (datetime.now() - listed_date).days
                if age_days > RISK_THRESHOLDS['max_age_days']:
                    return False
            except (ValueError, TypeError):
                # If date is invalid, treat as new protocol
                pass
        
        # Check audits - handle various formats safely
        audits = protocol.get('audits', 0)
        if isinstance(audits, str):
            audits = 0 if audits == '0' else 1
        audits = int(audits or 0)
        
        if audits > RISK_THRESHOLDS['max_audits']:
            return False
        
        # Check TVL - handle missing TVL
        tvl = protocol.get('tvl', 0) or 0
        tvl = float(tvl)
        
        if (tvl < RISK_THRESHOLDS['min_tvl'] or 
            tvl > RISK_THRESHOLDS['max_tvl']):
            return False
        
        # Check GitHub availability
        if RISK_THRESHOLDS['require_github'] and not protocol.get('github'):
            return False
        
        return True
    
    def _enhance_protocol_data(self, protocol):
        """Enhance protocol data with calculated fields - FIXED VERSION"""
        enhanced = protocol.copy()
        
        # Calculate age in days safely
        listed_at = protocol.get('listedAt') or 0
        if listed_at:
            try:
                listed_date = datetime.fromtimestamp(listed_at)
                enhanced['age_days'] = (datetime.now() - listed_date).days
            except (ValueError, TypeError):
                enhanced['age_days'] = 0  # Default to new if invalid date
        else:
            enhanced['age_days'] = 0
        
        # Normalize audits count safely
        audits = protocol.get('audits', 0)
        if isinstance(audits, str):
            enhanced['audits'] = 0 if audits == '0' else 1
        else:
            enhanced['audits'] = int(audits or 0)
        
        # Ensure TVL is a number
        enhanced['tvl'] = float(protocol.get('tvl', 0) or 0)
        
        # Add discovery timestamp
        enhanced['discovered_at'] = datetime.now().isoformat()
        
        return enhanced
