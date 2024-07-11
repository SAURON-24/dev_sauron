import cv2
import numpy as np
from tensorflow.keras.models import load_model

# 학습된 모델 불러오기
model = load_model('soy_sauce_classifier.h5')

# 이미지 예측 함수
def predict_image(image_path, model):
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (150, 150))
    img_array = np.expand_dims(img_resized, axis=0) / 255.0
    
    prediction = model.predict(img_array)
    return prediction[0][0]

# 이미지에 상자 그리기
def draw_bounding_box(image_path, prediction):
    img = cv2.imread(image_path)
    label = 'Soy Sauce' if prediction > 0.5 else 'Soup Sauce'
    
    color = (0, 255, 0) if prediction > 0.5 else (0, 0, 255)
    cv2.putText(img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.rectangle(img, (50, 50), (img.shape[1]-50, img.shape[0]-50), color, 3)
    
    cv2.imshow('Prediction', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 예측 및 결과 시각화
image_path = 'path_to_your_image.jpg'
prediction = predict_image(image_path, model)
draw_bounding_box(image_path, prediction)
