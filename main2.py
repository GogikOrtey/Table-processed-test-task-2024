import pandas as pd
from fuzzywuzzy import fuzz

# Далее я решил масштабировать этот алгоритм, и обработать все строки из исходной таблицы "Данные поставщика"
# Но для начала ограничился 20 записями

# Программа делает копию таблицы, и создаёт в ней 2 дополнительных столбца - Тип товара и Точность распознавания
# 2й из них может быть полезен нам для дальшейшей отладки и проверки результатов

# Затем, программа построчно обрабатывает данные алгоритмом, описанном в файле main1.py
# и сохраняет результаты в нужные ячейки

# Шаг 1: Загрузка таблицы "Дерево категорий.xlsx"
df_tree = pd.read_excel("data/Дерево категорий.xlsx")
contr_type = df_tree["Тип товара"].tolist()

# Функция для классификации продукта
def classify_product(section):
    last_section = section.split('/')[-1]  # Извлечение последнего значения из поля "Раздел"
    best_match = None
    best_score = 0
    for type in contr_type:
        score = fuzz.ratio(last_section, type)
        if score > best_score:
            best_score = score
            best_match = type
    return best_match, best_score

# Шаг 2: Загрузка таблицы "Данные поставщика.xlsx"
df_supplier = pd.read_excel("data/Данные поставщика.xlsx")

# Создание копии с первыми 20 строками
count_str = 20
df_supplier_copy = df_supplier.head(count_str).copy()

# Добавление новых столбцов
df_supplier_copy.insert(2, "Тип товара", "")
df_supplier_copy.insert(3, "Точность распознавания", "")

# Шаг 3: Обработка данных и заполнение столбцов
inp_data_mass = df_supplier_copy["Раздел"].apply(lambda x: x.split('/')[-1]).tolist()
outp_type = []
acc_type = []

for section in inp_data_mass:
    product_type, accuracy = classify_product(section)
    outp_type.append(product_type)
    acc_type.append(accuracy)

df_supplier_copy["Тип товара"] = outp_type
df_supplier_copy["Точность распознавания"] = acc_type

# Шаг 4: Сохранение обновленной таблицы
df_supplier_copy.to_excel("Данные поставщика дополненные.xlsx", index=False)


print("Программа успешно завершила свою работу")
print(f"Было обработано {count_str} строк")


# Эта программа требовательна к ресурсам вашего компьютера, 
# по этому скорее всего будет выполнятся достаточно долго, даже для малого количества строк



