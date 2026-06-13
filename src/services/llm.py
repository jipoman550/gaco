"""
로컬 Ollama API 연동 관련 서비스 모듈 (OpenAI 호환 API 활용)
"""
import os
import subprocess
from openai import OpenAI
from core.exceptions import GacoError, APIKeyError

def _get_wsl_host_ip() -> str:
    """WSL2 우분투 안에서 실시간으로 윈도우 본체(호스트)의 가상 IP를 찾아 반환합니다."""
    try:
        # ip route 명령어를 실행하여 default 게이트웨이(윈도우) IP 추출
        cmd = "ip route | grep default | awk '{print $3}'"
        host_ip = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        if host_ip:
            return f"http://{host_ip}:11434/v1"
    except Exception:
        pass
    # 실패 시 최후의 보루로 localhost 반환
    return "http://localhost:11434/v1"

def initialize_gemini_client(api_key: str) -> OpenAI:
    """
    노트북 환경(WSL2 동적 IP 자동 추적)과 42 클러스터 환경을 완벽하게 동시 지원합니다.
    """
    try:
        # 1. 시스템에 OLLAMA_HOST 환경변수가 설정되어 있다면 최우선으로 사용 (42 클러스터 대응용)
        ollama_endpoint = os.getenv("OLLAMA_HOST")
        
        if not ollama_endpoint:
            # 2. 환경변수가 없다면 현재 노트북(WSL2) 환경으로 간주하여 실시간으로 윈도우 IP 추적
            ollama_endpoint = _get_wsl_host_ip()
            
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