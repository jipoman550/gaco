# 🚀 gaco - Git Auto COmmit

> `git diff`를 분석하여 Gemini API를 통해 최적화된 커밋 메시지와 상세 설명을 자동 생성하는 CLI 도구

---

## 📋 프로젝트 개요

- **프로그램 명:** `gaco` (Git Auto COmmit)
- **목적:** AI 기반 스마트 커밋 메시지 자동 생성
- **개발 환경:** Windows 11 (WSL2/PowerShell), Python 3.10+

---

## 🛠️ 기술 스택

| 분류 | 기술 | 용도 |
|------|------|------|
| Core | Python 3.10+ | 주 로직 구현 |
| Git Interface | subprocess | 시스템 Git 명령 실행 |
| LLM API | google-generativeai | Gemini API 연동 |
| Env 관리 | python-dotenv | API Key 관리 |

---

## 📁 프로젝트 구조

```
gaco/
├── gaco.py           # 메인 CLI 도구
├── GEMINI.md         # LLM 커밋 메시지 컨벤션 가이드라인
├── INSTRUCTIONS.md   # 개발 지침 문서
├── README.md         # 프로젝트 문서
├── requirements.txt  # Python 의존성 목록
└── .env              # API 키 (환경변수)
```

---

## 🗺️ 구현 계획 (Implementation Plan)

### Phase 1: 핵심 인프라 구축

- [ ] **1.1 환경 설정 모듈**
  - `.env` 파일에서 `GEMINI_API_KEY` 로드
  - API 키 유효성 검사 함수

- [ ] **1.2 에러 처리 유틸리티**
  - 커스텀 예외 클래스 정의
  - 사용자 친화적 에러 메시지 출력 함수

---

### Phase 2: Git 인터페이스 모듈

- [ ] **2.1 Git 저장소 검증**
  - 현재 디렉토리가 Git 저장소인지 확인
  - `.git` 폴더 존재 여부 검사

- [ ] **2.2 Diff 추출 기능**
  - `git diff --cached` 실행
  - Staged 변경사항 추출 및 반환

- [ ] **2.3 커밋 실행 기능**
  - `git commit -m` 명령 실행
  - 커밋 결과 출력

---

### Phase 3: LLM 연동 모듈

- [ ] **3.1 컨텍스트 로더**
  - `GEMINI.md` 파일 읽기
  - System Prompt로 변환

- [ ] **3.2 Gemini API 클라이언트**
  - API 초기화 및 모델 설정
  - 프롬프트 전송 및 응답 수신

- [ ] **3.3 프롬프트 엔지니어링**
  - System Prompt + Diff 조합
  - 최적화된 커밋 메시지 생성 요청

---

### Phase 4: 사용자 인터페이스

- [ ] **4.1 CLI 메인 루프**
  - 생성된 메시지 터미널 출력
  - 사용자 입력 대기 (y/n/e)

- [ ] **4.2 사용자 상호작용 처리**
  - `y`: 커밋 승인 및 실행
  - `n`: 취소 및 종료
  - `e`: 메시지 수정 모드

---

### Phase 5: 통합 및 테스트

- [ ] **5.1 모듈 통합**
  - 전체 워크플로우 연결
  - 엔트리포인트 구현

- [ ] **5.2 엣지 케이스 테스트**
  - Git 저장소 아닌 경우
  - Staged 파일 없는 경우
  - API 키 누락/무효
  - 네트워크 오류

---

## ⚡ 핵심 워크플로우

```
1. GEMINI.md 로드 → System Prompt 설정
2. git diff --cached → 변경사항 추출
3. System Prompt + Diff → Gemini API 전송
4. 생성된 메시지 출력 → (y/n/e) 선택 대기
5. 승인 시 → git commit -m 실행
```

---

## 🎯 설계 원칙

- **단일 책임:** 하나의 함수는 하나의 일만 수행
- **Type Hinting:** 모든 함수에 타입 힌트 적용
- **견고한 에러 처리:** 모든 예외 상황 대응
- **UTF-8 인코딩:** 파일 I/O 시 인코딩 명시
- **효율적 리소스 관리:** 임베디드 스타일 메모리 관리

---

## 📝 사용법 (예정)

```bash
# 변경사항 스테이징
git add .

# gaco 실행
python gaco.py

# 결과 예시
# ✨ 생성된 커밋 메시지:
# feat: Add user authentication module
#
# - Implement login/logout functionality
# - Add JWT token validation
# - Create user session management
#
# [y] 승인  [n] 거절  [e] 수정
```

---

## 📄 라이선스

MIT License
