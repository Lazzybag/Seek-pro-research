"""
Protocol Database Management
"""

import json
import os
from datetime import datetime, timedelta
from config.settings import DATA_DIR, PROTOCOLS_DIR

class ProtocolManager:
    def __init__(self):
        self.protocols_file = os.path.join(PROTOCOLS_DIR, "protocols_database.json")
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(PROTOCOLS_DIR, exist_ok=True)
    
    def load_protocols(self):
        """Load protocols from database"""
        if os.path.exists(self.protocols_file):
            with open(self.protocols_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_protocols(self, protocols):
        """Save protocols to database"""
        with open(self.protocols_file, 'w') as f:
            json.dump(protocols, f, indent=2)
    
    def add_protocol(self, protocol_data):
        """Add a new protocol to database"""
        protocols = self.load_protocols()
        
        # Check if protocol already exists
        existing_ids = [p.get('id') for p in protocols]
        if protocol_data.get('id') not in existing_ids:
            protocol_data['first_seen'] = datetime.now().isoformat()
            protocol_data['last_updated'] = datetime.now().isoformat()
            protocols.append(protocol_data)
            self.save_protocols(protocols)
    
    def update_protocol(self, protocol_id, updates):
        """Update protocol information"""
        protocols = self.load_protocols()
        for protocol in protocols:
            if protocol.get('id') == protocol_id:
                protocol.update(updates)
                protocol['last_updated'] = datetime.now().isoformat()
                break
        self.save_protocols(protocols)
    
    def get_high_risk_protocols(self):
        """Get protocols meeting high-risk criteria"""
        protocols = self.load_protocols()
        high_risk = []
        
        for protocol in protocols:
            if self._is_high_risk(protocol):
                high_risk.append(protocol)
        
        return high_risk
    
    def _is_high_risk(self, protocol):
        """Determine if protocol is high risk"""
        from config.settings import RISK_THRESHOLDS
        
        # Check age
        if protocol.get('age_days', 999) > RISK_THRESHOLDS['max_age_days']:
            return False
        
        # Check audits
        if protocol.get('audits', 0) > RISK_THRESHOLDS['max_audits']:
            return False
        
        # Check TVL
        tvl = protocol.get('tvl', 0)
        if (tvl < RISK_THRESHOLDS['min_tvl'] or 
            tvl > RISK_THRESHOLDS['max_tvl']):
            return False
        
        # Check GitHub availability
        if RISK_THRESHOLDS['require_github'] and not protocol.get('github'):
            return False
        
        return True
