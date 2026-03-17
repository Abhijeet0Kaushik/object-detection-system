"""
Core object detection module with YOLOv8
Handles real-time detection, counting, and logging
"""

from ultralytics import YOLO
import cv2
import numpy as np
from datetime import datetime
from collections import defaultdict
import csv
import os


class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt", confidence_threshold=0.5):
        """
        Initialize the object detector
        
        Args:
            model_path: Path to YOLO model weights
            confidence_threshold: Minimum confidence for detections
        """
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.object_counts = defaultdict(int)
        self.detection_log = []
        
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Initialize CSV log file
        self.log_file = f"logs/detections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(self.log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'object', 'confidence', 'bbox_x', 'bbox_y', 'bbox_w', 'bbox_h'])
    
    def detect(self, frame):
        """
        Run detection on a single frame
        
        Args:
            frame: Input image/frame (BGR format)
            
        Returns:
            annotated_frame: Frame with bounding boxes
            detections: List of detection details
        """
        # Run YOLO detection
        results = self.model(frame, conf=self.confidence_threshold)
        
        # Reset counts for this frame
        self.object_counts.clear()
        detections = []
        
        # Process detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Extract detection info
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                bbox = box.xyxy[0].cpu().numpy()
                
                # Get class name
                class_name = self.model.names[cls_id]
                
                # Count objects
                self.object_counts[class_name] += 1
                
                # Store detection
                detection = {
                    'class': class_name,
                    'confidence': conf,
                    'bbox': bbox
                }
                detections.append(detection)
                
                # Log detection
                self._log_detection(class_name, conf, bbox)
        
        # Get annotated frame
        annotated_frame = results[0].plot()
        
        return annotated_frame, detections
    
    def _log_detection(self, class_name, confidence, bbox):
        """Log detection to CSV file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                class_name,
                f"{confidence:.3f}",
                int(bbox[0]),
                int(bbox[1]),
                int(bbox[2] - bbox[0]),
                int(bbox[3] - bbox[1])
            ])
    
    def get_object_counts(self):
        """Get current object counts"""
        return dict(self.object_counts)
    
    def draw_stats(self, frame):
        """
        Draw statistics overlay on frame
        
        Args:
            frame: Input frame
            
        Returns:
            frame: Frame with stats overlay
        """
        # Create semi-transparent overlay
        overlay = frame.copy()
        
        # Stats panel dimensions
        panel_height = 40 + len(self.object_counts) * 30
        cv2.rectangle(overlay, (10, 10), (300, panel_height), (0, 0, 0), -1)
        
        # Blend overlay
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
        
        # Draw title
        cv2.putText(frame, "Object Detection Stats", (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw counts
        y_offset = 65
        for obj, count in sorted(self.object_counts.items()):
            text = f"{obj}: {count}"
            cv2.putText(frame, text, (20, y_offset),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            y_offset += 30
        
        return frame
# In detector.py
def cleanup_old_logs(days_to_keep=30):
    """Delete logs older than X days"""
    import glob
    from datetime import datetime, timedelta
    
    cutoff = datetime.now() - timedelta(days=days_to_keep)
    
    for log_file in glob.glob("logs/detections_*.csv"):
        # Extract timestamp from filename
        file_date = extract_date_from_filename(log_file)
        if file_date < cutoff:
            os.remove(log_file)
