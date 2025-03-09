import cv2
import torch
import os
from datetime import datetime
from ultralytics import YOLO
import threading
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Load custom-trained YOLO model (Replace 'best.pt' with your model)
model = YOLO("runs/detect/train4/weights/best.pt")  # Use custom-trained model for broken screens

# Create folder to save detected images
save_folder = "detected_defects"
os.makedirs(save_folder, exist_ok=True)

# Define defect labels (Modify based on custom training)
DEFECT_CLASSES = {
    0: "Scratch",
    1: "Oil",
    2: "stain"
}

scanning = False  # Scanning flag
cap = cv2.VideoCapture(0)  # Open camera

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# GUI Window
root = tk.Tk()
root.title("Mobile Defect Scanner")

# Display Camera Feed
label = Label(root)
label.pack()

def start_scanning():
    global scanning
    scanning = True
    print("Scanning started.")

def stop_scanning():
    global scanning
    scanning = False
    print("Scanning stopped.")

def update_frame():
    """ Continuously updates the camera feed and detects defects if scanning is enabled """
    global scanning

    ret, frame = cap.read()
    if not ret:
        return

    display_frame = frame.copy()
    defect_detected = False

    if scanning:
        results = model(frame)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                confidence = box.conf[0].item()  # Confidence score
                class_id = int(box.cls[0])  # Class ID
                
                if class_id in DEFECT_CLASSES and confidence > 0.6:  # Adjust threshold to 0.6 for better accuracy
                    defect_type = DEFECT_CLASSES[class_id]
                    color = (0, 255, 0) if defect_type == "Scratch" else (0, 0, 255)  # Green for scratch, Red for others
                    
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(display_frame, f"{defect_type} {confidence:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    defect_detected = True

        # If defect is detected, save image with boxes
        if defect_detected:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(save_folder, f"defect_{timestamp}.jpg")
            cv2.imwrite(image_path, display_frame)  # Save processed frame with bounding boxes
            print(f"Defect detected! Image saved at: {image_path}")

    # Convert OpenCV image to Tkinter format
    frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)

    label.imgtk = imgtk
    label.configure(image=imgtk)
    root.after(10, update_frame)  # Repeat after 10ms

# Start and Stop Buttons
btn_start = tk.Button(root, text="Start Scanning", command=start_scanning, font=("Arial", 12), bg="green", fg="white")
btn_start.pack(pady=10)

btn_stop = tk.Button(root, text="Stop Scanning", command=stop_scanning, font=("Arial", 12), bg="red", fg="white")
btn_stop.pack(pady=10)

# Start camera feed update loop
update_frame()

# Run the Tkinter GUI
root.mainloop()

# Release resources when GUI closes
cap.release()
cv2.destroyAllWindows()
