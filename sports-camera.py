import cv2
import serial
import collections
import threading
import time
import os
import imageio
from datetime import datetime

CAMERA_INDEX = 0
BUFFER_SECONDS = 30
FPS = 30
SERIAL_PORT = "COM3" 
RESOLUTION = (1280, 720)
OUTPUT_FOLDER = "records"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

buffer = collections.deque(maxlen=BUFFER_SECONDS * FPS)
recording = False


def capture():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])
    cap.set(cv2.CAP_PROP_FPS, FPS)

    if not cap.isOpened():
        print(f"[ERROR] Camera {CAMERA_INDEX} not found. Try another index.")
        return

    print("Camera started. Buffer active.")

    while True:
        ok, frame = cap.read()
        if ok:
            buffer.append(frame.copy())
        time.sleep(1 / FPS)


def save_buffer():
    global recording

    if recording:
        print("[WARN] Recording already in progress, please wait.")
        return
    if len(buffer) < 10:
        print("[WARN] Buffer is empty or too small.")
        return

    recording = True
    frames = list(buffer)
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_FOLDER, f"{name}.mp4")

    print(f"Saving {len(frames)} frames to {path} …")

    try:
        writer = imageio.get_writer(
            path,
            fps=FPS,
            codec="libx264",
            quality=8,
            pixelformat="yuv420p",
            macro_block_size=None,
        )
        for frame in frames:
            writer.append_data(frame[:, :, ::-1]) 
        writer.close()
        print(f"Video saved: {path}")
    except Exception as e:
        print(f"[ERROR] Failed to save video: {e}")
    finally:
        recording = False


def listen_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
        print(f"🔌 Serial connected: {SERIAL_PORT}")
    except Exception as e:
        print(f"[ERROR] Could not open {SERIAL_PORT}: {e}")
        print("Check the port and close the Arduino IDE Serial Monitor.")
        return

    while True:
        try:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if line in ("SAVE", "SALVAR"):
                threading.Thread(target=save_buffer, daemon=True).start()
        except Exception as e:
            print(f"[ERROR] Serial: {e}")
            time.sleep(1)


if __name__ == "__main__":
    print("=== Sports Camera System ===")
    print()

    threading.Thread(target=capture, daemon=True).start()
    listen_serial()