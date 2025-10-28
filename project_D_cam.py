import cv2
import numpy as np
import pyrealsense2 as rs

# RealSense 카메라 파이프라인 설정
pipeline = rs.pipeline()
config = rs.config()

# RGB와 Depth 스트림 모두 활성화
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # RGB 스트림 설정
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 깊이 스트림 설정

# 카메라 시작
pipeline.start(config)

try:
    while True:
        # 프레임 가져오기
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # 깊이 데이터를 Numpy 배열로 변환
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # 화면 크기 설정
        height, width = depth_image.shape

        # 중앙, 왼쪽, 오른쪽 위치에서 거리 계산
        center_x, center_y = width // 2, height // 2
        left_x, left_y = width // 4, height // 2
        right_x, right_y = 3 * width // 4, height // 2

        # 각 위치에서 거리 값 추출 (단위: mm)
        center_distance = depth_image[center_y, center_x]
        left_distance = depth_image[left_y, left_x]
        right_distance = depth_image[right_y, right_x]

        # 거리 출력 (단위: 미터로 변환)
        center_distance_m = center_distance / 1000.0
        left_distance_m = left_distance / 1000.0
        right_distance_m = right_distance / 1000.0

        # RGB 이미지 위에 거리값 표시
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(color_image, f"Center: {center_distance_m:.2f}m", (20, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(color_image, f"Left: {left_distance_m:.2f}m", (20, 60), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(color_image, f"Right: {right_distance_m:.2f}m", (20, 90), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # 깊이 이미지 색상 맵으로 변환
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # RGB 이미지와 Depth 이미지를 수평으로 합성하여 표시
        combined_image = np.hstack((color_image, depth_colormap))

        # 합성된 이미지 화면에 표시
        cv2.imshow('RGB + Depth Stream', combined_image)

        # 키 입력 대기 (Esc 눌러서 종료)
        key = cv2.waitKey(1)
        if key == 27:  # ESC 키로 종료
            break

finally:
    # 카메라 종료
    pipeline.stop()
    cv2.destroyAllWindows()
