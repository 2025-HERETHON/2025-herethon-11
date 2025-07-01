from crawler.services.config.category_config import (
    CATEGORY_MAPPING,      # 키워드 -> (카테고리, 서브카테고리) 매핑
    CATEGORY_KEYWORDS,     # 키워드 -> 카테고리 매핑
    EXCLUSIVE_PAIRS,       # 충돌 키워드 쌍 목록
)


# 새로운 키워드가 기존 키워드들과 충돌하는지 확인하는 함수
def is_conflicting(existing_keywords, new_keyword):
    for a, b in EXCLUSIVE_PAIRS:
        # 기존 키워드 중 하나가 있고, 새 키워드가 그와 충돌하면 True
        if (a in existing_keywords and b == new_keyword) or (b in existing_keywords and a == new_keyword):
            return True
    return False


# 상품 제목(title)로부터 카테고리와 서브카테고리를 추출하는 함수
def extract_subcategories_from_title(title):
    matched_subcategories = []   # 추출된 (카테고리, 서브카테고리) 튜플 저장
    matched_keywords = []        # 중복 및 충돌 체크를 위한 키워드 기록

    lower_title = title.lower()  # 소문자로 통일하여 검색

    # 서브카테고리 키워드 탐색
    for keyword, (cat, subcat) in CATEGORY_MAPPING.items():
        if keyword.lower() in lower_title:
            # '브라' 단어 단독 포함은 제외 (예: '브라렛' 같은 경우)
            if keyword.lower() == "브라":
                continue
            # 이미 들어간 키워드와 충돌하는 키워드면 제외
            if is_conflicting(matched_keywords, keyword.lower()):
                continue
            matched_keywords.append(keyword.lower())
            matched_subcategories.append((cat, subcat))

    # 최종 카테고리 추출
    if matched_subcategories:
        # 첫 번째 서브카테고리의 상위 카테고리를 사용
        category = matched_subcategories[0][0]
    else:
        # 서브카테고리가 없다면 CATEGORY_KEYWORDS에서만 추출
        category = None
        for keyword, cat in CATEGORY_KEYWORDS.items():
            if keyword.lower() in lower_title:
                category = cat
                break

    # 서브카테고리 이름만 리스트로 분리
    subcategories = [subcat for _, subcat in matched_subcategories]

    # "브라", "브래지어", "브라탑"만 포함된 경우 → 서브카테고리 제거
    if subcategories and all(kw in ["브라", "브래지어", "브라탑"] for kw in matched_keywords):
        subcategories = []

    return category, subcategories
