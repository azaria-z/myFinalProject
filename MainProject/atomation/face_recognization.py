
import cv2 as cv
import tensorflow as tf
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
import joblib
import matplotlib.pyplot as plt
import warnings
from sklearn.exceptions import InconsistentVersionWarning
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "2"

# טוען את המודל ואת ה-encoder
model = joblib.load(r"D:\temp\Documents\project\Text analysis\home_data\model\face_recognition_svc_model.pkl")
encoder = joblib.load(r"D:\temp\Documents\project\Text analysis\home_data\model\label_encoder.pkl")
embedder = FaceNet()
detector = MTCNN()

# faces_to_show = []
# def show_face(count,t_img):
#     for i in range(count):
#         x, y, w, h = detector.detect_faces(t_img)[i]['box']
#         face_img = t_img[y:y+h, x:x+w]
#         face_img = cv.resize(face_img, (160,160))
#         faces_to_show.append(face_img)

#     plt.figure(figsize=(12,4))
#     for i, face in enumerate(faces_to_show):
#         plt.subplot(1, len(faces_to_show), i+1)
#         plt.imshow(face)
#         plt.axis('off')
#     plt.show()



def get_embedding(face_img):
    if not isinstance(face_img, tf.Tensor):
        face_img = tf.convert_to_tensor(face_img, dtype=tf.float32)
    face_img = tf.expand_dims(face_img, axis=0)
    face_img = face_img.numpy()
    yhat = embedder.embeddings(face_img)
    return yhat[0]

def check_famaliy(t_img, i):
    faces = detector.detect_faces(t_img)
    # if i >= len(faces):
    #     print(f"Error: index {i} out of range for detected faces")
    #     return None, 0
    x, y, w, h = faces[i]['box'] 
    print(f"Face {i} box: {x},{y},{w},{h}")
   
    t_img = t_img[y:y + h, x:x + w]
    t_img = cv.resize(t_img, (160, 160))
    # faces_to_show.append(t_img)  # שמירת תמונת הפנים להצגה

    t_img = get_embedding(t_img)
    test_img = [t_img]
    ypred = model.predict(test_img)
    ypred = encoder.inverse_transform(ypred)
    prob = max(model.predict_proba(test_img)[0])
    print("Probabilities:", prob)
    return ypred, prob

def recognize_man(img):
    # בדיקה
    t_img = cv.imread(img)
    t_img = cv.cvtColor(t_img, cv.COLOR_BGR2RGB)
    face = detector.detect_faces(t_img)
    count = len(face)
    print("Number of faces:", count)

    flag = False
    words_list = []
    for i in range(count):
        man, prob = check_famaliy(t_img, i)
        if prob > 0.8:
            flag = True
            words_list.append(str(man[0]))
            # show_face(count,t_img)

    if flag ==True:
        if len(words_list)>1:
            for i in range(len(words_list)):
                print("The people identified in the family:", words_list[i])
        return(words_list[0])
    else:
        return("guest")
    
# if __name__=="main":
# print(recognize_man(r"D:\temp\Documents\project\picture\hila_emuna\DSCN2850.JPG"))












































































# import cv2 as cv
# import joblib



# import numpy as np
# from sklearn.preprocessing import LabelEncoder
# from sklearn.svm import SVC
# model = joblib.load(r"D:\temp\Documents\project\Text analysis\model\model_model.pkl")
# encoder = joblib.load(r"D:\temp\Documents\project\Text analysis\model\model_encoder.pkl")


# # def load_model_from_embeddings(npz_path="D:\temp\Documents\project\Text analysis\model\faces_embeddings_done_4classes_good.npz"):
# #     data = np.load(npz_path, allow_pickle=True)
# #     EMBEDDED_X = data['arr_0']
# #     Y = data['arr_1']
    
# #     # קידוד התוויות למספרים
# #     encoder = LabelEncoder()
# #     encoder.fit(Y)
# #     Y = encoder.transform(Y)

# #     # אימון המודל (מהיר – לא צריך לחשב שוב הטבעות)
# #     model = SVC(kernel='linear', probability=True)
# #     model.fit(EMBEDDED_X, Y)

# #     return model, encoder

# # model, encoder = load_model_from_embeddings()


# # פונקציה לבדיקת פנים חדשים

# def check_faces(image_path, model, encoder, embedder, detector, threshold=0.8):
#     t_img = cv.imread(image_path)
#     t_img = cv.cvtColor(t_img, cv.COLOR_BGR2RGB)
#     faces = detector.detect_faces(t_img)

#     found_names = []
#     for i, face in enumerate(faces):
#         x, y, w, h = face['box']
#         face_img = t_img[y:y+h, x:x+w]
#         face_img = cv.resize(face_img, (160, 160))
#         embedding = embedder.embeddings([face_img])[0]
#         pred = model.predict([embedding])
#         name = encoder.inverse_transform(pred)[0]
#         prob = max(model.predict_proba([embedding])[0])
#         print(f"Detected {name} with probability {prob:.2f}")
#         if prob > threshold:
#             found_names.append(name)

#     if found_names:
#         print("The people identified in the family:", found_names)
#     else:
#         print("there is a guest")

#     return found_names


# check_faces("D:\temp\Documents\project\picture_project\photo_20250424_160643.jpg")