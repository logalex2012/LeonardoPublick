import pandas as pd
import csv
import os

# 1. Загружаем данные из Excel
excel_file = 'static/Финалисты Московский фестиваль творческих открытий и инициатив Леонардо 2026 Средние и старшие классы.xlsx'
df = pd.read_excel(excel_file)

# Создаем словарь для быстрого поиска по ФИО
# Формат: {'ФИО': {'school': '...', 'grade': '...', 'teacher': '...'}}
excel_data = {}

for index, row in df.iterrows():
    fio = str(row['ФИ участника']).strip()
    if pd.notna(fio) and fio != 'nan':
        # Нормализуем ФИО (в нижний регистр, убираем лишние пробелы) для надежного поиска
        fio_key = ' '.join(fio.lower().split())
        excel_data[fio_key] = {
            'school': str(row['Образовательное учреждение']).strip() if pd.notna(row['Образовательное учреждение']) else "",
            'grade': str(row['Класс']).strip() if pd.notna(row['Класс']) else "",
            'teacher': str(row['ФИО руководителя']).strip() if pd.notna(row['ФИО руководителя']) else ""
        }

# 2. Читаем текущий data.csv (который мы сгенерировали из docx)
csv_file = 'static/data.csv'
merged_entries = []

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader) # Пропускаем заголовок
    
    for row in reader:
        if len(row) >= 7:
            fio = row[0]
            title = row[1]
            # row[2] - school, row[3] - grade, row[4] - teacher
            sec_type = row[5]
            cabinet = row[6]
            
            # Ищем в Excel
            fio_key = ' '.join(fio.lower().split())
            
            school = ""
            grade = ""
            teacher = ""
            
            # Пробуем найти точное совпадение
            if fio_key in excel_data:
                school = excel_data[fio_key]['school']
                grade = excel_data[fio_key]['grade']
                teacher = excel_data[fio_key]['teacher']
            else:
                # Пробуем найти частичное совпадение (если в docx перепутаны имя и фамилия)
                parts = fio_key.split()
                if len(parts) == 2:
                    reversed_key = f"{parts[1]} {parts[0]}"
                    if reversed_key in excel_data:
                        school = excel_data[reversed_key]['school']
                        grade = excel_data[reversed_key]['grade']
                        teacher = excel_data[reversed_key]['teacher']
            
            # Если в Excel было 'nan', делаем пустую строку
            if school == 'nan': school = ''
            if grade == 'nan': grade = ''
            if teacher == 'nan': teacher = ''
            
            merged_entries.append([fio, title, school, grade, teacher, sec_type, cabinet])

# 3. Сохраняем обратно в CSV
with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ФИ участника', 'Название работы', 'Образовательное учреждение', 'Класс', 'ФИО руководителя', 'Тип проекта', 'Кабинет'])
    for e in merged_entries:
        writer.writerow(e)

print(f"Успешно объединено {len(merged_entries)} записей.")
