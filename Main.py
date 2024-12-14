import cv2
import torch
import threading
import serial
import time
 
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
ser = serial.Serial('COM3', 9600) 

def detect_and_count_live(video_source, classes_to_detect):
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print(f"Error: Unable to open video source {video_source}")
        return

    while True:
         
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to retrieve frame from source:", video_source)
            break

         
        if frame is None or frame.size == 0:
            print("Empty frame received.")
            continue

         
        results = model(frame)
        people_count, vehicle_count = 0, 0

         
        if results and hasattr(results, 'xyxy'):
            for det in results.xyxy[0]:   
                 
                x1, y1, x2, y2 = map(int, det[:4])
                conf = det[4].item()
                cls = int(det[5].item())
                label = model.names[cls]

                if label in classes_to_detect:
                    if label == 'person':
                        color = (0, 255, 0)   
                        people_count += 1
                    else:
                        color = (255, 0, 0)   
                        vehicle_count += 1

                     
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
         
        cv2.putText(frame, f"People Count: {people_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Vehicle Count: {vehicle_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

         
        cv2.imshow(f"Live Detection - Source {video_source}", frame)

         
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print("People : ",people_count,"Vehicle : ", vehicle_count)

        ser.write(f"{people_count},{vehicle_count}\n".encode())
        time.sleep(0.3)
        
    cap.release()
    cv2.destroyAllWindows()

 
laptop_camera = 0   
droidcam_url = 1  

 
laptop_thread = threading.Thread(target=detect_and_count_live, args=(laptop_camera, ['person', 'car', 'truck', 'bus', 'motorbike']))
droidcam_thread = threading.Thread(target=detect_and_count_live, args=(droidcam_url, ['person', 'car', 'truck', 'bus', 'motorbike']))


 
laptop_thread.start()
droidcam_thread.start()

 
laptop_thread.join()
droidcam_thread.join()
