#!/usr/bin/env python3
"""
Simple Integration Script for Existing Website
Replace your current PII detection with SecureAI's superior detection.
"""

import os
import sys
import uuid
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleSecureAIIntegration:
    """
    Simple integration class to replace your existing PII detection.
    Drop-in replacement that works with your current system.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the integration.
        
        Args:
            api_key: Optional API key for advanced features
        """
        self.api_key = api_key or os.getenv("TINFOIL_API_KEY")
        self.entity_mappings = {}  # Simple in-memory storage
        self.sessions = {}
        
        # Try to initialize SecureAI, fallback to basic detection
        self.secureai_available = self._initialize_secureai()
        
        if self.secureai_available:
            logger.info("✅ SecureAI integration initialized successfully")
        else:
            logger.warning("⚠️  SecureAI not available, using enhanced basic detection")
    
    def _initialize_secureai(self) -> bool:
        """Try to initialize SecureAI components."""
        try:
            # Add the src directory to path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            src_path = os.path.join(current_dir, 'src')
            if os.path.exists(src_path):
                sys.path.insert(0, src_path)
            
            # Try to import SecureAI
            from secure_AI.ai_privacy_shield import AIPrivacyShield
            
            self.shield = AIPrivacyShield(
                tinfoil_api_key=self.api_key,
                enable_persistence=True
            )
            return True
            
        except ImportError as e:
            logger.error(f"SecureAI import failed: {e}")
            return False
        except Exception as e:
            logger.error(f"SecureAI initialization failed: {e}")
            return False
    
    def detect_and_redact(self, 
                         text: str, 
                         session_id: str = None,
                         user_id: str = None) -> Dict[str, Any]:
        """
        Detect and redact PII from text.
        
        Args:
            text: Input text to process
            session_id: Session identifier for entity persistence
            user_id: User identifier
            
        Returns:
            Dictionary with redacted text and entity information
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        start_time = datetime.now()
        
        if self.secureai_available:
            # Use SecureAI for superior detection
            result = self._detect_with_secureai(text, session_id, user_id)
        else:
            # Use enhanced basic detection as fallback
            result = self._detect_with_basic(text, session_id)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        result["processing_time_ms"] = processing_time
        result["session_id"] = session_id
        result["user_id"] = user_id
        
        # Store session data
        self.sessions[session_id] = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "entities": result["entities"],
            "text_length": len(text)
        }
        
        return result
    
    def _detect_with_secureai(self, text: str, session_id: str, user_id: str) -> Dict[str, Any]:
        """Use SecureAI for detection."""
        try:
            result = self.shield.redact_content(
                content=text,
                content_type="text",
                session_id=session_id,
                user_id=user_id
            )
            
            return {
                "redacted_text": result.redacted_content,
                "entities": [
                    {
                        "original": mapping.original_value,
                        "masked": mapping.masked_value,
                        "type": mapping.entity_type.value,
                        "confidence": mapping.confidence_score
                    }
                    for mapping in result.entity_mappings
                ],
                "confidence_score": result.confidence_score,
                "model_used": result.model_used,
                "detection_method": "secureai"
            }
            
        except Exception as e:
            logger.error(f"SecureAI detection failed: {e}")
            # Fallback to basic detection
            return self._detect_with_basic(text, session_id)
    
    def _detect_with_basic(self, text: str, session_id: str) -> Dict[str, Any]:
        """Enhanced basic detection using regex patterns."""
        import re
        
        entities = []
        redacted_text = text
        entity_count = 0
        
        # Enhanced patterns for better detection
        patterns = [
            # Email addresses
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'email'),
            # Phone numbers (various formats)
            (r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', 'phone'),
            (r'\b\(\d{3}\)\s?\d{3}[-.\s]?\d{4}\b', 'phone'),
            # Social Security Numbers
            (r'\b\d{3}-\d{2}-\d{4}\b', 'ssn'),
            # Credit card numbers
            (r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', 'credit_card'),
            # API keys
            (r'sk-[a-zA-Z0-9]{32,}', 'api_key'),
            (r'pk_[a-zA-Z0-9]{32,}', 'api_key'),
            # Database URLs
            (r'[a-zA-Z]+://[^/\s]+:[^/\s]+@[^/\s]+', 'database_url'),
            # IP addresses
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 'ip_address'),
            # Names (simple pattern)
            (r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', 'person_name'),
            # Addresses (basic pattern)
            (r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b', 'address'),
        ]
        
        for pattern, entity_type in patterns:
            for match in re.finditer(pattern, text):
                original_value = match.group()
                
                # Check if we already have a mapping for this entity
                mapping_key = f"{session_id}:{original_value}"
                if mapping_key in self.entity_mappings:
                    masked_value = self.entity_mappings[mapping_key]
                else:
                    # Create new mapping
                    entity_count += 1
                    masked_value = f"[{entity_type.upper()}_{entity_count}]"
                    self.entity_mappings[mapping_key] = masked_value
                
                entities.append({
                    "original": original_value,
                    "masked": masked_value,
                    "type": entity_type,
                    "confidence": 0.85
                })
                
                # Replace in text
                redacted_text = redacted_text.replace(original_value, masked_value)
        
        return {
            "redacted_text": redacted_text,
            "entities": entities,
            "confidence_score": 0.85,
            "model_used": "enhanced_regex",
            "detection_method": "basic_enhanced"
        }
    
    def get_session_entities(self, session_id: str) -> List[Dict[str, Any]]:
        """Get entities for a specific session."""
        entities = []
        for key, value in self.entity_mappings.items():
            if key.startswith(f"{session_id}:"):
                original_value = key.split(":", 1)[1]
                entity_type = value.strip("[]").split("_")[0].lower()
                entities.append({
                    "original": original_value,
                    "masked": value,
                    "type": entity_type
                })
        return entities
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics about the integration."""
        total_sessions = len(self.sessions)
        total_entities = len(self.entity_mappings)
        
        # Calculate average entities per session
        avg_entities = total_entities / total_sessions if total_sessions > 0 else 0
        
        return {
            "total_sessions": total_sessions,
            "total_entities_protected": total_entities,
            "average_entities_per_session": avg_entities,
            "secureai_available": self.secureai_available,
            "detection_method": "secureai" if self.secureai_available else "basic_enhanced"
        }

