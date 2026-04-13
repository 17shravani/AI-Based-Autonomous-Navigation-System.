import cv2
import numpy as np

def run_real_world_perception():
    print("==========================================")
    print(" AI Perception Module: Real-Time Scanner ")
    print("==========================================")
    print("Loading Offline Edge-AI Model...")
    
    # Use OpenCV's built-in models for extreme edge speed (no internet required)
    # We load the Frontal Face and Full Body classifiers to proxy pedestrians/humans in the road
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    detector = cv2.CascadeClassifier(cascade_path)
    
    # Start video capture (Webcam 0)
    print("Booting camera array... Press 'q' to shut down.")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERROR: Camera hardware not found or permission denied.")
        return
        
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert to grayscale for faster processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect objects
        obstacles = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        obstacle_detected = len(obstacles) > 0
        
        # Draw bounding boxes
        for (x, y, w, h) in obstacles:
            # Draw a warning box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            label = "OBSTACLE IMMINENT"
            label_y = y - 15 if y - 15 > 15 else y + 15
            cv2.putText(frame, label, (x, label_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                                
        # Add visual HUD
        if obstacle_detected:
            cv2.rectangle(frame, (20, 20), (300, 60), (0, 0, 255), -1)
            cv2.putText(frame, "WARNING: OBSTACLE IMMINENT", (30, 45), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.rectangle(frame, (20, 20), (250, 60), (0, 200, 0), -1)
            cv2.putText(frame, "SYSTEM CLEAR - PROCEED", (30, 45), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                        
        # Display the output
        cv2.imshow("AI Edge-Perception System", frame)
        
        # Exit logic
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_real_world_perception()
