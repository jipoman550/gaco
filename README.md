# gaco - Git Auto COmmit

AI 기반 스마트 커밋 메시지 자동 생성 CLI 도구

## 주요 기능

- ✅ Git diff 자동 분석[cite: 4]
- ✅ 로컬 AI (Ollama - Qwen2.5-Coder-3B) 기반 완전 무료 연동 지원
- ✅ 42 클러스터 PC 및 개인 노트북(WSL2 NAT) 완벽 호환 원격 서버 바인딩
- ✅ 사용자 친화적인 대화형 인터페이스[cite: 4]
- ✅ Windows 및 Ubuntu WSL 지원[cite: 4]
- ✅ 패키지 구조 리팩토링 및 가상환경(venv) 기반 모듈화 완료
- ✅ 다중 인코딩 자동 감지 (UTF-8, CP949)[cite: 4]

## 사용 방법

```bash
# 가상환경 활성화 (최초 1회 필요)
source .venv/bin/activate

# 파일 변경 후
git add .[cite: 4]

# gaco 실행
python src/main.py

```

### 🌍 글로벌 설정 (어디서든 실행하기)

`gaco` 폴더를 매번 복사할 필요 없이, 어디서든 실행할 수 있도록 설정할 수 있습니다.

#### Ubuntu / WSL / Mac

`~/.bashrc` 또는 `~/.zshrc` 파일에 가상환경과 패키지 진입점을 매핑한 alias를 추가하세요:

```bash
# gaco 경로를 실제 설치 경로로 변경해주세요
alias gaco='source /path/to/your/gaco/.venv/bin/activate && python3 /path/to/your/gaco/src/main.py'

```

적용 후:

```bash
source ~/.zshrc
cd /path/to/any/project
gaco

```

## 설치 및 인프라 구축

### 1. 의존성 설치

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

### 2. 로컬 AI 서버 가동 (Ollama)

노트북 환경(WSL2 NAT)에서는 외부 해커의 자원 도용을 차단하기 위해 **127.0.0.1**로 내부 봉인 후 가동합니다.

* **윈도우 시스템 환경 변수**: `OLLAMA_HOST` = `127.0.0.1` 등록
* **윈도우 CMD/PowerShell에서 Ollama 실행**:

```powershell
  $env:OLLAMA_HOST="0.0.0.0"
  ollama run qwen2.5-coder:3b

```

*(Ollama 인프라는 내부 가상 랜카드 신호를 수락하되, 시스템 변수 단에서 외부 Wi-Fi 접속을 차단하는 안전한 찰떡 세팅입니다.)*

## 환경 설정

프로젝트 루트의 `.env` 파일은 이제 로컬 AI용 더미 키로 구동됩니다. (실제 키 유출 위험 0%)

```text
GEMINI_API_KEY=ollama-local-dummy-key

```

## 🗺️ 로드맵 (Roadmap)

* [x] **Phase 1~5:** 핵심 기능 구현 완료 (API, Git, UI, 통합)


* [x] **v1.1.0:** 시스템 편집기를 통한 메시지 수정 기능


* [x] **v1.2.0:** 철갑 디코딩 — 다중 인코딩 자동 감지


* [x] **Phase 6:** 모듈화 리팩토링 및 패키지 구조 전환 (`src/main.py`)
* [x] **v1.3.0:** Ollama 로컬 런타임 탑재 및 WSL2 NAT 하이브리드 네트워크 연동 (보안 강화)
* [ ] **Phase 7:** 단위 테스트 (pytest + mock)


* [ ] **Phase 8:** CLI 옵션 추가 (`--dry-run`, `--model` 등)


* [ ] **Phase 9:** pip 패키지화 (`pyproject.toml`)



## 테스트 완료

* ✅ Windows 환경 테스트 완료


* ✅ Ubuntu WSL2 NAT 환경 테스트 & VS Code 원격 연동 안정화 완료
* ✅ 42 클러스터 PC 백그라운드 매크로 호환성 증명
* ✅ Deprecated 경고 및 OpenAI 최신 SDK 마이그레이션 완료

## 📚 문서 안내

| 문서 | 역할 |
|:---|:---|
| `README.md` | 프로젝트 소개 및 사용법 (이 문서) |
| `docs/dev/INSTRUCTIONS.md` | 설계 원칙, 기술 스택, 코딩 표준 |
| `docs/history/IMPLEMENTATION.md` | 구현 상세, Changelog, Roadmap |
| `docs/config/GEMINI.md` | 커밋 메시지 컨벤션 (LLM System Prompt) |
| `docs/history/TEST_RESULTS.md` | 테스트 환경 및 결과 증명 |
