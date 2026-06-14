"""
gaco 설정 관련 모듈
"""
import os
from pathlib import Path
from dotenv import load_dotenv

from .exceptions import APIKeyError, PromptFileNotFoundError, GacoError
from .utils import safe_decode

def load_api_key() -> str:
    """
    의미가 없는 함수인듯...?
    현재 실행 중인 프로젝트 루트 디렉토리의 .env 파일에서 GEMINI_API_KEY를 로드하고 반환
    """
    # 현재 터미널이 위치한 프로젝트 폴더(gaco) 기준으로 .env 경로 고정
    project_root = Path(__file__).resolve().parents[2]
    env_path = project_root / ".env"

    # .env 파일 로드
    load_dotenv(dotenv_path=env_path)

    # 환경변수에서 API 키 가져오기
    api_key = os.getenv("GEMINI_API_KEY")

    # API 키 유효성 검사 (로컬 우회용 dummy key도 통과됨)
    if not api_key or api_key.strip() == "":
        raise APIKeyError(
            "❌ LLM_API_KEY를 찾을 수 없습니다.\n"
            f"   {env_path} 파일에 LLM_API_KEY=your_api_key 형식으로 추가해주세요."
        )

    return api_key.strip()


def load_system_prompt() -> str:
    """
    docs/config/CONVENTION.md 파일을 읽어 System Prompt로 변환
    """
    project_root = Path(__file__).resolve().parents[2]
    gemini_file = project_root / "docs" / "config" / "CONVENTION.md"

    # GEMINI.md 파일 존재 확인
    if not gemini_file.exists():
        raise PromptFileNotFoundError(
            f"❌ {gemini_file} 파일을 찾을 수 없습니다.\n"
            "   커밋 메시지 컨벤션 가이드라인 파일을 생성해주세요."
        )

    try:
        # 파일을 바이너리로 읽어서 안전하게 디코딩
        content_bytes = gemini_file.read_bytes()
        content = safe_decode(content_bytes).strip()

        if not content:
            return "당신은 Git 커밋 메시지를 작성하는 전문가입니다. 변경사항을 분석하여 명확하고 간결한 커밋 메시지를 생성해주세요."

        return content

    except Exception as e:
        raise GacoError(f"❌ GEMINI.md 파일 읽기 중 오류 발생: {e}")