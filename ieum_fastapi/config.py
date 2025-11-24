import os
from dotenv import load_dotenv

load_dotenv()  # .env 읽기

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다. .env를 확인하세요.")
