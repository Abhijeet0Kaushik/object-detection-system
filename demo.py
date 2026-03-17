"""
Demo Script - Test Without Webcam
Uses test images to demonstrate detection capabilities
"""

import cv2
import numpy as np
from detector import ObjectDetector
from alerts import AlertSystem, AlertConfigHelper
import time
import requests
from io import BytesIO


def download_sample_image(url):
    """Download a sample image from URL"""
    try:
        response = requests.get(url, timeout=10)
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f"Failed to download image: {e}")
        return None


def create_test_image():
    """Create a simple test image with text"""
    img = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    text = "Object Detection Demo"
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, (100, 240), font, 1.5, (0, 0, 0), 2)
    
    return img


def demo_basic_detection():
    """Demo 1: Basic detection on sample images"""
    print("\n" + "="*60)
    print("DEMO 1: Basic Detection")
    print("="*60)
    print("\nDownloading sample images...")
    
    # Sample image URLs (public domain / creative commons)
    sample_urls = [
        "https://images.unsplash.com/photo-1551782450-a2132b4ba21d",  # City street
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",  # Mountain landscape
    ]
    
    detector = ObjectDetector(confidence_threshold=0.4)
    
    for i, url in enumerate(sample_urls, 1):
        print(f"\nProcessing image {i}...")
        
        # Create fallback image if download fails
        image = download_sample_image(url)
        if image is None:
            print("Using test image instead")
            image = create_test_image()
        
        # Run detection
        annotated, detections = detector.detect(image)
        annotated = detector.draw_stats(annotated)
        
        # Display results
        print(f"\nDetections found:")
        for det in detections:
            print(f"  - {det['class']}: {det['confidence']:.2%}")
        
        # Show image
        cv2.imshow(f"Demo - Image {i}", annotated)
        cv2.waitKey(3000)  # Show for 3 seconds
        cv2.destroyAllWindows()
        
        time.sleep(0.5)
    
    print("\n✅ Basic detection demo complete!")


def demo_with_alerts():
    """Demo 2: Detection with alert system"""
    print("\n" + "="*60)
    print("DEMO 2: Detection with Alerts")
    print("="*60)
    
    # Create test image with person
    print("\nCreating test image...")
    image = create_test_image()
    
    # Initialize detector and alerts
    detector = ObjectDetector(confidence_threshold=0.3)
    alert_config = AlertConfigHelper.console_alerts(['person', 'car', 'bottle'])
    alerts = AlertSystem(alert_config)
    
    print("\nRunning detection with alert monitoring...")
    
    # Run detection
    annotated, detections = detector.detect(image)
    annotated = detector.draw_stats(annotated)
    
    # Check for alerts
    alerts.check_and_alert(detections)
    
    # Display results
    print(f"\nDetections: {len(detections)}")
    
    cv2.imshow("Demo - Alerts", annotated)
    cv2.waitKey(3000)
    cv2.destroyAllWindows()
    
    print("\n✅ Alert demo complete!")


def demo_statistics():
    """Demo 3: Detection statistics and logging"""
    print("\n" + "="*60)
    print("DEMO 3: Statistics and Logging")
    print("="*60)
    
    detector = ObjectDetector(confidence_threshold=0.4)
    
    print("\nProcessing multiple frames...")
    
    # Simulate processing multiple frames
    for i in range(5):
        image = create_test_image()
        
        # Add some variation
        cv2.putText(image, f"Frame {i+1}", (20, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        annotated, detections = detector.detect(image)
        print(f"Frame {i+1}: {len(detections)} detections")
        
        time.sleep(0.1)
    
    # Show final statistics
    print("\nFinal Statistics:")
    counts = detector.get_object_counts()
    
    if counts:
        for obj, count in sorted(counts.items()):
            print(f"  {obj}: {count}")
    else:
        print("  No objects detected")
    
    print(f"\nLog saved to: {detector.log_file}")
    print("\n✅ Statistics demo complete!")


def demo_model_comparison():
    """Demo 4: Compare different confidence thresholds"""
    print("\n" + "="*60)
    print("DEMO 4: Confidence Threshold Comparison")
    print("="*60)
    
    image = create_test_image()
    
    thresholds = [0.3, 0.5, 0.7]
    
    print("\nComparing confidence thresholds...")
    
    for threshold in thresholds:
        print(f"\nThreshold: {threshold}")
        
        detector = ObjectDetector(confidence_threshold=threshold)
        annotated, detections = detector.detect(image)
        
        print(f"  Detections: {len(detections)}")
        
        if detections:
            avg_conf = sum(d['confidence'] for d in detections) / len(detections)
            print(f"  Average confidence: {avg_conf:.3f}")
    
    print("\n💡 Higher threshold = fewer detections, higher confidence")
    print("   Lower threshold = more detections, may include false positives")
    print("\n✅ Comparison demo complete!")


def run_all_demos():
    """Run all demo scripts"""
    print("\n" + "="*70)
    print("  OBJECT DETECTION SYSTEM - DEMO MODE")
    print("="*70)
    print("\nThis demo runs WITHOUT a webcam using test images")
    print("Perfect for testing the system before using live video\n")
    
    try:
        demo_basic_detection()
        demo_with_alerts()
        demo_statistics()
        demo_model_comparison()
        
        print("\n" + "="*70)
        print("  ALL DEMOS COMPLETE!")
        print("="*70)
        print("\nNext steps:")
        print("  1. Try with your webcam: python app.py")
        print("  2. Launch web dashboard: streamlit run dashboard.py")
        print("  3. Analyze logs: python example_analytics.py")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("\nMake sure you have all dependencies installed:")
        print("  pip install -r requirements.txt --break-system-packages")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        demo_num = sys.argv[1]
        
        if demo_num == '1':
            demo_basic_detection()
        elif demo_num == '2':
            demo_with_alerts()
        elif demo_num == '3':
            demo_statistics()
        elif demo_num == '4':
            demo_model_comparison()
        else:
            print("Usage: python demo.py [1|2|3|4]")
            print("  1 - Basic detection")
            print("  2 - With alerts")
            print("  3 - Statistics")
            print("  4 - Model comparison")
    else:
        run_all_demos()
