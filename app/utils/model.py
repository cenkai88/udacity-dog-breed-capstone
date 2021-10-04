import os
import json
import cv2
import pandas as pd
import numpy  as np
import io
from PIL import Image

from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.preprocessing import image

from utils.extract_bottleneck_features import extract_Resnet50

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

face_cascade = cv2.CascadeClassifier(DIR_PATH+'/../../haarcascades/haarcascade_frontalface_alt.xml')

with open(DIR_PATH+"/dog_names.json", "r") as f:
    dog_names = json.load(f)

bottleneck_features = np.load(DIR_PATH+'/../../bottleneck_features/DogResnet50Data.npz')
train_Resnet50 = bottleneck_features['train']

# define ResNet50 model
ResNet50_model = ResNet50(weights='imagenet')
Resnet50_model = Sequential()
Resnet50_model.add(GlobalAveragePooling2D(input_shape=train_Resnet50.shape[1:]))
Resnet50_model.add(Dense(133, activation='softmax'))

# load the model
Resnet50_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
Resnet50_model.load_weights(DIR_PATH+'/../../saved_models/weights.best.Resnet50.hdf5')

def path_to_tensor(bytes):
    """
    Parameter:
    bytes: the bytes of the image
    
    Returns:
    a 4D tensor with shape (1, 224, 224, 3) suitable for supplying to a Keras CNN
    """
    rawImage = Image.open(io.BytesIO(bytes))
    # loads RGB image as PIL.Image.Image type
    # img = image.load_img(rawImage, target_size=(224, 224))
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    img = rawImage.convert('RGB')
    img = img.resize((224, 224), Image.NEAREST)
    img = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    return np.expand_dims(img, axis=0)

def ResNet50_predict_labels(bytes):
    """
    Parameter:
    bytes: the bytes of the image
    
    Returns:
    Prediction vector for image
    """
    img = preprocess_input(path_to_tensor(bytes))
    return np.argmax(ResNet50_model.predict(img))

def face_detector(bytes):
    """
    Parameter:
    bytes: the bytes of the image
    
    Returns:
    Whether a face is detected in the image
    """
    rawImage = Image.open(io.BytesIO(bytes))
    gray = cv2.cvtColor(np.asarray(rawImage), cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return len(faces) > 0

def dog_detector(bytes):
    """
    Parameter:
    bytes: the bytes of the image
    
    Returns:
    Whether a dog is detected in the image
    """
    prediction = ResNet50_predict_labels(bytes)
    return ((prediction <= 268) & (prediction >= 151))

def dog_breed_pred(bytes):
    """
    Parameter:
    bytes: the bytes of the image
    
    Returns:
    Name of dog breed predicted
    """
    bottleneck_feature = extract_Resnet50(path_to_tensor(bytes))
    predicted_vector = Resnet50_model.predict(bottleneck_feature)
    return dog_names[np.argmax(predicted_vector)]

def image_predictor(bytes):
    """
    This function return the result of the dog/human and breed classification of input image

    Parameter:
    bytes: the bytes of the image user wants to identify dog breed
    
    Returns:
    A text message of result
    """
    if dog_detector(bytes) == 1:
        return "This image looks like a dog. And the breed is: " + dog_breed_pred(bytes)
    elif face_detector(bytes) == 1:
        return "This image looks like a human and it's like: "+ dog_breed_pred(bytes)
    else:
        return "This image is not dog or human."