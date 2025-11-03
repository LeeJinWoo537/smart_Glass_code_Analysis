# 인텔 뎁쓰 카메라 코드

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

## 📢 파이프라인이란??

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


## 🤔잠깐!! 근데 프레임은 왜 가져와야하는거지??
```python
# 프레임 가져오기
frames = pipeline.wait_for_frames()
```
- 카메라로부터 프레임을 가져오는 이유는 카메라가 실시간으로 캡처한 이미지나 깊이 데이터를 사용하여 다양한 작업을 수행하기 위해서입니다.
- 예를 들어, 실시간 이미지 처리, 물체 인식, 거리 측정 등을 하기 위해서는 카메라에서 지속적으로 데이터를 받아야 합니다.
- 프레임은 실시간 비디오의 각 한 장의 이미지  <br>
    - 예시:   <br>
        ● 물체 추적: 카메라에서 실시간으로 프레임을 가져와서, 각 프레임에서 물체를 인식하고 추적할 수 있습니다.     <br>
        ● 거리 측정: 깊이 카메라에서 실시간으로 깊이 데이터를 가져와서, 특정 물체와의 거리를 계산할 수 있습니다.       <br>
        ● 모션 감지: 연속된 프레임을 비교하여, 화면에서 움직이는 물체를 감지할 수 있습니다.
     
## 추가적으로 블록상태에 대해서도 배워보자!
- 프로그램 실행 흐름이 멈추고 대기하는 상태를 의미합니다.
- 프로그램이 특정 작업을 마칠 때까지 기다리도록 만드는 상태
<br>
비유:   <br>
    ● 블록 상태는 마치 우체국에 가서 우편물을 기다리는 상황과 비슷합니다. 우체국에 가서 우편물이 도착할 때까지 기다리는 것처럼, 프로그램은 특정 작업이 완료될 때까지 대기하는 상태입니다.

`wait_for_frames()` 함수의 블록 상태:
- pipeline.wait_for_frames()는 새로운 프레임이 준비될 때까지 기다리는 함수입니다. 카메라는 프레임을 실시간으로 캡처하지만, 새로운 프레임이 준비되지 않았을 때는 이 함수가 계속 대기하게 됩니다.
- 대기 상태에서 프로그램은 다른 작업을 하지 않고, 카메라가 새로운 프레임을 제공할 때까지 기다리게 됩니다.


## 으잉?? 새로운 프레임이라는게 무슨 의미야??
✅ 그러면 왜 "새로운 프레임"이라고 할까?
- 카메라는 계속 이미지를 보내지만,
- 프로그램 입장에서는 이전 프레임과 다른 새로 캡처된 이미지가 도착해야 처리할 수 있기 때문이야.

✅ 왜 기다려야 할까? (wait_for_frames())
이 함수는 말 그대로:
> "카메라야, 다음 장면 준비될 때까지 기다릴게"  <br>
> "준비되면 줘!"

즉, 카메라가 다음 사진을 찍어올 때까지 대기하는 것
그래야 실시간 처리가 가능해.

✅ 타이밍을 맞추기 위한 것
프레임은 그냥 막 아무 때나 처리하면 안 되고,
- 카메라가 새 이미지를 줄 때
- 그걸 받아서 처리해야 해

그래야 화면이 끊기지 않고,
지금 사람·거리·환경을 실제로 측정할 수 있어.

■ 좀 결론적으로 적으로 이야기하자면 같은 장면을 계속 찍는다고 해서 새로운 프레임이 아닌게 아니야 계속 새로운 프레임을 받는데 그 새로운 프레임을 받고 처리를 한 다음 그다음에 다음 프레임이 올 때까지 기다리는 것! 이라고 생각하면 돼!


✅ 코드 의미
```python
depth_frame = frames.get_depth_frame()
color_frame = frames.get_color_frame()
```
두 줄은 프레임 묶음(frames) 안에서
- 깊이(depth) 데이터만 꺼내오고
- 컬러(RGB) 데이터만 꺼내오는 코드야.

        변수	                   의미	                            데이터 형식
