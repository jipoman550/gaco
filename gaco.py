#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gaco - Git Auto COmmit
AI 기반 스마트 커밋 메시지 자동 생성 CLI 도구
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Tuple

# Windows 환경에서 UTF-8 인코딩 강제 설정
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from dotenv import load_dotenv
from google import genai


# ============================================================================
# Phase 1: 핵심 인프라 구축
# ============================================================================

class GacoError(Exception):
    """gaco 프로그램의 커스텀 예외 클래스"""
    pass


class GitNotFoundError(GacoError):
    """Git 저장소를 찾을 수 없을 때 발생하는 예외"""
    pass


class NoStagedChangesError(GacoError):
    """Staged된 변경사항이 없을 때 발생하는 예외"""
    pass


class APIKeyError(GacoError):
    """API 키 관련 오류가 발생했을 때의 예외"""
    pass


class GeminiFileNotFoundError(GacoError):
    """GEMINI.md 파일을 찾을 수 없을 때 발생하는 예외"""
    pass


def load_api_key() -> str:
    """
    .env 파일에서 GEMINI_API_KEY를 로드하고 반환

    Returns:
        str: Gemini API 키

    Raises:
        APIKeyError: API 키를 찾을 수 없거나 유효하지 않을 때
    """
    # .env 파일 로드
    load_dotenv()

    # 환경변수에서 API 키 가져오기
    api_key = os.getenv("GEMINI_API_KEY")

    # API 키 유효성 검사
    if not api_key or api_key.strip() == "":
        raise APIKeyError(
            "❌ GEMINI_API_KEY를 찾을 수 없습니다.\n"
            "   .env 파일에 GEMINI_API_KEY=your_api_key 형식으로 추가해주세요."
        )

    return api_key.strip()


def print_error(message: str) -> None:
    """
    사용자 친화적인 에러 메시지를 출력

    Args:
        message: 출력할 에러 메시지
    """
    print(f"\n{message}\n", file=sys.stderr)


# ============================================================================
# Phase 2: Git 인터페이스 모듈
# ============================================================================

def is_git_repository() -> bool:
    """
    현재 디렉토리가 Git 저장소인지 확인

    Returns:
        bool: Git 저장소이면 True, 아니면 False
    """
    # .git 폴더의 존재 여부로 Git 저장소 확인
    git_dir = Path.cwd() / ".git"
    return git_dir.exists() and git_dir.is_dir()


def get_staged_diff() -> str:
    """
    git diff --cached 명령을 실행하여 Staged 변경사항 추출

    Returns:
        str: Staged된 변경사항의 diff 결과

    Raises:
        GitNotFoundError: Git 저장소가 아닐 때
        NoStagedChangesError: Staged된 변경사항이 없을 때
    """
    # Git 저장소 확인
    if not is_git_repository():
        raise GitNotFoundError(
            "❌ 현재 디렉토리는 Git 저장소가 아닙니다.\n"
            "   git init을 먼저 실행해주세요."
        )

    try:
        # git diff --cached 실행
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )

        diff_output = result.stdout.strip()

        # Staged 변경사항이 없는 경우
        if not diff_output:
            raise NoStagedChangesError(
                "❌ Staged된 변경사항이 없습니다.\n"
                "   git add <파일명>을 먼저 실행해주세요."
            )

        return diff_output

    except subprocess.CalledProcessError as e:
        raise GacoError(f"❌ Git 명령 실행 중 오류 발생: {e}")


def execute_commit(commit_message: str) -> bool:
    """
    git commit -m 명령을 실행하여 실제 커밋 수행

    Args:
        commit_message: 커밋 메시지

    Returns:
        bool: 커밋 성공 시 True, 실패 시 False
    """
    try:
        # git commit -m 실행
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )

        # 커밋 결과 출력
        print("\n✅ 커밋이 성공적으로 완료되었습니다!")
        print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        print_error(f"❌ 커밋 실행 중 오류 발생:\n{e.stderr}")
        return False


