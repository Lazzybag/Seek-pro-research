"""
File and Data Processing Utilities
"""

import os
import json
import csv
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)

class FileProcessor:
    def __init__(self):
        self.supported_formats = ['.json', '.csv', '.yaml', '.yml']
    
    def save_json(self, data, file_path, indent=2):
        """Save data as JSON file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
            logger.debug(f"💾 JSON saved: {file_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to save JSON {file_path}: {e}")
            return False
    
    def load_json(self, file_path):
        """Load data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Failed to load JSON {file_path}: {e}")
            return None
    
    def save_csv(self, data, file_path, fieldnames=None):
        """Save data as CSV file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            if not data:
                logger.warning("⚠️ No data to save as CSV")
                return False
            
            if not fieldnames and data:
                fieldnames = data[0].keys()
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            logger.debug(f"💾 CSV saved: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save CSV {file_path}: {e}")
            return False
    
    def generate_report_filename(self, base_name, extension='json'):
        """Generate timestamped report filename"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{base_name}_{timestamp}.{extension}"
    
    def find_files_by_extension(self, directory, extension):
        """Find all files with specific extension"""
        matching_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extension):
                    matching_files.append(os.path.join(root, file))
        
        return matching_files
    
    def count_solidity_files(self, directory):
        """Count Solidity files in directory"""
        return len(self.find_files_by_extension(directory, '.sol'))
    
    def get_file_size(self, file_path):
        """Get file size in human-readable format"""
        try:
            size_bytes = os.path.getsize(file_path)
            
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.2f} {unit}"
                size_bytes /= 1024.0
            
            return f"{size_bytes:.2f} TB"
        except Exception as e:
            logger.error(f"❌ Failed to get file size {file_path}: {e}")
            return "Unknown"
    
    def clean_old_reports(self, directory, days_old=30):
        """Clean reports older than specified days"""
        try:
            cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            deleted_count = 0
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_time = os.path.getmtime(file_path)
                    
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        deleted_count += 1
            
            logger.info(f"🧹 Cleaned {deleted_count} old reports from {directory}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"❌ Failed to clean old reports: {e}")
            return 0
