#!/usr/bin/env python3
"""
License Manager for SecureAI SDK
Handles dual licensing: MIT (free) + Commercial (paid)
"""

import os
import json
import hashlib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

class LicenseType(Enum):
    """License types for different usage scenarios."""
    MIT = "mit"  # Free, open source
    COMMERCIAL = "commercial"  # Paid, enterprise
    TRIAL = "trial"  # 30-day trial
    EDUCATIONAL = "educational"  # Free for education

class FeatureTier(Enum):
    """Feature tiers based on license type."""
    BASIC = "basic"  # MIT license features
    STANDARD = "standard"  # Commercial basic
    ENTERPRISE = "enterprise"  # Commercial advanced
    CUSTOM = "custom"  # Custom enterprise

class LicenseManager:
    """
    Manages licensing for SecureAI SDK.
    Provides dual licensing: MIT (free) + Commercial (paid).
    """
    
    def __init__(self, license_key: str = None):
        """
        Initialize license manager.
        
        Args:
            license_key: Optional commercial license key
        """
        self.license_key = license_key or os.getenv("SECUREAI_LICENSE_KEY")
        self.license_info = None
        self.features = self._get_mit_features()  # Default to MIT features
        
        if self.license_key:
            self._validate_commercial_license()
    
    def _get_mit_features(self) -> Dict[str, bool]:
        """Get features available under MIT license (free)."""
        return {
            "basic_pii_detection": True,
            "entity_persistence": True,
            "basic_analytics": True,
            "session_management": True,
            "export_json": True,
            "up_to_1000_requests_per_day": True,
            "community_support": True,
            # Commercial features (False for MIT)
            "advanced_detection": False,
            "custom_entities": False,
            "api_gateway": False,
            "compliance_reports": False,
            "priority_support": False,
            "unlimited_requests": False,
            "white_label": False,
            "enterprise_integration": False
        }
    
    def _get_commercial_features(self, tier: FeatureTier) -> Dict[str, bool]:
        """Get features available under commercial license."""
        base_features = self._get_mit_features()
        
        if tier == FeatureTier.STANDARD:
            base_features.update({
                "advanced_detection": True,
                "custom_entities": True,
                "unlimited_requests": True,
                "priority_support": True
            })
        elif tier == FeatureTier.ENTERPRISE:
            base_features.update({
                "advanced_detection": True,
                "custom_entities": True,
                "api_gateway": True,
                "compliance_reports": True,
                "priority_support": True,
                "unlimited_requests": True,
                "white_label": True,
                "enterprise_integration": True
            })
        
        return base_features
    
    def _validate_commercial_license(self):
        """Validate commercial license key."""
        try:
            # In production, this would validate against your license server
            # For demo purposes, we'll simulate validation
            if self.license_key and self.license_key.startswith("SECUREAI_"):
                self.license_info = {
                    "type": LicenseType.COMMERCIAL,
                    "tier": FeatureTier.ENTERPRISE,
                    "expires": datetime.now() + timedelta(days=365),
                    "company": "Demo Company",
                    "features": self._get_commercial_features(FeatureTier.ENTERPRISE)
                }
                self.features = self.license_info["features"]
            else:
                print("Warning: Invalid commercial license key. Using MIT features.")
                self.features = self._get_mit_features()
                
        except Exception as e:
            print(f"License validation failed: {e}. Using MIT features.")
            self.features = self._get_mit_features()
    
    def has_feature(self, feature_name: str) -> bool:
        """Check if a feature is available with current license."""
        return self.features.get(feature_name, False)
    
    def get_license_info(self) -> Dict:
        """Get current license information."""
        if self.license_info:
            return self.license_info
        else:
            return {
                "type": LicenseType.MIT,
                "tier": FeatureTier.BASIC,
                "expires": None,
                "company": "Open Source",
                "features": self.features
            }
    
    def check_usage_limits(self, current_usage: int) -> bool:
        """Check if current usage is within license limits."""
        if self.has_feature("unlimited_requests"):
            return True
        
        # MIT license: 1000 requests per day
        daily_limit = 1000
        return current_usage < daily_limit
    
    def get_pricing_info(self) -> Dict:
        """Get pricing information for different tiers."""
        return {
            "mit": {
                "price": "Free",
                "features": list(self._get_mit_features().keys()),
                "limits": "1000 requests/day",
                "support": "Community"
            },
            "standard": {
                "price": "$99/month",
                "features": ["advanced_detection", "custom_entities", "unlimited_requests"],
                "limits": "Unlimited",
                "support": "Priority"
            },
            "enterprise": {
                "price": "$499/month",
                "features": ["api_gateway", "compliance_reports", "white_label"],
                "limits": "Unlimited",
                "support": "24/7"
            }
        }