# ============================================================================
# Phase 3: LLM 연동 모듈
# ============================================================================

def load_gemini_context() -> str:
    """
    GEMINI.md 파일을 읽어 System Prompt로 변환

    Returns:
        str: GEMINI.md 파일의 내용 (System Prompt)

    Raises:
        GeminiFileNotFoundError: GEMINI.md 파일을 찾을 수 없을 때
    """
    gemini_file = Path.cwd() / "GEMINI.md"

    # GEMINI.md 파일 존재 확인
    if not gemini_file.exists():
        raise GeminiFileNotFoundError(
            "❌ GEMINI.md 파일을 찾을 수 없습니다.\n"
            "   커밋 메시지 컨벤션 가이드라인 파일을 생성해주세요."
        )

    try:
        # UTF-8 인코딩으로 파일 읽기
        with open(gemini_file, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # 파일이 비어있는 경우 기본 프롬프트 반환
        if not content:
            return "당신은 Git 커밋 메시지를 작성하는 전문가입니다. 변경사항을 분석하여 명확하고 간결한 커밋 메시지를 생성해주세요."

        return content

    except Exception as e:
        raise GacoError(f"❌ GEMINI.md 파일 읽기 중 오류 발생: {e}")


def initialize_gemini_client(api_key: str) -> genai.Client:
    """
    Gemini API 클라이언트 초기화 및 모델 설정

    Args:
        api_key: Gemini API 키

    Returns:
        Client: 초기화된 Gemini 클라이언트 인스턴스

    Raises:
        APIKeyError: API 키가 유효하지 않을 때
    """
    try:
        # Gemini 클라이언트 초기화 (새로운 API)
        client = genai.Client(api_key=api_key)
        return client

    except Exception as e:
        raise APIKeyError(f"❌ Gemini API 초기화 중 오류 발생: {e}")


def generate_commit_message(client: genai.Client, system_prompt: str, diff: str) -> str:
    """
    System Prompt와 Diff를 조합하여 Gemini API로 커밋 메시지 생성

    Args:
        client: 초기화된 Gemini 클라이언트
        system_prompt: GEMINI.md의 내용 (커밋 메시지 작성 가이드라인)
        diff: git diff --cached의 결과

    Returns:
        str: 생성된 커밋 메시지

    Raises:
        GacoError: API 호출 중 오류 발생 시
    """
    try:
        # 프롬프트 엔지니어링: System Prompt + Diff 조합
        user_prompt = f"""아래는 git diff --cached의 결과입니다. 이 변경사항을 분석하여 적절한 커밋 메시지를 생성해주세요.

커밋 메시지 형식:
- 첫 줄: 간결한 요약 (50자 이내, 명령형)
- 빈 줄
- 상세 설명 (필요시, 각 항목을 bullet point로)

---
{diff}
---

위 변경사항에 대한 커밋 메시지를 생성해주세요:"""

        # Gemini API 호출 (새로운 API)
        print("\n🤖 AI가 커밋 메시지를 생성 중입니다...\n")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config={
                'system_instruction': system_prompt,
                'temperature': 0.7,
            }
        )

        # 응답 텍스트 추출
        commit_message = response.text.strip()

        return commit_message

    except Exception as e:
        raise GacoError(f"❌ 커밋 메시지 생성 중 오류 발생: {e}")


# ============================================================================
# Phase 4: 사용자 인터페이스
# ============================================================================

def display_commit_message(message: str) -> None:
    """
    생성된 커밋 메시지를 터미널에 출력

    Args:
        message: 출력할 커밋 메시지
    """
    print("=" * 70)
    print("✨ 생성된 커밋 메시지:")
    print("=" * 70)
    print(message)
    print("=" * 70)


def get_user_choice() -> str:
    """
    사용자로부터 선택 입력 받기 (y/n/e)

    Returns:
        str: 사용자의 선택 ('y', 'n', 'e' 중 하나)
    """
    while True:
        print("\n[y] 승인하고 커밋  [n] 취소  [e] 메시지 수정")
        choice = input("선택: ").strip().lower()

        if choice in ['y', 'n', 'e']:
            return choice
        else:
            print("⚠️  올바른 선택지를 입력해주세요 (y/n/e)")


