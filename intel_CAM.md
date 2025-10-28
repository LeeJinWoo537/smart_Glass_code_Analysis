## 인텔 뎁쓰 카메라 코드

```python
import cv2                      # OpenCV 라이브러리
import numpy as np      
import pyrealsense2 as rs       # intel RealSense 앱 연동

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

```

# 📢 파이프라인이란??

- 기본적으로 "순차적으로 이어지는 작업의 흐름"을 나타냅니다. 즉, 여러 단계로 구성된 작업 흐름에서 각 단계가 데이터를 처리하고 결과를 다음 단계로 넘기는 방식입니다.

1. 일반적인 파이프라인 개념
    - 파이프라인은 여러 개의 작업 단계로 구성되며, 각 단계는 입력을 받아 처리하고 그 결과를 다음 단계로 전달합니다.
    - 예를 들어, 파이프라인에서 입력 데이터는 첫 번째 단계에서 처리되어 두 번째 단계로 넘어가고, 그 후의 단계들이 계속해서 데이터를 처리해 최종 결과를 도출합니다.
    - 각 단계는 독립적으로 실행되며, 데이터가 각 단계를 거치면서 변형되고 최종적인 목표를 달성하게 됩니다.

2. 파이프라인의 주요 특징
    - 순차적 처리: 각 단계가 끝난 후 결과가 다음 단계로 전달됩니다. 이 과정은 순차적으로 이루어집니다.
    - 병렬 처리: 일부 파이프라인은 병렬로 작업을 수행할 수도 있습니다. 예를 들어, 여러 입력 데이터를 병렬로 처리하여 각 결과를 마지막에 결합할 수 있습니다.


> 🤔으잉?? 근데 그러면 절차지향적 C언어랑 별로 다를게 없어보여...
    ● 맞아!! 사실 C언어뿐만 아니라 다른 언어들(Python, Java, JavaScript, Go, Ruby) 등 어떤 언어에서도 파이프라인의 기본 개념은 같아

```c
void step1(FILE *input) {
    // 첫 번째 단계: 파일에서 데이터 읽기
    // 데이터를 읽고 변환하는 작업
}

void step2() {
    // 두 번째 단계: 데이터 처리
}

void step3() {
    // 세 번째 단계: 처리된 데이터 출력
}

int main() {
    FILE *input = fopen("input.txt", "r");
    step1(input);  // 첫 번째 단계
    step2();       // 두 번째 단계
    step3();       // 세 번째 단계
    fclose(input);
    return 0;
}
```
- 이런식으로 사용하는게 다 파이프라인 형식이라고 할 수 있어



```python
pipeline = rs.pipeline()
```
- Intel RealSense 카메라에서 데이터를 스트리밍하는 파이프라인 객체를 생성하는 코드
- `rs.pipeline()`은 RealSense 카메라의 데이터 처리 흐름을 관리하는 객체로, 이 객체를 통해 카메라의 스트림을 설정하고 실행한다.

> 🤔 스트리밍이란?: 데이터를 **실시간으로 연속적으로 전송하고 처리하는 방식**입니다. <br>
> 스트리밍은 데이터를 전체를 한 번에 처리하는 것이 아니라, 조각조각 나누어 실시간으로 처리하는 방식
- 특징은: 데이터를 실시간으로 처리되서 지연 없이 바로 처리가 가능!

1. rs.pipeline() 객체
    - rs.pipeline()은 RealSense SDK에서 제공하는 클래스로, 데이터 스트리밍을 위한 파이프라인을 관리합니다.
    - 이 파이프라인 객체는 카메라의 비디오 스트림, 깊이 데이터, 임의의 센서 데이터 등을 처리하고, 이를 순차적으로 받아오는 역할을 합니다.
    - 카메라의 스트리밍을 시작, 정지, 데이터 처리 등 다양한 작업을 파이프라인 객체를 통해 처리할 수 있습니다.

