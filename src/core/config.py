"""
gaco 설정 관련 모듈
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from .exceptions import APIKeyError, GeminiFileNotFoundError, GacoError
from .utils import safe_decode

def load_api_key() -> str:
    """
    .env 파일에서 GEMINI_API_KEY를 로드하고 반환

    Returns:
        str: Gemini API 키

    Raises:
        APIKeyError: API 키를 찾을 수 없거나 유효하지 않을 때
    """
    # 프로젝트 루트 디렉토리 찾기
    # 현재 파일: .../src/gaco/core/config.py
    # parents[0]=core, parents[1]=gaco, parents[2]=src, parents[3]=root
    try:
        current_file = Path(__file__).resolve()
        project_root = current_file.parents[3]
    except Exception:
        # fallback if run from odd location
        project_root = Path.cwd()

    env_path = project_root / ".env"

    # .env 파일 로드
    load_dotenv(dotenv_path=env_path)

    # 환경변수에서 API 키 가져오기
    api_key = os.getenv("GEMINI_API_KEY")

    # API 키 유효성 검사
    if not api_key or api_key.strip() == "":
        raise APIKeyError(
            "❌ GEMINI_API_KEY를 찾을 수 없습니다.\n"
            f"   {env_path} 파일에 GEMINI_API_KEY=your_api_key 형식으로 추가해주세요."
        )

    return api_key.strip()


def load_gemini_context() -> str:
    """
    docs/config/GEMINI.md 파일을 읽어 System Prompt로 변환

    Returns:
        str: GEMINI.md 파일의 내용 (System Prompt)

    Raises:
        GeminiFileNotFoundError: docs/config/GEMINI.md 파일을 찾을 수 없을 때
    """
    try:
        current_file = Path(__file__).resolve()
        project_root = current_file.parents[3]
    except Exception:
        project_root = Path.cwd()

    gemini_file = project_root / "docs" / "config" / "GEMINI.md"

    # GEMINI.md 파일 존재 확인
    if not gemini_file.exists():
        # CWD fallback
        cwd_gemini = Path.cwd() / "docs" / "config" / "GEMINI.md"
        if cwd_gemini.exists():
            gemini_file = cwd_gemini
        else:
            raise GeminiFileNotFoundError(
                f"❌ {gemini_file} 파일을 찾을 수 없습니다.\n"
                "   커밋 메시지 컨벤션 가이드라인 파일을 생성해주세요."
            )

    try:
        # 파일을 바이너리로 읽어서 안전하게 디코딩
        content_bytes = gemini_file.read_bytes()
        content = safe_decode(content_bytes).strip()

        # 파일이 비어있는 경우 기본 프롬프트 반환
        if not content:
            return "당신은 Git 커밋 메시지를 작성하는 전문가입니다. 변경사항을 분석하여 명확하고 간결한 커밋 메시지를 생성해주세요."

        return content

    except Exception as e:
        raise GacoError(f"❌ GEMINI.md 파일 읽기 중 오류 발생: {e}")
