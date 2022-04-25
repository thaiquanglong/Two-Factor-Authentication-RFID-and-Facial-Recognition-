# It helps in identifying the faces
import cv2, numpy, os, sys
def resource_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return base_path



class Facial_Model:
    def __init__(self) -> None:
        self.size = 4
        self.haar_file = resource_path()+'\haarcascade_frontalface_default.xml'
        print(self.haar_file)
        self.datasets = 'datasets'
        self.refresh()
        (self.width, self.height) = (130, 100)
        self.model = cv2.face.LBPHFaceRecognizer_create()
        if(self.id > 0) : self.build_model()

    def refresh(self):
        (self.images, self.labels, self.names, self.id) = ([], [], {}, 0)
        for (self.subdirs, self.dirs, self.files) in os.walk(self.datasets):
            for subdir in self.dirs:
                self.names[self.id] = subdir
                subjectpath = os.path.join(self.datasets, subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + '/' + filename
                    label = self.id
                    self.images.append(cv2.imread(path, 0))
                    self.labels.append(int(label))
                self.id += 1
    
    def build_model(self):
        self.refresh()
        (images, labels) = [numpy.array(lis) for lis in [self.images, self.labels]]
        self.model.train(images, labels)


    def create_new_face(self, sub_data :str) -> None:
        
        path = os.path.join(self.datasets, sub_data)
        if not os.path.isdir(path):
            os.makedirs(path)
        

        (width, height) = (130, 100)   
        

        faceCascade = cv2.CascadeClassifier(self.haar_file)
        vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        
        count = 0
        while count < 100:
            ret, frame = vid.read()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor = 1.1,
                minNeighbors = 5,
                minSize = (30,30))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                cv2.imwrite('% s/% s.png' % (path, count), face_resize)
                count += 1
            
            cv2.imshow('OpenCV', frame)
            key = cv2.waitKey(10)
            if key == 27:
                break

        vid.release()
        cv2.destroyAllWindows()
        self.build_model()
    
    def recognize(self,user:str) -> bool:
        self.refresh()
        faceCascade = cv2.CascadeClassifier(self.haar_file)
        vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        count = 0
        sum = 0
        num_of_pics = 50
        while count < num_of_pics:
            self.ret, frame = vid.read()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor = 1.1,
                minNeighbors = 5,
                minSize = (30,30))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (self.width, self.height))
                # Try to recognize the face
                prediction = self.model.predict(face_resize)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        
                if (self.names[prediction[0]] == user) and (prediction[1]>=55):
        
                    cv2.putText(frame, "% s - %.0f%% - Correct User" %
                                    (self.names[prediction[0]], prediction[1]), (x-10, y-10),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    count += 1
                    sum += prediction[1]
                if (self.names[prediction[0]] != user) and (prediction[1]>=55):
        
                    cv2.putText(frame, "% s - %.0f%% - Wrong User" %
                                    (self.names[prediction[0]], prediction[1]), (x-10, y-10),
                                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    count += 1
                else:
                    cv2.putText(frame, 'not recognized', (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        
            cv2.imshow('OpenCV', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        if sum == 0: return False
        if (sum/num_of_pics) < 55: return False
        return True

    