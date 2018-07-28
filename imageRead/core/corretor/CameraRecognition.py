from time import time

import cv2
import numpy as np


class CameraRecognition:
    
    def __init__(self, amount_question = 10):
        self.TEST_GENERIC = "dataset/imgs/gabarito_template_geral2.png"
        self.TEMPLATE_ALTERNATIVAS = cv2.imread('dataset/imgs/gabarito_template_geral_alternativas.png',0)
        self.MAX_FEATURES = 500
        self.GOOD_MATCH_PERCENT = 0.15
        self.HEIGHT = 0
        self.WIDTH = 0
        self.AMOUNT_QUESTION = amount_question        
        self.BLUE  = (255,0,0)
        self.GREEN = (0,255,0)
        self.INIT = None
        self.END = None
    
    def get_test_generic(self):
        
        return self.load_image(self.TEST_GENERIC)
    
    
    def load_image(self,path_image):
        
        return cv2.imread(path_image, cv2.IMREAD_COLOR)
    
    
    def load_image_gray(self,path_image):
        image = self.load_image(path_image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray
    
    
    #função responsável por alinhar as imagens baseado no template pré-configurado
    def align_images(self, im1, im2=None):
        
        if im2 is None:
            im2 = self.get_test_generic()
        else:
            im2 = self.load_image_gray(im2)
        
        
        #Alterando imagens para escola cinza
        im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        #Detectando características do ORB e calculando descritores.
        orb = cv2.ORB_create(self.MAX_FEATURES)
        keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
        keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

        # Ocorrências de características
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(descriptors1, descriptors2, None)

        # Ordenando melhores ocorrências
        matches.sort(key=lambda x: x.distance, reverse=False)

        # Removendo ocorrências que não possuem melhores porcentagem de reconhecimento
        numGoodMatches = int(len(matches) * self.GOOD_MATCH_PERCENT)
        matches = matches[:numGoodMatches]

        # Draw melhores matches
        imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)

        # Extraindo localização de melhores correspondências
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt
            points2[i, :] = keypoints2[match.trainIdx].pt

        # buscando homografia
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

        # Usando homografia
        self.HEIGHT, self.WIDTH, channels = im2.shape
        im1Reg = cv2.warpPerspective(im1, h, (self.WIDTH, self.HEIGHT))

        print("Homografia Estimada : \n",  h)
        # A imagem alinhada será restaurada na im1Reg. 
        # A homografia estimada será armazenada em h.
        #cv2.imshow("im1Reg",im1Reg)
        #cv2.waitKey(0)
        return im1Reg, h
    
    
    def answer_values(self,point_occupation):
        
        occupation = round((point_occupation*100)/self.WIDTH)
        if occupation < 15: return
        if occupation < 30: return 'A'
        if occupation < 50: return 'B'
        if occupation < 70: return 'C'
        if occupation < 90: return 'D'
        return 'E'

    def coordinates_question(self,image):

        # Criando o detector baseado na versão do CV
        is_cv3 = cv2.__version__.startswith("3.")
        if is_cv3:
            detector = cv2.SimpleBlobDetector_create()
        else:
            detector = cv2.SimpleBlobDetector()

        #Detectando corpos
        keypoints = detector.detect(image)
        return keypoints
    

    def evaluate_question(self,image):

        coordinates = self.coordinates_question(image)  
        response = []
        if coordinates:
            for point in coordinates:            
                response.append(self.answer_values(point.pt[0]))   
        return response

    
    def get_answer(self,image):
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, self.TEMPLATE_ALTERNATIVAS, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        self.HEIGHT, self.WIDTH = self.TEMPLATE_ALTERNATIVAS.shape[:2]

        #Create Bounding Box
        top_left = max_loc
        bottom_right = (top_left[0] + self.WIDTH, top_left[1] + self.HEIGHT)        

        answer_values = {}
        #Particiona o gabarito e identifica isoladamente a resposta de cada questão
        for i in range(self.AMOUNT_QUESTION):
            bottom_right = (bottom_right[0], bottom_right[1] + self.HEIGHT)
            top_left     = (top_left[0]    ,     top_left[1] + self.HEIGHT)                        

            cropped = image[
                            top_left[1]:bottom_right[1],
                            top_left[0]:bottom_right[0]
                           ]

            answer_values[i+1] = self.evaluate_question(cropped)
    
        return answer_values

    
    def identify_alternative(self,image,cropped):

        try:            
            gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)

            rows = gray.shape[0]
            circles = cv2.HoughCircles(gray,
                                       cv2.HOUGH_GRADIENT,1,
                                       rows/10,
                                       param1=50,
                                       param2=30,
                                       minRadius=0, 
                                       maxRadius=30)

            if circles is not None:
                circles = np.uint16(np.around(circles))

                for i in circles[0, :]:
                    center = (i[0], i[1])

                    #Ponto central
                    cv2.circle(image, center, 1, self.BLUE, 3)

                    #Circulo externo
                    radius = i[2]
                    cv2.circle(image, center, radius, self.GREEN, 3)
                    self.END = time()

                if(self.INIT and int(self.END - self.INIT) >= 2):
                    return True
            else:
                self.INIT = time()
            cv2.imshow("corrector", image)
            
        except:
            cv2.destroyAllWindows()
            exit(0)
    
    
    def delimiter(self,image,color):
        
        self.HEIGHT, self.WIDTH = image.shape[:2]
        
        # Define ROI Box Dimensions (Note some of these things should be outside the loop)
        top_left_x     = int(   self.WIDTH / 8)
        top_left_y     = int( (self.HEIGHT / 2) + (self.HEIGHT / 3))
        bottom_right_x = int((self.WIDTH / 2.3) * 2)
        bottom_right_y = int( (self.HEIGHT / 2) - (self.HEIGHT / 3))
        
        # Draw rectangular window for our region of interest
        cv2.rectangle(image, (top_left_x,top_left_y), (bottom_right_x,bottom_right_y), color, 2)

        mask = np.zeros(image.shape[:2], dtype = "uint8")
        cropped = image[bottom_right_y:top_left_y , top_left_x:bottom_right_x]  
        cropped_mask = cv2.bitwise_and(image.copy(), image.copy(), mask = mask)
        cropped_mask[bottom_right_y:top_left_y , top_left_x:bottom_right_x] = cropped

        return cropped_mask,cropped
    
    
    def identify_test(self,image):  
        cropped_mask,_ = self.delimiter(image,self.GREEN)

        status = self.identify_alternative(image,cropped_mask)  
        _, crooped = self.delimiter(image,self.BLUE)
        return status,crooped
    
    
    
    def camera_processing(self):
    
        cap = cv2.VideoCapture(0)

        while(True):        
            ret, frame = cap.read()
            frame = cv2.flip(frame,1)
            status,cropped = self.identify_test(frame)
            if (cv2.waitKey(1) & 0xFF == ord('q')) or status: 
                cropped = cv2.flip(cropped,1)
                imReg, h = self.align_images(cropped)
                print(self.get_answer(imReg))
                break

        cap.release()
        cv2.destroyAllWindows()
    

if __name__ == "__main__":
    recognition = CameraRecognition()

    recognition.camera_processing()
    
    cv2.destroyAllWindows()

