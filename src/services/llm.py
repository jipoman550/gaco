"""
로컬 Ollama API 연동 관련 서비스 모듈 (OpenAI 호환 API 활용)
"""
import os 
from openai import OpenAI
from core.exceptions import GacoError, APIKeyError

def initialize_gemini_client(api_key: str) -> OpenAI:
    """
    기존 Gemini 초기화 함수 이름을 유지하여 호환성을 깨지 않고,
    노트북 환경(WSL2 -> Windows 호스트)과 42 클러스터 환경을 모두 지원합니다.
    """
    try:
        # 1. 시스템에 OLLAMA_HOST 환경변수가 설정되어 있다면 최우선으로 사용 (42 클러스터 대응용)
        ollama_endpoint = "http://172.20.64.1:11434/v1"
        
        
        if not ollama_endpoint:
            # 2. 환경변수가 없다면 현재 노트북(WSL2 -> Windows 호스트 통신) 환경으로 간주
            # WSL2 내부에서 127.0.0.1은 우분투 내부를 돌지만, 'localhost'는 윈도우 호스트 포트 포워딩을 탑니다.
            ollama_endpoint = "http://localhost:11434/v1"
            
        print(f"\n🔗 연결 중인 Ollama 엔드포인트: {ollama_endpoint}")
        
        client = OpenAI(
            base_url=ollama_endpoint,
            api_key="ollama-local"
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