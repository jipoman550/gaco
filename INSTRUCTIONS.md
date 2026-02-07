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
| **LLM API** | `google-generativeai` | Gemini API 연동 |
| **Env 관리** | `python-dotenv` | `.env` 파일의 API Key 관리 |

---

## 3. 설계 원칙 (Coding Standards - The 42 Way)

* **Modularization:** 모든 기능은 함수 단위로 쪼개며, **하나의 함수는 하나의 일**만 수행한다.
* **Error Handling:** 아래 예외 상황에 대해 견고한 처리를 포함한다.
* 현재 디렉토리가 Git 저장소가 아닐 때.
* Staged된 변경 사항(`git add`)이 없을 때.
* Gemini API 키가 유효하지 않거나 네트워크 연결이 끊겼을 때.
* `GEMINI.md`(컨벤션 파일)가 존재하지 않을 때.


* **Clean Code:** 변수명은 명확하게 지정하고, 불필요한 주석은 배제하되 **코드 자체로 논리를 설명**한다.

---

## 4. 핵심 기능 워크플로우 (Functional Workflow)

1. **Context Loading:** `GEMINI.md` 파일을 읽어 LLM의 `System Prompt`로 설정한다.
2. **Diff Extraction:** `git diff --cached` 명령을 실행해 변경 사항을 가져온다.
3. **Prompt Engineering:** `System Prompt`와 `Diff Result`를 조합하여 Gemini에게 전달한다.
4. **Interaction:** 생성된 메시지를 터미널에 출력하고, 사용자가 `(y/n/e)` (승인/거절/수정) 중 선택하게 한다.
5. **Execution:** 사용자가 승인하면 `git commit -m`을 실제로 실행한다.

---

## 5. Antigravity 에이전트를 위한 특별 지시

* **Type Hinting:** 모든 함수의 인자와 반환값에 파이썬 타입 힌트를 적극적으로 사용해라.
* **Resource Management:** 임베디드 개발자 스타일의 효율적인 메모리 및 리소스 관리를 고려해라.
* **Encoding:** 파일 입출력 시 인코딩(`UTF-8`) 문제를 방지하는 로직을 필수로 포함해라.
* **Documentation:** 각 코드 블록, 함수, 클래스마다 독스트링(Docstring)과 주석을 활용하여 구조를 명확히 설명해라.
