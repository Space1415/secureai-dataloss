#!/usr/bin/env python3
"""
Website Integration Example
Simple example showing how to integrate SecureAI into your existing website.
"""

from secureai_sdk import SecureAI, protect_text
import json

class YourWebsiteIntegration:
    """
    Example integration for your existing website.
    Replace your current PII detection with this.
    """
    
    def __init__(self):
        # Initialize SecureAI SDK
        self.secureai = SecureAI()
        print("SecureAI SDK initialized successfully")
    
    def process_user_input(self, user_text: str, user_id: str = None):
        """
        Process user input with SecureAI protection.
        Replace your existing PII detection with this function.
        """
        # Protect the user's text
        result = self.secureai.protect(
            text=user_text,
            user_id=user_id
        )
        
        # Your existing ChatGPT/Claude API calls would go here
        # For this example, we'll simulate an AI response
        ai_response = self.simulate_ai_response(result.protected_text)
        
        # Protect the AI response too
        protected_ai_response = self.secureai.protect(
            text=ai_response,
            user_id=user_id
        )
        
        return {
            "original_user_text": user_text,
            "protected_user_text": result.protected_text,
            "ai_response": ai_response,
            "protected_ai_response": protected_ai_response.protected_text,
            "entities_detected": len(result.entities),
            "confidence_score": result.confidence_score,
            "session_id": result.session_id,
            "processing_time_ms": result.processing_time_ms
        }
    
    def simulate_ai_response(self, protected_text: str):
        """Simulate your existing AI API call."""
        # Replace this with your actual ChatGPT/Claude API call
        return f"AI processed: {protected_text}"
    
    def get_session_entities(self, session_id: str):
        """Get entities for a specific session."""
        return self.secureai.get_session_entities(session_id)
    
    def get_analytics(self):
        """Get analytics about protection usage."""
        return self.secureai.get_analytics()

def demonstrate_integration():
    """Demonstrate the integration with your website."""
    print("SecureAI Website Integration Demo")
    print("=" * 50)
    
    # Initialize integration
    website = YourWebsiteIntegration()
    
    # Test cases that might come from your website
    test_cases = [
        {
            "text": "Hi, I'm John Smith from Acme Corporation. My email is john.smith@acme.com",
            "user_id": "user_123"
        },
        {
            "text": "My phone number is 555-123-4567 and I need help with my account",
            "user_id": "user_123"
        },
        {
            "text": "Can you help me with my SSN 123-45-6789 and credit card 1234-5678-9012-3456?",
            "user_id": "user_456"
        }
    ]
    
    print("Processing User Inputs:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"User ID: {test_case['user_id']}")
        print(f"Original: {test_case['text']}")
        
        # Process with your integration
        result = website.process_user_input(
            test_case['text'], 
            test_case['user_id']
        )
        
        print(f"Protected: {result['protected_user_text']}")
        print(f"AI Response: {result['protected_ai_response']}")
        print(f"Entities: {result['entities_detected']} detected")
        print(f"Confidence: {result['confidence_score']:.1f}%")
        print(f"Processing time: {result['processing_time_ms']:.2f}ms")
        print(f"Session ID: {result['session_id']}")
    
    # Test entity persistence across sessions
    print(f"\nTesting Entity Persistence:")
    print("-" * 40)
    
    # Same user, different messages
    user_id = "user_123"
    
    message1 = "Hi, I'm John Smith from Acme Corp."
    message2 = "John Smith's email is john@acme.com"
    
    result1 = website.process_user_input(message1, user_id)
    result2 = website.process_user_input(message2, user_id)
    
    print(f"Message 1: {result1['protected_user_text']}")
    print(f"Message 2: {result2['protected_user_text']}")
    print("Notice how 'John Smith' gets the same alias in both messages")
    
    # Get analytics
    print(f"\nAnalytics:")
    print("-" * 40)
    
    analytics = website.get_analytics()
    print(f"Total Sessions: {analytics['total_sessions']}")
    print(f"Total Entities Protected: {analytics['total_entities_protected']}")
    print(f"Entity Types: {analytics['entity_type_breakdown']}")
    print(f"Advanced Detection: {analytics['advanced_detection_available']}")
    
    # Export session data for compliance
    print(f"\nCompliance Export:")
    print("-" * 40)
    
    session_id = result1['session_id']
    export_data = website.secureai.export_session_data(session_id, format="json")
    print("Session data exported for compliance:")
    print(export_data)

def quick_integration_example():
    """Show the simplest possible integration."""
    print("\nQuick Integration Example")
    print("=" * 40)
    
    # The simplest way to integrate - just one line!
    original_text = "Hi, I'm John Smith. My email is john@example.com"
    
    # Replace your existing PII detection with this:
    protected_text = protect_text(original_text)
    
    print(f"Original: {original_text}")
    print(f"Protected: {protected_text}")
    print("That's it! Just one line of code.")

def flask_integration_example():
    """Example Flask integration."""
    print("\nFlask Integration Example")
    print("=" * 40)
    
    flask_code = '''
from flask import Flask, request, jsonify
from secureai_sdk import SecureAI

app = Flask(__name__)
secureai = SecureAI()

@app.route('/protect', methods=['POST'])
def protect_text():
    data = request.json
    text = data.get('text')
    user_id = data.get('user_id')
    
    result = secureai.protect(text, user_id=user_id)
    
    return jsonify({
        'protected_text': result.protected_text,
        'entities_detected': len(result.entities),
        'confidence_score': result.confidence_score,
        'session_id': result.session_id
    })

if __name__ == '__main__':
    app.run(debug=True)
'''
    
    print("Add this to your Flask app:")
    print(flask_code)

def django_integration_example():
    """Example Django integration."""
    print("\nDjango Integration Example")
    print("=" * 40)
    
    django_code = '''
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from secureai_sdk import SecureAI

secureai = SecureAI()

@csrf_exempt
@require_http_methods(["POST"])
def protect_text(request):
    data = json.loads(request.body)
    text = data.get('text')
    user_id = data.get('user_id')
    
    result = secureai.protect(text, user_id=user_id)
    
    return JsonResponse({
        'protected_text': result.protected_text,
        'entities_detected': len(result.entities),
        'confidence_score': result.confidence_score,
        'session_id': result.session_id
    })
'''
    
    print("Add this to your Django views:")
    print(django_code)

if __name__ == "__main__":
    # Run the main demonstration
    demonstrate_integration()
    
    # Show quick integration
    quick_integration_example()
    
    # Show framework examples
    flask_integration_example()
    django_integration_example()
    
    print("\n" + "=" * 50)
    print("Integration Complete!")
    print("Your website now has superior PII protection!")
    print("=" * 50) 