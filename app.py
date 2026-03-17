"""
Real-Time Object Detection System
Main application entry point
"""

import cv2
import argparse
from detector import ObjectDetector
from alerts import AlertSystem, AlertConfigHelper

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Real-Time Object Detection System')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help='Path to YOLO model weights')
    parser.add_argument('--confidence', type=float, default=0.5,
                        help='Confidence threshold for detections')
    parser.add_argument('--source', type=str, default='0',
                        help='Video source (0 for webcam, or video file path)')
    parser.add_argument('--alerts', action='store_true',
                        help='Enable console alerts for person detection')
    parser.add_argument('--no-stats', action='store_true',
                        help='Hide object count statistics overlay')
    
    args = parser.parse_args()
    
    # Initialize detector
    print("🚀 Initializing Object Detector...")
    detector = ObjectDetector(
        model_path=args.model,
        confidence_threshold=args.confidence
    )
    
    # Initialize alert system
    if args.alerts:
        alert_config = AlertConfigHelper.console_alerts(['person', 'car'])
        alerts = AlertSystem(alert_config)
        print("⚠️  Alert system enabled for: person, car")
    else:
        alerts = AlertSystem({'enabled': False})
    
    # Open video source
    print(f"📹 Opening video source: {args.source}")
    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)
    
    if not cap.isOpened():
        print("❌ Error: Could not open video source")
        return
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"✅ Video source opened: {width}x{height} @ {fps:.1f} FPS")
    print("\nControls:")
    print("  - Press 'q' to quit")
    print("  - Press 's' to toggle stats overlay")
    print("  - Detection logs saved to logs/ directory")
    print("\nStarting detection...\n")
    
    show_stats = not args.no_stats
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("End of video stream")
                break
            
            frame_count += 1
            
            # Run detection
            annotated_frame, detections = detector.detect(frame)
            
            # Check for alerts
            alerts.check_and_alert(detections)
            
            # Add stats overlay
            if show_stats:
                annotated_frame = detector.draw_stats(annotated_frame)
            
            # Add frame counter
            cv2.putText(annotated_frame, f"Frame: {frame_count}", 
                        (width - 150, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display frame
            cv2.imshow("Real-Time Object Detection", annotated_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\n🛑 Stopping detection...")
                break
            elif key == ord('s'):
                show_stats = not show_stats
                print(f"Stats overlay: {'ON' if show_stats else 'OFF'}")
    
    except KeyboardInterrupt:
        print("\n🛑 Detection interrupted by user")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n✅ Detection complete!")
        print(f"Total frames processed: {frame_count}")
        print(f"Detection log saved to: {detector.log_file}")


if __name__ == "__main__":
    main()
