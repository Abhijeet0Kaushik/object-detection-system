"""
Alert system for object detection
Supports email and console notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


class AlertSystem:
    def __init__(self, alert_config=None):
        """
        Initialize alert system
        
        Args:
            alert_config: Dictionary with alert settings
                {
                    'enabled': True/False,
                    'method': 'email' or 'console',
                    'triggers': ['person', 'car'],  # Objects to trigger alerts
                    'email_config': {
                        'smtp_server': 'smtp.gmail.com',
                        'smtp_port': 587,
                        'sender_email': 'your_email@gmail.com',
                        'sender_password': 'your_password',
                        'recipient_email': 'recipient@example.com'
                    }
                }
        """
        self.config = alert_config or {'enabled': False}
        self.last_alert_time = {}
        self.cooldown_seconds = 10  # Prevent alert spam
    
    def check_and_alert(self, detections):
        """
        Check detections and send alerts if needed
        
        Args:
            detections: List of detection dictionaries
        """
        if not self.config.get('enabled', False):
            return
        
        triggers = self.config.get('triggers', [])
        
        for detection in detections:
            obj_class = detection['class']
            
            if obj_class in triggers:
                # Check cooldown
                current_time = datetime.now()
                last_time = self.last_alert_time.get(obj_class)
                
                if last_time:
                    time_diff = (current_time - last_time).total_seconds()
                    if time_diff < self.cooldown_seconds:
                        continue
                
                # Send alert
                self._send_alert(detection)
                self.last_alert_time[obj_class] = current_time
    
    def _send_alert(self, detection):
        """Send alert based on configured method"""
        method = self.config.get('method', 'console')
        
        if method == 'console':
            self._console_alert(detection)
        elif method == 'email':
            self._email_alert(detection)
    
    def _console_alert(self, detection):
        """Print alert to console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        obj_class = detection['class']
        confidence = detection['confidence']
        
        print(f"\n{'='*50}")
        print(f"⚠️  ALERT: {obj_class.upper()} DETECTED")
        print(f"Time: {timestamp}")
        print(f"Confidence: {confidence:.2%}")
        print(f"{'='*50}\n")
    
    def _email_alert(self, detection):
        """Send email alert"""
        email_config = self.config.get('email_config', {})
        
        if not email_config:
            print("Email config not provided, falling back to console alert")
            self._console_alert(detection)
            return
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = email_config['recipient_email']
            msg['Subject'] = f"Object Detection Alert: {detection['class']}"
            
            # Email body
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            body = f"""
Object Detection Alert

Object Detected: {detection['class']}
Confidence: {detection['confidence']:.2%}
Time: {timestamp}

This is an automated alert from your object detection system.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['sender_email'], email_config['sender_password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✉️  Email alert sent for {detection['class']}")
            
        except Exception as e:
            print(f"Failed to send email alert: {e}")
            print("Falling back to console alert")
            self._console_alert(detection)


class AlertConfigHelper:
    """Helper class to create alert configurations"""
    
    @staticmethod
    def console_alerts(trigger_objects):
        """Create console-based alert config"""
        return {
            'enabled': True,
            'method': 'console',
            'triggers': trigger_objects
        }
    
    @staticmethod
    def email_alerts(trigger_objects, smtp_server, smtp_port, sender_email, 
                     sender_password, recipient_email):
        """Create email-based alert config"""
        return {
            'enabled': True,
            'method': 'email',
            'triggers': trigger_objects,
            'email_config': {
                'smtp_server': smtp_server,
                'smtp_port': smtp_port,
                'sender_email': sender_email,
                'sender_password': sender_password,
                'recipient_email': recipient_email
            }
        }
    
    @staticmethod
    def no_alerts():
        """Create config with alerts disabled"""
        return {'enabled': False}
