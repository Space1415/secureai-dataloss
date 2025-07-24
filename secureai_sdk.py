#!/usr/bin/env python3
"""
SecureAI SDK - Simple and Easy-to-Use PII Protection
A developer-friendly SDK for protecting sensitive data in AI applications.
"""

import os
import sys
import uuid
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProtectionLevel(Enum):
    """Protection levels for different use cases."""
    BASIC = "basic"
    STANDARD = "standard"
    ENTERPRISE = "enterprise"

class EntityType(Enum):
    """Types of entities that can be detected."""
    PERSON = "person"
    EMAIL = "email"
    PHONE = "phone"
    SSN = "ssn"
    CREDIT_CARD = "credit_card"
    API_KEY = "api_key"
    DATABASE_URL = "database_url"
    IP_ADDRESS = "ip_address"
    ADDRESS = "address"
    DATE = "date"

@dataclass
class Entity:
    """Represents a detected entity."""
    original_value: str
    masked_value: str
    entity_type: str
    confidence: float
    start_position: int
    end_position: int

@dataclass
class ProtectionResult:
    """Result of a protection operation."""
    original_text: str
    protected_text: str
    entities: List[Entity]
    confidence_score: float
    processing_time_ms: float
    session_id: str
    protection_level: str

class SecureAI:
    """
    SecureAI SDK - Simple and powerful PII protection.
    
    Usage:
        from secureai_sdk import SecureAI
        
        # Initialize
        secureai = SecureAI()
        
        # Protect text
        result = secureai.protect("Hi, I'm John Smith. My email is john@example.com")
        print(result.protected_text)
    """
    
    def __init__(self, 
                 api_key: str = None,
                 protection_level: ProtectionLevel = ProtectionLevel.STANDARD,
                 enable_persistence: bool = True):
        """
        Initialize SecureAI SDK.
        
        Args:
            api_key: Optional API key for advanced features
            protection_level: Level of protection to apply
            enable_persistence: Enable entity persistence across sessions
        """
        self.api_key = api_key or os.getenv("SECUREAI_API_KEY")
        self.protection_level = protection_level
        self.enable_persistence = enable_persistence
        
        # Storage for entity mappings and sessions
        self.entity_mappings = {}
        self.sessions = {}
        
        # Try to initialize advanced detection
        self.advanced_available = self._initialize_advanced()
        
        if self.advanced_available:
            logger.info("SecureAI advanced detection initialized")
        else:
            logger.info("Using enhanced basic detection")
    
    def _initialize_advanced(self) -> bool:
        """Try to initialize advanced SecureAI components."""
        try:
            # Add src directory to path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            src_path = os.path.join(current_dir, 'src')
            if os.path.exists(src_path):
                sys.path.insert(0, src_path)
            
            # Try to import advanced components
            from secure_AI.ai_privacy_shield import AIPrivacyShield
            
            self.shield = AIPrivacyShield(
                tinfoil_api_key=self.api_key,
                enable_persistence=self.enable_persistence
            )
            return True
            
        except ImportError:
            return False
        except Exception as e:
            logger.warning(f"Advanced detection not available: {e}")
            return False
    
    def protect(self, 
                text: str, 
                session_id: str = None,
                user_id: str = None) -> ProtectionResult:
        """
        Protect text by detecting and redacting PII.
        
        Args:
            text: Text to protect
            session_id: Session identifier for entity persistence
            user_id: User identifier
            
        Returns:
            ProtectionResult with protected text and entity information
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        start_time = datetime.now()
        
        if self.advanced_available:
            result = self._protect_advanced(text, session_id, user_id)
        else:
            result = self._protect_basic(text, session_id)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Store session data
        self.sessions[session_id] = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "text_length": len(text),
            "entities_count": len(result.entities)
        }
        
        return ProtectionResult(
            original_text=text,
            protected_text=result.protected_text,
            entities=result.entities,
            confidence_score=result.confidence_score,
            processing_time_ms=processing_time,
            session_id=session_id,
            protection_level=self.protection_level.value
        )
    
    def _protect_advanced(self, text: str, session_id: str, user_id: str) -> ProtectionResult:
        """Use advanced SecureAI detection."""
        try:
            result = self.shield.redact_content(
                content=text,
                content_type="text",
                session_id=session_id,
                user_id=user_id
            )
            
            entities = [
                Entity(
                    original_value=mapping.original_value,
                    masked_value=mapping.masked_value,
                    entity_type=mapping.entity_type.value,
                    confidence=mapping.confidence_score,
                    start_position=0,  # Advanced detection doesn't provide positions
                    end_position=0
                )
                for mapping in result.entity_mappings
            ]
            
            return ProtectionResult(
                original_text=text,
                protected_text=result.redacted_content,
                entities=entities,
                confidence_score=result.confidence_score,
                processing_time_ms=0,
                session_id=session_id,
                protection_level="advanced"
            )
            
        except Exception as e:
            logger.error(f"Advanced protection failed: {e}")
            return self._protect_basic(text, session_id)
    
    def _protect_basic(self, text: str, session_id: str) -> ProtectionResult:
        """Enhanced basic detection using regex patterns."""
        import re
        
        entities = []
        protected_text = text
        entity_count = 0
        
        # Enhanced patterns for comprehensive detection
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
            (r'AIza[0-9A-Za-z-_]{35}', 'api_key'),  # Google API keys
            # Database URLs
            (r'[a-zA-Z]+://[^/\s]+:[^/\s]+@[^/\s]+', 'database_url'),
            # IP addresses
            (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 'ip_address'),
            # Names (enhanced pattern)
            (r'\b[A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b', 'person'),
            # Addresses (basic pattern)
            (r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b', 'address'),
            # Dates (various formats)
            (r'\b\d{1,2}/\d{1,2}/\d{4}\b', 'date'),
            (r'\b\d{4}-\d{2}-\d{2}\b', 'date'),
        ]
        
        for pattern, entity_type in patterns:
            for match in re.finditer(pattern, text):
                original_value = match.group()
                
                # Check for existing mapping
                mapping_key = f"{session_id}:{original_value}"
                if self.enable_persistence and mapping_key in self.entity_mappings:
                    masked_value = self.entity_mappings[mapping_key]
                else:
                    # Create new mapping
                    entity_count += 1
                    masked_value = f"[{entity_type.upper()}_{entity_count}]"
                    if self.enable_persistence:
                        self.entity_mappings[mapping_key] = masked_value
                
                entities.append(Entity(
                    original_value=original_value,
                    masked_value=masked_value,
                    entity_type=entity_type,
                    confidence=0.85,
                    start_position=match.start(),
                    end_position=match.end()
                ))
                
                # Replace in text
                protected_text = protected_text.replace(original_value, masked_value)
        
        return ProtectionResult(
            original_text=text,
            protected_text=protected_text,
            entities=entities,
            confidence_score=0.85,
            processing_time_ms=0,
            session_id=session_id,
            protection_level="basic_enhanced"
        )
    
    def get_session_entities(self, session_id: str) -> List[Entity]:
        """Get entities for a specific session."""
        entities = []
        for key, value in self.entity_mappings.items():
            if key.startswith(f"{session_id}:"):
                original_value = key.split(":", 1)[1]
                entity_type = value.strip("[]").split("_")[0].lower()
                entities.append(Entity(
                    original_value=original_value,
                    masked_value=value,
                    entity_type=entity_type,
                    confidence=0.85,
                    start_position=0,
                    end_position=0
                ))
        return entities
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics about protection usage."""
        total_sessions = len(self.sessions)
        total_entities = len(self.entity_mappings)
        
        # Calculate entity type breakdown
        entity_types = {}
        for key, value in self.entity_mappings.items():
            entity_type = value.strip("[]").split("_")[0].lower()
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
        
        return {
            "total_sessions": total_sessions,
            "total_entities_protected": total_entities,
            "average_entities_per_session": total_entities / total_sessions if total_sessions > 0 else 0,
            "entity_type_breakdown": entity_types,
            "advanced_detection_available": self.advanced_available,
            "protection_level": self.protection_level.value,
            "persistence_enabled": self.enable_persistence
        }
    
    def export_session_data(self, session_id: str, format: str = "json") -> str:
        """Export session data for compliance."""
        session_data = {
            "session_id": session_id,
            "timestamp": self.sessions.get(session_id, {}).get("timestamp"),
            "user_id": self.sessions.get(session_id, {}).get("user_id"),
            "entities": [
                {
                    "original": entity.original_value,
                    "masked": entity.masked_value,
                    "type": entity.entity_type,
                    "confidence": entity.confidence
                }
                for entity in self.get_session_entities(session_id)
            ]
        }
        
        if format.lower() == "json":
            return json.dumps(session_data, indent=2)
        else:
            return str(session_data)

