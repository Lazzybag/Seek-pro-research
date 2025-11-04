"""
Professional Security Research Platform - Main Settings
"""

# DeFi Llama API Configuration
DEFI_LLAMA_ENDPOINTS = {
    'all_protocols': 'https://api.llama.fi/protocols',
    'protocol_details': 'https://api.llama.fi/protocol/{}',
    'recently_added': 'https://api.llama.fi/updatedProtocols'
}

# Risk Assessment Settings
RISK_THRESHOLDS = {
    'max_age_days': 90,           # Target protocols < 3 months old
    'max_audits': 1,              # 0-1 audits maximum
    'min_tvl': 1000,              # At least $1K TVL
    'max_tvl': 10000000,          # Maximum $10M TVL
    'require_github': True        # Must have source code
}

# Universal V2 AMM Patterns
V2_AMM_PATTERNS = {
    'interfaces': [
        'IUniswapV2Pair', 'IPancakePair', 'IJoePair', 'ISushiSwapPair',
        'IQuickSwapPair', 'ISpookySwapPair', 'IPangolinPair'
    ],
    'vulnerabilities': [
        'getReserves()',
        'token0()',
        'token1()',
        'balanceOf(0x'
    ]
}

# File Paths
DATA_DIR = "data/"
PROTOCOLS_DIR = "data/protocols/"
VULNERABILITIES_DIR = "data/vulnerabilities/"
REPORTS_DIR = "data/reports/"

# Scan Settings
MAX_PROTOCOLS_PER_DAY = 50
SCAN_INTERVAL_HOURS = 24
