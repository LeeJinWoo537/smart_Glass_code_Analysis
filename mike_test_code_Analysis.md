# 음성을 텍스트로 변환하는 코드 분석!

```bash
pip install SpeechRecognition pyaudio
```

```python
import speech_recognition as sr

def recognize_once():
    # 인식기 객체 생성
    r = sr.Recognizer()

    # 마이크에서 음성 입력 받기
    with sr.Microphone() as source:
        print("🎙️ 준비 완료! 말씀하세요...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print("⏳ 인식 중...")

    try:
        text = r.recognize_google(audio, language="ko-KR")
        print("📝 인식된 내용:", text)
    except sr.UnknownValueError:
        print("❗ 음성을 인식하지 못했습니다.")
    except sr.RequestError as e:
        print(f"⚠️ API 요청 에러: {e}")

def main():
    while True:
        user_input = input("\n'1'을 입력하면 녹음을 시작합니다 (종료하려면 q): ")

        if user_input == "1":
            recognize_once()
        elif user_input.lower() == "q":
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("❗ 잘못된 입력입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main()
```

```python
import speech_recognition as sr
```
- 일단 라이브러리부터 설명을 하자면!
- 이 라이브러리는 이름 그대로 “음성을 인식(Speech Recognition)” 하는 기능을 제공합니다.
> 보통은 음성를 녹음하거나 혹은 지금 현재 코드처럼 음성 데이터를 텍스트로 변환을 하는 등등 다양한 기능이 있는 라이브러리이다.

## main부터 봐보자!
```python
def main():
    while True:
        user_input = input("\n'1'을 입력하면 녹음을 시작합니다 (종료하려면 q): ")

        if user_input == "1":
            recognize_once()
        elif user_input.lower() == "q":
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("❗ 잘못된 입력입니다. 다시 시도하세요.")
```
- `main`에서 첫번째로 보이는 `while`문 이거는 계속 반복을 하겠다는건데 `True`를 사용함으로써 계속 중간 특정 이벤트가 발생해서 `break`를 실행하지 않는 이상은 계속 실행을 하겠다라는 뜻
- 그 밑에 보이는 input은 사용자 입력을 할 수 있는 파이썬 함수이다.
- 그리고 그 밑에 보이는건 해당 사용자가 입력을 **1**를 입력하면 `if`에서 `recognize_once()`함수를 실행을 하고 **q**를 입력하면 `elif`가 실행이되서 종료를 하고 **1**과 **q**입력말고 다른걸 입력하면 `else`가 실행이 된다.

## 🤔으잉? 근데 저 `user_input.lower()` 이것중에 `.lower()`은 뭐야??
🧩 `lower()` 란?
- `lower()`는 **문자열(string)** 객체의 내장 메서드로,
- 해당 문자열 안의 모든 대문자를 소문자로 바꿔주는 기능을 합니다.

🔍 예를 들어서
```python
text = "Hello World"
print(text.lower())   # 출력: "hello world"
```
즉,     <br>
- `"Q".lower()` → `"q"`
- `"q".lower()` → `"q"`
- `"Quit".lower()` → `"quit"`   

이런 식으로 대문자든 소문자든 상관없이 결과가 전부 소문자가 돼요.       <br>
그니까 한마디로 이야기하자면 사요자가 입력을 했을 때 `q`를 입력하든 `Q`를 입력하든 종료를 하겠다라는 뜻


## `recognize_once()` 함수를 알아보자!
```python
r = sr.Recognizer()
```
- `speech_recognition` 라이브러리 안의 `Recognizer` 클래스를 이용해서
- “음성을 텍스트로 변환할 수 있는 인식기 객체”를 하나 생성하는 거예요.

-----------------------------
🧩 `Recognizer` 클래스란?

`Recognizer`는 **SpeechRecognition** 라이브러리에서 음성 인식 기능을 담당하는 주요 클래스예요.