# Convenience functions for quick usage
def protect_text(text: str, api_key: str = None) -> str:
    """
    Quick function to protect text.
    
    Args:
        text: Text to protect
        api_key: Optional API key
        
    Returns:
        Protected text
    """
    secureai = SecureAI(api_key=api_key)
    result = secureai.protect(text)
    return result.protected_text

def protect_batch(texts: List[str], api_key: str = None) -> List[str]:
    """
    Protect multiple texts in batch.
    
    Args:
        texts: List of texts to protect
        api_key: Optional API key
        
    Returns:
        List of protected texts
    """
    secureai = SecureAI(api_key=api_key)
    results = []
    
    for text in texts:
        result = secureai.protect(text)
        results.append(result.protected_text)
    
    return results

# Example usage and demonstration
def demonstrate_sdk():
    """Demonstrate the SecureAI SDK functionality."""
    print("SecureAI SDK - Easy PII Protection")
    print("=" * 50)
    
    # Initialize SDK
    secureai = SecureAI(protection_level=ProtectionLevel.STANDARD)
    
    # Test cases
    test_cases = [
        "Hi, I'm John Smith. My email is john.smith@company.com",
        "Call me at 555-123-4567 or email sarah@example.com",
        "My SSN is 123-45-6789 and credit card is 1234-5678-9012-3456",
        "API key: sk-1234567890abcdef and database: postgresql://user:pass@host/db"
    ]
    
    print("Testing PII Detection and Redaction:")
    print("-" * 40)
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Original: {test_text}")
        
        result = secureai.protect(test_text)
        
        print(f"Protected: {result.protected_text}")
        print(f"Entities: {len(result.entities)} detected")
        print(f"Confidence: {result.confidence_score:.1f}%")
        print(f"Processing time: {result.processing_time_ms:.2f}ms")
        
        if result.entities:
            print("Detected entities:")
            for entity in result.entities:
                print(f"  • {entity.original_value} → {entity.masked_value} ({entity.entity_type})")
    
    # Test entity persistence
    print(f"\nTesting Entity Persistence:")
    print("-" * 40)
    
    # Same person in different messages
    text1 = "Hi, I'm John Smith from Acme Corp."
    text2 = "John Smith's email is john@acme.com"
    
    result1 = secureai.protect(text1, session_id="test_session")
    result2 = secureai.protect(text2, session_id="test_session")
    
    print(f"Message 1: {result1.protected_text}")
    print(f"Message 2: {result2.protected_text}")
    print("Notice how 'John Smith' gets the same alias in both messages")
    
    # Get analytics
    print(f"\nAnalytics:")
    print("-" * 40)
    
    analytics = secureai.get_analytics()
    print(f"Total Sessions: {analytics['total_sessions']}")
    print(f"Total Entities Protected: {analytics['total_entities_protected']}")
    print(f"Entity Types: {analytics['entity_type_breakdown']}")
    print(f"Advanced Detection: {analytics['advanced_detection_available']}")
    
    # Quick function examples
    print(f"\nQuick Function Examples:")
    print("-" * 40)
    
    # Quick protect
    protected = protect_text("My email is test@example.com")
    print(f"Quick protect: {protected}")
    
    # Batch protect
    texts = ["Email: user1@test.com", "Phone: 555-111-2222"]
    protected_batch_result = protect_batch(texts)
    print(f"Batch protect: {protected_batch_result}")

if __name__ == "__main__":
    demonstrate_sdk() 