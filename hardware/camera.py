import cv2
import time

class Camera:
    def __init__(self):
        # initialize cam
        self.cap = cv2.VideoCapture(0)

        # initialize hog detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # params
        self.DETECTION_INTERVAL = 1

        # status
        self.is_detecting = False

    def start_detection(self):
        self.is_detecting = True

        last_detection_time = 0
        while self.is_detecting:

            current_time = time.time()
            if current_time - last_detection_time >= self.DETECTION_INTERVAL:
                ret, frame = self.cap.read()
                if not ret:
                    print("cannot read cam")
                    self.is_detecting = False
                    break

                resized = cv2.resize(frame, (640, 480))
                boxes, weights = self.hog.detectMultiScale(resized, winStride=(8, 8))

                if len(boxes) > 0:
                    print("Human detected")
                    self.is_detecting = False
                    return True

                last_detection_time = current_time


    def destroy(self):
        """
        Call this methods when everything ends
        """
        self.cap.release()
        cv2.destroyAllWindows()