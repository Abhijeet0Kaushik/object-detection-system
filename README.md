# 🎯 Real-Time Object Detection System

A production-ready computer vision application that performs real-time object detection using YOLOv8, featuring web dashboard, analytics, alerts, and comprehensive logging.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Latest-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Core Capabilities
- **Real-Time Detection**: Detects 80+ common objects using state-of-the-art YOLOv8
- **Live Object Counting**: Track counts of each detected object type in real-time
- **Detection Logging**: Automatic CSV logging with timestamps, confidence scores, and bounding boxes
- **Alert System**: Configurable alerts (console/email) when specific objects are detected
- **Web Dashboard**: Browser-based interface using Streamlit
- **Analytics & Reporting**: Generate detailed reports and visualizations from detection logs

### Objects Detected (80+ classes)
- **People**: person
- **Vehicles**: car, truck, bus, motorcycle, bicycle
- **Electronics**: laptop, phone, keyboard, mouse, TV, remote
- **Everyday Items**: bottle, cup, book, scissors, chair, couch
- **Animals**: dog, cat, bird, horse, cow, and more

## 🏗️ Architecture

```
┌─────────────────┐
│   Webcam Input  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Frame Capture  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   YOLOv8 Model  │
│   (Detection)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Post-Process   │
│  - Count        │
│  - Log          │
│  - Alert        │
└────────┬────────┘
         │
         ├────────────────┬────────────────┐
         ▼                ▼                ▼
    ┌────────┐      ┌────────┐      ┌─────────┐
    │Display │      │  CSV   │      │ Alerts  │
    │ (Live) │      │  Logs  │      │ System  │
    └────────┘      └────────┘      └─────────┘
```

## 📂 Project Structure

```
object-detection-system/
│
├── app.py                 # Main CLI application
├── dashboard.py           # Streamlit web dashboard
├── detector.py            # Core detection logic
├── alerts.py             # Alert system (console/email)
├── utils.py              # Analytics and reporting utilities
│
├── requirements.txt      # Python dependencies
├── README.md            # This file
│
├── logs/                # Detection logs (auto-generated)
│   └── detections_YYYYMMDD_HHMMSS.csv
│
├── reports/             # Generated reports (auto-generated)
│   ├── report_YYYYMMDD_HHMMSS.txt
│   ├── distribution_YYYYMMDD_HHMMSS.png
│   └── timeline_YYYYMMDD_HHMMSS.png
│
└── screenshots/         # Demo images and videos
    └── demo.gif
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam or video input device
- (Optional) GPU for faster processing

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/object-detection-system.git
cd object-detection-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**

**Option A: Command Line Interface**
```bash
python app.py
```

**Option B: Web Dashboard**
```bash
streamlit run dashboard.py
```

## 💻 Usage

### Command Line Application

**Basic usage:**
```bash
python app.py
```

**With custom settings:**
```bash
python app.py --confidence 0.6 --alerts --show-stats
```

**Command line options:**
- `--model`: YOLO model to use (yolov8n.pt, yolov8s.pt, yolov8m.pt)
- `--confidence`: Confidence threshold (0.0-1.0, default: 0.5)
- `--source`: Video source (0 for webcam, or path to video file)
- `--alerts`: Enable console alerts
- `--show-stats`: Show statistics overlay

**Controls during detection:**
- Press `q` to quit
- Press `s` to toggle statistics overlay

### Web Dashboard

1. Start the dashboard:
```bash
streamlit run dashboard.py
```

2. Open browser to `http://localhost:8501`

3. Configure settings in sidebar:
   - Adjust confidence threshold
   - Select model size
   - Enable/disable statistics overlay
   - Configure alert triggers

4. Click "Start Detection" to begin

## 📊 Analytics & Reporting

### Generate Analysis Report

```python
from utils import DetectionAnalyzer

# Analyze latest log
analyzer = DetectionAnalyzer()

# Generate complete report with charts
analyzer.generate_report()
```

This creates:
- Text summary report
- Object distribution chart
- Detection timeline graph
- Confidence score distribution

### Quick Log Summary

```python
from utils import print_log_summary

print_log_summary()
```

## 🔔 Alert System

### Console Alerts

```python
from alerts import AlertConfigHelper, AlertSystem

# Configure alerts for specific objects
config = AlertConfigHelper.console_alerts(['person', 'car'])
alert_system = AlertSystem(config)
```

### Email Alerts

```python
config = AlertConfigHelper.email_alerts(
    trigger_objects=['person'],
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    sender_email='your_email@gmail.com',
    sender_password='your_app_password',
    recipient_email='recipient@example.com'
)
alert_system = AlertSystem(config)
```

## 🎓 How It Works

### YOLOv8 Detection Pipeline

1. **Input**: Frame from webcam/video
2. **Preprocessing**: Resize and normalize image
3. **Detection**: YOLOv8 processes frame in single pass
4. **Post-processing**:
   - Filter by confidence threshold
   - Apply Non-Maximum Suppression (NMS)
   - Extract bounding boxes and class labels
5. **Output**: Annotated frame with detections

### Performance Optimization

- **Model Selection**: 
  - `yolov8n.pt`: Fastest, smallest (recommended for CPU)
  - `yolov8s.pt`: Balanced speed/accuracy
  - `yolov8m.pt`: Better accuracy, slower

- **Confidence Tuning**: Higher threshold = fewer false positives, might miss objects

## 📈 Example Use Cases

### 1. Retail Analytics
- Count customers entering/leaving store
- Track product interactions
- Monitor queue lengths

### 2. Security & Surveillance
- Detect unauthorized persons
- Alert on vehicle presence
- Monitor restricted areas

### 3. Traffic Monitoring
- Count vehicles by type
- Analyze traffic patterns
- Detect congestion

### 4. Smart Home
- Person detection at door
- Package delivery alerts
- Pet monitoring

## 🔧 Advanced Configuration

### Custom Detection Classes

```python
from detector import ObjectDetector

detector = ObjectDetector(
    model_path='yolov8n.pt',
    confidence_threshold=0.6
)

# Filter to specific classes only
results = detector.detect(frame)
filtered = [d for d in results if d['class'] in ['person', 'car']]
```

### Video File Processing

```bash
python app.py --source path/to/video.mp4
```

### Batch Processing

```python
import cv2
from detector import ObjectDetector

detector = ObjectDetector()
cap = cv2.VideoCapture('input.mp4')

# Process entire video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    annotated, detections = detector.detect(frame)
    # Process detections...

cap.release()
```

## 📊 Detection Log Format

CSV logs contain:

| Column | Description |
|--------|-------------|
| timestamp | Detection time (YYYY-MM-DD HH:MM:SS.mmm) |
| object | Object class name |
| confidence | Detection confidence (0.0-1.0) |
| bbox_x | Bounding box top-left X coordinate |
| bbox_y | Bounding box top-left Y coordinate |
| bbox_w | Bounding box width |
| bbox_h | Bounding box height |

## 🚧 Troubleshooting

### Webcam Not Found
```bash
# List available cameras
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```

### Low FPS
- Use smaller model (yolov8n.pt)
- Lower webcam resolution
- Use GPU if available

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🎯 Future Improvements

- [ ] GPU acceleration with CUDA
- [ ] Multi-camera support
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Real-time metrics dashboard
- [ ] Mobile app integration
- [ ] Object tracking across frames
- [ ] Custom model training
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] REST API for external integrations
- [ ] Docker containerization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection model
- [OpenCV](https://opencv.org/) - Computer vision library
- [Streamlit](https://streamlit.io/) - Web dashboard framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Python, YOLOv8, and OpenCV**
