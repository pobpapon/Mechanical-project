# 🎯 Mechanical Project - RCWS Control System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Raspberry%20Pi-Supported-red.svg" alt="Raspberry Pi">
  <img src="https://img.shields.io/badge/Arduino-Compatible-00979D.svg" alt="Arduino">
  <img src="https://img.shields.io/badge/OpenCV-Enabled-green.svg" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

<p align="center">
  <strong>A distributed control system for Remote Controlled Weapon System (RCWS)</strong>
</p>

---

## 📋 Overview

This project implements a comprehensive software solution for controlling an RCWS (Remote Controlled Weapon System) using a distributed architecture across three platforms: PC, Raspberry Pi, and Arduino. The system provides real-time video processing, joystick control, and precise motor control for weapon platform positioning.

## 🏗️ System Architecture
```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│     PC      │◄────────┤ Raspberry Pi │────────►│   Arduino   │
│             │  Video  │              │ Serial  │             │
│ - Image     │         │ - Camera Hub │ Comm.   │ - Motor     │
│   Processing│         │ - Signal     │         │   Control   │
│ - Joystick  │────────►│   Relay      │         │ - Stepper   │
│   Input     │ Control │              │         │   Driver    │
└─────────────┘         └──────────────┘         └─────────────┘
```

## ✨ Features

- 🎮 **Real-time Joystick Control** - Responsive control input from PC
- 📹 **Dual Camera System** - Live video streaming from two cameras
- 🖼️ **Image Processing** - Real-time computer vision on PC
- 🔗 **Distributed Architecture** - Efficient task distribution across platforms
- ⚡ **Serial Communication** - Reliable Pi-Arduino communication
- 🎯 **Precise Motor Control** - Accurate stepper motor positioning

---

## 🖥️ Components Breakdown

### 1️⃣ PC Side
**Responsibilities:**
- Receives video streams from dual cameras via Raspberry Pi
- Performs real-time image processing using computer vision algorithms
- Reads and processes joystick input signals
- Sends control commands to Raspberry Pi

**Technologies:**
- Python
- OpenCV
- Joystick/Game Controller Library

### 2️⃣ Raspberry Pi Side
**Responsibilities:**
- Captures video from 2 cameras
- Streams video data to PC
- Receives joystick control signals from PC
- Transmits control commands to Arduino via serial communication
- Acts as communication hub between PC and Arduino

**Technologies:**
- Python
- PiCamera / USB Camera drivers
- Serial Communication (UART)
- Network Communication

### 3️⃣ Arduino Side
**Responsibilities:**
- Receives control signals from Raspberry Pi via serial communication
- Drives stepper motors based on received commands
- Controls weapon platform positioning
- Provides precise motor control

**Technologies:**
- Arduino C/C++
- Stepper Motor Drivers
- Serial Communication

---

## 🔧 Technologies Used

<table>
  <tr>
    <td align="center"><b>Platform</b></td>
    <td align="center"><b>Language</b></td>
    <td align="center"><b>Key Libraries</b></td>
  </tr>
  <tr>
    <td>PC</td>
    <td>Python</td>
    <td>OpenCV, PyGame, Socket</td>
  </tr>
  <tr>
    <td>Raspberry Pi</td>
    <td>Python</td>
    <td>PiCamera, Serial, Socket</td>
  </tr>
  <tr>
    <td>Arduino</td>
    <td>C/C++</td>
    <td>Stepper, Serial</td>
  </tr>
</table>

---

## 📦 Installation

### PC Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/Mechanical-project.git
cd Mechanical-project/pc-side

# Install dependencies
pip install -r requirements.txt
```

### Raspberry Pi Setup
```bash
# Navigate to Pi directory
cd raspberry-pi-side

# Install dependencies
pip install -r requirements.txt

# Configure camera
sudo raspi-config
# Enable Camera Interface
```

### Arduino Setup
```bash
# Open Arduino IDE
# Load the arduino-side/arduino-side.ino file
# Select your Arduino board and port
# Upload the sketch
```

---

## 🚀 Usage

1. **Start Arduino**
   - Connect Arduino to Raspberry Pi via USB
   - Ensure serial communication is established

2. **Start Raspberry Pi**
```bash
   python3 pi_main.py
```

3. **Start PC**
```bash
   python pc_main.py
```

4. **Connect Joystick**
   - Plug in your joystick/game controller to PC
   - Calibrate if necessary

5. **Operate System**
   - View dual camera feeds on PC
   - Control RCWS using joystick
   - Monitor real-time image processing

---

## 📁 Project Structure
```
Mechanical-project/
│
├── pc-side/
│   ├── pc_main.py
│   ├── image_processing.py
│   ├── joystick_handler.py
│   └── requirements.txt
│
├── raspberry-pi-side/
│   ├── pi_main.py
│   ├── camera_handler.py
│   ├── serial_comm.py
│   └── requirements.txt
│
├── arduino-side/
│   ├── arduino_main.ino
│   ├── motor_control.h
│   └── serial_handler.h
│
└── README.md
```

---

## 🔌 Wiring Diagram

> Add your wiring diagram image here
```markdown
![Wiring Diagram](path/to/wiring-diagram.png)
```

---

## 🎥 Demo

> Add demo video or GIF here
```markdown
![Demo](path/to/demo.gif)
```

---

## ⚙️ Configuration

<details>
<summary>Click to expand configuration options</summary>

### PC Configuration
- Video resolution: 1920x1080
- Processing FPS: 30
- Joystick sensitivity: Adjustable

### Pi Configuration
- Camera 1: Front view
- Camera 2: Side view
- Serial baud rate: 115200

### Arduino Configuration
- Motor steps per revolution: 200
- Microstepping: 1/16
- Serial baud rate: 115200

</details>

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No camera feed | Check camera connections and permissions |
| Joystick not detected | Verify USB connection and drivers |
| Serial communication error | Check baud rate and port settings |
| Motors not responding | Verify power supply and wiring |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**

- GitHub: [@pobpapon99](https://github.com/pobpapon99)
- Email: pobpapon99@gmail.com

---

## 🙏 Acknowledgments

- Thanks to the OpenCV community
- Raspberry Pi Foundation
- Arduino community

---

<p align="center">
  Made with ❤️ for robotics enthusiasts
</p>

<p align="center">
  ⭐ Star this repo if you find it helpful!
</p>
