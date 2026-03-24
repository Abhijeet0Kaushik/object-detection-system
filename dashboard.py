"""
Web Dashboard for Real-Time Object Detection
Built with Streamlit for browser-based viewing
Features: Sample Demo Video + User Upload
"""

import streamlit as st
import cv2
import numpy as np
from detector import ObjectDetector
from alerts import AlertSystem, AlertConfigHelper
import time
from datetime import datetime
import pandas as pd
import tempfile
import requests
from io import BytesIO


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
    .demo-badge {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_detector(model_path, confidence):
    """Load and cache the detector"""
    return ObjectDetector(model_path=model_path, confidence_threshold=confidence)


def process_video(video_source, detector, show_stats, alerts, alert_objects, is_demo=False):
    """Process video file (uploaded or demo)"""
    
    if isinstance(video_source, str):  # URL or file path
        cap = cv2.VideoCapture(video_source)
    else:  # Uploaded file
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_source.read())
        cap = cv2.VideoCapture(tfile.name)
    
    if not cap.isOpened():
        st.error("❌ Could not open video file")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📹 Detection in Progress")
        video_placeholder = st.empty()
    
    with col2:
        st.markdown("### 📊 Live Statistics")
        stats_placeholder = st.empty()
        
        st.markdown("### 🔔 Alerts")
        alerts_placeholder = st.empty()
    
    # Progress bar
    progress_placeholder = st.empty()
    
    frame_count = 0
    alert_history = []
    all_detections = []
    
    # Process frames
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame_count += 1
        
        # Run detection
        annotated_frame, detections = detector.detect(frame)
        all_detections.extend(detections)
        
        # Add stats overlay if enabled
        if show_stats:
            annotated_frame = detector.draw_stats(annotated_frame)
        
        # Check for alerts
        alerts.check_and_alert(detections)
        
        # Update alert history
        for detection in detections:
            if detection['class'] in alert_objects:
                alert_history.append({
                    'Frame': frame_count,
                    'Object': detection['class'],
                    'Confidence': f"{detection['confidence']:.2%}"
                })
        
        # Convert BGR to RGB for Streamlit
        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        # Display every few frames to speed up
        if frame_count % 3 == 0 or is_demo:
            video_placeholder.image(annotated_frame, channels="RGB", use_container_width=True)
            
            # Update statistics
            counts = detector.get_object_counts()
            if counts:
                stats_df = pd.DataFrame([
                    {"Object": obj, "Count": count}
                    for obj, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)
                ])
                stats_placeholder.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            # Show alerts
            if alert_history:
                recent_alerts = alert_history[-5:]  # Last 5 alerts
                alerts_df = pd.DataFrame(recent_alerts)
                alerts_placeholder.dataframe(alerts_df, use_container_width=True, hide_index=True)
            else:
                alerts_placeholder.info("No alerts triggered")
            
            # Update progress
            if total_frames > 0:
                progress_placeholder.progress(frame_count / total_frames, 
                                             text=f"Processing frame {frame_count}/{total_frames}")
    
    cap.release()
    
    if total_frames > 0:
        progress_placeholder.progress(1.0, text="✅ Processing complete!")
    
    # Final summary
    st.success(f"✅ Processed {frame_count} frames successfully!")
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Frames", frame_count)
    
    with col2:
        st.metric("Total Detections", len(all_detections))
    
    with col3:
        unique_objects = len(set([d['class'] for d in all_detections]))
        st.metric("Unique Objects", unique_objects)
    
    # All alerts summary
    if alert_history:
        with st.expander("📋 View All Alerts"):
            st.dataframe(pd.DataFrame(alert_history), use_container_width=True)


