from flask import Flask, Response
import cv2
import torch
from ultralytics import YOLO
import pyttsx3  
import time
import threading  
import os
import keyboard  # Import keyboard module for key press detection

app = Flask(__name__)

model = YOLO("models/best.pt")  # Load YOLO model
# Replace with your ESP32-CAM stream URL
cap = cv2.VideoCapture("http://192.168.137.44:81/stream")  # Camera stream URL
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer size
cap.set(cv2.CAP_PROP_FPS, 25)  # Set FPS to 25 for better performance

last_detected_objects = set()
last_speak_time = 0  # Last time an object was spoken
speak_interval = 5  # Minimum time between repeated speech
photo_counter = 0  # Counter for saving photos

def reconnect_camera():
    global cap
    cap.release()
    time.sleep(2)
    cap = cv2.VideoCapture("http://192.168.1.8:81/stream")
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS, 25)
    print("🔄 Reconnecting to camera...")

def check_camera_connection():
    while True:
        time.sleep(5)
        if not cap.isOpened():
            print("⚠ Camera connection lost, attempting reconnect...")
            reconnect_camera()

threading.Thread(target=check_camera_connection, daemon=True).start()

@app.route('/')
def home():
    return "Server is running!"

def process_video():
    global last_detected_objects, last_speak_time, photo_counter
    frame_interval = 2

    while True:
        cap.grab()
        ret, frame = cap.retrieve()
        if not ret:
            print("⚠ Lost connection to camera, attempting reconnect...")
            reconnect_camera()
            continue  

        frame = cv2.resize(frame, (640, 480))  
        current_objects = set()
        object_detected = False  
        detected_names = []

        if int(time.time()) % frame_interval == 0:
            results = model(frame)

            for result in results:
                for box in result.boxes:
                    conf = box.conf[0].item() * 100
                    cls = int(box.cls[0].item())
                    label = f'{model.names[cls]}: {conf:.2f}%'
                    detected_names.append(model.names[cls])

                    if conf >= 50:
                        object_detected = True
                        current_objects.add(cls)

                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        if object_detected and (current_objects != last_detected_objects or time.time() - last_speak_time > speak_interval):
            print("🔊 Speaking...")
            threading.Thread(target=speak, args=(", ".join(detected_names),), daemon=True).start()
            last_speak_time = time.time()

        last_detected_objects = current_objects

        # Check if 'P' key is pressed to capture photo
        if keyboard.is_pressed('p'):
            capture_photo(frame)

        ret, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])  
        if not ret:
            continue  

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"❌ Error in TTS: {e}")

def capture_photo(frame):
    global photo_counter
    frame = cv2.resize(frame, (1280, 960))  # Resize image to larger size
    photo_filename = f'photo_{photo_counter}.jpg'
    cv2.imwrite(photo_filename, frame)
    print(f"📸 Photo saved as {photo_filename}")
    photo_counter += 1

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        cap.release()
        cv2.destroyAllWindows()
