import pandas as pd
import datetime as dt
from pathlib import Path

from src.logger import get_logger

logger = get_logger(__name__, file_path="logs/quality_alerts.log", config_path="config.yaml")

def check_quality(data: list[dict]) -> bool:
    if not data:
        logger.error("Данные пусты.")
        return False

    df_q = pd.DataFrame(columns=["name", "price", "description", "timestamp"])
    df = pd.DataFrame(columns=["name", "price", "description", "timestamp"])

    for item in data:
        if not all(key in item for key in ["name", "price", "description", "timestamp"]):
            logger.error(f"Отсутствуют необходимые поля в данных: {item}")
            return False
        if not isinstance(item["price"], (int, float)) or item["price"] <= 0:
            logger.error(f"Некорректная цена в данных: {item}")
            return False
        if item["name"] == "" or item["price"] == 0:
            logger.warning(f"Пустое название или цена равна нулю в данных: {item}")
            df_q = pd.concat([df_q, pd.DataFrame([item], columns=["name", "price", "description", "timestamp"])], ignore_index=True)
        else:
            df = pd.concat([df, pd.DataFrame([item], columns=["name", "price", "description", "timestamp"])], ignore_index=True)

    # Сохраняем результаты проверки в CSV файлы
    path_q = "data/quarantine/Ответ_Задание_2_1_Царегородцвев_Мачрченко.csv"
    df_q.to_csv(path_q, index=False, mode="w", encoding="utf-8")

    now = dt.datetime.now().strftime("%Y-%m-%d")
    path = Path(f"data/{now}")
    path.mkdir(parents=True, exist_ok=True)
    path = path / "Ответ_Задание_2_1_Царегорodцвев_Мачрченко.csv"
    df.to_csv(path, index=False, mode="w", encoding="utf-8")

    return True