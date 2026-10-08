import cv2
import numpy as np
from pupil_apriltags import Detector

# 创建tag36h11检测器
at_detector = Detector(
    families="tag36h11",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25
)

cap = cv2.VideoCapture(0)

# 临时假内参，仅用于demo验证库是否可用，任务二标定后要替换成真实参数
fx, fy = 600, 600
cx, cy = 320, 240
tag_size = 0.08  # 单位m，tag黑色方块边长

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取摄像头画面")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    tags = at_detector.detect(
        gray,
        estimate_tag_pose=True,
        camera_params=[fx, fy, cx, cy],
        tag_size=tag_size
    )

    for tag in tags:
        # 画四个角点方框
        pts = tag.corners.astype(np.int32)
        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        # 打印ID
        cv2.putText(frame, f"ID:{tag.tag_id}",
                    (int(pts[0][0]), int(pts[0][1]) - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        # 打印位姿
        t = tag.pose_t
        print(f"Tag ID={tag.tag_id} | x={t[0][0]:.2f} m, y={t[1][0]:.2f} m, z={t[2][0]:.2f} m")

    cv2.imshow("AprilTag Demo (press q to quit)", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
