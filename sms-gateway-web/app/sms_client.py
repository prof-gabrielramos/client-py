"""
SMS Gateway client with proper error handling and security
"""
import requests
import logging
from flask import current_app
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class SMSGatewayClient:
    """Secure SMS Gateway client"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url or current_app.config.get('GATEWAY_URL')
        self.api_key = api_key or current_app.config.get('GATEWAY_API_KEY')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set headers
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
        
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'SMS-Gateway-Web/1.0'
        })
    
    def send_sms(self, phone_numbers: List[str], message: str, 
                 with_delivery_report: bool = True, sim_number: Optional[int] = None,
                 ttl: Optional[int] = None) -> Dict[str, Any]:
        """Send SMS with proper error handling"""
        try:
            payload = {
                'message': message,
                'phoneNumbers': phone_numbers,
                'withDeliveryReport': with_delivery_report
            }
            
            if sim_number is not None:
                payload['simNumber'] = sim_number
            
            if ttl is not None:
                payload['ttl'] = ttl
            
            response = self.session.post(
                f"{self.base_url}/message",
                json=payload,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"SMS sent successfully to {len(phone_numbers)} recipients")
            return result
            
        except requests.exceptions.Timeout:
            logger.error("SMS gateway timeout")
            raise Exception("Gateway timeout - please try again")
        
        except requests.exceptions.ConnectionError:
            logger.error("SMS gateway connection error")
            raise Exception("Cannot connect to SMS gateway")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"SMS gateway HTTP error: {e}")
            if e.response.status_code == 401:
                raise Exception("Invalid API credentials")
            elif e.response.status_code == 429:
                raise Exception("Rate limit exceeded")
            else:
                raise Exception(f"Gateway error: {e.response.status_code}")
        
        except Exception as e:
            logger.error(f"Unexpected error sending SMS: {e}")
            raise Exception("Failed to send SMS")
    
    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """Get message status"""
        try:
            response = self.session.get(
                f"{self.base_url}/message/{message_id}",
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error getting message status: {e}")
            raise Exception("Failed to get message status")
    
    def test_connection(self) -> bool:
        """Test connection to SMS gateway"""
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def __del__(self):
        """Cleanup session"""
        if hasattr(self, 'session'):
            self.session.close()