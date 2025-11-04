from gtts import gTTS
import pygame
import io

# 텍스트
text = "안녕하세요, gTTS를 사용한 음성 변환 예제입니다."

# gTTS 객체 생성
tts = gTTS(text=text, lang='ko')

# 음성을 메모리에서 바로 재생하기 위한 바이너리 데이터로 변환
fp = io.BytesIO()
#tts.save(fp)
tts.write_to_fp(fp)   # ✅ 올바른 방식
fp.seek(0)

# pygame 초기화
pygame.mixer.init()

# pygame을 사용해 음성 재생
pygame.mixer.music.load(fp, 'mp3')
pygame.mixer.music.play()

# 음성이 끝날 때까지 대기
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
