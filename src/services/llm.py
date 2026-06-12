"""
로컬 Ollama API 연동 관련 서비스 모듈 (OpenAI 호환 API 활용)
"""
from openai import OpenAI
from .core.exceptions import GacoError, APIKeyError

def initialize_gemini_client(api_key: str) -> OpenAI:
    """
    기존 Gemini 초기화 함수 이름을 유지하여 main.py와의 호환성을 깨지 않고,
    내부적으로는 우리 포트(11435)를 바라보는 OpenAI 클라이언트를 반환합니다.

    Args:
        api_key: 로컬 구동이므로 아무 문자열이나 들어와도 무방합니다.

    Returns:
        OpenAI: 초기화된 OpenAI 클라이언트 인스턴스 (Ollama 바인딩)
    """
    try:
        # 포트 11435번의 Ollama 서버를 OpenAI 호환 엔드포인트(/v1)로 연결
        client = OpenAI(
            base_url="http://127.0.0.1:11435/v1",
            api_key="ollama-local"  # 로컬이므로 아무 값이나 넣어도 작동합니다.
        )
        return client

    except Exception as e:
        raise APIKeyError(f"❌ 로컬 Ollama 클라이언트 초기화 중 오류 발생: {e}")


def generate_commit_message(client: OpenAI, system_prompt: str, diff: str) -> str:
    """
    System Prompt와 Diff를 조합하여 로컬 Ollama(Qwen2.5-Coder) API로 커밋 메시지 생성

    Args:
        client: 초기화된 OpenAI 클라이언트
        system_prompt: docs/config/GEMINI.md의 내용 (커밋 메시지 작성 가이드라인)
        diff: git diff --cached의 결과

    Returns:
        str: 생성된 커밋 메시지
    """
    try:
        # gaco의 원래 프롬프트 엔지니어링 구조 그대로 유지
        user_prompt = f"""아래는 git diff --cached의 결과입니다. 이 변경사항을 분석하여 적절한 커밋 메시지를 생성해주세요.

커밋 메시지 형식:
- 첫 줄: 간결한 요약 (50자 이내, 명령형)
- 빈 줄
- 상세 설명 (필요시, 각 항목을 bullet point로)

---
{diff}
---

위 변경사항에 대한 커밋 메시지를 생성해주세요:"""

        print("\n🤖 로컬 AI(Qwen2.5-Coder-3B)가 커밋 메시지를 분석 중입니다...", flush=True)

        # 다운로드받은 Qwen 3B 모델 지정하여 OpenAI 호환 규격으로 호출
        response = client.chat.completions.create(
            model="qwen2.5-coder:3b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2  # 일관된 규칙 준수를 위해 낮은 온도로 세팅
        )

        # 결과 텍스트 추출 및 반환
        return response.choices[0].message.content.strip()

    except Exception as e:
        raise GacoError(f"❌ 로컬 Ollama API 호출 중 오류 발생: {e}")