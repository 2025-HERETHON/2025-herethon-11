from .models import Product, SubCategory

# innerwear_type -> category 매핑
type_to_category = {
    "노와이어": "브래지어",
    "브라렛": "브래지어",
    "팬티 세트": "브래지어",
    "노라인": "팬티",
    "볼륨패드": "브래지어",
    "누브라": "브래지어",
    "푸쉬업": "브래지어",
    "코르셋": "브래지어",
    "3/4컵": "브래지어",
    "와이어": "브래지어",
    "앞 후크": "브래지어",
    "니플 패치": "패치",
    "볼륨업": "브래지어",
    "홑겹": "브래지어",
    "하프컵": "브래지어",
    "삼각": "팬티",
    "사각": "팬티",
    "드로즈": "팬티",
    "하이웨스트": "팬티",
    "티스트링": "팬티",
    "오프숄더 브래지어": "브래지어",
}

def save_product(data):
    external_id = data["id"]
    title = data["title"]
    price = data["price"]
    thumbnail_url = data["thumbnail_url"]
    link = data["link"]
    subcategory_names = data["subcategories"]  # ["노와이어", "앞 후크"] 등

    category = type_to_category.get(subcategory_names[0], "기타")

    product, _ = Product.objects.update_or_create(
        external_id = external_id,
        defaults={
            "title": title,
            "price": price,
            "thumbnail_url": thumbnail_url,
            "link": link,
            "category": category,
        }
    )

    product.subcategories.clear()
    for name in subcategory_names:
        try:
            subcat = SubCategory.objects.get(name=name)
            product.subcategories.add(subcat)
        except SubCategory.DoesNotExist:
            continue
