# situation_classifier.py

import re
from typing import List, Dict, Tuple
from statistics import mean

try:
    from konlpy.tag import Okt
    _okt = Okt()
except Exception:
    _okt = None  # 미설치/에러 시 안전하게 동작

from sentence_transformers import SentenceTransformer, util

# ----- 카테고리 -----
SITUATIONS = [
    "party", "work", "relaxation", "exercise", "running",
    "stretching", "driving", "gathering", "morning"
]

# ----- 부정 토큰 -----
NEGATION_TOKENS = [
    "안", "않", "못", "그만", "싫", "금지", "하지 말", "하지말", "말자", "말아", "그치자", "그만해"
]

# ----- 키워드 사전 (party에서 '친구랑' 제외) -----
KEYWORDS: Dict[str, Dict[str, float]] = {
    "party": {"파티": 1.2, "술자리": 1.0, "클럽": 1.2, "party": 1.0, "club": 1.0},
    "work": {"공부": 1.2, "집중": 1.0, "과제": 1.1, "업무": 1.1, "회사": 0.9, "study": 1.0, "work": 1.0},
    "relaxation": {"휴식": 1.2, "릴랙스": 1.0, "명상": 1.1, "힐링": 1.0, "차분": 0.9, "relax": 1.0, "meditation": 1.0,
                   "조용히": 1.1, "쉬": 1.1, "쉼": 1.0, "편안": 1.0},
    "exercise": {"운동": 1.0, "헬스": 1.1, "근력": 1.0, "웨이트": 1.0, "체육관": 0.9, "workout": 1.0, "gym": 1.0},
    "running": {"러닝": 1.2, "달리기": 1.2, "조깅": 1.0, "마라톤": 1.0, "유산소": 0.9, "run": 1.0, "jog": 1.0},
    "stretching": {"스트레칭": 1.2, "요가": 1.2, "필라테스": 1.1, "유연성": 0.9, "쿨다운": 0.9, "stretch": 1.0, "yoga": 1.0},
    "driving": {"드라이브": 1.2, "운전": 1.2, "고속도로": 0.8, "도로": 0.7, "차안": 0.9, "drive": 1.0},
    "gathering": {"모임": 1.1, "회식": 1.0, "친목": 1.0, "가족모임": 1.0, "동아리": 0.9, "gathering": 1.0},
    "morning": {"아침": 1.2, "모닝": 1.1, "기상": 1.0, "출근준비": 1.0, "아침운동": 1.0, "morning": 1.0}
}

# ----- 대표문장 3개씩 -----
REPRESENTATIVE_SENTENCES: Dict[str, List[str]] = {
    "party": ["친구들과 신나게 놀 수 있는 파티 음악이 필요해.","클럽에서 춤추기 좋은 에너지 넘치는 분위기가 좋아.","술자리에서 분위기를 띄울 업비트 노래 찾아줘."],
    "work": ["공부할 때 집중을 높여주는 잔잔한 음악이 좋아.","업무에 몰입할 수 있도록 방해가 적은 비트가 필요해.","생산성을 올릴 수 있는 집중용 플레이리스트가 필요해."],
    "relaxation": ["마음을 가라앉히고 휴식할 수 있는 편안한 음악이 듣고 싶어.","명상하기 좋은 잔잔하고 부드러운 사운드가 필요해.","긴장을 풀 수 있는 차분한 분위기의 곡을 추천해줘."],
    "exercise": ["운동할 때 동기부여 되는 파워풀한 비트가 필요해.","헬스장에서 힘이 나는 고에너지 음악을 듣고 싶어.","근력 운동에 템포 좋은 곡을 추천해줘."],
    "running": ["러닝할 때 리듬 타기 좋은 BPM의 곡이 필요해.","달리기 페이스를 유지할 신나는 음악을 추천해줘.","조깅하며 기분을 끌어올릴 수 있는 곡이 좋아."],
    "stretching": ["스트레칭하면서 몸을 천천히 풀 수 있는 음악이 필요해.","요가할 때 호흡과 어울리는 편안한 곡을 듣고 싶어.","쿨다운에 적합한 부드러운 사운드를 추천해줘."],
    "driving": ["드라이브하면서 기분 전환될 음악을 듣고 싶어.","차 안에서 길게 들어도 편안한 곡을 추천해줘.","도로 위에서 흐름이 좋은 룰루랄라 분위기의 음악이 좋아."],
    "gathering": ["가벼운 모임에서 다 함께 듣기 좋은 무난한 음악이 필요해.","회식 자리에서 배경으로 깔릴 부담 없는 플레이리스트가 좋아.","친목 도모에 분위기 망치지 않는 곡을 추천해줘."],
    "morning": ["아침에 상쾌하게 시작할 수 있는 음악이 듣고 싶어.","모닝루틴에 어울리는 가벼운 템포의 곡을 추천해줘.","출근 준비하면서 기분이 좋아지는 음악이 필요해."]
}

# ----- 임베딩 모델 (모듈 로드시 1회 로드) -----
_model = SentenceTransformer("jhgan/ko-sroberta-multitask")
_rep_embeds = {
    s: _model.encode(REPRESENTATIVE_SENTENCES[s], convert_to_tensor=True, normalize_embeddings=True)
    for s in SITUATIONS
}

# ========= 유틸 =========

