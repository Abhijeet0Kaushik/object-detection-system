"""
Configuration Template
Copy this to config.py and customize for your needs
"""

# ============================================================================
# DETECTOR CONFIGURATION
# ============================================================================

DETECTOR_CONFIG = {
    # Model selection
    # Options: 'yolov8n.pt' (fastest), 'yolov8s.pt', 'yolov8m.pt' (most accurate)
    'model_path': 'yolov8n.pt',
    
    # Confidence threshold (0.0 to 1.0)
    # Higher = fewer false positives, might miss real objects
    # Lower = more detections, more false positives
    'confidence_threshold': 0.5,
    
    # Video source
    # 0 = default webcam
    # 1 = external webcam
    # 'path/to/video.mp4' = video file
    'video_source': 0,
}

# ============================================================================
# ALERT CONFIGURATION
# ============================================================================

ALERT_CONFIG = {
    # Enable/disable alerts
    'enabled': True,
    
    # Alert method: 'console' or 'email'
    'method': 'console',
    
    # Objects that trigger alerts
    'triggers': ['person', 'car'],
    
    # Cooldown between alerts for same object (seconds)
    'cooldown_seconds': 10,
    
    # Email configuration (only used if method='email')
    'email_config': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender_email': 'your_email@gmail.com',
        'sender_password': 'your_app_password',  # Use app password, not regular password
        'recipient_email': 'recipient@example.com'
    }
}

# ============================================================================
# DISPLAY CONFIGURATION
# ============================================================================

DISPLAY_CONFIG = {
    # Show statistics overlay
    'show_stats': True,
    
    # Show frame counter
    'show_frame_count': True,
    
    # Display window size (None for auto)
    'window_width': None,
    'window_height': None,
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    # Enable CSV logging
    'enabled': True,
    
    # Log directory
    'log_dir': 'logs',
    
    # Log filename format
    'filename_format': 'detections_%Y%m%d_%H%M%S.csv',
}

# ============================================================================
# ANALYTICS CONFIGURATION
# ============================================================================

ANALYTICS_CONFIG = {
    # Auto-generate reports after detection
    'auto_report': False,
    
    # Report directory
    'report_dir': 'reports',
    
    # Chart DPI (higher = better quality, larger files)
    'chart_dpi': 300,
    
    # Timeline resample interval
    'timeline_interval': '1min',  # Options: '30s', '1min', '5min', '1H'
}

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================

PERFORMANCE_CONFIG = {
    # Use GPU if available
    'use_gpu': True,
    
    # Frame skip (process every Nth frame for better performance)
    # 1 = process every frame
    # 2 = process every other frame
    'frame_skip': 1,
    
    # Maximum FPS (None for unlimited)
    'max_fps': None,
}

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

"""
To use this configuration in your code:

from config import DETECTOR_CONFIG, ALERT_CONFIG

detector = ObjectDetector(
    model_path=DETECTOR_CONFIG['model_path'],
    confidence_threshold=DETECTOR_CONFIG['confidence_threshold']
)

alerts = AlertSystem(ALERT_CONFIG)
"""
