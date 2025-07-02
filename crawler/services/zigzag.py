import requests
import time
import re
from bs4 import BeautifulSoup
import os
import django

# 장고 프로젝트 세팅 연결
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eve.settings")
django.setup()

# 장고 모델, 카테고리 추출 함수 불러오기
from products.models import Product, SubCategory
from crawler.services.utils.category_extractor import extract_subcategories_from_title
from products.models import Category
from crawler.services.config.category_config import CATEGORY_MAPPING

# ------------------------ 설정 ------------------------

# 검색할 주요 키워드 (브래지어, 팬티, 패치)
SEARCH_KEYWORDS = ["브래지어", "팬티", "패치"]

# 각 키워드당 몇 페이지까지 크롤링할지 지정
KEYWORD_PAGE_MAP = {
    "브래지어": 3,
    "팬티": 1,
    "패치": 1,
}

# 지그재그 API URL
ZIGZAG_SEARCH_URL = "https://api.zigzag.kr/api/2/graphql/GetSearchResult"

# 요청 헤더 설정
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://zigzag.kr",
    "Referer": "https://zigzag.kr/",
}

# 상품 리스트 요청 GraphQL 쿼리문
SEARCH_QUERY = """
query GetSearchResult($input: SearchResultInput!) {
  search_result(input: $input) {
    total_count
    has_next
    end_cursor
    searched_keyword
    ui_item_list {
      ... on UxGoodsCardItem {
        title
        image_url
        product_url
        final_price
        shop_name
      }
    }
  }
}
"""

# 옵션(사이즈/색상) 요청 GraphQL 쿼리문
DETAIL_QUERY = """
query GetPdpOptionInfo($catalog_product_id: ID!) {
  pdp_option_info(catalog_product_id: $catalog_product_id) {
    catalog_product {
      product_option_list {
        name
        value_list {
          value
        }
      }
    }
  }
}
"""

# ------------------------ 공통 GraphQL 호출 함수 ------------------------

# 공통 GraphQL 호출 함수
# noinspection PyShadowingNames

def call_graphql_api(operation_name, query, variables):
    # payload 지정
    payload = {
        "operationName": operation_name,
        "query": query,
        "variables": variables
    }

    try:
        # POST 요청 전송
        res = requests.post(ZIGZAG_SEARCH_URL, headers = HEADERS, json = payload)

        # 요청 전송 시 받아온 데이터를 json으로 반환
        return res.json()

    # 예외 처리
    except Exception as e:
        print(f"GraphQL 요청 실패 ({operation_name}):", e)
        return {}

# ------------------------ 유틸 함수 ------------------------

# 고유 아이디 추출
def extract_external_id(url):
    # products/ 뒤에 붙는 id를 저장
    match = re.search(r'/products/(\d+)', url)

    # id 리턴
    return match.group(1) if match else None


# 상품 상세 페이지에서 소재 추출
def extract_material_from_detail_page(product_url):
    try:
        # BeautifulSoup으로 받아온 데이터를 처리
        res = requests.get(product_url, headers = {"User-Agent": "Mozilla/5.0"}, timeout = 5)
        soup = BeautifulSoup(res.text, 'html.parser')

        # div를 반복하면서 소재, 혼용률, 구성이 있으면 텍스트 100까지 반환
        for div in soup.find_all("div"):
            text = div.get_text(strip = True)
            if any(k in text for k in ["소재", "혼용률", "구성"]) and len(text) >= 3:
                return text[:100]

        return None

    except Exception as material_e:
        print("소재 크롤링 실패:", material_e)
        return None


# 상품 상세 페이지에서 색상과 사이즈 추출
def extract_options_from_detail_response(option_data):
    # 색상과 사이즈 리스트
    color_values = []
    size_values = []

    # 색상 및 사이즈 단어 지정
    for option in option_data.get("product_option_list", []):
        name = option.get("name", "").strip()
        values = [v["value"] for v in option.get("value_list", []) if "value" in v]

        # 색상 및 사이즈 값 삽입
        if name in ["색상", "컬러"]:
            color_values.extend(values)
        elif name in ["사이즈", "크기"]:
            size_values.extend(values)

    # 색상과 사이즈 요소들을 ,를 붙여 반환
    return ", ".join(color_values) or None, ", ".join(size_values) or None


# 상품 ID를 이용해 색상/사이즈 등의 옵션 정보를 가져오는 GraphQL 요청 함수
def get_detail_response(product_id):
    # noinspection PyShadowingNames
    variables = {"catalog_product_id": product_id}
    return call_graphql_api("GetPdpOptionInfo", DETAIL_QUERY, variables)


# 상품 ID와 키워드를 이용해 검색 결과에서 해당 상품의 메타 정보(title, price 등)를 가져오는 함수
# noinspection PyShadowingNames
def get_product_meta_info(external_id, keyword):
    # 검색 키워드를 포함한 GraphQL 쿼리 변수 정의
    # noinspection PyShadowingNames
    variables = {
        "input": {
            "keyword": keyword,
            "start_cursor": "",
            "sort": "RELEVANCE",
            "search_type": "PRODUCT",
        }
    }

    # 지그재그 검색 API 호출
    data = call_graphql_api("GetSearchResult", SEARCH_QUERY, variables)

    # 검색 결과에서 상품 리스트 추출
    items = data.get("data", {}).get("search_result", {}).get("ui_item_list", [])

    # 상품 ID가 포함된 URL을 찾아 해당 메타 정보(title, price 등) 반환
    for item in items:
        url = item.get("product_url", "")
        if external_id in url:
            return {
                "title": item.get("title"),
                "final_price": item.get("final_price"),
                "image_url": item.get("image_url"),
                "shop_name": item.get("shop_name"),
            }

    # 찾지 못한 경우 빈 딕셔너리 반환
    return {}

