#!/usr/bin/env python
# coding: utf-8

# In[1]:


##https://towardsdatascience.com/building-a-convolutional-neural-network-cnn-in-keras-329fbbadc5f5
##https://www.udemy.com/course/deep-learning-and-computer-vision/
##https://medium.com/technologymadeeasy/the-best-explanation-of-convolutional-neural-networks-on-the-internet-fbb8b1ad5df8

import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras.layers import Dense, Activation, Dropout, Flatten

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import numpy as np


# In[3]:


num_classes = 7 #the dataset fer2013 has 7 classes for various emotions
batch_size = 256 # number of batches taken at each forward and backward pass
epochs = 5 #number of epochs. 1 epoch is 1 forward and 1 backwards pass


# In[4]:


#Store dataset in numpy array
with open ('fer2013.csv') as f: 
    content = f.readlines()
    
lines = np.array(content)


# In[5]:


numInstances = lines.size
print('instances :', numInstances)


# In[6]:


import pandas as pd


# In[7]:


dataset = pd.read_csv('fer2013.csv') #use pandas to read and store the dataset


# In[8]:


dataset.head()


# In[9]:


x_train, y_train, x_test, y_test = [], [], [], []


# In[10]:


for i in range(1, numInstances): # loop from 1 to number of instances in dataset
    try: #try catch
        emotion, image, usage = lines[i].split(",") #split dataset by comma (csv file)
        imgval = image.split(" ") #remove white space
        
        pixels = np.array(imgval, 'float32') #convert image pixels to float32 as expected by CNN
        
        emotion = keras.utils.to_categorical(emotion, num_classes) #stores the emotion value as a binary matrix
        
        if 'Training' in usage: #filter values marked as training
            y_train.append(emotion) #add emotion value as y train
            x_train.append(pixels) #add image pixel value as x train
        elif 'PublicTest' in usage: #filter values marked as testing
            y_test.append(emotion) #add emotion value as y test
            x_test.append(pixels) #add image pixel value as x test
    except:
        print("", end="")


# In[11]:


##converting all values to float32 as expected by CNN

x_train = np.array(x_train, 'float32')
y_train = np.array(y_train, 'float32')
x_test = np.array(x_test, 'float32')
y_test = np.array(y_test, 'float32')


# In[12]:


## pixel range is from 0 to 255. Must divide by 255 to get correct format for CNN
x_train /= 255 
x_test /= 255


# In[13]:


#model expects 48 x 48 pixels grey scale
#reshaping x_train into 48 x 48 pixels with 1 colour channel(black & white)
x_train = x_train.reshape(x_train.shape[0], 48,48, 1) 
x_train = x_train.astype('float32') #converting back to float32

x_test = x_test.reshape(x_test.shape[0], 48,48, 1) 
x_test = x_test.astype('float32') #converting back to float32


# In[14]:


#test to output the number of train and test samples before proceeding
#don't want to accidentally proceed with no samples!

print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')


# In[15]:


#### constructing the CNN ####

model = Sequential()
## add convolutional layer ##

## add Conv2D layer with activation type relu (rectified linear unit) and input shape 48x48 with 1 colour channel

## input shape required as first layer in model
model.add(Conv2D(64, (5,5), activation = 'relu', input_shape=(48,48,1)))

## add pooling layer ##
## pooling used to downsample and reduce computation times

## add MaxPooling2D layer, size corresponding to convolutional layer, with strides of 2 pixels
model.add(MaxPooling2D(pool_size = (5,5), strides= (2,2)))

##add more convolutional layers (this time no input shape required)

model.add(Conv2D(64, (3,3), activation='relu'))
model.add(Conv2D(64, (3,3), activation='relu'))

##add another pooling layer - this time average pool

model.add(AveragePooling2D(pool_size = (3,3), strides= (2,2)))

##add another 2 convolutional layers

model.add(Conv2D(128, (3,3), activation='relu'))
model.add(Conv2D(128, (3,3), activation='relu'))

##add another average pooling layer

model.add(AveragePooling2D(pool_size = (3,3), strides= (2,2)))

##add flatten layer

model.add(Flatten())

## add dense layer

model.add(Dense(1024, activation = 'relu'))
##add dropout layer
model.add(Dropout(0.2))

##add another hidden layers

model.add(Dense(1024, activation = 'relu'))
model.add(Dropout(0.2))

##final dense layer
model.add(Dense(num_classes, activation = 'softmax'))


# In[16]:


gen = ImageDataGenerator()

train_generator = gen.flow(x_train, y_train, batch_size = batch_size)


# In[17]:


model.compile(loss = 'categorical_crossentropy',
              optimizer = keras.optimizers.Adam(),
              metrics = ['accuracy'])


# In[18]:


model.fit_generator(train_generator, 
                    steps_per_epoch = batch_size, 
                    epochs = epochs)

##saving model weiights and structure to file

model_json = model.to_json()
with open('facial_expression_model_structure.json', 'w') as json_file:
    json_file.write(model_json)
    
model.save_weights('facial_expression_model_weights.h5')

print('Model saved!')


# In[ ]:





# In[ ]:




