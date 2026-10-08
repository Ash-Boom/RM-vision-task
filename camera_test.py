import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("0号设备打不开，尝试换编号1/2/3")
else:
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("usb_camera", frame)
        # 按键盘 q 退出画面窗口
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()