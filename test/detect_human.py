import cv2
import time

# 初始化摄像头
cap = cv2.VideoCapture(0)  # 0 表示默认摄像头

# 初始化 HOG 人体检测器（Histogram of Oriented Gradients）
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# 检测间隔（秒）
DETECTION_INTERVAL = 1
last_detection_time = 0

print("启动靠近检测器，按 q 键退出。")

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取摄像头")
        break

    current_time = time.time()
    if current_time - last_detection_time >= DETECTION_INTERVAL:
        # 缩小图像，加快处理速度
        resized = cv2.resize(frame, (640, 480))

        # 检测人体（返回矩形框）
        boxes, weights = hog.detectMultiScale(resized, winStride=(8, 8))

        if len(boxes) > 0:
            print("Human detected")

        last_detection_time = current_time

    # 按 q 退出程序
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()