# ------------------------ 저장 / 업데이트 함수 ------------------------

# 상품 정보를 크롤링 결과로부터 추출하고 DB에 저장하는 함수
def save_product_to_db(product_item, main_category, subcategory_list):
    # 상품 URL에서 외부 ID 추출
    external_id = extract_external_id(product_item.get("product_url", ""))

    # ID가 없거나 이미 DB에 존재하면 저장하지 않고 종료
    if not external_id or Product.objects.filter(external_id = external_id).exists():
        return

    # 상품 상세 정보 요청 (옵션: 색상, 사이즈 포함)
    detail_data = get_detail_response(external_id).get("data", {}).get("pdp_option_info", {}).get("catalog_product", {})

    # 옵션 정보에서 색상과 사이즈 추출
    color, size = extract_options_from_detail_response(detail_data)

    # HTML 페이지에서 소재 정보 크롤링
    material = extract_material_from_detail_page(product_item.get("product_url", ""))

    # Product 모델 인스턴스 생성 및 DB에 저장
    product = Product.objects.create(
        external_id = external_id,
        title = product_item.get("title", ""),
        price = product_item.get("final_price", ""),
        image_url = product_item.get("image_url", ""),
        link = product_item.get("product_url", ""),
        shop = product_item.get("shop_name", ""),
        size = size,
        color = color,
        material = material,
        source_keyword = main_category
    )

    product.save()

    # 메인 카테고리 + 서브카테고리 기반 카테고리 모두 모으기
    category_names = {main_category}
    for subcat in subcategory_list:
        if subcat in CATEGORY_MAPPING:
            cat_name, _ = CATEGORY_MAPPING[subcat]
            category_names.add(cat_name)

    # 카테고리 저장
    for cat_name in category_names:
        cat_obj, _ = Category.objects.get_or_create(name=cat_name)
        product.categories.add(cat_obj)

    # 서브카테고리 저장
    for subcat_name in subcategory_list:
        subcat, _ = SubCategory.objects.get_or_create(name=subcat_name)
        product.subcategories.add(subcat)


# DB에 저장된 상품 중 누락된 필드(title, price, image_url 등)를 업데이트하는 함수
# noinspection PyShadowingNames
def update_missing_fields(product: Product, keyword: str):
    # 1. 상품 상세 옵션 정보 요청 (색상, 사이즈)
    detail_data = get_detail_response(product.external_id).get("data", {}).get("pdp_option_info", {}).get("catalog_product", {})
    color, size = extract_options_from_detail_response(detail_data)

    # 2. 상품 HTML 페이지에서 소재 정보 크롤링
    material = extract_material_from_detail_page(product.link)

    # 3. 상품 메타 정보(title, 가격 등) 요청
    meta_info = get_product_meta_info(product.external_id, keyword)

    # 4. 각 필드가 비어 있을 경우에만 업데이트
    if not product.title and meta_info.get("title"):
        product.title = meta_info.get("title")
    if not product.price and meta_info.get("final_price"):
        product.price = meta_info.get("final_price")
    if not product.image_url and meta_info.get("image_url"):
        product.image_url = meta_info.get("image_url")
    if not product.shop and meta_info.get("shop_name"):
        product.shop = meta_info.get("shop_name")
    if not product.color and color:
        product.color = color
    if not product.size and size:
        product.size = size
    if not product.material and material:
        product.material = material

    # 5. 변경 사항 저장
    product.save()

# ------------------------ 크롤링 시작 ------------------------

# 크롤링 스크립트의 시작점
if __name__ == "__main__":
    # 키워드별로 지정된 페이지 수만큼 반복
    for keyword, max_pages in KEYWORD_PAGE_MAP.items():
        end_cursor = None  # 페이지네이션 커서
        page_count = 0     # 현재 페이지 수

        while page_count < max_pages:
            # GraphQL 검색 요청 파라미터 설정
            variables = {
                "input": {
                    "enable_guided_keyword_search": True,
                    "initial": page_count == 0,     # 첫 페이지 여부
                    "page_id": "srp_item",          # 고정값
                    "q": keyword,                   # 검색 키워드
                    "after": end_cursor,            # 페이지 커서
                    "filter_list": [],
                    "filter_id_list": ["205"],      # 고정 필터
                    "sub_filter_id_list": [],
                }
            }

            # 상품 검색 요청
            data = call_graphql_api("GetSearchResult", SEARCH_QUERY, variables)
            result = data.get("data", {}).get("search_result", {})

            # 각 상품에 대해 저장 시도
            for item in result.get("ui_item_list", []):
                title = item.get("title", "")

                # '패치' 키워드의 경우 원하는 키워드 필터링
                if keyword == "패치":
                    if not any(k in title for k in ["니플", "가슴", "유두", "브라", "가슴패치"]):
                        continue

                # 상품명으로부터 카테고리 및 서브카테고리 추출
                category, subcategories = extract_subcategories_from_title(title)
                if not category:
                    category = keyword  # fallback

                # DB에 저장
                save_product_to_db(item, category, subcategories)

            # 누락된 상품 정보 업데이트
            products = Product.objects.filter(material__isnull=True)
            for p in products:
                if p.source_keyword:
                    update_missing_fields(p, p.source_keyword)

            # 다음 페이지가 없으면 중단
            if not result.get("has_next"):
                break

            # 다음 페이지로 이동
            end_cursor = result.get("end_cursor")
            page_count += 1

            # 서버 부하 방지를 위한 대기 시간
            time.sleep(1.0)

