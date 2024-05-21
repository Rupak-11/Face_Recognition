import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'Imgbasics'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)

def findEncoding(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

def markAttendance(name):
    with open('Attendance.csv' , 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])

if name not in nameList:
    from datetime import datetime
    now = datetime.now()
    dtString = now.strftime('%H:%M:%S')
    with open('yourfile.txt', 'a') as f:
        f.writelines(f'\n{name},{dtString}')

markAttendance('Rupak')
      


encodeListKnown = findEncoding(images)
# print(len(encodeListKnown))
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0) , None , 0.25 ,0.25)
    imgS = cv2.cvtColor(imgS , cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS , facesCurrentFrame)

    for encodeFace , faceLoc in zip(encodesCurFrame,facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown , encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown , encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches [matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1 , x2 , y2 , x1 = faceLoc
            y1 , x2 , y2 , x1 =  y1*4 , x2*4 , y2*4 , x1*4 
            
            cv2.rectangle(img , (x1 , y1) , (x2 , y2) , (0,255 ,0), 2)
            cv2.rectangle(img ,(x1 , y2-35) , (x2 , y2), (0,255,0), cv2.FILLED)
            cv2.putText(img ,name ,(x1+6 , y2-6), cv2.FONT_HERSHEY_COMPLEX , 1 ,(255 , 255 , 255) , 2 )


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Webcam' , img)
    cv2.waitKey(1)







# faceLoc = face_recognition.face_locations(imgElon)[0]
# encodeElon = face_recognition.face_encodings(imgElon)[0]
# cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 255, 0), 2)

# faceLocTest = face_recognition.face_locations(imgTest)[0]
# encodeTest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (0, 255, 0), 2)

# results = face_recognition.compare_faces([encodeElon], encodeTest)
# facedis = face_recognition.face_distance([encodeElon] , encodeTest)
# facedis = face_recognition.face_distance([encodeElon] , encodeTest)


# imgElon = face_recognition.load_image_file('Imgbasics/ElonMusk.jpg')
# imgElon = cv2.cvtColor(imgElon , cv2.COLOR_BGR2RGB)
# imgBill = face_recognition.load_image_file('Imgbasics/Billo.jpg')
# imgBill = cv2.cvtColor(imgBill , cv2.COLOR_BGR2RGB)
# imgAkash = face_recognition.load_image_file('Imgbasics/Akash.jpg')
# imgAkash = cv2.cvtColor(imgAkash , cv2.COLOR_BGR2RGB)
