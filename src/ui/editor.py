"""
시스템 기본 편집기를 이용한 커밋 메시지 수정 모듈
"""
import os
import subprocess
import tempfile
from pathlib import Path

from ..core.utils import safe_decode

def edit_commit_message(original_message: str) -> str:
    """
    시스템 기본 편집기(Vim/Nvim 등)를 열어 커밋 메시지를 수정함
    """
    # 환경 변수에서 편집기 확인, 없으면 vim 사용
    editor = os.environ.get('EDITOR', 'vim')

    # 1. 임시 파일 생성 및 AI 추천 메시지 쓰기
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False, mode='w', encoding='utf-8') as tf:
        tf.write(original_message)
        temp_path = tf.name

    try:
        # 2. 편집기 실행 (subprocess 사용)
        subprocess.run([editor, temp_path], check=True)

        # 3. 수정된 내용 읽기
        edited_bytes = Path(temp_path).read_bytes()
        edited_message = safe_decode(edited_bytes).strip()

        if not edited_message:
            print("⚠️ 메시지가 비어있어 원본 메시지를 사용합니다.")
            return original_message

        return edited_message

    except subprocess.CalledProcessError:
        print("⚠️ 편집기 실행 중 오류가 발생했습니다.")
        return original_message
    finally:
        # 4. 사용이 끝난 임시 파일 삭제
        if os.path.exists(temp_path):
            os.remove(temp_path)
