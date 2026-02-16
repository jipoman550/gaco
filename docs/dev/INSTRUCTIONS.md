# 📄 INSTRUCTIONS.md

## 1. 프로젝트 개요 (Project Overview)

* **프로그램 명:** `gaco` (Git Auto COmmit)
* **목적:** `git diff`를 분석하여 Gemini API를 통해 최적화된 커밋 메시지와 상세 설명을 자동 생성하는 CLI 도구.
* **개발 환경:** Windows 11 (WSL2 또는 PowerShell), Python 3.10 이상, Ubuntu에서도 작동되야됨.

---

## 2. 기술 스택 및 라이브러리 (Tech Stack)

| 분류 | 기술 / 라이브러리 | 용도 |
| --- | --- | --- |
| **Core** | `Python` | 주 로직 구현 |
| **Git Interface** | `subprocess` | 시스템 Git 명령 실행 (의존성 최소화) |
| **LLM API** | `google-genai` | Gemini API 연동 |
| **Env 관리** | `python-dotenv` | `.env` 파일의 API Key 관리 |

---

## 3. 설계 원칙 (Coding Standards - The 42 Way)

* **Modularization:** 모든 기능은 함수 단위로 쪼개며, **하나의 함수는 하나의 일**만 수행한다.
* **Error Handling:** 아래 예외 상황에 대해 견고한 처리를 포함한다.
    * 현재 디렉토리가 Git 저장소가 아닐 때.
    * Staged된 변경 사항(`git add`)이 없을 때.
    * Gemini API 키가 유효하지 않거나 네트워크 연결이 끊겼을 때.
    * `GEMINI.md`(컨벤션 파일)가 존재하지 않을 때.
* **철갑 디코딩 (Safe Decode):** 외부 프로세스 출력이나 파일 읽기 시 `safe_decode()` 패턴을 적용한다.
    * **규칙:** `subprocess`의 결과는 항상 바이너리(`text=False`)로 받고, `safe_decode()`로 디코딩한다.
    * **폴백 순서:** UTF-8 → CP949 → `errors='replace'` (프로그램 절대 중단 방지)
    * **적용 범위:** `get_staged_diff()`, `execute_commit()`, `load_gemini_context()`, `edit_commit_message()`
* **Clean Code:** 변수명은 명확하게 지정하고, 불필요한 주석은 배제하되 **코드 자체로 논리를 설명**한다.

---

## 4. 핵심 기능 워크플로우 (Functional Workflow)

1. **Context Loading:** `GEMINI.md` 파일을 읽어 LLM의 `System Prompt`로 설정한다.
2. **Diff Extraction:** `git diff --cached` 명령을 바이너리 모드로 실행, `safe_decode()`로 디코딩한다.
3. **Prompt Engineering:** `System Prompt`와 `Diff Result`를 조합하여 Gemini에게 전달한다.
4. **Interaction:** 생성된 메시지를 터미널에 출력하고, 사용자가 `(y/n/e)` (승인/거절/수정) 중 선택하게 한다.
5. **Execution:** 사용자가 승인하면 `git commit -m`을 실제로 실행한다.

---

## 5. 함수 목록 (Function Reference)

| 함수명 | 모듈 | 역할 |
|--------|------|------|
| `load_api_key()` | `core.config` | `.env`에서 API 키 로드 및 검증 |
| `print_error()` | `core.utils` | stderr로 에러 메시지 출력 |
| `safe_decode()` | `core.utils` | 바이너리 → 문자열 안전 디코딩 |
| `is_git_repository()` | `core.git` | `.git` 폴더 존재 여부 확인 |
| `get_staged_diff()` | `core.git` | `git diff --cached` 실행 및 디코딩 |
| `execute_commit()` | `core.git` | `git commit -m` 실행 |
| `load_gemini_context()` | `core.config` | `GEMINI.md` 로드 (System Prompt) |
| `initialize_gemini_client()` | `services.llm` | Gemini API 클라이언트 초기화 |
| `generate_commit_message()` | `services.llm` | LLM으로 커밋 메시지 생성 |
| `display_commit_message()` | `ui.terminal` | 생성된 메시지 터미널 출력 |
| `get_user_choice()` | `ui.terminal` | `y/n/e` 사용자 입력 받기 |
| `edit_commit_message()` | `ui.editor` | 시스템 편집기로 메시지 수정 |
| `handle_user_interaction()` | `ui.terminal` | 전체 사용자 상호작용 관리 |
| `main()` | `main` | 메인 엔트리포인트 (Facade) |

---

## 6. Antigravity 에이전트를 위한 특별 지시

* **Type Hinting:** 모든 함수의 인자와 반환값에 파이썬 타입 힌트를 적극적으로 사용해라.
* **Resource Management:** 임베디드 개발자 스타일의 효율적인 메모리 및 리소스 관리를 고려해라.
* **Encoding:** 파일 입출력 및 subprocess 호출 시 반드시 `safe_decode()` 패턴을 사용해라. 직접 `.decode("utf-8")`을 호출하지 말 것.
* **Documentation:** 각 코드 블록, 함수, 클래스마다 독스트링(Docstring)과 주석을 활용하여 구조를 명확히 설명해라.
* **Living Document:** 기능 추가/변경 시 `IMPLEMENTATION.md`의 Changelog와 함수 테이블을 반드시 업데이트해라.
