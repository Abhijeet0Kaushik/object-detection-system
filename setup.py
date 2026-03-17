#!/usr/bin/env python3
"""
Setup script for Object Detection System
Automates installation and initial setup
"""

import subprocess
import sys
import os


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"⚙️  {description}...")
    try:
        subprocess.run(command, check=True, shell=True)
        print(f"✅ {description} completed\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}\n")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    # Upgrade pip
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    )
    
    # Install requirements
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt --break-system-packages",
        "Installing packages from requirements.txt"
    ):
        return False
    
    return True


def download_model():
    """Download YOLOv8 model"""
    print_header("Downloading YOLOv8 Model")
    
    print("📥 Downloading yolov8n.pt (smallest, fastest model)...")
    
    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")
        print("✅ Model downloaded successfully\n")
        return True
    except Exception as e:
        print(f"❌ Model download failed: {e}\n")
        return False


def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = ['logs', 'reports', 'screenshots']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    print()
    return True


def verify_installation():
    """Verify that everything is installed correctly"""
    print_header("Verifying Installation")
    
    required_packages = [
        'ultralytics',
        'cv2',
        'numpy',
        'pandas',
        'matplotlib',
        'streamlit'
    ]
    
    all_good = True
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT FOUND")
            all_good = False
    
    print()
    return all_good


def print_next_steps():
    """Print instructions for next steps"""
    print_header("Setup Complete!")
    
    print("🎉 Your object detection system is ready to use!\n")
    print("Next steps:\n")
    print("1. Run the CLI application:")
    print("   python app.py\n")
    print("2. Or start the web dashboard:")
    print("   streamlit run dashboard.py\n")
    print("3. Read the README for more options:")
    print("   cat README.md\n")
    print("Controls during detection:")
    print("  - Press 'q' to quit")
    print("  - Press 's' to toggle statistics\n")
    print("Logs will be saved to: logs/")
    print("Reports can be generated with: python -c 'from utils import DetectionAnalyzer; DetectionAnalyzer().generate_report()'\n")
    print("="*60 + "\n")


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  OBJECT DETECTION SYSTEM - SETUP")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Download model
    if not download_model():
        print("\n⚠️  Model download failed, but you can download it later")
        print("   The model will auto-download on first run")
    
    # Create directories
    create_directories()
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️  Some packages may not have installed correctly")
        print("   Try: pip install -r requirements.txt --break-system-packages")
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
