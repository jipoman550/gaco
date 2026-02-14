# 🎉 gaco 구현 보고서 (Living Document)

> **Last Updated: 2026-02-14**
> 이 문서는 프로젝트의 현재 상태를 반영하는 **살아있는 문서**입니다. 새로운 기능이 추가되거나 구조가 변경될 때마다 업데이트됩니다.

---

## 🕒 최근 변경 사항 (Changelog)

### v1.2.0 — 철갑 디코딩 적용 (2026-02-14)
- `safe_decode()` 함수 추가: UTF-8 → CP949 → Replace 순으로 자동 디코딩
- `get_staged_diff()`: `text=True` 대신 바이너리 모드로 diff를 가져온 뒤 `safe_decode` 적용
- `execute_commit()`: 커밋 결과 및 에러 메시지 출력 시 `safe_decode` 적용
- `load_gemini_context()`: `GEMINI.md`를 바이너리로 읽어 `safe_decode`로 디코딩
- `edit_commit_message()`: 편집된 임시 파일을 `safe_decode`로 읽기

### v1.1.0 — 메시지 수정 기능 개선 (2026-02-14)
- 기존 터미널 직접 입력 방식에서 시스템 편집기(`nvim`/`vim`) 호출 방식으로 변경
- 환경 변수 `EDITOR`를 통한 동적 편집기 선택 로직 구현
- 임시 파일(`tempfile`)을 활용한 안전한 텍스트 편집 워크플로우 적용

### v1.0.0 — 초기 구현 완료
- Phase 1~5 전체 구현
- Gemini API 연동 및 프롬프트 엔지니어링
- `y/n/e` 사용자 상호작용 CLi
- 글로벌 실행을 위한 `gaco` 쉘 스크립트 및 `gaco.bat` 래퍼 추가
- Windows UTF-8 인코딩 강제 설정

---

## 🧠 현재 고민 중인 부분

