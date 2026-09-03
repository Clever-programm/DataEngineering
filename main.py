from src.parser import fetch_products
from src.quality_check import check_quality

if __name__ == "__main__":
    products = fetch_products()
    if check_quality(products):
        print("Данные прошли проверку качества.")
    else:
        print("Данные не прошли проверку качества.")
