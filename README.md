# Hand-Gesture-VFX-Project

A real-time computer vision project that uses hand gesture recognition to create Doctor Strange-style magic circle effects using OpenCV, MediaPipe, and Pygame.

---

## 🔥 Demo
<img width="798" height="576" alt="image" src="https://github.com/user-attachments/assets/58ed2e5d-0dc5-4c1a-93f8-75bcae74ccdf" />

<img width="794" height="589" alt="Screenshot 2026-04-20 153702" src="https://github.com/user-attachments/assets/cfaeb05d-3f91-4d6e-af70-f639e591b9e2" />



---

## 📌 Description

This project detects hand gestures using a webcam and overlays animated magic circle effects on your palm. It tracks 21 hand landmarks and calculates finger distances to identify gestures in real time.

- Semi-open hand → draws geometric lines  
- Fully open hand → displays rotating magic circles  

---

## ✨ Features

- Real-time hand tracking  
- Gesture-based interaction  
- Magic circle animation with rotation  
- Transparent image overlay  
- Background music integration  
- Smooth and lightweight execution  

---

## 🧠 How It Works

1. Captures webcam video using OpenCV  
2. Detects hand landmarks using MediaPipe  
3. Calculates distances between fingers  
4. Determines gesture using ratio logic  
5. Displays visual effects accordingly  

---

## 📁 Project Structure
Hand-Gesture-VFX-Project/
│
├── main.py
├── requirements.txt
├── README.md
├── hand_landmarker.task
├── bgm.mp3
│
├── magic_circles/
│ ├── magic_circle_cw.png
│ └── magic_circle_ccw.png
│
└── assets/
└── demo.gif


---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Pratikfating123/Hand-Gesture-VFX-Project
cd Hand-Gesture-VFX-Project
--------------------------------------
Step 2: Create Virtual Environment
python -m venv .venv
-------------------------------------
Step 3: Activate Virtual Environment
For Windows:
.venv\Scripts\activate

For Mac/Linux:
source .venv/bin/activate
--------------------------------------
Step 4: Install Dependencies
pip install -r requirements.txt
-------------------------------------
Step 5: Run the Project
python main.py
```
🧩 Requirements

opencv-python
mediapipe
pygame
numpy

🚀 Future Improvements

More gesture controls
Multiple visual effects
GUI interface
AR integration
