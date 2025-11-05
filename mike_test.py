import speech_recognition as sr

def recognize_once():
    r = sr.Recognizer()

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