# Example usage for your existing website
def integrate_with_your_website():
    """
    Example of how to integrate this with your existing website.
    Replace your current PII detection with this.
    """
    
    # Initialize the integration
    secureai = SimpleSecureAIIntegration()
    
    # Example: Your existing website processing
    def process_user_input(user_text: str, user_id: str = None):
        """
        Replace your existing PII detection with this function.
        """
        # Detect and redact PII
        result = secureai.detect_and_redact(
            text=user_text,
            user_id=user_id
        )
        
        # Your existing ChatGPT/Claude API calls
        redacted_text = result["redacted_text"]
        
        # Example: Call your AI APIs
        ai_response = call_your_ai_apis(redacted_text)
        
        return {
            "original_text": user_text,
            "redacted_text": redacted_text,
            "ai_response": ai_response,
            "entities_detected": result["entities"],
            "session_id": result["session_id"],
            "confidence_score": result["confidence_score"],
            "detection_method": result["detection_method"]
        }
    
    def call_your_ai_apis(text: str) -> str:
        """
        Your existing ChatGPT/Claude API calls.
        Replace this with your actual implementation.
        """
        # Example implementation
        return f"AI processed: {text}"
    
    # Test the integration
    test_text = "Hi, I'm John Smith. My email is john.smith@company.com and my phone is 555-123-4567."
    
    print("🔄 Testing Integration with Your Website")
    print("=" * 50)
    
    result = process_user_input(test_text, user_id="user_123")
    
    print(f"Original Text: {result['original_text']}")
    print(f"Redacted Text: {result['redacted_text']}")
    print(f"AI Response: {result['ai_response']}")
    print(f"Entities Detected: {len(result['entities_detected'])}")
    print(f"Confidence Score: {result['confidence_score']:.1f}%")
    print(f"Detection Method: {result['detection_method']}")
    print(f"Session ID: {result['session_id']}")
    
    print("\n🔍 Detected Entities:")
    for entity in result['entities_detected']:
        print(f"  • {entity['original']} → {entity['masked']} ({entity['type']})")
    
    # Get analytics
    analytics = secureai.get_analytics()
    print(f"\n📊 Analytics:")
    print(f"  • Total Sessions: {analytics['total_sessions']}")
    print(f"  • Total Entities Protected: {analytics['total_entities_protected']}")
    print(f"  • SecureAI Available: {analytics['secureai_available']}")
    print(f"  • Detection Method: {analytics['detection_method']}")

# Quick test function
def quick_test():
    """Quick test to verify the integration works."""
    print("🧪 Quick Integration Test")
    print("=" * 30)
    
    secureai = SimpleSecureAIIntegration()
    
    test_cases = [
        "My email is john@example.com",
        "Call me at 555-123-4567",
        "My SSN is 123-45-6789",
        "API key: sk-1234567890abcdef"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_text}")
        result = secureai.detect_and_redact(test_text)
        print(f"Result: {result['redacted_text']}")
        print(f"Entities: {len(result['entities'])} detected")

if __name__ == "__main__":
    # Run quick test
    quick_test()
    
    print("\n" + "=" * 50)
    
    # Run full integration example
    integrate_with_your_website() 