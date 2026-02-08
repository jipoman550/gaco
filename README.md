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

### 🌍 글로벌 설정 (어디서든 실행하기)

`gaco` 폴더를 매번 복사할 필요 없이, 어디서든 실행할 수 있도록 설정할 수 있습니다.

#### Ubuntu / WSL / Mac

`~/.bashrc` 또는 `~/.zshrc` 파일에 다음 alias를 추가하세요:

```bash
# gaco 경로를 실제 설치 경로로 변경해주세요
alias gaco='python3 /path/to/your/gaco/gaco.py'
```

적용 후:
```bash
source ~/.bashrc
cd /path/to/any/project
gaco
```

#### Windows (PowerShell)

1. `gaco` 폴더 경로를 복사합니다.
2. 환경 변수 편집 > Path에 `gaco` 폴더 경로를 추가합니다.
3. 새로운 터미널을 열고 어디서든 `gaco.bat` 또는 `gaco` 명령어를 실행할 수 있습니다.

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
