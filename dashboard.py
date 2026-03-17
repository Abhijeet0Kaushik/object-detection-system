"""
Web Dashboard for Real-Time Object Detection
Built with Streamlit for browser-based viewing
"""

import streamlit as st
import cv2
import numpy as np
from detector import ObjectDetector
from alerts import AlertSystem, AlertConfigHelper
import time
from datetime import datetime
import pandas as pd


# Page config
st.set_page_config(
    page_title="Object Detection Dashboard",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_detector(model_path, confidence):
    """Load and cache the detector"""
    return ObjectDetector(model_path=model_path, confidence_threshold=confidence)


def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 Real-Time Object Detection Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.header("⚙️ Settings")
    
    confidence_threshold = st.sidebar.slider(
        "Confidence Threshold",
        min_value=0.1,
        max_value=1.0,
        value=0.5,
        step=0.05
    )
    
    model_size = st.sidebar.selectbox(
        "Model Size",
        ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"],
        help="Larger models are more accurate but slower"
    )
    
    show_stats = st.sidebar.checkbox("Show Statistics Overlay", value=True)
    
    enable_alerts = st.sidebar.checkbox("Enable Alerts", value=False)
    
    alert_objects = []
    if enable_alerts:
        alert_objects = st.sidebar.multiselect(
            "Alert Triggers",
            ["person", "car", "phone", "laptop", "bottle"],
            default=["person"]
        )
    
    # Load detector
    detector = load_detector(model_size, confidence_threshold)
    
    # Initialize alert system
    if enable_alerts and alert_objects:
        alert_config = AlertConfigHelper.console_alerts(alert_objects)
        alerts = AlertSystem(alert_config)
    else:
        alerts = AlertSystem({'enabled': False})
    
    # Main layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Live Feed")
        video_placeholder = st.empty()
    
    with col2:
        st.subheader("📊 Detection Statistics")
        stats_placeholder = st.empty()
        
        st.subheader("🔔 Recent Alerts")
        alerts_placeholder = st.empty()
    
    # Control buttons
    col_start, col_stop = st.columns(2)
    
    with col_start:
        start_button = st.button("🎬 Start Detection", use_container_width=True)
    
    with col_stop:
        stop_button = st.button("🛑 Stop Detection", use_container_width=True)
    
    # Session state
    if 'running' not in st.session_state:
        st.session_state.running = False
    
    if 'alert_history' not in st.session_state:
        st.session_state.alert_history = []
    
    if start_button:
        st.session_state.running = True
    
    if stop_button:
        st.session_state.running = False
    
    # Main detection loop
    if st.session_state.running:
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Could not open webcam")
            st.session_state.running = False
            return
        
        frame_count = 0
        
        while st.session_state.running:
            ret, frame = cap.read()
            
            if not ret:
                st.warning("Failed to grab frame")
                break
            
            frame_count += 1
            
            # Run detection
            annotated_frame, detections = detector.detect(frame)
            
            # Add stats overlay if enabled
            if show_stats:
                annotated_frame = detector.draw_stats(annotated_frame)
            
            # Check for alerts
            alerts.check_and_alert(detections)
            
            # Update alert history
            for detection in detections:
                if detection['class'] in alert_objects:
                    st.session_state.alert_history.append({
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'object': detection['class'],
                        'confidence': detection['confidence']
                    })
                    # Keep only last 10 alerts
                    st.session_state.alert_history = st.session_state.alert_history[-10:]
            
            # Convert BGR to RGB for Streamlit
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            
            # Display video
            video_placeholder.image(annotated_frame, channels="RGB", use_container_width=True)
            
            # Update statistics
            counts = detector.get_object_counts()
            
            if counts:
                stats_df = pd.DataFrame([
                    {"Object": obj, "Count": count}
                    for obj, count in sorted(counts.items())
                ])
                stats_placeholder.dataframe(stats_df, use_container_width=True, hide_index=True)
            else:
                stats_placeholder.info("No objects detected")
            
            # Update alerts
            if st.session_state.alert_history:
                alerts_df = pd.DataFrame(st.session_state.alert_history)
                alerts_placeholder.dataframe(
                    alerts_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                alerts_placeholder.info("No alerts triggered")
            
            # Small delay to prevent overwhelming the browser
            time.sleep(0.03)
        
        cap.release()
    
    else:
        # Show placeholder when not running
        with col1:
            st.info("👆 Click 'Start Detection' to begin")
        
        with col2:
            st.info("Statistics will appear here during detection")


if __name__ == "__main__":
    main()
