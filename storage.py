import csv
import os

# Указываем путь к папке и файлу
DATA_DIR = 'data'
CSV_FILE = os.path.join(DATA_DIR, 'workout_history.csv')


def save_workout(workouts):
    """Сохраняет список тренировок в CSV, создавая папку data при необходимости."""
    # Создаем папку data, если её еще нет
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        fieldnames = ["value", "activity", "date", "notes", "intensity"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for w in workouts:
            writer.writerow(w.to_dict())

def save_all_workouts(workout_list):
    """
    Полностью перезаписывает файл переданным списком словарей.
    Используется при удалении данных.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ["value", "activity", "date", "notes", "intensity"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for w_dict in workout_list:
            writer.writerow(w_dict)

def load_workouts():
    """Загружает тренировки из папки data."""
    workouts = []
    if not os.path.isfile(CSV_FILE):
        return workouts

    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            workouts.append(row)
    return workouts