def edit_commit_message(original_message: str) -> str:
    """
    사용자가 커밋 메시지를 직접 수정할 수 있도록 함

    Args:
        original_message: 원본 커밋 메시지

    Returns:
        str: 수정된 커밋 메시지
    """
    print("\n📝 커밋 메시지를 수정하세요 (여러 줄 입력 가능, 빈 줄 입력 시 종료):")
    print("현재 메시지:")
    print("-" * 70)
    print(original_message)
    print("-" * 70)
    print("\n새 메시지를 입력하세요:")

    lines = []
    while True:
        try:
            line = input()
            if line == "" and len(lines) > 0:
                # 빈 줄이 입력되고 이미 내용이 있으면 종료
                break
            lines.append(line)
        except EOFError:
            break

    edited_message = "\n".join(lines).strip()

    # 수정된 메시지가 비어있으면 원본 반환
    if not edited_message:
        print("⚠️  메시지가 비어있어 원본 메시지를 사용합니다.")
        return original_message

    return edited_message


def handle_user_interaction(commit_message: str) -> Tuple[bool, str]:
    """
    사용자 상호작용 처리 (y/n/e 선택에 따른 동작)

    Args:
        commit_message: 생성된 커밋 메시지

    Returns:
        Tuple[bool, str]: (커밋 실행 여부, 최종 커밋 메시지)
    """
    current_message = commit_message

    while True:
        # 커밋 메시지 출력
        display_commit_message(current_message)

        # 사용자 선택 받기
        choice = get_user_choice()

        if choice == 'y':
            # 승인: 커밋 실행
            return True, current_message

        elif choice == 'n':
            # 거절: 취소
            print("\n❌ 커밋이 취소되었습니다.")
            return False, current_message

        elif choice == 'e':
            # 수정: 메시지 편집
            current_message = edit_commit_message(current_message)


# ============================================================================
# Phase 5: 통합 및 메인 엔트리포인트
# ============================================================================

def main() -> int:
    """
    gaco의 메인 엔트리포인트
    전체 워크플로우를 통합하여 실행

    Returns:
        int: 프로그램 종료 코드 (0: 성공, 1: 실패)
    """
    try:
        print("🚀 gaco - Git Auto COmmit")
        print("=" * 70)

        # Phase 1: 환경 설정
        print("\n📌 Step 1: API 키 로드 중...")
        api_key = load_api_key()
        print("✅ API 키 로드 완료")

        # Phase 2: Git 변경사항 확인
        print("\n📌 Step 2: Git 변경사항 확인 중...")
        diff = get_staged_diff()
        print(f"✅ {len(diff)} 바이트의 변경사항 발견")

        # Phase 3: LLM 연동
        print("\n📌 Step 3: Gemini API 초기화 중...")
        system_prompt = load_gemini_context()
        client = initialize_gemini_client(api_key)
        print("✅ Gemini API 초기화 완료")

        print("\n📌 Step 4: 커밋 메시지 생성 중...")
        commit_message = generate_commit_message(client, system_prompt, diff)
        print("✅ 커밋 메시지 생성 완료")

        # Phase 4: 사용자 인터페이스
        print("\n📌 Step 5: 사용자 확인 대기 중...")
        should_commit, final_message = handle_user_interaction(commit_message)

        # 커밋 실행
        if should_commit:
            success = execute_commit(final_message)
            return 0 if success else 1
        else:
            return 1

    except GacoError as e:
        # gaco 관련 예외 처리
        print_error(str(e))
        return 1

    except KeyboardInterrupt:
        # Ctrl+C 처리
        print_error("\n\n⚠️  사용자에 의해 중단되었습니다.")
        return 1

    except Exception as e:
        # 예상치 못한 예외 처리
        print_error(f"❌ 예상치 못한 오류 발생:\n{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
