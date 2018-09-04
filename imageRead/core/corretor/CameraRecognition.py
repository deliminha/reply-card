import os
import threading

import cv2
import numpy as np

try:
    from .scanner import Scanner
except:
    from scanner import Scanner


class CameraRecognition(object):
    MAX_FEATURES = 500
    GOOD_MATCH_PERCENT = 0.15
    HEIGHT = 0
    WIDTH = 0
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    TEST_GENERIC = "dataset/imgs/gabarito_template_geral.png"

    def __init__(self, amount_question=10):

        self.TEMPLATE_ALTERNATIVAS = self.load_image_gray('dataset/imgs/gabarito_template_geral_alternativas.png')
        self.TEMPLATE_ALTERNATIVAS_SCANNER = self.load_image_gray(
            'dataset/imgs/gabarito_template_geral_alternativas_scanner.png')
        self.AMOUNT_QUESTION = amount_question
        threading.Thread.__init__(self)

    def get_test_generic(self):

        return self.load_image(self.TEST_GENERIC)

    def load_image(self, path_image):

        path_full = os.path.join(os.path.dirname(__file__), path_image)
        return cv2.imread(path_full, cv2.IMREAD_COLOR)

    def load_image_gray(self, path_image):
        image = self.load_image(path_image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    # função responsável por alinhar as imagens baseado no template pré-configurado
    def align_images(self, im1, im2=None):
        try:
            if im2 is None:
                im2 = self.get_test_generic()
            else:
                im2 = self.load_image_gray(im2)

            # Alterando imagens para escola cinza
            im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
            im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
            _, frame_bin = cv2.threshold(im1Gray, 155, 255, cv2.THRESH_OTSU)  # tornando a diferença uma img binária

            im1Gray = cv2.adaptiveThreshold(im1Gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            im2Gray = cv2.adaptiveThreshold(im2Gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

            # Detectando características do ORB e calculando descritores.
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

            print("Homografia Estimada : \n", h)
            # A imagem alinhada será restaurada na im1Reg.
            # A homografia estimada será armazenada em h.

            return im1Reg, h
        except:
            print("ERROR 'align_images' IMAGE ")
            self.cap.release()
            cv2.destroyAllWindows()
            exit(0)

    def answer_values(self, point_occupation):

        occupation = round((point_occupation * 100) / self.WIDTH)
        if occupation < 15: return
        if occupation < 30: return 'A'
        if occupation < 50: return 'B'
        if occupation < 70: return 'C'
        if occupation < 90: return 'D'
        return 'E'

    def coordinates_question(self, image):
        try:
            # Criando o detector baseado na versão do CV
            is_cv3 = cv2.__version__.startswith("3.")
            if is_cv3:
                detector = cv2.SimpleBlobDetector_create()
            else:
                detector = cv2.SimpleBlobDetector()

            # Detectando corpos
            keypoints = detector.detect(image)
            im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0, 0, 255),
                                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            return keypoints
        except:
            print("ERROR 'coordinates_question' IMAGE")
            self.cap.release()
            cv2.destroyAllWindows()
            exit(0)

    def evaluate_question(self, image):
        try:
            coordinates = self.coordinates_question(image)
            response = []
            if coordinates:
                for point in coordinates:
                    response.append(self.answer_values(point.pt[0]))
            return response
        except:
            print("ERROR 'evaluate_question' IMAGE ")
            self.cap.release()
            cv2.destroyAllWindows()
            exit(0)

    def get_answer(self, image):
        try:

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            if self.isImage:
                result = cv2.matchTemplate(gray, self.TEMPLATE_ALTERNATIVAS_SCANNER, cv2.TM_CCOEFF_NORMED)
            else:
                result = cv2.matchTemplate(gray, self.TEMPLATE_ALTERNATIVAS, cv2.TM_CCOEFF_NORMED)

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if self.isImage:
                self.HEIGHT, self.WIDTH = self.TEMPLATE_ALTERNATIVAS_SCANNER.shape[::1]
            else:
                self.HEIGHT, self.WIDTH = (53, 440)
            # Create Bounding Box
            top_left = max_loc
            bottom_right = (top_left[0] + self.WIDTH, top_left[1] + self.HEIGHT)

            cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
            answer_values = {}
            # Particiona o gabarito e identifica isoladamente a resposta de cada questão
            for i in range(self.AMOUNT_QUESTION):
                bottom_right = (bottom_right[0], bottom_right[1] + self.HEIGHT)
                top_left = (top_left[0], top_left[1] + self.HEIGHT)

                cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
                cropped = image[
                          top_left[1]:bottom_right[1],
                          top_left[0]:bottom_right[0]
                          ]

                answer_values[i + 1] = self.evaluate_question(cropped)

            return answer_values
        except:
            print("ERROR 'get_answer' IMAGE ")
            cv2.destroyAllWindows()
            exit(0)

    def identify_alternative(self, image_full, image_cropped):
        try:
            # Function that compares input image to template
            # It then returns the number of ORB matches between them
            image_template = self.load_image_gray(self.TEST_GENERIC).copy()
            image1 = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2GRAY)

            # Create ORB detector with 1000 keypoints with a scaling pyramid factor of 1.2
            orb = cv2.ORB_create(1000, 1.2)

            # Detect keypoints of original image
            (kp1, des1) = orb.detectAndCompute(image1, None)

            # Detect keypoints of rotated image
            (kp2, des2) = orb.detectAndCompute(image_template, None)

            # Create matcher
            # Note we're no longer using Flannbased matching
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            # Do matching
            matches = bf.match(des1, des2)

            # Sort the matches based on distance.  Least distance
            # is better
            matches = sorted(matches, key=lambda val: val.distance)

            # Our threshold to indicate object deteciton
            # For new images or lightening conditions you may need to experiment a bit
            # Note: The ORB detector to get the top 1000 matches, 350 is essentially a min 35% match
            self.threshold = 250
            is_valid = len(matches) > self.threshold
            if not self.isImage:
                cv2.imshow("corrector", image_full)
                if is_valid:
                    self.delimiter(image_full, self.BLUE)

                    cv2.imshow("corrector", image_full)
                    cv2.waitKey(10)
                    cv2.destroyAllWindows()
                # If matches exceed our threshold then object has been detected
            return is_valid
        except:
            print("ERROR 'identify_alternative' IMAGE ")
            self.cap.release()
            cv2.destroyAllWindows()
            exit(0)

    def delimiter(self, image, color):
        try:
            self.HEIGHT, self.WIDTH = image.shape[:2]

            # Define ROI Box Dimensions (Note some of these things should be outside the loop)
            top_left_x = int(self.WIDTH / 50)
            top_left_y = int((self.HEIGHT / 2.3) + (self.HEIGHT / 3))
            bottom_right_x = int((self.WIDTH / 2.05) * 2)
            bottom_right_y = int((self.HEIGHT / 2) - (self.HEIGHT / 3))

            # Draw rectangular window for our region of interest
            cv2.rectangle(image, (top_left_x - 8, top_left_y + 8), (bottom_right_x + 2, bottom_right_y - 2), color, 2)

            mask = np.zeros(image.shape[:2], dtype="uint8")
            cropped = image[bottom_right_y:top_left_y, top_left_x:bottom_right_x]
            cropped_mask = cv2.bitwise_and(image.copy(), image.copy(), mask=mask)
            cropped_mask[bottom_right_y:top_left_y, top_left_x:bottom_right_x] = cropped

            return cropped_mask, cropped
        except:
            print("ERROR 'delimiter' IMAGE ")
            self.cap.release()
            cv2.destroyAllWindows()
            exit(0)

    def identify_test(self, image):
        cropped_mask, _ = self.delimiter(image, self.GREEN)

        status = self.identify_alternative(image, cropped_mask)
        _, crooped = self.delimiter(image, self.BLUE)
        return status, crooped

    def image_processing(self, image):
        scanner = Scanner()
        imReg = None
        self.isImage = True
        try:
            image = self.load_image(image)
            status, _ = self.identify_test(image)
            scanning = scanner.scanning(image)
            if scanning is not None:
                imReg = scanning.copy()
            if (cv2.waitKey(1) & 0xFF == ord('q')) or status:
                if imReg is not None:
                    respostas = self.get_answer(imReg)
                    cv2.destroyAllWindows()

                    return respostas
                else:
                    print("ERRO 'scanner' IMAGE")
        except:
            print("ERRO 'image_processing' IMAGE")
            cv2.destroyAllWindows()

    def camera_processing(self):
        scanner = Scanner()
        self.cap = cv2.VideoCapture(0)
        imReg = None
        self.isImage = False
        try:
            while (self.cap.isOpened()):

                ret, frame = self.cap.read()
                frame = cv2.flip(frame, 1)
                status, cropped = self.identify_test(frame.copy())
                cropped = cv2.flip(cropped, 1)
                scanning = scanner.scanning(cropped)
                if scanning is not None:
                    imReg = scanning.copy()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.cap.release()
                    cv2.destroyAllWindows()
                    return False, None
                if status:
                    # imReg, h = self.align_images(cropped)
                    if imReg is not None:
                        respostas = self.get_answer(imReg)
                        self.cap.release()
                        cv2.destroyAllWindows()

                        return True, respostas
                    else:
                        print("ERRO 'scanner' IMAGE")
                        return False
        except:
            print("ERRO 'camera_processing' IMAGE")
            self.cap.release()
            cv2.destroyAllWindows()
        self.cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def image_processing_test(self):
        self.isImage = True
        frame = self.load_image('dataset/imgs/gabarito_template_geral_preenchido.png')
        self.image_processing('dataset/imgs/gabarito_template_geral_preenchido.png')


class myThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.camera = CameraRecognition()

    def run_thread(self, quantidadeQuestao):
        if quantidadeQuestao is not None:
            self.camera = CameraRecognition(quantidadeQuestao)
        return self.camera.camera_processing()


if __name__ == "__main__":
    recognition = CameraRecognition()

    recognition.image_processing_test()

    cv2.destroyAllWindows()