2. RealSense 파이프라인의 역할
    - 스트림 설정: 파이프라인 객체는 `rs.config()`와 함께 사용되어 카메라의 스트림 설정을 담당합니다. 예를 들어, RGB 스트림과 Depth 스트림을 설정한 후, 이를 파이프라인에 전달하여 시작합니다.
    - 데이터 흐름 처리: 파이프라인은 각 스트림의 데이터를 연속적으로 받아오고 처리합니다. 예를 들어, `pipeline.wait_for_frames()` 메서드는 실시간으로 카메라에서 프레임을 기다리고 이를 처리하는 역할을 합니다.
    - 실행 및 종료: 파이프라인 객체는 카메라 스트리밍을 시작하고, 종료할 때는 pipeline.stop()을 호출하여 스트리밍을 멈추는 역할을 합니다.
    > 데이터를 연속적이고 순차적으로 처리할 수 있도록 흐르는 데이터의 흐름

    📌 비교분석!
    1. 스트림(Stream)
        ● 스트림은 마치 하천의 물줄기입니다. 물이 계속해서 흐르는 길을 생각하면 됩니다. 물은 이 하천을 따라 끊임없이 흐릅니다. 물줄기 자체가 바로 스트림입니다.
        ● 물줄기는 흐르는 방향을 제공하며, 그 안에서 물이 계속 흐릅니다. 스트림도 마찬가지로 데이터를 흐르게 할 수 있는 경로나 채널입니다.

    2. 스트리밍(Streaming)
        ● 스트리밍은 하천에서 흐르는 물을 사용하는 과정에 비유할 수 있습니다. 예를 들어, 하천의 물이 흐르고 있을 때, 그 물을 끊임없이 사용하며, 물의 흐름을 실시간으로 따라가는 것이 바로 스트리밍입니다.
        ● 물이 하천을 따라 흘러가는 것처럼, 데이터도 스트림을 따라 실시간으로 전송되고 처리됩니다. 물을 한 번에 다 사용하지 않고, 계속 흐르는 물을 사용하는 방식입니다.

3. rs.pipeline()을 사용하는 기본 흐름
    - 파이프라인 객체 생성: `pipeline = rs.pipeline()`을 통해 파이프라인 객체를 생성합니다.
    - 스트림 설정: `rs.config()`를 사용해 스트림을 설정합니다.
    - 파이프라인 시작: `pipeline.start(config)`로 스트리밍을 시작합니다.
    - 프레임 처리: `pipeline.wait_for_frames()`로 실시간 데이터를 처리합니다.
    - 파이프라인 종료: `pipeline.stop()`으로 스트리밍을 중지합니다.


```python
config = rs.config()
```
- 이거는 **RealSense 카메라의 설정을 정의하는 객체**
- 스트림을 설정, 데이터의 해상도, 프레임 속도 등을 지정하는 역할

    > 이거는 이제 밑에있는 코드랑 연결이되는데

```python
# RGB와 Depth 스트림 모두 활성화
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # RGB 스트림 설정
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)   # 깊이(Deth) 스트림 설정
```
- `rs.stream.color`: RGB 이미지 스트림을 활성화합니다.
- `rs.stream.depth`: Depth 이미지 스트림을 활성화합니다.
    1. **640x480**: 스트리밍 해상도를 설정합니다.
    2. **30fps**: 프레임 속도를 설정합니다. 즉, 1초에 30번 데이터를 캡처하고 전송합니다.
    3. `rs.format.bgr8`: RGB 이미지를 BGR 8비트 형식으로 설정합니다.
    4. `rs.format.z16`: 깊이 이미지를 16비트 형식으로 설정합니다.

✏️ `format`의 역할
- 카메라가 캡처한 각 프레임의 데이터 형식을 정의(인코딩할지와 그에 따른 메모리 크기와 정확도)
    - 인코딩은 데이터를 특정 형식으로 변환하는 과정
    - 이미지 인코딩: 카메라에서 찍은 사진은 원본 데이터(예: 빛의 강도)를 픽셀 값으로 변환하고, 그 픽셀 값은 0~255 범위의 8비트 데이터로 저장될 수 있습니다.
        - 인코딩은 **"빛의 강도"**를 0~255라는 수치로 변환하여 파일로 저장하는 것입니다.
    - 음악 인코딩: 음악을 MP3 파일로 저장할 때, 음악의 아날로그 신호를 디지털 값으로 변환하여 파일 형식에 맞게 저장합니다. <br>
    📉 인코딩의 목적은 데이터를 효율적으로 저장하거나 전송할 수 있도록 형식을 맞추는 것입니다. 

<br>
📗 잠깐!! 잠깐!! 왜? 🤔 하필 RGB를 8비트로 한거죠? 그리고 깊이는 왜 16비트로 한거죠??

- 2^8 = 256이다 보통 RGB(red, green, blue)라고 했을 때 하나의 픽셀에 값이 0 ~ 255에 값이다 16비트로 하면 색살의 차이를 좀 더 세밀하게 할 수 있겠지만 메모리가 커질 수가 있어서 RGB 규격에 맞게 사용하자.
- 16비트 이미지는 0~65535 범위의 색상을 표현하므로, 각 채널당 65536가지 색상을 사용할 수 있습니다. 이로 인해 색상 차이가 더 세밀하게 표현됩니다.


```python
# 카메라 시작
pipeline.start(config)
```
- 카메라 스트리밍을 시작
- 데이터를 실시간으로 캡처하기 시작하는 명령

