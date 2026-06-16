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
        # 1. 시스템 환경변수 확인
        ollama_endpoint = os.getenv("OLLAMA_HOST")

        # 💡 [황금 밸런스 방어 코드]
        # 환경변수에 127.0.0.1이나 localhost가 들어왔을 때,
        # 진짜 윈도우 WSL2 환경('Microsoft' 문구가 OS 릴리즈에 포함됨)일 때만 가상 IP를 추적합니다.
        # 42 클러스터 순수 리눅스/맥 환경이라면 이 조건을 스킵하고 127.0.0.1을 그대로 고수합니다!
        is_wsl = False
        try:
            if os.path.exists("/proc/version"):
                with open("/proc/version", "r") as f:
                    if "microsoft" in f.read().lower():
                        is_wsl = True
        except Exception:
            pass

        # WSL2 환경일 때만 127.0.0.1을 윈도우 가상 IP로 치환
        if is_wsl:
            if not ollama_endpoint or "127.0.0.1" in ollama_endpoint or "localhost" in ollama_endpoint:
                ollama_endpoint = _get_wsl_host_ip()
        else:
            # 42 클러스터 등 순수 유닉스/리눅스 환경에서는 환경변수가 없거나 부실하면 127.0.0.1 로컬로 고정
            if not ollama_endpoint:
                ollama_endpoint = "http://127.0.0.1:11434/v1"

            # 유저가 강제로 http:// 없이 IP만 적었을 경우를 대비한 유틸리티 보정
            if not ollama_endpoint.startswith("http"):
                ollama_endpoint = f"http://{ollama_endpoint}"
            if not ollama_endpoint.endswith("/v1"):
                ollama_endpoint = f"{ollama_endpoint}/v1" if ollama_endpoint.endswith("/") else f"{ollama_endpoint}/v1"

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
        target_model = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")

        user_prompt = f"""Analyze the following git diff --cached result and generate a professional commit message STRICTLY in English.

Commit Message Format:
- First line: Concise summary (under 50 chars, imperative mood)
- Blank line
- Detailed description (bullet points starting with '-')

CRITICAL REQUIREMENT:
- DO NOT use Korean. Output must be 100% English.
- Follow the system convention strictly.

---
{diff}
---

Generate the English commit message:"""

        print(f"\n🤖 로컬 AI({target_model})가 커밋 메시지를 분석 중입니다...", flush=True)

        response = client.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            timeout=60.0
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        raise GacoError(f"❌ 로컬 Ollama API 호출 중 오류 발생: {e}")