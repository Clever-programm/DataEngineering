import re
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

# Целевой URL каталога с товарами
URL = "https://sushkilove.ru/shop/page/1/?count=24&paged="

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def clean_price(raw_price: str) -> float:
    """Очищает строку цены от символов валюты, пробелов и приводит к float."""
    if not raw_price:
        return None
    # Удаляем неразрывные пробелы \xa0 и обычные пробелы
    cleaned = raw_price.replace("\xa0", " ").replace(" ", "")
    # Ищем последовательность цифр (с возможной точкой или запятой)
    match = re.search(r"(\d+[\.,]?\d*)", cleaned)
    if match:
        return float(match.group(1).replace(",", "."))
    return None

def fetch_products(limit: int = 20) -> list[dict]:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    
    # Селектор карточек WooCommerce
    items = soup.select("li.product")
    collected_data = []

    for item in items:
        if len(collected_data) < limit: pass
        elif len(collected_data) >= limit:
            break

        # Название товара
        title_el = item.select_one(".woocommerce-loop-product__title") or item.select_one("h2, h3")
        name = title_el.get_text(strip=True) if title_el else ""

        # Цена товара
        price_el = item.select_one(".price ins .woocommerce-Price-amount") or item.select_one(".price .woocommerce-Price-amount")
        raw_price = price_el.get_text(strip=True) if price_el else ""
        price = clean_price(raw_price)

        # Описание
        desc_el = item.select_one(".product-loop-title") or item.select_one(".product-short-description")
        href = desc_el.get("href") if desc_el else None
        description_response = requests.get(href, headers=HEADERS, timeout=10)
        description_soup = BeautifulSoup(description_response.text, "lxml")
        description = description_soup.select_one("#tab-description").get_text("") if description_soup else ""
        #print(description)


        # 4. Timestamp в формате ISO 8601
        timestamp = datetime.now(timezone.utc).isoformat()

        collected_data.append({
            "name": name,
            "price": price,
            "description": description.strip().replace("Описание\n", "").replace("\xa0", ""),
            "timestamp": timestamp,
        })

    return collected_data

if __name__ == "__main__":
    products = fetch_products(limit=20)
    print(f"Собрано товаров: {len(products)}")
    for idx, item in enumerate(products[:20], 1):
        print(f"#{idx}: {item}")