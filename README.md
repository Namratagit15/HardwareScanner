# HardwareScanner
This project is a AI-powered hardware Scanner designed to detect manufacturing defects such as scratches, oil marks, and stains on mobile hardware using YOLO (You Only Look Once) object detection model. The application uses a live camera feed to capture images and identify defects in real-time.
🚀 Features
•	Real-time defect detection for mobile hardware.
•	Detects defects like Scratches, Oil, and Stains.
•	Captures and saves images with defects.
•	Provides a simple GUI to start/stop scanning.
•	Automatically saves detected defect images in a folder.

📂 Folder Structure
|-- detected_defects/       # Contains images of detected defects
|-- scanner.py              # Main application file

💻 Requirements
•	Python 3.8+
•	Torch and torchvision
•	Ultralytics YOLOv8
•	OpenCV
•	PIL (Pillow)
•	Tkinter

📜 Installation
1.	Clone the repository:
git clone https://github.com/Namratagit15/HardwareScanner.git
cd HardwareScanner

2.	Install the required packages:
pip install torch torchvision ultralytics opencv-python pillow tkinter

3.	Place your custom YOLO model (best.pt) in the path:
runs/detect/train4/weights/best.pt

4.	Run the application:
python scanner.py

🎥 How to Use
1.	Open the application by running scanner.py.
2.	The camera feed will open in a new window.
3.	Click "Start Scanning" to start detecting defects.
4.	If any defect is detected, a bounding box with a label will appear.
5.	The image with detected defects will be automatically saved in the detected_defects folder.
6.	Click "Stop Scanning" to stop the detection.

💾 Output
•	All images with detected defects are saved in the detected_defects folder.
•	The filename format is: defect_YYYYMMDD_HHMMSS.jpg.

📊 Defect Classes

•	The model is trained to detect the following defects:

Class ID	Defect Type
0	Scratch
1	Oil
2	Stain

📷 Camera Settings
•	The application uses the default camera (cv2.VideoCapture(0)).
•	If you want to use an external camera, modify this line:
cap = cv2.VideoCapture(1)

🛠 Model Configuration

The YOLO model path is configured in the code as:

model = YOLO("runs/detect/train4/weights/best.pt")
If you have a different model path, update the line accordingly.

✅ Notes
•	Ensure the camera has good lighting for better defect detection.
•	You can adjust the confidence threshold in the code:
if class_id in DEFECT_CLASSES and confidence > 0.6:
•	You can add more defect classes by extending the DEFECT_CLASSES dictionary.

          📜 License
•	This project is open-source and free to use under the MIT License.

💡 Future Improvements
•	✅ Add support for more defect classes.
•	✅ Generate a detailed defect report.
✅ Implement automatic report generation.
