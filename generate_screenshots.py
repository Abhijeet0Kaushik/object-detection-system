"""
Screenshot and Demo Content Generator
Helps create portfolio-ready screenshots and demos
"""

import cv2
import numpy as np
from detector import ObjectDetector
import matplotlib.pyplot as plt
from datetime import datetime
import os


class DemoContentGenerator:
    """Generate screenshots and demo content for portfolio"""
    
    def __init__(self, output_dir="screenshots"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def create_demo_frame(self, width=1280, height=720):
        """Create a demo frame with sample detections"""
        # Create background
        frame = np.ones((height, width, 3), dtype=np.uint8) * 240
        
        # Add title
        cv2.putText(frame, "Real-Time Object Detection System", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

        # Simulate bounding boxes
        boxes = [
            (100, 150, 250, 400, "person", 0.95),
            (350, 200, 500, 450, "laptop", 0.88),
            (600, 250, 750, 400, "phone", 0.92),
            (850, 180, 1100, 500, "chair", 0.85),
        ]
        
        for x1, y1, x2, y2, label, conf in boxes:
            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            
            # Add label background
            label_text = f"{label} {conf:.2%}"
            (text_w, text_h), _ = cv2.getTextSize(
                label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
            )
            cv2.rectangle(frame, (x1, y1 - text_h - 10), 
                         (x1 + text_w + 10, y1), (0, 255, 0), -1)
            
            # Add label text
            cv2.putText(frame, label_text, (x1 + 5, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Add stats panel
        stats_y = 150
        cv2.rectangle(frame, (50, stats_y), (300, stats_y + 150), 
                     (0, 0, 0), -1)
        cv2.rectangle(frame, (50, stats_y), (300, stats_y + 150), 
                     (0, 255, 0), 2)
        
        cv2.putText(frame, "Detection Stats", (60, stats_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, "person: 1", (60, stats_y + 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, "laptop: 1", (60, stats_y + 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, "phone: 1", (60, stats_y + 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, "chair: 1", (60, stats_y + 135),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame
    
    def generate_detection_screenshot(self):
        """Generate main detection screenshot"""
        print("📸 Generating detection screenshot...")
        
        frame = self.create_demo_frame()
        
        output_path = os.path.join(self.output_dir, "detection_example.png")
        cv2.imwrite(output_path, frame)
        
        print(f"✅ Saved: {output_path}")
        return output_path
    
    def generate_dashboard_mockup(self):
        """Generate dashboard mockup screenshot"""
        print("📸 Generating dashboard mockup...")
        
        # Create larger canvas for dashboard
        width, height = 1920, 1080
        img = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # Header
        cv2.rectangle(img, (0, 0), (width, 80), (31, 119, 180), -1)
        cv2.putText(img, "Object Detection Dashboard", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    
        # Main video area
        video_frame = self.create_demo_frame(1200, 675)
        img[100:775, 50:1250] = video_frame
        
        
        # Stats sidebar
        cv2.rectangle(img, (1300, 100), (1870, 1000), (240, 240, 240), -1)
        cv2.putText(img, "Statistics", (1320, 150),
                   cv2.FONT_HERSHEY_BOLD, 1.0, (0, 0, 0), 2)
        
        # Add sample stats
        stats = [
            "Total Detections: 1,247",
            "Session Time: 00:15:32",
            "Avg FPS: 28.5",
            "",
            "Object Counts:",
            "  person: 423",
            "  car: 156",
            "  phone: 89",
            "  laptop: 67",
        ]
        
        y_offset = 200
        for stat in stats:
            cv2.putText(img, stat, (1320, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            y_offset += 40
        
        output_path = os.path.join(self.output_dir, "dashboard_mockup.png")
        cv2.imwrite(output_path, img)
        
        print(f"✅ Saved: {output_path}")
        return output_path
    
    def generate_analytics_chart(self):
        """Generate sample analytics chart"""
        print("📊 Generating analytics chart...")
        
        # Sample data
        objects = ['person', 'car', 'phone', 'laptop', 'bottle', 'chair']
        counts = [423, 156, 89, 67, 45, 34]
        
        # Create chart
        plt.figure(figsize=(12, 6))
        plt.bar(objects, counts, color='steelblue')
        plt.title('Object Detection Distribution', fontsize=16, fontweight='bold')
        plt.xlabel('Object Type', fontsize=12)
        plt.ylabel('Detection Count', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        
        output_path = os.path.join(self.output_dir, "analytics_chart.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
        return output_path
    
    def generate_timeline_chart(self):
        """Generate sample timeline chart"""
        print("📈 Generating timeline chart...")
        
        import pandas as pd
        
        # Sample timeline data
        times = pd.date_range('2024-01-01 00:00', periods=100, freq='1min')
        detections = np.random.poisson(5, 100)
        
        plt.figure(figsize=(14, 6))
        plt.plot(times, detections, color='darkgreen', linewidth=2)
        plt.fill_between(times, detections, alpha=0.3, color='green')
        plt.title('Detection Timeline', fontsize=16, fontweight='bold')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Detections per Minute', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        output_path = os.path.join(self.output_dir, "timeline_chart.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Saved: {output_path}")
        return output_path
    
    def generate_architecture_diagram(self):
        """Generate architecture diagram"""
        print("🏗️  Generating architecture diagram...")
        
        # Create diagram
        width, height = 1400, 800
        img = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # Colors
        color_input = (100, 150, 255)      # Blue
        color_process = (100, 255, 150)    # Green
        color_output = (255, 150, 100)     # Orange
        
        # Title
        cv2.putText(img, "System Architecture", (500, 50),
                   cv2.FONT_HERSHEY_BOLD, 1.5, (0, 0, 0), 3)
        
        # Components
        components = [
            # (x, y, w, h, label, color)
            (100, 150, 200, 80, "Webcam\nInput", color_input),
            (400, 150, 200, 80, "YOLOv8\nDetection", color_process),
            (700, 100, 200, 80, "Logging", color_output),
            (700, 250, 200, 80, "Alerts", color_output),
            (700, 400, 200, 80, "Display", color_output),
            (1000, 250, 250, 80, "Analytics &\nReports", color_output),
        ]
        
        for x, y, w, h, label, color in components:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
            
            # Add text (multi-line)
            lines = label.split('\n')
            for i, line in enumerate(lines):
                text_y = y + h//2 + (i - len(lines)//2) * 25
                (text_w, text_h), _ = cv2.getTextSize(
                    line, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
                )
                text_x = x + (w - text_w) // 2
                cv2.putText(img, line, (text_x, text_y),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        # Arrows
        arrows = [
            (300, 190, 400, 190),   # Input → Detection
            (600, 190, 700, 140),   # Detection → Logging
            (600, 190, 700, 290),   # Detection → Alerts
            (600, 190, 700, 440),   # Detection → Display
            (900, 290, 1000, 290),  # Alerts/Logging → Analytics
        ]
        
        for x1, y1, x2, y2 in arrows:
            cv2.arrowedLine(img, (x1, y1), (x2, y2), (0, 0, 0), 3, 
                           tipLength=0.05)
        
        output_path = os.path.join(self.output_dir, "architecture.png")
        cv2.imwrite(output_path, img)
        
        print(f"✅ Saved: {output_path}")
        return output_path
    
    def generate_all(self):
        """Generate all demo content"""
        print("\n" + "="*60)
        print("GENERATING PORTFOLIO SCREENSHOTS")
        print("="*60 + "\n")
        
        screenshots = []
        
        screenshots.append(self.generate_detection_screenshot())
        screenshots.append(self.generate_dashboard_mockup())
        screenshots.append(self.generate_analytics_chart())
        screenshots.append(self.generate_timeline_chart())
        screenshots.append(self.generate_architecture_diagram())
        
        print("\n" + "="*60)
        print("✅ ALL SCREENSHOTS GENERATED!")
        print("="*60)
        print(f"\nLocation: {self.output_dir}/")
        print("\nGenerated files:")
        for screenshot in screenshots:
            print(f"  - {os.path.basename(screenshot)}")
        
        print("\nNext steps:")
        print("  1. Add these to your README.md")
        print("  2. Use in LinkedIn/Twitter posts")
        print("  3. Include in portfolio website")
        print("  4. Create a GIF from detection_example.png")
        
        return screenshots


def main():
    """Generate demo content"""
    generator = DemoContentGenerator()
    generator.generate_all()


if __name__ == "__main__":
    main()
