import pandas as pd
import matplotlib.pyplot as plt
import os

# Указываем путь к данным
CSV_FILE = os.path.join('data', 'workout_history.csv')

def get_workout_report(year, month):
    """Генерирует текстовый отчет и фильтрует DataFrame за указанный период с помощью Pandas."""
    if not os.path.exists(CSV_FILE):
        return "Данные еще не собраны. Добавьте первую тренировку!", None

    # Читаем CSV из папки data
    df = pd.read_csv(CSV_FILE)

    # Преобразуем дату в формат datetime для Pandas
    df['date'] = pd.to_datetime(df['date'])

    # Фильтруем данные по году и месяцу
    filtered_df = df[(df['date'].dt.year == year) & (df['date'].dt.month == month)]

    if filtered_df.empty:
        return f"За {month:02d}.{year} тренировок не найдено.", None

    # Считаем статистику
    total_minutes = filtered_df['value'].sum()
    avg_minutes = filtered_df['value'].mean()
    workout_count = len(filtered_df)

    # Группируем по виду активности
    activity_stats = filtered_df.groupby('activity')['value'].sum()

    report = (
        f"--- Отчет за {month:02d}.{year} ---\n"
        f"Всего тренировок: {workout_count}\n"
        f"Общее время: {total_minutes:.1f} мин.\n"
        f"Средняя длительность: {avg_minutes:.1f} мин.\n\n"
        f"Распределение по видам:\n{activity_stats.to_string()}"
    )

    return report, filtered_df


def show_workout_chart(df):
    """Построение графика активности."""
    activity_totals = df.groupby('activity')['value'].sum()

    plt.figure(figsize=(8, 5))
    activity_totals.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Общее время по видам спорта (мин)")
    plt.xlabel("Вид активности")
    plt.ylabel("Минуты")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()