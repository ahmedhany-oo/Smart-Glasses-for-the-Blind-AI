# Smart Glasses for the Blind AI

A smart glasses project that uses Computer Vision and AI to help visually impaired people recognize objects around them through real-time voice feedback.

---

## Project Overview

The idea behind this project is to give visually impaired people a simple way to understand what's around them.

An ESP32-CAM captures live video and sends it to a Python application. A YOLO model processes each frame, detects nearby objects, and converts the detected object names into speech so the user receives instant audio feedback.

This project was developed as a team project, and I worked as the team leader. I participated in planning, testing, integrating the different modules, and contributed to both the AI and software development.

---

## Technologies

- Python
- YOLO
- OpenCV
- Flask
- ESP32-CAM
- pyttsx3

---

## Hardware Components

- ESP32-CAM
- Bluetooth Audio Receiver (VHM-314)
- TP4056 Charging Module
- MT3608 Boost Converter
- 3.7V Li-ion Battery

---

## Features

- Real-time object detection
- Live camera streaming
- Voice feedback
- Automatic camera reconnection
- Image capture support

---

## Project Images
### Final Prototype

![Final Glasses](images/Final%20glasses.png)

### System Overview

| Hardware | Block Diagram |
|----------|---------------|
| ![](images/System%20Hardware.png) | ![](images/Project%20Block-diagram.png) |

### Object Detection

| Detection 1 | Detection 2 |
|------------|-------------|
| ![](images/Object%10Detection.png) | ![](images/Object%20Detection%202.png) |

### Final Results 

![](images/Final%20Results.png)


## Challenges

During this project, one of the biggest challenges was integrating the AI model with the hardware while keeping the system responsive. We also worked on reducing camera disconnections and improving the overall detection experience.

---

## What I Learned

This project helped me gain practical experience with Computer Vision, object detection using YOLO, Flask, embedded systems integration, and working as part of a team to build a complete AI application.

---

## Future Improvements

- Face recognition
- OCR for reading text
- Currency recognition
- GPS navigation
- Mobile application