def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 Real-Time Object Detection Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Welcome banner
    st.success("""
    🎉 **Welcome!** Try the demo video below or upload your own video to see object detection in action!
    """)
    
    # Sidebar controls
    st.sidebar.header("⚙️ Settings")
    
    confidence_threshold = st.sidebar.slider(
        "Confidence Threshold",
        min_value=0.1,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Higher values = fewer detections but more accurate"
    )
    
    model_size = st.sidebar.selectbox(
        "Model Size",
        ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"],
        help="Larger models are more accurate but slower"
    )
    
    show_stats = st.sidebar.checkbox("Show Statistics Overlay", value=True)
    
    enable_alerts = st.sidebar.checkbox("Enable Alerts", value=True)
    
    alert_objects = []
    if enable_alerts:
        alert_objects = st.sidebar.multiselect(
            "Alert Triggers",
            ["person", "car", "phone", "laptop", "bottle", "chair", "dog", "cat"],
            default=["person", "car"],
            help="Get alerts when these objects are detected"
        )
    
    # GitHub repo link in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 📂 Source Code
    [View on GitHub](https://github.com/Abhijeet0Kaushik/object-detection-system)
    
    ### 💻 Run Locally
    ```bash
    git clone https://github.com/Abhijeet0Kaushik/object-detection-system.git
    cd object-detection-system
    pip install -r requirements.txt
    streamlit run dashboard.py
    ```
    """)
    
    # Load detector
    detector = load_detector(model_size, confidence_threshold)
    
    # Initialize alert system
    if enable_alerts and alert_objects:
        alert_config = AlertConfigHelper.console_alerts(alert_objects)
        alerts = AlertSystem(alert_config)
    else:
        alerts = AlertSystem({'enabled': False})
    
    # Main content - tabs
    tab1, tab2, tab3 = st.tabs(["🎬 Demo Video", "📤 Upload Your Video", "ℹ️ About"])
    
    with tab1:
        st.markdown('<div class="demo-badge">🌟 LIVE DEMO</div>', unsafe_allow_html=True)
        st.markdown("### See Object Detection in Action!")
        
        st.info("""
        👇 Click the button below to process our sample video and see real-time object detection!
        
        **What you'll see:**
        - Real-time bounding boxes around detected objects
        - Live statistics showing object counts
        - Alert notifications when specific objects appear
        """)
        
        # Demo video URLs - Using publicly accessible sample videos
        demo_videos = {
            "🚗 Traffic Scene (Cars & People)": "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/car-detection.mp4",
            "🚶 Pedestrians Walking": "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/people-detection.mp4",
            "🏪 Store Scene": "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/bottle-detection.mp4",
            "🎬 My Demo": "https://github.com/Abhijeet0Kaushik/object-detection-system/blob/main/sample/demo.mp4"
        }
        
        selected_demo = st.selectbox(
            "Choose a demo video:",
            list(demo_videos.keys()),
            help="Select different scenarios to see how detection works"
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("▶️ Run Demo", type="primary", use_container_width=True):
                st.session_state.run_demo = True
        
        with col2:
            st.caption("⚡ Processing takes 30-60 seconds depending on video length")
        
        if st.session_state.get('run_demo', False):
            st.markdown("---")
            with st.spinner("🎬 Loading demo video and initializing detection..."):
                try:
                    process_video(
                        demo_videos[selected_demo],
                        detector,
                        show_stats,
                        alerts,
                        alert_objects,
                        is_demo=True
                    )
                except Exception as e:
                    st.error(f"""
                    ⚠️ Demo video couldn't load from the default source.
                    
                    **No worries!** You can:
                    1. Try the "Upload Your Video" tab instead
                    2. Download any short video and upload it
                    3. Use your phone to record a 10-second video
                    
                    Error details: {str(e)}
                    """)
            
            st.session_state.run_demo = False
    
    with tab2:
        st.markdown("### 📤 Upload Your Own Video")
        
        st.info("""
        Upload any video to see object detection in action!
        
        **Best results:**
        - 📹 Videos with people, cars, or common objects
        - ⏱️ Shorter videos (10-30 seconds) process faster
        - 🎥 Clear lighting and stable footage
        - 📏 MP4, AVI, MOV, or MKV format
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a video file",
            type=['mp4', 'avi', 'mov', 'mkv', 'webm'],
            help="Maximum file size: 200MB"
        )
        
        if uploaded_file is not None:
            # Show file info
            file_size = uploaded_file.size / (1024 * 1024)  # Convert to MB
            st.success(f"✅ Uploaded: **{uploaded_file.name}** ({file_size:.2f} MB)")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                process_btn = st.button("🎬 Process Video", type="primary", use_container_width=True)
            
            with col2:
                st.caption(f"⏱️ Estimated processing time: {int(file_size * 2)}-{int(file_size * 4)} seconds")
            
            if process_btn:
                st.markdown("---")
                with st.spinner("Processing your video... Please wait."):
                    process_video(uploaded_file, detector, show_stats, alerts, alert_objects)
        else:
            # Tips and sample videos to try
            st.markdown("### 💡 Don't have a video? Try these!")
            
            st.markdown("""
            **Quick ideas:**
            1. 📱 **Record on your phone** - 10-20 seconds of:
               - Street scene with cars
               - People walking
               - Your desk (laptop, phone, bottle)
               - Living room (TV, couch, chair)
            
            2. 🌐 **Download free stock videos:**
               - [Pexels Videos](https://www.pexels.com/videos/) - Search "traffic" or "people"
               - [Pixabay Videos](https://pixabay.com/videos/) - Search "street" or "crowd"
            
            3. 🎥 **Use existing videos:**
               - Any video from your phone's gallery
               - Dashcam footage
               - Security camera clips
            """)
    
    with tab3:
        st.markdown("### 🎯 About This Project")
        
        st.markdown("""
        ## Real-Time Object Detection System
        
        A production-ready computer vision application that detects objects in videos with high accuracy.
        
        ### ✨ Features
        
        - **🎯 80+ Object Classes** - Detects people, vehicles, animals, electronics, furniture, and more
        - **📊 Real-Time Analytics** - Live statistics and object counting
        - **🔔 Smart Alerts** - Get notified when specific objects appear
        - **⚡ Fast Processing** - Optimized for speed and accuracy
        - **💾 Storage Efficient** - 99.7% less storage than traditional video recording
        - **🌐 Web-Based** - No installation needed to try the demo
        
        ### 🔧 Technology Stack
        
        - **YOLOv8** - State-of-the-art object detection model
        - **OpenCV** - Computer vision library for video processing
        - **Streamlit** - Interactive web dashboard
        - **Python** - Core programming language
        
        ### 📈 How It Works
        
        ```
        Video Input → Frame Extraction → YOLOv8 Detection → 
        Object Identification → Bounding Boxes → Statistics → Alerts
        ```
        
        ### 🚀 Use Cases
        
        - 🏪 **Retail Analytics** - Customer counting, behavior tracking
        - 🚗 **Traffic Monitoring** - Vehicle counting, traffic analysis  
        - 🔒 **Security** - Person detection, intrusion alerts
        - 🏠 **Smart Home** - Package delivery detection, pet monitoring
        - 📊 **Research** - Computer vision studies, dataset analysis
        
        ### 💻 Run Locally for Full Features
        
        For webcam access and advanced features:
        
        ```bash
        # Clone the repository
        git clone https://github.com/Abhijeet0Kaushik/object-detection-system.git
        
        # Navigate to directory
        cd object-detection-system
        
        # Install dependencies
        pip install -r requirements.txt
        
        # Run the application
        python app.py          # CLI version
        streamlit run dashboard.py  # Web dashboard
        ```
        
        ### 📂 Source Code
        
        Full source code available on GitHub:  
        **[github.com/Abhijeet0Kaushik/object-detection-system](https://github.com/Abhijeet0Kaushik/object-detection-system)**
        
        ⭐ Star the repo if you find it useful!
        
        ### 👨‍💻 Built By
        
        **Abhijeet Kaushik**
        
        - 🌐 GitHub: [@Abhijeet0Kaushik](https://github.com/Abhijeet0Kaushik)
        - 💼 LinkedIn: [Add your LinkedIn URL]
        - 📧 Email: [Add your email]
        
        ---
        
        ### 📄 License
        
        This project is open source and available under the MIT License.
        
        ### 🙏 Acknowledgments
        
        - Ultralytics team for YOLOv8
        - OpenCV contributors
        - Streamlit team
        """)


if __name__ == "__main__":
    main()