- **모듈화 구조:** 현재 ~480줄의 `gaco.py`를 `core/`, `services/`, `ui/`로 어떻게 깔끔하게 쪼갤 것인가? (디자인 패턴 적용 고민 중)
- **테스트 코드:** `test_sample.py`는 더미 파일. 실질적인 단위 테스트(mock 기반) 도입 필요
- **커밋 메시지 품질:** Gemini가 가끔 ` ``` `을 메시지 앞뒤에 붙이는 문제 → `GEMINI.md` 주의사항에 추가 완료

---

## 🗺️ 로드맵 (Roadmap)

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 1~5 | 핵심 기능 구현 (API, Git, UI, 통합) | ✅ 완료 |
| Phase 6 | 모듈화 리팩토링 (`gaco.py` 분리) | 📋 계획 |
| Phase 7 | 단위 테스트 (pytest + mock) | 📋 계획 |
| Phase 8 | CLI 옵션 추가 (`--dry-run`, `--model` 등) | 💡 아이디어 |
| Phase 9 | pip 패키지화 (`setup.py` / `pyproject.toml`) | 💡 아이디어 |

---

## ✅ 구현 완료 항목

### Phase 1: 핵심 인프라 구축 ✓

#### 1.1 환경 설정 모듈
- ✅ `load_api_key()`: .env 파일에서 GEMINI_API_KEY 로드
- ✅ API 키 유효성 검사 (빈 값, None 체크)
- ✅ 명확한 에러 메시지 제공

#### 1.2 에러 처리 유틸리티
- ✅ `GacoError`: 기본 예외 클래스
- ✅ `GitNotFoundError`: Git 저장소 없음
- ✅ `NoStagedChangesError`: Staged 변경사항 없음
- ✅ `APIKeyError`: API 키 관련 오류
- ✅ `GeminiFileNotFoundError`: GEMINI.md 파일 없음
- ✅ `print_error()`: 사용자 친화적 에러 메시지 출력

---

### Phase 2: Git 인터페이스 모듈 ✓

#### 2.1 Git 저장소 검증
- ✅ `is_git_repository()`: .git 폴더 존재 여부 확인

#### 2.2 Diff 추출 기능
- ✅ `get_staged_diff()`: git diff --cached 실행
- ✅ `safe_decode()`를 통한 다중 인코딩 폴백 디코딩
- ✅ subprocess를 통한 안전한 명령 실행 (바이너리 모드)

#### 2.3 커밋 실행 기능
- ✅ `execute_commit()`: git commit -m 실행 (safe_decode 적용)

---

### Phase 3: LLM 연동 모듈 ✓

#### 3.1 컨텍스트 로더
- ✅ `load_gemini_context()`: GEMINI.md 파일 읽기 (safe_decode 적용)

#### 3.2 Gemini API 클라이언트
- ✅ `initialize_gemini_client()`: API 초기화
- ✅ gemini-2.5-flash 모델 사용

#### 3.3 프롬프트 엔지니어링
- ✅ `generate_commit_message()`: 커밋 메시지 생성
- ✅ System Prompt + Diff 조합

---

### Phase 4: 사용자 인터페이스 ✓

- ✅ `display_commit_message()`: 메시지 출력
- ✅ `get_user_choice()`: y/n/e 입력 받기
- ✅ `edit_commit_message()`: 시스템 편집기를 통한 메시지 수정
- ✅ `handle_user_interaction()`: 전체 상호작용 관리

---

### Phase 5: 통합 및 테스트 ✓

- ✅ `main()`: 전체 워크플로우 통합
- ✅ 5단계 진행 상황 표시
- ✅ 모든 엣지 케이스 예외 처리

---

## 📊 코드 구조 분석

### 함수별 역할

| 함수명 | 역할 | Phase |
|--------|------|-------|
| `load_api_key()` | API 키 로드 및 검증 | 1.1 |
| `print_error()` | 에러 메시지 출력 | 1.2 |
| `safe_decode()` | 다중 인코딩 안전 디코딩 | 2.0 |
| `is_git_repository()` | Git 저장소 확인 | 2.1 |
| `get_staged_diff()` | Staged 변경사항 추출 | 2.2 |
| `execute_commit()` | 커밋 실행 | 2.3 |
| `load_gemini_context()` | GEMINI.md 로드 | 3.1 |
| `initialize_gemini_client()` | Gemini API 초기화 | 3.2 |
| `generate_commit_message()` | 커밋 메시지 생성 | 3.3 |
| `display_commit_message()` | 메시지 출력 | 4.1 |
| `get_user_choice()` | 사용자 선택 입력 | 4.2 |
| `edit_commit_message()` | 편집기로 메시지 수정 | 4.2 |
| `handle_user_interaction()` | 상호작용 관리 | 4.2 |
| `main()` | 메인 엔트리포인트 | 5.1 |

### 전체 라인 수
- **총 라인:** ~476줄
- **함수:** 14개
- **커스텀 예외 클래스:** 5개

---

## 📦 파일 구조

```
gaco/
├── gaco.py              # 메인 CLI 도구 (~476줄)
├── gaco                 # Linux/Mac 실행 스크립트 (wrapper)
├── gaco.bat             # Windows 실행 스크립트 (wrapper)
├── GEMINI.md            # 커밋 메시지 컨벤션 가이드 (LLM System Prompt)
├── INSTRUCTIONS.md      # 개발 지침 및 설계 원칙
├── IMPLEMENTATION.md    # 이 문서 (Living Document)
├── README.md            # 프로젝트 소개 및 사용법
├── requirements.txt     # Python 의존성 (google-genai, python-dotenv)
├── test_sample.py       # 테스트용 샘플 파일
├── .env                 # API 키 설정 (gitignored)
└── .gitignore           # Git 무시 패턴
```

---

## 🎨 코드 품질 특징

### 1. Type Hinting
```python
def load_api_key() -> str:
def get_staged_diff() -> str:
def safe_decode(binary_data: bytes) -> str:
def handle_user_interaction(commit_message: str) -> Tuple[bool, str]:
```

### 2. 계층적 에러 처리
```python
try:
    # 작업 수행
except GacoError as e:
    # gaco 관련 예외
except KeyboardInterrupt:
    # Ctrl+C 처리
except Exception as e:
    # 예상치 못한 예외
```

### 3. 철갑 디코딩 (safe_decode 패턴)
```python
def safe_decode(binary_data: bytes) -> str:
    for encoding in ['utf-8', 'cp949']:
        try:
            return binary_data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return binary_data.decode('utf-8', errors='replace')
```
- 모든 외부 바이너리 입력에 적용
- 프로그램 중단 없이 최대한 복원

### 4. 리소스 관리
- Context Manager(`with`)로 파일 자동 닫기
- `tempfile`로 편집 후 자동 정리
- Path 객체로 크로스 플랫폼 호환

---

## 🚀 사용 방법

```bash
# 1. 환경 설정
echo "GEMINI_API_KEY=your_api_key_here" > .env
pip install -r requirements.txt

# 2. 변경사항 스테이징 후 실행
git add .
python gaco.py    # 또는 ./gaco (Linux) / gaco.bat (Windows)
```
