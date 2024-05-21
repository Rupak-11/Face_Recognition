import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta
import subprocess

# Directory containing images
path = 'Imgbasics'
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)

# Function to encode faces
def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Function to mark attendance
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.strip().split(',')
            nameList.append(entry[0])

        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')

        if name == "Unknown":
            f.writelines(f'\n{name},{dtString}')
        elif name not in nameList:
            f.writelines(f'\n{name},{dtString}')

# Function to run csv_to_mongodb.py script
def run_csv_to_mongodb():
    subprocess.run(['python', 'csv_to_mongodb.py'])

# Find encodings for known faces
encodeListKnown = findEncoding(images)
print('Encoding Complete')

# Initialize webcam
cap = cv2.VideoCapture(0)
last_run_time = datetime.now() - timedelta(seconds=4)  # Initialize to ensure the first run happens

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurrentFrame)

    face_detected = False  # Flag to check if any face is detected

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            markAttendance(name)
            face_detected = True
        else:
            name = "UNKNOWN"
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            markAttendance(name)
            face_detected = True

    # Run the script if a face is detected and 4 seconds have passed since the last run
    if face_detected and (datetime.now() - last_run_time).seconds >= 4:
        run_csv_to_mongodb()
        last_run_time = datetime.now()

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
