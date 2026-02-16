# gaco - Git Auto COmmit

AI 기반 스마트 커밋 메시지 자동 생성 CLI 도구

## 주요 기능

- ✅ Git diff 자동 분석
- ✅ Gemini AI를 활용한 커밋 메시지 자동 생성
- ✅ 사용자 친화적인 대화형 인터페이스
- ✅ Windows 및 Ubuntu 지원
- ✅ 최신 google-genai API 사용
- ✅ 다중 인코딩 자동 감지 (UTF-8, CP949)

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

## 🗺️ 로드맵 (Roadmap)

- [x] **Phase 1~5:** 핵심 기능 구현 완료 (API, Git, UI, 통합)
- [x] **v1.1.0:** 시스템 편집기를 통한 메시지 수정 기능
- [x] **v1.2.0:** 철갑 디코딩 — 다중 인코딩 자동 감지
- [ ] **Phase 6:** 모듈화 리팩토링 (`gaco.py` → 패키지 구조)
- [ ] **Phase 7:** 단위 테스트 (pytest + mock)
- [ ] **Phase 8:** CLI 옵션 추가 (`--dry-run`, `--model` 등)
- [ ] **Phase 9:** pip 패키지화 (`pyproject.toml`)

## 테스트 완료

- ✅ Windows 환경 테스트 완료
- ✅ Ubuntu WSL 환경 테스트 완료
- ✅ Deprecated 경고 해결 완료
- ✅ 실행 파일 생성 완료

## 📚 문서 안내

| 문서 | 역할 |
|------|------|
| `README.md` | 프로젝트 소개 및 사용법 (이 문서) |
| `docs/dev/INSTRUCTIONS.md` | 설계 원칙, 기술 스택, 코딩 표준 |
| `docs/history/IMPLEMENTATION.md` | 구현 상세, Changelog, Roadmap |
| `docs/config/GEMINI.md` | 커밋 메시지 컨벤션 (LLM System Prompt) |
| `docs/history/TEST_RESULTS.md` | 테스트 환경 및 결과 증명 |
