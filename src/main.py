"""
gaco 메인 엔트리포인트 (Facade)
"""
import sys

# gaco 패키지 내부 모듈 임포트
from core.exceptions import GacoError
from core.utils import print_error
from core.config import load_api_key, load_gemini_context
from core.git import get_staged_diff, execute_commit
from services.llm import initialize_llm_client, generate_commit_message
from ui.terminal import handle_user_interaction


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
        print("\n📌 Step 3: LLM API 초기화 중...")
        system_prompt = load_gemini_context()
        client = initialize_llm_client(api_key)
        print("✅ LLM API 초기화 완료")

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