----------------------------------------------------------------------
- `depth_frame`	   카메라가 찍은 깊이(depth) 이미지 프레임	        픽셀마다 거리값(mm)
- `color_frame`	   카메라가 찍은 컬러(RGB) 이미지 프레임	        일반 색상 이미지

✅ 흐름으로 설명하면

1. `wait_for_frames()` → 카메라가 보낸 하나의 프레임 묶음 받음 (이 안에 RGB + Depth 같이 들어 있음)
2. `get_depth_frame()` → 그 묶음 중 깊이 정보만 뽑아냄
3. `get_color_frame()` → 그 묶음 중 RGB 영상만 뽑아냄

즉, 한 번에 카메라가 **두 종류의 데이터를 보내고**
우리는 거기서 **따로따로 꺼내오는 것**

🤔으잉?? 근데 왜 그러면 두 프레임을 주는거야??
 ✅ RealSense가 왜 두 프레임을 주냐?

RealSense 카메라는 **듀얼 스트림**(multi-stream) 장치야.
- RGB 카메라
- Depth 카메라

두 센서를 동시에 사용하니까
**각각의 데이터가 따로 존재**하는 거지.

```python
if not depth_frame or not color_frame:
    continue
```
- 이건 깊이 프레임이랑 RGB프레임 그니까 새로운 값이 안들어오면 그냥 넘어가겠다라는 뜻



```python
# 깊이 데이터를 Numpy 배열로 변환
depth_image = np.asanyarray(depth_frame.get_data())
color_image = np.asanyarray(color_frame.get_data())
```
✅ `depth_frame.get_data()` / `color_frame.get_data()` 는 뭐야?
`get_data()`    <br>
→ ***카메라 프레임 안에 들어있는 실제 Raw 데이터(메모리 버퍼)를 가져오는 함수***야.
- 깊이 프레임이면 → 각 픽셀별 거리값(depth)
- 컬러 프레임이면 → RGB 픽셀 값들

즉, **카메라가 센싱한 원본 데이터**를 들고오는 함수라고 보면 돼.

✅ `np.asanyarray()` 는 뭐야?
파이썬 RealSense가 제공하는 데이터는 C/C++의 메모리를 가리키는 형태야.
그걸 Python에서 쓰려면 NumPy 배열로 변환해야 하지.

- `np.array()` → 무조건 새로운 배열 생성 (복사)
- `np.asanyarray()` → 가능하면 기존 데이터를 그대로 NumPy 형태로 wrapping (복사 X)

즉, 속도가 더 빠르고 메모리를 덜 써.
RealSense처럼 스트리밍 데이터에는 `asanyarray()`가 더 적합해.
> "가능하면 원본 포인터를 유지하고, 필요하면 변환"

🤔으잉?? 복사는 무슨말이야??
✅ 예시로 이해하기
📦 원본 상자(데이터)가 있어

이 상자에 과자 100개가 들어있다고 하자.

1) 복사 O (np.array())

새로운 상자를 하나 더 만들고
과자 100개를 모두 옮겨 담는 것 → 메모리 2배 사용
```python
new_box = np.array(old_box)  # 데이터 복사 발생
```
2) 복사 X (np.asanyarray())

새 상자 안에 그냥 원래 상자를 가리키는 표지판만 꽂기
즉, 데이터는 안 옮기고 같은 메모리를 공유
```python
view = np.asanyarray(old_data)  # 복사 없이 참조
```
✅ depth_image는 뭐야?
- 바로 깊이(depth) 데이터를 담은 NumPy 배열(이미지) 이야.

✅ .shape는 뭐야?

`.shape`는 ***NumPy 배열의 크기(차원)를 알려주는 속성***이야.

예를 들어 깊이 이미지가 480x640이라면:
```python
depth_image.shape → (480, 640)
```

즉,
`height = 480`
`width = 640`

이렇게 들어가.

📌 비유     <br>
`shape`는 이미지의 "해상도"라고 생각하면 됨.