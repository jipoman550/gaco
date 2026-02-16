"""
Gemini API 연동 관련 서비스 모듈
"""
from google import genai
from ..core.exceptions import GacoError, APIKeyError

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
        system_prompt: docs/config/GEMINI.md의 내용 (커밋 메시지 작성 가이드라인)
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
