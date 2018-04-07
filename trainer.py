import os
import cv2
import numpy as np
from PIL import Image

rec = cv2.face.createLBPHFaceRecognizer()
path='dataSet'

def getImagesWithId(path):
    imagesPath = [os.path.join(path,f) for f in os.listdir(path)]
    faces = []
    IDs =[]

    for imagePath in imagesPath:
        faceImage = Image.open(imagePath).convert('L')
        faceNp = np.array( faceImage,'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow('training',faceNp)
    return np.array(IDs),faces

Ids,faces = getImagesWithId(path)
rec.train(faces,np.array(Ids))
rec.save('recognizer/traindata.yml')
cv2.destroyAllWindows()
