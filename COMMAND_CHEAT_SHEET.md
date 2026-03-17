# ⚡ COMMAND CHEAT SHEET - Copy & Paste These!

## 🎯 The ONLY Commands You Need

---

### ✅ Step 1: Open PowerShell

1. Go to: `C:\Users\abhij\Desktop\object-detection-system`
2. **Shift + Right-click** in the folder
3. Click **"Open PowerShell window here"**

---

### ✅ Step 2: Install (ONE TIME ONLY)

**Copy-paste this:**

```powershell
pip install ultralytics opencv-python pandas matplotlib streamlit pillow
```

**Wait 2-3 minutes.** When done, you'll see "Successfully installed..."

---

### ✅ Step 3: Test It Works

**Copy-paste this:**

```powershell
python demo.py
```

**✅ If you see demo windows = IT WORKS!**

---

### ✅ Step 4: Run the Real App

**Choose ONE:**

#### Option A: Webcam Detection (Command Line)
```powershell
python app.py
```
Press `q` to quit, `s` for stats

#### Option B: Web Dashboard (Browser)
```powershell
streamlit run dashboard.py
```
Opens automatically in your browser

---

### 📸 Bonus: Create Portfolio Images

```powershell
python generate_screenshots.py
```

Creates 5 images in `screenshots/` folder

---

## 🚀 That's Literally It!

**Just 3 commands:**
1. Install stuff (one time)
2. Test it (demo.py)
3. Run it (app.py or dashboard.py)

---

## 🐛 If You Get Errors

### "pip is not recognized"
```powershell
python -m pip install ultralytics opencv-python pandas matplotlib streamlit pillow
```

### "python is not recognized"
Install Python from: https://www.python.org/downloads/
✅ Check "Add Python to PATH" during install

### "No module named 'cv2'"
```powershell
pip install opencv-python --force-reinstall
```

---

## 📋 Quick Reference

| Command | What It Does |
|---------|-------------|
| `python demo.py` | Test (no webcam) |
| `python app.py` | CLI with webcam |
| `streamlit run dashboard.py` | Web interface |
| `python generate_screenshots.py` | Make images |
| `python setup.py` | Alternative installer |

---

## ✅ Success Checklist

- [ ] Folder created: `C:\Users\abhij\Desktop\object-detection-system`
- [ ] All files in that folder
- [ ] PowerShell opened in that folder
- [ ] Ran install command
- [ ] Ran `python demo.py` - WORKS! ✅
- [ ] Ran app or dashboard - WORKS! ✅

---

**🎉 You're Done! That's All You Need!**

For more details → READ_ME_FIRST.md
