import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, BatchNormalization, Concatenate
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model
import numpy as np
import os
import cv2
from io import BytesIO
import tempfile
from datetime import datetime


def predict(data, width, height):
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the parent directory
    parent_dir = os.path.dirname(current_dir)
    models_and_harrcascade=os.path.join(parent_dir, 'emo','models_and_harrcascade')
    # Path to the model file in the parent directory
    model1_path = os.path.join(models_and_harrcascade, 'base_grayscale_model.h5')
   
    model2_path = os.path.join(models_and_harrcascade, 'base_grayscale_model_2.h5')
   
    model3_path = os.path.join(models_and_harrcascade, 'kaggle_grayscale_model.h5')
   
    model4_path = os.path.join(models_and_harrcascade, 'kaggle_grayscale_model2.h5')
    model1 = load_model(model1_path)
    model2 = load_model(model2_path)
    model3 = load_model(model3_path)
    model4 = load_model(model4_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # file_content = data.read()
    
    # # Convert the content to a numpy array
    # blob_array = np.frombuffer(file_content, dtype=np.uint8)
    channels = 3  # Replace ... with the actual number of channels of each frame
    width=int(width)
    height=int(height)
    frame_size = height * width * channels
    combined_video_data = b''
        
        # Iterate through the video chunks and concatenate them
    for chunk in data:
        for chunk_data in chunk.chunks():
            combined_video_data += chunk_data
    
    video_stream = BytesIO(combined_video_data)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(video_stream.getvalue())
        temp_file_path = temp_file.name

  
    

    # Reshape the flattened blob_array into individual frames
    
    # Create a VideoCapture object from the byte buffer
    cap = cv2.VideoCapture(temp_file_path)
    emotion_history = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break 

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = gray_frame[y:y+h, x:x+w]
            face = np.array(face)
            face = cv2.resize(face, (48, 48))

            face = np.expand_dims(face, axis=0)

            preds_model1 = model1.predict(face)
            preds_model2 = model2.predict(face)
            preds_model3 = model3.predict(face)
            preds_model4 = model4.predict(face)

            weight_model1 = 0.25
            weight_model2 = 0.5
            weight_model3 = 0.25
            weight_model4 = 0.25

            # Calculate the weighted average prediction
            weighted_average_preds = (
                weight_model1 * preds_model1 +
                weight_model2 * preds_model2 +
                weight_model3 * preds_model3 +
                weight_model4 * preds_model4
            )


            predicted_class_index = np.argmax(weighted_average_preds, axis=1)
            integer_to_label = {0: 'angry', 1: 'neutral', 2: 'happy', 3: 'fear', 4: 'disgust', 5: 'sad', 6: 'surprise'}
            predicted_emotion = integer_to_label[predicted_class_index[0]]

            # Get the current timestamp
            timestamp = datetime.now()
            
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")

            # Append the emotion and timestamp to the history list
            emotion_history.append({'emotion': predicted_emotion, 'timestamp': timestamp})
    
    return emotion_history


