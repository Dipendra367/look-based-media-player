# 👁️ Look Based Media Player

A Python-based media player that automatically pauses when you look away from the screen and resumes playback when you look back — using real-time face detection via webcam.

## 🎯 Features

- 🎬 Plays all major media formats (MP4, MKV, AVI, MOV, MP3, WAV, FLAC)
- 👤 Real-time face detection using webcam
- ⏸️ Auto-pauses when user looks away
- ▶️ Auto-resumes when user looks back
- ⏩ Forward / Backward 10 second skip
- 📊 Progress bar with seek support
- 🎨 Clean dark-themed UI

## 🛠️ Tech Stack

- **Python 3.10**
- **OpenCV** — face detection
- **python-vlc** — media playback
- **PyQt5** — GUI

## ⚙️ Installation

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/look-based-media-player.git
cd look-based-media-player
```

**2. Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Install VLC (Linux)**
```bash
sudo apt install vlc -y
```

**5. Run**
```bash
python main.py
```

## 📁 Project Structure
look-based-media-player/
├── main.py            # Main GUI application
├── face_detector.py   # Webcam face detection module
├── media_player.py    # VLC media player module
├── requirements.txt   # Dependencies
└── assets/            # Icons and resources

## 🚀 How It Works

1. Webcam continuously monitors for user's face every 400ms
2. If face is detected → media plays
3. If face is not detected → media pauses automatically
4. User can skip forward/backward and seek via progress bar

## ⚠️ Known Limitation

Manual pause is not supported — playback is entirely controlled by face detection.
