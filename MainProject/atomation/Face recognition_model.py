
import cv2 as cv
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib

# מחלקה שחותכת את הפנים
class FACELOADING:
    def __init__(self, directory):
        self.directory = directory
        self.target_size = (160, 160)
        self.X = []
        self.Y = []
        self.detector = MTCNN()

    def extract_face(self, filename):
        img = cv.imread(filename)
        if img is None:
            raise FileNotFoundError(f"Cannot load image: {filename}")
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = cv.resize(img, (600, 600))
        x, y, w, h = self.detector.detect_faces(img)[0]['box']
        x, y = abs(x), abs(y)
        face = img[y:y + h, x:x + w]
        face_arr = cv.resize(face, self.target_size)
        return face_arr

    def load_faces(self, dir):
        FACES = []
        for im_name in os.listdir(dir):
            try:
                path = dir + im_name
                single_face = self.extract_face(path)
                FACES.append(single_face)
            except Exception as e:
                print(f"Error processing image {im_name}: {e}")
        return FACES

    def loaded_classes(self):
        for sub_dir in os.listdir(self.directory):
            path = self.directory + '/' + sub_dir + '/'
            FACES = self.load_faces(path)
            labels = [sub_dir for _ in range(len(FACES))]
            print(f"loaded successfully: {len(labels)}")
            self.X.extend(FACES)
            self.Y.extend(labels)
        return np.asarray(self.X), np.asarray(self.Y)
    
    def plot_image (self):
        plt.figure(figsize=(18,16))
        for num,image in enumerate(self.X):
            ncols=3
            nrows=len(self.Y)//ncols+1
            plt.subplot(nrows,ncols,num+1)
            plt.imshow(image)
            plt.axis('off')

# --- התחלת אימון --- 
faceloading = FACELOADING("D:\\temp\\Documents\\project\\picture")
X, Y = faceloading.loaded_classes()

# faceloading.plot_image()

embedder = FaceNet()

def get_embedding(face_img):
    if not isinstance(face_img, tf.Tensor):
        face_img = tf.convert_to_tensor(face_img, dtype=tf.float32)
    face_img = tf.expand_dims(face_img, axis=0)
    face_img = face_img.numpy()
    yhat = embedder.embeddings(face_img)
    return yhat[0]

EMBEDDED_X = np.asarray([get_embedding(img) for img in X])
np.savez_compressed("D:\\temp\\Documents\\project\\Text analysis\\home_data\\model\\faces_embeddings_done_4classes_good.npz", EMBEDDED_X, Y)

encoder = LabelEncoder()
encoder.fit(Y)
Y_encoded = encoder.transform(Y)

X_train, X_test, Y_train, Y_test = train_test_split(EMBEDDED_X, Y_encoded, shuffle=True, random_state=17)

model = SVC(kernel='linear', probability=True)
model.fit(X_train, Y_train)

# שמירת המודל וה-Encoder
joblib.dump(model, "D:\\temp\\Documents\\project\\Text analysis\\home_data\\model\\face_recognition_svc_model.pkl")
joblib.dump(encoder, "D:\\temp\\Documents\\project\\Text analysis\\home_data\\model\\label_encoder.pkl")










































































































# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# import cv2 as cv
# import numpy as np
# import tensorflow as tf
# import matplotlib.pyplot as plt
# from mtcnn.mtcnn import MTCNN
# from keras_facenet import FaceNet
# from sklearn.svm import SVC
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import accuracy_score
# import joblib


# # מחלקה לטעינה וחיתוך פנים
# class FACELOADING:
#     def __init__(self, directory):
#         self.directory = directory
#         self.target_size = (160, 160)
#         self.X = []
#         self.Y = []
#         self.detector = MTCNN()

#     def extract_face(self, filename):
#         img = cv.imread(filename)
#         if img is None:
#             raise FileNotFoundError(f"Cannot load image: {filename}")
#         img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#         img = cv.resize(img, (600, 600))
#         x, y, w, h = self.detector.detect_faces(img)[0]['box']
#         x, y = abs(x), abs(y)
#         face = img[y:y+h, x:x+w]
#         face_arr = cv.resize(face, self.target_size)
#         return face_arr

#     def load_faces(self, dir):
#         FACES = []
#         for im_name in os.listdir(dir):
#             try:
#                 path = dir + im_name
#                 single_face = self.extract_face(path)
#                 FACES.append(single_face)
#             except Exception as e:
#                 print(f"Error processing image {im_name}: {e} the face is not clear")
#         return FACES
    
#     #תיקיה שמכילה הרבה תיקיות קטנות
#     #כל שם  של תיקיה זה אדם
#     def loaded_classes(self):
#         for sub_dir in os.listdir(self.directory):
#             path = self.directory + '/' + sub_dir + '/'
#             FACES = self.load_faces(path)
#              #כל תמונה מהתיקיה מקבלת תגית של שם התיקיה
#             labels = [sub_dir for _ in range(len(FACES))]
#             print(f"loaded successfully:{len(labels)}")
#             self.X.extend(FACES)
#             self.Y.extend(labels)
#         return np.asarray(self.X), np.asarray(self.Y)

#     # def plot_image(self):
#     #     plt.figure(figsize=(18, 16))
#     #     for num, image in enumerate(self.X):
#     #         ncols = 3
#     #         nrows = len(self.Y) // ncols + 1
#     #         plt.subplot(nrows, ncols, num + 1)
#     #         plt.imshow(image)
#     #         plt.axis('off')

# # פונקציה לאימון המודל ושמירתו
# def train_face_model(image_dir, save_path):
#     faceloading = FACELOADING(image_dir)
#     X, Y = faceloading.loaded_classes()

#     embedder = FaceNet()
#     EMBEDDED_X = [embedder.embeddings([face])[0] for face in X]
#     EMBEDDED_X = np.asarray(EMBEDDED_X)

#     np.savez_compressed(save_path, EMBEDDED_X, Y)

#     encoder = LabelEncoder()
#     encoder.fit(Y)
#     Y_encoded = encoder.transform(Y)

#     X_train, X_test, Y_train, Y_test = train_test_split(EMBEDDED_X, Y_encoded, shuffle=True, random_state=17)
#     model = SVC(kernel='linear', probability=True)
#     model.fit(X_train, Y_train)

#     acc_train = accuracy_score(Y_train, model.predict(X_train))
#     acc_test = accuracy_score(Y_test, model.predict(X_test))
#     print("Train Accuracy:", acc_train)
#     print("Test Accuracy:", acc_test)

#     save_model(model,encoder,r"D:\temp\Documents\project\Text analysis\model")

#     return model, encoder, embedder, faceloading.detector




# def save_model(model, encoder, path):
#     joblib.dump(model, path + '_model.pkl')
#     joblib.dump(encoder, path + '_encoder.pkl')
# Original_pictures="D:\\temp\\Documents\\project\\picture"
# Face_pictures="D:\\temp\\Documents\\project\\Text analysis\\model\\faces_embeddings_done_4classes_good.npz"

# train_face_model(Original_pictures,Face_pictures)























































































































































