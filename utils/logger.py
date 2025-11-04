"""
Professional Logging System
"""

import logging
import sys
from datetime import datetime
import os

def setup_logger(name, log_level=logging.INFO):
    """Setup professional logger with formatting"""
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(levelname)-8s %(message)s'
    )
    
    # File handler (detailed)
    log_file = os.path.join(log_dir, f"security_scan_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler (clean)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Custom log levels for better visibility
def log_protocol_discovery(logger, protocol_name, risk_level):
    logger.info(f"🎯 PROTOCOL DISCOVERED: {protocol_name} | Risk: {risk_level}")

def log_vulnerability_found(logger, protocol_name, severity, count):
    emoji = "🚨" if severity == "CRITICAL" else "⚠️" if severity == "HIGH" else "🔍"
    logger.warning(f"{emoji} VULNERABILITY: {protocol_name} | {severity}: {count} found")

def log_scan_complete(logger, total_protocols, vulnerabilities_found):
    logger.info(f"✅ SCAN COMPLETE: {total_protocols} protocols | {vulnerabilities_found} vulnerabilities")