이 객체(r)를 이용하면:
- 마이크나 음성 파일로부터 입력받은 음성을 듣고(`listen`)
- 그 음성을 텍스트로 변환(`recognize_google`, `recognize_sphinx` 등) 할 수 있습니다.
------------------------------

### 1️⃣ `with sr.Microphone() as source:`
- **역할:** 마이크를 열어서 음성을 입력 받을 준비를 하는 부분
- `sr.Microphone()`은 마이크를 나타내는 클래스예요.
- `with`를 쓰는 이유:
    - 블록이 끝나면 자동으로 마이크를 닫아서 자원을 안전하게 해제
    - 예외가 나도 마이크가 닫히도록 보장
`with`에 대해서 조금 더 설명을 하자면
`with`는 **컨텍스트 매니저(Context Manager)**를 사용할 때 쓰는 키워드예요.
- 무엇을 하는가:
    “블록 안에서 어떤 자원을 사용하고, 블록이 끝나면 자동으로 정리해라”
- 즉, 자원 관리를 편하게 해주는 문법
```python
with 객체 as 이름:
    # 블록 안에서 객체 사용
    ...
# 블록 끝나면 객체 자동 정리(닫기)
```
```python
with open("hello.txt", "w") as f:
    f.write("안녕하세요!")
# 블록 끝나면 f.close()가 자동으로 호출됨
```
- `open()`으로 파일을 열었지만, `with` 덕분에 블록 끝나면 자동으로 닫힘
- 안 쓰면 직접 `f.close()`를 호출해야 함
- `sr.Microphone()` → 마이크를 여는 객체
- as source → 이 객체를 source라는 이름으로 사용
- 블록 끝나면 → 자동으로 마이크 닫힘, 자원 해제     <br>
💡 덕분에 예외가 나도 마이크가 계속 켜져 있는 문제가 없음
<br>

➡️ “마이크를 열고, 음성을 받아올 준비가 되면 `source` 객체로 사용하겠다” 라는 뜻이에요.

### 2️⃣ `r.adjust_for_ambient_noise(source)`
- **역할:** 주변 배경 소음을 분석해서, 음성을 구분하기 쉽게 조정
- 내부적으로:
    - 마이크에서 잠시 소리를 듣고 평균 에너지를 계산
    - `Recognizer` 객체의 소리에너지(`energy_threshold`)를 자동 조정

- 덕분에:
    - 주변에 시끄러운 소음이 있어도 말소리를 잘 감지
    - 너무 작은 소리를 잡음으로 오인하지 않음

💡 참고: `adjust_for_ambient_noise`를 호출하지 않으면, 조용한 방에서는 좋지만 시끄러운 환경에서는 인식이 잘 안될 수 있어요.


### 3️⃣ audio = r.listen(source)

- **역할:** 실제로 사용자가 말하는 음성을 한 번 녹음
- 내부적으로:
    - 마이크에서 버퍼 단위로 음성 데이터를 읽음
    - 소리 에너지(`energy_threshold`) 기반으로 말 시작/끝 감지
    - 말을 멈추면 자동으로 녹음 종료

- 반환값: `AudioData` 객체
    - 나중에 `r.recognize_google(audio)` 등으로 텍스트 변환 가능

### 🤔으잉?? 소리에너지가 뭐야??  소리 에너지(`energy_threshold`)
- 이건 음성 인식에서 **"소리가 얼마나 커야 음성으로 인식할지"**를 결정하는 기준값(Threshold) 입니다.
> 🎧 "이 정도 이상의 소리면 사람 목소리라고 판단하고 녹음 시작!"    <br>
> 🎤 "이보다 작으면 그냥 주변 잡음(노이즈)로 무시하자"  <br>
> 이걸 구분하는 기준이에요. <br>

