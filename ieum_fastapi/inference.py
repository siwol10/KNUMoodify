# inference.py
import os
import torch
import numpy as np
from typing import Dict
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ===== 설정 =====
# 1) 학습된 모델이 있으면 해당 경로로 지정 (환경변수로 덮어쓰기 가능)
DEFAULT_MODEL_DIR = "models/kobert-emotion-final/best"
MODEL_DIR = os.getenv("MODEL_DIR", DEFAULT_MODEL_DIR)

# 2) 디바이스: 로컬 CPU 테스트가 목적이므로 기본은 cpu
DEVICE = os.getenv("DEVICE", "cpu").lower()
if DEVICE not in {"cpu", "cuda"}:
    DEVICE = "cpu"
if DEVICE == "cuda" and not torch.cuda.is_available():
    DEVICE = "cpu"

# 3) 최대 시퀀스 길이
MAX_LEN = int(os.getenv("MAX_LEN", "192"))

# 4) 라벨/한글 맵핑
LABEL_LIST = ["joy", "anger", "fear", "sadness", "surprise"]
ID2LABEL = {i: lab for i, lab in enumerate(LABEL_LIST)}
ENG2KOR = {
    "joy": "기쁨",
    "anger": "분노",
    "fear": "두려움",
    "sadness": "슬픔",
    "surprise": "놀람",
}


# ===== 모델/토크나이저 로드 =====
def _load_tokenizer_and_model():
    """
    1) 로컬 fine-tuned 모델(MODEL_DIR)이 있으면 그것을 로드
    2) 없으면 허브의 'skt/kobert-base-v1' 로드 (분류헤드는 랜덤 초기화)
       → 이 경우 추론 품질보다는 '서버 구동/호출 테스트' 용도
    """
    if os.path.exists(MODEL_DIR):
        tok = AutoTokenizer.from_pretrained(MODEL_DIR, use_fast=False)
        mdl = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        print(f"[INFO] Loaded fine-tuned model from: {MODEL_DIR}")
    else:
        base_id = "skt/kobert-base-v1"
        tok = AutoTokenizer.from_pretrained(base_id, use_fast=False)
        mdl = AutoModelForSequenceClassification.from_pretrained(
            base_id,
            num_labels=len(LABEL_LIST),
            id2label=ID2LABEL,
            label2id={v: k for k, v in ID2LABEL.items()},
        )
        print(f"[WARN] Fine-tuned model not found. Loaded base: {base_id} (for API smoke test)")
    return tok, mdl


tokenizer, model = _load_tokenizer_and_model()
model.to(DEVICE)
model.eval()
torch.set_grad_enabled(False)
torch.set_num_threads(1)  # Windows/Jupyter 안정화


# KoBERT 안전 추론 (token_type_ids=0, position_ids=0..L-1)
def predict_one(text: str) -> str:
    """
    입력 문장 -> {'result': 'emotion="기쁨"'} 형태로 반환
    (실서비스에서는 모델을 fine-tuning 한 가중치로 교체하세요)
    """
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=min(MAX_LEN, getattr(model.config, "max_position_embeddings", 512)),
        return_token_type_ids=True,
        padding=False,
    )
    # KoBERT 안전 처리
    inputs["token_type_ids"] = torch.zeros_like(inputs["input_ids"])
    L = inputs["input_ids"].shape[1]
    inputs["position_ids"] = torch.arange(L, dtype=torch.long).unsqueeze(0)

    # 디바이스
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    # 추론
    logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=-1).detach().cpu().numpy()[0]
    pred_id = int(np.argmax(probs))
    eng_label = model.config.id2label[pred_id] if hasattr(model.config, "id2label") else ID2LABEL[pred_id]
    kor_label = ENG2KOR.get(eng_label, eng_label)


    # 요구 포맷에 맞게 반환
    #return {"result": f'emotion="{kor_label}"'}
    return eng_label