def _normalize(text: str) -> str:
    t = text.strip()
    t = re.sub(r"[\u200b\u200c\u200d]+", "", t)
    t = re.sub(r"[\n\r\t]+", " ", t)
    t = re.sub(r"[^\w\s가-힣A-Za-z]", " ", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t

def _split_sentences(text: str) -> List[str]:
    parts = re.split(r"[.!?？！…\n]+", text)
    return [p.strip() for p in parts if p.strip()]

def _split_clauses(text: str) -> List[str]:
    parts = re.split(r"(?:[,.!?？！…]|그리고|하지만|는데|고\s)", text)
    return [p.strip() for p in parts if p.strip()]

def _okt_pos(text: str):
    return _okt.pos(text, norm=True, stem=True) if _okt else [(w, "N/A") for w in text.split()]

def _has_local_neg(tokens: List[Tuple[str, str]], kw_idx: int, window_tokens: int = 3) -> bool:
    L = max(0, kw_idx - window_tokens)
    R = min(len(tokens), kw_idx + window_tokens + 1)
    window = "".join(t for t, _ in tokens[L:R])
    return any(neg in window for neg in NEGATION_TOKENS)

def _clause_has_direct_negation(clause: str, keyword: str) -> bool:
    pat = rf"{re.escape(keyword)}\s*(?:은|는|이|가)?\s*싫"
    pat2 = rf"{re.escape(keyword)}\s*(?:을|를)?\s*하지\s*말"
    return bool(re.search(pat, clause)) or bool(re.search(pat2, clause))

# ========= 스코어링 =========

def _keyword_scores(text: str) -> Dict[str, float]:
    scores = {s: 0.0 for s in SITUATIONS}
    clauses = _split_clauses(text)
    for clause in clauses:
        pos = _okt_pos(clause)
        tokens_only = [w for w, _ in pos]
        token_set = set(tokens_only)
        for s in SITUATIONS:
            for kw, w in KEYWORDS[s].items():
                matched = (kw in clause) if (" " in kw or len(kw) > 3) else ((kw in token_set) or (kw in clause))
                if not matched:
                    continue
                if _clause_has_direct_negation(clause, kw):
                    continue
                penalized = False
                for i, (tok, _) in enumerate(pos):
                    if tok == kw and _has_local_neg(pos, i, 3):
                        penalized = True
                        break
                if penalized:
                    continue
                scores[s] += w
        # relaxation 시그널 보너스
        if any(sig in clause for sig in ["조용히", "쉬", "쉼", "편안", "차분", "휴식"]):
            scores["relaxation"] += 0.2
    return scores

def _embedding_scores(text: str) -> Dict[str, float]:
    vec = _model.encode([text], convert_to_tensor=True, normalize_embeddings=True)[0]
    return {s: float(util.cos_sim(vec, reps).mean()) for s, reps in _rep_embeds.items()}

def _rank(items: Dict[str, float]) -> List[Tuple[str, float]]:
    return sorted(items.items(), key=lambda x: x[1], reverse=True)

def _decide(kws: Dict[str, float], embs: Dict[str, float], text: str,
            min_sim: float = 0.40, margin: float = 0.04) -> Tuple[str, bool, List[Tuple[str, float]]]:
    matched = [s for s, sc in kws.items() if sc > 0]
    emb_ranked = _rank(embs)
    top2 = emb_ranked[:2]
    top_s, top_v = top2[0]
    second_v = top2[1][1] if len(top2) > 1 else -1.0

    # 키워드 단일매칭 확정
    if len(matched) == 1:
        return matched[0], False, top2

    # 임베딩 상위 후보가 명시적 부정이면 소폭 감점
    if top_s in KEYWORDS:
        for kw in list(KEYWORDS[top_s].keys())[:3]:
            if _clause_has_direct_negation(text, kw):
                top_v -= 0.02
                break

    confident = (top_v >= min_sim) and ((top_v - second_v) >= margin)
    if confident:
        return top_s, False, top2

    # 키워드 합을 타이브레이커로 고려
    if matched:
        best_by_kw = max(matched, key=lambda s: kws[s])
        if kws[best_by_kw] >= 0.8 * max(kws.values()):
            return best_by_kw, True, top2

    return "unknown", True, top2

# ========= 외부 API =========

def analyze_situation_list(text: str, min_sim: float = 0.40, margin: float = 0.04) -> List[str]:
    """
    항상 리스트 반환: 확정 ['work'], 모호 ['running','exercise']
    """
    t = _normalize(text)
    sents = _split_sentences(t) or [t]

    vote_acc: Dict[str, float] = {}
    emb_acc: Dict[str, List[float]] = {s: [] for s in SITUATIONS}
    kw_acc: Dict[str, List[float]] = {s: [] for s in SITUATIONS}

    for i, sent in enumerate(sents):
        kws = _keyword_scores(sent)
        embs = _embedding_scores(sent)
        decided, amb, top2 = _decide(kws, embs, sent, min_sim=min_sim, margin=margin)

        weight = 1.0 + (i / max(1, len(sents) - 1)) * 0.2 if len(sents) > 1 else 1.0
        vote_acc[decided] = vote_acc.get(decided, 0.0) + weight

        for s in SITUATIONS:
            kw_acc[s].append(kws[s])
            emb_acc[s].append(embs[s])

    final = max(vote_acc.items(), key=lambda x: x[1])[0]

    # 문서 레벨 모호성 판단
    mean_emb = {s: mean(vals) if vals else 0.0 for s, vals in emb_acc.items()}
    top2_global = _rank(mean_emb)[:2]
    ambiguous = (final == "unknown")
    if not ambiguous and len(top2_global) >= 2:
        if (top2_global[0][1] - top2_global[1][1]) < margin or top2_global[0][1] < min_sim:
            ambiguous = True

    if ambiguous:
        labels = [k for k, _ in top2_global] or [final]
    else:
        labels = [final]
    return labels
