"""
터미널 입출력 관련 모듈
"""
from typing import Tuple
from .editor import edit_commit_message

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


def handle_user_interaction(commit_message: str) -> Tuple[bool, str]:
    """
    사용자 상호작용 처리 (y/n/e 선택에 따른 동작)
    Facade 역할로 터미널 입출력과 에디터 호출을 조정

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
