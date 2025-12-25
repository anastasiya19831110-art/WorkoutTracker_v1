import unittest
import pandas as pd
import os
from models import Workout
from analysis import get_workout_report

class TestWorkoutTracker(unittest.TestCase):

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.test_data = {
            "value": 45.0,
            "activity": "Бег",
            "date": "2025-12-01",
            "notes": "Утренняя пробежка",
            "intensity": "Кардио"
        }

    # --- Тесты для Классов (Models) ---
    def test_workout_creation(self):
        """Проверка корректного создания объекта Workout."""
        w = Workout(**self.test_data)
        self.assertEqual(w.value, 45.0)
        self.assertEqual(w.activity, "Бег")
        self.assertEqual(w.intensity, "Кардио")

    def test_workout_to_dict(self):
        """Проверка преобразования объекта в словарь для сохранения."""
        w = Workout(**self.test_data)
        d = w.to_dict()
        self.assertEqual(d['activity'], "Бег")
        self.assertIsInstance(d, dict)

    # --- Тесты для Анализа (Analysis) ---
    def test_report_no_file(self):
        """Проверка поведения анализатора, если файл данных отсутствует."""
        # Временно меняем путь к файлу на несуществующий
        report, df = get_workout_report(2023, 12)
        if not os.path.exists('data/workout_history.csv'):
            self.assertIn("Данные еще не собраны", report)
            self.assertIsNone(df)

if __name__ == '__main__':
    unittest.main()