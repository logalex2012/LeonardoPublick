import pandas as pd
import os

# Путь к файлу
input_file = 'static/Финалисты Московский фестиваль творческих открытий и инициатив Леонардо 2026 Средние и старшие классы.xlsx'
output_file = 'static/data.csv'

def convert_excel_to_csv():
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден.")
        return

    df = pd.read_excel(input_file)
    
    # Подготовка списка для новых данных
    new_data = []
    current_type = "Общий" # Значение по умолчанию
    
    # Итерируемся по строкам DataFrame
    for index, row in df.iterrows():
        fio = row['ФИ участника']
        title = row['Название работы']
        school = row['Образовательное учреждение']
        grade = row['Класс']
        teacher = row['ФИО руководителя']
        
        # Проверка на строку-заголовок секции
        # Если ФИО есть, а Названия работы нет (NaN), считаем это заголовком секции
        if pd.notna(fio) and pd.isna(title):
            current_type = str(fio).strip()
            continue
            
        # Если это строка с данными (есть и ФИО и Название)
        if pd.notna(fio) and pd.notna(title):
            new_data.append({
                'ФИ участника': str(fio).strip(),
                'Название работы': str(title).strip(),
                'Образовательное учреждение': str(school).strip() if pd.notna(school) else "",
                'Класс': str(grade).strip() if pd.notna(grade) else "",
                'ФИО руководителя': str(teacher).strip() if pd.notna(teacher) else "",
                'Тип проекта': current_type
            })
            
    # Создаем новый DataFrame
    new_df = pd.DataFrame(new_data)
    
    # Сохраняем в CSV без индекса
    new_df.to_csv(output_file, index=False, header=False) # header=False чтобы не было строки заголовков, если скрипты ожидают чистые данные или сами пропускают первую строку
    # Но стоп, скрипты обычно делают `const [header, ...rows] = lines;`. Значит заголовок НУЖЕН.
    
    new_df.to_csv(output_file, index=False, header=True)
    print(f"Конвертация завершена. Файл сохранен в {output_file}")
    print(f"Всего записей: {len(new_df)}")

if __name__ == "__main__":
    convert_excel_to_csv()