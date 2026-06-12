"""
Git 명령 실행 관련 모듈
"""
import subprocess
from pathlib import Path

from .exceptions import GacoError, GitNotFoundError, NoStagedChangesError
from .utils import safe_decode, print_error

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
        # git diff --cached 실행 (바이너리로 가져옴)
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            check=True
        )

        # 안전한 디코딩 적용
        diff_output = safe_decode(result.stdout).strip()

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
            check=True
        )

        # 커밋 결과 출력
        print("\n✅ 커밋이 성공적으로 완료되었습니다!")
        print(safe_decode(result.stdout))
        return True

    except subprocess.CalledProcessError as e:
        print_error(f"❌ 커밋 실행 중 오류 발생:\n{safe_decode(e.stderr)}")
        return False
