# situation_classifier_openai.py

from typing import List
from pydantic import BaseModel, Field
from openai_client import client  # 같은 폴더의 openai_client.py에서 client 가져옴

# 사용할 상황 라벨 9개
SITUATIONS = [
    "party",
    "work",
    "relaxation",
    "exercise",
    "running",
    "stretching",
    "driving",
    "gathering",
    "morning",
]


class SituationOutput(BaseModel):
    """
    OpenAI Responses API의 structured output용 Pydantic 모델.
    situations: 가능성이 높은 순서대로 정렬된 상황 라벨 리스트 (0~N개)
    """
    situations: List[str] = Field(default_factory=list)


def classify_situation_kor(text: str, max_choices: int = 2) -> List[str]:
    """
    한국어 텍스트를 받아 9가지 상황 중 0~max_choices개를 반환한다.

    반환 규칙 (이 함수 자체는 리스트만 돌려줌):
    - 상황 단서 없음 -> []  (main.py에서 ['None']으로 변환)
    - 확정 1개 -> ['situation']
    - 모호한 경우 -> ['situation1', 'situation2']  (max_choices=2 기준)

    실제 최종 형태는 main.py에서 후처리:
      if not raw_situations: situations = ['None']
      elif len(raw_situations) == 1: situations = raw_situations
      else: situations = raw_situations[:2]
    """

    # 상황 라벨 정의 및 사용 규칙을 한국어로 명확히 설명
    situation_definitions = """
- party: 친구/사람들과 술, 클럽, 파티, 신나게 노는 모임
- work: 공부, 업무, 과제, 집중해야 하는 상황
- relaxation: 쉬는 중, 누워있음, 멍때리기, 힐링, 휴식
- exercise: 헬스, 웨이트 등 일반적인 운동 (달리기/요가/스트레칭은 아래 라벨 우선)
- running: 조깅, 러닝, 마라톤 등 달리기
- stretching: 스트레칭, 요가, 가벼운 몸 풀기
- driving: 자동차/지하철/버스/택시 등 이동 중, 출퇴근/등하교 길
- gathering: 가족/지인/동료와의 모임, 회식, 식사 (party보다 차분한 모임)
- morning: 아침 시간대(기상 후 ~ 오전)와 관련된 상황 (아침 운동, 등교/출근 준비 등)
"""

    system_prompt = f"""
너는 한국어 텍스트에서 사용자의 '상황'을 분석하는 어시스턴트야.

다음 9개의 상황 라벨만 사용할 수 있어:
{", ".join(SITUATIONS)}

각 라벨 의미는 다음과 같아:
{situation_definitions}

규칙:
- 반드시 SituationOutput 스키마를 따르는 JSON 구조만 생성해.
- situations 리스트에는 위 라벨들만 넣어.
- situations에는 '가능성이 높은 순서대로' 라벨을 넣어.
- 최대 {max_choices}개까지 선택해. 그 이상은 넣지 마.
- 텍스트에 상황 단서가 거의 없으면 빈 리스트 [] 를 반환해.
"""

    user_prompt = f"""
다음 한국어 텍스트에서 사용자의 상황(무엇을 하고 있는지, 어떤 맥락인지)을 분석해줘.

텍스트: "{text}"
"""

    try:
        # OpenAI Responses API + structured outputs (Pydantic)
        # 참고: client.responses.parse(...) 사용 예시는 공식/튜토리얼 문서에서 확인 가능.
        response = client.responses.parse(
            model="gpt-4.1-mini",  # 필요에 따라 gpt-4.1, gpt-4.1-mini, gpt-4o-mini 등으로 변경 가능
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,  # 분류이므로 0으로 고정하는 것이 안정적
            text_format=SituationOutput,  # Pydantic 모델로 파싱
        )

        parsed: SituationOutput = response.output_parsed

        # 허용된 라벨만 필터링
        situations = [s for s in parsed.situations if s in SITUATIONS]

        # 혹시 모델이 3개 이상 넣더라도 max_choices까지만 사용
        return situations[:max_choices]

    except Exception as e:
        # API 에러 시 안전하게 "상황 단서 없음"으로 처리되도록 빈 리스트 반환
        print("[WARN] OpenAI 상황 분류 중 오류 발생:", e)
        return []
