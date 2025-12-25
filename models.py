class Workout:
    """Класс для представления тренировки и подготовки данных к сохранению."""
    def __init__(self, value, activity, date, notes, intensity):
        """Инициализация объекта тренировки."""
        self.value = value        # Длительность в минутах
        self.activity = activity  # Название (например, Бег)
        self.date = date          # Дата
        self.notes = notes        # Заметки
        self.intensity = intensity # Тип нагрузки (Кардио/Силовая)

    def to_dict(self):
        """Преобразует объект в словарь для удобного сохранения в CSV."""
        return {
            "value": self.value,
            "activity": self.activity,
            "date": self.date,
            "notes": self.notes,
            "intensity": self.intensity
        }

    def to_dict(self):
        """Преобразование в словарь для удобного сохранения в CSV."""
        return {
            "value": self.value,
            "activity": self.activity,
            "date": self.date,
            "notes": self.notes,
            "intensity": self.intensity
        }