# Enhanced SecureAI with licensing
class SecureAICommercial(SecureAI):
    """
    Enhanced SecureAI with commercial licensing support.
    """
    
    def __init__(self, 
                 license_key: str = None,
                 protection_level: ProtectionLevel = ProtectionLevel.STANDARD,
                 enable_persistence: bool = True):
        """
        Initialize SecureAI with license management.
        """
        super().__init__(protection_level, enable_persistence)
        self.license_manager = LicenseManager(license_key)
        
        # Check license and set features
        self._setup_licensed_features()
    
    def _setup_licensed_features(self):
        """Setup features based on license."""
        if self.license_manager.has_feature("advanced_detection"):
            # Enable advanced detection features
            self.advanced_patterns = self._get_advanced_patterns()
            self.custom_entities = self._get_custom_entities()
        
        if self.license_manager.has_feature("api_gateway"):
            # Enable API gateway features
            self.api_gateway_enabled = True
    
    def protect(self, text: str, session_id: str = None, user_id: str = None) -> ProtectionResult:
        """Protect text with license checking."""
        # Check usage limits
        if not self.license_manager.check_usage_limits(self._get_current_usage()):
            raise Exception("Usage limit exceeded. Please upgrade to commercial license.")
        
        # Use enhanced features if available
        if self.license_manager.has_feature("advanced_detection"):
            return self._protect_advanced(text, session_id, user_id)
        else:
            return self._protect_basic(text, session_id)
    
    def _get_advanced_patterns(self) -> List:
        """Get advanced detection patterns (commercial feature)."""
        return [
            # Advanced patterns for commercial users
            (r'\b[A-Z]{2}\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\b', 'passport'),  # Passport numbers
            (r'\b\d{1,2}\s[A-Za-z]+\s\d{4}\b', 'date_uk'),  # UK dates
            (r'\b[A-Z]{3}\d{6}\b', 'drivers_license'),  # Driver's license
            # Add more advanced patterns
        ]
    
    def _get_custom_entities(self) -> Dict:
        """Get custom entity definitions (commercial feature)."""
        return {
            "project_code": r"PROJ-\d{4}",
            "ticket_number": r"TKT-\d{6}",
            "internal_id": r"INT-\d{8}"
        }
    
    def _get_current_usage(self) -> int:
        """Get current usage count (simplified)."""
        return len(self.sessions)  # In production, this would track actual usage
    
    def get_license_status(self) -> Dict:
        """Get current license status and features."""
        return {
            "license_info": self.license_manager.get_license_info(),
            "available_features": [k for k, v in self.license_manager.features.items() if v],
            "pricing": self.license_manager.get_pricing_info()
        }

# Example usage
def demonstrate_licensing():
    """Demonstrate the licensing system."""
    print("SecureAI Licensing Demonstration")
    print("=" * 50)
    
    # MIT License (Free)
    print("\n1. MIT License (Free):")
    mit_secureai = SecureAICommercial()
    mit_status = mit_secureai.get_license_status()
    print(f"License Type: {mit_status['license_info']['type'].value}")
    print(f"Features: {len(mit_status['available_features'])} available")
    print(f"Pricing: {mit_status['pricing']['mit']['price']}")
    
    # Commercial License (Paid)
    print("\n2. Commercial License (Paid):")
    commercial_secureai = SecureAICommercial(license_key="SECUREAI_DEMO_KEY")
    commercial_status = commercial_secureai.get_license_status()
    print(f"License Type: {commercial_status['license_info']['type'].value}")
    print(f"Features: {len(commercial_status['available_features'])} available")
    print(f"Pricing: {commercial_status['pricing']['enterprise']['price']}")
    
    # Test protection
    test_text = "Hi, I'm John Smith. My email is john@example.com"
    
    print(f"\n3. Protection Test:")
    print(f"Original: {test_text}")
    
    mit_result = mit_secureai.protect(test_text)
    print(f"MIT Result: {mit_result.protected_text}")
    
    commercial_result = commercial_secureai.protect(test_text)
    print(f"Commercial Result: {commercial_result.protected_text}")

if __name__ == "__main__":
    demonstrate_licensing() 