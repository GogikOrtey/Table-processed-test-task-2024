# Программа по обработке данных в таблицах

# Задача:
# Определить тип для каждого товара

import pandas as pd
from fuzzywuzzy import fuzz

# Загрузка данных из файла 'Дерево категорий.xlsx'
df_tree = pd.read_excel("data/Дерево категорий.xlsx")
contr_type = df_tree["Тип товара"].tolist()

def classify_product(section):
    # Извлечение последнего значения из поля "Раздел"
    last_section = section.split('/')[-1]

    # Поиск наиболее похожего типа товара
    best_match = None
    best_score = 0
    for type in contr_type:
        score = fuzz.ratio(last_section, type)
        if score > best_score:
            best_score = score
            best_match = type

    # Вывод результата, если точность > 85%
    if best_score > 85:
        return f"{last_section} - {best_match} (accuracy: {best_score}%)"
    else:
        return f"{last_section} - ! Не найдено подходящего типа товара"
    
    # accuracy 85% даёт результаты необходимой точности
    # Однако, этот алгоритм не всесилен. Т.к. например для товара 
    # Губки для шлифования он найдёт наиболее подходящую категорию:
    # Губки для шлифования - Губка для рисования (accuracy: 82%)

    # По этому, такие значения нужно будет отловить, и потом уже обрботать в ручном режиме

# Пример использования
# section_example = "Режущий инструмент/Приспособления для шлифования/Губки для шлифования"
section_example = "Отделочный инструмент/Средства индивидуальной защиты/Щитки защитные"
print(classify_product(section_example))
