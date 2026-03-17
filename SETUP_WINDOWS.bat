@echo off
echo ================================================
echo Object Detection System - Quick Setup
echo ================================================
echo.

echo Step 1: Installing dependencies...
pip install ultralytics opencv-python pandas matplotlib streamlit pillow --break-system-packages
echo.

echo Step 2: Testing installation...
python demo.py
echo.

echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo   1. Run: python app.py (for webcam detection)
echo   2. Run: streamlit run dashboard.py (for web interface)
echo   3. Run: python generate_screenshots.py (for portfolio images)
echo.
echo Press any key to exit...
pause > nul