🔍 자세히 설명하면  <br>
🔹 energy_threshold는 “소리 세기” 기준값
- speech_recognition.Recognizer 객체가 오디오 신호의 에너지 레벨(dB 단위로 생각하면 비슷한 개념) 을 측정합니다.
- 기본값은 보통 300~400 정도입니다.
- 숫자가 낮으면 → 작은 소리도 “음성”으로 감지
- 숫자가 높으면 → 큰 소리만 “음성”으로 감지

```python
try:
    text = r.recognize_google(audio, language="ko-KR")
    print("📝 인식된 내용:", text)
except sr.UnknownValueError:
    print("❗ 음성을 인식하지 못했습니다.")
except sr.RequestError as e:
    print(f"⚠️ API 요청 에러: {e}")
```
**try 블록:**
- “이 안의 코드를 실행해보고, 문제가 생기면 예외 처리하겠다”는 의미

**except 블록:**
- 특정 오류가 발생하면 어떻게 처리할지 정의

1️⃣ `r.recognize_google(audio, language="ko-KR")`
- `r` → `Recognizer` 객체
- `audio` → `r.listen()`으로 녹음한 음성 데이터 (`AudioData` 객체)
- `language="ko-KR"` → 구글 음성 인식 API에 한국어로 인식하도록 지시

💡 **실제 동작:**
- 구글 서버로 음성 데이터를 보내고
- 텍스트로 변환된 결과를 반환

그 다음에 인식된 내용을 출력
`print("📝 인식된 내용:", text)`
- 음성이 성공적으로 인식되면 결과 출력

**예시:**   <br>
📝 인식된 내용: 안녕하세요, 오늘 날씨 어때요?

1️⃣ `recognize_google()`의 역할
```python
text = r.recognize_google(audio, language="ko-KR")
```
- `Recognizer` 객체(`r`)가 가진 메서드 중 하나
- 내부적으로 구글의 음성 인식 **API(Google Speech Recognition API)** 를 사용해서 음성을 텍스트로 변환
- 입력: `AudioData` (마이크나 파일에서 녹음한 음성)
- 출력: 변환된 텍스트 문자열    <br>
즉, 내 컴퓨터에서 알아서 변환하는 게 아니라, 구글 서버에 보내서 처리하는 방식이에요.
그래서 온라인 그니까 인터넷이 연결이 되어야 구글서버로 전송이 가능 만약에 인터넷이 끊기면
`sr.RequestError` 발생
<br> <br>

2️⃣ **참고: 오프라인 방법도 있음**
- `recognize_google()`은 온라인 방식
- **오프라인 음성 인식**도 가능
    - 예: `recognize_sphinx()` (PocketSphinx 기반), 혹은 vosk형식
    - 장점: 인터넷 필요 없음
    - 단점: 정확도가 구글 API보다 낮을 수 있음

```python
except sr.UnknownValueError:
    print("❗ 음성을 인식하지 못했습니다.")
```
- `speech_recognition` 라이브러리에서 제공하는 **예외 클래스(Exception)**
- 의미: **음성은 들어왔지만, 인식기가 내용을 이해하지 못했다**  <br>
즉, "오디오 데이터 자체는 정상적이지만, 텍스트로 변환할 수 없음” 상황에 사용됩니다.

**언제 발생할까?**  <br>
🔹 **흔한 경우**
1. **발음이 너무 불분명할 때**
    - 중얼거림, 소리가 작음

2. **배경 소음이 심할 때**
    - 시끄러운 카페, 길거리 등

3. **짧거나 의미 없는 소리일 때**
    - “음…”, “으…” 같은 경우

다른 오프라인 음성을 텍스트로 변환!
vosk는
1. Vosk는 "음소 단위" 인식만 합니다
- Vosk는 Kaldi 기반으로,
- 소리를 단어가 아니라 음소(소리의 최소 단위) 단위로 인식해
- 모델이 학습한 단어 확률에 따라 조합합니다.    <br>
그래서 약간 맞춤법이라든가 띄어쓰기가 잘 안됌 인식도 잘 될때가 있고 안될때가 있음