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
        # NAT 모드에서 수시로 바뀌는 윈도우 호스트의 가상 게이트웨이 IP를 실시간 추출
        cmd = "ip route | grep default | awk '{print $3}'"
        host_ip = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
        if host_ip:
            return f"http://{host_ip}:11434/v1"
    except Exception:
        pass
    return "http://localhost:11434/v1"

def initialize_llm_client(api_key: str) -> OpenAI:
    """
    노트북 NAT 환경(동적 IP 자동 추적)과 42 클러스터 환경을 완벽하게 동시 지원합니다.
    """
    try:
        # 1. 시스템에 OLLAMA_HOST 환경변수가 설정되어 있다면 가져옴
        ollama_endpoint = os.getenv("OLLAMA_HOST")
        
        # 윈도우 환경변수 127.0.0.1이 WSL2로 잘못 넘어왔거나 변수가 없다면 강제로 진짜 윈도우 IP 추적
        if not ollama_endpoint or "127.0.0.1" in ollama_endpoint:
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
    """System Prompt와 Diff를 조합하여 로컬 Ollama API로 커밋 메시지 생성"""
    try:
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

        response = client.chat.completions.create(
            model="qwen2.5-coder:3b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        raise GacoError(f"❌ 로컬 Ollama API 호출 중 오류 발생: {e}")