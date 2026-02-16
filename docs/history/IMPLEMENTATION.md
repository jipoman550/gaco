# 🎉 gaco 구현 보고서 (Living Document)

> **Last Updated: 2026-02-14**
> 이 문서는 프로젝트의 현재 상태를 반영하는 **살아있는 문서**입니다. 새로운 기능이 추가되거나 구조가 변경될 때마다 업데이트됩니다.

---

## 🕒 최근 변경 사항 (Changelog)

### v1.3.0 — 모듈화 리팩토링 (Phase 6) (2026-02-14)
- **Architecture**: 단일 파일(`gaco.py`)에서 패키지 구조(`src/gaco/`)로 분리
- **Core**: `core/config.py`, `core/git.py`, `core/utils.py`, `core/exceptions.py`로 핵심 로직 분리
- **Services**: `services/llm.py`로 Gemini API 연동 로직 분리
- **UI**: `ui/terminal.py`, `ui/editor.py`로 사용자 인터페이스 로직 분리
- **Entry Point**: `main.py` (Facade) 도입 및 `gaco` wrapper script 수정

### v1.2.0 — 철갑 디코딩 적용 (2026-02-14)
- `safe_decode()` 함수 추가: UTF-8 → CP949 → Replace 순으로 자동 디코딩
- `get_staged_diff()`: `text=True` 대신 바이너리 모드로 diff를 가져온 뒤 `safe_decode` 적용
- `execute_commit()`: 커밋 결과 및 에러 메시지 출력 시 `safe_decode` 적용

### v1.1.0 — 메시지 수정 기능 개선 (2026-02-14)
- 기존 터미널 직접 입력 방식에서 시스템 편집기(`nvim`/`vim`) 호출 방식으로 변경
- 환경 변수 `EDITOR`를 통한 동적 편집기 선택 로직 구현

---

## 🧠 현재 고민 중인 부분

- **단위 테스트:** 모듈화가 완료되었으므로 `pytest` 도입이 시급함. `tests/` 디렉토리와 Mock 객체 활용 전략 수립 필요.
- **설정 파일:** `.env` 외에 `.gacorc` 등을 통한 사용자 정의 프롬프트 지원 여부.
- **패키징:** `pyproject.toml`을 추가하여 `pip install gaco` 형태로 배포할지 결정 필요.

---

## 🗺️ 로드맵 (Roadmap)

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 1~5 | 핵심 기능 구현 (API, Git, UI, 통합) | ✅ 완료 |
| Phase 6 | 모듈화 리팩토링 (`gaco.py` 분리) | ✅ 완료 |
| Phase 7 | 단위 테스트 (pytest + mock) | 📋 계획 |
| Phase 8 | CLI 옵션 추가 (`--dry-run`, `--model` 등) | 💡 아이디어 |
| Phase 9 | pip 패키지화 (`pyproject.toml`) | 💡 아이디어 |

---

## 📦 파일 구조

```
gaco/
├── gaco                 # Wrapper script (Linux/Mac)
├── gaco.bat             # Wrapper script (Windows)
├── src/
│   └── gaco/
│       ├── __init__.py
│       ├── main.py            # Entry Point (Facade)
│       ├── core/
│       │   ├── config.py      # Env & Context Loading
│       │   ├── exceptions.py  # Custom Exceptions
│       │   ├── git.py         # Git subprocess wrappers
│       │   └── utils.py       # safe_decode, print_error
│       ├── services/
│       │   └── llm.py         # Gemini API Integration
│       └── ui/
│           ├── editor.py      # System Editor Integration
│           └── terminal.py    # CLI Interaction
├── GEMINI.md            # LLM System Prompt
├── INSTRUCTIONS.md      # Development Guidelines
├── IMPLEMENTATION.md    # Living Document (This file)
├── README.md            # Project Documentation
├── requirements.txt     # Dependencies
├── test_sample.py       # Minimal test sample
└── .env                 # API Key (gitignored)
```

---

## 📊 모듈별 역할 요약

| 모듈 | 파일 | 역할 |
|------|------|------|
| **Core** | `core.config` | 설정 로드 (.env, GEMINI.md) 및 경로 해결 |
| | `core.git` | Git 명령 실행 및 결과 파싱 |
| | `core.utils` | 공통 유틸리티 (인코딩, 에러출력) |
| | `core.exceptions` | 커스텀 예외 정의 |
| **Services** | `services.llm` | AI 모델 연동 및 프롬프트 생성 |
| **UI** | `ui.terminal` | 사용자 입력/출력 처리 |
| | `ui.editor` | 외부 편집기 실행 및 결과 캡처 |
| **Main** | `main.py` | 전체 워크플로우 제어 (Facade) |
