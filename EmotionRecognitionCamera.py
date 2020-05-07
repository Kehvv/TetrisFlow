#!/usr/bin/env python
# coding: utf-8

# In[77]:


import numpy as np
import cv2
from keras.preprocessing import image


# In[78]:


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# In[79]:


from keras.models import model_from_json ##load model created earlier
model = model_from_json(open("facial_expression_model_structure.json", "r").read())
model.load_weights('facial_expression_model_weights.h5')


# In[80]:


emotion_category = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral') ## defining the emotion categories


# In[81]:


cameraCap = cv2.VideoCapture(0) ## using the built in open cv video capture using webcam
frame = 0


while(True): ## continuously read the frames of the video like an image
    
    ret, capRead = cameraCap.read() ## ret returns 1 if video captured
    capRead = cv2.resize(capRead, (640, 360)) ##resize captured video to this dimension
    capRead = capRead[0:308,:] 
    vidBW = cv2.cvtColor(capRead, cv2.COLOR_BGR2GRAY) ##convert loaded video frame to grayscale
    faces = face_cascade.detectMultiScale(vidBW, 1.3, 5) ##detect face in loaded gray frame using cascade classifier provided by OpenCV

    for (xpos,ypos,w,h) in faces:
        if w > 130: ## only detect images over this width
            cv2.rectangle(capRead,(xpos,ypos),(xpos+w,ypos+h),(0,255,0),2) ##draw rectangle around detected face using coordinates
            
            face_detected = capRead[int(ypos):int(ypos+h), int(xpos):int(xpos+w)] ##convert coordinates to int
            face_detected = cv2.cvtColor(face_detected, cv2.COLOR_BGR2GRAY) ##convert to grayscale
            face_detected = cv2.resize(face_detected, (48, 48)) ##must resize to 48x48 pixels

            img_pixels = image.img_to_array(face_detected) ## add to array
            img_pixels = np.expand_dims(img_pixels, axis = 0) ##expand the dimensions
            img_pixels /= 255 ##normalise 

            predict = model.predict(img_pixels) ##storing predictions of each emotion
            top_emotion = np.argmax(predict[0]) ##take highest probability prediction

            overlay = capRead.copy() ##overlay to store prediction text
            opacity = 0.7 
            
            cv2.rectangle(capRead,(xpos+w+10,ypos-25),(xpos+w+150,ypos+115),(64,64,64),cv2.FILLED) ##adds an offset rectangle to show emotion list
            cv2.addWeighted(overlay, opacity, capRead, 1 - opacity, 0, capRead) 
            cv2.line(capRead,(int((xpos+xpos+w)/2),ypos+15),(xpos+w,ypos-20),(255,255,255),1) ##line that points to detected face
            cv2.line(capRead,(xpos+w,ypos-20),(xpos+w+10,ypos-20),(255,255,255),1)
            emotion = "" ##initialise as blank string
            
            for i in range(len(predict[0])): 
                emotion = "%s %s%s" % (emotion_category[i], round(predict[0][i]*100, 2), '%') ##output emotion and prediction percentage
                color = (255,255,255)
                cv2.putText(capRead, emotion, (int(xpos+w+15), int(ypos-12+i*20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1) ## image display
                
                with open('emotion.txt', 'w') as f:
                      f.write(str(top_emotion))   

    cv2.imshow('TetrisFlow Capture',capRead)
    frame = frame + 1 ##continuously increasing frame
    if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
        break

cameraCap.release()
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:





# In[ ]:




