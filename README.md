# gaco - Git Auto COmmit

AI 기반 스마트 커밋 메시지 자동 생성 CLI 도구

## 주요 기능

- ✅ Git diff 자동 분석
- ✅ Gemini AI를 활용한 커밋 메시지 자동 생성
- ✅ 사용자 친화적인 대화형 인터페이스
- ✅ Windows 및 Ubuntu 지원
- ✅ 최신 google-genai API 사용

## 사용 방법

```bash
# 파일 변경 후
git add .

# gaco 실행
python gaco.py
# 또는
./gaco        # Ubuntu/Linux
gaco.bat      # Windows
```

## 설치

```bash
pip install -r requirements.txt
```

## 환경 설정

`.env` 파일에 Gemini API 키를 추가하세요:

```
GEMINI_API_KEY=your_api_key_here
```

## 테스트 완료

- ✅ Windows 환경 테스트 완료
- ✅ Ubuntu WSL 환경 테스트 완료
- ✅ Deprecated 경고 해결 완료
- ✅ 실행 파일 생성 완료
