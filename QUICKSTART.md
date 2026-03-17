# 🚀 Quick Start Guide

Get up and running with the Object Detection System in 5 minutes!

## Step 1: Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/object-detection-system.git
cd object-detection-system

# Run automated setup
python setup.py
```

That's it! The setup script will:
- ✅ Check Python version
- ✅ Install all dependencies
- ✅ Download the YOLO model
- ✅ Create necessary directories

## Step 2: Run Your First Detection (30 seconds)

### Option A: Command Line (Fastest)

```bash
python app.py
```

**Controls:**
- Press `q` to quit
- Press `s` to toggle statistics

### Option B: Web Dashboard (Most User-Friendly)

```bash
streamlit run dashboard.py
```

Then open your browser to `http://localhost:8501`

## Step 3: Explore the Results (2 minutes)

### Check Your Detection Logs

```bash
ls logs/
```

You'll see files like: `detections_20240316_143022.csv`

### Generate an Analysis Report

```python
python example_analytics.py
```

This creates:
- 📄 Text report
- 📊 Charts and graphs
- 📈 Timeline analysis

## Common Use Cases

### 1. Security Monitoring (Person Detection)

```bash
python app.py --alerts
```

Gets an alert whenever a person is detected!

### 2. Traffic Counting (Vehicle Detection)

```bash
python app.py --confidence 0.6
```

Higher confidence = more accurate car/truck/bus detection

### 3. Analyzing Recorded Video

```bash
python app.py --source path/to/video.mp4
```

Process any video file instead of live webcam

## Customization in 3 Lines

```python
from detector import ObjectDetector

detector = ObjectDetector(
    model_path='yolov8n.pt',      # Model: n=fast, m=accurate
    confidence_threshold=0.6       # Higher = fewer false positives
)
```

## What Gets Detected?

**80+ objects including:**

| Category | Examples |
|----------|----------|
| People | person |
| Vehicles | car, truck, bus, motorcycle, bicycle |
| Electronics | laptop, phone, TV, keyboard, mouse |
| Furniture | chair, couch, table, bed |
| Kitchen | bottle, cup, fork, knife, bowl |
| Animals | dog, cat, bird, horse, cow |
| Sports | ball, racket, skateboard, surfboard |

## Troubleshooting

### "No module named 'ultralytics'"
```bash
pip install -r requirements.txt --break-system-packages
```

### "Camera not found"
```bash
# Try different camera indices
python app.py --source 1  # or 2, 3, etc.
```

### Low FPS / Slow Performance
```bash
# Use faster model
python app.py --model yolov8n.pt

# Or skip frames
# (edit config_template.py and set frame_skip: 2)
```

## Next Steps

1. **Read the full README**: `README.md`
2. **Customize configuration**: Copy `config_template.py` to `config.py`
3. **Try the analytics**: `python example_analytics.py`
4. **Build your own features**: Check the code in `detector.py`, `alerts.py`, `utils.py`

## Example Projects to Build

### Beginner Level
- Count people entering a room
- Detect when a package is delivered
- Monitor if your pet is on the couch

### Intermediate Level
- Traffic counting dashboard
- Retail customer analytics
- Smart doorbell with person detection

### Advanced Level
- Multi-camera surveillance system
- Object tracking across frames
- Custom model training for specific objects
- Cloud deployment with real-time alerts

## Getting Help

- 📖 Read the full documentation in README.md
- 💬 Open an issue on GitHub
- 📧 Contact: [your email]

---

**You're ready to go! Start detecting objects now:**

```bash
python app.py
```

Happy detecting! 🎯
